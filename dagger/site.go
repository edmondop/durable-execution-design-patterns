package main

import (
	"context"
	"fmt"
	"os"

	"dagger.io/dagger"
)

func buildSite(ctx context.Context, client *dagger.Client, repo *dagger.Directory) error {
	uvCache := client.CacheVolume("uv-cache")
	npmCache := client.CacheVolume("npm-cache")

	// Base image with all system dependencies
	base := client.Container().
		From("node:22-bookworm").
		WithExec([]string{"apt-get", "update", "-qq"}).
		WithExec([]string{"apt-get", "install", "-y", "-qq",
			"graphviz", "plantuml", "python3", "python3-pip", "python3-venv", "git",
		}).
		WithExec([]string{"sh", "-c",
			"curl -LsSf https://astral.sh/uv/install.sh | sh",
		}).
		WithEnvVariable("PATH", "/root/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin").
		WithMountedCache("/root/.cache/uv", uvCache).
		WithMountedCache("/root/.npm", npmCache)

	// Mount the repo
	work := base.
		WithDirectory("/repo", repo).
		WithWorkdir("/repo")

	// Render Python diagrams
	fmt.Println("=== Rendering Python diagrams ===")
	work = work.WithExec([]string{"mkdir", "-p", "diagrams/rendered"}).
		WithExec([]string{"sh", "-c",
			`for f in diagrams/ch*.py diagrams/intro*.py; do
				[ -f "$f" ] || continue
				echo "  Rendering $(basename "$f" .py)..."
				uv run "$f"
			done`,
		})

	// Render PlantUML diagrams
	fmt.Println("=== Rendering PlantUML diagrams ===")
	work = work.WithExec([]string{"sh", "-c",
		`for f in diagrams/*.puml; do
			[ -f "$f" ] || continue
			echo "  Rendering $(basename "$f" .puml)..."
			plantuml -tsvg "$f" -o rendered/
		done`,
	})

	// Copy rendered SVGs to Antora images dir
	work = work.WithExec([]string{"sh", "-c",
		"cp diagrams/rendered/*.svg docs/modules/ROOT/images/",
	})

	// Build Antora site
	fmt.Println("=== Building Antora site ===")
	work = work.WithExec([]string{"npx", "antora", "antora-playbook.yml"})

	// Export the built site to host
	fmt.Println("=== Exporting site to _build/site/ ===")
	siteDir := work.Directory("/repo/_build/site")

	_, err := siteDir.Export(ctx, "../_build/site")
	if err != nil {
		return fmt.Errorf("export site: %w", err)
	}

	// Also export rendered diagrams so they can be committed
	renderedDir := work.Directory("/repo/diagrams/rendered")
	_, err = renderedDir.Export(ctx, "../diagrams/rendered")
	if err != nil {
		return fmt.Errorf("export diagrams: %w", err)
	}

	imagesDir := work.Directory("/repo/docs/modules/ROOT/images")
	_, err = imagesDir.Export(ctx, "../docs/modules/ROOT/images")
	if err != nil {
		return fmt.Errorf("export images: %w", err)
	}

	fmt.Println("=== Site built: _build/site/ ===")
	fmt.Println("Rendered diagrams exported to diagrams/rendered/ and docs/modules/ROOT/images/")

	// Check if user wants to serve
	if len(os.Args) > 2 && os.Args[2] == "--serve" {
		fmt.Println("Serving at http://localhost:8000/dedp/")
		_, err = work.
			WithExec([]string{"python3", "-m", "http.server", "8000", "--directory", "_build/site"}).
			WithExposedPort(8000).
			Sync(ctx)
		return err
	}

	return nil
}
