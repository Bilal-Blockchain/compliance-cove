from skills_core.workflow import chainalysis_workflow
from aws_durable_execution_sdk_python import DurableContext


@chainalysis_workflow
def handler(event: dict, context: DurableContext) -> dict:
    from chainalysis_skill_address_screening import AddressScreeningClient

    address = event.get("address", "").strip()
    if not address:
        return {"error": "No address provided"}

    client = AddressScreeningClient()

    try:
        result = client.get_risk_assessment(address)
    except Exception as e:
        return {"error": str(e)}

    # Build a clean response
    exposures = []
    for exp in result.get("exposures", []):
        exposures.append({
            "category": exp.get("category", "Unknown"),
            "value": exp.get("value", 0),
            "exposureType": exp.get("exposureType", "unknown"),
        })

    triggers = []
    for trig in result.get("triggers", []):
        triggers.append({
            "category": trig.get("category", "Unknown"),
            "percentage": trig.get("percentage", 0),
            "message": trig.get("message", ""),
            "riskLevel": trig.get("ruleTriggered", {}).get("risk", "Unknown") if trig.get("ruleTriggered") else None,
        })

    identifications = []
    for ident in result.get("addressIdentifications", []):
        identifications.append({
            "name": ident.get("name"),
            "category": ident.get("category", "Unknown"),
            "description": ident.get("description"),
        })

    cluster_info = None
    if result.get("cluster"):
        cluster_info = {
            "name": result["cluster"].get("name"),
            "category": result["cluster"].get("category"),
        }

    return {
        "address": result.get("address", address),
        "risk": result.get("risk", "Unknown"),
        "riskReason": result.get("riskReason"),
        "addressType": result.get("addressType"),
        "status": result.get("status"),
        "cluster": cluster_info,
        "identifications": identifications,
        "exposures": sorted(exposures, key=lambda x: x["value"], reverse=True),
        "triggers": triggers,
    }
