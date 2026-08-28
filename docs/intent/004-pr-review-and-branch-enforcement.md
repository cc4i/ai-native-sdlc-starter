# Intent: Automated AI PR Review & Branch Protection Enforcement

**Author**: Product Owner & DevOps Lead  
**Date**: 2026-08-28  
**Status**: Approved  
**Target Milestone**: v1.0-mvp  

---

## 1. Problem Statement
- **Current State**: Developers and AI agents can commit directly to the `main` branch, bypassing the GitHub Pull Request review stage. Furthermore, pull requests opened on GitHub lacked an automated AI review action that inspects the diff, scores it against `REVIEW.md` and `spec.md`, and posts an audit report comment back onto the PR.
- **User Pain / Friction**: Without enforced branch protection and automated PR reviews, human code owners are forced to manually inspect every line of diff or risk unverified, unreviewed code merging straight to production.
- **Impact & Urgency**: Critical. To be a true AI-native SDLC template, the repository must prevent direct commits to `main`, automate multi-pass PR review audits in CI, store persistent `reviews/` artifacts, and require human approval gates on Pull Requests.

---

## 2. Proposed Outcome
1. **Branch Protection**: Block all local commits directly on `main`/`master` in `.githooks/pre-commit`, requiring developers and agents to work on feature branches (`feat/NNN-*`, `fix/NNN-*`).
2. **Automated PR Review in CI**: Enhance `.github/workflows/ai-pr-review.yml` to automatically execute the `ReviewAgent` on PR diffs, output a markdown audit report, and post it as a comment on the GitHub PR.
3. **CLI PR Review Command**: Enhance `src/cli.py` with `review-pr` command to review git diffs against base branches and specs.
4. **Persistent `reviews/` Artifact Store**: Create `reviews/` directory to store versioned PR Review Audit Reports (`reviews/NNN-[title].md`).
5. **Live Verification**: Run this entire milestone through a real GitHub Pull Request with automated AI review and merge.

---

## 3. Affected Users & Systems
- **Target Personas**: Developers, Autonomous Subagents, Code Owners, CI/CD pipelines.
- **Affected Systems**: `.githooks/pre-commit`, `.github/workflows/ai-pr-review.yml`, `src/cli.py`, `reviews/`, `GEMINI.md`, `bootstrap.sh`.

---

## 4. Constraints & Boundaries
- **Zero External API Keys Needed for Baseline Review**: The baseline review engine must run self-contained in GitHub Actions without requiring external paid API keys.
- **Strict Verdict Handling**: If the ReviewAgent outputs `BLOCKED` or `CHANGES_REQUESTED`, the GitHub Actions PR check must fail (non-zero exit).

---

## 5. Approval & Handover
- **Product Owner Review**: Approved by @product-owner on 2026-08-28
- **Ready for Stage 2 (Design)**: `specs/004-pr-review-and-branch-enforcement.md`
