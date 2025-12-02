# Container Build and Management

This directory contains all assets needed to build and manage the project specific container.

## Overview

**Why a Project-Specific Container?**

The base `ai-assistant-home` image provides Claude Code CLI and common development tools. However, most projects need additional tools specific to their technology stack. This directory allows you to:

- **Add project-specific tools** (e.g., language runtimes, build tools, CLIs)
- **Install custom dependencies** (e.g., Python packages, Node modules)
- **Configure project environment** (e.g., environment variables, PATH settings)

**Example:** The [XPai repository's `.devcontainer/Dockerfile`](https://github.com/rise8-us/XPai/blob/main/.devcontainer/Dockerfile) extends the base image by adding:
- GitHub CLI for repository management
- Chromium for browser automation
- Mermaid CLI for diagram generation
- Python tools (UV, LLM, yamllint)
- Build tools (g++, xvfb)

**Workflow-First Approach**: This starter uses pre-built container images published by GitHub workflows. The `.devcontainer/devcontainer.json` files reference images by digest (SHA256), ensuring reproducible builds and faster container startup times.

**Benefits:**
- **Fast startup**: Pull pre-built images instead of building locally (seconds vs minutes)
- **Tested images**: Workflow runs security scans and validation before publishing
- **Reproducible**: Digest pinning ensures everyone uses the exact same image
- **CI/CD ready**: Same container can be used in development and automated workflows

## Directory Structure

- **Dockerfile** - Container image definition
- **.trivyignore** - Security scan configuration
- **test.sh** - Container validation script

## Quick Start

### 1. Use Pre-built Container

The `.devcontainer/devcontainer.json` files reference pre-built images from GitHub Container Registry. The GitHub workflow automatically builds and publishes images when you push changes to `project-container/` directory.

**First-time setup:**
1. Push container changes to trigger workflow build
2. Wait for `.github/workflows/build-project-container.yml` to complete
3. Update `.devcontainer/devcontainer.json` with the new image digest
4. Open in VS Code: Command Palette → "Dev Containers: Reopen in Container"

### 2. Local Development (Optional)

For testing Dockerfile changes locally before pushing:

```bash
# Test with podman (default)
project-container/test.sh

# Temporarily use local build in devcontainer.json:
# Replace "image": "ghcr.io/..." with "image": "test-project-container:latest"
```

## Customization

### Adding Tools

1. Edit `Dockerfile`:
   ```dockerfile
   # Add after existing tool installations
   RUN apt-get update && apt-get install -y \
       your-tool \
       another-tool
   ```

2. Push changes to trigger workflow build:
   ```bash
   git add project-container/Dockerfile
   git commit -m "Add new tools to container"
   git push
   ```

3. Wait for workflow to complete and update devcontainer.json with new digest

### Adding Tests

1. Edit `test.sh` and add your test in the customization section:
   ```bash
   echo "Testing my-tool..."
   MY_TOOL_VERSION=$(podman run --rm $IMAGE_TAG /bin/bash -c "my-tool --version" 2>&1) || {
     echo "❌ ERROR: my-tool not installed or not working: $MY_TOOL_VERSION"
     exit 1
   }
   echo "✅ my-tool: $MY_TOOL_VERSION"
   ```

2. The workflow will automatically run tests on each build

## Security Scanning

Run Trivy scan:
```bash
trivy image --severity CRITICAL,HIGH my-container:latest
```

Accepted vulnerabilities are documented in `.trivyignore`.

## Troubleshooting

See main repository documentation: `docs/TROUBLESHOOTING.md`

### Common Issues

#### Build fails with permission denied
- Check that you have permission to build containers
- On macOS with podman, ensure the podman machine is running: `podman machine start`

#### Container fails to start
- Check logs: `podman logs <container-name>`
- Verify environment variables are set correctly in `.devcontainer/devcontainer.json`
- Ensure required ports are not already in use

#### Tools not found in container
- Verify tools are installed in Dockerfile
- Run tests to validate: `IMAGE_TAG=test-container project-container/test.sh`
- Check that PATH is set correctly in container

## Additional Resources

- [DevContainer Specification](https://containers.dev/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Trivy Documentation](https://aquasecurity.github.io/trivy/)
