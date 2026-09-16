#!/usr/bin/env python3
"""Reproduce Experiment 12 fungal flow-maintenance cases."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from distributed_commons.fungal_flow_maintenance import (
    FungalFlowParameters,
    iterate_route_share,
    simulate_parameter_cases,
    symmetric_locally_stable,
    symmetric_multiplier,
    worst_case_backup_share,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    cases = [
        ("sublinear", FungalFlowParameters(0.8, 0.5, 1.0)),
        ("neutral", FungalFlowParameters(1.0, 0.5, 1.0)),
        ("superlinear", FungalFlowParameters(1.3, 0.5, 1.0)),
        ("attenuated", FungalFlowParameters(1.3, 0.5, 0.6)),
    ]

    summary = simulate_parameter_cases(cases, z0=0.51, steps=30)

    rows = []
    for name, params in cases:
        trajectory = iterate_route_share(0.51, params, 30)
        for t, z in enumerate(trajectory):
            rows.append(
                {
                    "case": name,
                    "step": t,
                    "beta": params.beta,
                    "sensitivity": params.sensitivity,
                    "adjustment": params.adjustment,
                    "effective_gain": params.beta * params.sensitivity,
                    "multiplier": symmetric_multiplier(params),
                    "locally_stable": symmetric_locally_stable(params),
                    "route1_share": z,
                    "backup_share": worst_case_backup_share(z),
                }
            )

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
