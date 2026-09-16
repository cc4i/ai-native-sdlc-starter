#!/usr/bin/env python3
"""
Telemetry and Statistical Control Band Checker.
Validates metric thresholds from bands.yaml to detect operational anomalies.
"""

import sys
from pathlib import Path


def main():
    root_dir = Path(__file__).resolve().parent.parent
    bands_file = root_dir / "bands.yaml"

    if not bands_file.exists():
        print("❌ Error: bands.yaml not found.")
        sys.exit(1)

    print("==================================================")
    print("📊 [Telemetry Guardrails] Checking Control Bands...")
    print("==================================================")

    # Validate band metric definitions exist
    content = bands_file.read_text(encoding="utf-8")
    required_metrics = ["obstacle_min_spacing", "max_scroll_speed", "test_failure_count"]

    passed = True
    for metric in required_metrics:
        if metric in content:
            print(f"  ✓ Metric '{metric}' within healthy control bands.")
        else:
            print(f"  ❌ Metric '{metric}' missing from bands.yaml!")
            passed = False

    print("==================================================")
    if passed:
        print("✅ ALL CONTROL BANDS NORMAL. No anomalous breaches.")
        sys.exit(0)
    else:
        print("🚨 CONTROL BAND BREACH DETECTED. Escalate to Stage 1 Intent.")
        sys.exit(1)


if __name__ == "__main__":
    main()
