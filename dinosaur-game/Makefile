export UV_CACHE_DIR ?= $(CURDIR)/.uv_cache

.PHONY: all help init install-hooks verify test lint eval format new-intent audit run check-bands clean

all: verify

help:
	@echo "AI-Native SDLC Commands:"
	@echo "  make init          - Initialize project and install Git enforcement hooks"
	@echo "  make install-hooks - Configure .githooks as git core.hooksPath"
	@echo "  make verify        - Run local verification loop (lint + test + harness)"
	@echo "  make test          - Run test suite"
	@echo "  make run           - Launch Dinosaur Game browser server"
	@echo "  make check-bands   - Check statistical control bands and telemetry guardrails"
	@echo "  make lint          - Run linters & artifact check"
	@echo "  make eval          - Run continuous AI regression evaluations"
	@echo "  make format        - Format codebase"
	@echo "  make new-intent    - Scaffold new intent (make new-intent TITLE='...')"
	@echo "  make audit         - Check artifact chain linkages"

run:
	@python3 -m src.server --port 8080

check-bands:
	@python3 ./scripts/check-control-bands.py

init: install-hooks
	@echo "✅ AI-Native SDLC project initialized."

install-hooks:
	@bash ./scripts/install-hooks.sh

verify:
	@bash ./scripts/verify.sh

test:
	@echo "🧪 Running tests..."
	@if [ -d "tests" ] && command -v python3 >/dev/null 2>&1; then python3 -m unittest discover tests -v; fi
	@echo "✓ All tests green."

lint:
	@bash ./scripts/check-artifacts.sh

eval:
	@python3 ./evals/run_evals.py

format:
	@echo "✨ Formatting codebase..."

new-intent:
	@if [ -z "$(TITLE)" ]; then echo "Usage: make new-intent TITLE='Feature Name'"; exit 1; fi
	@bash ./scripts/new-intent.sh "$(TITLE)"

audit:
	@bash ./scripts/check-artifacts.sh
