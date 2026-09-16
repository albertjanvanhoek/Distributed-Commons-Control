"""Experiment 6: participant contribution to access of stored capacity.

This joins Experiment 3's failure topology to Experiment 5's slow corrective
capacity without assigning capacity additively to participants.

Let pi(S) be the probability that every participant in coalition S is disabled.
Let the passive finite-shock margin be

    X - V,

and let accessible corrective capacity add kappa*C to that margin when at least
one participant remains functional.

The expected finite-shock margin is

    E[M | S] = X - V + (1-pi(S))*kappa*C.

Thus the marginal contribution of participant i is

    Delta_i M
      = kappa*C * (pi(S) - pi(S union {i})).

The participant's contribution therefore depends on network failure topology
and on the current reserve-capacity state C. The same participant can have
zero value when C=0 and positive value when stored corrective capacity exists.

A stricter "certified" margin is also provided: the capacity extension counts
only when pi(S) is below a declared access-failure target.
"""

from __future__ import annotations

from math import isfinite

from .corrective_capacity import CapacityParameters
from .viability import FailureTopology


def expected_access_margin(
    topology: FailureTopology,
    coalition: set[str] | frozenset[str],
    shared_state: float,
    capacity: float,
    p: CapacityParameters,
) -> float:
    """Expected finite-shock margin under binary access to corrective capacity."""

    x = float(shared_state)
    c = float(capacity)
    if not isfinite(x) or not 0.0 <= x <= 1.0:
        raise ValueError("shared_state must lie in [0,1]")
    if not isfinite(c) or c < 0.0:
        raise ValueError("capacity must be finite and nonnegative")
    failure = topology.escape_probability(coalition)
    return (
        x
        - p.viability_floor
        + (1.0 - failure) * p.correction_efficiency * c
    )


def certified_access_margin(
    topology: FailureTopology,
    coalition: set[str] | frozenset[str],
    shared_state: float,
    capacity: float,
    access_failure_target: float,
    p: CapacityParameters,
) -> float:
    """Finite-shock margin certified at a declared access-failure target."""

    target = float(access_failure_target)
    if not isfinite(target) or not 0.0 <= target <= 1.0:
        raise ValueError("access_failure_target must lie in [0,1]")
    x = float(shared_state)
    c = float(capacity)
    if not isfinite(x) or not 0.0 <= x <= 1.0:
        raise ValueError("shared_state must lie in [0,1]")
    if not isfinite(c) or c < 0.0:
        raise ValueError("capacity must be finite and nonnegative")

    passive = x - p.viability_floor
    failure = topology.escape_probability(coalition)
    if failure <= target:
        return passive + p.correction_efficiency * c
    return passive


def expected_participant_contribution(
    topology: FailureTopology,
    participant: str,
    coalition_without: set[str] | frozenset[str],
    shared_state: float,
    capacity: float,
    p: CapacityParameters,
) -> float:
    """Expected-margin contribution from adding one participant."""

    coalition = frozenset(coalition_without)
    if participant not in topology.participant_names:
        raise ValueError(f"unknown participant: {participant}")
    if participant in coalition:
        raise ValueError("participant must not already be in coalition")

    before = expected_access_margin(
        topology, coalition, shared_state, capacity, p
    )
    after = expected_access_margin(
        topology, coalition | {participant}, shared_state, capacity, p
    )
    return after - before


def certified_participant_contribution(
    topology: FailureTopology,
    participant: str,
    coalition_without: set[str] | frozenset[str],
    shared_state: float,
    capacity: float,
    access_failure_target: float,
    p: CapacityParameters,
) -> float:
    """Certified-margin contribution from adding one participant."""

    coalition = frozenset(coalition_without)
    before = certified_access_margin(
        topology,
        coalition,
        shared_state,
        capacity,
        access_failure_target,
        p,
    )
    after = certified_access_margin(
        topology,
        coalition | {participant},
        shared_state,
        capacity,
        access_failure_target,
        p,
    )
    return after - before
