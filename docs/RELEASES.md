# Release Management & Governance (`docs/RELEASES.md`)

> Operational guide for versioning, cutting, and publishing releases in the **AI-Native Software Development Life Cycle (SDLC)**.

---

## 🏷️ Semantic Versioning Policy

We strictly adhere to [Semantic Versioning 2.0.0](https://semver.org/):
- **MAJOR (`vX.0.0`)**: Incompatible API breaks, architectural restructuring, or major lifecycle protocol changes.
- **MINOR (`v1.X.0`)**: Backwards-compatible features, new agent skills, or new lifecycle stages.
- **PATCH (`v1.0.X`)**: Backwards-compatible bug fixes, security patches, or documentation improvements.

---

## 🚀 The Release Lifecycle

```
        [All Milestones Complete in 00-ROADMAP.md]
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
    [Method A: By Git Tag]      [Method B: By CLI Command]
             │                           │
  [make release VERSION=v1.1.0] [make release-remote VERSION=v1.1.0]
  (Validates & tags without      (Dispatches release.yml with
   direct commits to main)        target version tag)
             │                           │
             ▼                           │
   [git push origin v1.1.0]              │
             │                           │
             └─────────────┬─────────────┘
                           ▼
             [GitHub Actions release.yml]
                           │
                           ├── 1. Runs verify.sh on Ubuntu CI
                           └── 2. Generates notes directly from git history
                                  (gh release create --generate-notes)
```

---

## 📋 Release Workflows

### Method A: Release via Git Tag (Recommended)

1. **Verify Active Milestones**:
   - Check [`docs/plans/00-ROADMAP.md`](plans/00-ROADMAP.md). Ensure all milestones under the target release are marked `COMPLETED` with valid shipped commit hashes (`Shipped: <SHA>`).
2. **Run Local Verification**:
   ```bash
   make verify && make eval
   ```
3. **Cut and Push Release Tag**:
   ```bash
   # Option 1: In one single command
   make release-push VERSION=v1.1.0

   # Option 2: Step-by-step
   make release VERSION=v1.1.0
   git push origin v1.1.0
   ```
   *(Note: Zero `git commit` commands are executed, guaranteeing 100% compliance with `main` branch protection).*

### Method B: Release via CLI Command (Remote Dispatch)

You can trigger a full build and release without creating tags locally:
```bash
# Via Makefile:
make release-remote VERSION=v1.1.0

# Or via GitHub CLI:
gh workflow run release.yml -f tag=v1.1.0
```

GitHub Actions will check out `main`, verify health, create the tag, and publish the release with changelog automatically derived from git commits.

---

## 🔄 Post-Release Actions

1. Update [`docs/plans/00-ROADMAP.md`](plans/00-ROADMAP.md): Move the shipped release to `Previous Releases` and open a new `Active Release` header for the next iteration.
2. Announce release highlights in community channels.
