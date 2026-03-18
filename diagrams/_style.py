"""Canonical color palette and typography for all book diagrams.

Every diagram script should import from here instead of defining colors inline.
Keep in sync with the book CSS theme (book/theme/book.css).

Design rule: strong or clean. Solid accent fills with white text for key
elements, plain white for regular nodes. No pastels, no pale washes.
"""

# --- Colors ---

ACCENT = "#4338CA"       # Indigo — the pattern's key element
SUCCESS = "#047857"      # Green — completed steps, forward flow, ok paths
DANGER = "#b91c1c"       # Red — failures, deadlines, error paths
DATA_STORE = "#0f766e"   # Teal — databases, caches, persistent storage

STROKE = "#555555"       # Default node borders, neutral arrows
STROKE_LIGHT = "#999999" # Notes, annotations, secondary elements

TEXT = "#333333"          # Primary label text
TEXT_LIGHT = "#666666"    # Secondary text, annotations, edge labels
TEXT_MUTED = "#999999"    # Tertiary text (timestamps, parentheticals)

FILL = "#ffffff"          # Node backgrounds
FILL_ALT = "#f8f9fa"     # Cluster backgrounds (structural grouping only)
BG = "transparent"        # SVG background — let the page show through

# --- Typography ---

FONT = "Helvetica"        # All diagrams — renders reliably in SVG
FONT_MONO = "Courier"     # Code identifiers in diagrams
FONT_SIZE = 14            # Node labels — readable at any zoom
FONT_SIZE_EDGE = 10       # Edge labels
FONT_SIZE_CLUSTER = 13    # Cluster (subgraph) titles
FONT_SIZE_NOTE = 10       # Annotation notes
FONT_SIZE_TITLE = 11      # Graph title

# --- Graphviz presets ---

GRAPH_ATTRS = {
    "fontname": FONT,
    "fontsize": str(FONT_SIZE_TITLE),
    "bgcolor": BG,
    "pad": "0.4",
    "nodesep": "0.6",
    "ranksep": "0.7",
    "compound": "true",
}

NODE_ATTRS = {
    "fontname": FONT,
    "fontsize": "14",
    "fontcolor": TEXT,
    "shape": "box",
    "style": "filled,rounded",
    "fillcolor": FILL,
    "color": STROKE,
    "penwidth": "1.2",
}

EDGE_ATTRS = {
    "fontname": FONT,
    "fontsize": "10",
    "fontcolor": TEXT_LIGHT,
    "color": STROKE,
    "arrowsize": "0.7",
}

CLUSTER_ATTRS = {
    "style": "filled,rounded",
    "color": STROKE,
    "fillcolor": FILL_ALT,
    "fontcolor": TEXT,
    "fontsize": "13",
    "fontname": FONT,
    "penwidth": "1.5",
    "margin": "16",
}

NOTE_ATTRS = {
    "shape": "note",
    "fillcolor": FILL,
    "fontsize": "10",
    "fontcolor": TEXT_LIGHT,
    "color": STROKE_LIGHT,
}

# --- PlantUML skinparams (paste into .puml files) ---

PLANTUML_SKIN = """
skinparam backgroundColor transparent
skinparam sequence {
  ArrowColor #555555
  LifeLineBorderColor #555555
  LifeLineBackgroundColor #ffffff
  ParticipantBorderColor #555555
  ParticipantBackgroundColor #ffffff
  ParticipantFontColor #333333
  ParticipantFontSize 11
  ActorBorderColor #555555
}
skinparam note {
  BackgroundColor #ffffff
  BorderColor #999999
  FontSize 9
  FontColor #666666
}
""".strip()
