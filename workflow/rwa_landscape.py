from skills_core.workflow import chainalysis_workflow
from aws_durable_execution_sdk_python import DurableContext

# Tokenized RWA / securities tokens on Ethereum mainnet -> Data Solutions asset_ids.
RWA = {
    "USDY": {"id": "eip155:1:96f6ef951840721adbf46ac996b59e0235cb985c", "issuer": "Ondo Finance", "kind": "Tokenized US Dollar Yield"},
    "BUIDL": {"id": "eip155:1:7712c34205737192402172409a8f7ccef8aa2aec", "issuer": "BlackRock / Securitize", "kind": "Tokenized Treasury Fund"},
    "OUSG": {"id": "eip155:1:1b19c19393e2d034d8ff31ff34c81252fcbbee92", "issuer": "Ondo Finance", "kind": "Tokenized Short-Term Treasuries"},
    "USYC": {"id": "eip155:1:136471a34f6ef19fe571effc1ca711fdb8e49f2b", "issuer": "Hashnote / Circle", "kind": "Tokenized US Treasury Yield"},
    "USTB": {"id": "eip155:1:43415eb6ff9db7e26a15b704e7a3edce97d31c4e", "issuer": "Superstate", "kind": "Tokenized Short-Duration Treasuries"},
    "PAXG": {"id": "eip155:1:45804880de22913dafe09f4980848ece6ecbaf78", "issuer": "Paxos", "kind": "Tokenized Gold"},
    "XAUT": {"id": "eip155:1:68749665ff8d2d112fa859aa293f07a622782f38", "issuer": "Tether", "kind": "Tokenized Gold"},
}

RISKY = ["scam", "sanctioned entity", "sanctioned jurisdiction", "special measures",
         "mixing", "darknet market", "ransomware", "stolen funds", "fraud shop",
         "terrorist financing", "no kyc exchange"]


def _addr_to_asset_id(addr: str) -> str:
    return "eip155:1:" + addr.lower().replace("0x", "")


def _landscape(client, days: int) -> dict:
    id_list = ",".join(f"'{v['id']}'" for v in RWA.values())
    sql = f"""
SELECT asset_symbol,
  COUNT(*) AS `transfers`,
  ROUND(SUM(amount_usd)) AS `volume_usd`,
  COUNT(DISTINCT receiver_cluster_id) AS `holders`,
  COUNT(DISTINCT sender_cluster_id) AS `senders`,
  ROUND(SUM(CASE WHEN receiver_category IN ({",".join(f"'{c}'" for c in RISKY)})
    THEN amount_usd ELSE 0 END)) AS `risky_usd`
FROM ethereum.transfers_clustered
WHERE asset_id IN ({id_list})
  AND transaction_timestamp >= DATE_SUB(CURRENT_DATE(), {int(days)})
GROUP BY asset_symbol
ORDER BY volume_usd DESC
"""
    res = client.query(sql)
    if res.get("status") != "success":
        return {"ok": False, "error": "query failed", "detail": str(res)[:300]}
    tokens = []
    for row in res.get("results", []):
        sym = row["asset_symbol"]
        meta = RWA.get(sym, {})
        vol = row["volume_usd"] or 0
        risky = row["risky_usd"] or 0
        tokens.append({
            "symbol": sym,
            "issuer": meta.get("issuer", ""),
            "kind": meta.get("kind", ""),
            "volume_usd": vol,
            "transfers": row["transfers"],
            "holders": row["holders"],
            "senders": row["senders"],
            "risky_usd": risky,
            "risky_pct": round(risky / vol * 100, 4) if vol else 0,
        })
    return {"ok": True, "mode": "landscape", "days": days, "tokens": tokens}


def _token_holders(client, symbol: str, address: str, days: int) -> dict:
    if address:
        asset_id = _addr_to_asset_id(address)
    elif symbol and symbol.upper() in RWA:
        asset_id = RWA[symbol.upper()]["id"]
    else:
        return {"ok": False, "error": "provide symbol or address"}

    cat_sql = f"""
SELECT COALESCE(receiver_category,'unidentified') AS `category`,
  ROUND(SUM(amount_usd)) AS `volume_usd`, COUNT(*) AS `transfers`
FROM ethereum.transfers_clustered
WHERE asset_id = '{asset_id}' AND transaction_timestamp >= DATE_SUB(CURRENT_DATE(), {int(days)})
GROUP BY receiver_category HAVING SUM(amount_usd) > 0
ORDER BY volume_usd DESC LIMIT 15
"""
    name_sql = f"""
SELECT receiver_name AS `holder`, receiver_category AS `category`,
  ROUND(SUM(amount_usd)) AS `volume_usd`, COUNT(*) AS `transfers`
FROM ethereum.transfers_clustered
WHERE asset_id = '{asset_id}' AND transaction_timestamp >= DATE_SUB(CURRENT_DATE(), {int(days)})
  AND receiver_name IS NOT NULL
GROUP BY receiver_name, receiver_category
ORDER BY volume_usd DESC LIMIT 12
"""
    cats_r = client.query(cat_sql)
    names_r = client.query(name_sql)
    if cats_r.get("status") != "success" or names_r.get("status") != "success":
        return {"ok": False, "error": "query failed"}

    cats = cats_r.get("results", [])
    total = sum((r["volume_usd"] or 0) for r in cats)
    categories = [{
        "category": r["category"], "volume_usd": r["volume_usd"] or 0,
        "transfers": r["transfers"],
        "pct": round((r["volume_usd"] or 0) / total * 100, 2) if total else 0,
        "risky": r["category"] in RISKY,
    } for r in cats]
    holders = [{
        "holder": r["holder"], "category": r["category"] or "unidentified",
        "volume_usd": r["volume_usd"] or 0, "transfers": r["transfers"],
        "risky": (r["category"] or "") in RISKY,
    } for r in names_r.get("results", [])]

    return {"ok": True, "mode": "token_holders", "asset_id": asset_id,
            "symbol": symbol.upper() if symbol else "", "days": days,
            "total_volume_usd": total, "categories": categories, "holders": holders}


@chainalysis_workflow
def handler(event: dict, context: DurableContext) -> dict:
    """Compliance Cove: Tokenized securities / RWA landscape via Data Solutions.

    Powers rwa-demo.html (EquiChain). Queries ethereum.transfers_clustered for
    real on-chain RWA tokens (USDY, BUIDL, OUSG).

    Modes:
      - landscape: per-token volume, transfers, holders, risky exposure (365d default).
        Input: {mode: "landscape", days?: 365}
      - token_holders: counterparty category breakdown + top named holders for one token.
        Input: {mode: "token_holders", symbol?: "BUIDL", address?: "0x...", days?: 365}
    """
    mode = (event.get("mode") or "landscape").strip()
    days = int(event.get("days", 365))
    try:
        from chainalysis_skill_data_solutions import DataSolutionsClient
        client = DataSolutionsClient()
        if mode == "landscape":
            return _landscape(client, days)
        elif mode == "token_holders":
            return _token_holders(client, event.get("symbol", ""), event.get("address", ""), days)
        return {"ok": False, "error": f"unknown mode: {mode}"}
    except Exception as e:
        return {"ok": False, "error": str(e)}
