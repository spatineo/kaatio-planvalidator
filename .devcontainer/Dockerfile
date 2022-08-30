# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.234.0/containers/python-3/.devcontainer/base.Dockerfile

# Python version: 3, 3.10, 3.9, 3.8, 3.7, 3.6, 3-bullseye, 3.10-bullseye, 3.9-bullseye, 3.8-bullseye, 3.7-bullseye, 3.6-bullseye, 3-buster, 3.10-buster, 3.9-buster, 3.8-buster, 3.7-buster, 3.6-buster
# Use -bullseye variants on local arm64/Apple Silicon)
ARG VARIANT="3.10-bullseye"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

# Node.js version: none, lts/*, 16, 14, 12, 10
ARG NODE_VERSION="lts/*"
RUN if [ "${NODE_VERSION}" != "none" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi

# Default Python requirements.
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
RUN pip --no-cache-dir install \
    poetry

# Default OS packages.
RUN export DEBIAN_FRONTEND=noninteractive \
    && apt update \
    && apt upgrade -yqq \
    && apt install -yqq \
    apt-transport-https \
    ca-certificates \
    curl \
    gdal-bin \
    fzf \
    software-properties-common \
    tar \
    tree \
    unzip \
    vim \
    zip

# Swith user
USER vscode

# Default environment variables.
ENV LOCAL_BIN=/home/vscode/.local/bin
ENV PATH=$LOCAL_BIN:$PATH

# Local binaries.
# TODO: figure out why docker works with sudo on builds but not without sudo!
RUN mkdir -p $LOCAL_BIN \
    && echo "npx --yes aws-cdk@1.x \$@" > $LOCAL_BIN/cdk1 \
    && echo "npx --yes aws-cdk@2.x \$@" > $LOCAL_BIN/cdk2 \
    && echo "sudo docker $@" > $LOCAL_BIN/docker \ 
    && chmod +x $LOCAL_BIN/*

# Modify PROMPT_DIRTRIM in .bashrc
RUN sed -i 's|PROMPT_DIRTRIM=4|PROMPT_DIRTRIM=2|' ~/.bashrc

# Add FZF setup to .bashrc
RUN echo "# FZF" >> ~/.bashrc \
    && echo "source /usr/share/doc/fzf/examples/completion.bash" >> ~/.bashrc \
    && echo "source /usr/share/doc/fzf/examples/key-bindings.bash" >> ~/.bashrc
