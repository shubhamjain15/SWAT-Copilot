# syntax=docker/dockerfile:1
FROM mambaorg/micromamba:1.5.8-focal
SHELL ["/bin/bash", "-lc"]

# IMPORTANT: be root for build-time steps (kept till end)
USER root

# Copy env early for caching
COPY --chown=mambauser:mambauser .devcontainer/environment.yml /tmp/environment.yml

# Basics
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends git curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Pre-create workspace so the wrapper doesn't choke
RUN mkdir -p /workspaces && chown -R 1000:1000 /workspaces

# Workdir (Dev Containers will mount your repo here)
WORKDIR /workspaces/SWAT-Copilot
