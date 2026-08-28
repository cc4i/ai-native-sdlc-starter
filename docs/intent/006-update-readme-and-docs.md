# Intent: Align README.md and Onboarding Docs with Codebase Reality

**Initiative**: Milestone 006  
**Author**: Antigravity & User  
**Date**: 2026-08-28  
**Status**: Approved  

---

## 1. Problem Statement

Following the successful completion of Milestone 004 (PR Review Automation & Branch Protection) and Milestone 005 (Docs Restructure, Shipped Commit Tracking, Stage 6 Control Bands, and Jetski Lifecycle Hooks), [`README.md`](file:///Users/chuancc/mywork/ai/project-start/README.md) and [`ONBOARDING.md`](file:///Users/chuancc/mywork/ai/project-start/ONBOARDING.md) are out of sync with the actual repository layout and capabilities:

- The directory tree diagrams list legacy root folders (`intent/`, `specs/`, `plans/`, `templates/`) instead of the unified `docs/` hierarchy.
- Crucial production files and modules are completely missing from documentation: `docs/reviews/`, `bands.yaml`, `hooks.json`, `src/tools/band_detector.py`, `scripts/jetski_guard.py`, `scripts/check-control-bands.py`, and `tests/`.
- The command guide does not mention `make review-pr` or the statistical control band check.
- Traceability descriptions omit the `shipped: <SHA>` standard.

---

## 2. Desired Outcome

1. **Synchronize `README.md`**:
   - Update the 6 stages overview table to reference `docs/intent/`, `docs/specs/`, `docs/plans/`, `docs/reviews/`, `docs/templates/`.
   - Update repository structure diagram to accurately reflect `docs/`, `src/`, `tests/`, `bands.yaml`, `hooks.json`, and all scripts.
   - Expand walkthrough sections with `make review-pr`, `bands.yaml` statistical anomaly detection, and Jetski `PreToolUse`/`Stop` lifecycle hooks.
2. **Synchronize `ONBOARDING.md`**:
   - Update artifact paths to `docs/` and add explanations for `bands.yaml` and `hooks.json`.
3. **Verify Zero Regressions**:
   - All 33 unit/integration tests and 5 AI evals must continue to pass cleanly.

---

## 3. Constraints & Boundaries

- Maintain clean, high-density, professional documentation.
- Use valid markdown links throughout.
- Keep all existing user instructions intact while enhancing accuracy.
