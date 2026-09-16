"""Experiment 12: fungal flow-coupled maintenance.

Substrate: cord-forming fungal mycelial networks.

Empirical grounding motivating the model:
- mycelial network architecture is continuously reconfigured by growth,
  branching, fusion and regression in response to resource/environmental cues,
  damage and predation;
- in Phanerochaete velutina, cords predicted to carry faster/larger currents
  were significantly more likely to increase in size;
- fluid flow can therefore act as a local signal carrying information about a
  cord's role in the wider network.

The exact nonlinear reinforcement law below is a model extension, not an
empirical claim about fungal physiology.

Minimal two-route model
-----------------------
Let z in [0,1] be the fraction of a fixed transport/maintenance allocation in
route 1; route 2 has share 1-z.

Let s in [0,1] represent effective contrast sensitivity of the local
flow-coupled maintenance signal:
    u1 = 1/2 + s(z-1/2)
    u2 = 1-u1.
s=1 means the return signal tracks relative route use exactly; s=0 removes all
route-use contrast.

Let beta > 0 be the reinforcement elasticity. The preferred new allocation is
    A = u1**beta / (u1**beta + u2**beta).

With adjustment rate delta in (0,1],
    z_next = (1-delta) z + delta A.

At the symmetric redundant state z=1/2, the local multiplier is

    M = 1 - delta + delta * beta * s.

Under the declared parameter bounds M is nonnegative, so local stability is
exactly

    beta * s < 1.

Thus:
- beta*s < 1: perturbations are restored toward equal redundancy;
- beta*s = 1: neutral local allocation;
- beta*s > 1: small asymmetries are amplified and allocation concentrates.

This challenges any universal rule that stronger positive reinforcement of
high-use routes is always beneficial. Strong use-dependent reinforcement can
erode backup-route resilience.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Iterable


@dataclass(frozen=True)
class FungalFlowParameters:
    beta: float = 1.0
    adjustment: float = 0.5
    sensitivity: float = 1.0

    def __post_init__(self) -> None:
        if not isfinite(self.beta) or self.beta <= 0.0:
            raise ValueError("beta must be finite and positive")
        if (
            not isfinite(self.adjustment)
            or not 0.0 < self.adjustment <= 1.0
        ):
            raise ValueError("adjustment must lie in (0,1]")
        if (
            not isfinite(self.sensitivity)
            or not 0.0 <= self.sensitivity <= 1.0
        ):
            raise ValueError("sensitivity must lie in [0,1]")


def _validate_share(z: float) -> float:
    z = float(z)
    if not isfinite(z) or not 0.0 <= z <= 1.0:
        raise ValueError("route share must lie in [0,1]")
    return z


def local_flow_signal_share(
    z: float,
    sensitivity: float,
) -> float:
    """Effective local signal for route 1.

    This is an interpolation between no route-specific information (1/2) and
    exact relative-use information (z).
    """

    z = _validate_share(z)
    s = float(sensitivity)
    if not isfinite(s) or not 0.0 <= s <= 1.0:
        raise ValueError("sensitivity must lie in [0,1]")
    return 0.5 + s * (z - 0.5)


def preferred_maintenance_share(
    z: float,
    beta: float,
    sensitivity: float = 1.0,
) -> float:
    z = _validate_share(z)
    beta = float(beta)
    s = float(sensitivity)
    if not isfinite(beta) or beta <= 0.0:
        raise ValueError("beta must be finite and positive")
    if not isfinite(s) or not 0.0 <= s <= 1.0:
        raise ValueError("sensitivity must lie in [0,1]")

    u1 = local_flow_signal_share(z, s)
    u2 = 1.0 - u1

    # beta > 0; 0**beta is well-defined at the extreme exact-signal endpoints.
    a1 = u1**beta
    a2 = u2**beta
    denom = a1 + a2
    if denom <= 0.0:
        raise ArithmeticError("maintenance allocation denominator vanished")
    return a1 / denom


def update_route_share(
    z: float,
    params: FungalFlowParameters,
) -> float:
    z = _validate_share(z)
    preferred = preferred_maintenance_share(
        z,
        params.beta,
        params.sensitivity,
    )
    return (
        (1.0 - params.adjustment) * z
        + params.adjustment * preferred
    )


def symmetric_multiplier(params: FungalFlowParameters) -> float:
    """Local multiplier around z=1/2."""

    return (
        1.0
        - params.adjustment
        + params.adjustment
        * params.beta
        * params.sensitivity
    )


def symmetric_locally_stable(params: FungalFlowParameters) -> bool:
    return abs(symmetric_multiplier(params)) < 1.0


def effective_reinforcement_gain(params: FungalFlowParameters) -> float:
    return params.beta * params.sensitivity


def worst_case_backup_share(z: float) -> float:
    """Route capacity remaining after loss of the stronger of two routes.

    For a fixed total route allocation normalized to one, the worst single-route
    loss leaves the smaller route share. This is maximized at z=1/2.
    """

    z = _validate_share(z)
    return min(z, 1.0 - z)


def iterate_route_share(
    z0: float,
    params: FungalFlowParameters,
    steps: int,
) -> list[float]:
    if isinstance(steps, bool) or not isinstance(steps, int) or steps < 0:
        raise ValueError("steps must be a nonnegative integer")
    z = _validate_share(z0)
    out = [z]
    for _ in range(steps):
        z = update_route_share(z, params)
        out.append(z)
    return out


def backup_trajectory(
    z0: float,
    params: FungalFlowParameters,
    steps: int,
) -> list[float]:
    return [
        worst_case_backup_share(z)
        for z in iterate_route_share(z0, params, steps)
    ]


def simulate_parameter_cases(
    cases: Iterable[tuple[str, FungalFlowParameters]],
    z0: float = 0.51,
    steps: int = 30,
) -> dict[str, dict[str, float]]:
    result: dict[str, dict[str, float]] = {}
    for name, params in cases:
        trajectory = iterate_route_share(z0, params, steps)
        result[name] = {
            "initial_share": trajectory[0],
            "final_share": trajectory[-1],
            "initial_backup": worst_case_backup_share(trajectory[0]),
            "final_backup": worst_case_backup_share(trajectory[-1]),
            "multiplier": symmetric_multiplier(params),
            "effective_gain": effective_reinforcement_gain(params),
        }
    return result
