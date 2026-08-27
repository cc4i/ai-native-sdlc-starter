# Plan: AI Code Review & Security Auditor Agent Implementation

**Linked Spec**: [`specs/001-code-review-agent.md`](file:///Users/chuancc/mywork/ai/project-start/specs/001-code-review-agent.md)  
**Author**: Antigravity Builder Agent  
**Date**: 2026-08-27  
**Status**: Completed  

---

## 1. Scope & Strategy

- **Objective**: Implement a modular, zero-external-dependency AI code review agent capable of secret detection, AST security checking, spec compliance verification, and structured report formatting.
- **Strategy**: Strict Test-Driven Development (TDD) across 3 sequential execution groups.

---

## 2. File Change Map

| Path | Change Type | Purpose |
| :--- | :--- | :--- |
| `src/models/review.py` | New | Core data models (`Severity`, `Verdict`, `Finding`, `ReviewReport`) |
| `src/tools/secret_scanner.py` | New | High-precision regex secret and credential scanner |
| `src/tools/ast_checker.py` | New | Python AST parser for dangerous functions, anti-patterns, and bad practices |
| `src/tools/spec_matcher.py` | New | Verification of code diffs against spec requirements |
| `src/agent/review_agent.py` | New | Autonomous agent orchestrator and report renderer |
| `src/cli.py` | New | CLI entrypoint for running reviews from terminal or CI |
| `tests/unit/test_tools.py` | New | Unit tests for all individual inspection tools |
| `tests/unit/test_agent.py` | New | Unit tests for agent orchestration and verdict logic |
| `tests/integration/test_cli.py` | New | End-to-end integration tests for CLI execution |

---

## 3. Micro-Stepped Execution Groups

### Execution Group 1: Data Models & Inspection Tools (TDD)
- [x] **Step 1.1 (Red)**: Write unit tests in `tests/unit/test_tools.py` for `SecretScannerTool`, `AstSecurityCheckerTool`, and `SpecComplianceTool`.
- [x] **Step 1.2 (Green)**: Implement `src/models/review.py` and tools under `src/tools/`.
- [x] **Step 1.3 (Refactor)**: Verify all tool unit tests pass cleanly.

### Execution Group 2: Agent Orchestration & Report Synthesis (TDD)
- [x] **Step 2.1 (Red)**: Write unit tests in `tests/unit/test_agent.py` testing multi-tool coordination, verdict computation (`PASS`, `CHANGES_REQUESTED`, `BLOCKED`), and markdown report formatting.
- [x] **Step 2.2 (Green)**: Implement `src/agent/review_agent.py`.
- [x] **Step 2.3 (Refactor)**: Verify all agent unit tests pass.

### Execution Group 3: CLI Entrypoint, Integration Tests & Verification
- [x] **Step 3.1 (Red)**: Write integration tests in `tests/integration/test_cli.py`.
- [x] **Step 3.2 (Green)**: Implement `src/cli.py` supporting `review` command with exit codes.
- [x] **Step 3.3 (Verify)**: Update `scripts/verify.sh` to run the test suite and verify `make verify` passes 100%.

---

## 4. Proof of Correctness & Harness

- [x] All 15 unit and integration tests pass with 0 failures (`make test` / `make verify`).
- [x] `make verify` executes all linting, test, and artifact checks with exit code 0 in ~0.1s.
- [x] Continuous AI evals in `evals/` pass 5/5 assertions (`make eval`).
- [x] Running `python3 -m src.cli review <sample>` outputs expected audit report.
