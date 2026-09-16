"""Closed-loop commons models.

This module closes the return path from commons health X to future control.
The default closure funds monitoring partly from the commons,

    r(X) = reward_scale * (baseline_funding + reward_health_weight * X).

Two alternative return paths are included for robustness tests:

    c(X) = effort_cost * exp(cost_stress * (1 - X))
    g(X) = capture_gain + capture_stress * (1 - X).

All three can be combined, but the experiments also test them separately.
For fixed X the producer-monitor subsystem has a unique behavioural fixed
point. The reduced commons analysis traces

    delta*(X) = gamma * (1-X) / P*(X).

For the declared discrete-time commons map with 0 < gamma <= 1 and P*(X)
positive and nonincreasing, local linear stability of an interior equilibrium
is equivalent to loop gain eta(X) < 1, where

    eta(X) = -(1-X) * d ln P*(X) / dX.

The algebraic multiplier equivalence is formalized in Lean; existence and
location of folds for the concrete closures are numerical results.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from math import exp, inf, isfinite

from .model import (
    conditional_escape_probability,
    producer_bad_attempt_floor,
    producer_target_bad_rate,
)


@dataclass(frozen=True)
class ClosedLoopParameters:
    monitors: int = 5
    correlation: float = 0.05
    effort_cost: float = 0.25
    reward_scale: float = 1.0
    baseline_funding: float = 0.0
    reward_health_weight: float = 1.0
    cost_stress: float = 0.0
    capture_gain: float = 0.8
    capture_stress: float = 0.0
    detection_penalty: float = 1.8
    producer_temperature: float = 0.25
    regeneration: float = 0.04
    damage: float = 0.20

    def __post_init__(self) -> None:
        if isinstance(self.monitors, bool) or not isinstance(self.monitors, int) or self.monitors < 1:
            raise ValueError("monitors must be a positive integer")
        if not 0.0 <= self.correlation < 1.0:
            raise ValueError("correlation must lie in [0, 1)")
        if not 0.0 < self.regeneration <= 1.0:
            raise ValueError("regeneration must lie in (0, 1]")
        for name in ("effort_cost", "producer_temperature"):
            value = getattr(self, name)
            if not isfinite(value) or value <= 0.0:
                raise ValueError(f"{name} must be finite and positive")
        for name in (
            "reward_scale",
            "baseline_funding",
            "reward_health_weight",
            "cost_stress",
            "capture_gain",
            "capture_stress",
            "detection_penalty",
            "damage",
        ):
            value = getattr(self, name)
            if not isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")


def _health(health: float) -> float:
    health = float(health)
    if not isfinite(health) or not 0.0 <= health <= 1.0:
        raise ValueError("health must lie in [0, 1]")
    return health


def reward(health: float, p: ClosedLoopParameters) -> float:
    health = _health(health)
    return p.reward_scale * (
        p.baseline_funding + p.reward_health_weight * health
    )


def effective_effort_cost(health: float, p: ClosedLoopParameters) -> float:
    health = _health(health)
    return p.effort_cost * exp(p.cost_stress * (1.0 - health))


def effective_capture_gain(health: float, p: ClosedLoopParameters) -> float:
    health = _health(health)
    return p.capture_gain + p.capture_stress * (1.0 - health)


def _monitor_response(
    bad_rate: float, health: float, p: ClosedLoopParameters
) -> float:
    raw = (
        bad_rate
        * (1.0 - p.correlation)
        * reward(health, p)
        / effective_effort_cost(health, p)
    )
    return min(1.0, max(0.0, raw))


def _producer_response(
    effort: float, health: float, p: ClosedLoopParameters
) -> float:
    detection = 1.0 - conditional_escape_probability(
        effort, p.monitors, p.correlation
    )
    return producer_target_bad_rate(
        detection,
        effective_capture_gain(health, p),
        p.detection_penalty,
        p.producer_temperature,
    )


@dataclass(frozen=True)
class BehaviouralEquilibrium:
    bad_attempt_rate: float
    effort: float
    bad_finalization: float


def behavioural_equilibrium(
    health: float, p: ClosedLoopParameters, *, iterations: int = 100
) -> BehaviouralEquilibrium:
    """Unique producer-monitor fixed point at fixed commons health.

    For fixed X, monitor effort is nondecreasing in b, collective detection is
    nondecreasing in effort, and producer response is nonincreasing in
    detection. Hence response(b)-b is strictly decreasing. Its value is
    positive at b=0 and negative at b=1, so bisection finds the unique root.
    """

    health = _health(health)
    if isinstance(iterations, bool) or not isinstance(iterations, int) or iterations < 1:
        raise ValueError("iterations must be a positive integer")
    lo, hi = 0.0, 1.0
    for _ in range(iterations):
        mid = 0.5 * (lo + hi)
        target = _producer_response(
            _monitor_response(mid, health, p), health, p
        )
        if target > mid:
            lo = mid
        else:
            hi = mid
    b = 0.5 * (lo + hi)
    q = _monitor_response(b, health, p)
    return BehaviouralEquilibrium(
        b,
        q,
        b * conditional_escape_probability(q, p.monitors, p.correlation),
    )


def equilibrium_damage(health: float, p: ClosedLoopParameters) -> float:
    """Damage coefficient delta at which health is an interior equilibrium."""

    health = _health(health)
    bad = behavioural_equilibrium(health, p).bad_finalization
    return p.regeneration * (1.0 - health) / bad


def loop_gain(
    health: float, p: ClosedLoopParameters, *, step: float = 1e-5
) -> float:
    """Numerical eta(X)=-(1-X)d ln P*/dX."""

    health = _health(health)
    if not isfinite(step) or step <= 0.0:
        raise ValueError("step must be positive")
    lo = max(0.0, health - step)
    hi = min(1.0, health + step)
    if lo == hi:
        raise ValueError("finite-difference interval collapsed")
    p_lo = behavioural_equilibrium(lo, p).bad_finalization
    p_hi = behavioural_equilibrium(hi, p).bad_finalization
    p_mid = behavioural_equilibrium(health, p).bad_finalization
    return -(1.0 - health) * (p_hi - p_lo) / (hi - lo) / p_mid


def max_loop_gain(
    p: ClosedLoopParameters, *, points: int = 400
) -> tuple[float, float]:
    """Maximum numerical loop gain and the health at which it occurs."""

    if isinstance(points, bool) or not isinstance(points, int) or points < 2:
        raise ValueError("points must be an integer >= 2")
    xs = [0.999 * i / (points - 1) for i in range(points)]
    values = [loop_gain(x, p) for x in xs]
    i = max(range(points), key=values.__getitem__)
    return values[i], xs[i]


def critical_return_strength(
    p: ClosedLoopParameters,
    field: str,
    *,
    lo: float = 0.0,
    hi: float,
    points: int = 400,
) -> float:
    """Smallest tested closure strength whose maximum loop gain reaches one.

    This is a numerical threshold for a one-parameter closure family, not a
    theorem about arbitrary return paths. The field is restricted to the two
    alternative closure-strength parameters used in Experiment 2.
    """

    if field not in {"cost_stress", "capture_stress"}:
        raise ValueError("field must be cost_stress or capture_stress")
    if not isfinite(lo) or not isfinite(hi) or lo < 0.0 or hi <= lo:
        raise ValueError("require finite 0 <= lo < hi")

    def peak(value: float) -> float:
        gain, _ = max_loop_gain(replace(p, **{field: value}), points=points)
        return gain

    if peak(lo) >= 1.0:
        return lo
    if peak(hi) < 1.0:
        raise ValueError("loop gain remains below one at the upper bracket")
    for _ in range(50):
        mid = 0.5 * (lo + hi)
        if peak(mid) >= 1.0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def common_mode_finalization_floor(p: ClosedLoopParameters) -> float:
    """State-independent lower bound inherited from common-mode failure."""

    return p.correlation * producer_bad_attempt_floor(
        p.correlation,
        p.capture_gain,
        p.detection_penalty,
        p.producer_temperature,
    )


def hysteresis_ratio_upper_bound(p: ClosedLoopParameters) -> float:
    """Upper bound on fold/collapse ratio from the common-mode floor."""

    floor = common_mode_finalization_floor(p)
    if floor == 0.0:
        return inf
    p0 = behavioural_equilibrium(0.0, p).bad_finalization
    return p0 / floor


@dataclass(frozen=True)
class HysteresisWindow:
    """Damage range with coexisting healthy and collapsed attractors."""

    collapse_damage: float
    fold_damage: float
    fold_health: float

    @property
    def ratio(self) -> float:
        return self.fold_damage / self.collapse_damage


def bifurcation_curve(
    p: ClosedLoopParameters, points: int = 400
) -> list[tuple[float, float, bool]]:
    """Rows (health, damage, stable) tracing interior equilibria.

    The stability flag uses the sign of the equilibrium-damage slope, which
    is equivalent to eta<1 for the declared reduced map under the assumptions
    documented above.
    """

    if isinstance(points, bool) or not isinstance(points, int) or points < 2:
        raise ValueError("points must be an integer >= 2")
    xs = [i / points for i in range(points)]
    ds = [equilibrium_damage(x, p) for x in xs]
    rows = []
    for i, (x, d) in enumerate(zip(xs, ds)):
        j = min(i + 1, points - 1)
        k = max(i - 1, 0)
        rows.append((x, d, ds[j] - ds[k] < 0.0))
    return rows


def hysteresis_window(
    p: ClosedLoopParameters, points: int = 2000
) -> HysteresisWindow | None:
    """Return the collapse-to-fold window, assuming a unimodal damage curve."""

    if isinstance(points, bool) or not isinstance(points, int) or points < 3:
        raise ValueError("points must be an integer >= 3")
    xs = [i / points for i in range(points)]
    ds = [equilibrium_damage(x, p) for x in xs]
    i = max(range(points), key=ds.__getitem__)
    if i == 0:
        return None
    a, b = xs[max(i - 1, 0)], xs[min(i + 1, points - 1)]
    golden = 0.6180339887498949
    for _ in range(60):
        c1 = b - golden * (b - a)
        c2 = a + golden * (b - a)
        if equilibrium_damage(c1, p) > equilibrium_damage(c2, p):
            b = c2
        else:
            a = c1
    x_fold = 0.5 * (a + b)
    return HysteresisWindow(
        ds[0],
        equilibrium_damage(x_fold, p),
        x_fold,
    )


def critical_baseline_funding(
    p: ClosedLoopParameters, hi: float = 10.0
) -> float:
    """Baseline funding at which the default reward-funded fold disappears.

    This diagnostic varies kappa while holding the other closure strengths
    fixed. For the reported default family the first loss of the fold occurs
    at eta(0+)=1.
    """

    if not isfinite(hi) or hi <= 0.0:
        raise ValueError("hi must be positive")

    def gain(kappa: float) -> float:
        return loop_gain(1e-4, replace(p, baseline_funding=kappa))

    lo = 0.0
    if gain(hi) > 1.0:
        raise ValueError("loop gain still exceeds one at the upper bracket")
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if gain(mid) > 1.0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


@dataclass(frozen=True)
class ClosedLoopRecord:
    round: int
    health: float
    bad_attempt_rate: float
    effort: float
    bad_finalization: float


def simulate_closed_loop(
    p: ClosedLoopParameters,
    *,
    initial_health: float,
    initial_bad_attempt_rate: float,
    initial_effort: float | None = None,
    adjustment: float = 0.15,
    steps: int = 3000,
) -> list[ClosedLoopRecord]:
    """Full discrete-time model with finite producer and monitor adjustment."""

    x = _health(initial_health)
    b = float(initial_bad_attempt_rate)
    if not isfinite(b) or not 0.0 <= b <= 1.0:
        raise ValueError("initial_bad_attempt_rate must lie in [0, 1]")
    if initial_effort is None:
        q = _monitor_response(b, x, p)
    else:
        q = float(initial_effort)
        if not isfinite(q) or not 0.0 <= q <= 1.0:
            raise ValueError("initial_effort must lie in [0, 1]")
    if not isfinite(adjustment) or not 0.0 < adjustment <= 1.0:
        raise ValueError("adjustment must lie in (0, 1]")
    if isinstance(steps, bool) or not isinstance(steps, int) or steps < 1:
        raise ValueError("steps must be a positive integer")

    out: list[ClosedLoopRecord] = []
    for t in range(steps):
        escape = conditional_escape_probability(
            q, p.monitors, p.correlation
        )
        bad = b * escape
        out.append(ClosedLoopRecord(t, x, b, q, bad))
        b_target = _producer_response(q, x, p)
        q_target = _monitor_response(b, x, p)
        x = min(
            1.0,
            max(
                0.0,
                x
                + p.regeneration * (1.0 - x)
                - p.damage * bad,
            ),
        )
        b += adjustment * (b_target - b)
        q += adjustment * (q_target - q)
    return out


def final_health(p: ClosedLoopParameters, **kwargs: object) -> float:
    return simulate_closed_loop(p, **kwargs)[-1].health


def basin_threshold(
    p: ClosedLoopParameters,
    initial_bad_attempt_rate: float,
    *,
    adjustment: float = 0.15,
    steps: int = 3000,
    collapsed_below: float = 0.05,
) -> float | None:
    """Smallest initial health from which the full model recovers.

    Monitors start at their private optimum for the supplied initial attack
    rate. Returns None if all initial health values recover, and 1.0 if none
    recover.
    """

    if not isfinite(collapsed_below) or not 0.0 <= collapsed_below <= 1.0:
        raise ValueError("collapsed_below must lie in [0, 1]")

    def recovers(x0: float) -> bool:
        return final_health(
            p,
            initial_health=x0,
            initial_bad_attempt_rate=initial_bad_attempt_rate,
            adjustment=adjustment,
            steps=steps,
        ) > collapsed_below

    if recovers(0.0):
        return None
    if not recovers(1.0):
        return 1.0
    lo, hi = 0.0, 1.0
    for _ in range(30):
        mid = 0.5 * (lo + hi)
        if recovers(mid):
            hi = mid
        else:
            lo = mid
    return hi
