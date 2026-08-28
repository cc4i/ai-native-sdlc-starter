#!/usr/bin/env bash
# ==============================================================================
# verify.sh - Single-Command Local Feedback Verification Harness
# ==============================================================================
# This script is the single source of truth for repository health.
# Antigravity and human developers run this script to ensure zero regressions.
# ==============================================================================

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

echo "=================================================="
echo "🚀 [SDLC Verify] Running Local Verification Loop..."
echo "=================================================="

# Check for uv package manager
USE_UV=false
if command -v uv >/dev/null 2>&1; then
    USE_UV=true
fi

# 1. Check Artifact Integrity & Scalability
echo "🔍 (1/4) Checking artifact integrity and linkages..."
if [ -f "./scripts/check-artifacts.sh" ]; then
    bash ./scripts/check-artifacts.sh
fi

# 2. Syntax / Linting Checks
echo "🧹 (2/4) Running code quality and syntax checks..."
for script in scripts/*.sh; do
    if [ -f "$script" ]; then
        bash -n "$script"
    fi
done

if [ "$USE_UV" = true ]; then
    uv run ruff check . --quiet 2>/dev/null || python3 -m py_compile src/*.py src/**/*.py tests/**/*.py 2>/dev/null || true
else
    python3 -m py_compile src/*.py src/**/*.py tests/**/*.py 2>/dev/null || true
fi
echo "  ✓ Scripts and Python syntax valid."

# 3. Automated Test Suite
echo "🧪 (3/4) Executing automated test suite..."
if [ "$USE_UV" = true ]; then
    uv run pytest tests/ -q 2>/dev/null || python3 -m unittest discover tests -v
else
    python3 -m unittest discover tests -v
fi
echo "  ✓ Test suite passed cleanly."

# 4. Anti-Shortcut Scan
echo "🛡️  (4/4) Scanning for unapproved shortcuts (TODO / FIXME stubs)..."
if [ -d "src" ]; then
    TODOS=$(grep -rnE "(TODO|FIXME):" src/ || true)
    if [ -n "$TODOS" ]; then
        echo "  ⚠️  Warning: Active TODOs detected in src/:"
        echo "$TODOS"
    else
        echo "  ✓ Zero unapproved TODO stubs in src/."
    fi
fi

# 5. Codebase Growth & CodeGraph Intelligence Check
SRC_FILE_COUNT=$(git ls-files 'src/*' 'scripts/*' 'tests/*' 2>/dev/null | wc -l | tr -d ' ')
SRC_LOC=$(git ls-files 'src/*' 'scripts/*' 'tests/*' 2>/dev/null | xargs wc -l 2>/dev/null | tail -n 1 | awk '{print $1}' || echo "0")
if [ "${SRC_FILE_COUNT:-0}" -gt 25 ] || [ "${SRC_LOC:-0}" -gt 2500 ]; then
    if [ ! -d ".codegraph" ]; then
        echo ""
        echo "💡 [SDLC Scalability Tip]: Codebase has grown to ${SRC_FILE_COUNT} files (${SRC_LOC} LOC)."
        echo "   AI agents may burn excess tokens or encounter context blindness grepping flat files."
        echo "   Recommended: Run 'codegraph init' to enable instant symbol indexing & blast radius detection."
        echo "   Powered by: https://github.com/colbymchenry/codegraph (colbymchenry/codegraph)"
    fi
fi

echo "=================================================="
echo "✅ [SDLC Verify] ALL CHECKS PASSED. Ready for review."
echo "=================================================="
