from skills_core.workflow import chainalysis_workflow
from aws_durable_execution_sdk_python import DurableContext


# Real, publicly documented stolen-funds clusters traced via Chainalysis.
# Source nodes are NAMED stolen-funds clusters; final nodes are NAMED
# cashout exchanges, so both ends of the flow are unmistakable in Reactor.
#
# Cases:
#   ascendex : AscendEX.com exchange hack (Dec 2021, ~$80M) -> KuCoin.com
#   atomic   : Atomic Wallet hack (Jun 2023, ~$100M, Lazarus) -> HTX.com
#   alphapo  : AlphaPo.net hack (Jul 2023, Lazarus) -> Binance.com
SCENARIOS = {
    "ascendex": {
        "name": "CG-2026-0847: AscendEX Exchange Hack ($74M) - cashout at KuCoin",
        "nodes": [
            {"addr": "2c6900b24221de2b4a45c8c89482fff96ffb7e55"},  # AscendEX Stolen Funds (named)
            {"addr": "9eee6862b78fb6f9627d7d5a908d2114814fcecd"},  # laundering wallet
            {"addr": "03e6fa590cadcf15a38e86158e9b3d06ff3399ba"},  # KuCoin.com (named)
        ],
        "edges": [
            {"from": 0, "to": 1, "label": "$53.5M (primary laundering wallet)"},
            {"from": 1, "to": 2, "label": "$7.6M traced to KuCoin (indirect)"},
        ],
    },
    "atomic": {
        "name": "CG-2026-0812: Atomic Wallet Hack ($100M, Lazarus) - cashout at HTX",
        "nodes": [
            {"addr": "d29061b76101c5fa086694bd034a88e43594d30f"},  # Atomic Wallet Stolen Funds (named)
            {"addr": "7f691eba903423900b40a397d94f9062cae72dbf"},  # laundering wallet
            {"addr": "5910a9f4a27d3905b70372efa6f766ddc982e697"},  # HTX.com (named)
        ],
        "edges": [
            {"from": 0, "to": 1, "label": "$3.6M (laundering wallet)"},
            {"from": 1, "to": 2, "label": "$7.7M traced to HTX (indirect)"},
        ],
    },
    "alphapo": {
        "name": "CG-2026-0756: AlphaPo Hack (Lazarus) - cashout at Binance",
        "nodes": [
            {"addr": "040a96659fd7118259ebcd547771f6ecb9580d17"},  # AlphaPo Stolen Funds (named)
            {"addr": "8dc4f02e620fb24d07208c09950b9cba343805e8"},  # laundering wallet
            {"addr": "001866ae5b3de6caa5a51543fd9fb64f524f5478"},  # Binance.com (named)
        ],
        "edges": [
            {"from": 0, "to": 1, "label": "$11.1M (laundering wallet)"},
            {"from": 1, "to": 2, "label": "$44K traced to Binance (indirect)"},
        ],
    },
}


@chainalysis_workflow
def handler(event: dict, context: DurableContext) -> dict:
    """Build a multi-node Reactor investigation graph with labeled flow edges.

    Source = named stolen-funds cluster, end = named cashout exchange.
    Used by insurance-demo.html.

    Input:
      - scenario: "ascendex" | "atomic" | "alphapo"
    """
    from chainalysis_skill_graph import (
        GraphClient,
        add_cluster,
        add_annotation,
        add_annotation_edge,
    )
    from chainalysis_skill_graph.commands import Network

    scenario_key = event.get("scenario", "ascendex")
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

        # Phase 1: cluster nodes, spaced left-to-right with slight stagger
        node_commands = []
        for i, node in enumerate(nodes):
            addr = node["addr"].lower().replace("0x", "")
            y = (i % 2) * 15
            node_commands.append(
                add_cluster(
                    graph_id,
                    Network.ETHEREUM_MAINNET,
                    addr,
                    {"x": i * 45, "y": y},
                )
            )
        node_commands.append(
            add_annotation(graph_id, graph_name, {"x": 0, "y": -25})
        )
        client.execute_commands(graph_id, node_commands)

        # Phase 2: labeled flow edges
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
