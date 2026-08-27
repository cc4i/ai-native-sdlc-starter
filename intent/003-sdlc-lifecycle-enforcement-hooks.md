# Intent: AI-Native SDLC Strict Lifecycle Enforcement & Git Hooks

**Author**: Product Owner & Security Lead  
**Date**: 2026-08-27  
**Status**: Approved  
**Target Milestone**: v1.0-mvp  

---

## 1. Problem Statement
- **Current State**: Developers and autonomous AI agents can theoretically bypass the SDLC stages by writing code directly to `src/` without first authoring an `intent.md`, `spec.md`, and `plan.md`.
- **User Pain / Friction**: Without deterministic, automated enforcement mechanisms (git hooks and CI gate checks), rules in `GEMINI.md` rely purely on agent compliance. A human or rogue agent can push code straight to `main` without traceability or verified tests.
- **Impact & Urgency**: High. To make this repository an enterprise-ready template, the artifact chain (`intent ➔ spec ➔ plan ➔ verify ➔ review ➔ prod`) must be enforced deterministically at the commit, push, and PR merge stages.

---

## 2. Proposed Outcome
- Provide local Git hooks (`.githooks/pre-commit` and `.githooks/pre-push`) that block any commit/push if code in `src/` lacks corresponding `intent/`, `specs/`, `plans/`, or if `make verify` / `make eval` fails.
- Provide a `make install-hooks` command and wire it automatically into `bootstrap.sh` and `make init`.
- Enhance CI workflow (`.github/workflows/artifact-integrity.yml`) to strictly enforce that PRs touching code must have verified traceability across the full artifact chain before allowing merge to `main`.
- Add explicit, non-negotiable enforcement directives to `GEMINI.md`.

---

## 3. Affected Users & Systems
- **Target Personas**: Developers, AI agents (Antigravity), Code Reviewers, Release Managers.
- **Affected Systems**: Git hooks (`.githooks/`), Local CLI toolchain (`scripts/`), CI/CD pipeline (`.github/workflows/`), Agent directives (`GEMINI.md`).

---

## 4. Constraints & Boundaries
- **Zero-Bypass**: Hooks must check both human and AI commits.
- **Fast Execution**: Pre-commit validation must execute in < 1 second on typical changes.
- **Clear Remediation Guidance**: When a commit or PR is blocked, the hook/CI must output exact, step-by-step commands to resolve the violation.

---

## 5. Open Questions & Assumptions
1. *Can emergency hotfixes bypass the hook?* -> **Resolved**: Standard `git commit --no-verify` exists for rare manual emergencies, but CI server-side branch protection on `main` will strictly reject PRs without artifact traceability.

---

## 6. Approval & Handover
- **Product Owner Review**: Approved by @product-owner on 2026-08-27
- **Ready for Stage 2 (Design)**: `specs/003-sdlc-lifecycle-enforcement-hooks.md`
