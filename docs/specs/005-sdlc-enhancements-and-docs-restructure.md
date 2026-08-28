# Specification: SDLC Enhancements and Docs Directory Restructure

**Linked Intent**: [`intent/005-sdlc-enhancements-and-docs-restructure.md`](../../intent/005-sdlc-enhancements-and-docs-restructure.md)  
**Author**: Antigravity Staff Architect  
**Date**: 2026-08-28  
**Status**: Ready for Planning  

---

## 1. Overview & Architecture

This specification covers four interconnected system enhancements:
1. **Restructure Artifact Hierarchy**: Move `intent/`, `specs/`, `plans/`, `templates/`, `reviews/` under `docs/`.
2. **`shipped: <SHA>` Verification**: Ensure all `COMPLETED` milestones in `plans/` (or `docs/plans/`) record the resolving git commit SHA.
3. **Stage 6 Control Bands Engine**: Add `bands.yaml` and `src/tools/band_detector.py` providing statistical $\sigma$-deviation tracking and tier actions (`log`, `diagnose`, `act`).
4. **Agent Lifecycle Hook**: Add `hooks.json` and `scripts/agent_guard.py` implementing `PreToolUse` tool call interception and `Stop` loop validation.

---

## 2. Gherkin Acceptance Scenarios

### Feature: Unified Docs Hierarchy
```gherkin
Scenario: Artifact validation with docs/ layout
  Given the repository contains artifacts under docs/intent/, docs/specs/, docs/plans/, docs/reviews/, docs/templates/
  When the developer or CI runs "bash scripts/check-artifacts.sh"
  Then the script checks docs/ paths and exits with code 0.

Scenario: Scaffolding a new intent under docs/
  Given the new-intent script is updated
  When the developer runs "make new-intent TITLE='Telemetry Pipeline'"
  Then a new file is created at "docs/intent/NNN-telemetry-pipeline.md".
```

### Feature: Shipped Commit Traceability
```gherkin
Scenario: Plan marked completed with valid commit SHA
  Given a plan file with "Status: COMPLETED"
  And the plan includes a "Shipped: <SHA>" or "shipped: <SHA>" header with a valid git commit SHA
  When "bash scripts/check-artifacts.sh" runs
  Then the check accepts the plan as verified.

Scenario: Plan marked completed missing commit SHA
  Given a plan file with "Status: COMPLETED"
  And the plan lacks a valid "shipped: <SHA>" reference
  When "bash scripts/check-artifacts.sh" runs
  Then the check warns or fails the verification.
```

### Feature: Stage 6 Control Bands Anomaly Detection
```gherkin
Scenario: Metric within normal baseline
  Given bands.yaml configures baseline_days=28 and sigma thresholds
  When band_detector evaluates a daily metric series with deviation < 1.0 sigma
  Then it assigns tier "log" and triggers no action.

Scenario: Metric exceeding tier 3 threshold
  Given a metric has a deviation >= 3.0 sigma and exceeds min_absolute_change
  When band_detector evaluates the metric
  Then it assigns tier "act" with action "open_intent_pr".
```

### Feature: Agent PreToolUse Guard
```gherkin
Scenario: Agent attempts git add -A or git commit -a
  Given hooks.json is active with PreToolUse matcher "run_command"
  When the agent sends tool call "git add -A" or "git commit -am 'message'"
  Then scripts/agent_guard.py outputs decision "deny" with a descriptive reason.

Scenario: Agent runs valid verification command
  When the agent sends tool call "make verify"
  Then scripts/agent_guard.py outputs decision "allow".
```

---

## 3. Interfaces & Contracts

### 3.1 Control Band Configuration Schema (`bands.yaml`)
```yaml
defaults:
  baseline_days: 28
  min_baseline_points: 14
  sigma:
    log: 1.0
    diagnose: 2.0
    act: 3.0

metrics:
  - name: daily_llm_cost_usd
    unit: USD
    direction: increase
    min_absolute_change: 5.0
    tier_3_action: open_intent_pr

  - name: daily_error_rate_pct
    unit: percent
    direction: increase
    min_absolute_change: 1.0
    tier_3_action: open_intent_pr
```

### 3.2 Agent Hook Specification (`hooks.json`)
```json
{
  "agent-guard": {
    "enabled": true,
    "PreToolUse": [
      {
        "matcher": "run_command",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ./scripts/agent_guard.py",
            "timeout": 15
          }
        ]
      }
    ]
  }
}
```
