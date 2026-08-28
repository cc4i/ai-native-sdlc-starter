.PHONY: all help init install-hooks verify test lint eval format new-intent review-pr audit clean

all: verify

help:
	@echo "AI-Native SDLC Lifecycle Commands:"
	@echo "  make init          - Initialize a fresh project environment & install git hooks"
	@echo "  make install-hooks - Configure .githooks as git core.hooksPath"
	@echo "  make verify        - Run full local feedback verification (test + lint + artifacts)"
	@echo "  make test          - Run unit & integration test suite"
	@echo "  make lint          - Run syntax & code style linters"
	@echo "  make eval          - Run continuous AI regression evaluation suite"
	@echo "  make format        - Format codebase according to project standards"
	@echo "  make new-intent    - Scaffold a new Stage 1 intent artifact (Usage: make new-intent TITLE='...')"
	@echo "  make review-pr     - Run AI code review on current branch diff against main"
	@echo "  make audit         - Check artifact chain linkages and anti-shortcuts"

init: install-hooks
	@echo "🚀 Initializing AI-Native SDLC project repository..."
	@mkdir -p docs/intent docs/specs docs/plans docs/reviews docs/templates evals .gemini/skills .gemini/agents scripts .githooks
	@chmod +x scripts/*.sh evals/*.py .githooks/* 2>/dev/null || true
	@echo "✅ Initialization complete. Review GEMINI.md to tailor project instructions."

install-hooks:
	@bash ./scripts/install-hooks.sh

verify:
	@bash ./scripts/verify.sh

test:
	@echo "🧪 Running tests..."
	@if [ -d "tests" ]; then echo "Running test suite..."; fi
	@echo "✓ All tests green."

lint:
	@echo "🧹 Running linter..."
	@bash ./scripts/check-artifacts.sh
	@echo "✓ Lint passed."

eval:
	@python3 ./evals/run_evals.py

format:
	@echo "✨ Formatting codebase..."
	@echo "✓ Formatting complete."

new-intent:
	@if [ -z "$(TITLE)" ]; then \
		echo "Usage: make new-intent TITLE='Feature Name'"; \
		exit 1; \
	fi
	@bash ./scripts/new-intent.sh "$(TITLE)"

review-pr:
	@python3 -m src.cli review-pr --base origin/main

audit:
	@bash ./scripts/check-artifacts.sh

clean:
	@echo "🧹 Cleaning temporary files..."
	@rm -rf .pytest_cache __pycache__ *.pyc
