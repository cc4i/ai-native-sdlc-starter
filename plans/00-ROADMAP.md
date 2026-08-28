# Master Product Roadmap (`plans/00-ROADMAP.md`)

This roadmap tracks all active and planned milestones for the repository across the AI-Native SDLC lifecycle.

---

## 🚀 Active Release: v1.0-mvp

| Milestone | Linked Spec | Linked Plan | Status | Owner |
| :--- | :--- | :--- | :--- | :--- |
| **000: AI-Native SDLC Template & Engine** | [`specs/000-ai-sdlc-starter-template.md`](file:///Users/chuancc/mywork/ai/project-start/specs/000-ai-sdlc-starter-template.md) | [`plans/000-ai-sdlc-starter-template.md`](file:///Users/chuancc/mywork/ai/project-start/plans/000-ai-sdlc-starter-template.md) | COMPLETED | @antigravity |
| **001: Autonomous AI Code Review Agent** | [`specs/001-code-review-agent.md`](file:///Users/chuancc/mywork/ai/project-start/specs/001-code-review-agent.md) | [`plans/001-code-review-agent.md`](file:///Users/chuancc/mywork/ai/project-start/plans/001-code-review-agent.md) | COMPLETED | @antigravity |
| **002: Insurance Claims Status Reference** | [`specs/002-claims-status-example.md`](file:///Users/chuancc/mywork/ai/project-start/specs/002-claims-status-example.md) | [`plans/002-claims-status-example.md`](file:///Users/chuancc/mywork/ai/project-start/plans/002-claims-status-example.md) | COMPLETED | @alex-chen |
| **003: Strict SDLC Lifecycle Enforcement & Git Hooks** | [`specs/003-sdlc-lifecycle-enforcement-hooks.md`](file:///Users/chuancc/mywork/ai/project-start/specs/003-sdlc-lifecycle-enforcement-hooks.md) | [`plans/003-sdlc-lifecycle-enforcement-hooks.md`](file:///Users/chuancc/mywork/ai/project-start/plans/003-sdlc-lifecycle-enforcement-hooks.md) | COMPLETED | @product-owner |
| **004: Automated AI PR Review & Branch Protection** | [`specs/004-pr-review-and-branch-enforcement.md`](file:///Users/chuancc/mywork/ai/project-start/specs/004-pr-review-and-branch-enforcement.md) | [`plans/004-pr-review-and-branch-enforcement.md`](file:///Users/chuancc/mywork/ai/project-start/plans/004-pr-review-and-branch-enforcement.md) | COMPLETED | @product-owner |

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
