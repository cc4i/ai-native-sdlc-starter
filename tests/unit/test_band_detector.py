"""
Unit tests for Stage 6 Control Bands Anomaly Detector.
"""

import unittest

from src.tools.band_detector import BandDetector, Tier


class TestBandDetector(unittest.TestCase):
    def setUp(self):
        self.detector = BandDetector()
        self.metric_config = {
            "name": "daily_llm_cost_usd",
            "direction": "increase",
            "min_absolute_change": 5.0,
            "tier_3_action": "open_intent_pr",
            "min_baseline_points": 14,
        }

    def test_insufficient_baseline_data(self):
        # Only 5 baseline points, but 14 required
        baseline = [10.0, 11.0, 10.5, 9.8, 10.2]
        result = self.detector.evaluate(
            current_value=15.0, baseline_points=baseline, metric_config=self.metric_config
        )
        self.assertEqual(result.tier, Tier.INSUFFICIENT_DATA)
        self.assertFalse(result.action_required)

    def test_normal_variation_returns_log_tier(self):
        # 14 points around 10.0 with stddev ~ 1.0
        baseline = [10.0 + (i % 3 - 1) * 0.5 for i in range(14)]
        result = self.detector.evaluate(
            current_value=10.5, baseline_points=baseline, metric_config=self.metric_config
        )
        self.assertEqual(result.tier, Tier.LOG)
        self.assertFalse(result.action_required)

    def test_below_min_absolute_change_stays_log_tier(self):
        # Flat baseline of 1.0, current = 3.0 (increase = 2.0 < min_absolute_change 5.0)
        baseline = [1.0] * 14
        result = self.detector.evaluate(
            current_value=3.0, baseline_points=baseline, metric_config=self.metric_config
        )
        self.assertEqual(result.tier, Tier.LOG)
        self.assertFalse(result.action_required)

    def test_moderate_deviation_returns_diagnose_tier(self):
        # Mean = 10.0, stddev ~ 0.462. For z ~ 2.5 sigma, delta ~ 1.15 -> current = 11.15
        config = dict(self.metric_config, min_absolute_change=1.0)
        baseline = [9.0, 11.0, 10.0, 10.0, 9.5, 10.5, 9.8, 10.2, 9.7, 10.3, 10.1, 9.9, 10.0, 10.0]
        result = self.detector.evaluate(
            current_value=11.15, baseline_points=baseline, metric_config=config
        )
        self.assertEqual(result.tier, Tier.DIAGNOSE)
        self.assertEqual(result.action, "diagnose")

    def test_critical_spike_returns_act_tier(self):
        # Mean = 10.0, stddev ~ 1.0. Current = 25.0 (delta = 15.0, z > 10.0 sigma)
        baseline = [9.0, 11.0, 10.0, 10.0, 9.5, 10.5, 9.8, 10.2, 9.7, 10.3, 10.1, 9.9, 10.0, 10.0]
        result = self.detector.evaluate(
            current_value=25.0, baseline_points=baseline, metric_config=self.metric_config
        )
        self.assertEqual(result.tier, Tier.ACT)
        self.assertTrue(result.action_required)
        self.assertEqual(result.action, "open_intent_pr")


if __name__ == "__main__":
    unittest.main()
