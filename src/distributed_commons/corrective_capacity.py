"""Experiment 5: shared state and slow corrective capacity.

This is a substrate-neutral two-state model.

X is the current shared-state condition.
C is a slower stock that bounds how much fast corrective action can be
deployed after a shock.

Between shocks,

    X[t+1] = X[t] + gamma * (1 - X[t])
    C[t+1] = (1 - delta) * C[t] + maintenance[t].

A shock of size s lowers X. Up to kappa*C units can be corrected immediately.
For a declared viability floor V, the uncapped shock margin is

    M(X,C) = X - V + kappa*C.

This is derived from the post-shock condition

    X - s + kappa*C >= V

and is therefore an operational disturbance margin, not a bookkeeping
definition of fragility.

At X=1 with zero maintenance, the observed shared state stays exactly at 1
while C decays. The local recovery multiplier of X remains 1-gamma, but the
shock margin declines. Thus current state and local critical-slowing
information can be identical while finite-shock robustness differs.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class CapacityParameters:
    regeneration: float = 0.10
    capacity_decay: float = 0.05
    correction_efficiency: float = 0.50
    viability_floor: float = 0.70

    def __post_init__(self) -> None:
        if not 0.0 < self.regeneration <= 1.0:
            raise ValueError("regeneration must lie in (0,1]")
        if not 0.0 <= self.capacity_decay <= 1.0:
            raise ValueError("capacity_decay must lie in [0,1]")
        if not isfinite(self.correction_efficiency) or self.correction_efficiency < 0.0:
            raise ValueError("correction_efficiency must be finite and nonnegative")
        if not 0.0 <= self.viability_floor <= 1.0:
            raise ValueError("viability_floor must lie in [0,1]")


def uncapped_shock_margin(
    shared_state: float,
    capacity: float,
    p: CapacityParameters,
) -> float:
    """Largest shock compatible with the viability floor using full capacity."""

    x = float(shared_state)
    c = float(capacity)
    if not isfinite(x) or not 0.0 <= x <= 1.0:
        raise ValueError("shared_state must lie in [0,1]")
    if not isfinite(c) or c < 0.0:
        raise ValueError("capacity must be finite and nonnegative")
    return x - p.viability_floor + p.correction_efficiency * c


def shock_margin(
    shared_state: float,
    capacity: float,
    p: CapacityParameters,
) -> float:
    """Operational shock margin restricted to shocks in [0,1]."""

    return min(1.0, max(0.0, uncapped_shock_margin(shared_state, capacity, p)))


def post_shock_state(
    shared_state: float,
    capacity: float,
    shock: float,
    p: CapacityParameters,
) -> float:
    """Best immediate post-shock state using available corrective capacity."""

    x = float(shared_state)
    c = float(capacity)
    s = float(shock)
    if not isfinite(x) or not 0.0 <= x <= 1.0:
        raise ValueError("shared_state must lie in [0,1]")
    if not isfinite(c) or c < 0.0:
        raise ValueError("capacity must be finite and nonnegative")
    if not isfinite(s) or not 0.0 <= s <= 1.0:
        raise ValueError("shock must lie in [0,1]")
    correction = min(s, p.correction_efficiency * c)
    return min(1.0, max(0.0, x - s + correction))


def shock_is_viable(
    shared_state: float,
    capacity: float,
    shock: float,
    p: CapacityParameters,
) -> bool:
    return (
        post_shock_state(shared_state, capacity, shock, p)
        >= p.viability_floor
    )


def quiet_step(
    shared_state: float,
    capacity: float,
    p: CapacityParameters,
    *,
    maintenance: float = 0.0,
) -> tuple[float, float]:
    """One shock-free step with independent capacity maintenance."""

    x = float(shared_state)
    c = float(capacity)
    m = float(maintenance)
    if not isfinite(x) or not 0.0 <= x <= 1.0:
        raise ValueError("shared_state must lie in [0,1]")
    if not isfinite(c) or c < 0.0:
        raise ValueError("capacity must be finite and nonnegative")
    if not isfinite(m) or m < 0.0:
        raise ValueError("maintenance must be finite and nonnegative")

    x_next = x + p.regeneration * (1.0 - x)
    c_next = (1.0 - p.capacity_decay) * c + m
    return min(1.0, max(0.0, x_next)), max(0.0, c_next)


def quiet_trajectory(
    shared_state: float,
    capacity: float,
    p: CapacityParameters,
    *,
    steps: int,
    maintenance: float = 0.0,
) -> list[tuple[int, float, float, float]]:
    if isinstance(steps, bool) or not isinstance(steps, int) or steps < 0:
        raise ValueError("steps must be a nonnegative integer")
    out: list[tuple[int, float, float, float]] = []
    x, c = shared_state, capacity
    for t in range(steps + 1):
        out.append((t, x, c, shock_margin(x, c, p)))
        if t < steps:
            x, c = quiet_step(x, c, p, maintenance=maintenance)
    return out


def local_shared_state_multiplier(p: CapacityParameters) -> float:
    """Linear recovery multiplier of X around its quiet fixed point X=1."""

    return 1.0 - p.regeneration


def required_maintenance_for_capacity(
    target_capacity: float, p: CapacityParameters
) -> float:
    """Per-step maintenance input that keeps a target capacity stationary."""

    c = float(target_capacity)
    if not isfinite(c) or c < 0.0:
        raise ValueError("target_capacity must be finite and nonnegative")
    return p.capacity_decay * c


def maintenance_shortfall(
    required_margin: float,
    shared_state: float,
    capacity: float,
    p: CapacityParameters,
) -> float:
    """Derived shortfall relative to a declared required shock margin."""

    required = float(required_margin)
    if not isfinite(required) or required < 0.0:
        raise ValueError("required_margin must be finite and nonnegative")
    return max(
        0.0,
        required - shock_margin(shared_state, capacity, p),
    )
