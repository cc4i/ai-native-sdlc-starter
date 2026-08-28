#!/usr/bin/env bash
# ==============================================================================
# check-artifacts.sh - Verify Artifact Chain Integrity & Traceability
# ==============================================================================

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

echo "  - Checking directory structure..."

# Support canonical docs/ hierarchy with fallback to root folders
DOCS_PREFIX=""
if [ -d "docs/intent" ]; then
    DOCS_PREFIX="docs/"
    REQUIRED_DIRS=("docs/intent" "docs/specs" "docs/plans" "docs/reviews" "docs/templates" "evals" ".gemini/skills" ".gemini/agents")
else
    REQUIRED_DIRS=("intent" "specs" "plans" "reviews" "evals" "templates" ".gemini/skills" ".gemini/agents")
fi

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        echo "  ❌ Missing required directory: $dir"
        exit 1
    fi
done

# Check that every spec references an intent
echo "  - Verifying spec -> intent traceability..."
for spec in ${DOCS_PREFIX}specs/[0-9][0-9][0-9]-*.md; do
    if [ -f "$spec" ]; then
        if ! grep -qi "Linked Intent" "$spec"; then
            echo "  ⚠️  Warning: Spec $spec is missing a 'Linked Intent' reference."
        fi
    fi
done

# Check that every plan references a spec and completed plans have shipped commit
echo "  - Verifying plan -> spec traceability and shipped status..."
for plan in ${DOCS_PREFIX}plans/[0-9][0-9][0-9]-*.md; do
    if [ -f "$plan" ]; then
        if ! grep -qi "Linked Spec" "$plan"; then
            echo "  ⚠️  Warning: Plan $plan is missing a 'Linked Spec' reference."
        fi

        # Shipped commit verification: completed plans must track shipped: <SHA>
        if grep -qi "Status:.*Complete" "$plan"; then
            if ! grep -qi "Shipped:" "$plan"; then
                echo "  ⚠️  Warning: Completed plan $plan is missing 'Shipped: <SHA>' commit hash."
            fi
        fi
    fi
done

# Check CodeGraph knowledge index status
if [ -d ".codegraph" ]; then
    echo "  ✓ CodeGraph knowledge index active (.codegraph/ detected)."
fi

echo "  ✓ Artifact chain structure verified."
