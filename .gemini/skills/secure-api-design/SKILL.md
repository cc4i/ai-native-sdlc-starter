---
name: secure-api-design
description: Apply security, privacy, and API standards to designs, code, and review passes. Trigger whenever creating/updating endpoints, models, or authentication flows.
---

# Secure API Design & Governance Skill

This skill enforces baseline enterprise security and privacy standards.

## 🛡️ Core Rules
1. **Authentication & Authorization**:
   - Every external endpoint must require valid authentication credentials (e.g. JWT/OAuth2) except explicit `/health` or `/metrics`.
   - Always verify tenant and user ownership (`sub` matching record `user_id`).
2. **Input Validation**:
   - Validate payload bodies against strict schemas (e.g., Pydantic, Zod, JSON Schema).
   - Reject unknown / unexpected fields (prevent mass assignment).
3. **Data Classification & Privacy (PII)**:
   - Sensitive fields (passwords, tokens, SSNs, credit card numbers) must NEVER appear in application logs or unmasked error messages.
4. **Resilience & Rate Limiting**:
   - Protect downstream services with timeout budgets, circuit breakers, and TTL caching where appropriate.
