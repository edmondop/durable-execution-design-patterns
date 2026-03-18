package main

import (
	"context"
	"fmt"
	"os"

	"dagger.io/dagger"
)

func main() {
	cmd := "check"
	if len(os.Args) > 1 {
		cmd = os.Args[1]
	}

	ctx := context.Background()
	client, err := dagger.Connect(ctx, dagger.WithLogOutput(os.Stderr))
	if err != nil {
		fmt.Fprintf(os.Stderr, "dagger connect: %v\n", err)
		os.Exit(1)
	}
	defer client.Close()

	repo := client.Host().Directory("..", dagger.HostDirectoryOpts{
		Exclude: []string{
			"_build",
			".git",
			"dagger",
			"node_modules",
			"diagrams/rendered",
		},
	})

	switch cmd {
	case "check":
		if err := check(ctx, client, repo); err != nil {
			fmt.Fprintf(os.Stderr, "check failed: %v\n", err)
			os.Exit(1)
		}
	default:
		fmt.Fprintf(os.Stderr, "unknown command: %s\n", cmd)
		os.Exit(1)
	}
}

func check(ctx context.Context, client *dagger.Client, repo *dagger.Directory) error {
	fmt.Println("=== Checking Go examples (ch01, ch06) ===")
	if err := checkGo(ctx, client, repo); err != nil {
		return fmt.Errorf("go: %w", err)
	}

	fmt.Println("=== Checking Python examples (ch02, ch07) ===")
	if err := checkPython(ctx, client, repo); err != nil {
		return fmt.Errorf("python: %w", err)
	}

	fmt.Println("=== Checking Java examples (ch03, ch08) ===")
	if err := checkJava(ctx, client, repo); err != nil {
		return fmt.Errorf("java: %w", err)
	}

	fmt.Println("=== Checking TypeScript examples (ch04, ch09) ===")
	if err := checkTypeScript(ctx, client, repo); err != nil {
		return fmt.Errorf("typescript: %w", err)
	}

	fmt.Println("=== Checking .NET examples (ch05, ch10) ===")
	if err := checkDotnet(ctx, client, repo); err != nil {
		return fmt.Errorf("dotnet: %w", err)
	}

	fmt.Println("=== Checking AsciiDoc include tags ===")
	if err := checkIncludes(ctx, client, repo); err != nil {
		return fmt.Errorf("includes: %w", err)
	}

	fmt.Println("=== All checks passed ===")
	return nil
}
