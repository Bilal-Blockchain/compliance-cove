from skills_core.workflow import chainalysis_workflow
from aws_durable_execution_sdk_python import DurableContext

# Stablecoin contracts (Ethereum mainnet) mapped to Data Solutions asset_ids.
STABLES = {
    "USDC": "eip155:1:a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
    "USDT": "eip155:1:dac17f958d2ee523a2206206994597c13d831ec7",
    "PYUSD": "eip155:1:6c3ea9036406852006290770bedfcaba0e23a0e8",
    "DAI": "eip155:1:6b175474e89094c44da98b954eedeac495271d0f",
    "USDe": "eip155:1:4c9edd5852cd905f086c759e8383e09bff1e68b3",
}

# Risk categories grouped for the risk-profile summary.
RISK_GROUPS = {
    "sanctions": [
        "sanctioned entity",
        "sanctioned jurisdiction",
        "special measures",
    ],
    "mixer": ["mixing"],
    "darknet": ["darknet market", "drug vendor"],
    "illicit": [
        "ransomware",
        "scam",
        "stolen funds",
        "fraud shop",
        "malware",
        "child abuse material",
        "terrorist financing",
    ],
    "gambling": ["gambling"],
    "no_kyc": ["no kyc exchange"],
}


def _addr_to_asset_id(addr: str) -> str:
    """Convert a 0x contract address to a Data Solutions asset_id."""
    return "eip155:1:" + addr.lower().replace("0x", "")


def _risk_profiles(client, days: int) -> dict:
    """Return risk-percentage profiles for all tracked stablecoins."""
    id_list = ",".join(f"'{v}'" for v in STABLES.values())

    cases = []
    for key, cats in RISK_GROUPS.items():
        cat_list = ",".join(f"'{c}'" for c in cats)
        cases.append(
            f"SUM(CASE WHEN sender_category IN ({cat_list}) "
            f"OR receiver_category IN ({cat_list}) "
            f"THEN amount_usd ELSE 0 END) AS `{key}_usd`"
        )
    case_sql = ",\n  ".join(cases)

    sql = f"""
SELECT
  asset_symbol,
  COUNT(*) AS `transfer_count`,
  SUM(amount_usd) AS `total_volume_usd`,
  {case_sql}
FROM ethereum.transfers_clustered
WHERE asset_id IN ({id_list})
  AND transaction_timestamp >= DATE_SUB(CURRENT_DATE(), {int(days)})
  AND transaction_timestamp < CURRENT_DATE()
GROUP BY asset_symbol
ORDER BY total_volume_usd DESC
"""
    result = client.query(sql)
    if result.get("status") != "success":
        return {"ok": False, "error": "query failed", "detail": str(result)}

    profiles = []
    for row in result.get("results", []):
        total = row["total_volume_usd"] or 1
        profile = {
            "symbol": row["asset_symbol"],
            "volume_usd": total,
            "transfers": row["transfer_count"],
        }
        for key in RISK_GROUPS:
            v = row.get(f"{key}_usd", 0) or 0
            profile[f"{key}_pct"] = round(v / total * 100, 4)
            profile[f"{key}_usd"] = v
        risky_total = sum(row.get(f"{k}_usd", 0) or 0 for k in RISK_GROUPS)
        profile["risky_pct"] = round(risky_total / total * 100, 4)
        profile["risk_level"] = (
            "High"
            if profile["risky_pct"] > 1
            else "Medium" if profile["risky_pct"] > 0.1 else "Low"
        )
        profiles.append(profile)

    return {"ok": True, "mode": "risk_profiles", "days": days, "profiles": profiles}


def _token_exposure(client, address: str, symbol: str, days: int) -> dict:
    """Return a detailed category breakdown for a single token."""
    if address:
        asset_id = _addr_to_asset_id(address)
    elif symbol and symbol.upper() in STABLES:
        asset_id = STABLES[symbol.upper()]
    else:
        return {"ok": False, "error": "provide address or symbol"}

    sql = f"""
SELECT
  COALESCE(sender_category, 'unidentified') AS `category`,
  SUM(amount_usd) AS `volume_usd`,
  COUNT(*) AS `transfer_count`
FROM ethereum.transfers_clustered
WHERE asset_id = '{asset_id}'
  AND transaction_timestamp >= DATE_SUB(CURRENT_DATE(), {int(days)})
  AND transaction_timestamp < CURRENT_DATE()
GROUP BY sender_category
HAVING SUM(amount_usd) > 0
ORDER BY volume_usd DESC
LIMIT 20
"""
    result = client.query(sql)
    if result.get("status") != "success":
        return {"ok": False, "error": "query failed"}

    categories = []
    total = sum((r["volume_usd"] or 0) for r in result.get("results", []))
    for row in result.get("results", []):
        v = row["volume_usd"] or 0
        categories.append(
            {
                "category": row["category"],
                "volume_usd": v,
                "transfers": row["transfer_count"],
                "pct": round(v / total * 100, 2) if total else 0,
            }
        )

    return {
        "ok": True,
        "mode": "token_exposure",
        "asset_id": asset_id,
        "days": days,
        "total_volume_usd": total,
        "categories": categories,
    }


@chainalysis_workflow
def handler(event: dict, context: DurableContext) -> dict:
    """Compliance Cove: Token intelligence via Data Solutions.

    Powers trading-firm-demo.html. Queries ethereum.transfers_clustered to
    compute per-token risk exposure by category.

    Modes:
      - risk_profiles: Risk percentages for all tracked stablecoins (7d window).
        Input: {mode: "risk_profiles", days?: 7}
      - token_exposure: Full category breakdown for a single token.
        Input: {mode: "token_exposure", address?: "0x...", symbol?: "USDC", days?: 7}
    """
    mode = (event.get("mode") or "risk_profiles").strip()
    days = int(event.get("days", 7))

    try:
        from chainalysis_skill_data_solutions import DataSolutionsClient

        client = DataSolutionsClient()

        if mode == "risk_profiles":
            return _risk_profiles(client, days)
        elif mode == "token_exposure":
            return _token_exposure(
                client, event.get("address", ""), event.get("symbol", ""), days
            )
        else:
            return {"ok": False, "error": f"unknown mode: {mode}"}
    except Exception as e:
        return {"ok": False, "error": str(e)}
