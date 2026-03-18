#!/usr/bin/env python3
"""Verify that every include:: directive in .adoc files resolves to an
existing file and that any tag= references exist in the target file."""

import re
import sys
from pathlib import Path

ADOC_DIR = Path("docs/modules/ROOT/pages")
EXAMPLES_DIR = Path("docs/modules/ROOT/examples")

INCLUDE_RE = re.compile(
    r"include::\{examplesdir\}/(.+?)\[([^\]]*)\]"
)
TAG_RE = re.compile(r"tag=(\w+)")


def check() -> list[str]:
    errors: list[str] = []

    for adoc in sorted(ADOC_DIR.glob("*.adoc")):
        for line_no, line in enumerate(adoc.read_text().splitlines(), 1):
            m = INCLUDE_RE.search(line)
            if not m:
                continue

            rel_path = m.group(1)
            attrs = m.group(2)
            target = EXAMPLES_DIR / rel_path

            if not target.exists():
                errors.append(f"{adoc.name}:{line_no}: file not found: {rel_path}")
                continue

            tag_match = TAG_RE.search(attrs)
            if tag_match:
                tag = tag_match.group(1)
                content = target.read_text()
                if f"tag::{tag}[]" not in content:
                    errors.append(
                        f"{adoc.name}:{line_no}: tag '{tag}' not found in {rel_path}"
                    )

    return errors


def main() -> None:
    errors = check()
    if errors:
        print(f"Found {len(errors)} include error(s):", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        sys.exit(1)
    else:
        print("All include directives verified.")


if __name__ == "__main__":
    main()
