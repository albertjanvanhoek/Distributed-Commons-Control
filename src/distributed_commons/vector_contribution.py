"""Experiment 7: vector-valued participant contribution across viability loops.

Once several viability loops are declared, participant contribution is a vector

    Delta_i M = (Delta_i M_1, ..., Delta_i M_k).

A scalar "net contribution" exists only after an explicit weighting or utility
function is supplied. In particular, if a participant contributes positively
to one loop and negatively to another, positive weights can produce either a
positive or negative scalar total.

This module keeps that scalarization choice explicit.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Mapping


@dataclass(frozen=True)
class ContributionVector:
    values: Mapping[str, float]

    def __post_init__(self) -> None:
        if not self.values:
            raise ValueError("contribution vector must contain at least one loop")
        for name, value in self.values.items():
            if not name:
                raise ValueError("loop names must be nonempty")
            if not isfinite(value):
                raise ValueError("contribution values must be finite")

    def weighted(self, weights: Mapping[str, float]) -> float:
        if set(weights) != set(self.values):
            raise ValueError("weights must be supplied for exactly the declared loops")
        total = 0.0
        for name, value in self.values.items():
            weight = float(weights[name])
            if not isfinite(weight) or weight < 0.0:
                raise ValueError("weights must be finite and nonnegative")
            total += weight * value
        return total


def opposite_sign_weight_witnesses(
    positive_loop_value: float,
    negative_loop_value: float,
) -> tuple[tuple[float, float], tuple[float, float]]:
    """Positive weights producing positive and negative scalar totals.

    For a>0 and b<0:
      positive witness weights: (-2b, a), scalar = -a*b > 0
      negative witness weights: (-b, 2a), scalar = a*b < 0
    """

    a = float(positive_loop_value)
    b = float(negative_loop_value)
    if not isfinite(a) or not isfinite(b) or not a > 0.0 or not b < 0.0:
        raise ValueError("require a positive first-loop value and negative second-loop value")
    return ((-2.0 * b, a), (-b, 2.0 * a))
