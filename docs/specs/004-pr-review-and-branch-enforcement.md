# Spec: Automated AI PR Review & Branch Protection Enforcement

**Linked Intent**: [`intent/004-pr-review-and-branch-enforcement.md`](../../intent/004-pr-review-and-branch-enforcement.md)  
**Author**: Systems Architect & Security Lead  
**Date**: 2026-08-28  
**Status**: Approved  

---

## 1. Overview & Architecture

Formalize requirements for automated PR reviews and local branch protection to ensure all code changes flow through:
`Feature Branch ➔ Local Verify ➔ Git Push ➔ GitHub PR ➔ CI ReviewAgent Audit ➔ Code Owner Approval ➔ Merge to main`.

```
                    ┌─────────────────────────────────────────────────┐
                    │ 🚫 Local Hook: Forbid Direct Commits on 'main'  │
                    │ Force: git checkout -b feat/NNN-feature-name    │
                    └─────────────────────────────────────────────────┘
                                              │
                                              ▼
                    ┌─────────────────────────────────────────────────┐
                    │ 🧪 Local Verification: make verify & make eval  │
                    └─────────────────────────────────────────────────┘
                                              │
                                              ▼
                    ┌─────────────────────────────────────────────────┐
                    │ 🚀 Git Push Branch & Open PR (gh pr create)     │
                    └─────────────────────────────────────────────────┘
                                              │
                                              ▼
                    ┌─────────────────────────────────────────────────┐
                    │ 🤖 GitHub Action (.github/workflows/ai-pr-review)│
                    │ 1. Run ReviewAgent on PR Diff                   │
                    │ 2. Post Review Audit Comment to GitHub PR       │
                    │ 3. Fail check if BLOCKED / CHANGES_REQUESTED    │
                    └─────────────────────────────────────────────────┘
                                              │
                                              ▼
                    ┌─────────────────────────────────────────────────┐
                    │ 👥 Human Code Owner Signs Off & Merges PR       │
                    └─────────────────────────────────────────────────┘
```

---

## 2. User Stories & Acceptance Criteria (Gherkin)

### Story 1: Block Direct Commits on `main` / `master`
**As a** repository maintainer  
**I want** `git commit` on `main` to be blocked by pre-commit hook  
**So that** all changes must go through a feature branch and pull request  

#### Scenario 1.1: Direct commit on `main` is rejected
```gherkin
Given the current git branch is "main" or "master"
When the user executes "git commit -m 'some commit'"
Then the pre-commit hook aborts with exit code 1
And prints: "❌ SDLC VIOLATION: Direct commits to 'main' branch are forbidden."
And instructs the user to branch: "git checkout -b feat/NNN-feature-name"
```

#### Scenario 1.2: Commits on feature branch are permitted
```gherkin
Given the current git branch is "feat/004-pr-review-and-branch-enforcement"
And artifact chain is present and "make verify" passes
When the user executes "git commit"
Then the commit succeeds
```

### Story 2: Automated AI PR Review & Comment in CI
**As a** pull request reviewer and developer  
**I want** CI to run `ReviewAgent` on every opened/updated PR  
**So that** security leaks, dangerous AST calls, and spec deviations are posted directly on GitHub  

#### Scenario 2.1: CI executes review and produces report
```gherkin
Given a Pull Request opened on GitHub targeting "main"
When GitHub Actions workflow "ai-pr-review.yml" runs
Then it executes "python3 -m src.cli review-pr" on all changed files
And generates a markdown report matching "REVIEW.md"
And posts or updates the audit report comment on the PR
And passes the check if verdict is "PASS"
```

#### Scenario 2.2: CI fails PR check on security blocker
```gherkin
Given a Pull Request containing a hardcoded API secret
When "ai-pr-review.yml" runs
Then the ReviewAgent issues verdict "BLOCKED"
And the CI job exits with code 1
And the PR is blocked from merging
```

### Story 3: CLI PR Review Command
**As a** developer or agent running locally  
**I want** a CLI command `python3 -m src.cli review-pr`  
**So that** I can review branch diffs locally before opening a PR  

#### Scenario 3.1: Local review-pr execution
```gherkin
When the user runs "python3 -m src.cli review-pr --base origin/main --output reviews/004-audit.md"
Then all modified files in the branch diff are analyzed
And the aggregated audit report is written to "reviews/004-audit.md"
And printed to stdout
```

---

## 3. Adversarial Review & Sign-Off
- **Spec Validator Gate**: PASSED (3/3 skeptics)
- **Approved by**: @product-owner on 2026-08-28
- **Ready for Stage 3 (Build)**: `plans/004-pr-review-and-branch-enforcement.md`
