# Durable Execution Design Patterns — Book

## What This Is

An open-source book about design patterns enabled by durable execution.
10 chapters, each covering one pattern. Examples use Temporal (different
SDK language per chapter). Published via Antora (multi-page HTML) and
asciidoctor-pdf (PDF for Leanpub).

## Architecture

- **Single source of truth**: `docs/modules/ROOT/pages/*.adoc`
- **PDF build**: `book/book.adoc` includes from the Antora pages
- **Diagrams**: Python scripts in `diagrams/`, rendered SVGs in
  `diagrams/rendered/`, copied to `docs/modules/ROOT/images/`
- **Code examples**: `docs/modules/ROOT/examples/` — included via
  `{examplesdir}` attribute (resolves differently for Antora vs PDF)
- **Antora playbook**: `antora-playbook.yml` (uses worktree mode for
  local preview of uncommitted changes)
- **CSS theme**: `supplemental-ui/css/extra.css` (Literata body, Inter
  headings, JetBrains Mono code, indigo accent `#4338CA`)

## Chapter Structure

Every chapter follows this flow. Do not deviate.

1. **Quote** — one-sentence pattern summary in a blockquote
2. **Intent** — 2-3 sentences: what structural tension this resolves
3. **Motivation** — a concrete scenario. Make the reader feel the problem.
   Conversational, specific, vivid
4. **The Pattern** — diagram + one flowing description. Walk through the
   diagram naturally. No separate "Participants" / "Collaborations"
   subsections. No GoF formalism. Conversational tone.
5. **Traditionally...** — one short paragraph (5-8 lines max) explaining
   how you'd build this without durable execution. Optionally a small
   diagram. This is contrast, not a 40-line essay. The reader bought
   this book for DE patterns, not to relive infrastructure pain.
6. **With Durable Execution** — code listing with callouts, followed by
   explanation paragraphs that walk through the code. This is the heart
   of the chapter.
7. **Consequences** — trade-offs, limitations, when NOT to use it.
   Honest, specific, concrete.
8. **Distinction from...** — how this pattern differs from similar ones
   in the book. Only where needed.
9. **Origin of the example** — credit to Temporal samples or other
   sources where applicable
10. **Known Applications** — bullet list of real-world use cases
11. **Related Patterns** — bullet list with chapter references

## Voice and Style

- **Conversational, not academic.** Write like you're explaining to a
  sharp colleague, not submitting to a journal.
- **No GoF formalism.** No "Participants" / "Collaborations" /
  "Applicability" section headers. The structure above replaces them.
- **Bold inline labels** like `**Intent.**` and `**Consequences.**`
  work as anchors within flowing text. Keep them.
- **Standalone bold labels** (on their own line) must NOT have trailing
  periods: `**The Pattern**` not `**The Pattern.**`
- **Bold for key ideas** — use sparingly to highlight the most important
  phrases. Not every sentence. Think 2-3 bold phrases per section.
- **Italic for emphasis** — terms being introduced, pattern names on
  first use, the word being stressed in a sentence.
- **Body font is 0.95rem Literata.** Bold at weight 600 feels
  proportional. Don't worry about bold being too heavy.
- **No emojis.** Ever.

## Diagrams

### Routing (use the diagram-claude-plugin skill)

| Type | Tool |
|------|------|
| Architecture (boxes + arrows) | **graphviz** (auto-layout) |
| Sequence diagram | **PlantUML** (standard notation) |
| State machine | **PlantUML** |
| Custom comparison / timeline | **svgwrite** (precise coords) |

### Style — Canonical Palette (defined in `diagrams/_style.py`)

**Design rule: strong or clean.** Key elements get solid accent fills
with white text. Regular nodes stay white. No pastels, no pale washes.

| Token | Hex | Usage |
|-------|-----|-------|
| `accent` | `#4338CA` | Key element: solid fill + white text |
| `success` | `#047857` | Completed steps, forward flow, ok paths |
| `danger` | `#b91c1c` | Failures, deadlines, error paths |
| `data_store` | `#0f766e` | Databases, caches, persistent storage (cylinder shape) |
| `stroke` | `#555555` | Default node borders, neutral arrows (1-1.2px) |
| `stroke_light` | `#999999` | Notes, annotations, secondary elements |
| `text` | `#333333` | Primary label text |
| `text_light` | `#666666` | Secondary text, edge labels |
| `text_muted` | `#999999` | Tertiary text (timestamps, parentheticals) |
| `fill` | `#ffffff` | Node backgrounds |
| `fill_alt` | `#f8f9fa` | Cluster backgrounds (structural grouping only) |
| `bg` | `transparent` | SVG background — let the page show through |

- Font: Helvetica for all diagrams, Courier for code identifiers
- **Readability first**: nodes 14px, edges 10px, clusters 13px, notes 10px
- Edge labels: pad with spaces (`"  HTTP  "`) to avoid arrow overlap
- Cluster labels: use `margin` attr to prevent overlap with contents
- Use `compound=true` + `lhead`/`ltail` to target cluster borders
- PlantUML: use `<<stereotype>>` skinparam overrides for accent participants

### Sizing in AsciiDoc

Check the SVG viewBox dimensions. If the diagram is narrow (< 400px
wide), use `width=50%` or `width=60%` in the image macro to prevent
it from stretching to fill the page.

## Build Commands

```bash
# Render all diagrams
for f in diagrams/ch*.py diagrams/intro*.py; do uv run "$f"; done
cp diagrams/rendered/*.svg docs/modules/ROOT/images/

# Build Antora site (local preview)
npx antora antora-playbook.yml
# Site output: _build/site/

# Serve locally
python3 -m http.server 8000 --directory _build/site

# Build PDF
asciidoctor-pdf book/book.adoc -o _build/book.pdf
```

## Git Conventions

- One concern per commit
- Commit message: `type: short description` (style, content, fix, docs, diagrams)
- Do not commit rendered SVGs in `diagrams/rendered/` (gitignored)
- Do commit SVGs copied to `docs/modules/ROOT/images/`
