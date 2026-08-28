# Intent: Remove Legacy Branding References Across Entire Repository

**Author**: @chuancc  
**Date**: 2026-08-28  
**Status**: Approved  
**Target Milestone**: v1.1 - Evolution  

---

## 1. Problem Statement

The repository previously referenced both legacy dual-naming platforms and Antigravity across documentation, scripts, hooks, and test files. To standardize the project branding and eliminate obsolete or redundant naming:
- Legacy naming references must be completely removed from the entire repository.
- Branding and agent lifecycle hooks should focus exclusively on **Google Antigravity (AGY)** and general autonomous coding agent concepts.
- Script guard hooks and tests should be generalized to `scripts/agent_guard.py` and `tests/unit/test_agent_guard.py`.

---

## 2. Proposed Outcomes

1. **Clean Branding & Documentation**:
   - `README.md`, `ONBOARDING.md`, `bootstrap.sh`, `scripts/bootstrap.sh`, and markdown artifacts updated to reference Antigravity exclusively.
2. **Tooling & Hook Generalization**:
   - Guard hook script renamed to `scripts/agent_guard.py`.
   - `hooks.json` and `.gemini/hooks.json` updated to reference `agent_guard.py`.
   - Guard hook tests renamed to `tests/unit/test_agent_guard.py`.
3. **GitHub Repository Metadata**:
   - Remove legacy topics from repository topics using `gh repo edit`.
4. **Verification**:
   - Zero occurrences of legacy branding remain across the entire repository.
   - All tests pass via `make verify && make eval`.
