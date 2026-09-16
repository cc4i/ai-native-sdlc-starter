# Code Review Policy & Guidelines (REVIEW.md)

## 🏷️ Severity Classification Tiers

### 🚨 Tier 1: Blocker (Must fix before merge)
- Broken functional behavior or violated `spec.md` acceptance criteria.
- Security vulnerabilities (hardcoded secrets, injection, auth bypass).
- Missing test coverage on critical code paths; gutted or skipped tests.

### ⚠️ Tier 2: Important (Requires resolution or documented exception)
- Unhandled edge cases (timeouts, network errors).
- Significant deviations from `plan.md`.
- Anti-shortcuts (unimplemented `TODO` stubs).

### 💡 Tier 3: Nit / Suggestion (Optional, non-blocking)
- Minor variable naming or readability suggestions.

---

## 🚦 Governance & Gates
- Automated review checks PR against `REVIEW.md`.
- Code Owner must approve all Tier 1 Blocker resolutions.
