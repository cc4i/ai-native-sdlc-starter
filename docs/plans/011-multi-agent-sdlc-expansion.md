# Plan: Multi-Agent AI SDLC Expansion (Claude Code, Codex, Cursor, Copilot & Antigravity)

**Linked Spec**: [`specs/011-multi-agent-sdlc-expansion.md`](../specs/011-multi-agent-sdlc-expansion.md)  
**Author**: Lead Architect & Engineer  
**Date**: 2026-09-04  
**Status**: Completed  

---

## 1. Scope & Strategy

- **Objective**: Implement native, seamless support for Claude Code, OpenAI Codex, Cursor, GitHub Copilot, and Antigravity in the AI-Native SDLC template, including root directives, Claude slash commands, multi-provider ReviewAgent semantic auditing (Anthropic, OpenAI, Gemini), and universal bootstrapping.
- **Strategy**: 
  - Additive, zero-breaking-change expansion.
  - Test-Driven Development (TDD) for multi-provider semantic review backends using standard library HTTP.
  - Universal scaffolding in `bootstrap.sh` so every new project starts with multi-tool capabilities ready out of the box.
- **Estimated Execution Groups**: 4 sequential groups.

---

## 2. File Change Map

| Path | Change Type | Purpose / Description |
| :--- | :--- | :--- |
| `CLAUDE.md` | New | Complete system instructions and directives for Anthropic Claude Code |
| `AGENTS.md` | New | Universal cross-agent instructions standard for AI coding tools |
| `CODEX.md` | New | Directives and commands tailored for OpenAI Codex CLI |
| `.cursorrules` | New | Root-level directives for Cursor IDE |
| `.cursor/rules/sdlc.mdc` | New | MDC-formatted Cursor rule enforcing SDLC lifecycle and verification |
| `.github/copilot-instructions.md` | New | Workspace instructions for GitHub Copilot / Copilot Workspace |
| `.claude/commands/grill-me.md` | New | Claude Code slash command for Socratic intent grilling |
| `.claude/commands/spec-architect.md` | New | Claude Code slash command for spec generation |
| `.claude/commands/verify.md` | New | Claude Code slash command for `make verify` |
| `.claude/commands/review-pr.md` | New | Claude Code slash command for autonomous PR review |
| `.claude/commands/new-intent.md` | New | Claude Code slash command to scaffold new intent |
| `src/agent/semantic_reviewer.py` | New | Multi-provider reviewer abstraction (Anthropic, OpenAI, Gemini) |
| `src/agent/review_agent.py` | Modify | Integrate `SemanticReviewer` supporting multi-provider review |
| `src/cli.py` | Modify | Add `--provider` argument and env var handling |
| `tests/unit/test_semantic_reviewer.py` | New | Unit tests covering Gemini, Claude, and OpenAI reviewers & provider factory |
| `bootstrap.sh` & `scripts/bootstrap.sh` | Modify | Scaffold multi-agent directives & `.claude/commands` during bootstrap |
| `README.md` | Modify | Multi-agent badges, tool matrix, and getting started guides |
| `ONBOARDING.md` | Modify | Dedicated setup and workflow sections for each tool |

---

## 3. Micro-Stepped Execution Groups

### Execution Group 1: Universal Tool Directives & Claude Code Commands
- [x] **Step 1.1**: Create `CLAUDE.md` with lifecycle rules, essential commands, TDD contracts, and CodeGraph integration.
- [x] **Step 1.2**: Create `AGENTS.md` and `CODEX.md` conforming to industry open agent instruction standards.
- [x] **Step 1.3**: Create `.cursorrules`, `.cursor/rules/sdlc.mdc`, and `.github/copilot-instructions.md`.
- [x] **Step 1.4**: Create `.claude/commands/`: `grill-me.md`, `spec-architect.md`, `verify.md`, `review-pr.md`, `new-intent.md`.

### Execution Group 2: Multi-Provider ReviewAgent Implementation (TDD)
- [x] **Step 2.1 (Red)**: Write unit tests in `tests/unit/test_semantic_reviewer.py` testing provider auto-detection, `ClaudeReviewer`, `OpenAIReviewer`, `GeminiReviewer`, and fallback behaviors with mocked HTTP responses. Verify tests fail.
- [x] **Step 2.2 (Green)**: Implement `src/agent/semantic_reviewer.py` with `BaseSemanticReviewer`, `ClaudeReviewer`, `OpenAIReviewer`, `GeminiReviewer`, and `get_semantic_reviewer()`.
- [x] **Step 2.3 (Refactor & Wire)**: Update `src/agent/review_agent.py` and `src/cli.py` to support `--provider` (`gemini`, `claude`, `openai`, `auto`) and verify green tests.

### Execution Group 3: Bootstrap Scaffolding Expansion
- [x] **Step 3.1**: Update `bootstrap.sh` and `scripts/bootstrap.sh` to generate `CLAUDE.md`, `AGENTS.md`, `CODEX.md`, `.cursorrules`, `.github/copilot-instructions.md`, and `.claude/commands/`.
- [x] **Step 3.2**: Update bootstrap console output and next steps banner to guide users on Antigravity, Claude Code, Codex, and Cursor.

### Execution Group 4: Documentation Alignment & Full Verification
- [x] **Step 4.1**: Update `README.md` with multi-agent support section and command table.
- [x] **Step 4.2**: Update `ONBOARDING.md` with tool-specific workflows.
- [x] **Step 4.3**: Run `make verify` and verify 100% green tests and zero lint warnings.

---

## 4. Risk Matrix & Mitigations

| Risk | Severity | Mitigation Strategy |
| :--- | :--- | :--- |
| Discrepancy between agent rules across directive files | Medium | Shared core SDLC contracts (TDD, unbroken chain, single-command verify) strictly mirrored across all files |
| Missing API keys breaking local PR review | Low | Graceful fallback: when no API key is present, local deterministic passes run and succeed without error |
| Dependency bloat from AI SDKs | High | Zero new dependencies: use standard library `urllib.request` and `json` for all LLM API calls |

---

## 5. Proof of Correctness & Harness

- [x] `make verify` exits code 0.
- [x] Unit tests in `tests/unit/test_semantic_reviewer.py` passing 100%.
- [x] All directive files verified on disk.
- [x] `CLAUDE.md`, `AGENTS.md`, `CODEX.md`, `.cursorrules`, `.claude/commands/` successfully created.
