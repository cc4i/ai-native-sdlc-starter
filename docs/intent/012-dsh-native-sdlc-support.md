# Intent: DeepSeek Harness (DSH) Native SDLC Support & Local Environment Isolation

**Author**: DeepSeek Harness Lead & User  
**Date**: 2026-09-16  
**Status**: Approved  
**Target Milestone**: Milestone 012 (v1.2-dsh-expansion)  

---

## 1. Problem Statement

The AI-Native SDLC Starter Template provides stage-by-stage multi-agent development for tools such as Anthropic Claude Code, Google Antigravity, OpenAI Codex, Cursor, and GitHub Copilot. However:
1. **Missing DSH Discovery Paths**: DeepSeek Harness (DSH) natively discovers skills from `<projectRoot>/.agents/skills` and `<projectRoot>/.dsh/skills`. In the current repository, skills only exist under `.gemini/skills/`, meaning DSH agents cannot automatically discover the 5 core SDLC skills (`intent-capture`, `spec-architect`, `secure-api-design`, `adversarial-review`, `verifier-loop`).
2. **External Environment Leakage (UV Cache)**: Running `make verify` or `uv run` by default relies on `~/.cache/uv` outside the project directory. In sandboxed or isolated agent environments (like DSH `workspace-write`), touching the user's default environment or outside cache paths triggers sandbox denials and violates project isolation principles.
3. **Bootstrapper Scaffolding Gaps**: `bootstrap.sh` does not scaffold `.agents/skills/` or enforce project-local UV caching (`UV_CACHE_DIR=.uv_cache`), meaning newly bootstrapped projects also lack out-of-the-box DSH readiness.

- **Current State**: Developers using DSH must manually configure skills, handle external uv cache access issues, and lack documentation on running SDLC stages within DSH.
- **User Pain / Friction**: Running `make verify` in isolated sandbox environments can fail due to external path touches, and DSH does not auto-populate skills without manual configuration.
- **Impact & Urgency**: Resolving these items provides zero-configuration DSH support, enforces strict project isolation without touching user default environments, and standardizes multi-agent tooling across all supported ecosystems.

---

## 2. Proposed Outcome

1. **Project-Local Environment & UV Cache Isolation**:
   - Configure `UV_CACHE_DIR` to default strictly inside the repository root (`${ROOT_DIR}/.uv_cache`) in `scripts/verify.sh`, `Makefile`, and `bootstrap.sh`.
   - Add `.uv_cache/` to `.gitignore`.
   - Never touch or read outside user environment files during verification or testing.
2. **First-Class DSH Skill Discovery via Open Standard**:
   - Establish `.agents/skills/` adhering to the Open Agent standard and DSH `dsh-skill-filesystem` provider, making the 5 core SDLC skills auto-discoverable in DSH sessions via the `skill` tool.
   - Maintain full backward compatibility with Antigravity (`.gemini/skills/`) and Claude Code (`.claude/commands/`).
3. **Native DSH Directives & Guidance**:
   - Provide a dedicated `DSH.md` and update `AGENTS.md`, `README.md`, and `ONBOARDING.md` documenting DSH multi-agent tools (`subagent`, `workflow`, `ralph`, `todo_write`, `skill`).
4. **Universal Bootstrapper Update**:
   - Update `bootstrap.sh` to generate `.agents/skills/` and project-local `UV_CACHE_DIR` by default.
5. **Real-World Project Validation (Dinosaur Game)**:
   - Validate the duplicated workflow by bootstrapping and building a complete, playable browser-based Dinosaur Game (an endless runner with jumping/ducking, obstacles, collision physics, score tracking, and automated tests) following the full AI SDLC pipeline.

---

## 3. Affected Users & Systems

- **Target Personas / Users**:
  - Developers using DeepSeek Harness (DSH) Web GUI and CLI.
  - Multi-agent AI software teams standardizing on open agent interfaces (`.agents/skills`).
- **Affected Systems / Services**:
  - `scripts/verify.sh`, `Makefile`, `bootstrap.sh`, `.gitignore`.
  - `.agents/skills/` directory structure.
  - `DSH.md`, `README.md`, `ONBOARDING.md`, `AGENTS.md`.
  - Unit test suite (`tests/unit/test_multi_tool_directives.py`, `tests/unit/test_bootstrap_cli.py`).

---

## 4. Constraints & Boundaries

- **Zero Outside Environment Pollution**: Tools must operate strictly within the project boundary. Never touch user default configuration or files outside `$PWD`.
- **Full Backward Compatibility**: Claude Code, Antigravity, Cursor, Codex, and Copilot workflows must remain 100% operational with zero regressions.
- **Strict Verification**: `make verify` must pass with 0 warnings, 0 test failures, and 0 artifact check warnings under strict `workspace-write` mode.
- **Out of Scope**: Modifying remote DSH server binaries; all integration is handled through repository artifacts, configuration, and open standards.

---

## 5. Open Questions & Assumptions

1. *Q: Should `.agents/skills` be symlinks or independent files?*  
   *Decision*: In the starter template, `.agents/skills` can be linked or created so both Antigravity and DSH/open agents share a single source of truth. In `bootstrap.sh`, both directories are scaffolded cleanly.
2. *Q: Where should the isolated uv cache live?*  
   *Decision*: Under `<projectRoot>/.uv_cache`, ignored by `.gitignore`.

---

## 6. Approval & Handover

- **Product Owner Review**: Approved by @chuancc on 2026-09-16
- **Ready for Stage 2 (Design)**: `docs/specs/012-dsh-native-sdlc-support.md`
