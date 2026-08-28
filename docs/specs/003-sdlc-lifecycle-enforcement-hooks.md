# Spec: Strict SDLC Lifecycle Enforcement, Git Hooks & CI Merge Gates

**Linked Intent**: [`intent/003-sdlc-lifecycle-enforcement-hooks.md`](file:///Users/chuancc/mywork/ai/project-start/intent/003-sdlc-lifecycle-enforcement-hooks.md)  
**Author**: Staff Systems Architect & DevOps  
**Date**: 2026-08-27  
**Status**: Approved  

---

## 1. Overview & Architecture

Implement a deterministic 3-tier enforcement engine that prevents any code changes from reaching Git commits or merging into `main` without completing the full unbroken loop:
`intent.md ➔ spec.md ➔ plan.md ➔ make verify ➔ REVIEW.md audit ➔ production merge`.

```
                  ┌────────────────────────────────────────────────────────┐
                  │ 🛡️ TIER 1: Local Pre-Commit Hook (.githooks/pre-commit) │
                  └────────────────────────────────────────────────────────┘
                                            │
                        ┌───────────────────┴───────────────────┐
                        ▼                                       ▼
             Touched code under src/?               Only markdown/docs?
                        │                                       │
            ┌───────────┴───────────┐                           ▼
            ▼                       ▼                     Allow commit
    Missing intent/spec/     Valid artifacts &
    plan or make verify fails   make verify passes
            │                       │
            ▼                       ▼
      REJECT COMMIT           ALLOW COMMIT
            │
            ▼
┌──────────────────────────────────────────────────────────┐
│ 🛡️ TIER 2: Local Pre-Push Hook (.githooks/pre-push)       │
│ Runs `make eval` (Continuous AI regression evaluations)  │
└──────────────────────────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────┐
│ 🛡️ TIER 3: CI Server Merge Gate (.github/workflows)      │
│ Verifies PR artifact integrity, review verdict & tests   │
└──────────────────────────────────────────────────────────┘
```

---

## 2. User Stories & Acceptance Criteria (Gherkin)

### Story 1: Pre-Commit Hook Enforcement
**As a** repository maintainer  
**I want** `git commit` to block changes to `src/` if artifacts or tests are missing  
**So that** no ungrounded or untested code enters the Git history  

#### Scenario 1.1: Block commit when code is staged without active plan
```gherkin
Given a staged change in "src/services/new_feature.py"
And no staged or existing "plans/NNN-*.md" corresponds to this feature
When the user executes "git commit -m 'add new feature'"
Then the pre-commit hook aborts with exit code 1
And prints an error: "❌ SDLC Violation: Code modified in src/ without corresponding plan.md artifact."
And provides remediation instructions to create intent and plan first
```

#### Scenario 1.2: Block commit when `make verify` fails
```gherkin
Given staged changes in "src/" and corresponding "plans/001-feature.md"
When "make verify" fails due to a failing unit test or leftover TODO stub
Then the pre-commit hook aborts with exit code 1
And prints: "❌ SDLC Violation: Local verification loop failed. Run 'make verify' to debug."
```

#### Scenario 1.3: Allow commit when all checks pass
```gherkin
Given staged changes in "src/"
And complete artifact chain ("intent/001-*.md", "specs/001-*.md", "plans/001-*.md") exists
And "make verify" exits with code 0
When the user executes "git commit"
Then the commit succeeds cleanly
```

### Story 2: Automatic Git Hook Installation
**As a** developer cloning or bootstrapping this repository  
**I want** hooks configured automatically on `make init` and `bootstrap.sh`  
**So that** enforcement works out of the box with zero manual configuration  

#### Scenario 2.1: Hook activation
```gherkin
When the user runs "make init" or "./bootstrap.sh"
Then "git config core.hooksPath .githooks" is executed
And all hook scripts in ".githooks/" are marked executable (+x)
```

---

## 3. Adversarial Review & Sign-Off
- **Spec Validator Gate**: PASSED (3/3 Skeptics)
- **Approved by**: @product-owner on 2026-08-27
- **Ready for Stage 3 (Build)**: `plans/003-sdlc-lifecycle-enforcement-hooks.md`
