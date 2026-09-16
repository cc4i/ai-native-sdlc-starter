# Anthropic Claude Code Agent Directives (CLAUDE.md)

Project: **Dinosaur Runner Game**  
Stack: **generic**

---

## 🎯 Primary Directives & Workflow Loop

We follow the **AI-Native SDLC** lifecycle:
1. **Never write non-trivial code without an approved `plan.md`** (located under `plans/`).
2. **Always ground planning in `spec.md`** (located under `specs/`) and `intent.md` (located under `intent/`).
3. **Strict Test-Driven Development (TDD)**:
   - For new features: Write failing interface test -> Implement minimum code -> Refactor -> Verify green.
   - For bug fixes: Write reproducing test that fails -> Fix implementation without modifying the test -> Verify green.
4. **Never Gut or Skip Failing Tests**: When a test fails, fix the code, not the test assertion.
5. **Single-Command Verification**: Run `make verify` (or `./scripts/verify.sh`) before reporting any task complete.

---

## 🛠️ Essential Commands

| Target | Command | Expected Output / Contract |
| :--- | :--- | :--- |
| **Verify All** | `make verify` | Runs lint, format check, unit tests, and build. Must exit 0. |
| **Run Tests** | `make test` | Executes unit and integration test suite. Zero failures allowed. |
| **Run Linter** | `make lint` | Runs code quality, type checks, and security scanners. |
| **Run Evals** | `make eval` | Runs continuous AI regression tests (`evals/run_evals.py`). |
| **Format Code** | `make format` | Automatically formats codebase according to standard style. |

---

## ⚡ Claude Code Slash Commands

- `/grill-me`: Socratic interview to formulate `intent.md`
- `/spec-architect`: Transform intent into Gherkin `spec.md`
- `/verify`: Execute single-command verification (`make verify`)
- `/review-pr`: Run autonomous code review audit
- `/new-intent`: Scaffold a new feature intent artifact
