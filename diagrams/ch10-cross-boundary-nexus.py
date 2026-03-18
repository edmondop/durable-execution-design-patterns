# /// script
# requires-python = ">=3.10"
# dependencies = ["graphviz"]
# ///
"""Cross-Boundary Orchestration: Nexus connecting caller and handler namespaces."""

from pathlib import Path

import graphviz

OUTPUT_DIR = Path("diagrams/rendered")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    dot = graphviz.Digraph(
        name="cross_boundary_nexus",
        format="svg",
        engine="dot",
        graph_attr={
            "fontname": "Helvetica",
            "fontsize": "15",
            "rankdir": "LR",
            "pad": "0.4",
            "bgcolor": "transparent",
            "nodesep": "0.6",
            "ranksep": "1.2",
            "compound": "true",
        },
        node_attr={
            "fontname": "Helvetica",
            "fontsize": "18",
            "fontcolor": "#333333",
            "shape": "box",
            "style": "filled,rounded",
            "fillcolor": "#ffffff",
            "color": "#555555",
            "penwidth": "1.2",
        },
        edge_attr={
            "fontname": "Helvetica",
            "fontsize": "14",
            "fontcolor": "#666666",
            "color": "#555555",
            "arrowsize": "0.7",
        },
    )

    # Namespace A — caller side
    with dot.subgraph(name="cluster_ns_a") as c:
        c.attr(
            label="Namespace A  (Orders)",
            style="filled,rounded",
            color="#555555",
            fillcolor="#f8f9fa",
            fontcolor="#333333",
            fontsize="15",
            penwidth="1.5",
            margin="16",
        )
        c.node("order_wf", label="Order\nWorkflow")
        c.node("exec_op", label="ExecuteNexus\nOperation",
               fontname="Courier", fontsize="14")

    dot.edge("order_wf", "exec_op",
             label="  FulfillOrder  ")

    # Nexus Endpoint — the routing layer (accented)
    dot.node("nexus_ep",
             label="Nexus\nEndpoint",
             shape="hexagon",
             fillcolor="#4338CA",
             fontcolor="#ffffff",
             color="#4338CA",
             penwidth="1.5",
             fontsize="14")

    # Namespace B — handler side
    with dot.subgraph(name="cluster_ns_b") as c:
        c.attr(
            label="Namespace B  (Fulfillment)",
            style="filled,rounded",
            color="#555555",
            fillcolor="#f8f9fa",
            fontcolor="#333333",
            fontsize="15",
            penwidth="1.5",
            margin="16",
        )
        c.node("handler", label="Nexus\nHandler",
               fontname="Courier", fontsize="14")
        c.node("fulfill_wf", label="Fulfillment\nWorkflow")

    dot.edge("handler", "fulfill_wf",
             label="  starts  ")

    # Forward path: caller -> endpoint -> handler
    dot.edge("exec_op", "nexus_ep",
             label="  FulfillOrder operation  ",
             color="#4338CA", fontcolor="#4338CA",
             penwidth="1.5")
    dot.edge("nexus_ep", "handler",
             label="  routes to handler  ",
             color="#4338CA", fontcolor="#4338CA",
             penwidth="1.5")

    # Return path: result back
    dot.edge("fulfill_wf", "exec_op",
             label="  tracking number  ",
             style="dashed",
             color="#047857", fontcolor="#047857",
             constraint="false")

    # Operation Contract note
    dot.node("contract",
             label="Operation Contract\n\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n"
                   "Input:  OrderRequest\n"
                   "Output: TrackingNumber",
             shape="note",
             fillcolor="#ffffff",
             fontname="Courier",
             fontsize="12",
             fontcolor="#666666",
             color="#999999")
    dot.edge("nexus_ep", "contract",
             style="dotted", color="#999999",
             arrowhead="none")

    import re

    svg = dot.pipe(encoding="utf-8")

    # Nudge all edge labels up 2px — they sit on horizontal arrows
    # Edge labels are inside <g class="edge"> groups; find <text> inside those
    def nudge_edge_labels(svg_text: str) -> str:
        in_edge = False
        lines = svg_text.split("\n")
        result = []
        for line in lines:
            if 'class="edge"' in line:
                in_edge = True
            elif in_edge and "</g>" in line:
                in_edge = False
            elif in_edge and "<text " in line:
                line = re.sub(
                    r'y="([-\d.]+)"',
                    lambda m: f'y="{float(m.group(1)) - 2:.2f}"',
                    line,
                )
            result.append(line)
        return "\n".join(result)

    svg = nudge_edge_labels(svg)

    output_path = OUTPUT_DIR / "ch10-cross-boundary-nexus.svg"
    output_path.write_text(svg)
    print(f"  -> {output_path}")


if __name__ == "__main__":
    main()
