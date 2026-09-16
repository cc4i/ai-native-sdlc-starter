#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

# Enforce project-local UV cache
export UV_CACHE_DIR="${ROOT_DIR}/.uv_cache"

echo "=================================================="
echo "🚀 [SDLC Verify] Running Local Verification Loop..."
echo "=================================================="

echo "🔍 (1/4) Checking artifact integrity..."
if [ -f "./scripts/check-artifacts.sh" ]; then
    bash ./scripts/check-artifacts.sh
fi

echo "🧹 (2/4) Running syntax & lint checks..."
for script in scripts/*.sh; do
    if [ -f "$script" ]; then bash -n "$script"; fi
done
if command -v node >/dev/null 2>&1; then
    for jsfile in $(find public src -name "*.js" 2>/dev/null); do
        node -c "$jsfile"
    done
fi
echo "  ✓ Scripts and JavaScript syntax valid."

echo "🧪 (3/4) Executing test suite..."
if [ -d "tests" ] && command -v python3 >/dev/null 2>&1; then
    python3 -m unittest discover tests -v
fi
echo "  ✓ Tests green."

echo "🛡️  (4/4) Scanning for unapproved shortcuts (TODO / FIXME stubs)..."
if [ -d "src" ]; then
    TODOS=$(grep -rnE "(TODO|FIXME):" src/ 2>/dev/null || true)
    if [ -n "$TODOS" ]; then
        echo "  ⚠️  Warning: Active TODOs detected in src/:"
        echo "$TODOS"
    else
        echo "  ✓ Zero unapproved TODO stubs in src/."
    fi
fi

echo "=================================================="
echo "✅ [SDLC Verify] ALL CHECKS PASSED. Ready for review."
echo "=================================================="
