# Master Product Roadmap (`plans/00-ROADMAP.md`)

This roadmap tracks all active and planned milestones for the repository across the AI-Native SDLC lifecycle.

---

## 🚀 Active Release: v1.1-evolution

| Milestone | Linked Spec | Linked Plan | Status | Shipped Commit | Owner |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **008: Modern Tooling (uv), CodeGraph & Release Workflow** | [`specs/008-modern-tooling-codegraph-and-release.md`](../specs/008-modern-tooling-codegraph-and-release.md) | [`plans/008-modern-tooling-codegraph-and-release.md`](008-modern-tooling-codegraph-and-release.md) | COMPLETED | `2661740` | @antigravity |
| **009: Streamlined Release Workflow (Tag & Cmd Triggered)** | [`specs/009-streamlined-git-release-workflow.md`](../specs/009-streamlined-git-release-workflow.md) | [`plans/009-streamlined-git-release-workflow.md`](009-streamlined-git-release-workflow.md) | COMPLETED | `52c3fd1` | @antigravity |
| **010: Remove Legacy Branding References** | [`specs/010-remove-legacy-branding.md`](../specs/010-remove-legacy-branding.md) | [`plans/010-remove-legacy-branding.md`](010-remove-legacy-branding.md) | COMPLETED | `a5b3d51` | @antigravity |

---

## 📦 Previous Releases

### v1.0-mvp (Completed)

| Milestone | Linked Spec | Linked Plan | Status | Shipped Commit | Owner |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **000: AI-Native SDLC Template & Engine** | [`specs/000-ai-sdlc-starter-template.md`](../specs/000-ai-sdlc-starter-template.md) | [`plans/000-ai-sdlc-starter-template.md`](000-ai-sdlc-starter-template.md) | COMPLETED | `92c63bc` | @antigravity |
| **001: Autonomous AI Code Review Agent** | [`specs/001-code-review-agent.md`](../specs/001-code-review-agent.md) | [`plans/001-code-review-agent.md`](001-code-review-agent.md) | COMPLETED | `92c63bc` | @antigravity |
| **002: Insurance Claims Status Reference** | [`specs/002-claims-status-example.md`](../specs/002-claims-status-example.md) | [`plans/002-claims-status-example.md`](002-claims-status-example.md) | COMPLETED | `92c63bc` | @alex-chen |
| **003: Strict SDLC Lifecycle Enforcement & Git Hooks** | [`specs/003-sdlc-lifecycle-enforcement-hooks.md`](../specs/003-sdlc-lifecycle-enforcement-hooks.md) | [`plans/003-sdlc-lifecycle-enforcement-hooks.md`](003-sdlc-lifecycle-enforcement-hooks.md) | COMPLETED | `ab40c52` | @product-owner |
| **004: Automated AI PR Review & Branch Protection** | [`specs/004-pr-review-and-branch-enforcement.md`](../specs/004-pr-review-and-branch-enforcement.md) | [`plans/004-pr-review-and-branch-enforcement.md`](004-pr-review-and-branch-enforcement.md) | COMPLETED | `4a0e5c4` | @product-owner |
| **005: SDLC Enhancements & Docs Restructure** | [`specs/005-sdlc-enhancements-and-docs-restructure.md`](../specs/005-sdlc-enhancements-and-docs-restructure.md) | [`plans/005-sdlc-enhancements-and-docs-restructure.md`](005-sdlc-enhancements-and-docs-restructure.md) | COMPLETED | `ce6b60b` | @antigravity |
| **006: README & Onboarding Documentation Alignment** | [`specs/006-update-readme-and-docs.md`](../specs/006-update-readme-and-docs.md) | [`plans/006-update-readme-and-docs.md`](006-update-readme-and-docs.md) | COMPLETED | `f9770f8` | @antigravity |
| **007: Autonomous PR Inline Review Engine (Gemini 3.7 Flash)** | [`specs/007-inline-pr-review-and-gemini.md`](../specs/007-inline-pr-review-and-gemini.md) | [`plans/007-inline-pr-review-and-gemini.md`](007-inline-pr-review-and-gemini.md) | COMPLETED | `0ee3921` | @antigravity |

---

## 🔮 Backlog & Future Releases (v1.1+)

- [ ] GitHub App Webhook Integration for auto-reviewing PRs
- [ ] LLM Provider Router (Gemini Pro / Claude 3.5 Sonnet / Local Ollama)
- [ ] Automated Fix Generation via `@agent fix` comments

---

## 📊 Milestone Lifecycle State Machine

Each milestone advances through strict gates:
```
[PROPOSED] ──► [SPEC_DRAFT] ──► [SPEC_VALIDATED] ──► [PLAN_DRAFT] ──► [PLAN_VALIDATED] ──► [IN_CONSTRUCTION] ──► [AUDITED] ──► [COMPLETED]
```
