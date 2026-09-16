"""Experiment 9: JAM behavioral-maintenance operators.

This module is substrate-specific and uses the existing JAM/ELVES grounding.

Two grounded viability components are kept separate:

1. Safety certification margin

       M_safety = log(epsilon_star / P_accept_bound)

   where epsilon_star = nu/(n+nu) is the ELVES economic target and
   P_accept_bound is the pessimistic branching-process bound.

   Positive values are certified by the bound; negative values are not.

2. Scalability/liveness margin

       M_scale = 1 - A
               = 1 - u*s_delta

   where u is the share contributing to the no-show/fault reproduction term
   and A<1 is the ELVES subcriticality condition.

This yields a JAM-specific vector rather than a scalar score.

The individual counterfactuals below are deliberately fixed-size:
- client diversification changes one otherwise-honest validator from a shared
  vulnerable client profile to an independent/correct profile;
- reliability improvement removes one validator from the no-show-prone share.

For a fixed validator population n, both operations change their corresponding
reproduction margins by exactly s_delta/n:
- one client diversification raises lambda_f by s_delta/n;
- one reliability improvement raises 1-A by s_delta/n.

A global escalation-strength change has opposite signs:
- increasing s_delta raises lambda_f (better correction/safety);
- increasing s_delta lowers 1-A when u>0 (worse scalability).
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from math import isfinite, log

from .jam_elves import (
    attack_success_bound,
    economic_soundness_threshold,
)


@dataclass(frozen=True)
class JamMaintenanceState:
    validator_count: int = 1023
    adversarial_count: int = 205
    vulnerable_honest_count: int = 82
    no_show_share: float = 0.15
    s0: float = 30.0
    s_delta: float = 2.0
    collateral_share: float = 0.05

    def __post_init__(self) -> None:
        n = self.validator_count
        a = self.adversarial_count
        b = self.vulnerable_honest_count
        if isinstance(n, bool) or not isinstance(n, int) or n <= 0:
            raise ValueError("validator_count must be a positive integer")
        if isinstance(a, bool) or not isinstance(a, int) or not 0 <= a < n:
            raise ValueError("adversarial_count must be an integer in [0,n)")
        if (
            isinstance(b, bool)
            or not isinstance(b, int)
            or not 0 <= b <= n - a
        ):
            raise ValueError(
                "vulnerable_honest_count must lie within the honest population"
            )
        if not isfinite(self.no_show_share) or not 0.0 <= self.no_show_share < 1.0:
            raise ValueError("no_show_share must lie in [0,1)")
        if not isfinite(self.s0) or self.s0 <= 0.0:
            raise ValueError("s0 must be positive")
        if not isfinite(self.s_delta) or self.s_delta <= 0.0:
            raise ValueError("s_delta must be positive")
        if (
            not isfinite(self.collateral_share)
            or not 0.0 < self.collateral_share < 1.0
        ):
            raise ValueError("collateral_share must lie in (0,1)")

    @property
    def honest_count(self) -> int:
        return self.validator_count - self.adversarial_count

    @property
    def gamma(self) -> float:
        return self.adversarial_count / self.validator_count

    @property
    def vulnerable_honest_share(self) -> float:
        return self.vulnerable_honest_count / self.honest_count

    @property
    def economic_target(self) -> float:
        return economic_soundness_threshold(
            self.validator_count, self.collateral_share
        )

    @property
    def correction_reproduction(self) -> float:
        return (
            (1.0 - self.gamma)
            * (1.0 - self.vulnerable_honest_share)
            * self.s_delta
        )

    @property
    def failure_reproduction(self) -> float:
        return self.no_show_share * self.s_delta

    @property
    def scalability_margin(self) -> float:
        return 1.0 - self.failure_reproduction

    @property
    def attack_bound(self) -> float:
        return attack_success_bound(
            self.gamma,
            self.s0,
            self.s_delta,
            client_bug_share=self.vulnerable_honest_share,
        )

    @property
    def safety_log_margin(self) -> float:
        """Positive iff the pessimistic ELVES bound certifies the target."""

        return log(self.economic_target / self.attack_bound)

    @property
    def viability_vector(self) -> tuple[float, float]:
        return (self.safety_log_margin, self.scalability_margin)

    def diversify_one_honest_validator(self) -> "JamMaintenanceState":
        """Move one validator off the shared vulnerable client profile."""

        if self.vulnerable_honest_count <= 0:
            raise ValueError("no vulnerable honest validator remains")
        return replace(
            self,
            vulnerable_honest_count=self.vulnerable_honest_count - 1,
        )

    def improve_one_validator_reliability(self) -> "JamMaintenanceState":
        """Remove one validator-equivalent share from the no-show term."""

        step = 1.0 / self.validator_count
        if self.no_show_share < step:
            raise ValueError("no_show_share is smaller than one validator step")
        return replace(self, no_show_share=self.no_show_share - step)

    def with_escalation(self, s_delta: float) -> "JamMaintenanceState":
        return replace(self, s_delta=float(s_delta))


def one_validator_correction_gain(state: JamMaintenanceState) -> float:
    """Exact gain in lambda_f from diversifying one honest validator."""

    after = state.diversify_one_honest_validator()
    return after.correction_reproduction - state.correction_reproduction


def one_validator_scalability_gain(state: JamMaintenanceState) -> float:
    """Exact gain in 1-A from making one validator-equivalent reliable."""

    after = state.improve_one_validator_reliability()
    return after.scalability_margin - state.scalability_margin


def escalation_vector_change(
    state: JamMaintenanceState, new_s_delta: float
) -> tuple[float, float]:
    """Change in (safety log margin, scalability margin)."""

    after = state.with_escalation(new_s_delta)
    return (
        after.safety_log_margin - state.safety_log_margin,
        after.scalability_margin - state.scalability_margin,
    )
