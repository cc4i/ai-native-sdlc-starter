# Spec: Fix Duck-Jump State Glitch and Mid-Air Ducking Physics

**Linked Intent**: [`docs/intent/003-fix-duck-jump-glitch.md`](../intent/003-fix-duck-jump-glitch.md)  
**Author**: Game Engine Architect  
**Date**: 2026-09-16  
**Status**: Validated  

---

## 1. Overview & Scope

Ensures state mutual exclusion between jumping and ducking:
- Jumping clears ducking state.
- Airborne ducking activates fast-drop physics rather than a squashed flying sprite.

---

## 2. User Stories & Acceptance Criteria (Gherkin Scenarios)

### Story 1: Duck State Cancellation on Jump
**As a** player holding down duck,  
**I want** pressing jump to cancel ducking and perform a proper jump,  
**So that** my dinosaur stands tall to jump and doesn't float as a squashed box.

#### Scenario 1.1: Jump cancels duck state
```gherkin
Given a dinosaur with is_ducking = true
When the jump() method is executed
Then is_jumping transitions to true
And is_ducking transitions to false
And the effective hitbox uses full standing height (44.0)
```

#### Scenario 1.2: Airborne ducking accelerates descent (fast-drop)
```gherkin
Given a dinosaur jumping mid-air with upward or downward velocity
When duck(true) is invoked
Then gravity or downward velocity increases by fast-drop factor
And the dinosaur returns to ground faster than normal gravity
```

---

## 3. Adversarial Review & Sign-Off

- **Spec Gate Verdict**: PASSED
- **Sign-off**: Approved by @chuancc on 2026-09-16
- **Ready for Stage 3 (Build)**: `docs/plans/003-fix-duck-jump-glitch.md`
