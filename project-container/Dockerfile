# ==================================================================
# BASE IMAGE
# ==================================================================
# This container builds on the AI assistant base image which includes
# Claude Code CLI and common development tools.
#
# See https://github.com/rise8-us/XPai/pkgs/container/xpai%2Fai-assistant-home
# Current base version: ai-assistant-home (digest pinned for reproducibility)
FROM ghcr.io/rise8-us/xpai/ai-assistant-home@sha256:179f0024131b091ef8d48e98a52a60f5e9bdeb60ca2aa8c2da62e1c445c4ef50

# ==================================================================
# TOOL VERSIONS
# ==================================================================
# Pin specific versions for reproducibility. Update as needed.
# Instructions are included of where to find the latest versions.
# This helps both humans and AI assistants maintain the file.

# NOTE: This is an example of how to pin a version for to make it easy for a AI to update later
# curl https://github.com/cli/cli/releases to get latest version
# ARG GH_CLI_VERSION=2.81.0

USER root
# Fix /tmp permissions after USER switch - required even though base image has this fix
# When switching USER contexts, /tmp permissions can be reset due to runc v1.1.8 and crun v1.11+ bugs
# This chmod must be present before any apt-get commands in each USER root context
# See: https://github.com/opencontainers/runc/issues/3952
#
# Install additional tools here as needed.
# The goal is to give the AI assistant all the tools that it needs to be productive.
# Keep the image as small as possible while still being useful to reduce CVE surface area.
# When possible, install tools as the non-root aiAssistant user.
# See https://docs.docker.com/build/building/best-practices/ for guidelines.
# ==================================================================
RUN chmod 1777 /tmp && \
    apt-get update && \
    apt-get install -y --no-install-recommends wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ==================================================================
# EXAMPLE: Install GitHub CLI (gh)
# ==================================================================
# Uncomment the lines below to add the GitHub CLI to your container.
# This example shows proper architecture detection and version pinning.
# Also uncomment the ARG GH_CLI_VERSION above.
#
# RUN ARCH=$(dpkg --print-architecture) && \
#     if [ "$ARCH" = "arm64" ]; then GH_ARCH="arm64"; else GH_ARCH="amd64"; fi && \
#     wget -O /tmp/gh.tar.gz "https://github.com/cli/cli/releases/download/v${GH_CLI_VERSION}/gh_${GH_CLI_VERSION}_linux_${GH_ARCH}.tar.gz" && \
#     tar -xzf /tmp/gh.tar.gz -C /tmp && \
#     mv /tmp/gh_${GH_CLI_VERSION}_linux_${GH_ARCH}/bin/gh /usr/local/bin/ && \
#     chmod +x /usr/local/bin/gh && \
#     rm -rf /tmp/gh*
# ==================================================================

# Switch back to non-root user to increase security.
USER aiAssistant
