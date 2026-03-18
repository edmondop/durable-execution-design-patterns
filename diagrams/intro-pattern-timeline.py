# /// script
# requires-python = ">=3.12"
# dependencies = ["svgwrite"]
# ///
"""Timeline of design patterns in software engineering, from Alexander to CQRS."""

from pathlib import Path

import svgwrite

OUTPUT = Path("diagrams/rendered/intro-pattern-timeline.svg")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

ACCENT = "#4338CA"
STROKE = "#555555"
TEXT = "#333333"
TEXT_LIGHT = "#666666"
LINE = "#999999"

events = [
    (1977, "Alexander", "A Pattern Language"),
    (1987, "Beck & Cunningham", "Patterns in Smalltalk"),
    (1994, "GoF", "Design Patterns"),
    (1996, "Schmidt", "Reactor / Proactor"),
    (2003, "Hohpe & Woolf", "Enterprise Integration"),
    (2007, "Nygard", "Release It!"),
    (2010, "Young", "CQRS & Event Sourcing"),
]

W = 900
H = 230
AXIS_Y = 115
LEFT = 65
RIGHT = W - 80
SPACING = (RIGHT - LEFT) / (len(events) - 1)

dwg = svgwrite.Drawing(str(OUTPUT), size=(W, H), viewBox=f"0 0 {W} {H}")
dwg.add(dwg.style(
    "text { font-family: Helvetica, Arial, sans-serif; }"
))

dwg.add(dwg.line((LEFT - 20, AXIS_Y), (RIGHT + 20, AXIS_Y),
                  stroke=LINE, stroke_width=1.5))

for i, (year, author, title) in enumerate(events):
    x = LEFT + i * SPACING
    above = i % 2 == 0

    dwg.add(dwg.circle(center=(x, AXIS_Y), r=4.5, fill=STROKE))

    stem_y = AXIS_Y - 40 if above else AXIS_Y + 40
    dwg.add(dwg.line((x, AXIS_Y), (x, stem_y),
                      stroke=LINE, stroke_width=0.8))

    label_y = stem_y - 10 if above else stem_y + 18
    title_y = label_y + 16 if above else label_y + 16

    dwg.add(dwg.text(title, insert=(x, label_y), text_anchor="middle",
                     font_size="13", fill=TEXT, font_weight="500"))
    dwg.add(dwg.text(author, insert=(x, title_y), text_anchor="middle",
                     font_size="11", fill=TEXT_LIGHT))

    year_y = AXIS_Y + 18 if above else AXIS_Y - 10
    dwg.add(dwg.text(str(year), insert=(x, year_y), text_anchor="middle",
                     font_size="10", fill=TEXT_LIGHT))

dwg.save()
print(f"  -> {OUTPUT}")
