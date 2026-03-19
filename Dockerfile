FROM node:22.22.0-bookworm-slim AS builder

# Pinned versions
ARG UV_VERSION=0.7.8
ARG ANTORA_VERSION=3.1.14
ARG GRAPHVIZ_VERSION=2.43.0-1+b1
ARG PLANTUML_VERSION=1:1.2022.13+ds-3

# System dependencies (pinned where apt supports it)
RUN apt-get update -qq && \
    apt-get install -y -qq --no-install-recommends \
        curl \
        git \
        graphviz \
        default-jre-headless \
        plantuml \
        python3 \
        python3-venv \
        fonts-urw-base35 \
    && rm -rf /var/lib/apt/lists/* \
    && fc-cache -f

# uv (pinned)
RUN curl -LsSf https://astral.sh/uv/${UV_VERSION}/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# Antora (pinned)
RUN npm install -g @antora/cli@${ANTORA_VERSION} @antora/site-generator@${ANTORA_VERSION}

WORKDIR /repo

# Default: build the site
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["build"]
