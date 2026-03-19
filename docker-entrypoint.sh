#!/usr/bin/env bash
set -euo pipefail

render_diagrams() {
    echo "=== Rendering diagrams ==="
    mkdir -p diagrams/rendered
    for f in diagrams/ch*.py diagrams/intro*.py; do
        [ -f "$f" ] || continue
        echo "  $(basename "$f" .py)..."
        uv run "$f"
    done
    for f in diagrams/*.puml; do
        [ -f "$f" ] || continue
        echo "  $(basename "$f" .puml)..."
        plantuml -tsvg "$f" -o rendered/
    done
    cp diagrams/rendered/*.svg docs/modules/ROOT/images/
}

build_site() {
    render_diagrams
    echo "=== Building Antora site ==="
    antora antora-playbook.yml
    echo "=== Site built: _build/site/ ==="
}

check_diagrams() {
    echo "=== Checking diagrams are up to date ==="
    # Save current committed images
    local tmp
    tmp=$(mktemp -d)
    cp docs/modules/ROOT/images/*.svg "$tmp/"

    # Re-render
    render_diagrams

    # Diff
    local changed=0
    for f in docs/modules/ROOT/images/*.svg; do
        local name
        name=$(basename "$f")
        if ! diff -q "$f" "$tmp/$name" >/dev/null 2>&1; then
            echo "STALE: $name — re-render diagrams and commit"
            changed=1
        fi
    done

    rm -rf "$tmp"

    if [ "$changed" -eq 1 ]; then
        echo ""
        echo "Committed SVGs are stale. Run 'mise run build' and commit the results."
        exit 1
    fi
    echo "All SVGs are up to date."
}

case "${1:-build}" in
    build)
        build_site
        ;;
    diagrams)
        render_diagrams
        ;;
    check)
        check_diagrams
        ;;
    shell)
        exec /bin/bash
        ;;
    *)
        echo "Usage: $0 {build|diagrams|check|shell}"
        exit 1
        ;;
esac
