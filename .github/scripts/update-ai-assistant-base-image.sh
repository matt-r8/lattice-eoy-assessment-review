#!/bin/bash
set -e

# Update AI Assistant Base Image Script
# This script finds and updates all references to the AI assistant base container
# (ghcr.io/rise8-us/xpai/ai-assistant-home) to use a new SHA digest.
#
# Supports:
# - Dockerfiles (FROM lines)
# - devcontainer*.json files ("image" fields)
#
# Usage: ./update-ai-assistant-base-image.sh sha256:NEW_DIGEST

NEW_SHA="$1"

if [ -z "$NEW_SHA" ]; then
    echo "❌ Error: No SHA digest provided"
    echo "Usage: $0 sha256:<digest>"
    exit 1
fi

# Validate SHA format
if [[ ! "$NEW_SHA" =~ ^sha256:[a-f0-9]{64}$ ]]; then
    echo "❌ Error: Invalid SHA format. Expected: sha256:<64-char-hex>"
    echo "Got: $NEW_SHA"
    exit 1
fi

echo "🔄 Updating AI assistant base image references to: $NEW_SHA"
echo ""

BASE_IMAGE="ghcr.io/rise8-us/xpai/ai-assistant-home"
IMAGE_WITH_SHA="${BASE_IMAGE}@${NEW_SHA}"

# Counter for tracking changes
FILES_UPDATED=0
FILES_SKIPPED=0

# Function to update a Dockerfile
update_dockerfile() {
    local file="$1"
    local temp_file="${file}.tmp"

    if [ ! -f "$file" ]; then
        return
    fi

    # Check if file contains the base image reference
    if ! grep -q "$BASE_IMAGE" "$file"; then
        return
    fi

    # Update FROM lines in Dockerfile
    # Pattern matches: FROM ghcr.io/rise8-us/xpai/ai-assistant-home[@sha256:...]
    sed -E "s|FROM ${BASE_IMAGE}(@sha256:[a-f0-9]{64})?|FROM ${IMAGE_WITH_SHA}|g" "$file" > "$temp_file"

    # Check if the file actually changed
    if cmp -s "$file" "$temp_file"; then
        echo "⏭️  Skipping $file (already up to date)"
        rm "$temp_file"
        FILES_SKIPPED=$((FILES_SKIPPED + 1))
    else
        mv "$temp_file" "$file"
        echo "✅ Updated $file"
        FILES_UPDATED=$((FILES_UPDATED + 1))
    fi
}

# Function to update a devcontainer JSON file
update_devcontainer_json() {
    local file="$1"
    local temp_file="${file}.tmp"

    if [ ! -f "$file" ]; then
        return
    fi

    # Check if file contains the base image reference
    if ! grep -q "$BASE_IMAGE" "$file"; then
        return
    fi

    # Update "image" field in JSON
    # Pattern matches: "image": "ghcr.io/rise8-us/xpai/ai-assistant-home[@sha256:...]"
    sed -E "s|\"image\"[[:space:]]*:[[:space:]]*\"${BASE_IMAGE}(@sha256:[a-f0-9]{64})?\"|\"image\": \"${IMAGE_WITH_SHA}\"|g" "$file" > "$temp_file"

    # Check if the file actually changed
    if cmp -s "$file" "$temp_file"; then
        echo "⏭️  Skipping $file (already up to date)"
        rm "$temp_file"
        FILES_SKIPPED=$((FILES_SKIPPED + 1))
    else
        mv "$temp_file" "$file"
        echo "✅ Updated $file"
        FILES_UPDATED=$((FILES_UPDATED + 1))
    fi
}

# Update Dockerfiles
echo "📦 Checking Dockerfiles..."
if [ -f "project-container/Dockerfile" ]; then
    update_dockerfile "project-container/Dockerfile"
fi
echo ""

# Update devcontainer.json files
echo "🐳 Checking devcontainer files..."
for devcontainer_file in .devcontainer/devcontainer*.json; do
    if [ -f "$devcontainer_file" ]; then
        update_devcontainer_json "$devcontainer_file"
    fi
done
echo ""

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Summary:"
echo "   ✅ Files updated: $FILES_UPDATED"
echo "   ⏭️  Files skipped: $FILES_SKIPPED"
echo "   🎯 Target SHA: $NEW_SHA"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ "$FILES_UPDATED" -eq 0 ]; then
    echo ""
    echo "ℹ️  No files were updated. This could mean:"
    echo "   • All files are already using the specified SHA"
    echo "   • No files contain references to the AI assistant base image"
    exit 0
fi

echo ""
echo "✅ AI assistant base image update completed successfully"
