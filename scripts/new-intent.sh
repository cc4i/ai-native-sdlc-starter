#!/usr/bin/env bash
# ==============================================================================
# new-intent.sh - Scaffold a new Stage 1 Intent Markdown Artifact
# ==============================================================================

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

TITLE="${1:-}"

if [ -z "$TITLE" ]; then
    echo "Usage: $0 <feature-name-or-title>"
    echo "Example: $0 \"User Claims Status Self-Service\""
    exit 1
fi

# Detect directory target: prefer docs/intent/
INTENT_DIR="intent"
TEMPLATE_FILE="templates/intent.template.md"

if [ -d "docs/intent" ]; then
    INTENT_DIR="docs/intent"
    TEMPLATE_FILE="docs/templates/intent.template.md"
fi

# Generate slug
SLUG=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g' | sed -E 's/^-+|-+$//g')

# Calculate next sequence number
EXISTING_COUNT=$(find "$INTENT_DIR" -maxdepth 1 -name "[0-9][0-9][0-9]-*.md" | wc -l | tr -d ' ')
NEXT_NUM=$(printf "%03d" $((EXISTING_COUNT + 1)))

TARGET_FILE="${INTENT_DIR}/${NEXT_NUM}-${SLUG}.md"

if [ -f "$TARGET_FILE" ]; then
    echo "❌ Error: File $TARGET_FILE already exists."
    exit 1
fi

DATE_TODAY=$(date +"%Y-%m-%d")

# Copy template and replace title & date
sed -e "s/\[Short Feature \/ Improvement Title\]/${TITLE}/g" \
    -e "s/\[YYYY-MM-DD\]/${DATE_TODAY}/g" \
    "$TEMPLATE_FILE" > "$TARGET_FILE"

echo "✅ Created new intent artifact: $TARGET_FILE"
echo "👉 Next Step: Open Antigravity and brainstorm requirements using /grill-me!"
