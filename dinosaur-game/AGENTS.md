# Universal Agent Directives (AGENTS.md)

This file defines universal system instructions, engineering standards, and lifecycle guardrails for all autonomous and pair-programming AI agents operating within this repository (DeepSeek Harness, Anthropic Claude, Google Antigravity, OpenAI Codex, Cursor, Devin, and GitHub Copilot).

---

## 🎯 Universal AI-Native SDLC Lifecycle

1. **Artifact Chain Before Code**:
   - Never write non-trivial code in src/ without an approved implementation plan in plans/.
   - All planning must trace back to a validated specification (specs/) and feature intent (intent/).
2. **Strict Test-Driven Development (TDD)**:
   - Red: Failing test -> Green: Minimum code -> Refactor: Clean up while keeping green.
   - Never gut or bypass failing tests.
3. **Single-Command Verification**:
   - Always run make verify (or ./scripts/verify.sh) before declaring any task complete.
4. **Zero Anti-Shortcuts**:
   - No TODO stubs or fake mocks in production code. Every step must be fully implemented and covered by tests.
