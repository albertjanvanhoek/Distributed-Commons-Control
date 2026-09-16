#!/usr/bin/env python3
"""Reproduce the closed-loop commons experiments."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import asdict, replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from distributed_commons.closed_loop import (  # noqa: E402
    ClosedLoopParameters,
    basin_threshold,
    behavioural_equilibrium,
    bifurcation_curve,
    critical_baseline_funding,
    final_health,
    hysteresis_window,
)

KAPPAS = (0.0, 0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.5, 1.0, 1.2, 1.5)


def window_row(p: ClosedLoopParameters) -> dict[str, float | None]:
    w = hysteresis_window(p)
    return {
        "collapse_damage": None if w is None else w.collapse_damage,
        "fold_damage": None if w is None else w.fold_damage,
        "fold_health": None if w is None else w.fold_health,
        "ratio": None if w is None else w.ratio,
    }


def kappa_sweep(base: ClosedLoopParameters) -> list[dict[str, object]]:
    return [
        {
            "baseline_funding": k,
            **window_row(replace(base, baseline_funding=k)),
        }
        for k in KAPPAS
    ]


def robustness(base: ClosedLoopParameters) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    variations = {
        "correlation": (0.0, 0.05, 0.15, 0.30),
        "monitors": (1, 3, 5, 9),
        "effort_cost": (0.1, 0.25, 0.5, 1.0),
        "producer_temperature": (0.1, 0.25, 0.5, 1.0),
        "detection_penalty": (1.0, 1.8, 3.0),
    }
    for name, values in variations.items():
        for value in values:
            p = replace(base, **{name: value})
            rows.append(
                {
                    "parameter": name,
                    "value": value,
                    **window_row(p),
                }
            )
    return rows


def full_model_check(base: ClosedLoopParameters) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for kappa in (0.0, 0.05, 0.2):
        p0 = replace(base, baseline_funding=kappa)
        w = hysteresis_window(p0)
        assert w is not None
        regimes = (
            ("below_window", 0.5 * w.collapse_damage),
            (
                "inside_window",
                0.5 * (w.collapse_damage + w.fold_damage),
            ),
            ("above_fold", 1.2 * w.fold_damage),
        )
        for label, damage in regimes:
            p = replace(p0, damage=damage)
            b_collapsed = behavioural_equilibrium(
                0.0, p
            ).bad_attempt_rate
            rows.append(
                {
                    "baseline_funding": kappa,
                    "regime": label,
                    "damage": damage,
                    "final_health_from_healthy": final_health(
                        p,
                        initial_health=1.0,
                        initial_bad_attempt_rate=0.2,
                    ),
                    "final_health_from_collapsed": final_health(
                        p,
                        initial_health=0.0,
                        initial_bad_attempt_rate=b_collapsed,
                    ),
                }
            )
    return rows


def basin_table(base: ClosedLoopParameters) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for kappa in (0.0, 0.05):
        p0 = replace(base, baseline_funding=kappa)
        w = hysteresis_window(p0)
        assert w is not None
        p = replace(
            p0,
            damage=0.5 * (w.collapse_damage + w.fold_damage),
        )
        threshold_branch = [
            x
            for x, damage, stable in bifurcation_curve(p, 2000)
            if not stable and damage <= p.damage
        ]
        reduced = threshold_branch[-1]
        for b0 in (0.02, 0.05, 0.1, 0.2, 0.4, 0.6, 0.8, 0.95):
            rows.append(
                {
                    "baseline_funding": kappa,
                    "damage": p.damage,
                    "reduced_threshold": reduced,
                    "initial_bad_attempt_rate": b0,
                    "full_model_threshold": basin_threshold(p, b0),
                }
            )
    return rows


def alternative_closures() -> list[dict[str, object]]:
    """Test the fold under two non-reward return paths."""

    cases = {
        "reward_funding": ClosedLoopParameters(
            baseline_funding=0.05,
        ),
        "checking_cost": ClosedLoopParameters(
            baseline_funding=1.0,
            reward_health_weight=0.0,
            cost_stress=3.0,
        ),
        "capture_gain": ClosedLoopParameters(
            baseline_funding=1.0,
            reward_health_weight=0.0,
            capture_stress=1.2,
        ),
    }
    rows: list[dict[str, object]] = []
    for name, p0 in cases.items():
        w = hysteresis_window(p0)
        assert w is not None
        damage = 0.5 * (w.collapse_damage + w.fold_damage)
        p = replace(p0, damage=damage)
        b_collapsed = behavioural_equilibrium(
            0.0, p
        ).bad_attempt_rate
        rows.append(
            {
                "closure": name,
                "collapse_damage": w.collapse_damage,
                "fold_damage": w.fold_damage,
                "fold_health": w.fold_health,
                "ratio": w.ratio,
                "inside_damage": damage,
                "final_health_from_healthy": final_health(
                    p,
                    initial_health=1.0,
                    initial_bad_attempt_rate=0.2,
                ),
                "final_health_from_collapsed": final_health(
                    p,
                    initial_health=0.0,
                    initial_bad_attempt_rate=b_collapsed,
                ),
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()

    base = ClosedLoopParameters()
    results = {
        "critical_baseline_funding": critical_baseline_funding(base),
        "kappa_sweep": kappa_sweep(base),
        "robustness_kappa_0.05": robustness(
            replace(base, baseline_funding=0.05)
        ),
        "full_model_check": full_model_check(base),
        "basin": basin_table(base),
        "alternative_closures": alternative_closures(),
    }

    if args.output_dir:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        for key, rows in results.items():
            if isinstance(rows, list):
                with (
                    args.output_dir / f"closed_loop_{key}.csv"
                ).open("w", newline="", encoding="utf-8") as stream:
                    writer = csv.DictWriter(
                        stream, fieldnames=list(rows[0])
                    )
                    writer.writeheader()
                    writer.writerows(rows)

        curves: list[dict[str, object]] = []
        for kappa in (0.0, 0.05, 0.2, 0.5):
            p = replace(base, baseline_funding=kappa)
            for x, damage, stable in bifurcation_curve(p, 400):
                curves.append(
                    {
                        "baseline_funding": kappa,
                        "health": x,
                        "damage": damage,
                        "stable": stable,
                    }
                )
        with (
            args.output_dir / "closed_loop_bifurcation.csv"
        ).open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(
                stream, fieldnames=list(curves[0])
            )
            writer.writeheader()
            writer.writerows(curves)

    print(json.dumps({"parameters": asdict(base), **results}, indent=1))


if __name__ == "__main__":
    main()
