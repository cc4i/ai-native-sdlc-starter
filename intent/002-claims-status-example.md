# Intent: User Claims Status Self-Service

**Author**: Jordan Ortiz (Claims Operations)  
**Date**: 2026-08-27  
**Status**: Approved  
**Target Milestone**: v1.0-mvp  

---

## 1. Problem Statement
- **Current State**: Customers currently have to call the contact center to ask about the status of their insurance claims.
- **User Pain / Friction**: Call center handlers spend roughly 35% of total call duration simply looking up claim statuses. Customers experience 10-15 minute queue times for simple status queries.
- **Impact & Urgency**: Reducing call volume by providing online status visibility will reduce call center costs and increase CSAT score.

---

## 2. Proposed Outcome
- Customers can log into the web portal and view real-time claim status, next required action, and expected resolution date.
- Statuses updated in real-time or cached with a max latency of 60 seconds.

---

## 3. Affected Users & Systems
- **Target Personas**: Policyholders / End customers.
- **Affected Systems**: Customer Web Portal, Claims Core REST API (`/api/v1/claims`).
- **Dependencies**: Existing Auth0 JWT authentication gateway.

---

## 4. Constraints & Boundaries
- **Security**: Zero new PII collected or logged in the portal session. Use existing authenticated session tokens only.
- **Rate Limiting**: The Claims Core API rate limits at 50 rps; the portal service must implement aggressive caching.
- **Out of Scope**: Online claim submission or document uploads (deferred to v1.1).

---

## 5. Open Questions & Assumptions
1. *Do third-party adjusters need access to this view?* -> **Resolved**: No, customer portal only for v1.0.

---

## 6. Approval & Handover
- **Product Owner Review**: Approved by @sarah-pm on 2026-08-27
- **Ready for Stage 2 (Design)**: `specs/001-claims-status-self-service.md`
