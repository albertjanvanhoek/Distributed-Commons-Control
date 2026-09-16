"""Minimal static and adaptive models of distributed commons control.

All quantities are dimensionless. The module deliberately uses only the
Python standard library so every numerical claim can be reproduced without a
scientific software stack.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import exp, inf, expm1, log, isfinite


def _probability(name: str, value: float) -> float:
    value = float(value)
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must lie in [0, 1], got {value}")
    return value


def _positive(name: str, value: float) -> float:
    value = float(value)
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be positive, got {value}")
    return value


def _clip_probability(value: float) -> float:
    return min(1.0, max(0.0, value))


def conditional_escape_probability(
    effort: float, monitors: int, correlation: float
) -> float:
    """Probability harmful work escapes, conditional on being attempted.

    With probability ``correlation`` all monitors share a blind spot. In the
    complementary branch, their failures are independent and symmetric.
    """

    effort = _probability("effort", effort)
    correlation = _probability("correlation", correlation)
    if not isinstance(monitors, int) or monitors < 1:
        raise ValueError(f"monitors must be a positive integer, got {monitors!r}")
    return correlation + (1.0 - correlation) * (1.0 - effort) ** monitors


def conditional_detection_probability(
    effort: float, monitors: int, correlation: float
) -> float:
    """Probability harmful work is detected, conditional on being attempted."""

    return 1.0 - conditional_escape_probability(effort, monitors, correlation)


def bad_finalization_probability(
    bad_attempt_rate: float, effort: float, monitors: int, correlation: float
) -> float:
    """Unconditional probability of harmful work reaching shared state."""

    bad_attempt_rate = _probability("bad_attempt_rate", bad_attempt_rate)
    return bad_attempt_rate * conditional_escape_probability(
        effort, monitors, correlation
    )


@dataclass(frozen=True)
class EffortRequirement:
    """Result of solving a declared safety inequality for monitor effort."""

    attainable: bool
    effort: float | None
    correlation_floor: float
    reason: str


class ControlPhase(str, Enum):
    """Mutually exclusive regions of the static control problem."""

    NO_MONITORING_REQUIRED = "no_monitoring_required"
    STRUCTURALLY_UNATTAINABLE = "structurally_unattainable"
    SUFFICIENT_SELECTED_CONTROL = "sufficient_selected_control"
    UNDERPROVIDED_CONTROL = "underprovided_control"


@dataclass(frozen=True)
class PhaseAssessment:
    """Complete static classification for one parameter combination."""

    phase: ControlPhase
    selected_effort: float
    required_effort: float | None
    effort_margin: float | None
    correlation_floor: float
    selected_bad_finalization: float
    critical_effort_cost: float | None


def sufficient_effort(
    bad_attempt_rate: float,
    monitors: int,
    correlation: float,
    safety_target: float,
    *,
    tolerance: float = 1e-12,
) -> EffortRequirement:
    """Return minimum symmetric effort satisfying ``P_bad <= safety_target``.

    Structural comparisons use exact floating-point ordering; tolerance is
    retained for API compatibility but never relaxes the safety floor.
    ``effort=None`` marks structural unattainability under the current
    monitor count and common-mode mixture.
    """

    bad_attempt_rate = _probability("bad_attempt_rate", bad_attempt_rate)
    correlation = _probability("correlation", correlation)
    safety_target = _probability("safety_target", safety_target)
    if not isinstance(monitors, int) or monitors < 1:
        raise ValueError(f"monitors must be a positive integer, got {monitors!r}")
    if not isfinite(tolerance) or tolerance < 0.0:
        raise ValueError("tolerance must be nonnegative")

    floor = bad_attempt_rate * correlation
    if bad_attempt_rate == 0.0 or safety_target >= bad_attempt_rate:
        return EffortRequirement(True, 0.0, floor, "target met without monitoring")
    if safety_target < floor:
        return EffortRequirement(
            False,
            None,
            floor,
            "target lies below the common-mode correlation floor",
        )
    if correlation == 1.0:
        return EffortRequirement(
            False,
            None,
            floor,
            "all failures are common-mode and the target is not already met",
        )

    independent_escape = (safety_target - floor) / (
        bad_attempt_rate * (1.0 - correlation)
    )
    independent_escape = min(1.0, max(0.0, independent_escape))
    effort = (
        1.0 if independent_escape == 0.0
        else -expm1(log(independent_escape) / monitors)
    )
    return EffortRequirement(True, _clip_probability(effort), floor, "attainable")


def monitor_objective(
    effort: float,
    bad_attempt_rate: float,
    monitor_reward: float,
    effort_cost: float,
    correlation: float = 0.0,
) -> float:
    """Private objective ``b*(1-rho)*r*q - c*q^2/2``.

    Common-mode blind spots remove both collective detection and the
    individual opportunity to earn a detection-contingent reward.
    """

    effort = _probability("effort", effort)
    bad_attempt_rate = _probability("bad_attempt_rate", bad_attempt_rate)
    correlation = _probability("correlation", correlation)
    if monitor_reward < 0.0:
        raise ValueError("monitor_reward must be nonnegative")
    effort_cost = _positive("effort_cost", effort_cost)
    return (
        bad_attempt_rate * (1.0 - correlation) * monitor_reward * effort
        - 0.5 * effort_cost * effort**2
    )


def selected_effort(
    bad_attempt_rate: float,
    monitor_reward: float,
    effort_cost: float,
    correlation: float = 0.0,
) -> float:
    """Feasible private optimum for the declared quadratic objective."""

    bad_attempt_rate = _probability("bad_attempt_rate", bad_attempt_rate)
    correlation = _probability("correlation", correlation)
    if monitor_reward < 0.0:
        raise ValueError("monitor_reward must be nonnegative")
    effort_cost = _positive("effort_cost", effort_cost)
    return _clip_probability(
        bad_attempt_rate * (1.0 - correlation) * monitor_reward / effort_cost
    )


def selected_control_is_sufficient(
    bad_attempt_rate: float,
    monitors: int,
    correlation: float,
    safety_target: float,
    monitor_reward: float,
    effort_cost: float,
) -> bool:
    """Whether locally selected effort reaches the declared safety target."""

    requirement = sufficient_effort(
        bad_attempt_rate, monitors, correlation, safety_target
    )
    if not requirement.attainable:
        return False
    assert requirement.effort is not None
    return selected_effort(
        bad_attempt_rate, monitor_reward, effort_cost, correlation
    ) + 1e-12 >= requirement.effort


def assess_control_phase(
    bad_attempt_rate: float,
    monitors: int,
    correlation: float,
    safety_target: float,
    monitor_reward: float,
    effort_cost: float,
    *,
    tolerance: float = 1e-12,
) -> PhaseAssessment:
    """Classify the complete selected-versus-sufficient static phase.

    In the non-trivial attainable region, the exact interior boundary is

    ``effort_cost <= b*(1-rho)*reward / q_sufficient``.

    Because ``q_sufficient`` lies in ``(0, 1]``, clipping the privately
    selected effort to one does not change this sufficiency inequality.
    """

    requirement = sufficient_effort(
        bad_attempt_rate,
        monitors,
        correlation,
        safety_target,
        tolerance=tolerance,
    )
    chosen = selected_effort(
        bad_attempt_rate, monitor_reward, effort_cost, correlation
    )
    selected_bad = bad_finalization_probability(
        bad_attempt_rate, chosen, monitors, correlation
    )

    if not requirement.attainable:
        return PhaseAssessment(
            phase=ControlPhase.STRUCTURALLY_UNATTAINABLE,
            selected_effort=chosen,
            required_effort=None,
            effort_margin=None,
            correlation_floor=requirement.correlation_floor,
            selected_bad_finalization=selected_bad,
            critical_effort_cost=None,
        )

    assert requirement.effort is not None
    required = requirement.effort
    if safety_target >= bad_attempt_rate:
        return PhaseAssessment(
            phase=ControlPhase.NO_MONITORING_REQUIRED,
            selected_effort=chosen,
            required_effort=0.0,
            effort_margin=chosen,
            correlation_floor=requirement.correlation_floor,
            selected_bad_finalization=selected_bad,
            critical_effort_cost=inf,
        )

    private_marginal_return = (
        bad_attempt_rate * (1.0 - correlation) * monitor_reward
    )
    critical_cost = private_marginal_return / required
    effort_margin = chosen - required
    phase = (
        ControlPhase.SUFFICIENT_SELECTED_CONTROL
        if effort_margin + tolerance >= 0.0
        else ControlPhase.UNDERPROVIDED_CONTROL
    )
    return PhaseAssessment(
        phase=phase,
        selected_effort=chosen,
        required_effort=required,
        effort_margin=effort_margin,
        correlation_floor=requirement.correlation_floor,
        selected_bad_finalization=selected_bad,
        critical_effort_cost=critical_cost,
    )


@dataclass(frozen=True)
class DynamicsParameters:
    """Parameters for delayed producer-monitor-commons feedback."""

    monitors: int = 3
    correlation: float = 0.05
    safety_target: float = 0.01
    capture_gain: float = 0.8
    detection_penalty: float = 1.8
    producer_temperature: float = 0.25
    monitor_reward: float = 1.0
    effort_cost: float = 1.0
    producer_adjustment: float = 0.15
    monitor_adjustment: float = 0.15
    regeneration: float = 0.04
    damage: float = 0.20
    debt_recovery: float = 0.05
    initial_health: float = 1.0
    initial_effort: float = 0.25
    initial_bad_attempt_rate: float = 0.20

    def __post_init__(self) -> None:
        if not isinstance(self.monitors, int) or self.monitors < 1:
            raise ValueError("monitors must be a positive integer")
        for name in (
            "correlation",
            "safety_target",
            "producer_adjustment",
            "monitor_adjustment",
            "regeneration",
            "debt_recovery",
            "initial_health",
            "initial_effort",
            "initial_bad_attempt_rate",
        ):
            _probability(name, getattr(self, name))
        _positive("producer_temperature", self.producer_temperature)
        _positive("effort_cost", self.effort_cost)
        if self.capture_gain < 0.0:
            raise ValueError("capture_gain must be nonnegative")
        if self.detection_penalty < 0.0:
            raise ValueError("detection_penalty must be nonnegative")
        if self.monitor_reward < 0.0:
            raise ValueError("monitor_reward must be nonnegative")
        if self.damage < 0.0:
            raise ValueError("damage must be nonnegative")


@dataclass(frozen=True)
class RoundRecord:
    round: int
    commons_health: float
    monitor_effort: float
    bad_attempt_rate: float
    detection_probability: float
    bad_finalization_probability: float
    safety_gap: float
    required_effort: float
    effort_gap: float
    structurally_attainable: bool
    verification_debt: float


def _logistic(value: float) -> float:
    if value >= 0.0:
        z = exp(-value)
        return 1.0 / (1.0 + z)
    z = exp(value)
    return z / (1.0 + z)


def simulate(parameters: DynamicsParameters, steps: int = 250) -> list[RoundRecord]:
    """Simulate delayed local responses and their effect on shared state."""

    if not isinstance(steps, int) or steps < 1:
        raise ValueError("steps must be a positive integer")

    p = parameters
    health = p.initial_health
    effort = p.initial_effort
    bad_rate = p.initial_bad_attempt_rate
    debt = 0.0
    records: list[RoundRecord] = []

    for round_index in range(steps):
        detection = conditional_detection_probability(
            effort, p.monitors, p.correlation
        )
        bad_finalized = bad_finalization_probability(
            bad_rate, effort, p.monitors, p.correlation
        )
        requirement = sufficient_effort(
            bad_rate, p.monitors, p.correlation, p.safety_target
        )
        required_effort = requirement.effort if requirement.effort is not None else inf
        effort_gap = (
            max(0.0, required_effort - effort)
            if requirement.attainable
            else inf
        )
        safety_gap = bad_finalized - p.safety_target
        debt = max(0.0, (1.0 - p.debt_recovery) * debt + safety_gap)

        records.append(
            RoundRecord(
                round=round_index,
                commons_health=health,
                monitor_effort=effort,
                bad_attempt_rate=bad_rate,
                detection_probability=detection,
                bad_finalization_probability=bad_finalized,
                safety_gap=safety_gap,
                required_effort=required_effort,
                effort_gap=effort_gap,
                structurally_attainable=requirement.attainable,
                verification_debt=debt,
            )
        )

        target_bad_rate = _logistic(
            (p.capture_gain - p.detection_penalty * detection)
            / p.producer_temperature
        )
        target_effort = selected_effort(
            bad_rate, p.monitor_reward, p.effort_cost, p.correlation
        )
        health = _clip_probability(
            health + p.regeneration * (1.0 - health) - p.damage * bad_finalized
        )
        bad_rate = _clip_probability(
            bad_rate + p.producer_adjustment * (target_bad_rate - bad_rate)
        )
        effort = _clip_probability(
            effort + p.monitor_adjustment * (target_effort - effort)
        )

    return records
