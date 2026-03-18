package main

import (
	"context"
	"fmt"

	"dagger.io/dagger"
)

func checkGo(ctx context.Context, client *dagger.Client, repo *dagger.Directory) error {
	type goChapter struct {
		name    string
		hasTest bool
	}
	chapters := []goChapter{
		{"ch01-entity", true},
		{"ch06-scatter-gather", true},
	}
	goCache := client.CacheVolume("go-mod-cache")
	base := client.Container().
		From("golang:1.22-bookworm").
		WithMountedCache("/go/pkg/mod", goCache)

	for _, ch := range chapters {
		dir := fmt.Sprintf("examples/%s/go", ch.name)
		container := base.
			WithDirectory("/src", repo.Directory(dir)).
			WithWorkdir("/src").
			WithExec([]string{"go", "mod", "tidy"}).
			WithExec([]string{"go", "build", "./..."})

		if ch.hasTest {
			fmt.Printf("  testing %s...\n", ch.name)
			container = container.WithExec([]string{"go", "test", "./..."})
		} else {
			fmt.Printf("  building %s...\n", ch.name)
		}

		if _, err := container.Sync(ctx); err != nil {
			return fmt.Errorf("%s: %w", ch.name, err)
		}
	}
	return nil
}

func checkPython(ctx context.Context, client *dagger.Client, repo *dagger.Directory) error {
	type pyChapter struct {
		name    string
		hasTest bool
	}
	chapters := []pyChapter{
		{"ch02-code-as-state", true},
		{"ch07-pipeline", true},
	}
	pipCache := client.CacheVolume("pip-cache")
	lintBase := client.Container().
		From("python:3.12-slim").
		WithExec([]string{"pip", "install", "--no-cache-dir", "ruff"})
	testBase := client.Container().
		From("python:3.12").
		WithMountedCache("/root/.cache/pip", pipCache).
		WithExec([]string{"pip", "install", "--no-cache-dir", "ruff"})

	for _, ch := range chapters {
		dir := fmt.Sprintf("examples/%s/python", ch.name)
		var container *dagger.Container
		if ch.hasTest {
			fmt.Printf("  testing %s...\n", ch.name)
			container = testBase.
				WithDirectory("/src", repo.Directory(dir)).
				WithWorkdir("/src").
				WithExec([]string{"ruff", "check", "."}).
				WithExec([]string{"pip", "install", "--no-cache-dir", "temporalio", "pytest", "pytest-asyncio"}).
				WithExec([]string{"pytest", "-v"})
		} else {
			fmt.Printf("  checking %s...\n", ch.name)
			container = lintBase.
				WithDirectory("/src", repo.Directory(dir)).
				WithWorkdir("/src").
				WithExec([]string{"ruff", "check", "."}).
				WithExec([]string{"python", "-c", "import ast, pathlib; [ast.parse(f.read_text()) for f in pathlib.Path('.').glob('*.py')]"})
		}

		if _, err := container.Sync(ctx); err != nil {
			return fmt.Errorf("%s: %w", ch.name, err)
		}
	}
	return nil
}

func checkJava(ctx context.Context, client *dagger.Client, repo *dagger.Directory) error {
	type javaChapter struct {
		name    string
		hasTest bool
	}
	chapters := []javaChapter{
		{"ch03-durable-promise", true},
		{"ch08-perpetual-execution", true},
	}
	mavenCache := client.CacheVolume("maven-repo")
	base := client.Container().
		From("maven:3.9-eclipse-temurin-21").
		WithMountedCache("/root/.m2/repository", mavenCache)

	for _, ch := range chapters {
		dir := fmt.Sprintf("examples/%s/java", ch.name)
		container := base.
			WithDirectory("/src", repo.Directory(dir)).
			WithWorkdir("/src")

		if ch.hasTest {
			fmt.Printf("  testing %s...\n", ch.name)
			container = container.WithExec([]string{"mvn", "-q", "test"})
		} else {
			fmt.Printf("  compiling %s...\n", ch.name)
			container = container.WithExec([]string{"mvn", "-q", "compile"})
		}

		if _, err := container.Sync(ctx); err != nil {
			return fmt.Errorf("%s: %w", ch.name, err)
		}
	}
	return nil
}

func checkTypeScript(ctx context.Context, client *dagger.Client, repo *dagger.Directory) error {
	type tsChapter struct {
		name    string
		hasTest bool
	}
	chapters := []tsChapter{
		{"ch04-execution-singleton", true},
		{"ch09-durable-observer", true},
	}
	npmCache := client.CacheVolume("npm-cache")

	for _, ch := range chapters {
		dir := fmt.Sprintf("examples/%s/typescript", ch.name)
		container := client.Container().
			From("node:22").
			WithMountedCache("/root/.npm", npmCache).
			WithDirectory("/src", repo.Directory(dir)).
			WithWorkdir("/src").
			WithExec([]string{"npm", "install"})

		if ch.hasTest {
			fmt.Printf("  testing %s...\n", ch.name)
			container = container.
				WithExec([]string{"npx", "tsc", "--noEmit"}).
				WithExec([]string{"npm", "test"})
		} else {
			fmt.Printf("  type-checking %s...\n", ch.name)
			container = container.WithExec([]string{"npx", "tsc", "--noEmit"})
		}

		if _, err := container.Sync(ctx); err != nil {
			return fmt.Errorf("%s: %w", ch.name, err)
		}
	}
	return nil
}

func checkDotnet(ctx context.Context, client *dagger.Client, repo *dagger.Directory) error {
	nugetCache := client.CacheVolume("nuget-cache")
	base := client.Container().
		From("mcr.microsoft.com/dotnet/sdk:8.0").
		WithMountedCache("/root/.nuget/packages", nugetCache)

	// ch05-saga: test project references main project
	fmt.Printf("  testing ch05-saga...\n")
	_, err := base.
		WithDirectory("/src", repo.Directory("examples/ch05-saga/dotnet")).
		WithWorkdir("/src").
		WithExec([]string{"dotnet", "test", "SagaExample.Tests/SagaExample.Tests.csproj", "--nologo"}).
		Sync(ctx)
	if err != nil {
		return fmt.Errorf("ch05-saga: %w", err)
	}

	// ch10-caller: build only (Nexus caller can't be unit tested)
	fmt.Printf("  building ch10-caller...\n")
	_, err = base.
		WithDirectory("/src", repo.Directory("examples/ch10-cross-boundary-nexus/dotnet/CallerService")).
		WithWorkdir("/src").
		WithExec([]string{"dotnet", "build", "--nologo"}).
		Sync(ctx)
	if err != nil {
		return fmt.Errorf("ch10-caller: %w", err)
	}

	// ch10-handler: test project references main project
	fmt.Printf("  testing ch10-handler...\n")
	_, err = base.
		WithDirectory("/src", repo.Directory("examples/ch10-cross-boundary-nexus/dotnet")).
		WithWorkdir("/src").
		WithExec([]string{"dotnet", "test", "HandlerService.Tests/HandlerService.Tests.csproj", "--nologo"}).
		Sync(ctx)
	if err != nil {
		return fmt.Errorf("ch10-handler: %w", err)
	}

	return nil
}

func checkIncludes(ctx context.Context, client *dagger.Client, repo *dagger.Directory) error {
	_, err := client.Container().
		From("python:3.12-slim").
		WithDirectory("/repo", repo).
		WithWorkdir("/repo").
		WithExec([]string{"python3", "scripts/check-includes.py"}).
		Sync(ctx)
	return err
}
