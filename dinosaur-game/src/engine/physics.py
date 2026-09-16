"""
Dinosaur Runner Game core physics, AABB collision detection, and score progression.
"""

from enum import Enum
from typing import Any, Dict


class ObstacleType(Enum):
    CACTUS_SMALL = "cactus_small"
    CACTUS_LARGE = "cactus_large"
    PTERODACTYL_HIGH = "pterodactyl_high"
    PTERODACTYL_LOW = "pterodactyl_low"


class Dinosaur:
    """Represents the player dinosaur character and its physical state."""

    def __init__(self, ground_y: float = 0.0):
        self.ground_y = ground_y
        self.x = 50.0
        self.y = ground_y
        self.vy = 0.0
        self.width = 40.0
        self.height = 44.0
        self.duck_height = 26.0
        self.is_jumping = False
        self.is_ducking = False

        # Physical constants
        self.jump_velocity = 450.0  # pixels/sec
        self.gravity = 1400.0  # pixels/sec^2

    def jump(self) -> bool:
        """Triggers a jump if the dinosaur is currently grounded."""
        if not self.is_jumping:
            self.is_jumping = True
            self.is_ducking = False
            self.vy = self.jump_velocity
            return True
        return False

    def duck(self, state: bool) -> None:
        """Sets the ducking state of the dinosaur. Airborne ducking applies fast-drop."""
        if self.is_jumping:
            if state and self.vy > -800.0:
                self.vy -= 600.0  # Fast-drop downwards
            self.is_ducking = False
        else:
            self.is_ducking = state

    def update(self, dt: float) -> None:
        """Advances physics by delta time (in seconds)."""
        if self.is_jumping:
            self.y += self.vy * dt
            self.vy -= self.gravity * dt

            if self.y <= self.ground_y:
                self.y = self.ground_y
                self.vy = 0.0
                self.is_jumping = False

    def get_hitbox(self) -> Dict[str, float]:
        """Returns the current Axis-Aligned Bounding Box (AABB)."""
        current_h = self.duck_height if self.is_ducking else self.height
        return {
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": current_h,
        }


class Obstacle:
    """Represents an obstacle on the running track."""

    def __init__(
        self,
        obstacle_type: ObstacleType,
        x: float,
        y: float,
        width: float,
        height: float,
    ):
        self.type = obstacle_type
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def get_hitbox(self) -> Dict[str, float]:
        """Returns the obstacle bounding box."""
        return {
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
        }


def check_collision(box_a: Dict[str, Any], box_b: Dict[str, Any]) -> bool:
    """
    Evaluates Axis-Aligned Bounding Box (AABB) intersection between two rectangles.
    box format: {'x': float, 'y': float, 'width': float, 'height': float}
    """
    a_left = box_a["x"]
    a_right = box_a["x"] + box_a["width"]
    a_bottom = box_a["y"]
    a_top = box_a["y"] + box_a["height"]

    b_left = box_b["x"]
    b_right = box_b["x"] + box_b["width"]
    b_bottom = box_b["y"]
    b_top = box_b["y"] + box_b["height"]

    # In AABB, separation along ANY axis implies NO collision
    if a_right <= b_left or a_left >= b_right:
        return False
    if a_top <= b_bottom or a_bottom >= b_top:
        return False

    return True


def update_game_speed(base_speed: float, score: int) -> float:
    """
    Calculates current scroll speed based on base speed and accumulated score.
    Capped at maximum of 16.0 to preserve playable reaction windows.
    """
    speed_increase = min(10.0, score * 0.0035)
    return base_speed + speed_increase


def calculate_score(distance_traveled: float) -> int:
    """Calculates integer score based on distance traveled."""
    return int(distance_traveled * 0.1)


def calculate_min_safe_gap(speed: float) -> float:
    """
    Computes minimum safe gap in pixels between consecutive obstacles.
    Guarantees a lower bound of 140.0px to respect landing physics.
    Scales with speed to allow human reaction time.
    """
    dynamic_gap = speed * 0.45
    return max(140.0, dynamic_gap)


class GameSession:
    """Manages full game session lifecycle, including pause and mute states."""

    def __init__(self, base_speed: float = 360.0):
        self.dinosaur = Dinosaur(ground_y=0.0)
        self.obstacles: list[Obstacle] = []
        self.base_speed = base_speed
        self.distance_traveled = 0.0
        self.score = 0
        self.is_paused = False
        self.is_muted = False
        self.is_game_over = False

    def toggle_pause(self) -> bool:
        """Toggles paused state."""
        self.is_paused = not self.is_paused
        return self.is_paused

    def toggle_mute(self) -> bool:
        """Toggles sound effects mute state."""
        self.is_muted = not self.is_muted
        return self.is_muted

    def update(self, dt: float) -> None:
        """Advances session simulation if not paused and not game over."""
        if self.is_paused or self.is_game_over:
            return

        current_speed = update_game_speed(self.base_speed, self.score)
        self.distance_traveled += current_speed * dt
        self.score = calculate_score(self.distance_traveled)
        self.dinosaur.update(dt)
