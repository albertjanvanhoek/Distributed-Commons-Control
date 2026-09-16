#!/usr/bin/env python3
"""Reproduce Experiment 9 JAM maintenance-operator perturbations."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from distributed_commons.jam_maintenance import (  # noqa: E402
    JamMaintenanceState,
    escalation_vector_change,
    one_validator_correction_gain,
    one_validator_scalability_gain,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    rows = []

    crossing = JamMaintenanceState(
        validator_count=1023,
        adversarial_count=205,
        vulnerable_honest_count=119,
        no_show_prone_count=153,
        s0=30.0,
        s_delta=2.0,
        collateral_share=0.05,
    )
    crossing_after = crossing.diversify_one_honest_validator()

    baseline = JamMaintenanceState(
        validator_count=1023,
        adversarial_count=205,
        vulnerable_honest_count=82,
        no_show_prone_count=153,
        s0=30.0,
        s_delta=2.0,
        collateral_share=0.05,
    )

    for s_delta in (1.8, 1.9, 2.0, 2.08, 2.2):
        state = baseline.with_escalation(s_delta)
        rows.append(
            {
                "s_delta": s_delta,
                "lambda_correction": state.correction_reproduction,
                "attack_bound": state.attack_bound,
                "safety_log_margin": state.safety_log_margin,
                "scalability_margin": state.scalability_margin,
            }
        )

    d_safety, d_scale = escalation_vector_change(baseline, 2.08)

    summary = {
        "one_validator_exact_step": baseline.s_delta
        / baseline.validator_count,
        "one_validator_correction_gain":
            one_validator_correction_gain(crossing),
        "one_validator_scalability_gain":
            one_validator_scalability_gain(baseline),
        "certification_crossing": {
            "before_vulnerable_count": 119,
            "before_safety_log_margin": crossing.safety_log_margin,
            "after_vulnerable_count": 118,
            "after_safety_log_margin": crossing_after.safety_log_margin,
        },
        "escalation_2_to_2_08": {
            "delta_safety_log_margin": d_safety,
            "delta_scalability_margin": d_scale,
        },
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
