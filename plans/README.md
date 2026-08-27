# Stage 3: Implementation Plans (`plans/`)

This directory houses all Stage 3 implementation plans and release roadmaps.

## 🎯 Rules
1. **Plan Before Code**: Never implement non-trivial code changes without an approved `plan.md`.
2. **Micro-Stepped Tasks**: Break work into small, atomic execution groups with explicit `Red -> Green -> Refactor` TDD steps.
3. **Traceability**: Link directly to the underlying `specs/NNN-title.md`.
4. **Adversarial Plan Validation**: Run the `plan-validator` subagent to catch ordering bugs and false codebase assumptions.
5. **Living Document**: Check off tasks as you complete them; keep plan synchronized with code in the same commit.

## 📄 File Naming Convention
- `00-ROADMAP.md` (Release milestones and progress tracking)
- `NNN-feature-name.md` (e.g., `001-claims-status-self-service.md`)
