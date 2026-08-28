# AI-Native SDLC Starter Template (Antigravity Edition)

[![CI Build](https://github.com/cc4i/ai-native-sdlc-starter/actions/workflows/ai-evals.yml/badge.svg)](https://github.com/cc4i/ai-native-sdlc-starter/actions)
[![Python 3.14+](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![Packaging: uv](https://img.shields.io/badge/packaging-uv-purple.svg)](https://github.com/astral-sh/uv)
[![CodeGraph Integrated](https://img.shields.io/badge/codegraph-integrated-orange.svg)](https://github.com/colbymchenry/codegraph)
[![SDLC: AI-Native](https://img.shields.io/badge/SDLC-AI--Native-brightgreen.svg)](#-the-6-stages-at-a-glance)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> An enterprise-grade, stage-by-stage starter template for the **AI-Native Software Development Life Cycle (SDLC)**, adapted from Anthropic's AI-Native SDLC Playbook and powered by **Google Antigravity**.

👉 **New to this repo? Start with the [Team & Developer Onboarding Guide](ONBOARDING.md).**

---

## 🚀 Overview

In the AI-native era, **writing code is no longer the bottleneck**. When coding speeds accelerate by 10x–100x, traditional handoffs (PRD committee reviews, estimation meetings, manual ticket routing, synchronous code review queues) become the primary constraints.

The **AI-Native SDLC** transforms software engineering from a slow, linear waterfall/scrum process into a **fast, continuous, artifact-driven loop**. 

Every stage produces a version-controlled, human-readable, and machine-actionable Markdown artifact that triggers the next stage. Human judgment is concentrated at strategic **review and governance gates**, while AI handles synthesis, planning, implementation, verification, and diagnosis.

```
                   ┌──────────────────────────────────────────────────────────┐
                   │                                                          │
                   ▼                                                          │
        ┌─────────────────────┐                                               │
        │   01. PLAN STAGE    │                                               │
        │ Capture `intent.md` │ ───► Human Approval / PO Gate                 │
        └──────────┬──────────┘                                               │
                   │                                                          │
                   ▼                                                          │
        ┌─────────────────────┐                                               │
        │   02. DESIGN STAGE  │                                               │
        │ Produce `spec.md`   │ ───► 3-Skeptic Spec Gate (spec-validator)     │
        └──────────┬──────────┘                                               │
                   │                                                          │
                   ▼                                                          │
        ┌─────────────────────┐                                               │
        │   03. BUILD STAGE   │                                               │
        │ Micro-step `plan.md`│ ───► Plan Gate (plan-validator)               │
        │ TDD Code & Harness  │                                               │
        └──────────┬──────────┘                                               │
                   │                                                          │
                   ▼                                                          │
        ┌─────────────────────┐                                               │
        │   04. TEST STAGE    │                                               │
        │ Inner Feedback Loop │ ───► Auto-Verification (make verify)          │
        │ Continuous Evals    │ ───► CI Regression Gates                      │
        └──────────┬──────────┘                                               │
                   │                                                          │
                   ▼                                                          │
        ┌─────────────────────┐                                               │
        │  05. DEPLOY STAGE   │                                               │
        │ Bidirectional Review│ ───► Implementation Validator Gate            │
        │ Scoped Tool Release │ ───► Human Code Owner Merge Gate              │
        └──────────┬──────────┘                                               │
                   │                                                          │
                   ▼                                                          │
        ┌─────────────────────┐                                               │
        │  06. MAINTAIN STAGE │                                               │
        │ Metric Breach Alert │ ───► Auto-Diagnose Anomaly                    │
        └──────────┬──────────┘                                               │
                   │                                                          │
                   └──────────────────────────────────────────────────────────┘
```

---

## 🔄 The 6 Stages at a Glance

| Stage | Traditional SDLC | AI-Native SDLC (Antigravity) | Primary Artifact |
| :--- | :--- | :--- | :--- |
| **1. Plan** | Requirements gathered across weeks by committee | Originator brainstorms with AI via `/grill-me` into a structured proto-spec | [`docs/intent/NNN-title.md`](docs/intent) |
| **2. Design** | Analyst specs handed off to designers and architects | Requirements + Architecture compressed into one session with brand, UX & security skills | [`docs/specs/NNN-title.md`](docs/specs) |
| **3. Build** | Developer starts coding blindly from tickets; tribal knowledge | Plan-first mode (`plan.md`), TDD execution with subagents, shared rules in `GEMINI.md` | [`docs/plans/NNN-title.md`](docs/plans) + Code |
| **4. Test** | QA testing at release boundaries | Tight inner feedback loop (`make verify`), test-first bug reproduction, continuous CI evals | Test suites + [`evals/`](evals) |
| **5. Deploy** | Humans manually review every line of agent diffs | Automated PR review in CI (`make review-pr`), policy in `REVIEW.md`, human release gate | [`REVIEW.md`](REVIEW.md) + [`docs/reviews/`](docs/reviews) |
| **6. Maintain** | Reactive 3 AM on-call triage and stale postmortems | Statistical control bands (`bands.yaml`), metric anomaly detector triggers Stage 1 intent | [`bands.yaml`](bands.yaml) + `docs/intent/incident-NNN.md` |

---

## 📚 Architecture & Documentation Links

Detailed operational guides, scalability patterns, and complete file anatomy:

- 📖 **[Developer & Team Onboarding Guide](ONBOARDING.md)**: Role-by-role practical workflows, prompt recipes, and complete repository anatomy.
- 🧠 **[Codebase Intelligence & Scalability Guide](docs/architecture/SCALING_AND_CODEGRAPH.md)**: Integrating CodeGraph (`colbymchenry/codegraph`) to eliminate context bloat on large codebases.
- 🚀 **[Release Management & Governance](docs/RELEASES.md)**: Semantic versioning, verification checklists, and release automation.
- 🛡️ **[Code Review Policy (REVIEW.md)](REVIEW.md)**: PR review severity ladder (Blocker/Important/Nit) and human governance rules.

---

## 🛠️ Step-by-Step Walkthrough

### 1. Stage 1: Planning (`intent.md`)
* **Goal**: Capture what is wanted, why, and under which constraints in the originator's own words.
* **How to run**:
  1. Use slash command `/grill-me` or invoke the `product-owner` subagent in chat.
  2. Or run `make new-intent TITLE="My Feature Name"` (or `./scripts/new-intent.sh`).
  3. Brainstorm with Antigravity until scope, constraints, and success metrics are sharp.
  4. Save to `docs/intent/00X-feature-name.md` and commit to Git on a feature branch.
  5. Product Owner reviews and signs off.

### 2. Stage 2: Design (`spec.md`)
* **Goal**: Expand `intent.md` into an unambiguous, testable technical spec with Gherkin acceptance criteria.
* **How to run**:
  1. Ask Antigravity: *"Read `docs/intent/00X-feature-name.md` and generate `docs/specs/00X-feature-name.md` using our spec-architect and secure-api-design skills."*
  2. Optional: Run adversarial validation via `spec-validator` subagent to catch ambiguities and untestable requirements before planning.
  3. Product Owner and Tech Lead approve `spec.md`.

### 3. Stage 3: Build (`plan.md` + Code)
* **Goal**: Plan before touching code. Write micro-stepped, test-driven tasks with safety harnesses.
* **How to run**:
  1. Use slash command `/plan` or invoke the `architect` subagent: *"Read `docs/specs/00X-feature-name.md` and create `docs/plans/00X-feature-name.md`."*
  2. Run `plan-validator` to ensure all codebase assumptions and file paths are valid.
  3. Approve the plan and update `docs/plans/00-ROADMAP.md`.
  4. Dispatch the `engineer` subagent to implement using **Strict TDD** (Red -> Green -> Refactor).
  5. Update checkboxes in `docs/plans/00X-feature-name.md` as each step is completed.

### 4. Stage 4: Test (Feedback Loop & Continuous Evals)
* **Goal**: Give the agent a deterministic way to verify its own work before a human reviews it.
* **How to run**:
  1. Run `make verify` (or `./scripts/verify.sh`). The agent fixes any lint or test failures automatically (33 tests pass in <0.3s).
  2. For bug fixes: write the failing test first, commit it, then instruct the agent to make it pass without modifying the test.
  3. Run continuous evals via `make eval` to verify that prompt and skill modifications do not cause regressions.

### 5. Stage 5: Deploy (Automated PR Review & Merge Gate)
* **Goal**: Multi-perspective AI code review on PR diffs; human code owner makes the release decision.
* **How to run**:
  1. Run local review on branch diff: `make review-pr` (or `python3 -m src.cli review-pr --base origin/main`).
  2. Save persistent report to `docs/reviews/00X-feature-name.md`.
  3. Open a Pull Request (`gh pr create`). GitHub Actions automatically runs `ReviewAgent` (Tier 1 deterministic + Tier 2 Gemini 3.7 Flash) and posts inline diff comments with 1-click suggestions.
  4. Code owner approves and merges the Pull Request.
  5. Record the merge commit hash in the plan: `Shipped: <COMMIT_SHA>`.

> [!TIP]
> **One-Time GitHub Configuration for Autonomous PR Reviews**:
> ```bash
> # 1. Set Gemini API key for deep semantic reviews (optional but recommended):
> gh secret set GEMINI_API_KEY --body "YOUR_GEMINI_API_KEY"
>
> # 2. Ensure GitHub Actions has write access to PRs:
> gh api --method PUT /repos/:owner/:repo/actions/permissions/workflow \
>   -f default_workflow_permissions=write -F can_approve_pull_request_reviews=true
>
> # 3. Enforce AI Review & Artifact Integrity status checks before merging:
> gh api --method PUT /repos/:owner/:repo/branches/main/protection \
>   --input - << 'EOF'
> {"required_status_checks":{"strict":false,"contexts":["Autonomous AI Code Review & Policy Gate","Verify Unbroken Artifact Chain & Quality Gates"]},"enforce_admins":false,"required_pull_request_reviews":null,"restrictions":null}
> EOF
> ```

### 6. Stage 6: Maintain (Closing the Loop)
* **Goal**: Production anomalies and metric breaches automatically generate new intent artifacts.
* **How to run**:
  1. Statistical control bands in `bands.yaml` monitor rolling baselines ($\sigma$ deviations).
  2. Run `python3 scripts/check-control-bands.py` to evaluate metrics.
  3. Tier 3 critical breaches ($\ge 3.0\sigma$) automatically draft a new Stage 1 intent (`docs/intent/incident-NNN.md`) using `docs/templates/incident-intent.template.md`.
  4. On-call engineer triages the generated intent into Stage 2 (Design) or dismisses it.

---

## ⚡ Quick Start for New Projects

### Option A: Zero-Clone One-Liner Bootstrap (Fastest)
You do **not** even need to clone this repository. You can bootstrap any new or existing directory directly using the standalone bootstrap script:

```bash
# 1. Run bootstrap in a new or existing project folder:
curl -fsSL https://raw.githubusercontent.com/cc4i/ai-native-sdlc-starter/main/bootstrap.sh | bash -s -- /path/to/my-new-project --name="My Awesome Service" --stack=python

# 2. Enter your new project:
cd /path/to/my-new-project

# 3. Verify baseline health:
make verify && make eval
```

### Option B: Cloning this Template
```bash
git clone https://github.com/cc4i/ai-native-sdlc-starter.git my-new-project
cd my-new-project
make verify && make eval
```
