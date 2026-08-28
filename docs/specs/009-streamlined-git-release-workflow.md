# Spec: Streamlined Git-Native Release Workflow (Tag & Command Triggered)

**Linked Intent**: [`docs/intent/009-streamlined-git-release-workflow.md`](../intent/009-streamlined-git-release-workflow.md)  
**Author**: @antigravity  
**Date**: 2026-08-28  
**Status**: Validated  

---

## 1. Technical Requirements & Contracts

### 1.1 `scripts/release.sh` Refactoring Contract
- **No Working Tree Mutations**: `release.sh` MUST NOT run `git commit`, `sed`, or alter tracked files.
- **Flags**:
  - `<vX.Y.Z>`: Version string matching `^v[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9.]+)?$`.
  - `--dry-run`: Validates format and preconditions without creating tags.
  - `--skip-verify`: Skips local `bash scripts/verify.sh` check.
  - `--push`: Automatically pushes the tag to `origin` after creating it.
- **Tag Creation**:
  - `git tag -a "$VERSION" -m "Release $VERSION - AI-Native SDLC"`

### 1.2 `.github/workflows/release.yml` Dual-Trigger Contract
- **Triggers**:
  1. `push: tags: ['v*']`
  2. `workflow_dispatch`:
     - input `tag`: Target version tag (default: `v1.1.0`, required)
     - input `target_commit`: Branch or SHA to tag (default: `main`)
- **Execution**:
  - If triggered via `workflow_dispatch` and tag does not exist on remote:
    - Create the tag at `target_commit` and push it, or invoke `gh release create "$TAG_NAME" --target "$TARGET_COMMIT"`.
  - Compile auto-generated notes from git history: `gh release create "$TAG_NAME" --generate-notes`.

### 1.3 `Makefile` Integration
- `make release VERSION=vX.Y.Z`: Runs `bash scripts/release.sh $(VERSION)`.
- `make release-push VERSION=vX.Y.Z`: Runs `bash scripts/release.sh $(VERSION) --push`.
- `make release-remote VERSION=vX.Y.Z`: Dispatches GitHub Action release workflow via `gh workflow run release.yml -f tag=$(VERSION)`.

---

## 2. Acceptance Criteria (Gherkin)

### Scenario 1: Local release tagging on protected `main` branch
- **Given** the developer is on the `main` branch with a clean working tree
- **When** they run `bash scripts/release.sh v1.1.0` or `make release VERSION=v1.1.0`
- **Then** the script validates `v1.1.0` against the semantic version regex
- **And** runs `scripts/verify.sh`
- **And** creates annotated tag `v1.1.0`
- **And** executes zero `git commit` commands, avoiding the branch protection pre-commit hook violation.

### Scenario 2: Tag-triggered GitHub Release workflow
- **Given** a developer pushes a release tag `git push origin v1.1.0`
- **When** GitHub Actions `.github/workflows/release.yml` triggers on the tag push
- **Then** it runs verification
- **And** creates the official GitHub Release with release notes derived directly from git commit history (`--generate-notes`).

### Scenario 3: Command-triggered GitHub Release workflow (`workflow_dispatch`)
- **Given** a developer runs `gh workflow run release.yml -f tag=v1.1.0` or `make release-remote VERSION=v1.1.0`
- **When** GitHub Actions `.github/workflows/release.yml` runs via `workflow_dispatch`
- **Then** it checks out `main`
- **And** verifies health
- **And** publishes the GitHub Release with tag `v1.1.0` and git-derived release notes.
