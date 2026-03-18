# /// script
# requires-python = ">=3.10"
# dependencies = ["graphviz"]
# ///
"""Saga pattern: forward actions with compensating rollback on failure.

Layout is a V-shape: forward descends left, failure at bottom,
compensation climbs up on the right.
"""

from pathlib import Path

import graphviz

OUTPUT_DIR = Path("diagrams/rendered")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    dot = graphviz.Digraph(
        name="saga",
        format="svg",
        engine="dot",
        graph_attr={
            "fontname": "Helvetica",
            "fontsize": "11",
            "rankdir": "TB",
            "pad": "0.3",
            "bgcolor": "transparent",
            "nodesep": "0.8",
            "ranksep": "0.5",
            "newrank": "true",
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

    # --- Forward flow (left, in cluster) ---
    with dot.subgraph(name="cluster_forward") as fwd:
        fwd.attr(
            label="Forward Flow",
            style="filled,rounded",
            color="#555555",
            fillcolor="#f8f9fa",
            fontcolor="#333333",
            fontsize="13",
            penwidth="1.5",
            margin="16",
        )
        fwd.node("reserve_flight", label="Reserve\nFlight",
                 fillcolor="#047857", fontcolor="#ffffff", color="#047857")
        fwd.node("reserve_hotel", label="Reserve\nHotel",
                 fillcolor="#047857", fontcolor="#ffffff", color="#047857")
        fwd.node("charge_payment", label="Charge\nPayment",
                 fillcolor="#b91c1c", fontcolor="#ffffff", color="#b91c1c")

        fwd.edge("reserve_flight", "reserve_hotel",
                 label="  ok  ", color="#047857", fontcolor="#047857",
                 penwidth="1.5")
        fwd.edge("reserve_hotel", "charge_payment",
                 label="  ok  ", color="#047857", fontcolor="#047857",
                 penwidth="1.5")

    # --- Failure diamond (bottom center, outside both clusters) ---
    dot.node("failure", label="Payment\nFailed!",
             shape="diamond", fillcolor="#ffffff",
             color="#b91c1c", fontcolor="#b91c1c",
             penwidth="1.5", fontsize="12")

    # --- Compensation flow (right, in cluster) ---
    with dot.subgraph(name="cluster_compensate") as comp:
        comp.attr(
            label="Compensation Flow",
            style="filled,rounded",
            color="#555555",
            fillcolor="#f8f9fa",
            fontcolor="#333333",
            fontsize="13",
            penwidth="1.5",
            margin="16",
        )
        comp.node("cancel_hotel", label="Cancel\nHotel",
                  fillcolor="#4338CA", fontcolor="#ffffff", color="#4338CA")
        comp.node("cancel_flight", label="Cancel\nFlight",
                  fillcolor="#4338CA", fontcolor="#ffffff", color="#4338CA")

    # --- V-shape rank constraints ---
    with dot.subgraph() as s:
        s.attr(rank="same")
        s.node("reserve_flight")
        s.node("cancel_flight")

    with dot.subgraph() as s:
        s.attr(rank="same")
        s.node("reserve_hotel")
        s.node("cancel_hotel")

    # --- Invisible edges for left-right ordering ---
    dot.edge("reserve_flight", "cancel_flight", style="invis")
    dot.edge("reserve_hotel", "cancel_hotel", style="invis")

    # --- Error: down to failure diamond ---
    dot.edge("charge_payment", "failure",
             label="  error  ", color="#b91c1c", fontcolor="#b91c1c",
             style="dashed", penwidth="1.5")

    # --- Compensation edges (upward, right side) ---
    dot.edge("failure", "cancel_hotel",
             label="  compensate  ", color="#4338CA", fontcolor="#4338CA",
             penwidth="1.5", constraint="false")
    dot.edge("cancel_hotel", "cancel_flight",
             label="  undo  ", color="#4338CA", fontcolor="#4338CA",
             penwidth="1.5", constraint="false")

    # --- Compensation stack note ---
    dot.node("stack",
             label=(
                 "Compensation Stack\n"
                 "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n"
                 "1. Cancel Flight\n"
                 "2. Cancel Hotel"
             ),
             shape="note", fillcolor="#ffffff",
             fontname="Courier", fontsize="10",
             fontcolor="#4338CA", color="#999999",
             penwidth="1.2")

    dot.edge("stack", "failure",
             style="dotted", color="#999999",
             arrowhead="none", constraint="false")

    output_path = dot.render(
        filename="ch05-saga",
        directory=str(OUTPUT_DIR),
        cleanup=True,
    )
    print(f"  -> {output_path}")


if __name__ == "__main__":
    main()
