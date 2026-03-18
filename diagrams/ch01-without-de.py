# /// script
# requires-python = ">=3.12"
# dependencies = ["graphviz"]
# ///
"""Traditional entity: the shopping cart scattered across 3+ systems."""

from pathlib import Path

import graphviz

OUTPUT = Path("diagrams/rendered/ch01-without-de.svg")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

dot = graphviz.Digraph(
    format="svg",
    engine="dot",
    graph_attr={
        "bgcolor": "transparent",
        "rankdir": "TB",
        "fontname": "Helvetica",
        "fontsize": "15",
        "pad": "0.4",
        "nodesep": "0.5",
        "ranksep": "0.65",
        "compound": "true",
        "label": "",
    },
    node_attr={
        "fontname": "Helvetica",
        "fontsize": "18",
        "fontcolor": "#333333",
        "color": "#555555",
        "style": "filled,rounded",
        "fillcolor": "#ffffff",
        "penwidth": "1.2",
    },
    edge_attr={
        "fontname": "Helvetica",
        "fontsize": "14",
        "fontcolor": "#666666",
        "color": "#555555",
        "penwidth": "1",
        "arrowsize": "0.7",
    },
)

# --- Clients ---
dot.node("client_a", "Client A", shape="plaintext", fillcolor="transparent")
dot.node("client_b", "Client B", shape="plaintext", fillcolor="transparent")

# --- Stateless API ---
with dot.subgraph(name="cluster_api") as c:
    c.attr(
        label="Stateless API Layer",
        style="filled,rounded",
        color="#555555",
        fillcolor="#f8f9fa",
        fontcolor="#333333",
        fontsize="15",
        penwidth="1.5",
        margin="20",
        labeljust="l",
    )
    c.node("api", "API Service\n(business rules)")
    c.node("lock_check", "Optimistic Lock\nCheck", fontsize="16",
           style="filled,rounded,dashed", color="#b91c1c", fontcolor="#b91c1c")

# --- Data layer ---
with dot.subgraph(name="cluster_data") as c:
    c.attr(
        label="Data Layer",
        style="filled,rounded",
        color="#555555",
        fillcolor="#f8f9fa",
        fontcolor="#333333",
        fontsize="15",
        penwidth="1.5",
        margin="20",
    )
    c.node("db", "Database\n(cart state +\nversion column)", shape="cylinder",
           fillcolor="#0f766e", fontcolor="#ffffff", color="#0f766e",
           penwidth="1.5")
    c.node("cache", "Redis Cache\n(read performance)", shape="cylinder",
           fillcolor="#0f766e", fontcolor="#ffffff", color="#0f766e",
           penwidth="1.5")

# --- Background jobs ---
with dot.subgraph(name="cluster_jobs") as c:
    c.attr(
        label="Background Jobs",
        style="filled,rounded",
        color="#555555",
        fillcolor="#f8f9fa",
        fontcolor="#333333",
        fontsize="15",
        penwidth="1.5",
        margin="20",
    )
    c.node("cron", "Cron Job\n(expire abandoned\ncarts)")
    c.node("cleanup", "Cleanup Worker\n(delete expired\ndata)")

# --- Keep clients and API cluster left-aligned ---
with dot.subgraph() as s:
    s.attr(rank="same")
    s.node("client_a")
    s.node("client_b")

# --- Edges: clients to API ---
dot.edge("client_a", "api", label="  add item  ")
dot.edge("client_b", "api", label="  add item  ")

# --- API to data layer ---
dot.edge("api", "cache", label="  read  ")
dot.edge("api", "db", label="  read-modify-write  ")
dot.edge("api", "lock_check")
dot.edge("lock_check", "db", label="  version check  ",
         color="#b91c1c", fontcolor="#b91c1c", style="dashed")
dot.edge("cache", "db", label="  cache miss  ",
         style="dashed", color="#999999", fontcolor="#999999")
dot.edge("api", "cache", label="  invalidate  ",
         style="dashed", color="#999999", fontcolor="#999999",
         constraint="false")

# --- Background jobs to data ---
dot.edge("cron", "db", label="  scan expired rows  ")
dot.edge("cleanup", "db", label="  delete  ",
         style="dashed", color="#999999", fontcolor="#999999")

# --- Race condition annotation ---
dot.node("race_note",
         label="Race condition:\nClient adds item while\ncron expires the cart",
         shape="note", fillcolor="#ffffff",
         fontsize="14", fontcolor="#b91c1c",
         color="#b91c1c")
dot.edge("race_note", "cron",
         style="dotted", color="#b91c1c",
         arrowhead="none")

svg_content = dot.pipe(encoding="utf-8")
OUTPUT.write_text(svg_content)
print(f"  -> {OUTPUT}")
