# Code Review Policy & Guidelines (REVIEW.md)

This document defines the review standard for all human and AI-generated Pull Requests in this repository.

---

## 🎯 Review Objectives

In the AI-Native SDLC, routine syntax, formatting, and unit-test passes are automated. Human and AI reviewers focus on:
1. **Intent Alignment**: Does the diff fulfill the original requirements in `intent.md` and `spec.md`?
2. **Implementation Fidelity**: Does the diff match the approved steps and safety harnesses in `plan.md`?
3. **Risk & Security**: Does the diff introduce regressions, vulnerabilities, concurrency bugs, or unhandled failures?

---

## 🏷️ Severity Classification Tiers

Review findings must be classified into one of the following three tiers:

### 🚨 Tier 1: Blocker (Must fix before merge)
Issues that prevent deployment to any environment:
- Broken functional behavior or violated `spec.md` acceptance criteria.
- Security vulnerabilities (CWE top 25, auth bypass, injection, hardcoded credentials, secret leakage).
- Missing test coverage on critical or state-changing code paths.
- Gutted, disabled, or skipped tests.
- Breaking database migrations without backward compatibility.
- Data race conditions or resource/memory leaks.

### ⚠️ Tier 2: Important (Requires resolution or explicit exception)
Significant quality or maintainability issues:
- Unhandled edge cases (network timeout, upstream error, boundary condition).
- Significant deviations from the committed `plan.md` without documentation.
- Architecture violations (e.g., business logic leaking into presentation layer).
- Anti-shortcuts (unimplemented `TODO` items, placeholder stubs).
- Performance anti-patterns (e.g., N+1 database queries, unindexed queries).

### 💡 Tier 3: Nit / Suggestion (Optional, non-blocking)
Constructive feedback for future iterations:
- Minor variable or function naming suggestions.
- Non-critical code simplification or readability refinements.
- Documentation or comment improvements.

---

## 🔍 Review Passes Checklist

Every review pass evaluates the following areas:

### 1. Functional & Acceptance Verification
- [ ] Diff satisfies each `Given / When / Then` scenario in `spec.md`.
- [ ] All edge cases and negative test cases described in `spec.md` are covered.
- [ ] Error messages are clear, user-friendly, and contain no sensitive internal stack traces.

### 2. Security & Data Protection
- [ ] Authentication & authorization checks enforced on all endpoints.
- [ ] Input data validated against schemas; untrusted input rejected.
- [ ] PII and sensitive parameters are masked in logs and telemetry.
- [ ] Dependencies are scanned and approved.

### 3. Testing & Verification
- [ ] `make verify` passes cleanly with 0 errors/warnings.
- [ ] New code has accompanying automated unit/integration tests.
- [ ] Tests verify behavior, not trivial mock setups.

### 4. Traceability & Documentation
- [ ] PR description links to `intent.md`, `spec.md`, and `plan.md`.
- [ ] Any deviation from original plan is documented with rationale.

---

## 🚦 Governance & Approval Gates

- **AI Code Review**: Automated reviewers (e.g., `implementation-validator` or CI bot) review every PR and post findings classified by severity tier.
- **Auto-Fix Loop**: When `@agent fix` is mentioned on a review thread, the AI agent addresses the comment and pushes updated commits.
- **Human Release Gate**: A human Code Owner must review and approve all PRs containing **Blocker** resolutions or impacting production systems.
