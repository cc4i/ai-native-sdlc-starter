# Spec: AI-Native SDLC Starter Template & Bootstrap Engine

**Linked Intent**: [`intent/000-ai-sdlc-starter-template.md`](../../intent/000-ai-sdlc-starter-template.md)  
**Author**: Antigravity SDLC Architect  
**Date**: 2026-08-27  
**Status**: Approved  

---

## 1. Overview & Scope

Design and package a comprehensive repository template and standalone CLI bootstrapper for the AI-Native SDLC using Google Jetski and Antigravity.

- **In Scope**:
  - Core directory architecture (`intent/`, `specs/`, `plans/`, `evals/`, `templates/`, `.gemini/`, `scripts/`).
  - Native Antigravity skills (`intent-capture`, `spec-architect`, `secure-api-design`, `verifier-loop`, `adversarial-review`).
  - Antigravity subagent roles (`product-owner`, `architect`, `engineer`, `auditor`).
  - Single-command local verification harness (`make verify`, `scripts/verify.sh`).
  - Continuous AI evaluation regression suite (`make eval`, `evals/eval-config.json`, `evals/run_evals.py`).
  - Standalone, zero-clone `bootstrap.sh` script supporting stack auto-detection and custom naming.
  - Team onboarding documentation (`ONBOARDING.md`, `README.md`).
  - Reference working agentic application in `src/` and `tests/`.

---

## 2. User Stories & Acceptance Criteria (Gherkin)

### Story 1: Zero-Clone Project Initialization
**As a** software engineer starting a new project  
**I want** to run a single bootstrap command  
**So that** my repository is pre-configured with all AI-native SDLC directories, templates, and skills  

#### Scenario 1.1: Standalone bootstrap execution
```gherkin
Given an empty target directory "/tmp/new-service"
When the user executes "bash bootstrap.sh /tmp/new-service --name='New Service' --stack=python"
Then all lifecycle directories ("intent", "specs", "plans", "evals", "templates", ".gemini", "scripts") are created
And "GEMINI.md", "REVIEW.md", and "Makefile" are configured
And "make verify" and "make eval" in the target directory pass with exit code 0
```

### Story 2: Single-Command Local Feedback Loop
**As an** AI agent or human developer  
**I want** to execute a unified verification command  
**So that** I know immediately if tests, linters, or anti-shortcuts fail  

#### Scenario 2.1: Verification success
```gherkin
Given a project following the AI-native SDLC template
When "make verify" is executed
Then artifact linkages (spec->intent, plan->spec) are verified
And syntax and lint checks pass
And unit/integration tests pass
And zero unapproved "TODO" stubs are detected in production source code
And the command exits with code 0
```

---

## 3. Adversarial Review & Sign-Off
- **Spec Validator Gate**: PASSED (Unanimous 3/3 skeptics)
- **Approved by**: @cc4i on 2026-08-27
- **Ready for Stage 3 (Build)**: `plans/000-ai-sdlc-starter-template.md`
