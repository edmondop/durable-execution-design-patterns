# Leanpub Integration

Leanpub reads from the `manuscript/` directory and expects Markua format.

The book is authored in AsciiDoc (`book/chapters/`). A sync script converts
AsciiDoc to Markua for Leanpub publishing.

Run the sync:

```bash
uv run manuscript-sync/sync.py
```

This generates `.markua` files in this directory from the AsciiDoc sources.
