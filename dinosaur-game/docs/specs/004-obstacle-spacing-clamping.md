# Spec: Obstacle Minimum Spacing Clamping

**Linked Intent**: [`docs/intent/004-incident-INC-001-obstacle-spacing-clamping.md`](../intent/004-incident-INC-001-obstacle-spacing-clamping.md)  
**Author**: Game Engine Architect  
**Date**: 2026-09-16  
**Status**: Validated  

---

## 1. Overview & Scope

Enforces a deterministic minimum physical gap between consecutive obstacles to guarantee that every obstacle arrangement is physically jumpable.

- **In Scope**:
  - `calculate_min_safe_gap(speed: float) -> float` enforcing minimum pixel distance (>= 140px).
  - Validation in `src/engine/physics.py` and `public/game.js`.

---

## 2. User Stories & Acceptance Criteria (Gherkin Scenarios)

### Story 1: Obstacle Spacing Guarantee
**As a** player running at high speed,  
**I want** consecutive obstacles to never spawn closer than the minimum jump recovery gap,  
**So that** game over is always attributable to skill rather than impossible terrain.

#### Scenario 1.1: Minimum distance clamping
```gherkin
Given a previously spawned obstacle ending at position X1
When the next obstacle is scheduled to spawn at position X2
Then the distance (X2 - X1) is strictly >= MIN_SAFE_GAP (140.0 pixels)
And no impassable double-cactus clusters can be generated
```

---

## 3. Adversarial Review & Sign-Off

- **Spec Gate Verdict**: PASSED
- **Sign-off**: Approved by @chuancc on 2026-09-16
- **Ready for Stage 3 (Build)**: `docs/plans/004-obstacle-spacing-clamping.md`
