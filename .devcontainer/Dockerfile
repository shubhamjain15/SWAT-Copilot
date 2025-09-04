FROM mambaorg/micromamba:1.5.8-focal
ARG MAMBA_DOCKERFILE_ACTIVATE=1
COPY --chown=$MAMBA_USER:$MAMBA_USER environment.yml /tmp/environment.yml
RUN micromamba install -y -n base -f /tmp/environment.yml && micromamba clean -a -y
WORKDIR /workspaces/SWAT-Copilot
ENV PYTHONPATH=/workspaces/SWAT-Copilot/src
