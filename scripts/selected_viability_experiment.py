#!/usr/bin/env python3
"""Reproduce Experiment 4: selected viability reversal."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from distributed_commons.selected_viability import (  # noqa: E402
    REVERSAL_THRESHOLD,
    critical_cost_ratio,
    direct_addition_contribution,
    induced_response_effect,
    one_selected_margin,
    selected_addition_contribution,
    two_frozen_margin,
    two_participant_effort,
    two_selected_margin,
)


def rows(b: float, epsilon: float) -> list[dict[str, float]]:
    output: list[dict[str, float]] = []
    for i in range(1, 100):
        z = i / 100.0
        output.append(
            {
                "z": z,
                "q2": two_participant_effort(z),
                "margin_one": one_selected_margin(b, epsilon, z),
                "margin_two_frozen": two_frozen_margin(
                    b, epsilon, z
                ),
                "margin_two_selected": two_selected_margin(
                    b, epsilon, z
                ),
                "direct_contribution": direct_addition_contribution(
                    b, epsilon, z
                ),
                "induced_response": induced_response_effect(
                    b, epsilon, z
                ),
                "selected_contribution": selected_addition_contribution(
                    b, epsilon, z
                ),
            }
        )
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--b", type=float, default=0.2)
    parser.add_argument("--safety-target", type=float, default=0.025)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = rows(args.b, args.safety_target)
    summary = {
        "reversal_threshold_z": REVERSAL_THRESHOLD,
        "critical_cost_ratio_at_x_0.10": critical_cost_ratio(0.10),
        "counterexample": {
            "b": 0.2,
            "epsilon": 0.025,
            "z": 0.9,
            "q2": two_participant_effort(0.9),
            "margin_one": one_selected_margin(0.2, 0.025, 0.9),
            "margin_two_frozen": two_frozen_margin(
                0.2, 0.025, 0.9
            ),
            "margin_two_selected": two_selected_margin(
                0.2, 0.025, 0.9
            ),
        },
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
