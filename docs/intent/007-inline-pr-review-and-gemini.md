# Intent: Autonomous PR Inline Review Engine with Gemini 3.7 Flash

**Initiative**: Milestone 007  
**Author**: Antigravity Staff Architect & User  
**Date**: 2026-08-28  
**Status**: Approved  

---

## 1. Problem Statement

In Milestone 004 and 005, we built an initial PR review agent that scans diffs with deterministic tools (AST security checks, secret scanning, spec compliance) and posts a summary markdown report to the PR conversation thread.

However, state-of-the-art AI code review workflows (such as `anthropics/claude-code-action` in `coda`) have shown that:
1. **Summary-only reviews lack context**: Developers must manually cross-reference line numbers from a summary report against the code in the "Files Changed" tab.
2. **Deterministic tools alone miss semantic and architectural bugs**: While AST tools catch dangerous calls (`eval`, unhandled exceptions), they cannot catch subtle logic inversions, off-by-one errors, async deadlock/leak risks, or interface mismatches without LLM reasoning.
3. **Existing cloud review actions are slow, expensive, and fragile**: `claude-code-action` relies on expensive 30+ turn agent loops ($2+ per PR), risks turn overrun failures, requires 5 cloud secrets and custom GitHub Apps, and cannot run locally.

---

## 2. Desired Outcome

Build a built-in review engine that **matches and surpasses** `claude-code-action`:
1. **True Inline PR Review Comments**:
   - Parse `git diff` hunks to identify exact changed lines.
   - Anchor review findings directly to specific lines in the GitHub PR diff (`path`, `line`, `body`).
   - Format actionable suggestions with GitHub 1-click replacement blocks (` ```suggestion ... ``` `).
2. **Gemini 3.7 Flash Semantic Review Engine**:
   - Default model: **Gemini 3.7 Flash** (`gemini-3.7-flash`).
   - Executes structured multi-pass code review (Pass 1: Correctness, Pass 2: Security, Pass 3: Plan Compliance) based on [`REVIEW.md`](../../REVIEW.md).
   - Returns structured JSON findings with severity classification (`Important`, `Consider`, `Nit`) and machine-readable tally: `Important: n, Consider: n, Nit: n`.
   - Enforces a strict Nit cap (default max 5 nits per review) to prevent reviewer fatigue.
3. **Hybrid Two-Tier Architecture**:
   - **Tier 1 (Instant Local & CI Fallback)**: Deterministic AST, regex, and spec checks run locally via `make review-pr` in <0.2s with $0 cost and zero credentials.
   - **Tier 2 (Cloud Semantic Reasoning)**: In GitHub Actions CI or when `GEMINI_API_KEY` (or Google Cloud ADC) is present, Gemini 3.7 Flash performs deep semantic analysis and publishes inline review comments.
   - **Graceful degradation**: If cloud credentials are absent, the workflow logs a notice and seamlessly completes with Tier 1.

---

## 3. Constraints & Boundaries

- **Zero-Crash Resiliency**: CI must never fail on API quota or network error; it must fall back gracefully to deterministic analysis.
- **Model Standard**: Default model must be `gemini-3.7-flash`.
- **Standard Toolchain**: Use standard Python libraries (`urllib` or Google GenAI client if available) without bloat.
- **Verification Integrity**: `make verify` and `make eval` must pass cleanly.
