# Plan: Claims Status Self-Service Implementation

**Linked Spec**: [`specs/002-claims-status-example.md`](file:///Users/chuancc/mywork/ai/project-start/specs/002-claims-status-example.md)  
**Author**: Alex Chen (Staff Engineer)  
**Date**: 2026-08-27  
**Status**: Completed  
**Shipped**: 92c63bc  

---

## 1. Scope & Strategy

- **Objective**: Implement the backend claims status lookup endpoint with caching and ownership validation, followed by the frontend UI status component.
- **Strategy**: Test-Driven Development (TDD) in 3 micro-stepped execution groups.

---

## 2. File Change Map

| Path | Change Type | Purpose |
| :--- | :--- | :--- |
| `src/services/claims_service.py` | New | Domain logic for claim lookup, caching, and auth check |
| `src/api/routes/claims.py` | Modify | Route definition and error handler mapping |
| `tests/unit/test_claims_service.py` | New | Unit tests for domain rules & ownership validation |
| `tests/integration/test_claims_api.py` | New | End-to-end HTTP integration tests |
| `evals/eval-config.json` | Modify | Add regression evaluation test case |

---

## 3. Micro-Stepped Execution Groups

### Execution Group 1: Safety Harness & Domain Logic (TDD)
- [x] **Step 1.1 (Red)**: Write unit tests in `tests/unit/test_claims_service.py` for status evaluation, caching, and unauthorized access (Scenarios 1.1, 1.2, 1.3).
- [x] **Step 1.2 (Green)**: Implement `src/services/claims_service.py` with 60s cache layer.
- [x] **Step 1.3 (Refactor)**: Clean up types and docstrings. Verify all unit tests pass.

### Execution Group 2: API Route & Middleware Integration
- [x] **Step 2.1 (Red)**: Write integration contract tests in `tests/integration/test_claims_api.py`.
- [x] **Step 2.2 (Green)**: Wire router into `src/api/routes/claims.py` with JWT auth middleware.
- [x] **Step 2.3 (Verify)**: Run `make test`. Ensure zero regressions across entire suite.

### Execution Group 3: Continuous Evals & Verification
- [x] **Step 3.1**: Add test prompt and assertions to `evals/eval-config.json`.
- [x] **Step 3.2**: Run `make verify` and confirm zero lint/test/eval failures.
- [x] **Step 3.3**: Run `auditor` subagent and generate PR review report.

---

## 4. Risk Matrix & Mitigations

| Risk | Severity | Mitigation Strategy |
| :--- | :--- | :--- |
| Rate-limit breach on claims core API | High | 60-second in-memory TTL caching layer |
| Cross-tenant data leak | Critical | Strict equality assertion: `claim.user_id == auth_token.sub` |

---

## 5. Proof of Correctness & Harness

- `make verify` exited with code 0.
- 6 new unit tests passing (`tests/unit/test_claims_service.py`).
- 3 new integration tests passing (`tests/integration/test_claims_api.py`).
- Zero TODOs or mocked bypasses.
