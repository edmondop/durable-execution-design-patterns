# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Sync AsciiDoc chapters to Markua format for Leanpub.

This is a minimal converter that handles the most common AsciiDoc constructs.
For a production pipeline, consider using pandoc as an intermediate step:
  asciidoc -> docbook (via asciidoctor) -> markua (via pandoc + custom filter)
"""

import re
from pathlib import Path

BOOK_DIR = Path("book/chapters")
APPENDIX_DIR = Path("book/appendices")
OUTPUT_DIR = Path("leanpub/manuscript")


def convert_asciidoc_to_markua(text: str) -> str:
    # Section headings: == Title -> ## Title
    text = re.sub(r"^===== (.+)$", r"##### \1", text, flags=re.MULTILINE)
    text = re.sub(r"^==== (.+)$", r"#### \1", text, flags=re.MULTILINE)
    text = re.sub(r"^=== (.+)$", r"### \1", text, flags=re.MULTILINE)
    text = re.sub(r"^== (.+)$", r"## \1", text, flags=re.MULTILINE)

    # Code blocks: [source,lang]\n----\n...\n---- -> ```lang\n...\n```
    text = re.sub(
        r"\[source,(\w+)\]\n----\n",
        r"```\1\n",
        text,
    )
    text = text.replace("\n----\n", "\n```\n")

    # Admonitions: NOTE:/TIP:/WARNING: -> Markua aside blocks
    for admonition in ["NOTE", "TIP", "WARNING", "IMPORTANT"]:
        text = re.sub(
            rf"^{admonition}: (.+)$",
            rf"{{blurb, class: {admonition.lower()}}}\n\1\n{{/blurb}}",
            text,
            flags=re.MULTILINE,
        )

    # Images: image::file.svg[alt] -> ![alt](file.svg)
    text = re.sub(
        r"image::(.+?)\[(.+?)(?:,.*?)?\]",
        r"![\2](\1)",
        text,
    )

    # Bold: *text* -> **text**
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"**\1**", text)

    # Italic: _text_ -> *text*
    text = re.sub(r"(?<!_)_([^_]+)_(?!_)", r"*\1*", text)

    # Remove include directives (code will be inlined during full build)
    text = re.sub(r"^include::.+$", "<!-- include removed - inline code for Leanpub -->", text, flags=re.MULTILINE)

    # Remove AsciiDoc-specific attributes
    text = re.sub(r"^\[quote\]$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\..+$", "", text, flags=re.MULTILINE)  # Block titles

    return text


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for src_dir in [BOOK_DIR, APPENDIX_DIR]:
        for adoc_file in sorted(src_dir.glob("*.adoc")):
            text = adoc_file.read_text()
            markua = convert_asciidoc_to_markua(text)
            out_file = OUTPUT_DIR / adoc_file.with_suffix(".markua").name
            out_file.write_text(markua)
            print(f"  {adoc_file} -> {out_file}")

    print(f"Synced to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
