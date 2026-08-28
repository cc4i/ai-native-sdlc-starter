# Specification: Align README.md and Onboarding Docs with Codebase Reality

**Linked Intent**: [`docs/intent/006-update-readme-and-docs.md`](file:///Users/chuancc/mywork/ai/project-start/docs/intent/006-update-readme-and-docs.md)  
**Author**: Antigravity Staff Architect  
**Date**: 2026-08-28  
**Status**: Ready for Planning  

---

## 1. Overview & Scope

This specification defines the content updates and structural synchronization required in `README.md` and `ONBOARDING.md` to reflect all architectural additions made through Milestone 005.

---

## 2. Gherkin Acceptance Scenarios

### Feature: Accurate Repository Architecture
```gherkin
Scenario: Repository file tree matches reality
  Given a developer or evaluator reads README.md
  When they inspect the "Repository Structure" section
  Then it displays the unified "docs/" hierarchy ("docs/intent/", "docs/specs/", "docs/plans/", "docs/reviews/", "docs/templates/")
  And it displays "bands.yaml", "hooks.json", "src/", "tests/", and "bootstrap.sh".

Scenario: Stage 1 through 6 walkthrough consistency
  Given a developer follows the Stage walkthrough in README.md
  When they execute commands for each stage
  Then Stage 1 references "docs/intent/NNN-*.md"
  And Stage 2 references "docs/specs/NNN-*.md"
  And Stage 3 references "docs/plans/NNN-*.md" and "docs/plans/00-ROADMAP.md" (with Shipped SHAs)
  And Stage 4 references "make verify" (33 tests) and "make eval"
  And Stage 5 references "make review-pr" and "docs/reviews/NNN-*.md"
  And Stage 6 references "bands.yaml", "scripts/check-control-bands.py", and "docs/templates/incident-intent.template.md".
```

---

## 3. Detailed Changes Required

1. **`README.md`**:
   - Update Stage summary table (lines 64–75) to reflect `docs/` paths and Stage 5/6 tooling.
   - Update repository tree (lines 79–125) with exact file inventory.
   - Update Stage 1–6 step-by-step instructions.
   - Add documentation for `make review-pr`, `bands.yaml`, and `hooks.json`.
2. **`ONBOARDING.md`**:
   - Update path references from `intent/`, `specs/`, `plans/` to `docs/intent/`, `docs/specs/`, `docs/plans/`.
   - Update commands table to include `make review-pr`.
