# GitHub Copilot Instructions (.github/copilot-instructions.md)

You are an AI coding assistant working in this repository. Follow the AI-Native SDLC methodology:

## 1. Specification & Planning Precedence
- Never modify files in `src/` without checking or updating the corresponding `docs/plans/` and `docs/specs/` documents.
- If the user asks for a new feature, guide them to first define the intent (`docs/intent/`), formalize the spec (`docs/specs/`), and detail an execution plan (`docs/plans/`).

## 2. Test-Driven Development (TDD)
- When generating code, generate or update test cases in `tests/` first.
- Maintain failing tests until the implementation satisfies them; never relax assertions to make a test pass.

## 3. Verification & Clean Code
- Run `make verify` (or `pytest tests/ && ruff check .`) to ensure the codebase is clean.
- Ensure all code is production-ready: no TODO placeholders or mock stubs.
- Never hardcode secrets, API keys, or tokens.
