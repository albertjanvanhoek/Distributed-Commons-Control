#!/usr/bin/env python3
"""Reproduce Experiment 3: heterogeneous participant viability contribution."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from distributed_commons.viability import two_cause_example  # noqa: E402


def rows(rho: float, epsilon: float) -> list[dict[str, object]]:
    topology = two_cause_example(rho)
    coalitions = (
        frozenset(),
        frozenset({"A1"}),
        frozenset({"A2"}),
        frozenset({"B1"}),
        frozenset({"A1", "A2"}),
        frozenset({"A1", "B1"}),
        frozenset({"A2", "B1"}),
        frozenset({"A1", "A2", "B1"}),
    )
    shapley = topology.shapley_values(epsilon)
    dividends = topology.harsanyi_dividends(epsilon)
    output: list[dict[str, object]] = []
    for coalition in coalitions:
        output.append(
            {
                "coalition": ",".join(sorted(coalition)) or "empty",
                "escape_probability": topology.escape_probability(coalition),
                "viability_margin": topology.viability_margin(
                    coalition, epsilon
                ),
            }
        )

    output.append(
        {
            "coalition": "leave_one_out:B1",
            "escape_probability": None,
            "viability_margin": topology.leave_one_out_contribution(
                "B1", epsilon
            ),
        }
    )
    for participant, value in shapley.items():
        output.append(
            {
                "coalition": f"shapley:{participant}",
                "escape_probability": None,
                "viability_margin": value,
            }
        )
    for coalition, value in sorted(
        dividends.items(), key=lambda item: (len(item[0]), sorted(item[0]))
    ):
        if len(coalition) >= 2:
            output.append(
                {
                    "coalition": "interaction:"
                    + ",".join(sorted(coalition)),
                    "escape_probability": None,
                    "viability_margin": value,
                }
            )
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rho", type=float, default=0.05)
    parser.add_argument("--safety-target", type=float, default=0.001)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = rows(args.rho, args.safety_target)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(
                stream,
                fieldnames=(
                    "coalition",
                    "escape_probability",
                    "viability_margin",
                ),
            )
            writer.writeheader()
            writer.writerows(result)

    print(
        json.dumps(
            {
                "rho": args.rho,
                "safety_target": args.safety_target,
                "rows": result,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
