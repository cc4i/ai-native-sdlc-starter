#!/usr/bin/env bash
# ==============================================================================
# check-artifacts.sh - Verify Artifact Chain Integrity & Traceability
# ==============================================================================

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

echo "  - Checking directory structure..."

REQUIRED_DIRS=("intent" "specs" "plans" "evals" "templates" ".gemini/skills" ".gemini/agents")

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        echo "  ❌ Missing required directory: $dir"
        exit 1
    fi
done

# Check that every spec references an intent
echo "  - Verifying spec -> intent traceability..."
for spec in specs/[0-9][0-9][0-9]-*.md; do
    if [ -f "$spec" ]; then
        if ! grep -q "Linked Intent" "$spec"; then
            echo "  ⚠️  Warning: Spec $spec is missing a 'Linked Intent' reference."
        fi
    fi
done

# Check that every plan references a spec
echo "  - Verifying plan -> spec traceability..."
for plan in plans/[0-9][0-9][0-9]-*.md; do
    if [ -f "$plan" ]; then
        if ! grep -q "Linked Spec" "$plan"; then
            echo "  ⚠️  Warning: Plan $plan is missing a 'Linked Spec' reference."
        fi
    fi
done

echo "  ✓ Artifact chain structure verified."
