from skills_core.workflow import chainalysis_workflow
from aws_durable_execution_sdk_python import DurableContext


# Pre-built investigation scenarios with real addresses.
# Each scenario has a name and a list of nodes to add to the graph.
# Nodes are positioned left-to-right to visually show the fund flow.
SCENARIOS = {
    "theft": {
        "name": "CG-2026-0847: Wallet Compromise Investigation (158 ETH)",
        "nodes": [
            {"addr": "76fbb69ff6e3ec366671da195e58733d44225640", "label": "First Hop (from Coinbase victim)"},
            {"addr": "4c6f7ae61fa1ecd509189dce0ff33629b9d94c29", "label": "Swap via Paraswap (ETH to USDC)"},
            {"addr": "eefb36c4458da7798742cf038c5c27e07ab9c51e", "label": "Consolidation Wallet"},
            {"addr": "9b2a3b92b1d869384f6a51e104f9e49fba6a6d09", "label": "Scammer Main Wallet"},
            {"addr": "fada7810576254bed369065f988b6377a97fc7f1", "label": "Suspected Secondary Wallet"},
            {"addr": "678a902df7ac39a1e1bafe594f0e053097bf811c", "label": "Backpack.Exchange Deposit"},
        ],
    },
    "exploit": {
        "name": "CG-2026-0812: DeFi Protocol Exploit Investigation",
        "nodes": [
            {"addr": "eefb36c4458da7798742cf038c5c27e07ab9c51e", "label": "Exploit Consolidation"},
            {"addr": "9b2a3b92b1d869384f6a51e104f9e49fba6a6d09", "label": "Attacker Wallet"},
            {"addr": "fada7810576254bed369065f988b6377a97fc7f1", "label": "Layering Wallet"},
        ],
    },
}


@chainalysis_workflow
def handler(event: dict, context: DurableContext) -> dict:
    """Build a multi-node Reactor investigation graph for an insurance claim.

    Creates a persistent graph with cluster nodes laid out left-to-right
    to visualize the fund flow. Used by insurance-demo.html.

    Input:
      - scenario: key from SCENARIOS (e.g. "theft", "exploit")
      - OR addresses: [{addr, label?}] for a custom graph
      - name: optional graph name override
    """
    from chainalysis_skill_graph import GraphClient, add_cluster, add_annotation
    from chainalysis_skill_graph.commands import Network

    scenario_key = event.get("scenario", "")
    custom_addrs = event.get("addresses", [])
    name_override = event.get("name", "")

    # Determine which nodes to add
    if scenario_key and scenario_key in SCENARIOS:
        sc = SCENARIOS[scenario_key]
        nodes = sc["nodes"]
        graph_name = name_override or sc["name"]
    elif custom_addrs:
        nodes = custom_addrs
        graph_name = name_override or "Insurance Claim Investigation"
    else:
        return {"ok": False, "error": "Provide scenario or addresses"}

    try:
        client = GraphClient()
        result = client.create_graph(graph_name)
        graph_id = result["graph"]["id"]

        commands = []
        spacing = 35
        for i, node in enumerate(nodes):
            addr = node.get("addr", "").lower().replace("0x", "")
            if not addr:
                continue
            # Stagger y position slightly for visual variety
            y = (i % 2) * 12
            cmd = add_cluster(
                graph_id,
                Network.ETHEREUM_MAINNET,
                addr,
                {"x": i * spacing, "y": y},
            )
            commands.append(cmd)

        # Add an annotation with the investigation context
        ann = add_annotation(
            graph_id,
            graph_name,
            {"x": 0, "y": -20},
        )
        commands.append(ann)

        client.execute_commands(graph_id, commands)

        graph_url = f"https://reactor.chainalysis.com/graph-v2/{graph_id}"
        return {
            "ok": True,
            "graphId": graph_id,
            "graphUrl": graph_url,
            "nodes": len(nodes),
            "scenario": scenario_key or "custom",
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}
