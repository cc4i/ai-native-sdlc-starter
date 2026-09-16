# Spec: Pause and Audio Mute Controls

**Linked Intent**: [`docs/intent/002-pause-and-audio-mute-controls.md`](../intent/002-pause-and-audio-mute-controls.md)  
**Author**: Game Engine Architect  
**Date**: 2026-09-16  
**Status**: Validated  

---

## 1. Overview & Scope

Enables players to freeze gameplay and resume at will, as well as toggle synthesized audio sound effects.

- **In Scope**:
  - `GameState` supports `PAUSED`.
  - Pause keybind: <kbd>P</kbd> or clicking the HUD Pause button.
  - Resume: Pressing <kbd>P</kbd>, <kbd>Space</kbd>, or clicking "RESUME".
  - Mute keybind: <kbd>M</kbd> or clicking the sound icon.
  - Mute state persistence via `localStorage.getItem('dino_muted')`.
  - Python core engine state testing for paused updates.

---

## 2. User Stories & Acceptance Criteria (Gherkin Scenarios)

### Story 1: Pausing and Resuming Gameplay
**As a** player running an active game session,  
**I want** to pause the game at any moment,  
**So that** I can attend to interruptions without losing my progress.

#### Scenario 1.1: Pausing freezes game updates
```gherkin
Given a running game with score S and dinosaur velocity VY
When the player presses "P" or clicks the pause button
Then the game transitions to PAUSED state
And a "PAUSED" overlay is displayed
And advancing time (dt) does not change score S, dinosaur y, or obstacle positions
```

#### Scenario 1.2: Resuming restores exact game state
```gherkin
Given a paused game session
When the player presses "P", "Space", or clicks "RESUME"
Then the game transitions back to RUNNING state
And physics and score accumulation continue from the exact paused coordinates
```

---

### Story 2: Muting and Unmuting Sound Effects
**As a** player in a quiet environment,  
**I want** to mute sound effects,  
**So that** I do not disturb others.

#### Scenario 2.1: Mute suppresses all audio synthesis
```gherkin
Given a sound system with muted set to true
When a jump, milestone, or crash event occurs
Then no audio oscillator is triggered
And no sound is output
```

#### Scenario 2.2: Mute preference persists across restarts
```gherkin
Given the user toggles mute to true
When the page is refreshed or a new game is started
Then the mute state remains true from localStorage
And the HUD reflects the muted icon
```

---

## 3. Architecture & Interface Contracts

### 3.1 Physics & Game State Contract
```python
class GameSession:
    is_paused: bool
    is_muted: bool
    dinosaur: Dinosaur
    obstacles: list

    def update(self, dt: float) -> None:
        if self.is_paused:
            return
        ...
```

---

## 4. Policy, Security & Quality Constraints

- Zero external sound files.
- Zero audio leaks when muted.

---

## 5. Adversarial Review & Sign-Off

- **Spec Gate Verdict**: PASSED
- **Sign-off**: Approved by @chuancc on 2026-09-16
- **Ready for Stage 3 (Build)**: `docs/plans/002-pause-and-audio-mute-controls.md`
