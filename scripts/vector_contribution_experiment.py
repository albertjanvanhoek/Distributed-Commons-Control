#!/usr/bin/env python3
"""Reproduce Experiment 7: opposite scalar signs from one contribution vector."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from distributed_commons.vector_contribution import (  # noqa: E402
    ContributionVector,
    opposite_sign_weight_witnesses,
)


def main() -> None:
    vector = ContributionVector({"loop_a": 0.2, "loop_b": -0.1})
    positive_weights, negative_weights = opposite_sign_weight_witnesses(
        0.2, -0.1
    )
    positive = vector.weighted(
        {"loop_a": positive_weights[0], "loop_b": positive_weights[1]}
    )
    negative = vector.weighted(
        {"loop_a": negative_weights[0], "loop_b": negative_weights[1]}
    )
    print(
        json.dumps(
            {
                "vector": dict(vector.values),
                "positive_weights": positive_weights,
                "positive_scalar": positive,
                "negative_weights": negative_weights,
                "negative_scalar": negative,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
