"""Experiment 11: effort observability and return-loop closure in JAM.

Experiment 10 leaves the external reward differential R_C-R_R unidentified.
The current Gray Paper suggests an effort-observation mechanism: validators may
vote on their impression of each other's auditing effort and a median may be
used by the staking layer.

This module does not assume that mechanism is fully specified or perfectly
implemented. Instead it introduces two explicit higher-layer parameters:

- s in [0,1]: effective discrimination/observability of real compute versus
  rubber-stamping;
- W >= 0: maximum reward differential available when the effort signal
  successfully distinguishes real maintenance.

Then the expected reward advantage is s*W.

Combining this with Experiment 10, the compute-selection margin is

    s*W + b*d*L_F - c.

Actual computation is selected against rubber-stamping iff the margin is
nonnegative.

This makes "reinforcement" a return-loop condition rather than a moral label:
the network must both observe maintenance and return enough value to cover the
private cost not already covered by fault deterrence.
"""

from __future__ import annotations

from math import isfinite

from .jam_behavior_selection import certified_exposure_lower_bound
from .jam_maintenance import JamMaintenanceState


def maintenance_selection_margin(
    effort_observability: float,
    reward_budget: float,
    compute_cost: float,
    invalid_rate: float,
    exposure_probability: float,
    fault_loss: float,
) -> float:
    s = float(effort_observability)
    w = float(reward_budget)
    c = float(compute_cost)
    b = float(invalid_rate)
    d = float(exposure_probability)
    loss = float(fault_loss)

    if not isfinite(s) or not 0.0 <= s <= 1.0:
        raise ValueError("effort_observability must lie in [0,1]")
    for name, value in (
        ("reward_budget", w),
        ("compute_cost", c),
        ("fault_loss", loss),
    ):
        if not isfinite(value) or value < 0.0:
            raise ValueError(f"{name} must be finite and nonnegative")
    for name, value in (
        ("invalid_rate", b),
        ("exposure_probability", d),
    ):
        if not isfinite(value) or not 0.0 <= value <= 1.0:
            raise ValueError(f"{name} must lie in [0,1]")

    return s * w + b * d * loss - c


def required_effort_observability(
    reward_budget: float,
    compute_cost: float,
    invalid_rate: float,
    exposure_probability: float,
    fault_loss: float,
) -> float:
    """Raw observability threshold for W>0.

    Values <=0 mean fault deterrence alone closes the gap.
    Values in (0,1] are feasible with sufficient effort observability.
    Values >1 mean even perfect effort observability cannot close the gap at
    the supplied reward budget.
    """

    w = float(reward_budget)
    if not isfinite(w) or w <= 0.0:
        raise ValueError("reward_budget must be finite and positive")

    c = float(compute_cost)
    b = float(invalid_rate)
    d = float(exposure_probability)
    loss = float(fault_loss)

    if not isfinite(c) or c < 0.0:
        raise ValueError("compute_cost must be finite and nonnegative")
    if not isfinite(b) or not 0.0 <= b <= 1.0:
        raise ValueError("invalid_rate must lie in [0,1]")
    if not isfinite(d) or not 0.0 <= d <= 1.0:
        raise ValueError("exposure_probability must lie in [0,1]")
    if not isfinite(loss) or loss < 0.0:
        raise ValueError("fault_loss must be finite and nonnegative")

    return (c - b * d * loss) / w


def effort_channel_can_close_gap(
    reward_budget: float,
    compute_cost: float,
    invalid_rate: float,
    exposure_probability: float,
    fault_loss: float,
) -> bool:
    return (
        required_effort_observability(
            reward_budget,
            compute_cost,
            invalid_rate,
            exposure_probability,
            fault_loss,
        )
        <= 1.0
    )


def certified_required_effort_observability(
    state: JamMaintenanceState,
    reward_budget: float,
    compute_cost: float,
    invalid_rate: float,
    fault_loss: float,
) -> float:
    return required_effort_observability(
        reward_budget,
        compute_cost,
        invalid_rate,
        certified_exposure_lower_bound(state),
        fault_loss,
    )
