# Intent: Incident Anomaly Remediation [INC-001]

**Trigger Source**: Automated Control Band Breach / Telemetry Alert  
**Severity**: SEV-2  
**Detected At**: 2026-09-16 10:30:00 UTC  
**Diagnosing Agent**: SRE Diagnostics Agent  
**Status**: Approved  
**Target Milestone**: v1.1-sre-remediation  

---

## 1. Anomaly & Breached Metric

- **Metric**: `obstacle_min_spacing`
- **Observed Value**: Random obstacle generation permitted distance down to ~60px between obstacles at high speeds.
- **Control Threshold**: > 95.0px (Lower 3σ threshold in `bands.yaml`).
- **Symptom**: Players occasionally encountered two large cacti spawned 60px apart, making landing and jumping over both physically impossible without crashing.

---

## 2. Automated Root-Cause Diagnosis

- **Affected System**: `src/engine/physics.py` and `public/game.js:spawnObstacle()`.
- **Root Cause**: Random distance generator `1.1 + Math.random() * 1.4` multiplied by scroll speed yielded pixel gaps below the minimum landing recovery distance of the dinosaur.
- **Proposed Remediation**: Introduce an explicit `min_obstacle_gap` parameter enforcing at least 140px separation between the trailing edge of an obstacle and the next spawned obstacle.

---

## 3. Constraints & Safety Checks

- [x] Must not freeze obstacle spawning entirely.
- [x] Must enforce minimum gap >= 140px regardless of score or game speed.
- [x] Add automated unit test in `tests/test_game_engine.py`.

---

## 4. Triage & Lifecycle Handover

- **Action**: Fix Now (Escalate to Stage 2 `docs/specs/004-obstacle-spacing-clamping.md`)
- **Assigned To**: @dsh-agent
- **Next Artifact**: `docs/specs/004-obstacle-spacing-clamping.md`
