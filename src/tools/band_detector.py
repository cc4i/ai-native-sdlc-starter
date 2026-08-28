"""
Stage 6 Control Bands Anomaly Detector.
Evaluates time-series metrics against rolling statistical baselines (sigma deviations)
to close the SDLC loop between production observations and Stage 1 Intents.
"""

import math
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

class Tier(Enum):
    INSUFFICIENT_DATA = "insufficient_data"
    LOG = "log"
    DIAGNOSE = "diagnose"
    ACT = "act"

@dataclass
class BandResult:
    metric_name: str
    current_value: float
    mean: float
    stddev: float
    z_score: float
    tier: Tier
    action: str
    action_required: bool
    message: str

class BandDetector:
    """Statistical detector comparing metrics against rolling baselines."""

    def evaluate(
        self,
        current_value: float,
        baseline_points: List[float],
        metric_config: dict,
    ) -> BandResult:
        name = metric_config.get("name", "unnamed_metric")
        min_points = metric_config.get("min_baseline_points", 14)
        min_abs_change = metric_config.get("min_absolute_change", 0.0)
        direction = metric_config.get("direction", "increase")
        tier_3_action = metric_config.get("tier_3_action", "open_intent_pr")

        if len(baseline_points) < min_points:
            return BandResult(
                metric_name=name,
                current_value=current_value,
                mean=0.0,
                stddev=0.0,
                z_score=0.0,
                tier=Tier.INSUFFICIENT_DATA,
                action="none",
                action_required=False,
                message=f"Insufficient baseline points: have {len(baseline_points)}, require {min_points}.",
            )

        n = len(baseline_points)
        mean = sum(baseline_points) / n
        variance = sum((x - mean) ** 2 for x in baseline_points) / max(1, n - 1)
        stddev = math.sqrt(variance)

        # Delta calculation based on interest direction
        if direction == "increase":
            delta = current_value - mean
        elif direction == "decrease":
            delta = mean - current_value
        else:
            delta = abs(current_value - mean)

        # Check against minimum absolute change noise floor
        if delta <= 0 or delta < min_abs_change:
            return BandResult(
                metric_name=name,
                current_value=current_value,
                mean=mean,
                stddev=stddev,
                z_score=0.0,
                tier=Tier.LOG,
                action="log",
                action_required=False,
                message=f"Metric {name} variation ({delta:.2f}) within noise floor (< {min_abs_change}).",
            )

        # Z-score computation
        if stddev <= 1e-9:
            # Baseline is completely flat, any change above noise floor is a major deviation
            z_score = 10.0
        else:
            z_score = delta / stddev

        # Tier assignment
        if z_score >= 3.0:
            return BandResult(
                metric_name=name,
                current_value=current_value,
                mean=mean,
                stddev=stddev,
                z_score=z_score,
                tier=Tier.ACT,
                action=tier_3_action,
                action_required=True,
                message=f"CRITICAL BREACH: {name} value {current_value:.2f} is {z_score:.2f} sigma above baseline mean {mean:.2f}.",
            )
        elif z_score >= 2.0:
            return BandResult(
                metric_name=name,
                current_value=current_value,
                mean=mean,
                stddev=stddev,
                z_score=z_score,
                tier=Tier.DIAGNOSE,
                action="diagnose",
                action_required=False,
                message=f"ELEVATED: {name} value {current_value:.2f} is {z_score:.2f} sigma above baseline mean {mean:.2f}.",
            )
        else:
            return BandResult(
                metric_name=name,
                current_value=current_value,
                mean=mean,
                stddev=stddev,
                z_score=z_score,
                tier=Tier.LOG,
                action="log",
                action_required=False,
                message=f"NORMAL: {name} value {current_value:.2f} is within normal variation ({z_score:.2f} sigma).",
            )
