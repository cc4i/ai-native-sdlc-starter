# Plan: Obstacle Minimum Spacing Clamping

**Linked Spec**: [`docs/specs/004-obstacle-spacing-clamping.md`](../specs/004-obstacle-spacing-clamping.md)  
**Author**: Game Engine Architect  
**Date**: 2026-09-16  
**Status**: Completed  

---

## 1. Scope & Strategy

- **Strategy**: TDD — write test for minimum spacing calculation, implement clamping logic, verify with `make verify` and `check-control-bands.py`.

---

## 2. Micro-Stepped Execution Groups

### Execution Group 1: Minimum Gap Logic (TDD)
- [x] **Step 1.1 (Red)**: Add unit test in `tests/test_game_engine.py` asserting `calculate_min_safe_gap` never drops below 140.0px.
- [x] **Step 1.2 (Green)**: Implement `calculate_min_safe_gap` in `src/engine/physics.py` and clamp in `public/game.js`.
- [x] **Step 1.3 (Verify)**: Run `make test`, `python3 scripts/check-control-bands.py`, and `make verify`.

---

## 3. Proof of Correctness & Harness

- [x] Unit test `test_min_safe_obstacle_spacing` passes.
- [x] `check-control-bands.py` exits 0.
- [x] `make verify` exits 0.
