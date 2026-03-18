# /// script
# requires-python = ">=3.12"
# dependencies = ["svgwrite"]
# ///
"""Durable Promise: sequence diagram showing external fulfillment."""

from pathlib import Path

import svgwrite

OUTPUT = Path("diagrams/rendered/ch03-durable-promise-seq.svg")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

ACCENT = "#4338CA"
STROKE = "#555"
TEXT = "#333"
TEXT_LIGHT = "#888"
LINE_LIGHT = "#ccc"

W, H = 650, 360
PARTICIPANTS = [
    (80, "Client"),
    (220, "API"),
    (370, "Workflow"),
    (530, "Approver"),
]
TOP = 55
BOTTOM = 340

dwg = svgwrite.Drawing(str(OUTPUT), size=(W, H), viewBox=f"0 0 {W} {H}")
dwg.add(dwg.style(
    "@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');"
    "text { font-family: Inter, Helvetica, Arial, sans-serif; }"
))

marker = dwg.defs.add(dwg.marker(insert=(8, 4), size=(8, 8), orient="auto",
                                  markerUnits="strokeWidth"))
marker.add(dwg.path(d="M0,0 L8,4 L0,8 Z", fill=STROKE))

marker_dash = dwg.defs.add(dwg.marker(id="arrow_dash", insert=(8, 4), size=(8, 8),
                                       orient="auto", markerUnits="strokeWidth"))
marker_dash.add(dwg.path(d="M0,0 L8,4 L0,8 Z", fill=TEXT_LIGHT))

for x, name in PARTICIPANTS:
    dwg.add(dwg.rect((x - 35, TOP - 25), (70, 25),
                      fill="#fff", stroke=STROKE, stroke_width=1))
    dwg.add(dwg.text(name, insert=(x, TOP - 8), text_anchor="middle",
                     font_size="11", fill=TEXT, font_weight="500"))
    dwg.add(dwg.line((x, TOP), (x, BOTTOM), stroke=LINE_LIGHT, stroke_width=1,
                      stroke_dasharray="4,3"))


def msg(x1: int, x2: int, y: int, label: str, *, dashed: bool = False) -> None:
    style = {"stroke_dasharray": "5,3"} if dashed else {}
    m = marker_dash if dashed else marker
    s = TEXT_LIGHT if dashed else STROKE
    dwg.add(dwg.line((x1, y), (x2, y), stroke=s, stroke_width=1,
                      marker_end=m.get_funciri(), **style))
    dwg.add(dwg.text(label, insert=((x1 + x2) / 2, y - 6), text_anchor="middle",
                     font_size="9", fill=TEXT_LIGHT))


y = TOP + 30
msg(80, 220, y, "POST /approvals")
y += 32
msg(220, 370, y, "Start workflow")
y += 32
msg(370, 530, y, "Notify (activity)")
y += 20

dwg.add(dwg.rect((340, y), (60, 50), fill="#fafbfc", stroke=ACCENT,
                  stroke_width=1, stroke_dasharray="4,2"))
dwg.add(dwg.text("Suspended", insert=(370, y + 20), text_anchor="middle",
                 font_size="9", fill=ACCENT, font_style="italic"))
dwg.add(dwg.text("hours / days...", insert=(370, y + 34), text_anchor="middle",
                 font_size="8", fill=TEXT_LIGHT, font_style="italic"))
y += 65

msg(530, 220, y, "POST /approve")
y += 32
msg(220, 370, y, "Signal(approved)")
y += 32
msg(370, 80, y, "Result: approved", dashed=True)

dwg.save()
print(f"  -> {OUTPUT}")
