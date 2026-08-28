# Project Agent Directives (GEMINI.md)

This file provides system instructions, conventions, and operational workflows for **Antigravity** and any autonomous subagents working on this repository.

---

## 🎯 Primary Directives & Workflow Loop

We follow the **AI-Native SDLC** lifecycle:
1. **Never write non-trivial code without an approved `plan.md`** (located under `docs/plans/` or `plans/`).
2. **Always ground planning in `spec.md`** (located under `docs/specs/` or `specs/`) and `intent.md` (located under `docs/intent/` or `intent/`).
3. **Strict Test-Driven Development (TDD)**:
   - For new features: Write failing interface test -> Implement minimum code -> Refactor -> Verify green.
   - For bug fixes: Write reproducing test that fails -> Fix implementation without modifying the test -> Verify green.
4. **Never Gut or Skip Failing Tests**: When a test fails, fix the code, not the test assertion.
5. **Single-Command Verification**: Run `make verify` (or `./scripts/verify.sh`) before reporting any task complete.
6. **Unbroken Chain Enforcement**: Git pre-commit/pre-push hooks and CI block any commits or PRs modifying `src/` without corresponding `intent.md ➔ spec.md ➔ plan.md` artifacts. Always update the artifact chain first.

---

## 🛠️ Essential Commands

| Target | Command | Expected Output / Contract |
| :--- | :--- | :--- |
| **Verify All** | `make verify` | Runs lint, format check, unit tests, and build. Must exit 0. |
| **Run Tests** | `make test` | Executes unit and integration test suite. Zero failures allowed. |
| **Run Linter** | `make lint` | Runs code quality, type checks, and security scanners. |
| **Run Evals** | `make eval` | Runs continuous AI regression tests (`evals/run_evals.py`). |
| **Format Code** | `make format` | Automatically formats codebase according to standard style. |
| **Review PR** | `make review-pr` | Runs ReviewAgent on branch diff and posts audit report. |

---

## 📋 Artifact Locations & Schema

All project decisions are tracked in version-controlled Markdown artifacts under `docs/`:

- **`docs/intent/`**: Originator problem statement, desired outcome, constraints (`docs/intent/NNN-title.md`).
- **`docs/specs/`**: Formal requirements, Gherkin acceptance criteria (`Given / When / Then`), edge cases, and security boundaries (`docs/specs/NNN-title.md`).
- **`docs/plans/`**: Micro-stepped execution groups, files to change, risk matrix, proof harness (`docs/plans/NNN-title.md`), plus release milestones in `docs/plans/00-ROADMAP.md`.
- **`docs/reviews/`**: PR Review audit reports and governance sign-offs (`docs/reviews/NNN-title.md`).
- **`docs/templates/`**: Standard markdown templates for each SDLC stage.
- **`evals/`**: AI regression test prompts, assertions, and execution configs.
- **`REVIEW.md`**: Standard PR review criteria, severity definitions, and human approval rules.

---

## 🏗️ Architecture & Conventions

1. **Clean Separation of Concerns**:
   - `src/` (or equivalent application directory): Core business logic isolated from presentation and network drivers.
   - `scripts/`: Tooling, build scripts, and developer productivity utilities.
   - `tests/`: Automated unit, integration, and contract tests.
2. **Security & Privacy Guardrails**:
   - No hardcoded API keys, JWT secrets, or sensitive tokens. Always use environment variables or secret managers.
   - No PII in log streams or error traces.
   - Validate and sanitize all external inputs at system entry points.
3. **No Anti-Shortcuts / Placeholders**:
   - Do not leave `// TODO: Implement later` or stub methods in production code.
   - Every execution step must be fully implemented and covered by automated tests.

---

## 🧠 Codebase Intelligence & Scalability (CodeGraph)

- If `.codegraph/` exists or the `codegraph_explore` MCP tool is available:
  1. **Before editing or refactoring**: Query `codegraph_explore` to inspect callers, callees, and the change's blast radius instead of manually grepping files.
  2. **In Stage 2 (Design) & Stage 3 (Build)**: Use CodeGraph to populate the "Affected Callers & Blast Radius" section in `plan.md`.
  3. **In Stage 5 (Deploy / PR Review)**: Cross-check diffs against CodeGraph to catch breaking signature changes across un-staged files.
- Refer to `docs/architecture/SCALING_AND_CODEGRAPH.md` for full guidance.

---

## 🚨 Troubleshooting & Gotchas

- **Do not modify test files during bug fixing** unless the test itself was proven to be incorrectly specified in `spec.md`.
- **If a task touches generated files** or vendor dependencies, verify against schema definitions rather than manual edits.
- **Keep `GEMINI.md` concise**: When a mistake happens twice, add a single bullet point here so future agent sessions don't repeat it.
