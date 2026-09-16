---
name: secure-api-design
description: Apply enterprise security, privacy, and API standards to designs and code.
---

# Secure API Design & Governance Skill

1. **Auth**: Require valid token/session on all endpoints; verify record ownership.
2. **Input Validation**: Validate payload schemas; reject unknown attributes.
3. **Privacy**: Never log passwords, tokens, SSNs, or PII.
4. **Resilience**: Enforce timeouts, rate limits, and fallback caching.
