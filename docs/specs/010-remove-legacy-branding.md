# Spec: Remove Legacy Branding References Across Entire Repository

**Linked Intent**: [`docs/intent/010-remove-legacy-branding.md`](../intent/010-remove-legacy-branding.md)  
**Author**: @antigravity  
**Date**: 2026-08-28  
**Status**: Validated  

---

## 1. Technical Requirements & Contracts

### 1.1 Zero Occurrence Contract
- A case-insensitive search for legacy platform naming across all tracked files in the repository MUST return 0 matches.

### 1.2 File Renaming & Refactoring
- `scripts/agent_guard.py` is the unified lifecycle guard script.
- `tests/unit/test_agent_guard.py` is the unified lifecycle guard test suite.
- `.gemini/hooks.json` and `hooks.json` target `agent_guard.py`.

### 1.3 Documentation & Templates
- `README.md`, `ONBOARDING.md`, `bootstrap.sh`, `scripts/bootstrap.sh`, and `docs/**`:
  - Standardized on "Google Antigravity".
  - Standardized on "agent-guard".

---

## 2. Acceptance Criteria (Gherkin)

### Scenario 1: Verification of Zero Legacy Branding Occurrences
- **Given** all codebase updates are applied
- **When** the codebase is searched for legacy platform references
- **Then** the search exits with zero matches found.

### Scenario 2: Agent Guard Hook Operational Functionality
- **Given** `scripts/agent_guard.py` is invoked via `hooks.json`
- **When** `tests/unit/test_agent_guard.py` runs
- **Then** all tests verifying `PreToolUse` broad staging denial and `Stop` loop validation pass cleanly.

### Scenario 3: Full Test & Eval Suite Integrity
- **Given** the renaming and text replacements are completed
- **When** `make verify && make eval` is executed
- **Then** all quality gates, lint checks, tests, and AI evaluations pass with exit code 0.
