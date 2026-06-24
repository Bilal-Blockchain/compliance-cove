from skills_core.workflow import chainalysis_workflow
from aws_durable_execution_sdk_python import DurableContext


# Pre-built investigation scenarios with real addresses and flow edges.
# Each node has an address; each edge connects consecutive nodes with a label
# describing the fund movement.
SCENARIOS = {
    "theft": {
        "name": "CG-2026-0847: Wallet Compromise (158 ETH Stolen from Coinbase)",
        "nodes": [
            {"addr": "76fbb69ff6e3ec366671da195e58733d44225640"},
            {"addr": "4c6f7ae61fa1ecd509189dce0ff33629b9d94c29"},
            {"addr": "eefb36c4458da7798742cf038c5c27e07ab9c51e"},
            {"addr": "9b2a3b92b1d869384f6a51e104f9e49fba6a6d09"},
            {"addr": "fada7810576254bed369065f988b6377a97fc7f1"},
            {"addr": "678a902df7ac39a1e1bafe594f0e053097bf811c"},
        ],
        "edges": [
            {"from": 0, "to": 1, "label": "158 ETH ($233K)"},
            {"from": 1, "to": 2, "label": "$399K USDC (swapped via Paraswap)"},
            {"from": 2, "to": 3, "label": "$12K USDC batches"},
            {"from": 3, "to": 4, "label": "Multiple tokens"},
            {"from": 4, "to": 5, "label": "$99K cashout (Backpack)"},
            {"from": 3, "to": 5, "label": "$46K USDC direct"},
        ],
    },
    "laundering": {
        "name": "CG-2026-0812: Secondary Wallet Laundering Network",
        "nodes": [
            {"addr": "9b2a3b92b1d869384f6a51e104f9e49fba6a6d09"},
            {"addr": "fada7810576254bed369065f988b6377a97fc7f1"},
            {"addr": "678a902df7ac39a1e1bafe594f0e053097bf811c"},
        ],
        "edges": [
            {"from": 0, "to": 1, "label": "Tokens + ETH"},
            {"from": 1, "to": 2, "label": "$99K to Backpack.Exchange"},
            {"from": 0, "to": 2, "label": "$46K USDC direct"},
        ],
    },
    "takeover": {
        "name": "CG-2026-0756: Exchange Account Takeover (Connected to CG-0847)",
        "nodes": [
            {"addr": "eefb36c4458da7798742cf038c5c27e07ab9c51e"},
            {"addr": "9b2a3b92b1d869384f6a51e104f9e49fba6a6d09"},
            {"addr": "fada7810576254bed369065f988b6377a97fc7f1"},
            {"addr": "678a902df7ac39a1e1bafe594f0e053097bf811c"},
        ],
        "edges": [
            {"from": 0, "to": 1, "label": "$12K batches"},
            {"from": 1, "to": 2, "label": "Layering"},
            {"from": 2, "to": 3, "label": "$99K cashout"},
        ],
    },
}


@chainalysis_workflow
def handler(event: dict, context: DurableContext) -> dict:
    """Build a multi-node Reactor investigation graph with annotation edges.

    Creates a persistent graph with cluster nodes laid out left-to-right
    and labeled edges showing the fund flow between them.
    Used by insurance-demo.html.

    Input:
      - scenario: key from SCENARIOS ("theft", "laundering", "takeover")
    """
    from chainalysis_skill_graph import (
        GraphClient,
        add_cluster,
        add_annotation,
        add_annotation_edge,
    )
    from chainalysis_skill_graph.commands import Network

    scenario_key = event.get("scenario", "theft")

    if scenario_key not in SCENARIOS:
        return {"ok": False, "error": f"Unknown scenario: {scenario_key}"}

    sc = SCENARIOS[scenario_key]
    nodes = sc["nodes"]
    edges = sc.get("edges", [])
    graph_name = event.get("name") or sc["name"]

    try:
        client = GraphClient()
        result = client.create_graph(graph_name)
        graph_id = result["graph"]["id"]

        # Phase 1: add all cluster nodes, spaced left-to-right
        node_commands = []
        spacing_x = 40
        for i, node in enumerate(nodes):
            addr = node["addr"].lower().replace("0x", "")
            # Slight vertical stagger for readability
            y = (i % 2) * 15
            cmd = add_cluster(
                graph_id,
                Network.ETHEREUM_MAINNET,
                addr,
                {"x": i * spacing_x, "y": y},
            )
            node_commands.append(cmd)

        # Add a title annotation
        title_cmd = add_annotation(
            graph_id,
            graph_name,
            {"x": 0, "y": -25},
        )
        node_commands.append(title_cmd)

        client.execute_commands(graph_id, node_commands)

        # Phase 2: add annotation edges between nodes to show fund flow
        # We need the node IDs from the commands we just executed.
        # add_cluster returns a command dict with an "id" field.
        if edges:
            edge_commands = []
            for edge in edges:
                src_idx = edge["from"]
                dst_idx = edge["to"]
                label = edge.get("label", "")
                if src_idx < len(node_commands) and dst_idx < len(node_commands):
                    src_id = node_commands[src_idx]["id"]
                    dst_id = node_commands[dst_idx]["id"]
                    edge_cmd = add_annotation_edge(
                        graph_id,
                        src_id,
                        dst_id,
                        label=label,
                        pointer="SOURCE",
                    )
                    edge_commands.append(edge_cmd)
            if edge_commands:
                client.execute_commands(graph_id, edge_commands)

        graph_url = f"https://reactor.chainalysis.com/graph-v2/{graph_id}"
        return {
            "ok": True,
            "graphId": graph_id,
            "graphUrl": graph_url,
            "nodes": len(nodes),
            "edges": len(edges),
            "scenario": scenario_key,
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}
