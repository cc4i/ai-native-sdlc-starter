# Spec: [Feature / Improvement Name]

**Linked Intent**: [`intent/NNN-title.md`](file:///Users/chuancc/mywork/ai/project-start/intent)  
**Author**: [Architect / Product Owner / Agent]  
**Date**: [YYYY-MM-DD]  
**Status**: [Draft | Validated | Approved]  

---

## 1. Overview & Scope
*Summarize the functional and technical requirements derived from the approved intent artifact.*

- **Summary**: [High-level summary of what is being built]
- **Target Users**: [Personas and access tiers]
- **In Scope**: [List of capabilities included]
- **Out of Scope**: [List of capabilities excluded]

---

## 2. User Stories & Acceptance Criteria (Gherkin Scenarios)

### Story 1: [Primary User Flow]
**As a** [user role]  
**I want to** [action / capability]  
**So that** [benefit / business value]  

#### Scenario 1.1: [Happy path title]
```gherkin
Given [preconditions, e.g., an authenticated user with active subscription]
When [user performs action, e.g., requests claims status for claim "CLM-1234"]
Then [expected outcome, e.g., system returns status "In Review" with timestamp]
And [side effect, e.g., audit log entry is recorded]
```

#### Scenario 1.2: [Error / Edge case title]
```gherkin
Given [precondition, e.g., an authenticated user]
When [invalid input or network error occurs, e.g., non-existent claim ID "CLM-9999"]
Then [expected error response, e.g., system returns 404 with error code "CLAIM_NOT_FOUND"]
And [no internal system details or stack traces are leaked]
```

---

## 3. Architecture & Interface Contracts

### 3.1 Data Models & Schemas
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ExamplePayload",
  "type": "object",
  "properties": {
    "id": { "type": "string", "format": "uuid" },
    "status": { "type": "string", "enum": ["pending", "in_review", "approved", "rejected"] },
    "updatedAt": { "type": "string", "format": "date-time" }
  },
  "required": ["id", "status", "updatedAt"],
  "additionalProperties": false
}
```

### 3.2 API Contracts (REST / gRPC / Events)
- **Method & Route**: `GET /api/v1/claims/{id}/status`
- **Auth**: Bearer JWT (`scopes: ["claims:read"]`)
- **Rate Limit**: 50 req/sec per tenant

---

## 4. Policy, Security & Quality Constraints

- [ ] **Authentication & Access Control**: RBAC/ABAC verified on all routes.
- [ ] **Input Validation**: Strict schema enforcement; reject unknown fields.
- [ ] **PII & Logging**: Ensure zero sensitive or credit card/health data logged.
- [ ] **Performance SLA**: Response time under 200ms at 95th percentile.

---

## 5. Adversarial Review & Sign-Off

- **Spec Gate Verdict**: [ ] PASSED by `spec-validator` (2-of-3 skeptic majority)
- **Sign-off**: [ ] Tech Lead / Architect approval on YYYY-MM-DD
- **Ready for Stage 3 (Build)**: `plans/[NNN-title].md`
