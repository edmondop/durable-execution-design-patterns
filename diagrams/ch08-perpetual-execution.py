# /// script
# requires-python = ">=3.10"
# dependencies = ["graphviz"]
# ///
"""Perpetual Execution: ContinueAsNew lifecycle with history reset."""

from pathlib import Path

import graphviz

OUTPUT_DIR = Path("diagrams/rendered")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    dot = graphviz.Digraph(
        name="perpetual_execution",
        format="svg",
        engine="dot",
        graph_attr={
            "fontname": "Helvetica",
            "fontsize": "11",
            "rankdir": "LR",
            "pad": "0.3",
            "bgcolor": "transparent",
            "nodesep": "0.4",
            "ranksep": "0.6",
            "compound": "true",
        },
        node_attr={
            "fontname": "Helvetica",
            "fontsize": "14",
            "fontcolor": "#333333",
            "shape": "box",
            "style": "filled,rounded",
            "fillcolor": "#ffffff",
            "color": "#555555",
            "penwidth": "1.2",
        },
        edge_attr={
            "fontname": "Helvetica",
            "fontsize": "10",
            "fontcolor": "#666666",
            "color": "#555555",
            "arrowsize": "0.7",
        },
    )

    # --- Execution 1 ---
    with dot.subgraph(name="cluster_exec1") as c:
        c.attr(
            label="Execution 1  (history: 0 \u2192 N events)",
            style="filled,rounded",
            color="#555555",
            fillcolor="#f8f9fa",
            fontcolor="#333333",
            fontsize="13",
            penwidth="1.5",
            margin="16",
        )
        c.node("e1_charge", label="Charge")
        c.node("e1_receipt", label="Receipt")
        c.node("e1_sleep", label="Sleep\n30 days")
        c.node("e1_continue", label="ContinueAsNew",
               fillcolor="#4338CA", fontcolor="#ffffff",
               color="#4338CA", penwidth="1.5")

        c.edge("e1_charge", "e1_receipt")
        c.edge("e1_receipt", "e1_sleep")
        c.edge("e1_sleep", "e1_continue")

    # --- Execution 2 ---
    with dot.subgraph(name="cluster_exec2") as c:
        c.attr(
            label="Execution 2  (history: 0 \u2192 N events)",
            style="filled,rounded",
            color="#555555",
            fillcolor="#f8f9fa",
            fontcolor="#333333",
            fontsize="13",
            penwidth="1.5",
            margin="16",
        )
        c.node("e2_charge", label="Charge")
        c.node("e2_receipt", label="Receipt")
        c.node("e2_sleep", label="Sleep\n30 days")
        c.node("e2_continue", label="ContinueAsNew",
               fillcolor="#4338CA", fontcolor="#ffffff",
               color="#4338CA", penwidth="1.5")

        c.edge("e2_charge", "e2_receipt")
        c.edge("e2_receipt", "e2_sleep")
        c.edge("e2_sleep", "e2_continue")

    # --- ContinueAsNew bridge ---
    dot.edge("e1_continue", "e2_charge",
             label="  Carried State\n  history reset\n  to 0 events  ",
             color="#4338CA", fontcolor="#4338CA",
             penwidth="1.5", style="bold",
             fontsize="12",
             lhead="cluster_exec2")

    # --- Continuation ellipsis ---
    dot.node("ellipsis", label="...",
             shape="plain", fontsize="18", fontcolor="#555555")
    dot.edge("e2_continue", "ellipsis",
             color="#4338CA", penwidth="1.5", style="bold")

    import re

    svg = dot.pipe(encoding="utf-8")

    # Nudge the "Carried State / history reset / to 0 events" label up 2px
    def nudge_y(match: re.Match) -> str:
        before, y_val, after = match.group(1), float(match.group(2)), match.group(3)
        return f'{before}{y_val - 2:.2f}{after}'

    # Match the three text lines that contain the bridge label
    svg = re.sub(
        r'(y=")([-\d.]+)(" font-family="Helvetica,sans-Serif" font-size="12\.00" fill="#4338ca">)',
        nudge_y,
        svg,
    )

    output_path = OUTPUT_DIR / "ch08-perpetual-execution.svg"
    output_path.write_text(svg)
    print(f"  -> {output_path}")


if __name__ == "__main__":
    main()
