# GitHub Workflows

## Overview

Automated workflows for building, testing, and securing your project container.

**Workflows:**
- `build-project-container.yml` - Builds and publishes multi-arch container images
- `nightly-project-container-scan.yml` - Daily security vulnerability scanning
- `update-base-container-on-new-version.yml` - Auto-updates AI assistant base container references

**Actions:**
- `.github/actions/setup-container-build/` - Multi-arch build environment setup
- `.github/actions/trivy-scan/` - Security vulnerability scanning
- `.github/actions/create-automated-pr/` - Automated PR creation with bot identity

**Scripts:**
- `.github/scripts/update-ai-assistant-base-image.sh` - Updates base image SHA references

## Quick Start

To use these workflows in your project, copy the following from the starter template:

```bash
# From your project root, copy workflows, actions, and scripts
cp -r starter/.github/workflows/*.yml .github/workflows/
cp -r starter/.github/actions/* .github/actions/
cp -r starter/.github/scripts .github/
chmod +x .github/scripts/*.sh
```

**Important:** The `update-base-container-on-new-version.yml` workflow requires the script at `.github/scripts/update-ai-assistant-base-image.sh`. Make sure to copy both the workflows AND the scripts directory.

## Setup Requirements

### 1. Enable GitHub Container Registry

To allow workflows to publish container images:

**Repository Settings → Actions → General → Workflow permissions:**
- ✅ Read and write permissions

This grants workflows permission to push images to `ghcr.io`.

### 2. Configure GitHub App for Automated Updates (Optional)

The `update-base-container-on-new-version.yml` workflow requires a GitHub App for bot authentication. This allows the bot to create PRs that trigger other workflows (regular `GITHUB_TOKEN` cannot do this).

**Note:** Organization owners should perform this setup.

#### Create Organization GitHub App

1. **Go to Organization Settings → Developer settings → GitHub Apps → New GitHub App**
   - Or visit: `https://github.com/organizations/YOUR-ORG/settings/apps/new`

2. **Configure the app:**
   - **GitHub App name**: `rise8-ai-assistant-pr-bot` (must be unique across GitHub)
   - **Homepage URL**: Your organization URL
   - **Webhook**: Uncheck "Active"
   - **Permissions** (Repository permissions):
     - ✅ Contents: Read and write
     - ✅ Pull requests: Read and write
     - ✅ Metadata: Read-only (automatically added)
   - **Where can this GitHub App be installed?**: Only on this account

3. **After creation:**
   - Note the **App ID**
   - Click **Generate a private key**
   - Save the `.pem` file securely

4. **Install the app:**
   - App settings → Install App
   - Choose "All repositories" OR "Only select repositories"
   - Click Install

**IMPORTANT:** The GitHub App MUST be installed on your repository for the workflow to function. If using "Only select repositories", you must explicitly add each repository that needs automated updates. See the "Update Workflow Fails with 'Not Found' (404) Error" troubleshooting section below if you encounter issues.

#### Add Organization Secrets

**Organization Settings → Secrets and variables → Actions → New organization secret:**

1. `AI_ASSISTANT_PR_BOT_APP_ID`
   - Value: The App ID from step 3
   - Repository access: "All repositories" OR "Selected repositories"

2. `AI_ASSISTANT_PR_BOT_PRIVATE_KEY`
   - Value: Entire contents of the `.pem` file
   - Repository access: Same as above

**Note:** Ensure the GitHub App is installed on the same repositories that have access to these secrets.

**That's it!** All repositories with access to these secrets can now use the auto-update workflow. No per-repo configuration needed.

#### Testing

Actions tab → "Update Base Container For New Version" → Run workflow

#### If You Don't Want Automated Updates

Remove or disable `update-base-container-on-new-version.yml`

## Using Built Images

### In DevContainer

Update `.devcontainer/devcontainer*.json` with the published image digest:

```json
{
  "image": "ghcr.io/YOUR-ORG/YOUR-REPO/project-container@sha256:YOUR-DIGEST"
}
```

Get digest from workflow output or:
```bash
podman inspect ghcr.io/YOUR-ORG/YOUR-REPO/project-container:latest | grep Digest
```

### Direct Usage

```bash
podman pull ghcr.io/YOUR-ORG/YOUR-REPO/project-container:latest
podman run -it --rm ghcr.io/YOUR-ORG/YOUR-REPO/project-container:latest
```

## Accepting Known Vulnerabilities

Add accepted CVEs to `project-container/.trivyignore` with documentation:

```
# CVE-YYYY-XXXXX - Brief description
# Risk: Low/Medium - Why it's acceptable
# Review: YYYY-MM-DD
CVE-YYYY-XXXXX
```

## Troubleshooting

### Can't Pull Images Locally

```bash
gh auth login -s read:packages
gh auth token | podman login ghcr.io -u $(gh api user --jq .login) --password-stdin
```

### Workflow Can't Push Images

Check: Repository Settings → Actions → General → Workflow permissions
- Must be "Read and write permissions"

### Update Workflow Fails with "Not Found" (404) Error

**Error message:**
```
Failed to create token for "your-repo" (attempt 4): Not Found - https://docs.github.com/rest/apps/apps#get-a-repository-installation-for-the-authenticated-app
RequestError [HttpError]: Not Found
```

**Root cause:** The GitHub App is not installed on your repository.

**Solution:**

1. **Verify GitHub App secrets exist:**
   - Check that `AI_ASSISTANT_PR_BOT_APP_ID` and `AI_ASSISTANT_PR_BOT_PRIVATE_KEY` are configured
   - Navigate to: Organization Settings → Secrets and variables → Actions
   - Confirm your repository has access to these secrets

2. **Install the GitHub App on your repository:**
   - Go to: `https://github.com/organizations/YOUR-ORG/settings/installations`
   - Click on the AI Assistant PR Bot app
   - Click "Configure"
   - Under "Repository access":
     - Either select "All repositories"
     - Or add your specific repository to "Only select repositories"
   - Click "Save"

3. **Verify the installation:**
   - Re-run the workflow: Actions tab → "Update Base Container For New Version" → Run workflow
   - The workflow should now complete successfully

**Note:** If you don't see the GitHub App in your organization's installations, you need to create it first. See "Configure GitHub App for Automated Updates" section above.

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Trivy Documentation](https://aquasecurity.github.io/trivy/)
- [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
