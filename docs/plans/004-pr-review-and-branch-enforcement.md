# Plan: Automated AI PR Review & Branch Protection Enforcement

**Linked Spec**: [`specs/004-pr-review-and-branch-enforcement.md`](../../specs/004-pr-review-and-branch-enforcement.md)  
**Author**: Staff Engineer & DevOps  
**Date**: 2026-08-28  
**Status**: Completed  
**Shipped**: 4a0e5c4  

---

## 1. Scope & Strategy

- **Objective**: Implement branch protection in `.githooks/pre-commit`, build the `review-pr` CLI command in `src/cli.py`, create the `reviews/` artifact directory, and upgrade `.github/workflows/ai-pr-review.yml` to automatically comment review reports on GitHub PRs.
- **Strategy**: TDD implementation in 3 micro-stepped execution groups.

---

## 2. File Change Map

| Path | Change Type | Purpose |
| :--- | :--- | :--- |
| `.githooks/pre-commit` | Modify | Forbid commits on `main` and `master` branches |
| `reviews/README.md` | New | Document Stage 5 PR Review Audit artifacts |
| `reviews/000-ai-sdlc-starter-template.md` | New | Historical review audit for Milestone 000 |
| `reviews/001-code-review-agent.md` | New | Historical review audit for Milestone 001 |
| `reviews/002-claims-status-example.md` | New | Historical review audit for Milestone 002 |
| `reviews/003-sdlc-lifecycle-enforcement-hooks.md` | New | Historical review audit for Milestone 003 |
| `reviews/004-pr-review-and-branch-enforcement.md` | New | Review audit report for Milestone 004 |
| `src/agent/review_agent.py` | Modify | Support multi-file and git diff aggregation |
| `src/cli.py` | Modify | Add `review-pr` command for diffs |
| `tests/unit/test_cli_pr.py` | New | Unit tests for `review-pr` command |
| `tests/integration/test_pr_review.py` | New | Integration test for git diff review |
| `.github/workflows/ai-pr-review.yml` | Modify | Run ReviewAgent and post comments to PR |
| `scripts/check-artifacts.sh` | Modify | Add `reviews/` directory verification |
| `Makefile` | Modify | Add `make review-pr` command |
| `bootstrap.sh` & `scripts/bootstrap.sh` | Modify | Include `reviews/` in scaffolded projects |
| `plans/00-ROADMAP.md` | Modify | Track milestone 004 |

---

## 3. Micro-Stepped Execution Groups

### Execution Group 1: Local Branch Protection & Artifact Store (TDD)
- [x] **Step 1.1**: Update `.githooks/pre-commit` to check current branch and abort if on `main` or `master`.
- [x] **Step 1.2**: Create `reviews/` directory, `reviews/README.md`, and retrospective review reports.
- [x] **Step 1.3**: Update `scripts/check-artifacts.sh` to include `reviews/`.

### Execution Group 2: CLI `review-pr` Command & Multi-File Aggregation (TDD)
- [x] **Step 2.1 (Red)**: Write unit tests in `tests/unit/test_cli_pr.py` and integration tests in `tests/integration/test_pr_review.py`.
- [x] **Step 2.2 (Green)**: Update `src/agent/review_agent.py` and `src/cli.py` to support `review-pr --base <base> [--spec <spec>] [--output <file>]`.
- [x] **Step 2.3 (Refactor)**: Verify all 22 tests pass with `make verify`.

### Execution Group 3: CI/CD PR Review Action & Live Pull Request Validation
- [x] **Step 3.1**: Upgrade `.github/workflows/ai-pr-review.yml` to run `review-pr` and comment on PRs.
- [x] **Step 3.2**: Update `Makefile`, `bootstrap.sh`, and `scripts/bootstrap.sh`.
- [x] **Step 3.3**: Run `make verify` and `make eval`.
- [x] **Step 3.4**: Push branch, open Pull Request on GitHub with `gh pr create`, generate review report, and merge PR!
