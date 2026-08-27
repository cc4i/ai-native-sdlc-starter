# Plan: AI-Native SDLC Starter Template Construction

**Linked Spec**: [`specs/000-ai-sdlc-starter-template.md`](file:///Users/chuancc/mywork/ai/project-start/specs/000-ai-sdlc-starter-template.md)  
**Author**: Antigravity Builder Agent  
**Date**: 2026-08-27  
**Status**: Completed  

---

## 1. Scope & Strategy

- **Objective**: Build and verify the complete AI-native SDLC template structure, directives, skills, subagents, continuous evals, verification harness, documentation, and standalone bootstrap tool.
- **Strategy**: Test-driven micro-stepped execution with verification harness.

---

## 2. Micro-Stepped Execution Groups

### Execution Group 1: Core Framework, Templates & Directives
- [x] **Step 1.1**: Create `GEMINI.md` and `REVIEW.md` policies.
- [x] **Step 1.2**: Create standardized Markdown templates under `templates/`.
- [x] **Step 1.3**: Create Antigravity skills under `.gemini/skills/` and agent roles under `.gemini/agents/`.

### Execution Group 2: Developer Tooling, Verification & Evals
- [x] **Step 2.1**: Implement `scripts/verify.sh`, `scripts/new-intent.sh`, and `scripts/check-artifacts.sh`.
- [x] **Step 2.2**: Implement continuous AI eval runner `evals/run_evals.py` and `evals/eval-config.json`.
- [x] **Step 2.3**: Build `Makefile` exposing standard lifecycle targets.

### Execution Group 3: Reference Agent App & Documentation
- [x] **Step 3.1**: Build working Code Review Agent in `src/` and `tests/` with 100% test pass.
- [x] **Step 3.2**: Create comprehensive `README.md` and `ONBOARDING.md` guides.
- [x] **Step 3.3**: Implement zero-clone `bootstrap.sh` script and verify in isolated temp environment.

---

## 3. Proof of Correctness & Harness

- [x] `make verify` passes with 0 errors.
- [x] `make eval` passes 5/5 regression evaluations.
- [x] `bootstrap.sh` successfully creates and verifies a fresh project in an isolated temporary directory.
