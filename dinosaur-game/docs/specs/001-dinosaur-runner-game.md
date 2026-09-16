# Spec: Endless Runner Dinosaur Browser Game

**Linked Intent**: [`docs/intent/001-dinosaur-runner-game.md`](../intent/001-dinosaur-runner-game.md)  
**Author**: Game Engine Architect  
**Date**: 2026-09-16  
**Status**: Validated  

---

## 1. Overview & Scope

A high-performance HTML5 Canvas endless runner browser game with offline capability, procedural obstacle generation, collision physics, and retro synthesized audio.

- **In Scope**:
  - T-Rex runner player (running, jumping, ducking, crashed states).
  - Physics system: velocity, gravity, jumping impulse, floor clamping.
  - Obstacles: Small cactus, large cactus, triple cactus, flying pterodactyl with wing flapping animation.
  - Precise Axis-Aligned Bounding Box (AABB) collision detection with sub-box tolerances.
  - Game state management: Start screen, Running, Game Over, and Restart.
  - Procedural backdrop: Moving ground line, craters, floating clouds, day/night theme transitions.
  - Sound effects synthesized with Web Audio API (`AudioContext`).
  - Score counter, speed multiplier progression, and high score storage.
  - Built-in static web server (`src/server.py`).

---

## 2. User Stories & Acceptance Criteria (Gherkin Scenarios)

### Story 1: Dinosaur Jump & Duck Physics
**As a** player,  
**I want** responsive jumping and ducking controls,  
**So that** I can leap over cacti and duck beneath low-flying pterodactyls.

#### Scenario 1.1: Jumping and gravity curve
```gherkin
Given a dinosaur running on the ground baseline (y = 0)
When the player presses Space, Up arrow, or taps the screen
Then a vertical upward impulse is applied (-vy)
And gravity gradually pulls the dinosaur back down to the ground baseline (y = 0)
And the dinosaur cannot jump again while mid-air
```

#### Scenario 1.2: Ducking hitbox reduction
```gherkin
Given a running dinosaur with normal height H and width W
When the player presses and holds the Down arrow key
Then the dinosaur enters the ducking state
And its effective bounding box height is reduced to duckHeight (< H)
And when released, it returns to normal running height
```

---

### Story 2: Collision Detection & Game Over
**As a** player,  
**I want** fair and precise collision detection,  
**So that** collisions trigger game over while near-misses allow survival.

#### Scenario 2.1: Collision with cactus obstacle
```gherkin
Given a dinosaur at position (x, y) with bounding box D
And a cactus obstacle at position (ox, oy) with bounding box O
When D intersects with O
Then a collision is detected
And the game state transitions to GAMEOVER
And the crash sound is played
```

#### Scenario 2.2: Ducking under high pterodactyl
```gherkin
Given a pterodactyl flying at height Y_HIGH
When the player is in the ducking state beneath it
Then their reduced bounding box does not intersect the pterodactyl
And no collision is triggered
```

---

### Story 3: Score Tracking & Speed Scaling
**As a** player,  
**I want** my score to increase with distance survived and the game to become progressively faster,  
**So that** the gameplay remains challenging and engaging.

#### Scenario 3.1: Score accumulation and speed progression
```gherkin
Given a running game with initial speed S0
When time advances by delta T
Then score increases proportionally to distance traveled
And every 100 points a milestone sound is played
And the obstacle scroll speed increases by a factor of acceleration
```

#### Scenario 3.2: High score persistence
```gherkin
Given a game session ending with score S
When S exceeds the stored high score in localStorage
Then the high score is updated to S
And subsequent game restarts display the new high score
```

---

## 3. Architecture & Interface Contracts

### 3.1 Core Engine Physics Model
```python
class Dinosaur:
    x: float
    y: float
    vy: float
    is_jumping: bool
    is_ducking: bool
    width: float
    height: float

def check_collision(box_a: tuple, box_b: tuple) -> bool:
    # AABB intersection check
    ...
```

### 3.2 Web Interface
- `public/index.html`: Canvas container (800x250) + score display.
- `public/game.js`: Game loop, rendering pipeline, Web Audio sound synthesis.
- `src/server.py`: Python `http.server` serving `public/` on configurable port.

---

## 4. Policy, Security & Quality Constraints

- Zero external network assets (no CDNs, no external font or image URLs).
- Zero dependencies outside Python standard library and browser DOM/Canvas APIs.
- Clean 60 FPS animation loop with `requestAnimationFrame`.

---

## 5. Adversarial Review & Sign-Off

- **Spec Gate Verdict**: PASSED
- **Sign-off**: Approved by @chuancc on 2026-09-16
- **Ready for Stage 3 (Build)**: `docs/plans/001-dinosaur-runner-game.md`
