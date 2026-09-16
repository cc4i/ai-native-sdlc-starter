# Spec: DeepSeek Harness (DSH) Native SDLC Support & Local Environment Isolation

**Linked Intent**: [`docs/intent/012-dsh-native-sdlc-support.md`](../intent/012-dsh-native-sdlc-support.md)  
**Author**: DSH Lead Architect  
**Date**: 2026-09-16  
**Status**: Validated  

---

## 1. Overview & Scope

This specification defines the requirements, file interfaces, and behavioral contracts to enable first-class DeepSeek Harness (DSH) multi-agent support and enforce strict project-local environment isolation (UV cache):
- **Project-Local UV Isolation**: Configure `UV_CACHE_DIR` to default inside the workspace (`${ROOT_DIR}/.uv_cache`), ensuring `make verify`, `make test`, and `uv run` commands do not access the user's home directory or global environment.
- **DSH Skills Auto-Discovery**: Structure `.agents/skills/` adhering to the Open Agent standard and DSH's `dsh-skill-filesystem` provider, housing `intent-capture`, `spec-architect`, `secure-api-design`, `adversarial-review`, and `verifier-loop`.
- **DSH Directives & Multi-Agent Guide**: Provide `DSH.md` and update `AGENTS.md`, `README.md`, and `ONBOARDING.md` documenting DSH tools (`subagent`, `workflow`, `ralph`, `todo_write`, `skill`).
- **Bootstrapper Scaffolding**: Ensure `bootstrap.sh` scaffolds `.agents/skills/` and configures local UV caching for newly bootstrapped repositories.

---

## 2. User Stories & Acceptance Criteria (Gherkin Scenarios)

### Story 1: Project-Local UV Cache Isolation
**As a** developer or autonomous AI agent operating under sandboxed file permissions (e.g. `workspace-write`),  
**I want** all `uv` caches and virtual environments to reside strictly inside the project root,  
**So that** verification commands do not access external directories (like `~/.cache/uv`), fail with permission errors, or touch the user's global environment.

#### Scenario 1.1: Local UV cache directory is enforced in verification
```gherkin
Given a project repository configured with uv
When the verification harness "scripts/verify.sh" or "make verify" is executed
Then UV_CACHE_DIR is set to a project-local directory (e.g. "$ROOT_DIR/.uv_cache")
And no files outside the workspace root are created or accessed
And the check completes successfully under workspace-write sandbox mode
```

#### Scenario 1.2: UV cache is excluded from version control
```gherkin
Given the project .gitignore file
When inspecting ignored directory patterns
Then ".uv_cache/" is explicitly ignored
And no cached wheels or source dists are tracked in git
```

---

### Story 2: DSH Native Skill Discovery via Open Standard
**As an** AI agent running inside DeepSeek Harness (DSH),  
**I want** SDLC skills to be discoverable in ".agents/skills/" or ".dsh/skills/",  
**So that** the DSH skill provider automatically surfaces them in the `<available_skills>` session catalog without manual configuration.

#### Scenario 2.1: SDLC skills conform to open agent standard
```gherkin
Given the directory ".agents/skills"
When inspecting each skill directory ("intent-capture", "spec-architect", "secure-api-design", "adversarial-review", "verifier-loop")
Then each skill contains a "SKILL.md" file with valid YAML frontmatter containing "name" and "description"
And the skills are exposed to DSH's native "skill" tool
```

---

### Story 3: DSH Directives and Operational Documentation
**As an** engineering lead adopting this starter template with DSH,  
**I want** comprehensive instructions on how DSH interacts with AGENTS.md, subagents, and workflows,  
**So that** my team can run autonomous SDLC loops using DSH Web GUI or CLI.

#### Scenario 3.1: DSH directives and multi-agent mapping exist
```gherkin
Given the documentation files "DSH.md", "AGENTS.md", "README.md", and "ONBOARDING.md"
When a developer reviews DSH integration
Then DSH-specific tools ("subagent", "workflow", "ralph", "todo_write", "skill") are mapped to the 6 SDLC stages
And the documentation reflects universal multi-agent support
```

---

### Story 4: Standalone Bootstrapper Compatibility
**As a** developer bootstrapping a new project with "bootstrap.sh",  
**I want** the bootstrapper to generate ".agents/skills" and project-local UV settings,  
**So that** the new project is immediately ready for DSH and sandboxed agents out of the box.

#### Scenario 4.1: Bootstrapper generates .agents/skills and isolated uv config
```gherkin
Given a target directory passed to "bash bootstrap.sh <target-dir>"
When bootstrapping completes
Then the target directory contains ".agents/skills" with all 5 core skills
And "scripts/verify.sh" sets UV_CACHE_DIR project-locally
And "make verify" passes cleanly inside the bootstrapped project
```

---

## 3. Architecture & Interface Contracts

### 3.1 Directory Structure & Priority
```
<project-root>/
├── .agents/skills/           # Priority 200: Open Agent & DSH discovery root
│   ├── intent-capture/SKILL.md
│   ├── spec-architect/SKILL.md
│   ├── secure-api-design/SKILL.md
│   ├── adversarial-review/SKILL.md
│   └── verifier-loop/SKILL.md
├── .gemini/skills/           # Priority 100 (Antigravity): Symlinked or mirrored
├── DSH.md                    # DSH Directives & Multi-Agent Workflow mapping
├── AGENTS.md                 # Universal Agent Directives (loaded automatically by DSH)
└── .uv_cache/                # Git-ignored local UV cache
```

### 3.2 Environment Contract in Scripts & Makefile
```bash
# Enforce in scripts/verify.sh, scripts/install-hooks.sh, Makefile:
export UV_CACHE_DIR="${ROOT_DIR}/.uv_cache"
```

---

## 4. Policy, Security & Quality Constraints

- [x] **Zero External Pollution**: Never write to `~/.cache` or user home environment paths.
- [x] **Backward Compatibility**: Gemini Antigravity, Claude Code, Cursor, and Codex workflows remain completely intact.
- [x] **Artifact Integrity**: `scripts/check-artifacts.sh` checks `.agents/skills` or `.gemini/skills`.
- [x] **Zero Lint / Test Failures**: `make verify` must pass with 100% green tests.

---

## 5. Adversarial Review & Sign-Off

- **Spec Gate Verdict**: PASSED by DSH Architectural Review
- **Sign-off**: Approved by @chuancc on 2026-09-16
- **Ready for Stage 3 (Build)**: `docs/plans/012-dsh-native-sdlc-support.md`
