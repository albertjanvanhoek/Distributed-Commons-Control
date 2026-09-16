"""Experiment 4: direct structural contribution versus selected contribution.

This module is substrate-neutral. It studies a minimal shared-reward game in
which participants choose whether to perform a corrective check.

A harmful event occurs with rate b. If one or more participants check it, a
fixed reward r is split equally among the checkers. Participant i pays
quadratic effort cost c*q_i^2/2.

For one participant, the interior selected effort is

    q1 = z,   z = b*r/c.

For two symmetric participants, if the other participant checks with
probability q, the expected reward share conditional on checking is 1-q/2.
The interior best response is z*(1-q/2), so the symmetric fixed point is

    q2 = 2*z/(2+z).

The declared viability margin at harmful-attempt rate b and target epsilon is

    margin = epsilon - b * P(no participant checks).

The direct/frozen structural contribution of adding a second participant at
the incumbent effort z is always positive for 0<z<1:

    b*z*(1-z) > 0.

But after both participants re-equilibrate under shared rewards, the total
contribution is negative exactly when

    z^2 + 4*z - 4 > 0,

equivalently z > 2*(sqrt(2)-1) ~= 0.828427.

Thus a participant can improve the network mechanically while lowering the
realized viability margin through induced behavioral crowding-out.
"""

from __future__ import annotations

from math import isfinite, sqrt


REVERSAL_THRESHOLD = 2.0 * (sqrt(2.0) - 1.0)


def _probability(name: str, value: float) -> float:
    value = float(value)
    if not isfinite(value) or not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must lie in [0,1]")
    return value


def one_participant_effort(z: float) -> float:
    """Interior one-participant selected effort, clipped to feasibility."""

    if not isfinite(z) or z < 0.0:
        raise ValueError("z must be finite and nonnegative")
    return min(1.0, z)


def two_participant_effort(z: float) -> float:
    """Symmetric two-participant selected effort under equal reward sharing."""

    if not isfinite(z) or z < 0.0:
        raise ValueError("z must be finite and nonnegative")
    if z == 0.0:
        return 0.0
    return min(1.0, 2.0 * z / (2.0 + z))


def viability_margin(
    harmful_attempt_rate: float,
    safety_target: float,
    efforts: tuple[float, ...],
) -> float:
    """Safety slack epsilon - b*P(no check).

    A positive margin is safe, zero is the declared boundary, and a negative
    margin violates the declared target.
    """

    b = _probability("harmful_attempt_rate", harmful_attempt_rate)
    epsilon = _probability("safety_target", safety_target)
    miss = 1.0
    for effort in efforts:
        miss *= 1.0 - _probability("effort", effort)
    return epsilon - b * miss


def one_selected_margin(b: float, epsilon: float, z: float) -> float:
    return viability_margin(b, epsilon, (one_participant_effort(z),))


def two_frozen_margin(b: float, epsilon: float, z: float) -> float:
    """Margin immediately after addition if both participants keep effort z."""

    q = one_participant_effort(z)
    return viability_margin(b, epsilon, (q, q))


def two_selected_margin(b: float, epsilon: float, z: float) -> float:
    q = two_participant_effort(z)
    return viability_margin(b, epsilon, (q, q))


def direct_addition_contribution(b: float, epsilon: float, z: float) -> float:
    """Frozen-response effect of adding the second participant."""

    return two_frozen_margin(b, epsilon, z) - one_selected_margin(
        b, epsilon, z
    )


def selected_addition_contribution(
    b: float, epsilon: float, z: float
) -> float:
    """Total effect after both participants re-equilibrate."""

    return two_selected_margin(b, epsilon, z) - one_selected_margin(
        b, epsilon, z
    )


def induced_response_effect(b: float, epsilon: float, z: float) -> float:
    """Behavioral response term: total minus frozen direct contribution."""

    return two_selected_margin(b, epsilon, z) - two_frozen_margin(
        b, epsilon, z
    )


def reversal_polynomial(z: float) -> float:
    if not isfinite(z):
        raise ValueError("z must be finite")
    return z * z + 4.0 * z - 4.0


def reversal_occurs(z: float) -> bool:
    """Whether selected addition is negative in the interior 0<z<1 regime."""

    if not isfinite(z) or not 0.0 < z < 1.0:
        return False
    return reversal_polynomial(z) > 0.0


def critical_cost_ratio(safety_ratio: float) -> float:
    """c_crit,2 / c_crit,1 for x=epsilon/b in the interior model.

    The ratio is (1+sqrt(x))^2/2. Values below one mean the two-participant
    shared-reward system tolerates *less* effort cost than the one-participant
    system before selected checking falls below the same safety target.
    """

    x = float(safety_ratio)
    if not isfinite(x) or not 0.0 < x < 1.0:
        raise ValueError("safety_ratio must lie in (0,1)")
    return (1.0 + sqrt(x)) ** 2 / 2.0
