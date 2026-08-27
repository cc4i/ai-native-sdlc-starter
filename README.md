# AI-Native SDLC Starter Template (Jetski & Antigravity Edition)

> An enterprise-grade, stage-by-stage starter template for the **AI-Native Software Development Life Cycle (SDLC)**, adapted from Anthropic's AI-Native SDLC Playbook and powered by **Google Jetski / Antigravity**.

👉 **New to this repo? Start with the [Team & Developer Onboarding Guide](file:///Users/chuancc/mywork/ai/project-start/ONBOARDING.md).**

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

| Stage | Traditional SDLC | AI-Native SDLC (Jetski / Antigravity) | Primary Artifact |
| :--- | :--- | :--- | :--- |
| **1. Plan** | Requirements gathered across weeks by committee | Originator brainstorms with AI via `/grill-me` into a structured proto-spec | [`intent/NNN-title.md`](file:///Users/chuancc/mywork/ai/project-start/intent) |
| **2. Design** | Analyst specs handed off to designers and architects | Requirements + Architecture compressed into one session with brand, UX & security skills | [`specs/NNN-title.md`](file:///Users/chuancc/mywork/ai/project-start/specs) |
| **3. Build** | Developer starts coding blindly from tickets; tribal knowledge | Plan-first mode (`plan.md`), TDD execution with subagents, shared rules in `GEMINI.md` | [`plans/NNN-title.md`](file:///Users/chuancc/mywork/ai/project-start/plans) + Code |
| **4. Test** | QA testing at release boundaries | Tight inner feedback loop (`make verify`), test-first bug reproduction, continuous CI evals | Test suites + [`evals/`](file:///Users/chuancc/mywork/ai/project-start/evals) |
| **5. Deploy** | Humans manually review every line of agent diffs | 3-Skeptic adversarial review (`implementation-validator`), policy in `REVIEW.md`, human release gate | [`REVIEW.md`](file:///Users/chuancc/mywork/ai/project-start/REVIEW.md) + PR Audit |
| **6. Maintain** | Reactive 3 AM on-call triage and stale postmortems | Observability/metric alert triggers sidecar agent, diagnoses root cause, writes new `intent.md` | `intent/incident-NNN.md` |

---

## 📁 Repository Structure

```
.
├── GEMINI.md                    # Core project context, commands, and rules for Antigravity/Jetski
├── REVIEW.md                    # PR review criteria, severity tiers (Blocker/Important/Nit), governance
├── Makefile                     # Standard developer commands (make verify, make test, make eval, etc.)
├── README.md                    # This documentation guide
├── intent/                      # Stage 1 artifacts: User intent & problem proto-specs
│   ├── README.md
│   └── 001-example-intent.md    # Example intent artifact
├── specs/                       # Stage 2 artifacts: Requirements & Technical design specifications
│   ├── README.md
│   └── 001-example-spec.md      # Example spec artifact (Gherkin format + acceptance criteria)
├── plans/                       # Stage 3 artifacts: Micro-stepped implementation plans & roadmaps
│   ├── 00-ROADMAP.md            # Release milestones and progress tracker
│   ├── README.md
│   └── 001-example-plan.md      # Example plan artifact (TDD order, risk, proof)
├── templates/                   # Standardized markdown templates for all lifecycle stages
│   ├── intent.template.md       # Stage 1 Intent template
│   ├── spec.template.md         # Stage 2 Spec template
│   ├── plan.template.md         # Stage 3 Plan template
│   ├── review.template.md       # Stage 5 PR Review / Audit template
│   └── incident-intent.template.md # Stage 6 Incident -> Intent template
├── .gemini/                     # Antigravity & Jetski customizations
│   ├── skills/                  # Version-controlled institutional knowledge
│   │   ├── intent-capture/      # Skill: Interactive requirements grilling & intent capture
│   │   ├── spec-architect/      # Skill: Gherkin & testable spec synthesis
│   │   ├── secure-api-design/   # Skill: Corporate security & data privacy standard
│   │   ├── verifier-loop/       # Skill: Self-evaluation & verification harness
│   │   └── adversarial-review/  # Skill: 3-skeptic majority gate review
│   └── agents/                  # Swarm subagent definitions
│       ├── product-owner.md     # Requirements elicitation & roadmap management
│       ├── architect.md         # Technical design & micro-stepped planning
│       ├── engineer.md          # Strict TDD execution agent
│       └── auditor.md           # Quality gatekeeper & anti-shortcut checker
├── evals/                       # Stage 4 Continuous AI evaluation suite
│   ├── README.md
│   ├── eval-config.json         # Eval prompt test cases & assertions
│   └── run_evals.py             # Headless evaluation test runner
├── scripts/                     # Local developer & CI tooling
│   ├── verify.sh                # Single-command local feedback verification
│   ├── new-intent.sh            # CLI helper to scaffold a new intent artifact
│   └── check-artifacts.sh       # Linter checking complete intent->spec->plan chain
└── .github/workflows/           # CI/CD automation
    ├── ai-evals.yml             # Runs eval suite on prompt/skill/rule changes
    ├── ai-pr-review.yml         # Automated adversarial review on incoming PRs
    └── artifact-integrity.yml   # Verifies traceability of code diffs to spec/plan
```

---

## 🛠️ Step-by-Step Walkthrough

### 1. Stage 1: Planning (`intent.md`)
* **Goal**: Capture what is wanted, why, and under which constraints in the originator's own words.
* **How to run**:
  1. Use slash command `/grill-me` or invoke the `product-owner` subagent in chat.
  2. Or run `./scripts/new-intent.sh "My Feature Name"`.
  3. Brainstorm with Antigravity until scope, constraints, and success metrics are sharp.
  4. Save to `intent/00X-feature-name.md` and commit to Git.
  5. Product Owner reviews and signs off.

### 2. Stage 2: Design (`spec.md`)
* **Goal**: Expand `intent.md` into an unambiguous, testable technical spec applying corporate skills (security, UX, data privacy).
* **How to run**:
  1. Ask Antigravity: *"Read `intent/00X-feature-name.md` and generate `specs/00X-feature-name.md` using our spec-architect and secure-api-design skills."*
  2. Optional: Run adversarial validation via `spec-validator` subagent to catch ambiguities and untestable requirements before planning.
  3. Product Owner and Tech Lead approve `spec.md`.

### 3. Stage 3: Build (`plan.md` + Code)
* **Goal**: Plan before touching code. Write micro-stepped, test-driven tasks with safety harnesses.
* **How to run**:
  1. Use slash command `/plan` or invoke the `architect` subagent: *"Read `specs/00X-feature-name.md` and create `plans/00X-feature-name.md`."*
  2. Run `plan-validator` to ensure all codebase assumptions and file paths are valid.
  3. Approve the plan.
  4. Dispatch the `engineer` subagent to implement using **Strict TDD** (Red -> Green -> Refactor).
  5. Update checkboxes in `plan.md` as each step is completed.

### 4. Stage 4: Test (Feedback Loop & Continuous Evals)
* **Goal**: Give the agent a deterministic way to verify its own work before a human reviews it.
* **How to run**:
  1. Run `make verify` (or `./scripts/verify.sh`). The agent fixes any lint or test failures automatically.
  2. For bug fixes: write the failing test first, commit it, then instruct the agent to make it pass without modifying the test.
  3. Run continuous evals via `make eval` to verify that prompt and skill modifications do not cause regressions.

### 5. Stage 5: Deploy (Adversarial Review & Human Gate)
* **Goal**: AI conducts multi-perspective review; human code owner makes the release decision.
* **How to run**:
  1. Invoke `auditor` or `implementation-validator` to produce a review report against [`REVIEW.md`](file:///Users/chuancc/mywork/ai/project-start/REVIEW.md).
  2. Address review comments using Antigravity.
  3. Code owner approves PR for deployment.

### 6. Stage 6: Maintain (Closing the Loop)
* **Goal**: Production anomalies and metric breaches automatically generate new intent artifacts.
* **How to run**:
  1. Monitoring/alert webhook triggers a diagnostic agent.
  2. Agent analyzes logs and drafts `intent/incident-NNN.md` using `templates/incident-intent.template.md`.
  3. On-call engineer triages the generated intent into Stage 2 (Design) or dismisses it.

---

## ⚡ Quick Start for New Projects

### Option A: Zero-Clone One-Liner Bootstrap (Fastest)
You do **not** even need to clone this repository. You can bootstrap any new or existing directory directly using the standalone bootstrap script:

```bash
# 1. Run bootstrap in a new or existing project folder:
bash /Users/chuancc/mywork/ai/project-start/bootstrap.sh /path/to/my-new-project --name="My Awesome Service" --stack=python

# 2. Or from a remote URL (when hosted):
# curl -fsSL https://raw.githubusercontent.com/your-org/ai-sdlc-starter/main/bootstrap.sh | bash -s -- /path/to/my-new-project

# 3. Enter your new project:
cd /path/to/my-new-project

# 4. Verify baseline health:
make verify && make eval
```

### Option B: Copying this Template
```bash
cp -r /Users/chuancc/mywork/ai/project-start /path/to/my-new-project
cd /path/to/my-new-project
git init
make verify && make eval
```
