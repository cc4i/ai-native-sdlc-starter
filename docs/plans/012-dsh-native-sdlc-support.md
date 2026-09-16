# Plan: DeepSeek Harness (DSH) Native SDLC Support & Local Environment Isolation

**Linked Spec**: [`docs/specs/012-dsh-native-sdlc-support.md`](../specs/012-dsh-native-sdlc-support.md)  
**Author**: DSH Lead Architect  
**Date**: 2026-09-16  
**Status**: Completed  

---

## 1. Scope & Strategy

- **Objective**: Deliver first-class DeepSeek Harness (DSH) multi-agent support, establish `.agents/skills/` open standard discovery, enforce strict project-local UV caching (`UV_CACHE_DIR="${ROOT_DIR}/.uv_cache"`), update bootstrapper scaffolding, and validate the complete workflow by bootstrapping and building a real browser-based Dinosaur Game endless runner project.
- **Strategy**: Test-Driven Development (TDD) — author assertions for DSH directives, `.agents/skills/`, and project-local UV caching before wiring implementations.
- **Estimated Execution Groups**: 5 groups (Isolation Harness ➔ Skills & Artifacts ➔ DSH Directives ➔ Bootstrapper ➔ Real Project Validation).

---

## 2. File Change Map

| Path | Change Type | Purpose / Description |
| :--- | :--- | :--- |
| `.gitignore` | Modify | Ignore `.uv_cache/` |
| `scripts/verify.sh` | Modify | Enforce `export UV_CACHE_DIR="${ROOT_DIR}/.uv_cache"` |
| `Makefile` | Modify | Set `export UV_CACHE_DIR ?= $(CURDIR)/.uv_cache`; create `.agents/skills` on `init` |
| `.agents/skills/` | New | Symlink / directory mapping to `.gemini/skills/` for DSH discovery |
| `DSH.md` | New | Native DSH directives, tool definitions, and workflow reference |
| `AGENTS.md` | Modify | Add DSH multi-agent tool documentation |
| `README.md` | Modify | Add DSH badge and platform entry in multi-agent table |
| `ONBOARDING.md` | Modify | Add DSH workflow guide and quickstart |
| `scripts/check-artifacts.sh` | Modify | Support `.agents/skills` directory in verification |
| `bootstrap.sh` | Modify | Scaffold `.agents/skills` and local `UV_CACHE_DIR` config |
| `tests/unit/test_multi_tool_directives.py` | Modify | Add test coverage for DSH directives, `.agents/skills`, and UV cache isolation |
| `docs/plans/00-ROADMAP.md` | Modify | Record Milestone 012 |

---

## 3. Micro-Stepped Execution Groups

### Execution Group 1: UV Cache Isolation & TDD Red Harness
- [x] **Step 1.1 (Red)**: Add tests in `tests/unit/test_multi_tool_directives.py` verifying `DSH.md`, `.agents/skills`, and `UV_CACHE_DIR` isolation settings in `scripts/verify.sh` and `Makefile`.
- [x] **Step 1.2 (Green)**: Update `.gitignore`, `scripts/verify.sh`, and `Makefile` to set project-local `UV_CACHE_DIR`. Verify `make verify` runs cleanly without sandbox errors.

### Execution Group 2: DSH Native Skill Discovery (`.agents/skills`)
- [x] **Step 2.1**: Link `.agents/skills` to `.gemini/skills` so DSH discovers all 5 skills (`intent-capture`, `spec-architect`, `secure-api-design`, `adversarial-review`, `verifier-loop`).
- [x] **Step 2.2**: Update `scripts/check-artifacts.sh` to validate `.agents/skills` alongside `.gemini/skills`.

### Execution Group 3: DSH Directives & Multi-Agent Documentation
- [x] **Step 3.1**: Create `DSH.md` with instructions on DSH tools (`subagent`, `workflow`, `ralph`, `todo_write`, `skill`).
- [x] **Step 3.2**: Update `AGENTS.md`, `README.md`, and `ONBOARDING.md` with DSH quickstart and tool tables.

### Execution Group 4: Universal Bootstrapper Updates
- [x] **Step 4.1**: Update `bootstrap.sh` to generate `.agents/skills` and project-local UV settings.
- [x] **Step 4.2**: Verify `bootstrap.sh --help` and run existing bootstrap unit tests.

### Execution Group 5: Real-World Validation (Endless Runner Dinosaur Game)
- [x] **Step 5.1**: Use `bootstrap.sh` to generate an actual new project directory (`dinosaur-game`) with Python/HTML5 stack.
- [x] **Step 5.2**: Follow AI SDLC flow inside `dinosaur-game`: author intent (`docs/intent/001-dinosaur-game.md`), spec with Gherkin (`docs/specs/001-dinosaur-game.md`), and plan (`docs/plans/001-dinosaur-game.md`).
- [x] **Step 5.3**: Build the complete Dinosaur Game (canvas engine, player dinosaur, jump/duck mechanics, procedural cactus/pterodactyl obstacles, collision AABB physics, score and hi-score tracking, game over/restart state machine) and automated tests.
- [x] **Step 5.4**: Run `make verify` in `dinosaur-game` to confirm end-to-end health and SDLC compliance.

---

## 4. Risk Matrix & Mitigations

| Risk | Severity | Mitigation Strategy |
| :--- | :--- | :--- |
| UV cache pollution across different projects | Low | Scope cache strictly to `<projectRoot>/.uv_cache` |
| Symlink compatibility on Windows / non-POSIX | Medium | `bootstrap.sh` creates direct files; symlinks used locally |
| DSH skill schema mismatch | Low | Skills strictly adhere to open agent YAML frontmatter (`name`, `description`) |

---

## 5. Proof of Correctness & Harness

- [x] **Command**: `make verify` exits code 0 with 0 errors and zero external cache access.
- [x] **Unit Tests**: All unit tests in `tests/unit/test_multi_tool_directives.py` pass.
- [x] **Bootstrapped Game**: Fully functional, test-covered Dinosaur Game browser project verified with `make verify`.
