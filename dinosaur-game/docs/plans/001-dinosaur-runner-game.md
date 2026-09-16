# Plan: Endless Runner Dinosaur Browser Game

**Linked Spec**: [`docs/specs/001-dinosaur-runner-game.md`](../specs/001-dinosaur-runner-game.md)  
**Author**: Game Engine Architect  
**Date**: 2026-09-16  
**Status**: Completed  

---

## 1. Scope & Strategy

- **Objective**: Implement the full offline Dinosaur Runner Game with a testable physics engine, AABB collision detection, procedural obstacle spawning, HTML5 Canvas renderer, synthesized retro audio effects, and static game server.
- **Strategy**: Test-Driven Development (TDD) for core physics and game logic, followed by canvas rendering wiring and single-command verification (`make verify`).
- **Estimated Execution Groups**: 3 groups (Core Engine TDD ➔ Canvas Browser Game ➔ Verification & Server).

---

## 2. File Change Map

| Path | Change Type | Purpose / Description |
| :--- | :--- | :--- |
| `src/engine/physics.py` | New | Physics equations, AABB collision checks, obstacle spawn logic |
| `src/server.py` | New | Zero-dependency local web server for browser play |
| `tests/test_game_engine.py` | New | Automated unit test suite verifying physics, hitboxes, and scores |
| `public/index.html` | New | Game canvas DOM structure, controls, and HUD |
| `public/style.css` | New | Retro pixel-style styling and responsive layout |
| `public/game.js` | New | Canvas renderer, sprite vector drawing, Web Audio API sound synthesis |
| `docs/plans/00-ROADMAP.md` | Modify | Update Milestone 001 status to COMPLETED |

---

## 3. Micro-Stepped Execution Groups

### Execution Group 1: Core Physics & Collision Engine (TDD)
- [x] **Step 1.1 (Red)**: Author `tests/test_game_engine.py` testing dinosaur jump physics, ducking hitbox reduction, AABB collision detection, and score scaling.
- [x] **Step 1.2 (Green)**: Implement `src/engine/physics.py` satisfying all test cases.
- [x] **Step 1.3 (Refactor)**: Verify clean test execution and zero syntax issues.

### Execution Group 2: Canvas Browser Frontend & Audio
- [x] **Step 2.1**: Author `public/index.html` and `public/style.css` with responsive canvas and retro aesthetic.
- [x] **Step 2.2**: Implement `public/game.js` with pixel dinosaur drawing, cactus & pterodactyl generation, cloud layer, audio synthesis via Web Audio API, keyboard & touch inputs.
- [x] **Step 2.3**: Implement `src/server.py` to serve the browser game on `http://127.0.0.1:8000`.

### Execution Group 3: Verification & SDLC Proof
- [x] **Step 3.1**: Run `make verify` in `dinosaur-game` to confirm 100% green tests and zero anti-shortcuts.
- [x] **Step 3.2**: Update roadmap status in `docs/plans/00-ROADMAP.md`.

---

## 4. Risk Matrix & Mitigations

| Risk | Severity | Mitigation Strategy |
| :--- | :--- | :--- |
| Audio playback blocked by browser autoplay policy | Low | Initialize AudioContext on first user keydown/tap |
| Canvas scaling blur on high-DPI (Retina) screens | Low | Scale canvas by `window.devicePixelRatio` with CSS dimensions |
| Collision false positives on cactus needles | Medium | Use inset collision boxes (tolerance padding) for forgiving arcade feel |

---

## 5. Proof of Correctness & Harness

- [x] **Command**: `make verify` exits code 0 with all checks passing.
- [x] **Unit Tests**: Full test suite passing in `tests/`.
- [x] **Browser Play**: Complete endless runner playable in any browser.
