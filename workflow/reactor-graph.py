from skills_core.workflow import chainalysis_workflow
from aws_durable_execution_sdk_python import DurableContext


@chainalysis_workflow
def handler(event: dict, context: DurableContext) -> dict:
    from chainalysis_skill_graph import GraphClient, add_cluster
    from chainalysis_skill_graph.commands import Network

    address = event.get("address", "").strip()
    if not address:
        return {"error": "No address provided"}

    network_str = event.get("network", "ETH").upper()

    # Map network string to Network enum
    network_map = {
        "ETH": Network.ETHEREUM_MAINNET,
        "BTC": Network.BITCOIN_MAINNET,
        "SOL": Network.SOLANA_MAINNET,
        "MATIC": Network.POLYGON_POS_MAINNET,
        "AVAX": Network.AVALANCHE_C_CHAIN_MAINNET,
        "ARB": Network.ARBITRUM_ONE_MAINNET,
        "BASE": Network.BASE_MAINNET,
        "BSC": Network.BNB_SMART_CHAIN_MAINNET,
        "TRON": Network.TRON_MAINNET,
    }
    network = network_map.get(network_str, Network.ETHEREUM_MAINNET)

    # Normalize address: strip 0x prefix and lowercase for EVM chains
    clean = address.lower()
    if clean.startswith("0x"):
        clean = clean[2:]

    client = GraphClient()

    try:
        # Create a named graph
        short = f"0x{clean[:6]}…{clean[-4:]}" if len(clean) > 10 else clean
        result = client.create_graph(f"Investigation — {short}")
        graph_id = result["graph"]["id"]

        # Add the address as a cluster node
        cmd = add_cluster(graph_id, network, clean, {"x": 0, "y": 0})
        client.execute_commands(graph_id, [cmd])

        graph_url = f"https://reactor.chainalysis.com/graph-v2/{graph_id}"

        return {
            "graphId": graph_id,
            "graphUrl": graph_url,
            "address": address,
            "network": network_str,
        }
    except Exception as e:
        return {"error": str(e)}
