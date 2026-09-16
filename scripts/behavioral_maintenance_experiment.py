#!/usr/bin/env python3
"""Reproduce Experiment 8 behavioral-maintenance falsification boundaries."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from distributed_commons.behavioral_maintenance import (  # noqa: E402
    MaintenanceParameters,
    correction_multiplier,
    effective_corrective_gain,
    overcorrection_threshold,
    reinforcement_value_numerator,
    replacement_gap,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    p = MaintenanceParameters(
        decay=0.20,
        passive_renewal=0.05,
        viability_floor=0.80,
        target=1.0,
    )

    rows = []
    for i in range(21):
        gain = i / 10.0
        rows.append(
            {
                "gain": gain,
                "multiplier": correction_multiplier(p, gain),
                "stable": abs(correction_multiplier(p, gain)) < 1.0,
            }
        )

    summary = {
        "replacement_gap": replacement_gap(p),
        "overcorrection_threshold": overcorrection_threshold(p),
        "effective_gain_fidelity_0.4":
            effective_corrective_gain(1.0, 0.4),
        "effective_gain_fidelity_0.8":
            effective_corrective_gain(1.0, 0.8),
        "reinforcement_score_fidelity_0.4":
            reinforcement_value_numerator(0.5, 0.4, 1.0, 1.0),
        "reinforcement_score_fidelity_0.8":
            reinforcement_value_numerator(0.5, 0.8, 1.0, 1.0),
    }

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
