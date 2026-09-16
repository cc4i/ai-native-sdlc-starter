#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

echo "  - Checking directory structure..."
DOCS_PREFIX=""
if [ -d "docs/intent" ]; then
    DOCS_PREFIX="docs/"
    REQUIRED_DIRS=("docs/intent" "docs/specs" "docs/plans" "docs/reviews" "docs/templates" "evals" ".agents/skills" ".gemini/skills" ".gemini/agents")
else
    REQUIRED_DIRS=("intent" "specs" "plans" "reviews" "evals" "templates" ".agents/skills" ".gemini/skills" ".gemini/agents")
fi

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        echo "  ❌ Missing required directory: $dir"
        exit 1
    fi
done

echo "  - Verifying spec -> intent traceability..."
for spec in ${DOCS_PREFIX}specs/[0-9][0-9][0-9]-*.md; do
    if [ -f "$spec" ] && ! grep -q "Linked Intent" "$spec"; then
        echo "  ⚠️  Warning: Spec $spec is missing a 'Linked Intent' reference."
    fi
done

echo "  - Verifying plan -> spec traceability..."
for plan in ${DOCS_PREFIX}plans/[0-9][0-9][0-9]-*.md; do
    if [ -f "$plan" ] && ! grep -q "Linked Spec" "$plan"; then
        echo "  ⚠️  Warning: Plan $plan is missing a 'Linked Spec' reference."
    fi
done

echo "  ✓ Artifact chain structure verified."
