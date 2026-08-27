#!/usr/bin/env bash
# ==============================================================================
# Git Hooks Installer for AI-Native SDLC
# ==============================================================================
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

GREEN="\033[0;32m"
CYAN="\033[0;36m"
BOLD="\033[1m"
RESET="\033[0m"

echo -e "${CYAN}🔧 Installing AI-Native SDLC Git hooks...${RESET}"

mkdir -p .githooks
chmod +x .githooks/* 2>/dev/null || true

if [ -d ".git" ]; then
    git config core.hooksPath .githooks
    echo -e "${GREEN}${BOLD}✅ Git hooks path set to '.githooks'.${RESET}"
    echo -e "   - Pre-commit: Verifies artifact chain & runs ${CYAN}make verify${RESET}"
    echo -e "   - Pre-push  : Runs ${CYAN}make eval${RESET}"
else
    echo "⚠️  Not a git repository yet. Hooks will activate once 'git init' is run."
fi
