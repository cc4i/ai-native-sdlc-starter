# Plan: Remove Legacy Branding References Across Entire Repository

**Linked Spec**: [`docs/specs/010-remove-legacy-branding.md`](../specs/010-remove-legacy-branding.md)  
**Author**: @antigravity  
**Status**: Complete  
**Shipped**: a5b3d51  

---

## 1. Scope & Strategy

Rename guard scripts and test files to `agent_guard.py` and `test_agent_guard.py`. Update `hooks.json`, documentation files (`README.md`, `ONBOARDING.md`), bootstrap scripts, and historical docs to eliminate all legacy naming.

---

## 2. Micro-Stepped Execution Groups

### Group 1: Script, Test, and Hook Renaming
- [x] Rename guard script to `scripts/agent_guard.py`.
- [x] Rename guard tests to `tests/unit/test_agent_guard.py` and update test assertions/classes.
- [x] Update `.gemini/hooks.json` and `hooks.json` to reference `scripts/agent_guard.py`.

### Group 2: Documentation & Bootstrap Scripts
- [x] Update `README.md` and `ONBOARDING.md`.
- [x] Update `bootstrap.sh` and `scripts/bootstrap.sh`.
- [x] Update references in `docs/intent/`, `docs/specs/`, `docs/plans/`, `docs/reviews/`.

### Group 3: Verification & Repo Metadata
- [x] Remove legacy topic from GitHub repo via `gh repo edit`.
- [x] Verify zero occurrences across codebase.
- [x] Run `make verify && make eval` to ensure all tests pass.
