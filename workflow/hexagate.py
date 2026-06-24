from skills_core.workflow import chainalysis_workflow
from aws_durable_execution_sdk_python import DurableContext

DEMO_PREFIX = "Compliance Cove demo |"


def _items(listing):
    data = listing.get("data", listing) if isinstance(listing, dict) else listing
    if isinstance(data, dict):
        return data.get("items", data.get("results", [])) or []
    return data or []


@chainalysis_workflow
def handler(event: dict, context: DurableContext) -> dict:
    """Compliance Cove, live Hexagate (Monitoring + Gate DSL).

    Requires Hexagate connected in Chainalysis Connections. Used by
    hexagate-demo.html via /api/workflow/cove-hexagate. The demo falls back
    to validated sample data if a call is unavailable.

    Modes:
      - gate_validate: validate Gate DSL against live on-chain data.
      - create_monitor: create a real Hexagate monitor (auto-cleans prior demo monitors).
      - list_monitors: list monitors in the org (slimmed).
      - list_events: events for a monitor (requires monitorId).
      - analyze_transaction: analyze a transaction for risk.
    """
    mode = (event.get("mode") or "gate_validate").strip()
    try:
        if mode == "gate_validate":
            from chainalysis_skill_hexagate.gate import GateClient
            r = GateClient().validate_gate(
                event.get("gate") or "",
                chain_id=int(event.get("chainId", 1)),
                trace=True,
                from_block=event.get("fromBlock"),
                to_block=event.get("toBlock"),
                params=event.get("params") or {},
            )
            trace = r.get("trace") or {}
            slim = {}
            for k, v in trace.items():
                if isinstance(v, list) and len(v) > 6:
                    slim[k] = {"_count": len(v), "_sample": v[:3]}
                else:
                    slim[k] = v
            failed = r.get("failed") or []
            return {
                "ok": True, "mode": mode, "trace": slim,
                "failed": failed, "exceptions": r.get("exceptions") or [],
                "fired": len(failed) > 0,
                "block": (failed[0][1] if failed else None),
            }

        if mode == "create_monitor":
            from chainalysis_skill_hexagate.monitoring import (
                MonitoringClient, AddressFundMovementMonitor,
                threshold_condition, address,
            )
            mc = MonitoringClient()
            chain = int(event.get("chainId", 1))
            name = event.get("name") or (DEMO_PREFIX + " monitor")
            # Keep the org clean: remove prior demo monitors before creating a new one
            try:
                for m in _items(mc.list_monitors()):
                    if (m.get("name") or "").startswith(DEMO_PREFIX) and m.get("id"):
                        try:
                            mc.delete_monitor(m["id"])
                        except Exception:
                            pass
            except Exception:
                pass
            res = mc.create_monitor(
                AddressFundMovementMonitor,
                name=name,
                addresses=[address(event.get("address"), chain)],
                severity=event.get("severity", "High"),
                conditions=[AddressFundMovementMonitor.condition(
                    threshold_condition("MoreThan", str(event.get("threshold", "100000"))),
                    direction=event.get("direction", "to"),
                )],
            )
            data = res.get("data") if isinstance(res, dict) else None
            mid = (data or {}).get("id") if isinstance(data, dict) else None
            return {"ok": True, "mode": mode, "monitorId": mid, "name": name,
                    "createdBy": (data or {}).get("created_by") if isinstance(data, dict) else None}

        if mode == "list_monitors":
            from chainalysis_skill_hexagate.monitoring import MonitoringClient
            raw = _items(MonitoringClient().list_monitors())
            out = []
            for m in raw[:40]:
                params = m.get("params") or {}
                ents = m.get("entities") or []
                addr = None
                if ents:
                    ep = ents[0].get("params") or {}
                    addr = ep.get("address")
                out.append({
                    "id": m.get("id"),
                    "name": m.get("name"),
                    "type": params.get("type") or m.get("monitor_id"),
                    "severity": params.get("severity"),
                    "disabled": m.get("disabled"),
                    "createdBy": m.get("created_by"),
                    "entities": len(ents),
                    "address": addr,
                })
            return {"ok": True, "mode": mode, "count": len(raw), "monitors": out}

        if mode == "list_events":
            from chainalysis_skill_hexagate.monitoring import MonitoringClient
            return {"ok": True, "mode": mode,
                    "result": MonitoringClient().list_events(event.get("monitorId"))}

        if mode == "analyze_address":
            from chainalysis_skill_hexagate import HexagateClient
            r = HexagateClient().analyze_address(
                event.get("address"),
                blockchain=event.get("blockchain", "ethereum"),
                chain=event.get("chain", "mainnet"),
            )
            issues = [{"type": i.get("type"), "risk_level": i.get("risk_level")}
                      for i in (r.get("security_issues") or []) if i.get("result")]
            age = None
            for i in (r.get("security_issues") or []):
                ed = i.get("extra_details") or {}
                if isinstance(ed, dict) and ed.get("age_of_contract"):
                    age = ed.get("age_of_contract")
                    break
            return {"ok": True, "mode": mode, "risk_level": r.get("risk_level"),
                    "type": r.get("type"), "name": r.get("name"), "age": age,
                    "issues": issues, "checks": len(r.get("security_issues") or [])}

        if mode == "analyze_transaction":
            from chainalysis_skill_hexagate import HexagateClient
            return {"ok": True, "mode": mode,
                    "result": HexagateClient().analyze_transaction(event.get("transaction") or {})}

        return {"ok": False, "error": f"unknown mode {mode}"}
    except Exception as e:
        return {"ok": False, "error": str(e)}
