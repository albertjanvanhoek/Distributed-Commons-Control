#!/usr/bin/env python3
"""Reproduce Experiment 11 effort-observability thresholds."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from distributed_commons.jam_effort_observability import (
    certified_required_effort_observability,
    maintenance_selection_margin,
    required_effort_observability,
)
from distributed_commons.jam_maintenance import JamMaintenanceState


def main() -> None:
    strong = JamMaintenanceState(
        validator_count=1023,
        adversarial_count=205,
        vulnerable_honest_count=82,
        no_show_prone_count=153,
        s_delta=2.0,
    )
    collapsed = JamMaintenanceState(
        validator_count=1023,
        adversarial_count=205,
        vulnerable_honest_count=400,
        no_show_prone_count=153,
        s_delta=2.0,
    )

    summary = {
        "verifier_dilemma_threshold": required_effort_observability(
            reward_budget=2.0,
            compute_cost=1.0,
            invalid_rate=0.001,
            exposure_probability=1.0,
            fault_loss=10.0,
        ),
        "insufficient_reward_budget_threshold":
            required_effort_observability(
                reward_budget=0.5,
                compute_cost=1.0,
                invalid_rate=0.001,
                exposure_probability=1.0,
                fault_loss=10.0,
            ),
        "zero_observability_margin_even_with_large_reward":
            maintenance_selection_margin(
                effort_observability=0.0,
                reward_budget=1000.0,
                compute_cost=1.0,
                invalid_rate=0.001,
                exposure_probability=1.0,
                fault_loss=10.0,
            ),
        "strong_structure_required_observability":
            certified_required_effort_observability(
                strong, 2.0, 1.0, 0.1, 10.0
            ),
        "collapsed_structure_required_observability":
            certified_required_effort_observability(
                collapsed, 2.0, 1.0, 0.1, 10.0
            ),
    }

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
