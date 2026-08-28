#!/usr/bin/env bash
# ==============================================================================
# release.sh - AI-Native SDLC Release Management Script
# ==============================================================================
# Automates semantic version tagging, verification, and release preparation.
#
# Usage:
#   bash scripts/release.sh <vX.Y.Z> [--dry-run] [--skip-verify]
# ==============================================================================

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

BOLD="\033[1m"
GREEN="\033[0;32m"
BLUE="\033[0;34m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
RESET="\033[0m"

VERSION="${1:-}"
DRY_RUN=false
SKIP_VERIFY=false

for arg in "$@"; do
    case "$arg" in
        --dry-run)
            DRY_RUN=true
            ;;
        --skip-verify)
            SKIP_VERIFY=true
            ;;
    esac
done

if [ -z "$VERSION" ] || [ "$VERSION" = "--dry-run" ]; then
    echo -e "${RED}Error: Version argument required (e.g. v1.1.0).${RESET}"
    echo "Usage: $0 <vX.Y.Z> [--dry-run] [--skip-verify]"
    exit 1
fi

# Validate Semantic Versioning Format: vX.Y.Z or vX.Y.Z-tag
SEMVER_REGEX="^v[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9.]+)?$"
if [[ ! "$VERSION" =~ $SEMVER_REGEX ]]; then
    echo -e "${RED}Error: Invalid version format '$VERSION'. Must match 'vX.Y.Z' (e.g. v1.1.0).${RESET}"
    exit 1
fi

CLEAN_VERSION="${VERSION#v}"

echo -e "${BLUE}${BOLD}🚀 [AI-Native SDLC Release] Preparing release ${VERSION}...${RESET}"

if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}ℹ️  Dry run mode enabled. Validating configuration...${RESET}"
    echo "  - Target Tag: $VERSION"
    echo "  - Clean Version: $CLEAN_VERSION"
    echo "  ✓ Version syntax valid."
    echo -e "${GREEN}✓ Dry run completed successfully.${RESET}"
    exit 0
fi

# 1. Verify working tree is clean
if ! git diff --quiet || ! git diff --cached --quiet; then
    echo -e "${RED}❌ Error: Working tree has uncommitted changes. Please commit or stash them first.${RESET}"
    exit 1
fi

# 2. Check if tag already exists
if git rev-parse "$VERSION" >/dev/null 2>&1; then
    echo -e "${RED}❌ Error: Git tag '$VERSION' already exists.${RESET}"
    exit 1
fi

# 3. Run verification harness
if [ "$SKIP_VERIFY" = false ]; then
    echo -e "${BLUE}🧪 Running full verification loop before release...${RESET}"
    bash ./scripts/verify.sh
fi

# 4. Update pyproject.toml version
if [ -f "pyproject.toml" ]; then
    sed -i.bak -E "s/^version = \".*\"/version = \"$CLEAN_VERSION\"/" pyproject.toml
    rm -f pyproject.toml.bak
    if command -v uv >/dev/null 2>&1; then
        uv lock --quiet 2>/dev/null || true
    fi
    if ! git diff --quiet pyproject.toml; then
        git add pyproject.toml uv.lock 2>/dev/null || git add pyproject.toml
        git commit -m "chore(release): bump version to $VERSION"
    fi
fi

# 5. Create Annotated Git Tag
git tag -a "$VERSION" -m "Release $VERSION - AI-Native SDLC"
echo -e "${GREEN}${BOLD}✅ Release tag '$VERSION' created successfully!${RESET}"
echo ""
echo "To publish this release to GitHub and trigger release workflow, run:"
echo -e "  ${CYAN}git push origin $VERSION${RESET}"
