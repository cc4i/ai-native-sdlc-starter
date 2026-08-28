# Intent: Modern Packaging (uv, Python 3.14+), CodeGraph Scalability Guidance, Release Lifecycle & Repo Polish

**Author**: @chuancc  
**Date**: 2026-08-28  
**Status**: Approved  
**Target Milestone**: v1.1 - Evolution  

---

## 1. Problem Statement

To establish this repository as a gold-standard, high-bar open-source project on GitHub for AI-Native SDLC, four key areas require immediate modernization and elevation:

- **Current State & Gaps**:
  1. **Python Version & Packaging**: The repo lacks a formal `pyproject.toml` manifest and does not mandate modern Python (3.14+). Modern developers expect lightning-fast package management via [`uv`](https://github.com/astral-sh/uv) (sub-second resolution, lockfiles, and `ruff`).
  2. **Codebase Scalability & Context Blindness**: As repositories grow past 20–30 files, AI agents waste tokens and make errors grepping flat files without symbol dependency awareness. Mature tools like [`colbymchenry/codegraph`](https://github.com/colbymchenry/codegraph) (68k+ ⭐) exist with 20+ language support and native Antigravity/Jetski MCP integration, but our starter currently provides zero growth detection or proactive guidance when code outgrows simple search.
  3. **Repository Polish & Clutter**: `README.md` is bogged down by a 45-line ASCII directory tree (`## 📁 Repository Structure`) that creates maintenance friction and clutters the front page. The repository also lacks standard open-source promotion polish (badges, standardized "About" metadata, topic tags, and a crisp, high-signal value proposition).
  4. **Formal Release Lifecycle**: There is no structured process or tooling for regular releases (semantic version bumping, changelog notes, git release tagging, and automated GitHub releases).
  5. **Documentation Architecture**: As the repo grows more complex, comprehensive documentation must be properly folded into dedicated architecture and release guides rather than overloading single markdown files.

- **User Pain / Friction**:
  - Developers lack a standardized modern Python 3.14+ environment with `uv`.
  - AI agents navigating larger codebases burn tokens on brute-force file crawling.
  - The repository's visual presentation on GitHub lacks the punchy, high-bar polish of top-tier developer tools.
  - Releases are ad-hoc without formal versioning or automated distribution.

- **Impact & Urgency**:
  - High. Combining Python 3.14+ packaging, CodeGraph scaling guidance, a streamlined README, and release automation will ensure the repo maintains an enterprise-grade standard.

---

## 2. Proposed Outcome

1. **Python 3.14+ Baseline & Modern `uv` Packaging**:
   - Provide root `pyproject.toml` requiring `requires-python = ">=3.14"`, PEP 621 metadata, `ruff` (line-length 100, py314 target), `pytest`, and `ai-sdlc` CLI console script entry point.
   - Update `Makefile` and `scripts/verify.sh` to leverage `uv` when available with seamless standard Python fallback.
   - Update CI workflows to run against Python 3.14.

2. **Codebase Growth Detection & CodeGraph Guidance**:
   - Implement codebase growth detection in `scripts/verify.sh` and `scripts/check-artifacts.sh`. When tracked source files exceed 25 or lines of code exceed 2,500 and `.codegraph/` is not present, display a proactive, non-blocking advisory recommending `codegraph init` (`colbymchenry/codegraph`).
   - Add explicit subagent directives in `GEMINI.md` instructing Antigravity and review agents to leverage `codegraph_explore` MCP tool when `.codegraph/` exists.
   - Author a dedicated architecture guide: `docs/architecture/SCALING_AND_CODEGRAPH.md`.

3. **Streamline README & High-Bar Repository Polish**:
   - **Remove the verbose ASCII repository structure tree** from `README.md` to keep the front page clean, punchy, and focused on value proposition and workflow loops.
   - Add standard GitHub badges (CI Build, Python 3.14+, uv, CodeGraph Integrated, AI-Native SDLC, License).
   - Provide recommended GitHub "About" description and topic tags (`ai-sdlc`, `antigravity`, `jetski`, `code-review`, `codegraph`, `uv`, `developer-tools`) in documentation.
   - Keep detailed repository anatomy inside `ONBOARDING.md` where developers deep-dive.

4. **Regular Release Automation & Governance**:
   - Create `scripts/release.sh` and `make release VERSION=v1.X.X` to validate clean working tree, verify all checks, update version in `pyproject.toml`, generate changelog notes from roadmap/reviews, and create annotated git tags.
   - Add `.github/workflows/release.yml` to automatically publish GitHub Releases on tag push.
   - Document the release lifecycle in `docs/RELEASES.md`.

5. **Documentation Architecture Alignment**:
   - Fold architecture scaling details into `docs/architecture/SCALING_AND_CODEGRAPH.md`.
   - Synchronize `ONBOARDING.md` and `bootstrap.sh` with Python 3.14+, `uv`, CodeGraph, and release practices.

---

## 3. Affected Users & Systems

- **Target Personas / Users**: Software developers, tech leads, engineering maintainers, autonomous AI agents (Antigravity, Jetski, ReviewAgent).
- **Affected Systems / Services**: Local CLI, verification harness, git hooks, CI/CD workflows, documentation, release scripts.
- **Third-Party Dependencies / Integrations**: `uv`, `colbymchenry/codegraph` (MCP / CLI integration).

---

## 4. Constraints & Boundaries

- **Python Version**: Minimum supported Python is 3.14+.
- **No Proprietary Graph Parser**: Do NOT build a custom code graph parser; leverage existing, mature tools (`colbymchenry/codegraph`) and focus on detection, guidance, and MCP orchestration.
- **README Cleanliness**: `README.md` must NOT contain ASCII directory file trees; point to `ONBOARDING.md` or dedicated doc sections instead.
- **Single-Command Verification**: All verification tests must continue to run in <1 second.
- **Backward Compatibility**: Verification and CLI must still execute cleanly if `uv` or `codegraph` are not yet installed on a user's machine.

---

## 5. Open Questions & Assumptions

1. *Threshold for CodeGraph reminder*: Set to >25 source files or >2,500 LOC as the inflection point where symbol indexing saves significant tokens.
2. *Advisory behavior*: The reminder is purely informational stdout; it must never cause `verify.sh` or git hooks to exit non-zero.

---

## 6. Approval & Handover

- **Product Owner Review**: In Review by @chuancc
- **Ready for Stage 2 (Design)**: Upon approval ➔ `docs/specs/008-modern-tooling-codegraph-and-release.md`
