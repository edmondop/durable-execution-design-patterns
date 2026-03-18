# /// script
# requires-python = ">=3.10"
# dependencies = ["graphviz"]
# ///
"""Durable Observer pattern: event correlation with temporal windows."""

from pathlib import Path

import graphviz

OUTPUT_DIR = Path("diagrams/rendered")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    dot = graphviz.Digraph(
        name="durable_observer",
        format="svg",
        engine="dot",
        graph_attr={
            "fontname": "Helvetica",
            "fontsize": "11",
            "rankdir": "LR",
            "pad": "0.5",
            "bgcolor": "transparent",
            "nodesep": "0.5",
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

    # --- External event sources (left) ---
    with dot.subgraph(name="cluster_sources") as src:
        src.attr(
            label="Event Sources",
            style="filled,rounded",
            color="#555555",
            fillcolor="#f8f9fa",
            fontcolor="#333333",
            fontsize="11",
            fontname="Helvetica",
        )
        src.node("auth", label="Auth Service")
        src.node("txn", label="Transaction\nService")
        src.node("geo", label="Geo Service")

    # --- Observer Workflow (center, accented) ---
    with dot.subgraph(name="cluster_observer") as wf:
        wf.attr(
            label="Observer Workflow  (user-{id})",
            style="filled,rounded",
            color="#4338CA",
            fillcolor="#f8f9fa",
            fontcolor="#4338CA",
            fontsize="11",
            fontname="Helvetica",
            penwidth="1.5",
            margin="16",
        )

        wf.node("events", label="Events Array\n[ auth, txn, geo, ... ]",
                color="#4338CA")

        wf.node("timer", label="5-min Window\n(timer / deadline)",
                style="filled,rounded,dashed",
                color="#999999", fontcolor="#666666", fontsize="9")

        wf.node("rule", label="Correlation Rule\nevaluate(events)",
                style="filled,rounded",
                fillcolor="#4338CA", fontcolor="#ffffff", color="#4338CA")

    # --- Alert output (right) ---
    dot.node("alert", label="Alert\n(suspicious activity)",
             fillcolor="#b91c1c", fontcolor="#ffffff", color="#b91c1c",
             style="filled,rounded")

    # --- Edges ---
    dot.edge("auth", "events", label="  signal  ", lhead="cluster_observer")
    dot.edge("txn", "events", label="  signal  ", lhead="cluster_observer")
    dot.edge("geo", "events", label="  signal  ", lhead="cluster_observer")

    dot.edge("timer", "rule", label="  deadline  ",
             style="dashed", color="#999999", fontcolor="#999999")

    dot.edge("events", "rule", label="  evaluate  ",
             color="#4338CA", fontcolor="#4338CA")

    dot.edge("rule", "alert", label="  fires  ",
             color="#b91c1c", fontcolor="#b91c1c")

    output_path = dot.render(
        filename="ch09-durable-observer",
        directory=str(OUTPUT_DIR),
        cleanup=True,
    )
    print(f"  -> {output_path}")


if __name__ == "__main__":
    main()
