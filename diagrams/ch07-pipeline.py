# /// script
# requires-python = ">=3.10"
# dependencies = ["graphviz"]
# ///
"""Pipeline pattern: parent orchestrator fans out per-item child pipelines."""

from pathlib import Path

import graphviz

OUTPUT_DIR = Path("diagrams/rendered")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    dot = graphviz.Digraph(
        name="pipeline",
        format="svg",
        engine="dot",
        graph_attr={
            "fontname": "Helvetica",
            "fontsize": "11",
            "rankdir": "TB",
            "pad": "0.5",
            "bgcolor": "transparent",
            "nodesep": "0.5",
            "ranksep": "0.7",
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

    # --- Parent workflow ---
    dot.node("parent", label="Parent Workflow\n(10,000 claims)",
             fillcolor="#4338CA", fontcolor="#ffffff",
             color="#4338CA", penwidth="1.5")

    # --- Fan-out arrows ---
    dot.node("child1_label", label="Claim #1", shape="plaintext",
             fontsize="9", fontcolor="#333333")
    dot.node("child2_label", label="Claim #2", shape="plaintext",
             fontsize="9", fontcolor="#333333")
    dot.node("childn_label", label="Claim #N", shape="plaintext",
             fontsize="9", fontcolor="#333333")
    dot.node("dots", label="...", shape="plaintext",
             fontsize="16", fontcolor="#555555")

    dot.edge("parent", "child1_label", penwidth="1.2")
    dot.edge("parent", "child2_label", penwidth="1.2")
    dot.edge("parent", "dots", arrowhead="none", penwidth="1.2")
    dot.edge("parent", "childn_label", penwidth="1.2")

    # --- Detailed child pipeline (Claim #1) ---
    with dot.subgraph(name="cluster_child1") as c:
        c.attr(
            label="Child Workflow (one claim)",
            style="filled,rounded",
            color="#555555",
            fillcolor="#f8f9fa",
            fontcolor="#333333",
            fontsize="11",
            penwidth="1.5",
            margin="16",
        )

        c.node("ingest", label="Ingest")
        c.node("ocr", label="OCR +\nExtract")
        c.node("validate", label="Cross-\nValidate")
        c.node("fraud", label="Fraud\nScore")
        c.node("review", label="Adjuster\nReview",
               style="filled,rounded,dashed",
               fillcolor="#ffffff", fontcolor="#4338CA",
               color="#4338CA", penwidth="1.5")
        c.node("decide", label="Decision")

        c.edge("ingest", "ocr")
        c.edge("ocr", "validate")
        c.edge("validate", "fraud")
        c.edge("fraud", "review",
               label="  score > threshold  ",
               fontcolor="#4338CA", color="#4338CA",
               style="dashed", penwidth="1.2")
        c.edge("fraud", "decide",
               label="  score ok  ",
               fontcolor="#047857", color="#047857")
        c.edge("review", "decide")

    dot.edge("child1_label", "ingest", lhead="cluster_child1")

    # --- Wait annotation on review ---
    dot.node("wait_note",
             label="Blocks for hours/days\nuntil human signals",
             shape="note", fillcolor="#ffffff",
             fontsize="8", fontcolor="#666666",
             color="#999999")
    dot.edge("wait_note", "review",
             style="dotted", color="#999999",
             arrowhead="none")

    # --- Collapsed children (Claim #2, #N) ---
    dot.node("child2_collapsed",
             label="Ingest \u2192 OCR \u2192 ... \u2192 Decision",
             fontsize="9", fillcolor="#f8f9fa", color="#999999",
             fontcolor="#666666")
    dot.node("childn_collapsed",
             label="Ingest \u2192 OCR \u2192 ... \u2192 Decision",
             fontsize="9", fillcolor="#f8f9fa", color="#999999",
             fontcolor="#666666")

    dot.edge("child2_label", "child2_collapsed")
    dot.edge("childn_label", "childn_collapsed")

    # --- Results flow back to parent ---
    dot.node("aggregate",
             label="Parent aggregates\n9,855 done | 142 in review | 3 failed",
             shape="box", fillcolor="#4338CA",
             color="#4338CA", fontcolor="#ffffff",
             penwidth="1.5", style="filled,rounded",
             fontsize="9")

    dot.edge("decide", "aggregate",
             ltail="cluster_child1",
             color="#555555", style="dashed")
    dot.edge("child2_collapsed", "aggregate",
             color="#999999", style="dashed")
    dot.edge("childn_collapsed", "aggregate",
             color="#999999", style="dashed")

    output_path = dot.render(
        filename="ch07-pipeline",
        directory=str(OUTPUT_DIR),
        cleanup=True,
    )
    print(f"  -> {output_path}")


if __name__ == "__main__":
    main()
