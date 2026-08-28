# Plan: Autonomous PR Inline Review Engine with Gemini 3.7 Flash

**Linked Spec**: [`docs/specs/007-inline-pr-review-and-gemini.md`](../../docs/specs/007-inline-pr-review-and-gemini.md)  
**Author**: Antigravity Staff Architect  
**Date**: 2026-08-28  
**Status**: Completed  
**Shipped**: 0ee3921  

---

## 1. Execution Groups & Architecture

- **Group 1: Diff Parser & Inline Anchor Mapper**
  - Implement `src/tools/diff_parser.py` to parse unified diff headers and calculate modified line sets per file.
  - Unit tests in `tests/unit/test_diff_parser.py`.

- **Group 2: Gemini 3.7 Flash Semantic Review Engine**
  - Implement `src/agent/gemini_reviewer.py` targeting `gemini-3.7-flash` with structured outputs, prompt construction based on `REVIEW.md`, and resilient API error handling.
  - Unit tests in `tests/unit/test_gemini_reviewer.py`.

- **Group 3: GitHub Review Publisher & Tally Formatter**
  - Implement `src/tools/github_publisher.py` to construct GitHub batch review payloads (`github.rest.pulls.createReview` compatible JSON).
  - Implement the `Important: n, Consider: n, Nit: n` tally and 5-nit cap in `ReviewReport.render_markdown()`.
  - Update `src/cli.py` to support `--inline-output` and `--use-gemini`.
  - Unit tests in `tests/unit/test_github_publisher.py`.

- **Group 4: Workflow Integration & Full SDLC Loop Verification**
  - Update `.github/workflows/ai-pr-review.yml` to publish inline comments and summary tally on PRs.
  - Run `make verify` and `make eval`.
  - ReviewAgent review audit report in `docs/reviews/007-inline-pr-review-and-gemini.md`.
  - Commit, push branch, create PR #5, verify CI, and merge!

---

## 2. Micro-Stepped Tasks

### Execution Group 1: Diff Parser
- [x] Create `src/tools/diff_parser.py` parsing unified diffs into modified line sets.
- [x] Create `tests/unit/test_diff_parser.py` with 4 unit tests.
- [x] Verify green.

### Execution Group 2: Gemini 3.7 Flash Engine
- [x] Create `src/agent/gemini_reviewer.py` with `gemini-3.7-flash` default, structured review prompt, and HTTP API client using standard libraries.
- [x] Create `tests/unit/test_gemini_reviewer.py` with mocked responses and fallback tests.
- [x] Verify green.

### Execution Group 3: GitHub Review Publisher & Tally
- [x] Implement `src/tools/github_publisher.py` for batch PR review comments.
- [x] Update `src/models/review.py` and `src/agent/review_agent.py` to support `Important: n, Consider: n, Nit: n` and nit cap.
- [x] Update `src/cli.py` with `--inline-json` and `--use-gemini`.
- [x] Create `tests/unit/test_github_publisher.py`.
- [x] Verify green.

### Execution Group 4: CI Workflow & PR
- [x] Update `.github/workflows/ai-pr-review.yml` to publish inline review comments.
- [x] Run `make verify` and `make eval`.
- [x] Generate `docs/reviews/007-inline-pr-review-and-gemini.md`.
- [ ] Push to `origin feat/007-inline-pr-review-and-gemini`, open PR #5, and merge to `main`!
