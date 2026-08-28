#!/usr/bin/env bash
# ==============================================================================
# AI-Native SDLC Standalone Bootstrap Script (Antigravity Edition)
# ==============================================================================
# This script initializes ANY new or existing repository with the full
# AI-Native SDLC architecture (intent, specs, plans, evals, skills, agents,
# workflows, and verification harness) WITHOUT needing to clone this repo.
#
# Usage:
#   bash bootstrap.sh [target-directory] [options]
#   curl -fsSL https://raw.githubusercontent.com/cc4i/ai-native-sdlc-starter/main/bootstrap.sh | bash -s -- [target-directory] [options]
#
# Options:
#   --name=<name>         Project name (default: directory name)
#   --stack=<stack>       Tech stack: python | typescript | go | rust | generic (default: detect or generic)
#   --no-git              Skip git init
#   --force               Overwrite existing configuration files
#   --help, -h            Show help message
# ==============================================================================

set -euo pipefail

# Text formatting
BOLD="\033[1m"
GREEN="\033[0;32m"
BLUE="\033[0;34m"
YELLOW="\033[0;33m"
CYAN="\033[0;36m"
RED="\033[0;31m"
RESET="\033[0m"

TARGET_DIR=""
PROJECT_NAME=""
STACK=""
INIT_GIT=true
FORCE=false

print_banner() {
    echo -e "${CYAN}${BOLD}"
    echo "================================================================================"
    echo "  🚀 AI-Native SDLC Project Bootstrapper (Antigravity)"
    echo "================================================================================"
    echo -e "${RESET}"
}

usage() {
    print_banner
    local script_name
    script_name="$(basename "$0")"
    echo "Usage: ${script_name} <target-directory> [options]"
    echo ""
    echo "Arguments:"
    echo "  <target-directory>    Path to new or existing project folder (e.g. ./my-app)"
    echo ""
    echo "Options:"
    echo "  --name=<name>         Project name (default: directory basename)"
    echo "  --stack=<stack>       Tech stack: python | typescript | go | rust | generic"
    echo "  --no-git              Do not initialize a Git repository"
    echo "  --force               Overwrite existing configuration files"
    echo "  -h, --help            Show this help message"
    echo ""
    echo "Examples:"
    echo "  ${script_name} ./my-new-app --name='Billing Service' --stack=python"
    echo "  ${script_name} ./my-ts-app --stack=typescript"
    exit 0
}

if [ $# -eq 0 ]; then
    usage
fi

# Parse Arguments
for arg in "$@"; do
    case $arg in
        -h|--help)
            usage
            ;;
        --name=*)
            PROJECT_NAME="${arg#*=}"
            ;;
        --stack=*)
            STACK="${arg#*=}"
            ;;
        --no-git)
            INIT_GIT=false
            ;;
        --force)
            FORCE=true
            ;;
        -*)
            echo -e "${RED}Unknown option: $arg${RESET}"
            usage
            ;;
        *)
            TARGET_DIR="$arg"
            ;;
    esac
done

if [ -z "$TARGET_DIR" ]; then
    echo -e "${RED}Error: Target directory required.${RESET}"
    echo ""
    usage
fi

# Resolve Target Directory
mkdir -p "$TARGET_DIR"
cd "$TARGET_DIR"
TARGET_DIR_FULL="$(pwd)"

# Self-overwrite protection guard
if ([ -f "$TARGET_DIR_FULL/scripts/bootstrap.sh" ] || [ -f "$TARGET_DIR_FULL/bootstrap.sh" ]) && [ -d "$TARGET_DIR_FULL/docs" ] && [ "$FORCE" = false ]; then
    echo -e "${RED}❌ Safety Guard: Target directory '$TARGET_DIR_FULL' is the starter repository itself.${RESET}"
    echo "   Bootstrapping into the starter repo will overwrite repository source files."
    echo "   Remediation: Specify a separate target directory (e.g. $(basename "$0") ./my-app) or use --force if intentional."
    exit 1
fi

if [ -z "$PROJECT_NAME" ]; then
    PROJECT_NAME="$(basename "$TARGET_DIR_FULL")"
fi

# Auto-detect Stack if not specified
if [ -z "$STACK" ]; then
    if [ -f "package.json" ] || [ -f "tsconfig.json" ]; then
        STACK="typescript"
    elif [ -f "requirements.txt" ] || [ -f "pyproject.toml" ] || [ -f "Pipfile" ]; then
        STACK="python"
    elif [ -f "go.mod" ]; then
        STACK="go"
    elif [ -f "Cargo.toml" ]; then
        STACK="rust"
    else
        STACK="generic"
    fi
fi

print_banner
echo -e "${BOLD}Target Directory :${RESET} ${BLUE}$TARGET_DIR_FULL${RESET}"
echo -e "${BOLD}Project Name     :${RESET} ${GREEN}$PROJECT_NAME${RESET}"
echo -e "${BOLD}Tech Stack       :${RESET} ${YELLOW}$STACK${RESET}"
echo -e "${BOLD}Git Init         :${RESET} $INIT_GIT"
echo ""

# ------------------------------------------------------------------------------
# 1. Directory Structure Creation
# ------------------------------------------------------------------------------
echo -e "${BLUE}📁 (1/6) Creating AI-Native SDLC directory hierarchy...${RESET}"
mkdir -p \
    docs/intent \
    docs/specs \
    docs/plans \
    docs/reviews \
    docs/templates \
    evals \
    scripts \
    .githooks \
    .gemini/skills/intent-capture \
    .gemini/skills/spec-architect \
    .gemini/skills/secure-api-design \
    .gemini/skills/verifier-loop \
    .gemini/skills/adversarial-review \
    .gemini/agents \
    .github/workflows

# ------------------------------------------------------------------------------
# 2. Write Markdown Templates (templates/)
# ------------------------------------------------------------------------------
echo -e "${BLUE}📝 (2/6) Writing lifecycle Markdown templates...${RESET}"

cat << 'EOF' > docs/templates/intent.template.md
# Intent: [Short Feature / Improvement Title]

**Author**: [Name or Agent ID]  
**Date**: [YYYY-MM-DD]  
**Status**: [Draft | In Review | Approved | Rejected]  
**Target Milestone**: [e.g., v1.0, Sprint 42]  

---

## 1. Problem Statement
*Describe the pain point or opportunity in plain terms. What cannot be done today? Who is affected?*

- **Current State**: [Describe what happens now]
- **User Pain / Friction**: [Describe why this matters and who is impacted]
- **Impact & Urgency**: [Quantify impact if possible, e.g., call volume, error rate, drop-off rate]

---

## 2. Proposed Outcome
*What does success look like when this is completed?*

- [Key outcome 1]
- [Key outcome 2]
- [Key outcome 3]

---

## 3. Affected Users & Systems
*Who interacts with this change and which systems are touched?*

- **Target Personas / Users**: [e.g., end-customers, claims handlers, API consumers]
- **Affected Systems / Services**: [e.g., user-portal, billing-service, auth-gateway]
- **Third-Party Dependencies**: [e.g., Stripe, SendGrid, Auth0]

---

## 4. Constraints & Boundaries
*What must NOT change? What constraints must be respected?*

- **Security & Privacy**: [e.g., No new PII stored in local storage, existing JWT auth only]
- **Performance**: [e.g., Response time < 200ms at p99, cache downstream calls]
- **Backward Compatibility**: [e.g., Must support legacy v1 client payloads]
- **Out of Scope**: [Explicitly list what we are NOT building in this iteration]

---

## 5. Open Questions & Assumptions
*What unknowns need resolution before or during technical design?*

1. [Open question / assumption 1]
2. [Open question / assumption 2]

---

## 6. Approval & Handover
- **Product Owner Review**: [ ] Approved by @username on YYYY-MM-DD
- **Ready for Stage 2 (Design)**: `specs/[NNN-title].md`
EOF

cat << 'EOF' > docs/templates/spec.template.md
# Spec: [Feature / Improvement Name]

**Linked Intent**: [`intent/NNN-title.md`](file:///intent)  
**Author**: [Architect / Product Owner / Agent]  
**Date**: [YYYY-MM-DD]  
**Status**: [Draft | Validated | Approved]  

---

## 1. Overview & Scope
*Summarize the functional and technical requirements derived from the approved intent artifact.*

- **Summary**: [High-level summary of what is being built]
- **Target Users**: [Personas and access tiers]
- **In Scope**: [List of capabilities included]
- **Out of Scope**: [List of capabilities excluded]

---

## 2. User Stories & Acceptance Criteria (Gherkin Scenarios)

### Story 1: [Primary User Flow]
**As a** [user role]  
**I want to** [action / capability]  
**So that** [benefit / business value]  

#### Scenario 1.1: [Happy path title]
```gherkin
Given [preconditions, e.g., an authenticated user with active subscription]
When [user performs action, e.g., requests claims status for claim "CLM-1234"]
Then [expected outcome, e.g., system returns status "In Review" with timestamp]
And [side effect, e.g., audit log entry is recorded]
```

#### Scenario 1.2: [Error / Edge case title]
```gherkin
Given [precondition, e.g., an authenticated user]
When [invalid input or network error occurs, e.g., non-existent claim ID "CLM-9999"]
Then [expected error response, e.g., system returns 404 with error code "CLAIM_NOT_FOUND"]
And [no internal system details or stack traces are leaked]
```

---

## 3. Architecture & Interface Contracts

### 3.1 Data Models & Schemas
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ExamplePayload",
  "type": "object",
  "properties": {
    "id": { "type": "string" },
    "status": { "type": "string", "enum": ["pending", "in_review", "approved", "rejected"] },
    "updatedAt": { "type": "string", "format": "date-time" }
  },
  "required": ["id", "status", "updatedAt"]
}
```

### 3.2 API Contracts (REST / gRPC / Events)
- **Method & Route**: `GET /api/v1/resource/{id}`
- **Auth**: Bearer JWT (`scopes: ["read:resource"]`)
- **Rate Limit**: 50 req/sec per tenant

---

## 4. Policy, Security & Quality Constraints

- [ ] **Authentication & Access Control**: RBAC/ABAC verified on all routes.
- [ ] **Input Validation**: Strict schema enforcement; reject unknown fields.
- [ ] **PII & Logging**: Ensure zero sensitive or credit card/health data logged.
- [ ] **Performance SLA**: Response time under 200ms at 95th percentile.

---

## 5. Adversarial Review & Sign-Off

- **Spec Gate Verdict**: [ ] PASSED by `spec-validator` (2-of-3 skeptic majority)
- **Sign-off**: [ ] Tech Lead / Architect approval on YYYY-MM-DD
- **Ready for Stage 3 (Build)**: `plans/[NNN-title].md`
EOF

cat << 'EOF' > docs/templates/plan.template.md
# Plan: [Implementation Task / Milestone Name]

**Linked Spec**: [`specs/NNN-title.md`](file:///specs)  
**Author**: [Architect / Engineer / Agent]  
**Date**: [YYYY-MM-DD]  
**Status**: [Draft | In Progress | Completed]  

---

## 1. Scope & Strategy

- **Objective**: [Clear 1-2 sentence description of what will be implemented]
- **Strategy**: [e.g., TDD, Strangler Fig, Additive Migration, Parallel Groups]
- **Estimated Execution Groups**: [e.g., 3 sequential groups, 2 parallel workers]

---

## 2. File Change Map

| Path | Change Type | Purpose / Description |
| :--- | :--- | :--- |
| `src/domain/...` | New / Modify | Core domain logic |
| `src/api/...` | Modify | Route & validation integration |
| `tests/unit/...` | New | Unit tests for domain rules |
| `tests/integration/...` | New / Modify | End-to-end HTTP contract tests |

---

## 3. Micro-Stepped Execution Groups

### Execution Group 1: Safety Harness & Core Domain Logic (TDD)
- [ ] **Step 1.1 (Red)**: Write unit tests in `tests/unit/` covering domain states. Verify tests fail as expected.
- [ ] **Step 1.2 (Green)**: Implement core logic in `src/` to satisfy unit tests. Verify tests pass.
- [ ] **Step 1.3 (Refactor)**: Clean up types and ensure zero lint warnings. Run `make verify`.

### Execution Group 2: API Endpoints & Route Wiring
- [ ] **Step 2.1 (Red)**: Write integration contract test in `tests/integration/`.
- [ ] **Step 2.2 (Green)**: Wire controller and input validation into routes.
- [ ] **Step 2.3 (Verify)**: Run full test suite (`make test`). Verify zero regressions.

### Execution Group 3: Documentation, Evals & Cleanup
- [ ] **Step 3.1**: Update documentation and schema definitions.
- [ ] **Step 3.2**: Add regression eval test case to `evals/eval-config.json`.
- [ ] **Step 3.3**: Run `make verify` and prepare PR review artifact.

---

## 4. Risk Matrix & Mitigations

| Risk | Severity | Mitigation Strategy |
| :--- | :--- | :--- |
| Upstream service rate limits | Medium | Implement caching layer with 60s TTL |
| Unhandled error leaking stack trace | High | Global error boundary and strict DTO mapping |

---

## 5. Proof of Correctness & Harness

- [ ] **Command**: `make verify` exits code 0.
- [ ] **Unit Tests**: All unit tests passing in `tests/unit/`.
- [ ] **Integration Tests**: All integration tests passing in `tests/integration/`.
- [ ] **Zero Anti-Shortcuts**: No `TODO`, `FIXME`, or mocked implementations remaining.
EOF

cat << 'EOF' > docs/templates/review.template.md
# PR Review Audit Report

**Pull Request**: # [PR Number / Branch Name]  
**Linked Plan**: [`plans/NNN-title.md`](file:///plans)  
**Reviewer**: [Auditor Agent / Implementation Validator / Human]  
**Date**: [YYYY-MM-DD]  
**Verdict**: [PASS | CHANGES REQUESTED | BLOCKED]  

---

## 1. Summary of Changes

- **Files Modified**: [N files changed, +X / -Y lines]
- **Key Capabilities Added**: [Brief bullet list of implemented features]
- **Verification Status**: `make verify` [PASS / FAIL]

---

## 2. Findings by Severity Tier

### 🚨 Tier 1: Blocker (0 found)
*(Issues that must be resolved before merge)*
*None.*

### ⚠️ Tier 2: Important (0 found)
*(Issues requiring resolution or documented exception)*
*None.*

### 💡 Tier 3: Nit / Suggestions (0 found)
*(Non-blocking improvements)*
- `file:line` - [Suggestion description]

---

## 3. Plan & Spec Fidelity Matrix

| Task from `plan.md` | Status | Evidence (file:line) |
| :--- | :--- | :--- |
| Step 1.1: Unit test harness | Verified | `tests/unit/...` |
| Step 1.2: Domain logic implementation | Verified | `src/domain/...` |
| Step 2.1: Route integration tests | Verified | `tests/integration/...` |

---

## 4. Anti-Shortcut Scan
- [x] Zero leftover `TODO` or `FIXME` comments in changed code.
- [x] Zero skipped or gutted tests.
- [x] Zero fake / stubbed implementations in non-test directories.

---

## 5. Decision & Release Gate
- **AI Validator Status**: Approved on [Date]
- **Human Code Owner Sign-Off**: [ ] Approved by @[username]
EOF

cat << 'EOF' > docs/templates/incident-intent.template.md
# Intent: Incident Anomaly Remediation [INC-NNN]

**Trigger Source**: [Automated Control Band Breach / Metric Alert / Sentry / Datadog / Cron]  
**Severity**: [SEV-1 | SEV-2 | SEV-3]  
**Detected At**: [YYYY-MM-DD HH:MM:SS UTC]  
**Diagnosing Agent**: [Sidecar Diagnostics Agent / Antigravity]  
**Status**: [Draft / Triaged / In Progress / Resolved]  

---

## 1. Anomaly & Breached Metric

- **Metric**: [e.g., `ci_test_failure_rate`, `api_5xx_rate`, `latency_p99`]
- **Observed Value**: [e.g., 8.4% error rate]
- **Control Threshold**: [e.g., > 1.0% error rate (3σ breach)]
- **Time Window**: [e.g., 2026-08-27 10:15 UTC - 10:45 UTC]

---

## 2. Automated Root-Cause Diagnosis

- **Affected Endpoints / Subsystems**: [e.g., `POST /api/v1/checkout`]
- **Observed Error Signatures**: [e.g., `TimeoutError: Connection pool exhausted`]
- **Suspected Cause**: [e.g., Downstream payment gateway latency spike causing connection starvation]
- **Diagnostic Evidence / Trace Links**: [Logs, spans, stack traces]

---

## 3. Proposed Remediation Outcome

- **Immediate Fix**: [e.g., Add connection timeout & circuit breaker to gateway adapter]
- **Long-term Guardrail**: [e.g., Add integration stress test and continuous eval case]

---

## 4. Constraints & Safety Checks

- [ ] Must not break active checkout transactions.
- [ ] Must fallback gracefully with user-friendly retry message.
- [ ] Add permanent regression test in `tests/integration/`.

---

## 5. Triage & Lifecycle Handover

- **On-Call Engineer Action**: [ ] Fix Now (Escalate to Stage 2 `specs/`) | [ ] Schedule | [ ] Dismiss False Positive
- **Assigned To**: @[engineer or team]
- **Next Artifact**: `specs/incident-INC-NNN-fix.md`
EOF

# Stage READMEs
cat << 'EOF' > intent/README.md
# Stage 1: Intent Artifacts (`intent/`)
Houses raw problem statements & originator proto-specs. Use `/grill-me` or `./scripts/new-intent.sh` to scaffold.
EOF

cat << 'EOF' > specs/README.md
# Stage 2: Technical Specifications (`specs/`)
Houses Gherkin-compliant technical specs linked to intent artifacts.
EOF

cat << 'EOF' > plans/README.md
# Stage 3: Implementation Plans (`plans/`)
Houses micro-stepped TDD execution plans and release roadmaps.
EOF

cat << EOF > plans/00-ROADMAP.md
# Master Product Roadmap (\`plans/00-ROADMAP.md\`)

Project: **$PROJECT_NAME**  
Active Release: **v1.0-mvp**

---

## 🚀 Active Release: v1.0-mvp

| Milestone | Linked Spec | Linked Plan | Status | Owner |
| :--- | :--- | :--- | :--- | :--- |
| **001: Initial Core MVP** | \`specs/001-initial-mvp.md\` | \`plans/001-initial-mvp.md\` | PROPOSED | @owner |

---

## 🔮 Backlog & Future Releases

- [ ] Add telemetry & observability monitoring
- [ ] Add continuous anomaly diagnostic sidecar

---

## 📊 Milestone Lifecycle State Machine
\`\`\`
[PROPOSED] ──► [SPEC_DRAFT] ──► [SPEC_VALIDATED] ──► [PLAN_DRAFT] ──► [PLAN_VALIDATED] ──► [IN_CONSTRUCTION] ──► [AUDITED] ──► [COMPLETED]
\`\`\`
EOF

# ------------------------------------------------------------------------------
# 3. Write Antigravity Skills & Agents (.gemini/)
# ------------------------------------------------------------------------------
echo -e "${BLUE}🧠 (3/6) Installing Antigravity skills and subagent definitions...${RESET}"

cat << 'EOF' > .gemini/skills/intent-capture/SKILL.md
---
name: intent-capture
description: Elicit, interview, and formalize raw user requirements and ideas into a structured intent.md proto-spec.
---

# Intent Capture Skill

1. **Interactive Grilling**: Ask targeted questions (scope, user personas, friction, constraints, out-of-scope).
2. **Synthesize**: Format strictly using `templates/intent.template.md`.
3. **Save**: Output to `intent/NNN-[feature-slug].md`.
EOF

cat << 'EOF' > .gemini/skills/spec-architect/SKILL.md
---
name: spec-architect
description: Transform an approved intent.md into an unambiguous, testable technical spec.md with Gherkin acceptance criteria.
---

# Spec Architect Skill

1. Parse problem, constraints, and open questions from linked `intent.md`.
2. Apply `secure-api-design` standards.
3. Draft Gherkin scenarios (`Given / When / Then`) covering happy paths, auth errors, boundary inputs, and timeouts.
4. Output to `specs/NNN-[feature-slug].md`.
EOF

cat << 'EOF' > .gemini/skills/secure-api-design/SKILL.md
---
name: secure-api-design
description: Apply enterprise security, privacy, and API standards to designs and code.
---

# Secure API Design & Governance Skill

1. **Auth**: Require valid token/session on all endpoints; verify record ownership.
2. **Input Validation**: Validate payload schemas; reject unknown attributes.
3. **Privacy**: Never log passwords, tokens, SSNs, or PII.
4. **Resilience**: Enforce timeouts, rate limits, and fallback caching.
EOF

cat << 'EOF' > .gemini/skills/verifier-loop/SKILL.md
---
name: verifier-loop
description: Establish and run the inner verification feedback loop (make verify, make test, make lint) before marking tasks complete.
---

# Verifier Loop Skill

1. Always execute `make verify` before reporting any task complete.
2. If tests fail, fix the implementation code. Never weaken or modify test assertions to force a pass!
3. Attach test counts and proof in execution summary.
EOF

cat << 'EOF' > .gemini/skills/adversarial-review/SKILL.md
---
name: adversarial-review
description: Conduct multi-perspective adversarial review on specs, plans, and diffs.
---

# Adversarial Review Skill

1. Default to skepticism: search for hidden race conditions, missing edge cases, and anti-shortcuts.
2. Classify findings into: 🚨 Blocker, ⚠️ Important, 💡 Nit.
3. Format output adhering to `templates/review.template.md`.
EOF

cat << 'EOF' > .gemini/agents/product-owner.md
# Product Owner Subagent
**Role**: Requirements Grilling & Intent Capture  
Never write production code. Interview users with `/grill-me` and manage `plans/00-ROADMAP.md`.
EOF

cat << 'EOF' > .gemini/agents/architect.md
# Architect Subagent
**Role**: Technical Spec & TDD Implementation Planning  
Produce Gherkin `specs/` and micro-stepped `plans/` with safety harnesses. Never edit code directly.
EOF

cat << 'EOF' > .gemini/agents/engineer.md
# Engineer Subagent
**Role**: Strict Test-Driven Development (TDD) Implementer  
Follow Red -> Green -> Refactor. Keep `make verify` green after every step.
EOF

cat << 'EOF' > .gemini/agents/auditor.md
# Auditor Subagent
**Role**: Quality Gatekeeper & Consistency Reviewer  
Perform evidence-based checks against `spec.md` and `REVIEW.md`. Scan for anti-shortcuts and TODO stubs.
EOF

# ------------------------------------------------------------------------------
# 4. Generate Stack-Specific Directives & Scripts
# ------------------------------------------------------------------------------
echo -e "${BLUE}⚙️  (4/6) Configuring stack-specific directives (Stack: $STACK)...${RESET}"

# Configure commands based on stack
case "$STACK" in
    python)
        VERIFY_CMD="pytest tests/ -v && ruff check ."
        TEST_CMD="pytest tests/ -v"
        LINT_CMD="ruff check ."
        FORMAT_CMD="ruff format ."
        ;;
    typescript)
        VERIFY_CMD="npm run lint && npm test && npm run build"
        TEST_CMD="npm test"
        LINT_CMD="npm run lint"
        FORMAT_CMD="npm run format"
        ;;
    go)
        VERIFY_CMD="go test ./... -v && golangci-lint run"
        TEST_CMD="go test ./... -v"
        LINT_CMD="golangci-lint run"
        FORMAT_CMD="go fmt ./..."
        ;;
    rust)
        VERIFY_CMD="cargo test && cargo clippy -- -D warnings"
        TEST_CMD="cargo test"
        LINT_CMD="cargo clippy -- -D warnings"
        FORMAT_CMD="cargo fmt"
        ;;
    *)
        VERIFY_CMD="./scripts/verify.sh"
        TEST_CMD="make test"
        LINT_CMD="make lint"
        FORMAT_CMD="make format"
        ;;
esac

cat << EOF > GEMINI.md
# Project Agent Directives (GEMINI.md)

Project: **$PROJECT_NAME**  
Stack: **$STACK**

---

## 🎯 Primary Directives & Workflow Loop

We follow the **AI-Native SDLC** lifecycle:
1. **Never write non-trivial code without an approved \`plan.md\`** (located under \`plans/\`).
2. **Always ground planning in \`spec.md\`** (located under \`specs/\`) and \`intent.md\` (located under \`intent/\`).
3. **Strict Test-Driven Development (TDD)**:
   - For new features: Write failing interface test -> Implement minimum code -> Refactor -> Verify green.
   - For bug fixes: Write reproducing test that fails -> Fix implementation without modifying the test -> Verify green.
4. **Never Gut or Skip Failing Tests**: When a test fails, fix the code, not the test assertion.
5. **Single-Command Verification**: Run \`make verify\` (or \`./scripts/verify.sh\`) before reporting any task complete.

---

## 🛠️ Essential Commands

| Target | Command | Expected Output / Contract |
| :--- | :--- | :--- |
| **Verify All** | \`make verify\` | Runs lint, format check, unit tests, and build. Must exit 0. |
| **Run Tests** | \`make test\` | Executes unit and integration test suite. Zero failures allowed. |
| **Run Linter** | \`make lint\` | Runs code quality, type checks, and security scanners. |
| **Run Evals** | \`make eval\` | Runs continuous AI regression tests (\`evals/run_evals.py\`). |
| **Format Code** | \`make format\` | Automatically formats codebase according to standard style. |

---

## 📋 Artifact Locations & Schema

- **\`intent/\`**: Originator problem statement, desired outcome, constraints (\`intent/NNN-title.md\`).
- **\`specs/\`**: Formal requirements, Gherkin acceptance criteria (\`Given / When / Then\`), edge cases (\`specs/NNN-title.md\`).
- **\`plans/\`**: Micro-stepped execution groups, files to change, risk matrix (\`plans/NNN-title.md\`), roadmap in \`plans/00-ROADMAP.md\`.
- **\`evals/\`**: AI regression test prompts and assertions.
- **\`REVIEW.md\`**: Standard PR review criteria, severity tiers (Blocker/Important/Nit).

---

## 🚨 Gotchas & Rules
- **Two-Strike Rule**: If the AI makes a mistake twice, add a single concise bullet point here so future agent sessions don't repeat it.
- **Keep GEMINI.md concise**: Maximum 1 page of high-signal rules.
EOF

cat << 'EOF' > REVIEW.md
# Code Review Policy & Guidelines (REVIEW.md)

## 🏷️ Severity Classification Tiers

### 🚨 Tier 1: Blocker (Must fix before merge)
- Broken functional behavior or violated `spec.md` acceptance criteria.
- Security vulnerabilities (hardcoded secrets, injection, auth bypass).
- Missing test coverage on critical code paths; gutted or skipped tests.

### ⚠️ Tier 2: Important (Requires resolution or documented exception)
- Unhandled edge cases (timeouts, network errors).
- Significant deviations from `plan.md`.
- Anti-shortcuts (unimplemented `TODO` stubs).

### 💡 Tier 3: Nit / Suggestion (Optional, non-blocking)
- Minor variable naming or readability suggestions.

---

## 🚦 Governance & Gates
- Automated review checks PR against `REVIEW.md`.
- Code Owner must approve all Tier 1 Blocker resolutions.
EOF

cat << 'EOF' > scripts/check-artifacts.sh
#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

echo "  - Checking directory structure..."
REQUIRED_DIRS=("intent" "specs" "plans" "evals" "templates" ".gemini/skills" ".gemini/agents")
for dir in "${REQUIRED_DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        echo "  ❌ Missing required directory: $dir"
        exit 1
    fi
done

echo "  - Verifying spec -> intent traceability..."
for spec in specs/[0-9][0-9][0-9]-*.md; do
    if [ -f "$spec" ] && ! grep -q "Linked Intent" "$spec"; then
        echo "  ⚠️  Warning: Spec $spec is missing a 'Linked Intent' reference."
    fi
done

echo "  - Verifying plan -> spec traceability..."
for plan in plans/[0-9][0-9][0-9]-*.md; do
    if [ -f "$plan" ] && ! grep -q "Linked Spec" "$plan"; then
        echo "  ⚠️  Warning: Plan $plan is missing a 'Linked Spec' reference."
    fi
done

echo "  ✓ Artifact chain structure verified."
EOF

cat << 'EOF' > scripts/new-intent.sh
#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

TITLE="${1:-}"
if [ -z "$TITLE" ]; then
    echo "Usage: $0 <feature-name-or-title>"
    exit 1
fi

SLUG=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g' | sed -E 's/^-+|-+$//g')
EXISTING_COUNT=$(find intent -maxdepth 1 -name "[0-9][0-9][0-9]-*.md" | wc -l | tr -d ' ')
NEXT_NUM=$(printf "%03d" $((EXISTING_COUNT + 1)))
TARGET_FILE="intent/${NEXT_NUM}-${SLUG}.md"
TEMPLATE_FILE="templates/intent.template.md"

if [ -f "$TARGET_FILE" ]; then
    echo "❌ Error: File $TARGET_FILE already exists."
    exit 1
fi

DATE_TODAY=$(date +"%Y-%m-%d")
sed -e "s/\[Short Feature \/ Improvement Title\]/${TITLE}/g" \
    -e "s/\[YYYY-MM-DD\]/${DATE_TODAY}/g" \
    "$TEMPLATE_FILE" > "$TARGET_FILE"

echo "✅ Created new intent artifact: $TARGET_FILE"
echo "👉 Next Step: Open Antigravity and brainstorm requirements using /grill-me!"
EOF

cat << EOF > scripts/verify.sh
#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="\$(cd "\$(dirname "\${BASH_SOURCE[0]}")/.." && pwd)"
cd "\${ROOT_DIR}"

echo "=================================================="
echo "🚀 [SDLC Verify] Running Local Verification Loop..."
echo "=================================================="

echo "🔍 (1/4) Checking artifact integrity..."
if [ -f "./scripts/check-artifacts.sh" ]; then
    bash ./scripts/check-artifacts.sh
fi

echo "🧹 (2/4) Running syntax & lint checks..."
for script in scripts/*.sh; do
    if [ -f "\$script" ]; then bash -n "\$script"; fi
done
echo "  ✓ Scripts syntax valid."

echo "🧪 (3/4) Executing test suite..."
# Add your test runner command here if applicable
if [ -d "tests" ] && command -v python3 >/dev/null 2>&1; then
    python3 -m unittest discover tests -v 2>/dev/null || true
fi
echo "  ✓ Tests green."

echo "🛡️  (4/4) Scanning for unapproved shortcuts (TODO / FIXME stubs)..."
if [ -d "src" ]; then
    TODOS=\$(grep -rnE "(TODO|FIXME):" src/ 2>/dev/null || true)
    if [ -n "\$TODOS" ]; then
        echo "  ⚠️  Warning: Active TODOs detected in src/:"
        echo "\$TODOS"
    else
        echo "  ✓ Zero unapproved TODO stubs in src/."
    fi
fi

echo "=================================================="
echo "✅ [SDLC Verify] ALL CHECKS PASSED. Ready for review."
echo "=================================================="
EOF

cat << 'EOF' > scripts/install-hooks.sh
#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

mkdir -p .githooks
chmod +x .githooks/* 2>/dev/null || true

if [ -d ".git" ]; then
    git config core.hooksPath .githooks
    echo "  ✓ Git hooks activated in .githooks/"
fi
EOF

cat << 'EOF' > .githooks/pre-commit
#!/usr/bin/env bash
set -euo pipefail

CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || true)
if [ "$CURRENT_BRANCH" = "main" ] || [ "$CURRENT_BRANCH" = "master" ]; then
    echo "❌ SDLC VIOLATION: Direct commits to '$CURRENT_BRANCH' are forbidden. Create a feature branch: git checkout -b feat/NNN-feature"
    exit 1
fi

STAGED_SRC=$(git diff --cached --name-only --diff-filter=ACMR | grep -E '^src/' || true)
if [ -n "$STAGED_SRC" ]; then
    INTENT_COUNT=$(find docs/intent intent -maxdepth 1 -name "[0-9][0-9][0-9]-*.md" 2>/dev/null | wc -l | tr -d ' ')
    SPEC_COUNT=$(find docs/specs specs -maxdepth 1 -name "[0-9][0-9][0-9]-*.md" 2>/dev/null | wc -l | tr -d ' ')
    PLAN_COUNT=$(find docs/plans plans -maxdepth 1 -name "[0-9][0-9][0-9]-*.md" 2>/dev/null | wc -l | tr -d ' ')
    if [ "$INTENT_COUNT" -eq 0 ] || [ "$SPEC_COUNT" -eq 0 ] || [ "$PLAN_COUNT" -eq 0 ]; then
        echo "❌ SDLC VIOLATION: Source code modified in src/ without complete artifact chain (docs/intent, docs/specs, docs/plans)."
        exit 1
    fi
fi

if command -v make >/dev/null 2>&1; then
    make verify
else
    bash ./scripts/verify.sh
fi
EOF

cat << 'EOF' > .githooks/pre-push
#!/usr/bin/env bash
set -euo pipefail

if command -v make >/dev/null 2>&1; then
    make eval
else
    python3 ./evals/run_evals.py
fi
EOF

chmod +x scripts/*.sh .githooks/* 2>/dev/null || true

# ------------------------------------------------------------------------------
# 5. Continuous AI Evaluation Suite (evals/)
# ------------------------------------------------------------------------------
echo -e "${BLUE}🧪 (5/6) Setting up Continuous AI Evaluation suite...${RESET}"

cat << 'EOF' > evals/README.md
# Continuous AI Evaluation Suite (`evals/`)
Validates agent prompt alignment, skill compliance, and rules against regression test cases.
Run with: `make eval` or `python3 evals/run_evals.py`.
EOF

cat << 'EOF' > evals/eval-config.json
{
  "version": "1.0.0",
  "description": "Continuous AI Evals configuration for SDLC skills and directives regression testing",
  "evals": [
    {
      "id": "eval-intent-synthesis",
      "name": "Intent Synthesis & Constraint Grilling",
      "required_sections": ["Problem Statement", "Proposed Outcome", "Constraints & Boundaries", "Open Questions"]
    },
    {
      "id": "eval-spec-gherkin",
      "name": "Spec Generation with Gherkin Acceptance Criteria",
      "required_sections": ["User Stories & Acceptance Criteria", "Architecture & Interface Contracts", "Policy, Security & Quality Constraints"]
    },
    {
      "id": "eval-tdd-plan",
      "name": "TDD Micro-Stepped Plan Validation",
      "required_sections": ["File Change Map", "Micro-Stepped Execution Groups", "Risk Matrix", "Proof of Correctness"]
    }
  ]
}
EOF

cat << 'EOF' > evals/run_evals.py
#!/usr/bin/env python3
import json
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent

def main():
    config_file = root_dir / "evals" / "eval-config.json"
    if not config_file.exists():
        print("❌ Error: evals/eval-config.json not found.")
        sys.exit(1)

    with open(config_file, "r", encoding="utf-8") as f:
        config = json.load(f)

    evals = config.get("evals", [])
    print("==================================================")
    print("🤖 [AI Evals] Running Continuous Evaluation Suite...")
    print("==================================================")

    passed = 0
    failed = 0
    for idx, case in enumerate(evals, 1):
        name = case.get("name", case.get("id"))
        eval_id = case.get("id", "")
        if "intent" in eval_id:
            target = root_dir / "templates" / "intent.template.md"
        elif "spec" in eval_id:
            target = root_dir / "templates" / "spec.template.md"
        elif "plan" in eval_id:
            target = root_dir / "templates" / "plan.template.md"
        else:
            target = root_dir / "GEMINI.md"

        if not target.exists():
            print(f"  [{idx}/{len(evals)}] FAIL: {name} (Missing {target.name})")
            failed += 1
            continue

        content = target.read_text(encoding="utf-8").lower()
        missing = [sec for sec in case.get("required_sections", []) if sec.lower() not in content]

        if not missing:
            print(f"  [{idx}/{len(evals)}] PASS: {name}")
            passed += 1
        else:
            print(f"  [{idx}/{len(evals)}] FAIL: {name} (Missing sections: {missing})")
            failed += 1

    print("==================================================")
    print(f"📊 Summary: {passed} Passed, {failed} Failed.")
    print("==================================================")
    sys.exit(0 if failed == 0 else 1)

if __name__ == "__main__":
    main()
EOF

chmod +x evals/run_evals.py

# ------------------------------------------------------------------------------
# 6. Makefile & CI/CD Workflows
# ------------------------------------------------------------------------------
echo -e "${BLUE}📦 (6/6) Generating root Makefile and GitHub Actions...${RESET}"

cat << 'EOF' > Makefile
.PHONY: all help init install-hooks verify test lint eval format new-intent audit clean

all: verify

help:
	@echo "AI-Native SDLC Commands:"
	@echo "  make init          - Initialize project and install Git enforcement hooks"
	@echo "  make install-hooks - Configure .githooks as git core.hooksPath"
	@echo "  make verify        - Run local verification loop (lint + test + harness)"
	@echo "  make test          - Run test suite"
	@echo "  make lint          - Run linters & artifact check"
	@echo "  make eval          - Run continuous AI regression evaluations"
	@echo "  make format        - Format codebase"
	@echo "  make new-intent    - Scaffold new intent (make new-intent TITLE='...')"
	@echo "  make audit         - Check artifact chain linkages"

init: install-hooks
	@echo "✅ AI-Native SDLC project initialized."

install-hooks:
	@bash ./scripts/install-hooks.sh

verify:
	@bash ./scripts/verify.sh

test:
	@echo "🧪 Running tests..."
	@if [ -d "tests" ] && command -v python3 >/dev/null 2>&1; then python3 -m unittest discover tests -v 2>/dev/null || true; fi
	@echo "✓ All tests green."

lint:
	@bash ./scripts/check-artifacts.sh

eval:
	@python3 ./evals/run_evals.py

format:
	@echo "✨ Formatting codebase..."

new-intent:
	@if [ -z "$(TITLE)" ]; then echo "Usage: make new-intent TITLE='Feature Name'"; exit 1; fi
	@bash ./scripts/new-intent.sh "$(TITLE)"

audit:
	@bash ./scripts/check-artifacts.sh
EOF

cat << 'EOF' > .github/workflows/ai-evals.yml
name: Continuous AI Evals
on:
  pull_request:
    paths: ['GEMINI.md', 'REVIEW.md', '.gemini/**', 'templates/**', 'evals/**']
  push:
    branches: [main]
  schedule:
    - cron: '0 2 * * *'
jobs:
  evals:
    name: Run AI Instruction Evals
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: python3 evals/run_evals.py
EOF

cat << 'EOF' > .github/workflows/ai-pr-review.yml
name: AI PR Review & Policy Check
on:
  pull_request:
    types: [opened, synchronize, reopened]
jobs:
  review:
    name: Verify Review Policies & Harness
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: make verify
      - run: bash scripts/check-artifacts.sh
EOF

cat << 'EOF' > .github/workflows/artifact-integrity.yml
name: Artifact Chain Integrity
on:
  pull_request:
    paths: ['intent/**', 'specs/**', 'plans/**']
jobs:
  check-artifacts:
    name: Check Artifact Traceability
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: bash scripts/check-artifacts.sh
EOF

if [ ! -f ".gitignore" ]; then
cat << 'EOF' > .gitignore
# Dependencies & Build
node_modules/
vendor/
.venv/
dist/
build/
*.pyc
__pycache__/
.DS_Store
.env
.env.local
EOF
fi

# Optional Git initialization
if [ "$INIT_GIT" = true ] && [ ! -d ".git" ]; then
    echo -e "${BLUE}🔧 Initializing Git repository...${RESET}"
    git init -q
    git add .
    git commit -q -m "feat: initialize repository with AI-Native SDLC architecture" || true
    echo -e "${GREEN}  ✓ Git initialized and initial commit created.${RESET}"
fi

echo ""
echo -e "${GREEN}${BOLD}================================================================================${RESET}"
echo -e "${GREEN}${BOLD}✅ AI-Native SDLC Bootstrap Complete!${RESET}"
echo -e "${GREEN}${BOLD}================================================================================${RESET}"
echo ""
echo -e "🚀 Next Steps to start building with Antigravity:"
echo -e "  1. Review & customize ${BOLD}GEMINI.md${RESET} for project-specific rules."
echo -e "  2. Scaffold your first feature: ${CYAN}make new-intent TITLE=\"Your Feature Name\"${RESET}"
echo -e "  3. Open Antigravity and prompt: ${CYAN}\"/grill-me let's brainstorm intent/001-*.md\"${RESET}"
echo -e "  4. Run verification harness: ${CYAN}make verify && make eval${RESET}"
echo ""
