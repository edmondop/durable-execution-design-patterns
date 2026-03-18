# /// script
# requires-python = ">=3.10"
# dependencies = ["graphviz"]
# ///
"""Scatter-Gather pattern: fan-out to multiple activities, fan-in with deadline."""

from pathlib import Path

import graphviz

OUTPUT_DIR = Path("diagrams/rendered")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    dot = graphviz.Digraph(
        name="scatter_gather",
        format="svg",
        engine="dot",
        graph_attr={
            "fontname": "Helvetica",
            "fontsize": "11",
            "rankdir": "TB",
            "pad": "0.5",
            "bgcolor": "transparent",
            "nodesep": "0.6",
            "ranksep": "0.9",
            "compound": "true",
        },
        node_attr={
            "fontname": "Helvetica",
            "fontsize": "10",
            "fontcolor": "#333333",
            "shape": "box",
            "style": "filled,rounded",
            "fillcolor": "#ffffff",
            "color": "#555555",
            "penwidth": "1.2",
        },
        edge_attr={
            "fontname": "Helvetica",
            "fontsize": "9",
            "fontcolor": "#666666",
            "color": "#555555",
            "arrowsize": "0.7",
        },
    )

    # --- Coordinator ---
    dot.node("coordinator", label="Coordinator\nWorkflow",
             fillcolor="#4338CA", fontcolor="#ffffff", color="#4338CA")

    # --- Activity nodes (fan-out targets) ---
    airlines = []
    for i in range(1, 6):
        node_id = f"airline{i}"
        airlines.append(node_id)
        dot.node(node_id, label=f"Airline {i}\nActivity")

    with dot.subgraph() as s:
        s.attr(rank="same")
        for a in airlines:
            s.node(a)

    # --- Aggregation node ---
    dot.node("aggregation", label="Aggregation\n(best price)",
             fillcolor="#4338CA", fontcolor="#ffffff", color="#4338CA")

    # --- Deadline Timer ---
    dot.node("timer", label="Deadline Timer",
             fillcolor="#b91c1c", fontcolor="#ffffff", color="#b91c1c",
             style="filled,rounded")

    # --- Fan-out edges: Coordinator -> Airlines ---
    for a in airlines:
        dot.edge("coordinator", a, label="  search  ",
                 color="#4338CA", fontcolor="#4338CA")

    # --- Fan-in edges: Airlines -> Aggregation ---
    for a in airlines:
        dot.edge(a, "aggregation", label="  result  ",
                 color="#047857", fontcolor="#047857")

    # --- Timer -> Aggregation ---
    dot.edge("timer", "aggregation", label="  8s deadline  ",
             color="#b91c1c", fontcolor="#b91c1c", style="dashed")

    # --- Aggregation -> Result ---
    dot.node("result", label="Return\nBest Quotes",
             fillcolor="#ffffff", color="#555555")

    dot.edge("aggregation", "result", label="  complete  ")

    output_path = dot.render(
        filename="ch06-scatter-gather",
        directory=str(OUTPUT_DIR),
        cleanup=True,
    )
    print(f"  -> {output_path}")


if __name__ == "__main__":
    main()
