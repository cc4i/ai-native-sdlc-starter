# Universal Agent Directives (AGENTS.md)

This file defines the universal system instructions, engineering standards, and lifecycle guardrails for all autonomous and pair-programming AI agents operating within this repository (including OpenAI Codex, Cursor, Devin, GitHub Copilot, Anthropic Claude, and Google Antigravity).

---

## 🎯 Universal AI-Native SDLC Lifecycle

All agents working on this codebase MUST abide by the following non-negotiable rules:

1. **Artifact Chain Before Code**:
   - **Never write non-trivial code in `src/` without an approved implementation plan** located under `docs/plans/` or `plans/`.
   - All planning must trace back to a validated specification (`docs/specs/`) and feature intent (`docs/intent/`).
   - Git pre-commit and pre-push hooks strictly block any commits modifying `src/` without corresponding artifacts.

2. **Strict Test-Driven Development (TDD)**:
   - For new features: Write failing interface test -> Implement minimum code -> Refactor -> Verify green.
   - For bug fixes: Write a reproducing test that fails -> Fix implementation without touching the test -> Verify green.
   - **Never Gut or Skip Failing Tests**: When a test fails, fix the code, not the test assertion.

3. **Single-Command Verification**:
   - Always run `make verify` (or `./scripts/verify.sh`) before completing any task. Zero failures, zero lint warnings, and zero broken formats permitted.

4. **Branch-First Development**:
   - Always create a dedicated feature branch (`git checkout -b feat/NNN-title`) from `main` before modifying any files. Direct edits and commits on `main` are strictly forbidden.

5. **Zero Anti-Shortcuts**:
   - No `TODO: implement later`, placeholder functions, or fake mock stubs in production paths. Every execution step must be fully implemented and covered by automated tests.

---

## 🛠️ Essential Verification Commands

```bash
# Verify entire codebase (lint + format check + unit tests + build)
make verify

# Run test suite
make test

# Run linter and type checks
make lint

# Automatically format code
make format

# Run autonomous PR review on branch diff
make review-pr
```

---

## 📋 Artifact Locations & Schema

- **`docs/intent/`**: Originator problem statement, desired outcome, constraints (`docs/intent/NNN-title.md`).
- **`docs/specs/`**: Formal requirements, Gherkin acceptance criteria (`Given / When / Then`), edge cases, security boundaries (`docs/specs/NNN-title.md`).
- **`docs/plans/`**: Micro-stepped execution groups, files to change, risk matrix, proof harness (`docs/plans/NNN-title.md`), and master roadmap (`docs/plans/00-ROADMAP.md`).
- **`docs/reviews/`**: PR Review audit reports and governance sign-offs (`docs/reviews/NNN-title.md`).
- **`docs/templates/`**: Standard markdown templates for each SDLC stage.
- **`REVIEW.md`**: PR review criteria, severity definitions, and human sign-off rules.

---

## 🔒 Security, Secrets & Privacy Guardrails

- **Zero Hardcoded Secrets**: Never hardcode API keys, JWT secrets, passwords, or tokens. Use environment variables or secret managers.
- **Zero Sensitive Data in Logs**: Ensure no PII (Personally Identifiable Information), credentials, or internal stack traces leak into logs.
- **Input Sanitization**: Validate all inputs at domain boundaries using schemas and type checkers.
