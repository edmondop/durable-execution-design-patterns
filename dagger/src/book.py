"""Dagger module for building the book (AsciiDoc -> HTML + PDF)."""

import dagger


async def build_book(client: dagger.Client) -> dagger.Directory:
    src = client.host().directory(".", exclude=["_build", "diagrams/rendered"])

    container = (
        client.container()
        .from_("asciidoctor/docker-asciidoctor:latest")
        .with_mounted_directory("/work", src)
        .with_workdir("/work/book")
        .with_exec(["asciidoctor", "book.adoc", "-o", "../_build/html/index.html"])
        .with_exec([
            "asciidoctor-pdf", "book.adoc",
            "-a", "pdf-theme=theme/durable-patterns-theme.yml",
            "-a", "pdf-fontsdir=theme/fonts",
            "-o", "../_build/book.pdf",
        ])
    )

    return container.directory("/work/_build")
