# /// script
# requires-python = ">=3.12"
# dependencies = ["svgwrite"]
# ///
"""Code-as-State: implicit state machine via execution position."""

from pathlib import Path

import svgwrite

OUTPUT = Path("diagrams/rendered/ch02-code-as-state-fsm.svg")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

ACCENT = "#4338CA"
STROKE = "#555555"
TEXT = "#333333"
TEXT_LIGHT = "#666666"

states = ["Validating", "Paying", "Reserving", "Shipping", "Done"]
W = 780
H = 120
R = 32
SPACING = (W - 100) / (len(states) - 1)
CY = 65

dwg = svgwrite.Drawing(str(OUTPUT), size=(W, H), viewBox=f"0 0 {W} {H}")
dwg.add(dwg.style(
    "text { font-family: Helvetica, Arial, sans-serif; }"
))

marker = dwg.defs.add(dwg.marker(insert=(8, 4), size=(8, 8), orient="auto",
                                  markerUnits="strokeWidth"))
marker.add(dwg.path(d="M0,0 L8,4 L0,8 Z", fill=STROKE))

edge_labels = ["await", "await", "await", "return"]

for i, name in enumerate(states):
    cx = 50 + i * SPACING
    is_last = i == len(states) - 1
    stroke = ACCENT if is_last else STROKE
    fill = ACCENT if is_last else "#fff"
    text_fill = "#ffffff" if is_last else TEXT
    sw = 1.5 if is_last else 1

    dwg.add(dwg.circle(center=(cx, CY), r=R, fill=fill, stroke=stroke, stroke_width=sw))
    dwg.add(dwg.text(name, insert=(cx, CY + 4), text_anchor="middle",
                     font_size="10", fill=text_fill, font_weight="500"))

    if i < len(states) - 1:
        x1 = cx + R + 2
        x2 = 50 + (i + 1) * SPACING - R - 2
        dwg.add(dwg.line((x1, CY), (x2, CY), stroke=STROKE, stroke_width=1,
                          marker_end=marker.get_funciri()))
        dwg.add(dwg.text(edge_labels[i], insert=((x1 + x2) / 2, CY - 8),
                         text_anchor="middle", font_size="9", fill=TEXT_LIGHT))

dwg.add(dwg.text("Execution position IS the state", insert=(W / 2, 16),
                 text_anchor="middle", font_size="11", fill=TEXT, font_weight="500"))

dwg.save()
print(f"  -> {OUTPUT}")
