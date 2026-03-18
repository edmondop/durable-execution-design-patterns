# /// script
# requires-python = ">=3.12"
# dependencies = ["svgwrite"]
# ///
"""Execution Singleton: workflow ID as distributed lock."""

from pathlib import Path

import svgwrite

OUTPUT = Path("diagrams/rendered/ch04-execution-singleton.svg")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

ACCENT = "#4338CA"
STROKE = "#555555"
TEXT = "#333333"
TEXT_LIGHT = "#666666"
DANGER = "#b91c1c"

W, H = 620, 230
dwg = svgwrite.Drawing(str(OUTPUT), size=(W, H), viewBox=f"0 0 {W} {H}")
dwg.add(dwg.style(
    "text { font-family: Helvetica, Arial, sans-serif; }"
))

marker = dwg.defs.add(dwg.marker(insert=(8, 4), size=(8, 8), orient="auto",
                                  markerUnits="strokeWidth"))
marker.add(dwg.path(d="M0,0 L8,4 L0,8 Z", fill=STROKE))

marker_danger = dwg.defs.add(dwg.marker(id="arrow_danger", insert=(8, 4), size=(8, 8),
                                         orient="auto", markerUnits="strokeWidth"))
marker_danger.add(dwg.path(d="M0,0 L8,4 L0,8 Z", fill=DANGER))

# Cluster
dwg.add(dwg.rect((310, 30), (270, 170), fill="#f8f9fa", stroke=ACCENT, stroke_width=1.5,
                  rx=6, ry=6))
dwg.add(dwg.text("Workflow Runtime", insert=(445, 55), text_anchor="middle",
                 font_size="13", fill=ACCENT, font_weight="600"))

# Nodes
dwg.add(dwg.rect((30, 55), (130, 45), fill="#fff", stroke=STROKE, stroke_width=1, rx=4, ry=4))
dwg.add(dwg.text("Client A", insert=(95, 83), text_anchor="middle",
                 font_size="14", fill=TEXT))

dwg.add(dwg.rect((30, 130), (130, 45), fill="#fff", stroke=STROKE, stroke_width=1, rx=4, ry=4))
dwg.add(dwg.text("Client B", insert=(95, 158), text_anchor="middle",
                 font_size="14", fill=TEXT))

dwg.add(dwg.rect((360, 80), (200, 60), fill=ACCENT, stroke=ACCENT, stroke_width=1.5, rx=4, ry=4))
dwg.add(dwg.text("payment-pay123", insert=(460, 107), text_anchor="middle",
                 font_size="14", fill="#ffffff", font_weight="500"))
dwg.add(dwg.text("(Active)", insert=(460, 125), text_anchor="middle",
                 font_size="11", fill="#ccccdd"))

# Arrows
dwg.add(dwg.line((160, 77), (360, 103), stroke=STROKE, stroke_width=1,
                  marker_end=marker.get_funciri()))
dwg.add(dwg.text("Start \u2192 OK", insert=(250, 80), text_anchor="middle",
                 font_size="11", fill=TEXT_LIGHT))

dwg.add(dwg.line((160, 152), (360, 118), stroke=DANGER, stroke_width=1,
                  stroke_dasharray="5,3", marker_end=marker_danger.get_funciri()))
dwg.add(dwg.text("Start \u2192 Already Exists", insert=(250, 165), text_anchor="middle",
                 font_size="11", fill=DANGER))

dwg.save()
print(f"  -> {OUTPUT}")
