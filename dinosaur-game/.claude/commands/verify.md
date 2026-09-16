---
description: Run the single-command verification suite (make verify) and validate zero regressions
---

Run make verify in the terminal to execute the full quality verification suite:
- Linting and type checks
- Code format validation
- Unit and integration tests
- Build checks

If any check fails, analyze the failure and fix the implementation code. Never alter failing test assertions to mask a bug. Report the final test count and verification status clearly.
