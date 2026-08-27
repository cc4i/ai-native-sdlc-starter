---
name: spec-architect
description: Transform an approved intent.md into an unambiguous, testable technical spec.md with Gherkin acceptance criteria, API contracts, and edge cases.
---

# Spec Architect Skill

Use this skill to convert `intent/NNN-title.md` into a formal `specs/NNN-title.md`.

## 🎯 Process
1. **Read Intent**: Parse problem, constraints, and open questions from the linked intent artifact.
2. **Apply Architectural & Security Standards**:
   - Apply `secure-api-design` skill rules.
   - Enforce authentication, rate limiting, and zero-PII logging.
3. **Draft Gherkin Scenarios**: Every feature requirement MUST contain testable `Given / When / Then` acceptance criteria covering:
   - Happy path flow.
   - Unauthorized / forbidden access flow.
   - Malformed input / boundary condition flow.
   - Downstream failure / timeout flow.
4. **Format & Commit**: Format using `templates/spec.template.md` and save to `specs/NNN-[feature-slug].md`.
