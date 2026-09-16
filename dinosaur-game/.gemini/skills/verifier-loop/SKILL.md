---
name: verifier-loop
description: Establish and run the inner verification feedback loop (make verify, make test, make lint) before marking tasks complete.
---

# Verifier Loop Skill

1. Always execute `make verify` before reporting any task complete.
2. If tests fail, fix the implementation code. Never weaken or modify test assertions to force a pass!
3. Attach test counts and proof in execution summary.
