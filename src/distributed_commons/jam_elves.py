"""JAM/ELVES grounding utilities.

This module is intentionally substrate-specific. It does not modify the neutral
participant/network/commons theory.

Grounded ELVES quantities:
- economic soundness threshold epsilon* = nu / (n + nu);
- honest escalation reproduction number lambda = (1-gamma) * s_delta;
- no-show amplification A = (alpha + beta) * s_delta;
- branching-process attack bound q^(s0/s_delta), where
  q = exp(-lambda * (1-q)) is the extinction probability.

Our extension:
- a shared-client bug affects only the honest validators able to detect one
  crafted invalid report, giving
      lambda_f = (1-gamma) * (1-f) * s_delta.
  This is not part of the ELVES model.
"""

from __future__ import annotations

from math import exp, isfinite, log


def economic_soundness_threshold(n: int, collateral_share: float) -> float:
    """Strict upper boundary on epsilon from ELVES Corollary 1."""

    if isinstance(n, bool) or not isinstance(n, int) or n <= 0:
        raise ValueError("n must be a positive integer")
    if not isfinite(collateral_share) or not 0.0 < collateral_share < 1.0:
        raise ValueError("collateral_share must lie in (0,1)")
    return collateral_share / (n + collateral_share)


def required_collateral_share(
    n: int, acceptance_probability: float, *, collateral_units_lost: int = 1
) -> float:
    """Minimum nu from the same expected-profit inequality."""

    if isinstance(n, bool) or not isinstance(n, int) or n <= 0:
        raise ValueError("n must be a positive integer")
    p = float(acceptance_probability)
    if not isfinite(p) or not 0.0 <= p < 1.0:
        raise ValueError("acceptance_probability must lie in [0,1)")
    if (
        isinstance(collateral_units_lost, bool)
        or not isinstance(collateral_units_lost, int)
        or collateral_units_lost < 1
    ):
        raise ValueError("collateral_units_lost must be a positive integer")
    if p == 0.0:
        return 0.0
    return n * p / ((1.0 - p) * collateral_units_lost)


def honest_reproduction(
    gamma: float, s_delta: float, *, client_bug_share: float = 0.0
) -> float:
    """Mean effective honest offspring per no-show tranche."""

    for name, value in (
        ("gamma", gamma),
        ("client_bug_share", client_bug_share),
    ):
        if not isfinite(value) or not 0.0 <= value < 1.0:
            raise ValueError(f"{name} must lie in [0,1)")
    if not isfinite(s_delta) or s_delta <= 0.0:
        raise ValueError("s_delta must be positive")
    return (1.0 - gamma) * (1.0 - client_bug_share) * s_delta


def faulty_reproduction(alpha: float, beta: float, s_delta: float) -> float:
    """ELVES no-show amplification A=(alpha+beta)*s_delta."""

    for name, value in (("alpha", alpha), ("beta", beta)):
        if not isfinite(value) or not 0.0 <= value < 1.0:
            raise ValueError(f"{name} must lie in [0,1)")
    if alpha + beta >= 1.0:
        raise ValueError("alpha + beta must be < 1")
    if not isfinite(s_delta) or s_delta <= 0.0:
        raise ValueError("s_delta must be positive")
    return (alpha + beta) * s_delta


def extinction_probability(mean_offspring: float) -> float:
    """Extinction probability of a Poisson Galton-Watson process."""

    lam = float(mean_offspring)
    if not isfinite(lam) or lam < 0.0:
        raise ValueError("mean_offspring must be finite and nonnegative")
    if lam <= 1.0:
        return 1.0

    lo, hi = 0.0, 1.0 - 1e-15
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        residual = mid - exp(-lam * (1.0 - mid))
        if residual > 0.0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def attack_success_bound(
    gamma: float,
    s0: float,
    s_delta: float,
    *,
    client_bug_share: float = 0.0,
) -> float:
    """ELVES Lemma-3 bound, with optional shared-client extension."""

    if not isfinite(s0) or s0 <= 0.0:
        raise ValueError("s0 must be positive")
    if not isfinite(s_delta) or s_delta <= 0.0:
        raise ValueError("s_delta must be positive")
    lam = honest_reproduction(
        gamma, s_delta, client_bug_share=client_bug_share
    )
    q = extinction_probability(lam)
    return q ** (s0 / s_delta)


def expected_committee_bound(
    s0: float, alpha: float, beta: float, s_delta: float
) -> float:
    """Static ELVES expected-final-committee bound s0/(1-A)."""

    if not isfinite(s0) or s0 <= 0.0:
        raise ValueError("s0 must be positive")
    amplification = faulty_reproduction(alpha, beta, s_delta)
    if amplification >= 1.0:
        raise ValueError("faulty escalation is not subcritical")
    return s0 / (1.0 - amplification)


def critical_client_bug_share(gamma: float, s_delta: float) -> float:
    """Client share where effective honest escalation loses supercriticality."""

    base = honest_reproduction(gamma, s_delta)
    if base <= 1.0:
        return 0.0
    return min(1.0, max(0.0, 1.0 - 1.0 / base))


def max_client_bug_share_for_target(
    gamma: float, s0: float, s_delta: float, epsilon: float
) -> float | None:
    """Largest shared-client fraction supported by the extended bound."""

    if not isfinite(epsilon) or not 0.0 < epsilon < 1.0:
        raise ValueError("epsilon must lie in (0,1)")
    if not isfinite(s0) or s0 <= 0.0:
        raise ValueError("s0 must be positive")
    if not isfinite(s_delta) or s_delta <= 0.0:
        raise ValueError("s_delta must be positive")
    if not isfinite(gamma) or not 0.0 <= gamma < 1.0:
        raise ValueError("gamma must lie in [0,1)")

    baseline = attack_success_bound(gamma, s0, s_delta)
    if baseline > epsilon:
        return None

    q_target = epsilon ** (s_delta / s0)
    lambda_required = -log(q_target) / (1.0 - q_target)
    f_max = 1.0 - lambda_required / ((1.0 - gamma) * s_delta)
    return min(1.0, max(0.0, f_max))
