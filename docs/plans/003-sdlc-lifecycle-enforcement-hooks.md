# Plan: SDLC Lifecycle Enforcement & Git Hooks Implementation

**Linked Spec**: [`specs/003-sdlc-lifecycle-enforcement-hooks.md`](file:///Users/chuancc/mywork/ai/project-start/specs/003-sdlc-lifecycle-enforcement-hooks.md)  
**Author**: Staff Engineer & DevOps  
**Date**: 2026-08-27  
**Status**: Completed  
**Shipped**: ab40c52  

---

## 1. Scope & Strategy

- **Objective**: Implement local Git hooks (`.githooks/pre-commit`, `.githooks/pre-push`), installer script (`scripts/install-hooks.sh`), Makefile targets (`make init`, `make install-hooks`), CI gate updates, and bootstrap script updates to strictly enforce the unbroken artifact chain.
- **Strategy**: TDD / automated test validation across 3 execution groups.

---

## 2. File Change Map

| Path | Change Type | Purpose |
| :--- | :--- | :--- |
| `.githooks/pre-commit` | New | Local pre-commit hook enforcing artifacts + `make verify` |
| `.githooks/pre-push` | New | Local pre-push hook enforcing `make eval` |
| `scripts/install-hooks.sh` | New | One-command hook installer (`git config core.hooksPath .githooks`) |
| `scripts/check-artifacts.sh` | Modify | Add strict stage traceability validations |
| `Makefile` | Modify | Add `init` and `install-hooks` targets |
| `bootstrap.sh` & `scripts/bootstrap.sh` | Modify | Auto-install hooks upon project creation |
| `.github/workflows/artifact-integrity.yml` | Modify | Add server-side PR artifact enforcement |
| `GEMINI.md` | Modify | Add explicit non-negotiable enforcement directives |
| `tests/integration/test_hooks.py` | New | Automated tests for pre-commit hook validation |

---

## 3. Micro-Stepped Execution Groups

### Execution Group 1: Pre-Commit & Pre-Push Git Hooks
- [x] **Step 1.1**: Create `.githooks/pre-commit` script checking staged `src/` files against `intent/`, `specs/`, and `plans/`, and running `make verify`.
- [x] **Step 1.2**: Create `.githooks/pre-push` script running `make eval`.
- [x] **Step 1.3**: Create `scripts/install-hooks.sh` and make all hooks executable.

### Execution Group 2: Makefile & Bootstrap Integration
- [x] **Step 2.1**: Update `Makefile` with `init` and `install-hooks` targets.
- [x] **Step 2.2**: Update `bootstrap.sh` and `scripts/bootstrap.sh` to install hooks by default.
- [x] **Step 2.3**: Update `GEMINI.md` and `.github/workflows/artifact-integrity.yml`.

### Execution Group 3: Automated Test Harness & Verification
- [x] **Step 3.1**: Write unit/integration tests in `tests/integration/test_hooks.py` to verify hook behavior.
- [x] **Step 3.2**: Run `make verify` and `make eval` (18 tests green).
- [x] **Step 3.3**: Mark milestone in `plans/00-ROADMAP.md` as completed.
