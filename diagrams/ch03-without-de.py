# /// script
# requires-python = ">=3.12"
# dependencies = ["graphviz"]
# ///
"""Traditional approval: 6 components all wired to the same database."""

from pathlib import Path

import graphviz

OUTPUT = Path("diagrams/rendered/ch03-without-de.svg")
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
        "ranksep": "0.7",
        "compound": "true",
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

# --- Actors ---
dot.node("employee", "Employee", shape="plaintext", fillcolor="transparent")
dot.node("manager", "Manager", shape="plaintext", fillcolor="transparent")

# --- API layer ---
with dot.subgraph(name="cluster_api") as c:
    c.attr(
        label="API Layer",
        style="filled,rounded",
        color="#555555",
        fillcolor="#f8f9fa",
        fontcolor="#333333",
        fontsize="15",
        penwidth="1.5",
        margin="12",
    )
    c.node("submit_api", "Submission\nAPI")
    c.node("approve_api", "Approval\nAPI")

# --- The database (everything converges here) ---
dot.node("db", "Database\n(pending_requests table)",
         shape="cylinder",
         fillcolor="#0f766e", fontcolor="#ffffff", color="#0f766e",
         penwidth="1.5", fontsize="16",
         width="2.2", height="1.2")

# --- Background workers ---
with dot.subgraph(name="cluster_workers") as c:
    c.attr(
        label="Background Workers",
        style="filled,rounded",
        color="#555555",
        fillcolor="#f8f9fa",
        fontcolor="#333333",
        fontsize="15",
        penwidth="1.5",
        margin="12",
    )
    c.node("notify_worker", "Notification\nWorker\n(polls for new rows)")
    c.node("cron", "Timeout\nScheduler\n(scans for expired)")
    c.node("reconciler", "Reconciliation\nJob\n(catches edge cases)")

# --- External ---
dot.node("email", "Email Service", fillcolor="#ffffff")
dot.node("dlq", "Dead Letter\nQueue",
         fillcolor="#b91c1c", fontcolor="#ffffff", color="#b91c1c")

# --- Edges: actors to APIs ---
dot.edge("employee", "submit_api", label="  submit request  ")
dot.edge("manager", "approve_api", label="  approve / reject  ")

# --- APIs to database ---
dot.edge("submit_api", "db", label="  INSERT row  ")
dot.edge("approve_api", "db", label="  UPDATE status  ")

# --- Workers all poll the same DB ---
dot.edge("notify_worker", "db", label="  poll  ")
dot.edge("cron", "db", label="  scan  ")
dot.edge("reconciler", "db", label="  scan  ")

# --- Notification worker to email ---
dot.edge("notify_worker", "email", label="  send  ")

# --- Cron to DLQ ---
dot.edge("cron", "dlq", label="  move expired  ",
         style="dashed", color="#b91c1c", fontcolor="#b91c1c")

# --- Race condition note ---
dot.node("race_note",
         label="Race: manager approves at 71h 59m,\ncron expires at 72h 1m.\nRequires optimistic locking.",
         shape="note", fillcolor="#ffffff",
         fontsize="15", fontcolor="#b91c1c",
         color="#b91c1c")
dot.edge("race_note", "db",
         style="dotted", color="#b91c1c",
         arrowhead="none")

svg_content = dot.pipe(encoding="utf-8")
OUTPUT.write_text(svg_content)
print(f"  -> {OUTPUT}")
