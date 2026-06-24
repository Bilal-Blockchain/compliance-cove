from skills_core.workflow import chainalysis_workflow
from aws_durable_execution_sdk_python import DurableContext


# Real addresses traced from a verified scam network (root tx
# 0x53717bed...bf5e: victim withdrew from Coinbase, funds laundered and
# cashed out at multiple exchanges). Each scenario ends at a NAMED exchange
# cluster so the cashout point is unmistakable.
#
# Named exchange cluster IDs (render as "Backpack.Exchange" etc. in Reactor):
#   Backpack.Exchange : 0x2228e5704b637131a3798a186caf18366c146f74
#   LBank.com         : 0x120051a72966950b8ce12eb5496b5d1eeec1541b
#   VALR.com          : 0x05cdb1526f6e224e02919a4c018d9784ea25eb3d
SCENARIOS = {
    "theft": {
        "name": "CG-2026-0847: 158 ETH Scam (Coinbase victim to Backpack cashout)",
        "nodes": [
            {"addr": "76fbb69ff6e3ec366671da195e58733d44225640"},      # first hop
            {"addr": "4c6f7ae61fa1ecd509189dce0ff33629b9d94c29"},      # Paraswap swap
            {"addr": "eefb36c4458da7798742cf038c5c27e07ab9c51e"},      # consolidation
            {"addr": "9b2a3b92b1d869384f6a51e104f9e49fba6a6d09"},      # scammer main
            {"addr": "2228e5704b637131a3798a186caf18366c146f74"},      # Backpack.Exchange (named)
        ],
        "edges": [
            {"from": 0, "to": 1, "label": "158 ETH ($233K)"},
            {"from": 1, "to": 2, "label": "$399K USDC (swapped via Paraswap)"},
            {"from": 2, "to": 3, "label": "$12K USDC batches"},
            {"from": 3, "to": 4, "label": "$46K cashout at Backpack"},
        ],
    },
    "lbank": {
        "name": "CG-2026-0812: Laundering Branch (cashout at LBank.com)",
        "nodes": [
            {"addr": "eefb36c4458da7798742cf038c5c27e07ab9c51e"},      # consolidation
            {"addr": "9b2a3b92b1d869384f6a51e104f9e49fba6a6d09"},      # scammer main
            {"addr": "fada7810576254bed369065f988b6377a97fc7f1"},      # secondary wallet
            {"addr": "120051a72966950b8ce12eb5496b5d1eeec1541b"},      # LBank.com (named)
        ],
        "edges": [
            {"from": 0, "to": 1, "label": "$12K USDC batches"},
            {"from": 1, "to": 2, "label": "Multiple tokens"},
            {"from": 2, "to": 3, "label": "$23K cashout at LBank"},
        ],
    },
    "valr": {
        "name": "CG-2026-0756: Connected Wallet (cashout at VALR.com)",
        "nodes": [
            {"addr": "eefb36c4458da7798742cf038c5c27e07ab9c51e"},      # consolidation
            {"addr": "fada773a097b62d8fb08cf56811edbfff7ea230d"},      # VALR cashout wallet
            {"addr": "05cdb1526f6e224e02919a4c018d9784ea25eb3d"},      # VALR.com (named)
        ],
        "edges": [
            {"from": 0, "to": 1, "label": "Layered funds"},
            {"from": 1, "to": 2, "label": "$88K ETH cashout at VALR"},
        ],
    },
}


@chainalysis_workflow
def handler(event: dict, context: DurableContext) -> dict:
    """Build a multi-node Reactor investigation graph with labeled flow edges.

    Each scenario lays cluster nodes left-to-right and draws annotation edges
    showing the fund movement, ending at a NAMED exchange cluster (the cashout).
    Used by insurance-demo.html.

    Input:
      - scenario: "theft" | "lbank" | "valr"
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

        # Phase 1: cluster nodes laid out left-to-right with slight stagger
        node_commands = []
        for i, node in enumerate(nodes):
            addr = node["addr"].lower().replace("0x", "")
            y = (i % 2) * 15
            node_commands.append(
                add_cluster(
                    graph_id,
                    Network.ETHEREUM_MAINNET,
                    addr,
                    {"x": i * 40, "y": y},
                )
            )
        node_commands.append(
            add_annotation(graph_id, graph_name, {"x": 0, "y": -25})
        )
        client.execute_commands(graph_id, node_commands)

        # Phase 2: labeled flow edges between nodes
        if edges:
            edge_commands = []
            for edge in edges:
                s, d = edge["from"], edge["to"]
                if s < len(node_commands) and d < len(node_commands):
                    edge_commands.append(
                        add_annotation_edge(
                            graph_id,
                            node_commands[s]["id"],
                            node_commands[d]["id"],
                            label=edge.get("label", ""),
                            pointer="SOURCE",
                        )
                    )
            if edge_commands:
                client.execute_commands(graph_id, edge_commands)

        return {
            "ok": True,
            "graphId": graph_id,
            "graphUrl": f"https://reactor.chainalysis.com/graph-v2/{graph_id}",
            "nodes": len(nodes),
            "edges": len(edges),
            "scenario": scenario_key,
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}
