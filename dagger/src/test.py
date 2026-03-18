"""Dagger module for running code examples per chapter."""

import dagger


async def test_go_chapter(client: dagger.Client, chapter_dir: str) -> str:
    src = client.host().directory(chapter_dir)

    result = await (
        client.container()
        .from_("golang:1.22-alpine")
        .with_mounted_directory("/work", src)
        .with_workdir("/work")
        .with_exec(["go", "test", "./..."])
        .stdout()
    )
    return result


async def test_python_chapter(client: dagger.Client, chapter_dir: str) -> str:
    src = client.host().directory(chapter_dir)

    result = await (
        client.container()
        .from_("python:3.12-slim")
        .with_mounted_directory("/work", src)
        .with_workdir("/work")
        .with_exec(["pip", "install", "-e", ".[dev]"])
        .with_exec(["pytest"])
        .stdout()
    )
    return result
