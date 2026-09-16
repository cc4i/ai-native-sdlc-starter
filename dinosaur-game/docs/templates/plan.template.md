# Plan: [Implementation Task / Milestone Name]

**Linked Spec**: [`specs/NNN-title.md`](file:///specs)  
**Author**: [Architect / Engineer / Agent]  
**Date**: [YYYY-MM-DD]  
**Status**: [Draft | In Progress | Completed]  

---

## 1. Scope & Strategy

- **Objective**: [Clear 1-2 sentence description of what will be implemented]
- **Strategy**: [e.g., TDD, Strangler Fig, Additive Migration, Parallel Groups]
- **Estimated Execution Groups**: [e.g., 3 sequential groups, 2 parallel workers]

---

## 2. File Change Map

| Path | Change Type | Purpose / Description |
| :--- | :--- | :--- |
| `src/domain/...` | New / Modify | Core domain logic |
| `src/api/...` | Modify | Route & validation integration |
| `tests/unit/...` | New | Unit tests for domain rules |
| `tests/integration/...` | New / Modify | End-to-end HTTP contract tests |

---

## 3. Micro-Stepped Execution Groups

### Execution Group 1: Safety Harness & Core Domain Logic (TDD)
- [ ] **Step 1.1 (Red)**: Write unit tests in `tests/unit/` covering domain states. Verify tests fail as expected.
- [ ] **Step 1.2 (Green)**: Implement core logic in `src/` to satisfy unit tests. Verify tests pass.
- [ ] **Step 1.3 (Refactor)**: Clean up types and ensure zero lint warnings. Run `make verify`.

### Execution Group 2: API Endpoints & Route Wiring
- [ ] **Step 2.1 (Red)**: Write integration contract test in `tests/integration/`.
- [ ] **Step 2.2 (Green)**: Wire controller and input validation into routes.
- [ ] **Step 2.3 (Verify)**: Run full test suite (`make test`). Verify zero regressions.

### Execution Group 3: Documentation, Evals & Cleanup
- [ ] **Step 3.1**: Update documentation and schema definitions.
- [ ] **Step 3.2**: Add regression eval test case to `evals/eval-config.json`.
- [ ] **Step 3.3**: Run `make verify` and prepare PR review artifact.

---

## 4. Risk Matrix & Mitigations

| Risk | Severity | Mitigation Strategy |
| :--- | :--- | :--- |
| Upstream service rate limits | Medium | Implement caching layer with 60s TTL |
| Unhandled error leaking stack trace | High | Global error boundary and strict DTO mapping |

---

## 5. Proof of Correctness & Harness

- [ ] **Command**: `make verify` exits code 0.
- [ ] **Unit Tests**: All unit tests passing in `tests/unit/`.
- [ ] **Integration Tests**: All integration tests passing in `tests/integration/`.
- [ ] **Zero Anti-Shortcuts**: No `TODO`, `FIXME`, or mocked implementations remaining.
