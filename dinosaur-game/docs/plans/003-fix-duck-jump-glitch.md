# Plan: Fix Duck-Jump State Glitch and Mid-Air Ducking Physics

**Linked Spec**: [`docs/specs/003-fix-duck-jump-glitch.md`](../specs/003-fix-duck-jump-glitch.md)  
**Author**: Game Engine Architect  
**Date**: 2026-09-16  
**Status**: Completed  

---

## 1. Scope & Strategy

- **Strategy**: Strict Bug-Fix TDD (Reproducing test fails first -> Fix code without touching test -> Verify green).
- **Files Modified**: `tests/test_game_engine.py`, `src/engine/physics.py`, `public/game.js`.

---

## 2. Micro-Stepped Execution Groups

### Execution Group 1: Reproducing Test & Physics Fix (TDD)
- [x] **Step 1.1 (Red)**: Add reproducing test `test_jumping_cancels_ducking_state` in `tests/test_game_engine.py`. Confirm failure.
- [x] **Step 1.2 (Green)**: Update `Dinosaur.jump()` in `src/engine/physics.py` and `public/game.js` to clear `is_ducking = False` and support fast-drop.
- [x] **Step 1.3 (Verify)**: Run `make test` and `make verify`. Confirm test passes without touching test assertions.

---

## 3. Proof of Correctness & Harness

- [x] Unit test `test_jumping_cancels_ducking_state` passes.
- [x] `make verify` passes cleanly with 0 errors.
