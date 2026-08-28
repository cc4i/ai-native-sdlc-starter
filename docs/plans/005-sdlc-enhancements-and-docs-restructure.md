# Plan: SDLC Enhancements and Docs Directory Restructure

**Linked Spec**: [`specs/005-sdlc-enhancements-and-docs-restructure.md`](../specs/005-sdlc-enhancements-and-docs-restructure.md)  
**Author**: Antigravity Staff Architect  
**Date**: 2026-08-28  
**Status**: Completed  
**Shipped**: ce6b60b  

---

## 1. Scope & Execution Strategy

- **Group 1**: Migrate artifact directories under `docs/` (`docs/intent/`, `docs/specs/`, `docs/plans/`, `docs/reviews/`, `docs/templates/`) and update all path references in scripts, make targets, hooks, and guidelines.
- **Group 2**: Implement `shipped: <SHA>` tracking in `docs/plans/` and verify in `scripts/check-artifacts.sh`.
- **Group 3**: Build Stage 6 Control Bands engine (`bands.yaml`, `src/tools/band_detector.py`, `tests/unit/test_band_detector.py`).
- **Group 4**: Build Agent Lifecycle Hook (`hooks.json`, `scripts/agent_guard.py`, `tests/unit/test_agent_guard.py`).
- **Group 5**: Run full verification loop (`make verify`, `make eval`), generate Stage 5 review audit, open Pull Request, and merge!

---

## 2. Micro-Stepped Tasks

### Group 1: Docs Directory Restructure
- [x] Move `intent/`, `specs/`, `plans/`, `reviews/`, `templates/` into `docs/`.
- [x] Update `scripts/check-artifacts.sh` and `scripts/new-intent.sh`.
- [x] Update `.githooks/pre-commit` and `.githooks/pre-push`.
- [x] Update `Makefile` and `GEMINI.md`.
- [x] Update `bootstrap.sh` and `scripts/bootstrap.sh`.
- [x] Verify `make verify` passes with the new `docs/` hierarchy.

### Group 2: `shipped: <SHA>` Traceability
- [x] Add `shipped: <SHA>` to completed plans (`docs/plans/000` through `004`).
- [x] Update `scripts/check-artifacts.sh` to validate `shipped:` commit hash for completed plans.

### Group 3: Stage 6 Control Bands Engine (TDD)
- [x] Create `bands.yaml` with baseline configurations and metric thresholds.
- [x] Write unit tests `tests/unit/test_band_detector.py`.
- [x] Implement `src/tools/band_detector.py` calculating mean, standard deviation, and sigma tier.
- [x] Create `scripts/check-control-bands.py` CLI utility.

### Group 4: Agent Lifecycle Hook (TDD)
- [x] Create `hooks.json` mapping `PreToolUse` and `Stop` events.
- [x] Write unit tests `tests/unit/test_agent_guard.py`.
- [x] Implement `scripts/agent_guard.py` processing stdin JSON and returning structured decision on stdout.

### Group 5: Review, PR & Merge
- [x] Run `make verify` and `make eval` (33 unit/integration tests passing).
- [x] Generate Stage 5 review audit report `docs/reviews/005-sdlc-enhancements-and-docs-restructure.md`.
- [x] Commit, push branch `feat/005-sdlc-enhancements-and-docs-restructure`, and create GitHub PR.
- [x] Verify GitHub Actions CI and merge PR!
