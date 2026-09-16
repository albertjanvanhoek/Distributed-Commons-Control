#!/usr/bin/env python3
"""Run the first deterministic phase sweep and optionally save CSV output."""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import replace
from pathlib import Path
from statistics import fmean

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from distributed_commons import DynamicsParameters, simulate  # noqa: E402


def summarize(parameters: DynamicsParameters, steps: int, tail: int) -> dict[str, object]:
    records = simulate(parameters, steps)
    window = records[-min(tail, len(records)) :]
    return {
        "monitors": parameters.monitors,
        "correlation": parameters.correlation,
        "effort_cost": parameters.effort_cost,
        "mean_tail_health": fmean(r.commons_health for r in window),
        "mean_tail_effort": fmean(r.monitor_effort for r in window),
        "mean_tail_bad_attempt_rate": fmean(r.bad_attempt_rate for r in window),
        "mean_tail_bad_finalization": fmean(
            r.bad_finalization_probability for r in window
        ),
        "mean_tail_verification_debt": fmean(
            r.verification_debt for r in window
        ),
        "target_met_fraction": fmean(
            float(r.bad_finalization_probability <= parameters.safety_target)
            for r in window
        ),
        "structurally_attainable_fraction": fmean(
            float(r.structurally_attainable) for r in window
        ),
    }


def phase_sweep(steps: int = 300, tail: int = 75) -> list[dict[str, object]]:
    # A 3% target gives the sweep both target-met and target-missed regions;
    # it is an experimental threshold, not a claimed protocol constant.
    base = DynamicsParameters(safety_target=0.03)
    rows = []
    for monitors in (1, 3, 5):
        for correlation in (0.0, 0.05, 0.15, 0.30):
            for effort_cost in (0.25, 0.50, 1.0, 2.0):
                rows.append(
                    summarize(
                        replace(
                            base,
                            monitors=monitors,
                            correlation=correlation,
                            effort_cost=effort_cost,
                        ),
                        steps,
                        tail,
                    )
                )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=300)
    parser.add_argument("--tail", type=int, default=75)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    rows = phase_sweep(args.steps, args.tail)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)

    print(
        "monitors correlation cost mean_health mean_bad_finalization "
        "mean_debt target_met"
    )
    for row in rows:
        print(
            f"{row['monitors']:>8} {row['correlation']:>11.2f} "
            f"{row['effort_cost']:>4.2f} {row['mean_tail_health']:>11.4f} "
            f"{row['mean_tail_bad_finalization']:>21.5f} "
            f"{row['mean_tail_verification_debt']:>9.5f} "
            f"{row['target_met_fraction']:>10.2f}"
        )


if __name__ == "__main__":
    main()
