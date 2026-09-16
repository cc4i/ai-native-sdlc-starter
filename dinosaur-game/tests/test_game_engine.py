"""
Unit tests for Dinosaur Runner Game core physics, collision detection, and score progression.
"""

import unittest

from src.engine.physics import (
    Dinosaur,
    GameSession,
    Obstacle,
    ObstacleType,
    calculate_min_safe_gap,
    calculate_score,
    check_collision,
    update_game_speed,
)


class TestDinosaurPhysics(unittest.TestCase):
    def setUp(self):
        self.dino = Dinosaur(ground_y=0.0)

    def test_dinosaur_initial_state(self):
        self.assertEqual(self.dino.y, 0.0)
        self.assertFalse(self.dino.is_jumping)
        self.assertFalse(self.dino.is_ducking)
        self.assertEqual(self.dino.height, 44.0)
        self.assertEqual(self.dino.width, 40.0)

    def test_dinosaur_jump_and_gravity(self):
        self.dino.jump()
        self.assertTrue(self.dino.is_jumping)
        self.assertGreater(self.dino.vy, 0)

        # Cannot jump while already jumping
        initial_vy = self.dino.vy
        self.dino.jump()
        self.assertEqual(self.dino.vy, initial_vy)

        # Advance physics until landing
        dt = 0.016  # ~60 fps
        max_steps = 200
        landed = False
        for _ in range(max_steps):
            self.dino.update(dt)
            if not self.dino.is_jumping and self.dino.y == 0.0:
                landed = True
                break

        self.assertTrue(landed, "Dinosaur should return to ground baseline")
        self.assertFalse(self.dino.is_jumping)

    def test_dinosaur_ducking(self):
        normal_h = self.dino.height
        self.dino.duck(True)
        self.assertTrue(self.dino.is_ducking)
        self.assertLess(self.dino.get_hitbox()["height"], normal_h)

        self.dino.duck(False)
        self.assertFalse(self.dino.is_ducking)
        self.assertEqual(self.dino.get_hitbox()["height"], normal_h)

    def test_jumping_cancels_ducking_state(self):
        self.dino.duck(True)
        self.assertTrue(self.dino.is_ducking)

        # Jumping while ducking must clear the ducking flag
        self.dino.jump()
        self.assertTrue(self.dino.is_jumping)
        self.assertFalse(self.dino.is_ducking, "Dinosaur must not be ducking while jumping")
        self.assertEqual(
            self.dino.get_hitbox()["height"],
            self.dino.height,
            "Jumping dinosaur must use full standing hitbox",
        )


class TestCollisionDetection(unittest.TestCase):
    def test_aabb_collision(self):
        # Overlapping boxes
        box_a = {"x": 50, "y": 0, "width": 40, "height": 44}
        box_b = {"x": 70, "y": 0, "width": 25, "height": 40}
        self.assertTrue(check_collision(box_a, box_b))

        # Separated horizontally
        box_c = {"x": 150, "y": 0, "width": 25, "height": 40}
        self.assertFalse(check_collision(box_a, box_c))

        # Separated vertically
        box_d = {"x": 50, "y": 60, "width": 40, "height": 30}
        self.assertFalse(check_collision(box_a, box_d))

    def test_duck_avoids_flying_obstacle(self):
        dino = Dinosaur(ground_y=0.0)
        # High pterodactyl flying at y=32 with height 24 (y span: 32 to 56)
        pterodactyl = Obstacle(ObstacleType.PTERODACTYL_HIGH, x=50, y=32, width=40, height=24)

        # When standing (height 44: span 0 to 44), dinosaur intersects the pterodactyl
        self.assertTrue(
            check_collision(dino.get_hitbox(), pterodactyl.get_hitbox()),
            "Standing dinosaur should collide with high pterodactyl",
        )

        # When ducking (height 26: span 0 to 26), dinosaur ducks under it!
        dino.duck(True)
        self.assertFalse(
            check_collision(dino.get_hitbox(), pterodactyl.get_hitbox()),
            "Ducking dinosaur should pass safely under high pterodactyl",
        )


class TestGameProgression(unittest.TestCase):
    def test_speed_scaling(self):
        initial_speed = 6.0
        speed_at_0 = update_game_speed(base_speed=initial_speed, score=0)
        self.assertEqual(speed_at_0, initial_speed)

        speed_at_500 = update_game_speed(base_speed=initial_speed, score=500)
        self.assertGreater(speed_at_500, initial_speed)

        speed_at_2000 = update_game_speed(base_speed=initial_speed, score=2000)
        self.assertGreater(speed_at_2000, speed_at_500)
        # Verify speed doesn't exceed reasonable maximum cap
        self.assertLessEqual(speed_at_2000, 16.0)

    def test_score_calculation(self):
        # 100 meters traveled with speed factor
        score = calculate_score(distance_traveled=100.0)
        self.assertEqual(score, 10)

    def test_min_safe_obstacle_spacing(self):
        # Even at varying speeds (from base 360 to max 680 px/s), minimum gap must be >= 140px
        for test_speed in [200.0, 360.0, 500.0, 680.0]:
            min_gap = calculate_min_safe_gap(speed=test_speed)
            self.assertGreaterEqual(
                min_gap,
                140.0,
                f"Minimum safe gap at speed {test_speed} was {min_gap}, expected >= 140.0px",
            )


class TestGameSession(unittest.TestCase):
    def test_session_pause_freezes_state(self):
        session = GameSession()
        self.assertFalse(session.is_paused)
        self.assertFalse(session.is_muted)

        # Start jumping
        session.dinosaur.jump()
        self.assertTrue(session.dinosaur.is_jumping)
        session.update(0.1)
        y_before = session.dinosaur.y
        dist_before = session.distance_traveled

        # Pause session
        session.toggle_pause()
        self.assertTrue(session.is_paused)

        # Update while paused must NOT change dinosaur position or score
        session.update(0.5)
        self.assertEqual(session.dinosaur.y, y_before)
        self.assertEqual(session.distance_traveled, dist_before)

        # Unpause
        session.toggle_pause()
        self.assertFalse(session.is_paused)
        session.update(0.1)
        self.assertNotEqual(session.distance_traveled, dist_before)

    def test_session_mute_toggle(self):
        session = GameSession()
        self.assertFalse(session.is_muted)
        session.toggle_mute()
        self.assertTrue(session.is_muted)
        session.toggle_mute()
        self.assertFalse(session.is_muted)


if __name__ == "__main__":
    unittest.main()
