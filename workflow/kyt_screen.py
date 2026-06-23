from skills_core.workflow import chainalysis_workflow
from aws_durable_execution_sdk_python import DurableContext


@chainalysis_workflow
def handler(event: dict, context: DurableContext) -> dict:
    """Compliance Cove — live KYT screening.

    Supports two shapes:
      - mode="transfer":  monitor a real on-chain transfer (deposit/withdrawal).
          requires transferReference ("txhash:address"), direction.
      - mode="withdrawal": pre-screen an outgoing withdrawal by destination address.
          requires address (assetAmount/attemptTimestamp optional).

    Everything is namespaced under a single demo user in the shared KYT org,
    with idempotent identifiers so repeated runs reuse the same records.
    """
    import time
    from datetime import datetime, timezone
    from chainalysis_skill_kyt import KYTClient

    user = (event.get("userId") or "compliance-cove-demo").strip()
    mode = (event.get("mode") or "transfer").strip()
    network = (event.get("network") or "ETHEREUM").strip()
    asset = (event.get("asset") or "ETH").strip()

    client = KYTClient()

    # Ensure the demo user exists (idempotent)
    try:
        client.create_user(user, properties={"active": True, "country": "US"})
    except Exception:
        pass

    try:
        if mode == "withdrawal":
            address = (event.get("address") or "").strip()
            if not address:
                return {"ok": False, "error": "No address provided"}
            ts = event.get("attemptTimestamp") or datetime.now(timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%S.000Z"
            )
            attempt = {
                "network": network,
                "asset": asset,
                "address": address,
                "attemptIdentifier": event.get("attemptIdentifier")
                or ("cove-wd-" + address[:12]),
                "assetAmount": event.get("assetAmount", 1),
                "attemptTimestamp": ts,
            }
            reg = client.register_withdrawal_attempt(user, attempt)
            ext = reg["externalId"]
            get_summary = client.get_withdrawal_attempt
            get_alerts = client.get_withdrawal_attempt_alerts
            subject = address
        else:
            ref = (event.get("transferReference") or "").strip()
            if not ref:
                return {"ok": False, "error": "No transferReference provided"}
            transfer = {
                "network": network,
                "asset": asset,
                "direction": event.get("direction", "received"),
                "transferReference": ref,
            }
            reg = client.register_transfer(user, transfer)
            ext = reg["externalId"]
            get_summary = client.get_transfer
            get_alerts = client.get_transfer_alerts
            subject = ref

        # Poll until processed (bounded)
        summary = {}
        for _ in range(16):
            summary = get_summary(ext)
            if summary.get("updatedAt"):
                break
            time.sleep(2)

        alerts_raw = []
        try:
            alerts_raw = get_alerts(ext).get("alerts", []) or []
        except Exception:
            pass

        alerts = []
        for a in alerts_raw:
            alerts.append({
                "level": a.get("alertLevel"),
                "service": a.get("service"),
                "exposureType": a.get("exposureType"),
                "category": a.get("categoryId"),
                "amount": a.get("alertAmount"),
                "alertId": a.get("externalId"),
            })

        order = {"SEVERE": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}
        top = max(alerts, key=lambda a: order.get(a.get("level"), 0)) if alerts else None
        level = top["level"] if top else "CLEARED"

        # KYT alert (filtered to this alert) + Reactor graph of the alert
        alert_link = "https://kyt.chainalysis.com/alerts"
        graph_link = None
        if top and top.get("alertId"):
            graph_link = "https://kyt.chainalysis.com/alerts/graph-v2?alertIds=" + top["alertId"]
            alert_link = "https://kyt.chainalysis.com/alerts/" + top["alertId"]

        return {
            "ok": True,
            "mode": mode,
            "externalId": ext,
            "subject": subject,
            "processed": bool(summary.get("updatedAt")),
            "usdAmount": summary.get("usdAmount"),
            "asset": summary.get("asset", asset),
            "network": network,
            "level": level,
            "alertCount": len(alerts),
            "alerts": sorted(alerts, key=lambda a: order.get(a.get("level"), 0), reverse=True),
            "alertLink": alert_link,
            "graphLink": graph_link,
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}
