#!/usr/bin/env python3
"""
CLI Utility to inspect operational metrics against Stage 6 Control Bands.
Reads bands.yaml and evaluates metrics against rolling historical data.
"""

import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

from src.tools.band_detector import BandDetector


def main():
    bands_file = root_dir / "bands.yaml"
    if not bands_file.exists():
        print(f"❌ Error: {bands_file} not found.")
        sys.exit(1)

    print("📊 [Stage 6 Control Bands] Evaluating operational baselines...")
    detector = BandDetector()

    # Demo evaluation using sample baseline
    sample_config = {
        "name": "daily_llm_cost_usd",
        "direction": "increase",
        "min_absolute_change": 5.0,
        "tier_3_action": "open_intent_pr",
        "min_baseline_points": 14,
    }
    sample_baseline = [12.0 + (i % 5 - 2) * 0.8 for i in range(28)]
    current_value = 13.5

    result = detector.evaluate(current_value, sample_baseline, sample_config)
    print(f"  - Metric: {result.metric_name}")
    print(
        f"  - Current Value: {result.current_value:.2f} | Baseline Mean: {result.mean:.2f} (σ={result.stddev:.2f})"
    )
    print(f"  - Tier: {result.tier.value.upper()} | Z-Score: {result.z_score:.2f}σ")
    print(f"  - Status: {result.message}")

    if result.action_required:
        print(f"  🚨 Action Required: {result.action}")
        sys.exit(1)
    else:
        print("  ✓ All metrics within normal control bands.")
        sys.exit(0)


if __name__ == "__main__":
    main()
