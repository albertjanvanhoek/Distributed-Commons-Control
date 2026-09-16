#!/usr/bin/env python3
"""Reproduce Experiment 6: state-dependent participant contribution."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from distributed_commons.corrective_capacity import CapacityParameters  # noqa: E402
from distributed_commons.state_dependent_contribution import (  # noqa: E402
    certified_participant_contribution,
    expected_participant_contribution,
)
from distributed_commons.viability import two_cause_example  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rho", type=float, default=0.05)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    topology = two_cause_example(args.rho)
    p = CapacityParameters()

    rows = []
    for i in range(11):
        capacity = i / 10.0
        rows.append(
            {
                "capacity": capacity,
                "expected_B1_contribution":
                    expected_participant_contribution(
                        topology,
                        "B1",
                        {"A1", "A2"},
                        1.0,
                        capacity,
                        p,
                    ),
                "certified_B1_contribution_target_0.01":
                    certified_participant_contribution(
                        topology,
                        "B1",
                        {"A1", "A2"},
                        1.0,
                        capacity,
                        0.01,
                        p,
                    ),
            }
        )

    summary = {
        "rho": args.rho,
        "expected_contribution_at_C_0.5":
            expected_participant_contribution(
                topology, "B1", {"A1", "A2"}, 1.0, 0.5, p
            ),
        "certified_contribution_at_C_0.5_target_0.01":
            certified_participant_contribution(
                topology,
                "B1",
                {"A1", "A2"},
                1.0,
                0.5,
                0.01,
                p,
            ),
    }

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(
                stream, fieldnames=list(rows[0])
            )
            writer.writeheader()
            writer.writerows(rows)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
