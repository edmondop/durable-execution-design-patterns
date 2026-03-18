# Durable Execution Design Patterns

A design pattern catalog for the durable execution era.

**9 structural patterns** that arise when building distributed, stateful,
long-running applications — and how durable execution resolves each one.

Free to read online. Available as PDF via Leanpub.

## The Patterns

| # | Pattern | Category | SDK |
|---|---------|----------|-----|
| 1 | The Entity (Durable Object) | State | Go |
| 2 | Code-as-State (Implicit State Machine) | State | Python |
| 3 | The Durable Promise (External Fulfillment) | Coordination | Java |
| 4 | The Execution Singleton (Durable Lock) | Coordination | TypeScript |
| 5 | The Saga (Compensating Interaction) | Composition | .NET |
| 6 | The Scatter-Gather (Parallel Aggregation) | Composition | Go |
| 7 | The Pipeline (Checkpoint Chain) | Composition | Python |
| 8 | The Perpetual Execution (Living Process) | Lifecycle | Java |
| 9 | The Durable Observer (Event Correlator) | Lifecycle | TypeScript |
| B | Cross-Boundary Orchestration (Nexus) | Bonus | .NET |

Each chapter uses a **different Temporal SDK language** to prove these
patterns are universal.

## Quick Start

```bash
# Install mise (https://mise.jdx.dev)
mise install

# Build the book (HTML + PDF)
mise run book

# Test a specific chapter's code examples
mise run test -- 01

# Test all chapters
mise run test-all

# Render all diagrams
mise run diagrams

# Lint all code
mise run lint
```

## Project Structure

```
book/           AsciiDoc source for the book
examples/       Runnable code per chapter (Go, Python, Java, TS, .NET)
diagrams/       Python scripts that generate SVG diagrams via uv run
infrastructure/ Helm values, Kind config, Chaos Mesh
dagger/         CI pipeline definitions
```

## Key Invariants

1. **The book cannot build if any code example fails its tests.** CI enforces:
   test-all -> lint -> build-book.
2. **Code in the book IS the code that runs.** AsciiDoc `include::` with
   tagged regions. No copy-paste. Single source of truth.
3. **Every diagram is version-controlled Python.** Rendered SVGs are gitignored
   and regenerated during build via `uv run`.
4. **Each example is independently deployable.** Every chapter has its own Helm
   chart, Dockerfile, and tests.
5. **Failure simulation is first-class.** Helm charts include chaos templates.

## Licenses

- **Book text and diagrams**: [CC-BY-SA-4.0](LICENSE-BOOK)
- **Code examples**: [Apache-2.0](LICENSE-CODE)

## Contributing

1. Fork the repo
2. `mise install` to set up your environment
3. Make your changes
4. `mise run test-all && mise run lint` to verify
5. Open a PR

Code examples must have tagged regions matching the AsciiDoc includes.
All code must have passing tests.
