---
name: verifier-loop
description: Establish and run the inner verification feedback loop (make verify, make test, make lint) before marking tasks complete.
---

# Verifier Loop Skill

Give Antigravity a deterministic way to evaluate and prove its own work before a human reviews it.

## 🎯 Process
1. **Never Report Done Without Running Verification**: Always execute `make verify` (or `./scripts/verify.sh`).
2. **Handle Failures Internally**:
   - If tests fail, diagnose the root cause in the implementation code.
   - **DO NOT modify the test assertions** to make a failing test pass unless the test was proven to contradict `spec.md`.
3. **Attach Proof in Responses**:
   - Always report test count, pass/fail status, and linter output in your summary.
