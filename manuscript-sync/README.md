# Manuscript Sync

Converts AsciiDoc chapters to Markua format for Leanpub publishing.

```bash
uv run manuscript-sync/sync.py
```

This is a lightweight converter for common constructs. For complex chapters,
you may need to manually adjust the output.

The full pipeline for a production Leanpub build:

1. Run `mise run diagrams` to render all SVGs
2. Run `uv run manuscript-sync/sync.py` to convert chapters
3. Copy rendered diagrams to `leanpub/manuscript/images/`
4. Push to the Leanpub-connected branch
