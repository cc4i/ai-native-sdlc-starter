# Spec: Multi-Agent AI SDLC Expansion (Claude Code, Codex, Cursor, Copilot & Antigravity)

**Linked Intent**: [`intent/011-multi-agent-sdlc-expansion.md`](../intent/011-multi-agent-sdlc-expansion.md)  
**Author**: Lead Architect & Product Owner  
**Date**: 2026-09-04  
**Status**: Validated  

---

## 1. Overview & Scope

- **Summary**: Expand the AI-Native SDLC Starter Template to natively support Anthropic Claude Code, OpenAI Codex / ChatGPT, Cursor, GitHub Copilot, and Google Antigravity in a unified, multi-agent framework.
- **Target Users**: Any software engineer, team lead, or autonomous AI agent working within an AI-assisted codebase.
- **In Scope**:
  1. Universal Root Directives:
     - `CLAUDE.md`: Full directive specification for Claude Code (workflow loop, essential commands, unbroken chain, TDD, CodeGraph integration).
     - `AGENTS.md`: Cross-agent universal instructions standard following industry best practices.
     - `CODEX.md`: Directive file formatted for OpenAI Codex / Codex CLI.
     - `.cursorrules` and `.cursor/rules/sdlc.mdc`: Instructions for Cursor IDE.
     - `.github/copilot-instructions.md`: Instructions for GitHub Copilot Workspace and Agent Mode.
  2. Claude Code Native Workflows:
     - `.claude/commands/grill-me.md`: Socratic requirements elicitation slash command.
     - `.claude/commands/spec-architect.md`: Spec creation and Gherkin scenario generation.
     - `.claude/commands/verify.md`: Fast single-command verification (`make verify`).
     - `.claude/commands/review-pr.md`: Autonomous code review command (`make review-pr`).
     - `.claude/commands/new-intent.md`: Intent scaffolding command.
  3. Multi-Provider ReviewAgent Backend:
     - `SemanticReviewer`: Unified abstraction in `src/agent/semantic_reviewer.py` supporting `GeminiReviewer`, `ClaudeReviewer` (Anthropic Messages API), and `OpenAIReviewer` (OpenAI Chat Completions API) using zero external dependencies (`urllib.request`).
     - CLI flags and env vars: `--provider` (`gemini`, `claude`, `openai`, `auto`), `LLM_PROVIDER`, `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GEMINI_API_KEY`.
     - Preserving existing `--use-gemini` and default behavior for full backward compatibility.
  4. Multi-Agent Scaffolding in Bootstrapper:
     - Update `bootstrap.sh` and `scripts/bootstrap.sh` to generate all agent directives and Claude commands by default.
  5. Documentation & Onboarding:
     - Update `README.md` and `ONBOARDING.md` with multi-agent guide and tool comparison table.
- **Out of Scope**:
  - Writing proprietary IDE binary plugins.
  - Adding heavyweight client SDK dependencies (`openai`, `anthropic`).

---

## 2. User Stories & Acceptance Criteria (Gherkin Scenarios)

### Story 1: Universal Tool Directives Discovery
**As an** engineer opening the repository in Claude Code, Codex, Cursor, or Antigravity  
**I want** the agent to immediately load repository rules, TDD directives, and verification commands  
**So that** the agent never takes anti-shortcuts or modifies source files without approved specs and plans.

#### Scenario 1.1: Claude Code loads directives from `CLAUDE.md`
```gherkin
Given a developer launches Claude Code in the repository
When Claude Code inspects the repository root
Then it reads CLAUDE.md containing the AI-Native SDLC lifecycle rules
And it recognizes make verify, make test, and docs/ artifact chain requirements
```

#### Scenario 1.2: Cross-agent tools load directives from `AGENTS.md` and `CODEX.md`
```gherkin
Given an agent conforming to the AGENTS.md standard (e.g. OpenAI Codex, Cursor, Devin)
When it analyzes the project
Then it discovers AGENTS.md and CODEX.md containing the non-negotiable verification and TDD rules
And it refuses to create unverified PRs or skip failing tests
```

#### Scenario 1.3: Cursor IDE applies rules from `.cursorrules` and `.cursor/rules/`
```gherkin
Given a developer opens the project in Cursor IDE
When the developer prompts Composer or Agent Mode to implement a feature
Then Cursor loads .cursorrules and .cursor/rules/sdlc.mdc enforcing the spec -> plan -> tdd lifecycle
```

### Story 2: Claude Code Native Slash Workflows
**As a** developer using Claude Code CLI  
**I want** to execute custom slash commands (`/grill-me`, `/verify`, `/review-pr`)  
**So that** I have parity with Antigravity slash commands inside Claude Code.

#### Scenario 2.1: Executing `/grill-me` in Claude Code
```gherkin
Given a developer runs `/grill-me` in Claude Code
When the slash command prompt executes
Then Claude Code enters the Socratic Grill Loop to interrogate requirements
And it drafts an intent artifact conforming to docs/templates/intent.template.md
```

#### Scenario 2.2: Executing `/verify` in Claude Code
```gherkin
Given an agent completes a code modification in Claude Code
When `/verify` is invoked
Then it runs `make verify` and validates exit code 0
```

### Story 3: Multi-Provider ReviewAgent
**As a** developer or CI runner  
**I want** the autonomous ReviewAgent to support Anthropic Claude, OpenAI, or Google Gemini  
**So that** code review audits can be conducted using whatever AI provider my organization has configured.

#### Scenario 3.1: Provider auto-selection via environment variables
```gherkin
Given ANTHROPIC_API_KEY is set in the environment
And neither GEMINI_API_KEY nor OPENAI_API_KEY is configured
When ai-sdlc review-pr is executed with semantic review enabled
Then ReviewAgent automatically selects ClaudeReviewer
And it executes a 3-pass semantic audit using Anthropic Messages API
```

#### Scenario 3.2: Explicit provider flag override
```gherkin
Given OPENAI_API_KEY is set in the environment
When ai-sdlc review-pr --provider openai --model gpt-4o is executed
Then ReviewAgent routes the semantic audit to OpenAIReviewer using gpt-4o
And it outputs a standardized ReviewReport with findings and verdict
```

#### Scenario 3.3: Graceful fallback when no LLM API key is present
```gherkin
Given no AI API keys are set in the environment
When ai-sdlc review-pr is executed
Then ReviewAgent executes local deterministic passes (Secret Scanner, AST Security, Spec Compliance)
And it returns a clean verdict without crashing or raising network exceptions
```

---

## 3. Architecture & Interface Contracts

### 3.1 Reviewer Provider Interface
```python
class BaseSemanticReviewer(ABC):
    @abstractmethod
    def is_available(self) -> bool:
        """Returns True if provider credentials are configured."""
        ...

    @abstractmethod
    def review_diff(
        self,
        diff_text: str,
        review_policy: str = "",
        spec_content: str = "",
    ) -> Optional[ReviewReport]:
        """Runs cloud semantic review and returns ReviewReport."""
        ...
```

### 3.2 Provider Selection Logic
```
CLI Flag (--provider [gemini|claude|openai|auto])
  └──> Environment Variable (LLM_PROVIDER)
        └──> Auto-Detect Credentials:
              1. ANTHROPIC_API_KEY -> ClaudeReviewer (default: claude-3-7-sonnet-20250219)
              2. OPENAI_API_KEY    -> OpenAIReviewer (default: gpt-4o)
              3. GEMINI_API_KEY    -> GeminiReviewer (default: gemini-3.7-flash)
              4. None              -> No-op (Local deterministic passes only)
```

---

## 4. Policy, Security & Quality Constraints

- [x] **Zero Credential Leaks**: Never log or print `API_KEY` in error traces, CLI outputs, or markdown reports.
- [x] **Lightweight Architecture**: No third-party SDK dependencies added to `pyproject.toml`. Standard library HTTP only.
- [x] **Backward Compatibility**: Existing `--use-gemini` CLI flag and `GEMINI_API_KEY` workflows continue to work identically.
- [x] **Quality Gate**: `make verify` must pass with 100% green unit tests and zero ruff lint errors.

---

## 5. Adversarial Review & Sign-Off

- **Spec Gate Verdict**: PASSED by Lead Architect & Product Owner on 2026-09-04
- **Ready for Stage 3 (Build)**: `plans/011-multi-agent-sdlc-expansion.md`
