# Intent: Fix Duck-Jump State Glitch and Mid-Air Ducking Physics

**Author**: Quality Assurance Agent & User  
**Date**: 2026-09-16  
**Status**: Approved  
**Target Milestone**: v1.1-bugfix  

---

## 1. Problem Statement

A physics state machine glitch was discovered where the player dinosaur can be simultaneously jumping and ducking.
- **Current State**: If a player presses jump while holding duck, `is_jumping` becomes `True` while `is_ducking` remains `True`. The player floats through the air as a squashed ducking hitbox.
- **User Pain / Friction**: Unnatural flight animations and unfair hitbox clipping through obstacles while jumping.
- **Impact & Urgency**: High; violates game physics rules and causes visual glitching.

---

## 2. Proposed Outcome

1. Calling `jump()` immediately resets `is_ducking` to `False`.
2. When airborne, calling `duck(True)` triggers a "fast fall" (accelerates downward velocity) and prevents jumping-duck visual overlap.
3. Add automated regression unit test that reproduces the bug and guarantees zero regressions.

---

## 3. Affected Users & Systems

- **Affected Systems**: `src/engine/physics.py`, `public/game.js`, `tests/test_game_engine.py`.

---

## 4. Approval & Handover

- **Approved**: @chuancc on 2026-09-16
- **Ready for Stage 2 (Design)**: `docs/specs/003-fix-duck-jump-glitch.md`
