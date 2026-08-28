# Intent: SDLC Enhancements and Docs Directory Restructure

**Initiative**: Milestone 005  
**Author**: Antigravity & User  
**Date**: 2026-08-28  
**Status**: Approved  

---

## 1. Problem Statement

Following our comprehensive comparative analysis between the **Jetski/Antigravity AI-Native SDLC** and the **Claude Code AI-Native SDLC in Coda**, four key opportunities were identified to advance this template to parity with production-grade practices:

1. **Repository Root Clutter**: Currently, five separate artifact folders (`intent/`, `specs/`, `plans/`, `templates/`, `reviews/`) sit at the repository root. Grouping them cleanly under a unified `docs/` hierarchy (`docs/intent/`, `docs/specs/`, `docs/plans/`, `docs/reviews/`, `docs/templates/`) simplifies the repository structure, separating operational documentation from application code and build scripts.
2. **Missing Shipped Commit Traceability**: In `plans/00-ROADMAP.md` and phase plans, plans are marked `COMPLETED` without recording the exact Git commit SHA that delivered them. Tracking `shipped: <SHA>` ensures historical auditability.
3. **Absence of Stage 6 Operational Feedback Loop**: The AI SDLC loop should close after deployment. Without automated control bands (`bands.yaml` and anomaly detection), production incidents or metric deviations cannot automatically trigger Stage 1 intents.
4. **Agent Guardrail Interception (`PreToolUse` & `Stop` Hooks)**: While git hooks catch issues at commit/push time, lifecycle hooks in Jetski (`hooks.json` & `jetski_guard.py`) can intercept unsafe agent commands (e.g. `git add -A`, `git commit -a`, editing protected files) *before* tool execution, and enforce verification before completion.

---

## 2. Desired Outcome

1. **Unified `docs/` Artifact Hierarchy**:
   - `docs/intent/`, `docs/specs/`, `docs/plans/`, `docs/reviews/`, `docs/templates/`.
   - Update all tooling (`Makefile`, `scripts/check-artifacts.sh`, `scripts/new-intent.sh`, `.githooks/`, `bootstrap.sh`, `evals/`, `tests/`, `src/`) to reference and support `docs/`.
2. **`shipped: <SHA>` Traceability**:
   - Plans support a `shipped: <COMMIT_SHA>` field.
   - `scripts/check-artifacts.sh` verifies that completed milestones record a valid 7-40 character Git SHA.
3. **Stage 6 Automated Control Bands**:
   - Create `bands.yaml` declaring operational metrics, baseline parameters, and threshold tiers (`log`, `diagnose`, `act`).
   - Create `src/tools/band_detector.py` and `scripts/check-control-bands.py` to evaluate metrics against rolling baselines.
   - Include automated tests for the detector.
4. **Jetski Lifecycle Hook Integration**:
   - Provide `hooks.json` and `scripts/jetski_guard.py` implementing `PreToolUse` (blocking broad staging, protected paths) and `Stop` hooks.

---

## 3. Constraints & Principles

- **Zero Regression**: All existing 22 unit/integration tests and 5 AI evals must pass.
- **Strict Backward Compatibility**: Tooling should support both legacy root folders (if present) and the new canonical `docs/` structure.
- **Zero External Paid Dependencies**: Control bands and hook guards must remain pure Python/bash without requiring external cloud accounts or tokens.
- **Unbroken Traceability**: Maintain the full chain across all 5 milestones.
