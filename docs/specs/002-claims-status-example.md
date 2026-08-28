# Spec: User Claims Status Self-Service

**Linked Intent**: [`intent/002-claims-status-example.md`](../../intent/002-claims-status-example.md)  
**Author**: Alex Chen (Staff Architect)  
**Date**: 2026-08-27  
**Status**: Approved  

---

## 1. Overview & Scope

Provide a secure, cached REST endpoint and React UI panel enabling customers to retrieve real-time claims status and expected resolution dates.

- **In Scope**:
  - Backend `GET /api/v1/claims/{id}/status` endpoint.
  - Integration with existing Auth0 JWT middleware.
  - In-memory/Redis TTL caching (60s).
  - Frontend `StatusPanel` component with 4 distinct visual states.
- **Out of Scope**:
  - Modifying claim records or submitting new claims.

---

## 2. User Stories & Acceptance Criteria (Gherkin)

### Story 1: View Claim Status
**As an** authenticated policyholder  
**I want to** view my claim status in the web portal  
**So that** I know the progress without calling customer support  

#### Scenario 1.1: Successful claim status retrieval
```gherkin
Given a policyholder authenticated with valid JWT holding "sub: user_123"
And a claim with ID "CLM-8801" belonging to "user_123" in state "UNDER_REVIEW"
When the user sends GET request to "/api/v1/claims/CLM-8801/status"
Then the response code is 200 OK
And the JSON payload contains:
  | field         | value           |
  | claimId       | CLM-8801        |
  | status        | UNDER_REVIEW    |
  | nextStep      | Adjuster Review |
  | estimatedDate | 2026-09-05      |
```

#### Scenario 1.2: Unauthorized access to another user's claim
```gherkin
Given a policyholder authenticated with "sub: user_456"
When the user requests status for claim "CLM-8801" (owned by "user_123")
Then the response code is 403 Forbidden
And error code is "ACCESS_DENIED"
And no internal claim details are returned
```

#### Scenario 1.3: Non-existent claim lookup
```gherkin
Given an authenticated user
When the user requests status for non-existent claim "CLM-0000"
Then the response code is 404 Not Found
And error code is "CLAIM_NOT_FOUND"
```

---

## 3. Architecture & API Contract

### 3.1 Endpoint Contract
`GET /api/v1/claims/:claimId/status`

**Headers**:
- `Authorization: Bearer <jwt_token>`

**Response (200 OK)**:
```json
{
  "claimId": "CLM-8801",
  "status": "UNDER_REVIEW",
  "nextStep": "Adjuster Review",
  "estimatedDate": "2026-09-05T00:00:00Z",
  "cachedAt": "2026-08-27T10:00:00Z"
}
```

---

## 4. Policy, Security & Quality Constraints
- [x] **Auth Check**: Must verify `claim.userId === token.sub`.
- [x] **Rate Limit & Caching**: Cache responses for 60s to prevent hitting downstream 50 rps ceiling.
- [x] **PII Protection**: Do not return policyholder SSN, bank details, or claim notes in this response.

---

## 5. Adversarial Review & Sign-Off
- **Spec Validator Gate**: PASSED (3/3 skeptics approved, zero ambiguities)
- **Approved by**: @sarah-pm and @alex-architect on 2026-08-27
- **Ready for Stage 3 (Build)**: `plans/001-claims-status-self-service.md`
