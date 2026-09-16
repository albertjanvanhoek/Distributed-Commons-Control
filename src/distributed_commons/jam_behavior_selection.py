"""Experiment 10: partially identified JAM audit-behavior selection.

The current Gray Paper identifies the structure of the audit incentive problem
but does not close the numerical payoff model inside JAM core:
- auditing effort is not directly tracked on-chain;
- validators may vote on their impression of each other's effort;
- the chain itself does not issue validator rewards;
- faults/culprits can be recorded for punishment by a higher-level system.

We therefore model only the payoff differences that the grounded architecture
supports, leaving external reward and penalty magnitudes as parameters.

Actions after an audit announcement:
- C: compute/re-execute and issue the corresponding judgment;
- R: rubber-stamp a positive judgment without doing the full computation;
- N: no-show after announcement.

Let:
- c > 0 be compute cost;
- R_C, R_R, R_N be expected external reward/effort-score values;
- b be the probability/opportunity rate that the audited report is invalid;
- d be the probability a false positive judgment is exposed and finalized
  against the rubber-stamper;
- L_F be the external loss imposed for such a fault.

Then

    U_C = R_C - c
    U_R = R_R - b*d*L_F
    U_N = R_N.

Compute is privately selected iff it weakly dominates both alternatives:

    R_C - R_R + b*d*L_F >= c
    R_C - R_N >= c.

This creates two exact incentive gaps that the delegated staking/economic layer
must close. No specific JAM reward amount is invented here.

A certified exposure lower bound can be derived from the ELVES acceptance
bound: if P_accept <= P_bound, then exposure/rejection probability is at least
1-P_bound under the declared attack model. Using d_cert = 1-P_bound gives a
conservative sufficient compute-selection condition.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from .jam_maintenance import JamMaintenanceState


@dataclass(frozen=True)
class AuditBehaviorPayoffs:
    compute_cost: float
    reward_compute: float
    reward_rubber_stamp: float
    reward_no_show: float
    invalid_rate: float
    exposure_probability: float
    fault_loss: float

    def __post_init__(self) -> None:
        for name, value in (
            ("compute_cost", self.compute_cost),
            ("fault_loss", self.fault_loss),
        ):
            if not isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")

        for name, value in (
            ("invalid_rate", self.invalid_rate),
            ("exposure_probability", self.exposure_probability),
        ):
            if not isfinite(value) or not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must lie in [0,1]")

        for name, value in (
            ("reward_compute", self.reward_compute),
            ("reward_rubber_stamp", self.reward_rubber_stamp),
            ("reward_no_show", self.reward_no_show),
        ):
            if not isfinite(value):
                raise ValueError(f"{name} must be finite")

    @property
    def utility_compute(self) -> float:
        return self.reward_compute - self.compute_cost

    @property
    def utility_rubber_stamp(self) -> float:
        return (
            self.reward_rubber_stamp
            - self.invalid_rate
            * self.exposure_probability
            * self.fault_loss
        )

    @property
    def utility_no_show(self) -> float:
        return self.reward_no_show

    @property
    def compute_vs_rubber_margin(self) -> float:
        return self.utility_compute - self.utility_rubber_stamp

    @property
    def compute_vs_no_show_margin(self) -> float:
        return self.utility_compute - self.utility_no_show

    @property
    def compute_selected(self) -> bool:
        return (
            self.compute_vs_rubber_margin >= 0.0
            and self.compute_vs_no_show_margin >= 0.0
        )


def required_compute_reward_advantage_over_rubber(
    compute_cost: float,
    invalid_rate: float,
    exposure_probability: float,
    fault_loss: float,
) -> float:
    """Minimum R_C-R_R needed for compute to weakly dominate rubber-stamp."""

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

    return c - b * d * loss


def required_compute_reward_advantage_over_no_show(
    compute_cost: float,
) -> float:
    """Minimum R_C-R_N needed for compute to weakly dominate no-show."""

    c = float(compute_cost)
    if not isfinite(c) or c < 0.0:
        raise ValueError("compute_cost must be finite and nonnegative")
    return c


def certified_exposure_lower_bound(state: JamMaintenanceState) -> float:
    """Lower bound on exposure/rejection from the pessimistic acceptance bound."""

    return max(0.0, min(1.0, 1.0 - state.attack_bound))


def certified_required_reward_advantage_over_rubber(
    state: JamMaintenanceState,
    compute_cost: float,
    invalid_rate: float,
    fault_loss: float,
) -> float:
    """Sufficient R_C-R_R using the ELVES-derived exposure lower bound."""

    return required_compute_reward_advantage_over_rubber(
        compute_cost,
        invalid_rate,
        certified_exposure_lower_bound(state),
        fault_loss,
    )


def rubber_stamp_beats_no_show(
    reward_rubber_stamp: float,
    reward_no_show: float,
    invalid_rate: float,
    exposure_probability: float,
    fault_loss: float,
) -> bool:
    """Whether silent positive judgment privately dominates visible no-show."""

    rr = float(reward_rubber_stamp)
    rn = float(reward_no_show)
    b = float(invalid_rate)
    d = float(exposure_probability)
    loss = float(fault_loss)
    if not all(isfinite(x) for x in (rr, rn, b, d, loss)):
        raise ValueError("all values must be finite")
    if not 0.0 <= b <= 1.0 or not 0.0 <= d <= 1.0 or loss < 0.0:
        raise ValueError("invalid probability/loss parameters")
    return rr - b * d * loss >= rn
