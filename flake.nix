{
  description = "Durable Execution Design Patterns - Book & Examples";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
      in {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            # Book
            asciidoctor
            ruby_3_3
            graphviz

            # Languages
            go_1_22
            jdk21
            maven
            python312
            uv
            nodejs_22
            dotnet-sdk_8

            # Infrastructure
            kubernetes-helm
            kubectl
            kind

            # Quality
            pre-commit
            mise
            shellcheck
            actionlint
            golangci-lint
            ruff
          ];

          shellHook = ''
            echo "Durable Execution Design Patterns dev environment"
            echo ""
            echo "  mise run book          Build HTML + PDF"
            echo "  mise run test -- 01    Test chapter 1 examples"
            echo "  mise run test-all      Test all chapters"
            echo "  mise run diagrams      Render all diagrams"
            echo "  mise run lint          Lint all code"
            echo "  mise run k8s-up        Create Kind cluster + install Temporal"
            echo ""

            gem install asciidoctor-pdf rouge 2>/dev/null || true
          '';
        };
      });
}
