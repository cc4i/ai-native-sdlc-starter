# Plan: Modern Packaging (uv, Python 3.14+), CodeGraph Scalability Guidance, Release Lifecycle & Repo Polish

**Linked Spec**: [`docs/specs/008-modern-tooling-codegraph-and-release.md`](file:///Users/chuancc/mywork/ai/project-start/docs/specs/008-modern-tooling-codegraph-and-release.md)  
**Author**: @antigravity  
**Date**: 2026-08-28  
**Status**: Complete  

---

## 1. Scope & Strategy

- **Objective**: Establish Python 3.14+ baseline with `uv` packaging, integrate codebase growth detection with CodeGraph (`colbymchenry/codegraph`) guidance, streamline `README.md` by removing the directory tree and adding badges/promo, automate regular releases via `scripts/release.sh` and GitHub Actions, and provide dedicated architecture documentation.
- **Strategy**: Test-Driven Development (TDD) across 4 sequential micro-stepped execution groups.
- **Estimated Execution Groups**: 4 groups.

---

## 2. File Change Map

| Path | Change Type | Purpose / Description |
| :--- | :--- | :--- |
| `pyproject.toml` | New | PEP 621 manifest with Python >=3.14, uv, ruff, pytest, ai-sdlc CLI entrypoint |
| `Makefile` | Modify | Add uv support and make release target |
| `scripts/verify.sh` | Modify | Add uv detection and CodeGraph growth analyzer |
| `scripts/check-artifacts.sh` | Modify | Add CodeGraph growth advisor check |
| `scripts/release.sh` | New | Release automation script validating health, updating version, and tagging |
| `.github/workflows/release.yml` | New | GitHub Actions workflow publishing releases on tag push |
| `GEMINI.md` | Modify | Add directives on CodeGraph integration and scalability |
| `README.md` | Modify | Remove ASCII directory tree, add badges, repo promo, and modern quickstart |
| `docs/architecture/SCALING_AND_CODEGRAPH.md` | New | Architecture guide on codebase complexity and CodeGraph integration |
| `docs/RELEASES.md` | New | Guide to semantic versioning and release management |
| `ONBOARDING.md` | Modify | Add repository anatomy, multi-stack packaging guide, and CodeGraph setup |
| `bootstrap.sh` | Modify | Include pyproject.toml generation, Python 3.14+, and growth reminder |
| `tests/unit/test_packaging.py` | New | Unit tests for pyproject.toml and Python 3.14+ requirements |
| `tests/unit/test_growth_detector.py` | New | Unit tests for codebase growth and CodeGraph guidance |
| `tests/unit/test_release_script.py` | New | Unit tests for release script validation |
| `tests/unit/test_readme_cleanliness.py` | New | Unit tests ensuring README has badges and no ASCII directory tree |
| `docs/plans/00-ROADMAP.md` | Modify | Update Milestone 008 to IN_CONSTRUCTION |

---

## 3. Micro-Stepped Execution Groups

### Execution Group 1: Python 3.14+ Baseline & Modern Packaging with `uv`
- [x] **Step 1.1 (Red)**: Write unit tests in `tests/unit/test_packaging.py` verifying `pyproject.toml` existence, Python `>=3.14` constraint, PEP 621 metadata, `ruff` py314 configuration, and `ai-sdlc` console script. Verify tests fail before file creation.
- [x] **Step 1.2 (Green)**: Create root `pyproject.toml` with PEP 621 metadata, Python 3.14+, `ruff`, `pytest`, dependencies, and `ai-sdlc = "src.cli:main"`.
- [x] **Step 1.3 (Green)**: Update `Makefile` and `scripts/verify.sh` to check for `uv` and run `uv run ruff` / `uv run pytest` when present, smoothly falling back to Python standard library.
- [x] **Step 1.4 (Verify)**: Run `tests/unit/test_packaging.py` and ensure tests pass.

### Execution Group 2: Codebase Growth Analysis & CodeGraph Guidance
- [x] **Step 2.1 (Red)**: Write unit tests in `tests/unit/test_growth_detector.py` verifying growth detection logic and reminder formatting.
- [x] **Step 2.2 (Green)**: Add growth analyzer logic to `scripts/verify.sh` and `scripts/check-artifacts.sh` (>25 files or >2,500 LOC triggers non-blocking advisory to initialize `codegraph`).
- [x] **Step 2.3 (Directives)**: Update `GEMINI.md` instructing Antigravity and subagents to leverage `codegraph_explore` MCP tool when `.codegraph/` exists.
- [x] **Step 2.4 (Verify)**: Run `tests/unit/test_growth_detector.py` and ensure green.

### Execution Group 3: Regular Release Automation & GitHub Actions
- [x] **Step 3.1 (Red)**: Write unit tests in `tests/unit/test_release_script.py` validating argument checks, semantic version regex, and dry-run output.
- [x] **Step 3.2 (Green)**: Implement `scripts/release.sh` with tree-clean check, verify execution, version updating, git tagging, and changelog generation.
- [x] **Step 3.3 (Green)**: Add `make release VERSION=vX.Y.Z` target to `Makefile` and create `.github/workflows/release.yml`.
- [x] **Step 3.4 (Doc)**: Write `docs/RELEASES.md` documenting the release lifecycle.
- [x] **Step 3.5 (Verify)**: Run `tests/unit/test_release_script.py` and ensure tests pass.

### Execution Group 4: Streamlined README, Repository Promotion & Architecture Documentation
- [x] **Step 4.1 (Red)**: Write unit test in `tests/unit/test_readme_cleanliness.py` asserting that `README.md` contains required badges and does NOT contain an ASCII file directory tree block. Verify test fails.
- [x] **Step 4.2 (Green)**: Refactor `README.md`: remove the 45-line ASCII directory tree, add official status badges, add repository promotion metadata, and link to `ONBOARDING.md` for repository anatomy.
- [x] **Step 4.3 (Green)**: Author `docs/architecture/SCALING_AND_CODEGRAPH.md` detailing CodeGraph architecture, benchmarks, and MCP usage.
- [x] **Step 4.4 (Green)**: Synchronize `ONBOARDING.md` and `bootstrap.sh` with Python 3.14+, `uv`, CodeGraph, and release practices.
- [x] **Step 4.5 (Verify)**: Run `tests/unit/test_readme_cleanliness.py`, `make verify`, and `make eval` to ensure zero regressions across the entire suite.

---

## 4. Risk Matrix & Mitigations

| Risk | Severity | Mitigation Strategy |
| :--- | :--- | :--- |
| Older Python environments fail on >=3.14 | Medium | Explicit error message in `pyproject.toml` and documentation; user's environment is confirmed Python 3.14.0 |
| Machines without `uv` fail verification | High | Strict fallback to standard python3 / unittest in `verify.sh` |
| CodeGraph advisory causes false build failures | Medium | Advisory is strictly informational stdout, exit code stays 0 |
| Release script tags dirty branches | High | Strict validation of `git diff` before any tag operation |

---

## 5. Proof of Correctness & Harness

- [x] All 4 new unit test suites pass: `test_packaging.py`, `test_growth_detector.py`, `test_release_script.py`, `test_readme_cleanliness.py`.
- [x] `make verify` exits code 0 in < 1 second.
- [x] `make eval` passes all 5 continuous regression evals.
