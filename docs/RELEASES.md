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
                   ▼
       [Run Local make verify]
                   │
                   ▼
  [Execute make release VERSION=vX.Y.Z]
                   │
                   ├── 1. Validates clean working tree
                   ├── 2. Runs verify.sh & check-artifacts.sh
                   ├── 3. Updates pyproject.toml version
                   └── 4. Creates annotated git tag vX.Y.Z
                   │
                   ▼
        [git push origin vX.Y.Z]
                   │
                   ▼
   [GitHub Actions .github/workflows/release.yml]
                   │
                   └── Publishes GitHub Release with auto-generated notes
```

---

## 📋 Release Checklist

Before cutting a release:

1. **Verify Active Milestones**:
   - Check [`docs/plans/00-ROADMAP.md`](plans/00-ROADMAP.md). Ensure all milestones under the target release are marked `COMPLETED` with valid shipped commit hashes (`Shipped: <SHA>`).
2. **Run Local Verification**:
   ```bash
   make verify && make eval
   ```
   Both must pass with zero warnings or errors.
3. **Cut the Release**:
   ```bash
   make release VERSION=v1.1.0
   ```
   *(Use `--dry-run` to validate version syntax beforehand: `bash scripts/release.sh v1.1.0 --dry-run`)*
4. **Publish to GitHub**:
   ```bash
   git push origin v1.1.0
   ```
   This triggers `.github/workflows/release.yml` which automatically compiles release notes and publishes the release on GitHub.

---

## 🔄 Post-Release Actions

1. Update [`docs/plans/00-ROADMAP.md`](plans/00-ROADMAP.md): Move the shipped release to `Previous Releases` and open a new `Active Release` header for the next iteration.
2. Announce release highlights in community channels.
