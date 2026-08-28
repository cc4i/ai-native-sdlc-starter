# Plan: Streamlined Git-Native Release Workflow (Tag & Command Triggered)

**Linked Spec**: [`docs/specs/009-streamlined-git-release-workflow.md`](../specs/009-streamlined-git-release-workflow.md)  
**Author**: @antigravity  
**Status**: Complete  

---

## 1. Scope & Strategy

Remove all file mutation and commit logic from `scripts/release.sh` so it can be executed safely on protected branches like `main`. Add dual-trigger (`push: tags` and `workflow_dispatch`) support to `.github/workflows/release.yml` and provide convenient CLI command targets in `Makefile`.

---

## 2. Micro-Stepped Execution Groups

### Group 1: Streamline `scripts/release.sh` & Update `Makefile`
- [x] Remove `pyproject.toml` version bump and `git commit` from `scripts/release.sh`.
- [x] Add `--push` flag to `scripts/release.sh` to optionally push tag after creation.
- [x] Add `release-push` and `release-remote` targets to `Makefile`.

### Group 2: Dual-Trigger GitHub Release Workflow
- [x] Add `workflow_dispatch` trigger with `tag` and `target_commit` inputs to `.github/workflows/release.yml`.
- [x] Support `--target` in `gh release create` for workflow_dispatch events.

### Group 3: Tests & Documentation
- [x] Add unit test in `tests/unit/test_release_script.py` asserting `release.sh` contains zero `git commit` calls.
- [x] Update `docs/RELEASES.md` reflecting tag push and command-driven release triggers.
- [x] Update `docs/plans/00-ROADMAP.md` tracking Milestone 009.
- [x] Verify clean execution with `make verify && make eval`.
