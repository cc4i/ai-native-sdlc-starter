# Plan: Align README.md and Onboarding Docs with Codebase Reality

**Linked Spec**: [`docs/specs/006-update-readme-and-docs.md`](file:///Users/chuancc/mywork/ai/project-start/docs/specs/006-update-readme-and-docs.md)  
**Author**: Antigravity Staff Architect  
**Date**: 2026-08-28  
**Status**: Ready for Construction  

---

## 1. Scope & Execution Strategy

- **Group 1**: Update `README.md` to align with the complete `docs/` hierarchy, add `src/`, `tests/`, `bands.yaml`, `hooks.json`, and update the Stage 1–6 walkthrough.
- **Group 2**: Update `ONBOARDING.md` to reference `docs/` paths and add `make review-pr`.
- **Group 3**: Run `make verify` and `make eval`, generate review audit, open Pull Request #4, and merge!

---

## 2. Micro-Stepped Tasks

### Execution Group 1: README.md Overhaul
- [x] Update "The 6 Stages at a Glance" table in `README.md`.
- [x] Overhaul "Repository Structure" tree diagram with all real files and directories.
- [x] Update Stage 1 through Stage 6 step-by-step walkthroughs with `docs/` paths, `make review-pr`, `bands.yaml`, and `hooks.json`.

### Execution Group 2: ONBOARDING.md Synchronization
- [x] Update artifact paths in `ONBOARDING.md` from root folders to `docs/`.
- [x] Add `make review-pr` to commands table.

### Execution Group 3: Verification, PR & Merge
- [x] Run `make verify` and `make eval`.
- [x] Generate Stage 5 review audit report `docs/reviews/006-update-readme-and-docs.md`.
- [x] Commit on branch `feat/006-update-readme-and-docs`, push, and open Pull Request #4.
- [ ] Verify GitHub Actions CI and merge PR!
