"""Dagger module for rendering diagrams via uv run."""

import dagger


async def render_diagrams(client: dagger.Client) -> dagger.Directory:
    src = client.host().directory("diagrams")

    container = (
        client.container()
        .from_("python:3.12-slim")
        .with_exec(["pip", "install", "uv"])
        .with_mounted_directory("/work/diagrams", src)
        .with_workdir("/work")
        .with_exec([
            "sh", "-c",
            "mkdir -p diagrams/rendered && "
            "for f in diagrams/ch*.py diagrams/intro*.py; do "
            "[ -f \"$f\" ] && uv run \"$f\"; done",
        ])
    )

    return container.directory("/work/diagrams/rendered")
