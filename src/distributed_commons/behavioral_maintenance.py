"""Experiment 8: behavioral maintenance operators.

The model is substrate-neutral. "Behavior" means any state-contingent process
performed by a participant that changes future network/commons viability. It
does not imply intention, awareness, or animal/human cognition.

Let K be a maintenance-dependent enabling stock and V a declared viability
floor. Between perturbations,

    K[t+1] = (1-delta) K[t] + e + m(K[t]),

where
- delta is decay,
- e is passive/exogenous renewal,
- m is participant-supplied maintenance.

At the viability boundary K=V, persistence for one further step requires

    e + m(V) >= delta V.

Therefore participant maintenance is not universally necessary: if passive
renewal alone satisfies e >= delta V, zero participant maintenance can preserve
the boundary. But when e < delta V, aggregate participant maintenance must
close the exact replacement gap delta V - e.

A local corrective policy around target K* can be written

    m(K) = m0 + g (K* - K).

With m0 chosen so K* is an equilibrium, the local multiplier is

    1 - delta - g.

Hence too much corrective gain (g > 2-delta) creates a flip instability:
"more correction" is not monotonically better.

If the deficit signal is sign-inverted with probability 1-p, expected
corrective gain becomes (2p-1)g. Signal fidelity therefore controls whether
nominal correction remains negative feedback.

Positive reinforcement is also conditional. If a candidate process is helpful
with prior h, a helpful process yields benefit a>0, a harmful process causes
loss b>0, and a binary evaluation signal is correct with probability p, then
the unnormalised expected value among positively signalled processes is

    h p a - (1-h)(1-p)b.

Positive reinforcement is beneficial only when this quantity is positive.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Iterable


@dataclass(frozen=True)
class MaintenanceParameters:
    decay: float
    passive_renewal: float
    viability_floor: float
    target: float = 1.0

    def __post_init__(self) -> None:
        if not isfinite(self.decay) or not 0.0 < self.decay <= 1.0:
            raise ValueError("decay must lie in (0,1]")
        if not isfinite(self.passive_renewal) or self.passive_renewal < 0.0:
            raise ValueError("passive_renewal must be finite and nonnegative")
        if not isfinite(self.viability_floor) or self.viability_floor < 0.0:
            raise ValueError("viability_floor must be finite and nonnegative")
        if not isfinite(self.target) or self.target < self.viability_floor:
            raise ValueError("target must be finite and >= viability_floor")


def replacement_gap(p: MaintenanceParameters) -> float:
    """Participant maintenance required at the viability boundary."""

    return max(0.0, p.decay * p.viability_floor - p.passive_renewal)


def passive_renewal_suffices(p: MaintenanceParameters) -> bool:
    """Whether passive renewal alone preserves the viability boundary."""

    return p.passive_renewal >= p.decay * p.viability_floor


def boundary_next_state(
    p: MaintenanceParameters,
    participant_maintenance: float,
) -> float:
    """Next stock from K=V under aggregate participant maintenance."""

    m = float(participant_maintenance)
    if not isfinite(m) or m < 0.0:
        raise ValueError("participant_maintenance must be nonnegative")
    v = p.viability_floor
    return (1.0 - p.decay) * v + p.passive_renewal + m


def boundary_is_preserved(
    p: MaintenanceParameters,
    participant_maintenance: float,
) -> bool:
    return boundary_next_state(p, participant_maintenance) >= p.viability_floor


def decentralized_boundary_is_preserved(
    p: MaintenanceParameters,
    local_maintenance: Iterable[float],
) -> bool:
    """No coordinator is required in this additive maintenance model."""

    total = 0.0
    for value in local_maintenance:
        value = float(value)
        if not isfinite(value) or value < 0.0:
            raise ValueError("local maintenance values must be nonnegative")
        total += value
    return boundary_is_preserved(p, total)


def target_baseline_maintenance(p: MaintenanceParameters) -> float:
    """Baseline input that makes K=target an equilibrium before correction."""

    return p.decay * p.target - p.passive_renewal


def correction_multiplier(p: MaintenanceParameters, gain: float) -> float:
    """Local multiplier around the target for linear deficit correction."""

    g = float(gain)
    if not isfinite(g) or g < 0.0:
        raise ValueError("gain must be finite and nonnegative")
    return 1.0 - p.decay - g


def correction_is_locally_stable(
    p: MaintenanceParameters,
    gain: float,
) -> bool:
    return abs(correction_multiplier(p, gain)) < 1.0


def overcorrection_threshold(p: MaintenanceParameters) -> float:
    """Gain above this threshold produces |multiplier|>1."""

    return 2.0 - p.decay


def effective_corrective_gain(gain: float, signal_fidelity: float) -> float:
    """Expected signed gain under symmetric sign-flip signal noise."""

    g = float(gain)
    fidelity = float(signal_fidelity)
    if not isfinite(g) or g < 0.0:
        raise ValueError("gain must be finite and nonnegative")
    if not isfinite(fidelity) or not 0.0 <= fidelity <= 1.0:
        raise ValueError("signal_fidelity must lie in [0,1]")
    return (2.0 * fidelity - 1.0) * g


def noisy_correction_multiplier(
    p: MaintenanceParameters,
    gain: float,
    signal_fidelity: float,
) -> float:
    return 1.0 - p.decay - effective_corrective_gain(
        gain, signal_fidelity
    )


def reinforcement_value_numerator(
    helpful_prior: float,
    signal_fidelity: float,
    helpful_benefit: float,
    harmful_loss: float,
) -> float:
    """Sign of expected true contribution among positively signalled processes.

    The denominator (probability of a positive signal) is positive in
    nondegenerate cases, so the numerator determines the sign.
    """

    h = float(helpful_prior)
    fidelity = float(signal_fidelity)
    benefit = float(helpful_benefit)
    loss = float(harmful_loss)

    if not isfinite(h) or not 0.0 <= h <= 1.0:
        raise ValueError("helpful_prior must lie in [0,1]")
    if not isfinite(fidelity) or not 0.0 <= fidelity <= 1.0:
        raise ValueError("signal_fidelity must lie in [0,1]")
    if not isfinite(benefit) or benefit <= 0.0:
        raise ValueError("helpful_benefit must be positive")
    if not isfinite(loss) or loss <= 0.0:
        raise ValueError("harmful_loss must be positive")

    return (
        h * fidelity * benefit
        - (1.0 - h) * (1.0 - fidelity) * loss
    )


def positive_reinforcement_is_beneficial(
    helpful_prior: float,
    signal_fidelity: float,
    helpful_benefit: float,
    harmful_loss: float,
) -> bool:
    return reinforcement_value_numerator(
        helpful_prior,
        signal_fidelity,
        helpful_benefit,
        harmful_loss,
    ) > 0.0


def repair_net_value(
    repair_probability: float,
    repaired_value: float,
    outside_value: float,
    repair_cost: float,
) -> float:
    """SCAP repair/forgiveness inequality as a neutral operator value."""

    r = float(repair_probability)
    v = float(repaired_value)
    w = float(outside_value)
    cost = float(repair_cost)

    if not isfinite(r) or not 0.0 <= r <= 1.0:
        raise ValueError("repair_probability must lie in [0,1]")
    for name, value in (
        ("repaired_value", v),
        ("outside_value", w),
        ("repair_cost", cost),
    ):
        if not isfinite(value):
            raise ValueError(f"{name} must be finite")
    if cost < 0.0:
        raise ValueError("repair_cost must be nonnegative")

    return r * (v - w) - cost


def repair_is_worthwhile(
    repair_probability: float,
    repaired_value: float,
    outside_value: float,
    repair_cost: float,
) -> bool:
    return repair_net_value(
        repair_probability,
        repaired_value,
        outside_value,
        repair_cost,
    ) >= 0.0
