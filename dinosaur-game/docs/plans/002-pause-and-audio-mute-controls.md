# Plan: Pause and Audio Mute Controls

**Linked Spec**: [`docs/specs/002-pause-and-audio-mute-controls.md`](../specs/002-pause-and-audio-mute-controls.md)  
**Author**: Game Engine Architect  
**Date**: 2026-09-16  
**Status**: Completed  

---

## 1. Scope & Strategy

- **Objective**: Implement pause/resume and audio mute toggles with unit tests in `src/engine/physics.py` and front-end controls in `public/game.js`, `public/index.html`, and `public/style.css`.
- **Strategy**: TDD — Write tests for `GameSession` pause logic and mute states first, implement, wire frontend, run `make verify`.

---

## 2. File Change Map

| Path | Change Type | Purpose / Description |
| :--- | :--- | :--- |
| `tests/test_game_engine.py` | Modify | Add unit tests for GameSession pause state and mute toggle |
| `src/engine/physics.py` | Modify | Implement GameSession class managing paused state |
| `public/index.html` | Modify | Add Pause and Mute buttons to HUD, Add Paused Overlay |
| `public/style.css` | Modify | Style HUD control buttons and Paused Overlay |
| `public/game.js` | Modify | Implement STATE.PAUSED, <kbd>P</kbd>/<kbd>M</kbd> listeners, localStorage sync |

---

## 3. Micro-Stepped Execution Groups

### Execution Group 1: Core Engine GameSession & Pause Logic (TDD)
- [x] **Step 1.1 (Red)**: Write unit tests in `tests/test_game_engine.py` testing `GameSession` pause freezing updates.
- [x] **Step 1.2 (Green)**: Implement `GameSession` in `src/engine/physics.py`. Verify tests pass.

### Execution Group 2: Frontend HUD Controls & Keybinds
- [x] **Step 2.1**: Update `public/index.html` and `public/style.css` with pause/mute buttons and pause overlay.
- [x] **Step 2.2**: Update `public/game.js` to handle pause state, mute toggle, and localStorage persistence.

### Execution Group 3: Verification
- [x] **Step 3.1**: Run `make verify` and `make eval`.
- [x] **Step 3.2**: Record PR review audit report in `docs/reviews/002-pause-and-audio-mute-controls.md`.

---

## 4. Proof of Correctness & Harness

- [x] `make verify` exits code 0 with all tests passing.
- [x] Manual test: Pressing <kbd>P</kbd> freezes canvas, pressing <kbd>M</kbd> toggles audio.
