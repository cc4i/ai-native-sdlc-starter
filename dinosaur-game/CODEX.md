# OpenAI Codex Directives (CODEX.md)

This file provides system instructions, conventions, and operational workflows for OpenAI Codex and OpenAI-powered coding agents in this repository.

---

## 🎯 Primary Workflow & Lifecycle Rules
1. Spec & Plan First: Never generate non-trivial code in src/ without an approved plan.md in plans/ grounded in specs/ and intent/.
2. Strict TDD: Write failing tests in tests/ before implementing application logic in src/.
3. Verification: Always run make verify before completing any task.
4. No Placeholders: Zero TODO comments or unimplemented stubs in production files.
