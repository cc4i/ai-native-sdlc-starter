# Team & Developer Onboarding Guide: The AI-Native SDLC

> **Welcome to the AI-Native Software Development Life Cycle (SDLC) Starter Template.**  
> This guide is designed for developers, product managers, architects, and engineering leads who want to bootstrap new projects or adapt existing codebases to the AI-native workflow using **DeepSeek Harness**, **Anthropic Claude Code**, **Google Antigravity**, **OpenAI Codex**, **Cursor**, or **GitHub Copilot**.

---

## 📖 Table of Contents

1. [The AI-Native Philosophy](#1-the-ai-native-philosophy)
2. [5-Minute Quickstart](#2-5-minute-quickstart)
3. [Role-by-Role Practical Workflow](#3-role-by-role-practical-workflow)
   - [Product Managers / Business Originators](#31-product-managers--domain-originators)
   - [Software Architects & Tech Leads](#32-software-architects--tech-leads)
   - [Software Engineers / Builders](#33-software-engineers--builders)
   - [Reviewers & QA Gatekeepers](#34-reviewers--qa-gatekeepers)
   - [SRE & On-Call Engineers](#35-sre--on-call-engineers)
4. [End-to-End Walkthrough: The Dinosaur Runner Case Study](#4-end-to-end-walkthrough-the-dinosaur-runner-case-study)
   - [Action 1: Greenfield MVP Build](#41-action-1-greenfield-mvp-build)
   - [Action 2: New Feature Flow](#42-action-2-new-feature-flow)
   - [Action 3: Strict Bug-Fix Flow](#43-action-3-strict-bug-fix-flow-reproducing-test-first)
   - [Action 4: SRE Anomaly Remediation Flow](#44-action-4-sre-anomaly-remediation-flow-stage-6-maintain)
   - [Action 5: Quality Guardrails & Zero Error Swallowing](#45-action-5-quality-guardrails--zero-error-swallowing)
5. [Prompt Recipes & Slash Command Cheat Sheet](#5-prompt-recipes--slash-command-cheat-sheet)
6. [Governance, Guardrails & The "Two-Strike Rule"](#6-governance-guardrails--the-two-strike-rule)
7. [Repository Anatomy & Traceability Map](#7-repository-anatomy--traceability-map)

---

## 1. The AI-Native Philosophy

### Why Traditional SDLC Fails with AI Coding
In traditional software engineering, **writing code was the most expensive and time-consuming phase**. Elaborate estimation rituals, multi-week PRD workshops, and manual code review queues were built around the assumption of human typing speed.

When AI coding assistants can generate hundreds of lines of code in seconds, **the bottleneck shifts to the stages to the left and right of code generation**:
- 🛑 **Ambiguous intent** (building the wrong thing fast).
- 🛑 **Unvalidated design assumptions** (reworking code after building).
- 🛑 **Overwhelmed review queues** (PRs sitting unreviewed for days).
- 🛑 **Flaky / missing tests** (agents hallucinating passing behavior).

### The Core Paradigm: The Asynchronous Artifact Chain
Instead of passing tickets through slow human handoffs, every phase produces a **version-controlled, human-readable, and machine-actionable Markdown artifact**.

```
  ┌───────────────┐     ┌───────────────┐     ┌───────────────┐     ┌───────────────┐
  │   intent.md   │ ──► │    spec.md    │ ──► │    plan.md    │ ──► │  make verify  │
  └───────────────┘     └───────────────┘     └───────────────┘     └───────────────┘
  (Problem & Scope)     (Gherkin & APIs)      (TDD Micro-steps)     (Zero Regressions)
          ▲                                                                 │
          │                                                                 ▼
  ┌───────────────┐                                                 ┌───────────────┐
  │  incident.md  │ ◄────────────────────────────────────────────── │   REVIEW.md   │
  └───────────────┘                                                 └───────────────┘
  (Closed-Loop SRE)                                                 (Adversarial PR)
```

Human judgment is concentrated at **governance gates** (approving intent, signing off specs, authorizing production deployments) rather than typing syntax.

---

## 2. 5-Minute Quickstart

### Option A: Zero-Clone Bootstrap (Recommended)
You do **not** even need to clone this repository. Run the self-contained `bootstrap.sh` script to set up any new or existing project folder:

```bash
# 1. Run bootstrap (interactive or with flags)
curl -fsSL https://raw.githubusercontent.com/cc4i/ai-native-sdlc-starter/main/bootstrap.sh | bash -s -- /path/to/my-new-project --name="Payment Service" --stack=python

# 2. Enter your project and verify
cd /path/to/my-new-project
make verify && make eval
```

### Option B: Clone this Template
```bash
# 1. Clone into your new project directory
git clone https://github.com/cc4i/ai-native-sdlc-starter.git /path/to/my-new-project
cd /path/to/my-new-project

# 2. Verify health
make verify && make eval
```

---

## 3. Role-by-Role Practical Workflow

### 3.1 Product Managers / Domain Originators
* **Your Goal**: Turn user pain points, feature ideas, and customer requests into clean, structured intent proto-specs.
* **Workflow**:
  1. **Scaffold Intent**: Run `make new-intent TITLE="My Feature Name"` (or `./scripts/new-intent.sh`).
  2. **Brainstorm with Antigravity**: Use the slash command `/grill-me` or invoke the `product-owner` subagent:
     > *"I want to add self-service invoice downloads for billing customers. Grill me on requirements, constraints, security, and edge cases."*
  3. **Refine & Commit**: Antigravity populates [`docs/intent/00X-feature.md`](docs/intent) using [`docs/templates/intent.template.md`](docs/templates/intent.template.md).
  4. **Sign-off**: Review the generated artifact and commit it to git on a feature branch.

---

### 3.2 Software Architects & Tech Leads
* **Your Goal**: Convert approved intent into a robust, secure, testable specification with Gherkin acceptance criteria.
* **Workflow**:
  1. **Generate Spec**: Prompt Antigravity:
     > *"Read `docs/intent/00X-feature.md` and generate `docs/specs/00X-feature.md` using our `spec-architect` and `secure-api-design` skills."*
  2. **Adversarial Spec Validation**: Run the `spec-validator` subagent (3-skeptic panel) to hunt for ambiguities, missing status codes, and security flaws:
     > *"Run spec-validator on `docs/specs/00X-feature.md`. Poke holes in these requirements before we plan."*
  3. **Approve**: Once validated, update status in [`docs/plans/00-ROADMAP.md`](docs/plans/00-ROADMAP.md) to `SPEC_VALIDATED`.

---

### 3.3 Software Engineers / Builders
* **Your Goal**: Plan the implementation, write failing tests first (TDD), and implement code in atomic micro-steps.
* **Workflow**:
  1. **Plan First**: Use slash command `/plan` or the `architect` subagent:
     > *"Read `docs/specs/00X-feature.md` and create `docs/plans/00X-feature.md`. Break work into sequential TDD execution groups."*
  2. **Adversarial Plan Validation**: Run `plan-validator` to ensure all file paths, dependencies, and assumptions match reality.
  3. **Strict TDD Implementation**: Dispatch the `engineer` subagent:
     > *"Implement Execution Group 1 from `docs/plans/00X-feature.md` using strict Test-Driven Development (Red ➔ Green ➔ Refactor)."*
  4. **Continuous Local Proof**: Run `make verify` after each micro-step. **Never modify test assertions to fix a failing test!**

---

### 3.4 Reviewers & QA Gatekeepers
* **Your Goal**: Ensure all pull requests satisfy acceptance criteria, pass security policies, and contain zero anti-shortcuts.
* **Workflow**:
  1. **Automated Local Audit**: Run `make review-pr` locally or invoke the `auditor` / `implementation-validator` subagents:
     > *"Audit this branch against `docs/specs/00X-feature.md` and `REVIEW.md`. Classify findings into Blocker, Important, Nit."*
  2. **PR Comment & Inline Diff Review Automation**: When a PR is opened or updated, `.github/workflows/ai-pr-review.yml` runs `ReviewAgent` automatically:
     - **Tier 1 (Fast Deterministic)**: AST security analyzer and secret scanner execute in `<0.2s`.
     - **Tier 2 (Gemini 3.7 Flash)**: Deep semantic 3-pass review (`Correctness`, `Security`, `Plan Compliance`).
     - **Inline Diff Comments**: Findings inside active diff hunks are published as native GitHub line comments with 1-click ` ```suggestion ` replacement blocks.
     - **Tally & 5-Nit Cap**: Outputs standardized `Important: n, Consider: n, Nit: n` and caps low-severity nits at 5.
  3. **Auto-Fix Loop**: Tag `@agent fix` on PR comments for automated remediation.
  4. **Human Approval**: The designated Code Owner reviews findings, verifies `make verify` and `make eval` are green, and merges the PR.

#### 🔧 One-Time GitHub Configuration for Repository Admins

To enable the autonomous review engine and enforce merge gates on your repository:

##### Option A: Using GitHub CLI (`gh`) (Fastest)
```bash
# Step 1: Add Gemini API key for deep semantic reviews (from https://aistudio.google.com/apikey)
gh secret set GEMINI_API_KEY --body "YOUR_GEMINI_API_KEY"

# Step 2: Grant workflow write access to publish PR review comments
gh api --method PUT /repos/:owner/:repo/actions/permissions/workflow \
  -f default_workflow_permissions=write \
  -F can_approve_pull_request_reviews=true

# Step 3: Require AI Review & Artifact Integrity checks before merging to main
gh api --method PUT /repos/:owner/:repo/branches/main/protection \
  --input - << 'EOF'
{
  "required_status_checks": {
    "strict": false,
    "contexts": [
      "Autonomous AI Code Review & Policy Gate",
      "Verify Unbroken Artifact Chain & Quality Gates"
    ]
  },
  "enforce_admins": false,
  "required_pull_request_reviews": null,
  "restrictions": null
}
EOF
```

##### Option B: Using GitHub Web UI
1. **API Key Secret**: Go to **Settings** ➔ **Secrets and variables** ➔ **Actions** ➔ **New repository secret** ➔ Name: `GEMINI_API_KEY`, Value: `<your-key>`.
2. **Workflow Permissions**: Go to **Settings** ➔ **Actions** ➔ **General** ➔ Under **Workflow permissions**, select **Read and write permissions** and check **"Allow GitHub Actions to create and approve pull requests"**.
3. **Branch Protection**: Go to **Settings** ➔ **Branches** ➔ Edit rule for `main` ➔ Check **"Require status checks to pass before merging"** ➔ Select `Autonomous AI Code Review & Policy Gate` and `Verify Unbroken Artifact Chain & Quality Gates`.

---

### 3.5 SRE & On-Call Engineers
* **Your Goal**: Close the loop by converting production anomalies and metric breaches into actionable intent artifacts automatically.
* **Workflow**:
  1. Statistical control bands in [`bands.yaml`](bands.yaml) continuously monitor metric variance.
  2. Run `python3 scripts/check-control-bands.py` to evaluate metrics.
  3. Critical breaches ($\ge 3\sigma$) automatically draft a new intent artifact: [`docs/intent/incident-NNN.md`](docs/templates/incident-intent.template.md).
  4. On-call engineer triages the incident into Stage 2 (Design) or dismisses it.
  5. When the bug is fixed, a regression test is permanently added to [`evals/eval-config.json`](evals/eval-config.json).

---

## 4. End-to-End Walkthrough: The Dinosaur Runner Case Study

To understand how the AI-Native SDLC operates in practice across real development scenarios, this section walks through the complete lifecycle of building, expanding, fixing, and maintaining an offline **HTML5 Canvas Dinosaur Endless Runner Game** (inspired by Chromium's T-Rex runner).

Every action follows the non-negotiable chain: **Intent ➔ Spec ➔ Plan ➔ TDD (Red/Green/Refactor) ➔ Verification ➔ Review**.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        AI-NATIVE SDLC LIFECYCLE                        │
│ Intent (docs/intent/) ──► Spec (docs/specs/) ──► Plan (docs/plans/)    │
│           ▲                                            │               │
│           │                                            ▼               │
│ Maintain (bands.yaml) ◄── Review (docs/reviews/) ◄── TDD & make verify │
└────────────────────────────────────────────────────────────────────────┘
```

---

### 4.1 Action 1: Greenfield MVP Build (`001: Core MVP`)

* **Objective**: Build a responsive offline 2D canvas runner with jumping, ducking, procedural cacti and pterodactyl obstacles, score progression, and zero external image/audio assets.

#### Stage 1: Capture Intent
1. Scaffold intent:
   ```bash
   make new-intent TITLE="Dinosaur Runner Game"
   ```
2. Conduct the Socratic "Grill Loop" with the agent (using DSH `intent-capture` or Claude `/grill-me`):
   - **Problem**: Users need an offline, ad-free retro arcade runner.
   - **Constraints**: Pure HTML5/Canvas/CSS + Python standard library; zero external CDNs; procedural 8-bit sound synthesis via Web Audio API (`AudioContext`).
3. Output: `docs/intent/001-dinosaur-runner-game.md`. Human Product Owner approves.

#### Stage 2: Technical Specification & Gherkin
1. Dispatch `spec-architect` to convert intent into formal requirements and testable acceptance criteria.
2. Define Gherkin scenarios:
   ```gherkin
   Scenario: Jumping and gravity curve
     Given a dinosaur running on the ground baseline (y = 0)
     When the player presses Space, Up arrow, or taps the screen
     Then a vertical upward impulse is applied (-vy)
     And gravity gradually pulls the dinosaur back to the ground baseline (y = 0)
     And the dinosaur cannot jump again while mid-air

   Scenario: Axis-Aligned Bounding Box (AABB) Collision
     Given a dinosaur at position (x, y) with hitbox D
     And an obstacle at position (ox, oy) with hitbox O
     When D intersects with O
     Then a collision is detected and game state transitions to GAMEOVER
   ```
3. Output: `docs/specs/001-dinosaur-runner-game.md`.

#### Stage 3: Micro-Stepped TDD Plan
1. Dispatch `architect` to design execution groups and safety harness.
2. Record milestone in `docs/plans/00-ROADMAP.md` (`001: Initial Core MVP`).
3. Output: `docs/plans/001-dinosaur-runner-game.md` with 3 sequential groups:
   - Group 1: Core physics & AABB collision engine.
   - Group 2: Canvas renderer, sprites, and Web Audio API synthesizer.
   - Group 3: Built-in Python static server and verification.

#### Stage 4: Strict TDD Implementation
1. **Red**: Write unit tests first in `tests/test_game_engine.py` asserting jump trajectory, gravity clamp, ducking hitbox reduction, and AABB intersection. Run `make test` ➔ **Fails** (`ModuleNotFoundError: No module named 'src'`).
2. **Green**: Implement minimal code in `src/engine/physics.py` satisfying all assertions. Run `make test` ➔ **7/7 tests pass**.
3. **Frontend & Server**: Implement `public/index.html`, `public/game.js`, `public/style.css`, and `src/server.py`.
4. **Single-Command Verification**: Run `make verify` ➔ exits 0 with zero warnings.

---

### 4.2 Action 2: New Feature Flow (`002: Pause & Audio Mute`)

* **Objective**: Add pause/resume controls (<kbd>P</kbd> or HUD button) and audio mute toggles (<kbd>M</kbd> or HUD icon) persisted in `localStorage`.

1. **Scaffold Intent**:
   ```bash
   make new-intent TITLE="Pause and Audio Mute Controls"
   ```
   Author problem statement and constraints in `docs/intent/002-pause-and-audio-mute-controls.md`.
2. **Author Spec**:
   Define `docs/specs/002-pause-and-audio-mute-controls.md` with Gherkin criteria:
   ```gherkin
   Scenario: Pausing freezes game updates
     Given a running game with score S and dinosaur velocity VY
     When the player presses "P" or clicks the pause button
     Then the game transitions to PAUSED state
     And advancing time (dt) does not change score S, dinosaur y, or obstacle positions
   ```
3. **Create Plan**:
   Write `docs/plans/002-pause-and-audio-mute-controls.md` and set Roadmap status to `IN_CONSTRUCTION`.
4. **TDD Build**:
   - **Red**: Add `test_session_pause_freezes_state` and `test_session_mute_toggle` in `tests/test_game_engine.py`. Run test ➔ **Fails** (`ImportError: cannot import name 'GameSession'`).
   - **Green**: Implement `GameSession` in `src/engine/physics.py` and wire `togglePause()` / `toggleMute()` in `public/game.js`. Run test ➔ **9/9 tests pass**.
5. **PR Review & Audit**:
   Run `make review-pr` and save report to `docs/reviews/002-pause-and-audio-mute-controls.md`. Mark plan and roadmap status `COMPLETED`.

---

### 4.3 Action 3: Strict Bug-Fix Flow (Reproducing Test First!)

* **Objective**: Fix a physics state-machine glitch where pressing jump while ducking resulted in a squashed dinosaur flying through mid-air (`is_jumping=True` AND `is_ducking=True`).

> ⚠️ **The Non-Negotiable Bug-Fix Rule**:  
> Always write a reproducing test that fails first. Fix the code to make it pass. **Never modify or weaken test assertions to force a pass.**

1. **Capture Bug Intent**:
   Document root cause in `docs/intent/003-fix-duck-jump-glitch.md`: `jump()` fails to clear `is_ducking`.
2. **Draft Spec**:
   `docs/specs/003-fix-duck-jump-glitch.md` defines state mutual exclusion: `jump()` cancels ducking; airborne ducking initiates fast-drop.
3. **Plan**:
   `docs/plans/003-fix-duck-jump-glitch.md`.
4. **Reproducing Test (Red)**:
   Add reproducing assertion in `tests/test_game_engine.py`:
   ```python
   def test_jumping_cancels_ducking_state(self):
       self.dino.duck(True)
       self.dino.jump()
       self.assertTrue(self.dino.is_jumping)
       self.assertFalse(self.dino.is_ducking, "Dinosaur must not be ducking while jumping")
   ```
   Run `make test` ➔ **FAILS**:
   ```
   AssertionError: True is not false : Dinosaur must not be ducking while jumping
   ```
5. **Fix Implementation (Green)**:
   Update `Dinosaur.jump()` in `src/engine/physics.py` and `public/game.js` to set `self.is_ducking = False`.
   Run `make test` ➔ **PASSED cleanly without touching the test assertion!**
6. **Verification**: Run `make verify` (all 10 tests green). Record review audit in `docs/reviews/003-fix-duck-jump-glitch.md`.

---

### 4.4 Action 4: SRE Anomaly Remediation Flow (Stage 6 Maintain)

* **Objective**: Detect and remediate telemetry breaches using statistical control bands.

1. **Telemetry & Control Bands (`bands.yaml`)**:
   Define metric thresholds:
   ```yaml
   metrics:
     obstacle_min_spacing:
       description: Minimum distance in pixels between consecutive obstacles
       target: 140.0
       lower_threshold_3sigma: 95.0
       action: escalate_to_intent
   ```
2. **Metric Breach Detected (`INC-001`)**:
   At high scroll speeds, random interval generation allowed obstacles to spawn within ~60px of each other (< 95px lower 3σ threshold), creating impossible-to-jump clusters.
3. **Triage & Incident Intent**:
   SRE sidecar files `docs/intent/004-incident-INC-001-obstacle-spacing-clamping.md` from `docs/templates/incident-intent.template.md`.
4. **Spec & Plan**:
   `docs/specs/004-obstacle-spacing-clamping.md` specifies `calculate_min_safe_gap(speed) >= 140.0px`.
5. **TDD Remediation**:
   - Red: Author `test_min_safe_obstacle_spacing` across speed tiers (200 to 680 px/s). Fails.
   - Green: Implement `calculate_min_safe_gap` in `src/engine/physics.py` and clamp in `public/game.js`.
6. **Operational Proof**:
   ```bash
   make check-bands  # Reports: ALL CONTROL BANDS NORMAL
   make verify       # Exits 0 with all checks green
   ```

---

### 4.5 Action 5: Quality Guardrails & Zero Error Swallowing

A critical engineering standard in the AI-Native SDLC is **foolproof verification**:

1. **Zero Error Swallowing (No `|| true`)**:
   Never append `|| true` or `2>/dev/null` to test runners in verification scripts or Makefiles. Any failed assertion or unhandled exception must immediately halt execution with exit code `1`.
2. **Web Asset & JavaScript Syntax Compilation**:
   Python unit tests alone cannot detect frontend runtime errors. All web projects must enforce syntax checking:
   ```bash
   # Validate JavaScript syntax during make verify:
   if command -v node >/dev/null 2>&1; then
       for jsfile in $(find public src -name "*.js" 2>/dev/null); do
           node -c "$jsfile"
       done
   fi
   ```
3. **Automated Server & Asset Integration Tests (`tests/test_web_assets.py`)**:
   Automated tests spin up an ephemeral HTTP server, fetch `GET /` and `GET /game.js`, and verify HTTP 200 responses and valid MIME types.

---

### 4.6 Case Study Summary & Command Matrix

| Scenario | Command to Trigger | Primary Artifact | Verification Gate |
| :--- | :--- | :--- | :--- |
| **New Feature** | `make new-intent TITLE="..."` | `docs/intent/00X-*.md` ➔ `docs/specs/00X-*.md` | `make verify` (Red ➔ Green) |
| **Bug Fix** | Author bug intent & reproducing test | `docs/intent/fix-*.md` + `tests/test_*.py` | Reproducing test fails ➔ code fix ➔ green |
| **SRE Anomaly** | `make check-bands` | `bands.yaml` ➔ `docs/intent/incident-*.md` | Telemetry threshold restored |
| **PR Audit** | `make review-pr` | `docs/reviews/00X-*.md` | ReviewAgent verdict `PASS` |
| **Play Game** | `make run` (in game project) | `http://127.0.0.1:8080/` | Interactive browser canvas |

---

## 5. Prompt Recipes & Slash Command Cheat Sheet

### ⚡ Slash Commands Available in Anthropic Claude Code

| Command | Lifecycle Stage | Action Performed |
| :--- | :--- | :--- |
| **`/grill-me`** | Stage 1: Plan | Socratic requirements interview; synthesizes output into `docs/intent/` |
| **`/spec-architect`** | Stage 2: Design | Transforms approved `intent.md` into Gherkin-compliant `docs/specs/` |
| **`/verify`** | Stage 4: Test | Runs single-command quality verification (`make verify`) |
| **`/review-pr`** | Stage 5: Deploy | Runs autonomous multi-pass code review audit on current branch diff |
| **`/new-intent`** | Stage 1: Plan | Scaffolds a new intent document from standard template |

### 🎯 Slash Commands Available in Google Antigravity

| Command | When to Use | Example |
| :--- | :--- | :--- |
| **`/grill-me`** | In Stage 1 to interrogate requirements & discover hidden constraints | `"/grill-me We want to add OAuth2 login with Google"` |
| **`/plan`** | In Stage 3 before writing any non-trivial code | `"/plan Create TDD execution groups for specs/001-feature.md"` |
| **`/goal`** | For long-running, autonomous multi-step execution | `"/goal Implement all execution groups in plans/001-feature.md until make verify is green"` |
| **`/owl`** | For complex refactoring, multi-perspective strategic analysis & proof | `"/owl Review our data migration plan and find edge cases"` |
| **`/schedule`** | To set one-time reminders or recurring background tasks | `"/schedule @hourly run evals and check test status"` |
| **`/learn`** | When you correct the agent and want to persist the rule in directives | `"/learn Always use Decimal for currency calculations in this repo"` |

### 🤖 OpenAI Codex, Cursor & GitHub Copilot Workflows

- **OpenAI Codex CLI**: Loads system instructions from [`CODEX.md`](CODEX.md) and [`AGENTS.md`](AGENTS.md). Prompt directly: `"Read docs/intent/001-feature.md and implement the plan following strict TDD."`
- **Cursor IDE**: Directives automatically loaded from [`.cursorrules`](.cursorrules) and [`.cursor/rules/sdlc.mdc`](.cursor/rules/sdlc.mdc). Use Composer or Agent mode.
- **GitHub Copilot**: Context loaded from [`.github/copilot-instructions.md`](.github/copilot-instructions.md).

---

### 💡 Golden Prompt Recipes

#### Recipe 1: Stage 1 (Intent Elicitation)
```
Act as the Product Owner. I have an idea: [describe idea in 2 sentences].
Interview me using /grill-me until all edge cases, user personas, success metrics, and constraints are clear.
Then write the result to docs/intent/NNN-[feature-slug].md using docs/templates/intent.template.md.
```

#### Recipe 2: Stage 2 (Spec Generation with Standards)
```
Read docs/intent/NNN-[feature-slug].md.
Apply our `spec-architect` and `secure-api-design` skills to generate docs/specs/NNN-[feature-slug].md.
Include Gherkin acceptance scenarios for happy path, unauthorized access, invalid input, and timeout failure.
Flag any conflicting policies or open architectural questions.
```

#### Recipe 3: Stage 3 (TDD Implementation)
```
Read docs/plans/NNN-[feature-slug].md.
Implement Execution Group [N] following strict Test-Driven Development:
1. Write the failing unit test in tests/unit/ and run it to verify failure.
2. Implement minimum code in src/ to make it pass.
3. Refactor for clarity and run `make verify`.
Update the plan checkboxes as you complete each step.
```

#### Recipe 4: Stage 5 (Adversarial Code Review)
```
Act as the ReviewAgent. Review our current git diff against docs/specs/NNN-[feature-slug].md and REVIEW.md:
`make review-pr`
Classify all findings into:
- 🚨 Blocker (functional defect, security leak, gutted test)
- ⚠️ Important (unhandled edge case, plan deviation)
- 💡 Nit (readability suggestion)
Output the audit report to docs/reviews/NNN-[feature-slug].md.
```

---

## 6. Governance, Guardrails & The "Two-Strike Rule"

To maintain velocity while preserving high code quality, enforce these 4 golden rules:

### 1. The Plan-First Rule
**Never write non-trivial code without an approved `plan.md`.**  
If an agent starts editing code before a plan exists, immediately stop and require a plan first.

### 2. The Test Assertion Integrity Rule
**Never gut, weaken, disable, or skip a failing test.**  
When a test fails, fix the implementation in `src/`, not the test assertion in `tests/`.

### 3. Single-Command Verification Gate
**Every agent session must end with a green `make verify`.**  
A task is never complete until `make verify` exits with code `0` and attaches proof in the summary.

### 4. The Two-Strike Rule for `GEMINI.md`
**When the AI agent makes the same mistake twice, add a concise single-bullet directive to [`GEMINI.md`](GEMINI.md).**  
Keep `GEMINI.md` under one page so that it acts as high-signal working memory rather than bloated context.

---

## 7. Repository Anatomy & Traceability Map

| Directory / File | Lifecycle Stage | Description | Single Source of Truth |
| :--- | :--- | :--- | :--- |
| [`DSH.md`](DSH.md) | Universal | System instructions and multi-agent mapping for DeepSeek Harness | DSH Working Context |
| [`CLAUDE.md`](CLAUDE.md) | Universal | System instructions and commands for Anthropic Claude Code | Claude Code Working Context |
| [`GEMINI.md`](GEMINI.md) | Universal | System instructions and directives for Google Antigravity | Antigravity Working Context |
| [`AGENTS.md`](AGENTS.md) | Universal | Universal cross-agent directives standard | Open Agent Specification |
| [`CODEX.md`](CODEX.md) | Universal | System instructions for OpenAI Codex | Codex Working Context |
| [`.cursorrules`](.cursorrules) | Universal | IDE directives and lifecycle rules for Cursor | Cursor IDE Rules |
| [`.agents/skills/`](.agents/skills) | Knowledge | Open Agent standard skills auto-discovered by DSH | Institutional Memory |
| [`.claude/commands/`](.claude/commands) | Tooling | Custom slash commands for Claude Code (`/grill-me`, `/verify`, etc.) | Claude Workflow Tools |
| [`REVIEW.md`](REVIEW.md) | Stage 5: Deploy | Review policies, severity tiers, approval rules | Code Review Standard |
| [`bands.yaml`](bands.yaml) | Stage 6: Maintain | Statistical control bands configuration ($\sigma$ tiers) | Anomaly Thresholds |
| [`pyproject.toml`](pyproject.toml) | Packaging | PEP 621 metadata, Python >=3.14, `uv` dependency management | Dependency Specification |
| [`docs/architecture/`](docs/architecture) | Architecture | Codebase scaling guide & CodeGraph (`colbymchenry/codegraph`) integration | Scalability Architecture |
| [`docs/RELEASES.md`](docs/RELEASES.md) | Governance | Semantic versioning policy, release checklist, and automation | Release Governance |
| [`docs/intent/`](docs/intent) | Stage 1: Plan | Raw problem statements & originator requirements | Problem Definition |
| [`docs/specs/`](docs/specs) | Stage 2: Design | Gherkin acceptance criteria, API contracts | Functional & Technical Contract |
| [`docs/plans/`](docs/plans) | Stage 3: Build | Micro-stepped TDD execution groups & roadmaps (with Shipped SHAs) | Implementation Strategy |
| [`docs/reviews/`](docs/reviews) | Stage 5: Deploy | PR Review audit reports & sign-offs | Governance Records |
| [`docs/templates/`](docs/templates) | Templates | Standard markdown templates for all lifecycle stages | Artifact Schemas |
| [`src/`](src) | Stage 3: Build | Core application source code & review agent | Production Implementation |
| [`tests/`](tests) | Stage 4: Test | Automated unit, integration, and contract tests | Behavioral Verification |
| [`evals/`](evals) | Stage 4: Test | Continuous AI evaluation regression suite | Agent Instruction Testing |
| [`scripts/`](scripts) | Developer Tooling | `verify.sh`, `new-intent.sh`, `check-artifacts.sh`, `agent_guard.py` | Local Toolchain |
| [`.gemini/skills/`](.gemini/skills) | Knowledge | Versioned enterprise knowledge & policies | Institutional Memory |
| [`.gemini/agents/`](.gemini/agents) | Swarm | Subagent definitions (`product-owner`, `architect`, etc.) | Role Specialization |

---

## 🚀 Ready to Build?

1. Scaffold your first feature: `make new-intent TITLE="My First Feature"`
2. Launch your coding agent of choice:
   - **DeepSeek Harness (DSH)**: Open project in DSH, load `intent-capture` skill to brainstorm!
   - **Claude Code**: Run `claude` and type `/grill-me let's brainstorm this feature!`
   - **Google Antigravity**: Prompt `/grill-me let's brainstorm this feature!`
   - **OpenAI Codex / Cursor**: Ask the agent to review `docs/intent/` and generate the spec following `AGENTS.md`.
3. Happy building in the AI-Native SDLC!
