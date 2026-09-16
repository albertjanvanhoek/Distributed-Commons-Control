#!/usr/bin/env python3
"""Reproduce Experiment 5: quiet capacity erosion at unchanged shared state."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from distributed_commons.corrective_capacity import (  # noqa: E402
    CapacityParameters,
    local_shared_state_multiplier,
    quiet_trajectory,
    required_maintenance_for_capacity,
    shock_margin,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=40)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    p = CapacityParameters()
    rows = quiet_trajectory(1.0, 0.5, p, steps=args.steps)

    result = [
        {
            "round": t,
            "shared_state": x,
            "capacity": c,
            "shock_margin": margin,
        }
        for t, x, c, margin in rows
    ]

    summary = {
        "parameters": {
            "regeneration": p.regeneration,
            "capacity_decay": p.capacity_decay,
            "correction_efficiency": p.correction_efficiency,
            "viability_floor": p.viability_floor,
        },
        "local_shared_state_multiplier": local_shared_state_multiplier(p),
        "initial_margin": shock_margin(1.0, 0.5, p),
        "final_margin": rows[-1][3],
        "stationary_maintenance_for_C_0.5":
            required_maintenance_for_capacity(0.5, p),
    }

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(
                stream, fieldnames=list(result[0])
            )
            writer.writeheader()
            writer.writerows(result)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
