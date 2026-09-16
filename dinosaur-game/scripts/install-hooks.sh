#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

mkdir -p .githooks
chmod +x .githooks/* 2>/dev/null || true

if [ -d ".git" ]; then
    git config core.hooksPath .githooks
    echo "  ✓ Git hooks activated in .githooks/"
fi
