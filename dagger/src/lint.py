"""Dagger module for multi-language linting."""

import dagger


async def lint_go(client: dagger.Client, dirs: list[str]) -> str:
    results = []
    for d in dirs:
        src = client.host().directory(d)
        result = await (
            client.container()
            .from_("golangci/golangci-lint:latest")
            .with_mounted_directory("/work", src)
            .with_workdir("/work")
            .with_exec(["golangci-lint", "run"])
            .stdout()
        )
        results.append(f"{d}: {result}")
    return "\n".join(results)


async def lint_python(client: dagger.Client, dirs: list[str]) -> str:
    results = []
    for d in dirs:
        src = client.host().directory(d)
        result = await (
            client.container()
            .from_("python:3.12-slim")
            .with_exec(["pip", "install", "ruff"])
            .with_mounted_directory("/work", src)
            .with_workdir("/work")
            .with_exec(["ruff", "check", "."])
            .stdout()
        )
        results.append(f"{d}: {result}")
    return "\n".join(results)
