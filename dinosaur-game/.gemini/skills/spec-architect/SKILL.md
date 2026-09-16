---
name: spec-architect
description: Transform an approved intent.md into an unambiguous, testable technical spec.md with Gherkin acceptance criteria.
---

# Spec Architect Skill

1. Parse problem, constraints, and open questions from linked `intent.md`.
2. Apply `secure-api-design` standards.
3. Draft Gherkin scenarios (`Given / When / Then`) covering happy paths, auth errors, boundary inputs, and timeouts.
4. Output to `specs/NNN-[feature-slug].md`.
