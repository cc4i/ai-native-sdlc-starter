---
description: Run the autonomous ReviewAgent audit on branch diff and produce a PR review report
---

Execute `make review-pr` or `python3 -m src.cli review-pr --base origin/main` to run the autonomous multi-pass review agent:
1. Pass 1: Secret & Credential Scanning (no hardcoded tokens or keys).
2. Pass 2: AST Security & Anti-Pattern Analysis (eval, exec, shell injection).
3. Pass 3: Spec Acceptance Compliance (checks Gherkin criteria in `docs/specs/`).
4. Pass 4: Semantic Review (Gemini, Claude, or OpenAI review if API keys are configured).

Report the verdict (`PASS`, `CHANGES_REQUESTED`, `BLOCKED`) and findings categorized by severity (Blocker, Important, Nit).
