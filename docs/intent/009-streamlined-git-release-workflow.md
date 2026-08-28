# Intent: Streamlined Git-Native Release Workflow (Tag & Command Triggered)

**Author**: @antigravity  
**Date**: 2026-08-28  
**Status**: Draft  

---

## 1. Problem Statement

In Milestone 008, `scripts/release.sh` attempted to bump the `version` field in `pyproject.toml` and run `git commit` directly on the local `main` branch before creating the git tag.

When executed on `main`, this immediately triggered the repository's SDLC branch protection pre-commit hook:
```
🛡️  [SDLC Pre-Commit] Validating artifact chain and verification harness...
❌ SDLC VIOLATION: Direct commits to 'main' branch are forbidden.
👉 Rule: All changes must go through a feature branch and Pull Request review loop.
```

In modern AI-Native software engineering:
1. **Releases are checkpoints, not feature commits**: Releases tag existing, fully-reviewed commits on `main`. They should never attempt direct commits to `main`.
2. **Releases must be simple and git-native**: Release notes, author attributions, commit logs, and changelogs come directly from git history.
3. **Flexible triggers**: Developers should be able to trigger a release either by pushing a tag (`git tag` + `git push`) or via CLI command (`gh workflow run release.yml -f tag=v1.1.0` / `make release-remote`).

---

## 2. Desired Outcomes

1. **Zero-Commit Local Tagging**:
   - `scripts/release.sh` and `make release VERSION=vX.Y.Z` validate the semver format, ensure clean working tree, run `verify.sh`, and create the annotated git tag.
   - **No local `git commit`** is executed, guaranteeing 100% compliance with `main` branch protection.
2. **Dual-Trigger Release Automation**:
   - `.github/workflows/release.yml` triggers on tag push (`v*`) **AND** manual CLI/UI command dispatch (`workflow_dispatch` with `tag` input).
   - "Rest thing come from git": GitHub Release notes, changelog, and assets are generated automatically from git commits using `gh release create --generate-notes`.
3. **Single-Command CLI Release**:
   - Developer can release via command: `make release-remote VERSION=v1.1.0` or `gh workflow run release.yml -f tag=v1.1.0`.
4. **Comprehensive Documentation & Testing**:
   - Update `docs/RELEASES.md` with the simplified workflow.
   - Add unit tests verifying `release.sh` does not run `git commit`.

---

## 3. Scope & Boundaries

- **In Scope**:
  - `scripts/release.sh`: Remove `git commit` logic; add `--push` flag.
  - `Makefile`: Add `release-remote` target.
  - `.github/workflows/release.yml`: Add `workflow_dispatch` support.
  - `docs/RELEASES.md`: Update release instructions.
  - `tests/unit/test_release_script.py`: Test zero-commit guarantee.
- **Out of Scope**:
  - Modifying the branch protection rule itself (direct commits to `main` must remain forbidden for feature work).
