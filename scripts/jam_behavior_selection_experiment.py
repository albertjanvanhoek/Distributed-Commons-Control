#!/usr/bin/env python3
"""Reproduce Experiment 10 partial JAM behavior-selection boundaries."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from distributed_commons.jam_behavior_selection import (
    certified_exposure_lower_bound,
    certified_required_reward_advantage_over_rubber,
    required_compute_reward_advantage_over_rubber,
)
from distributed_commons.jam_maintenance import JamMaintenanceState


def main() -> None:
    safe = JamMaintenanceState(
        validator_count=1023,
        adversarial_count=205,
        vulnerable_honest_count=82,
        no_show_prone_count=153,
        s_delta=2.0,
    )
    weak = JamMaintenanceState(
        validator_count=1023,
        adversarial_count=205,
        vulnerable_honest_count=300,
        no_show_prone_count=153,
        s_delta=2.0,
    )

    summary = {
        "verifier_dilemma_example": {
            "compute_cost": 1.0,
            "invalid_rate": 0.001,
            "exposure_probability": 1.0,
            "fault_loss": 10.0,
            "required_compute_reward_advantage":
                required_compute_reward_advantage_over_rubber(
                    1.0, 0.001, 1.0, 10.0
                ),
        },
        "safe_structure": {
            "attack_bound": safe.attack_bound,
            "certified_exposure_lower_bound":
                certified_exposure_lower_bound(safe),
            "required_reward_advantage_b_0.1_L_10":
                certified_required_reward_advantage_over_rubber(
                    safe, 1.0, 0.1, 10.0
                ),
        },
        "weaker_structure": {
            "attack_bound": weak.attack_bound,
            "certified_exposure_lower_bound":
                certified_exposure_lower_bound(weak),
            "required_reward_advantage_b_0.1_L_10":
                certified_required_reward_advantage_over_rubber(
                    weak, 1.0, 0.1, 10.0
                ),
        },
    }

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
