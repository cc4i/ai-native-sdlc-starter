# Team & Developer Onboarding Guide: The AI-Native SDLC

> **Welcome to the AI-Native Software Development Life Cycle (SDLC) Starter Template.**  
> This guide is designed for developers, product managers, architects, and engineering leads who want to bootstrap new projects or adapt existing codebases to the AI-native workflow using **Google Jetski & Antigravity**.

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
4. [Prompt Recipes & Slash Command Cheat Sheet](#4-prompt-recipes--slash-command-cheat-sheet)
5. [Governance, Guardrails & The "Two-Strike Rule"](#5-governance-guardrails--the-two-strike-rule)
6. [Repository Anatomy & Traceability Map](#6-repository-anatomy--traceability-map)

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
  3. **Refine & Commit**: Antigravity populates [`docs/intent/00X-feature.md`](file:///Users/chuancc/mywork/ai/project-start/docs/intent) using [`docs/templates/intent.template.md`](file:///Users/chuancc/mywork/ai/project-start/docs/templates/intent.template.md).
  4. **Sign-off**: Review the generated artifact and commit it to git on a feature branch.

---

### 3.2 Software Architects & Tech Leads
* **Your Goal**: Convert approved intent into a robust, secure, testable specification with Gherkin acceptance criteria.
* **Workflow**:
  1. **Generate Spec**: Prompt Antigravity:
     > *"Read `docs/intent/00X-feature.md` and generate `docs/specs/00X-feature.md` using our `spec-architect` and `secure-api-design` skills."*
  2. **Adversarial Spec Validation**: Run the `spec-validator` subagent (3-skeptic panel) to hunt for ambiguities, missing status codes, and security flaws:
     > *"Run spec-validator on `docs/specs/00X-feature.md`. Poke holes in these requirements before we plan."*
  3. **Approve**: Once validated, update status in [`docs/plans/00-ROADMAP.md`](file:///Users/chuancc/mywork/ai/project-start/docs/plans/00-ROADMAP.md) to `SPEC_VALIDATED`.

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
  1. Statistical control bands in [`bands.yaml`](file:///Users/chuancc/mywork/ai/project-start/bands.yaml) continuously monitor metric variance.
  2. Run `python3 scripts/check-control-bands.py` to evaluate metrics.
  3. Critical breaches ($\ge 3\sigma$) automatically draft a new intent artifact: [`docs/intent/incident-NNN.md`](file:///Users/chuancc/mywork/ai/project-start/docs/templates/incident-intent.template.md).
  4. On-call engineer triages the incident into Stage 2 (Design) or dismisses it.
  5. When the bug is fixed, a regression test is permanently added to [`evals/eval-config.json`](file:///Users/chuancc/mywork/ai/project-start/evals/eval-config.json).

---

## 4. Prompt Recipes & Slash Command Cheat Sheet

### 🎯 Slash Commands Available in Antigravity

| Command | When to Use | Example |
| :--- | :--- | :--- |
| **`/grill-me`** | In Stage 1 to interrogate requirements & discover hidden constraints | `"/grill-me We want to add OAuth2 login with Google"` |
| **`/plan`** | In Stage 3 before writing any non-trivial code | `"/plan Create TDD execution groups for specs/001-feature.md"` |
| **`/goal`** | For long-running, autonomous multi-step execution | `"/goal Implement all execution groups in plans/001-feature.md until make verify is green"` |
| **`/owl`** | For complex refactoring, multi-perspective strategic analysis & proof | `"/owl Review our data migration plan and find edge cases"` |
| **`/schedule`** | To set one-time reminders or recurring background tasks | `"/schedule @hourly run evals and check test status"` |
| **`/learn`** | When you correct the agent and want to persist the rule in `GEMINI.md` | `"/learn Always use Decimal for currency calculations in this repo"` |

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

## 5. Governance, Guardrails & The "Two-Strike Rule"

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
**When the AI agent makes the same mistake twice, add a concise single-bullet directive to [`GEMINI.md`](file:///Users/chuancc/mywork/ai/project-start/GEMINI.md).**  
Keep `GEMINI.md` under one page so that it acts as high-signal working memory rather than bloated context.

---

## 6. Repository Anatomy & Traceability Map

| Directory / File | Lifecycle Stage | Description | Single Source of Truth |
| :--- | :--- | :--- | :--- |
| [`GEMINI.md`](file:///Users/chuancc/mywork/ai/project-start/GEMINI.md) | Universal | Core agent directives, conventions, commands | Agent Working Context |
| [`REVIEW.md`](file:///Users/chuancc/mywork/ai/project-start/REVIEW.md) | Stage 5: Deploy | Review policies, severity tiers, approval rules | Code Review Standard |
| [`bands.yaml`](file:///Users/chuancc/mywork/ai/project-start/bands.yaml) | Stage 6: Maintain | Statistical control bands configuration ($\sigma$ tiers) | Anomaly Thresholds |
| [`hooks.json`](file:///Users/chuancc/mywork/ai/project-start/hooks.json) | Governance | Jetski lifecycle hooks (`PreToolUse`, `Stop`) | Agent Tool Guardrails |
| [`docs/intent/`](file:///Users/chuancc/mywork/ai/project-start/docs/intent) | Stage 1: Plan | Raw problem statements & originator requirements | Problem Definition |
| [`docs/specs/`](file:///Users/chuancc/mywork/ai/project-start/docs/specs) | Stage 2: Design | Gherkin acceptance criteria, API contracts | Functional & Technical Contract |
| [`docs/plans/`](file:///Users/chuancc/mywork/ai/project-start/docs/plans) | Stage 3: Build | Micro-stepped TDD execution groups & roadmaps (with Shipped SHAs) | Implementation Strategy |
| [`docs/reviews/`](file:///Users/chuancc/mywork/ai/project-start/docs/reviews) | Stage 5: Deploy | PR Review audit reports & sign-offs | Governance Records |
| [`docs/templates/`](file:///Users/chuancc/mywork/ai/project-start/docs/templates) | Templates | Standard markdown templates for all lifecycle stages | Artifact Schemas |
| [`src/`](file:///Users/chuancc/mywork/ai/project-start/src) | Stage 3: Build | Core application source code & review agent | Production Implementation |
| [`tests/`](file:///Users/chuancc/mywork/ai/project-start/tests) | Stage 4: Test | Automated unit, integration, and contract tests (33 tests) | Behavioral Verification |
| [`evals/`](file:///Users/chuancc/mywork/ai/project-start/evals) | Stage 4: Test | Continuous AI evaluation regression suite | Agent Instruction Testing |
| [`scripts/`](file:///Users/chuancc/mywork/ai/project-start/scripts) | Developer Tooling | `verify.sh`, `new-intent.sh`, `check-artifacts.sh`, `jetski_guard.py` | Local Toolchain |
| [`.gemini/skills/`](file:///Users/chuancc/mywork/ai/project-start/.gemini/skills) | Knowledge | Versioned enterprise knowledge & policies | Institutional Memory |
| [`.gemini/agents/`](file:///Users/chuancc/mywork/ai/project-start/.gemini/agents) | Swarm | Subagent definitions (`product-owner`, `architect`, etc.) | Role Specialization |

---

## 🚀 Ready to Build?

1. Scaffold your first feature: `make new-intent TITLE="My First Feature"`
2. Tell Antigravity: `"/grill-me let's brainstorm this feature!"`
3. Happy building in the AI-Native SDLC!
