# Master Product Roadmap (`plans/00-ROADMAP.md`)

This roadmap tracks all active and planned milestones for the repository across the AI-Native SDLC lifecycle.

---

## 🚀 Active Release: v1.0-mvp

| Milestone | Linked Spec | Linked Plan | Status | Shipped Commit | Owner |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **000: AI-Native SDLC Template & Engine** | [`specs/000-ai-sdlc-starter-template.md`](file:///Users/chuancc/mywork/ai/project-start/docs/specs/000-ai-sdlc-starter-template.md) | [`plans/000-ai-sdlc-starter-template.md`](file:///Users/chuancc/mywork/ai/project-start/docs/plans/000-ai-sdlc-starter-template.md) | COMPLETED | `92c63bc` | @antigravity |
| **001: Autonomous AI Code Review Agent** | [`specs/001-code-review-agent.md`](file:///Users/chuancc/mywork/ai/project-start/docs/specs/001-code-review-agent.md) | [`plans/001-code-review-agent.md`](file:///Users/chuancc/mywork/ai/project-start/docs/plans/001-code-review-agent.md) | COMPLETED | `92c63bc` | @antigravity |
| **002: Insurance Claims Status Reference** | [`specs/002-claims-status-example.md`](file:///Users/chuancc/mywork/ai/project-start/docs/specs/002-claims-status-example.md) | [`plans/002-claims-status-example.md`](file:///Users/chuancc/mywork/ai/project-start/docs/plans/002-claims-status-example.md) | COMPLETED | `92c63bc` | @alex-chen |
| **003: Strict SDLC Lifecycle Enforcement & Git Hooks** | [`specs/003-sdlc-lifecycle-enforcement-hooks.md`](file:///Users/chuancc/mywork/ai/project-start/docs/specs/003-sdlc-lifecycle-enforcement-hooks.md) | [`plans/003-sdlc-lifecycle-enforcement-hooks.md`](file:///Users/chuancc/mywork/ai/project-start/docs/plans/003-sdlc-lifecycle-enforcement-hooks.md) | COMPLETED | `ab40c52` | @product-owner |
| **004: Automated AI PR Review & Branch Protection** | [`specs/004-pr-review-and-branch-enforcement.md`](file:///Users/chuancc/mywork/ai/project-start/docs/specs/004-pr-review-and-branch-enforcement.md) | [`plans/004-pr-review-and-branch-enforcement.md`](file:///Users/chuancc/mywork/ai/project-start/docs/plans/004-pr-review-and-branch-enforcement.md) | COMPLETED | `4a0e5c4` | @product-owner |
| **005: SDLC Enhancements & Docs Restructure** | [`specs/005-sdlc-enhancements-and-docs-restructure.md`](file:///Users/chuancc/mywork/ai/project-start/docs/specs/005-sdlc-enhancements-and-docs-restructure.md) | [`plans/005-sdlc-enhancements-and-docs-restructure.md`](file:///Users/chuancc/mywork/ai/project-start/docs/plans/005-sdlc-enhancements-and-docs-restructure.md) | COMPLETED | `ce6b60b` | @antigravity |
| **006: README & Onboarding Documentation Alignment** | [`specs/006-update-readme-and-docs.md`](file:///Users/chuancc/mywork/ai/project-start/docs/specs/006-update-readme-and-docs.md) | [`plans/006-update-readme-and-docs.md`](file:///Users/chuancc/mywork/ai/project-start/docs/plans/006-update-readme-and-docs.md) | IN_CONSTRUCTION | - | @antigravity |

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
