"""Rate-limited safety feedback; conditional on a valid observation envelope.

The controller sets aggregate monitoring effort directly. Financing and
strategic compliance are not endogenous in this extension.
"""
from dataclasses import dataclass
from math import isfinite

from .model import sufficient_effort, selected_effort, bad_finalization_probability


@dataclass(frozen=True)
class FeedbackParameters:
    monitors: int = 3
    correlation: float = 0.02
    safety_target: float = 0.03
    delay: int = 3
    upward_bound: float = 0.02
    depreciation: float = 0.05
    capacity: float = 0.06
    initial_effort: float = 0.5
    reward: float = 1.0
    cost: float = 0.5

    def __post_init__(self):
        sufficient_effort(0.2, self.monitors, self.correlation, self.safety_target)
        if isinstance(self.delay, bool) or not isinstance(self.delay, int) or self.delay < 0:
            raise ValueError('delay must be a nonnegative integer')
        for key in ('upward_bound', 'depreciation', 'capacity', 'initial_effort'):
            x = getattr(self, key)
            if not isfinite(x) or not 0 <= x <= 1:
                raise ValueError(f'{key} must be finite and in [0,1]')
        if not isfinite(self.reward) or self.reward < 0 or not isfinite(self.cost) or self.cost <= 0:
            raise ValueError('reward must be finite/nonnegative and cost finite/positive')


def simulate_feedback(attempt_rates, p=FeedbackParameters(), policy='robust'):
    """At t, observe b[max(0,t-delay)] and choose effort for t+1.

    robust: target safety for an upper envelope at t+1;
    reactive: target safety for the stale observation;
    private: target the previous quadratic individual optimum;
    fixed: target initial effort. All use the same physical actuator.

    Report conditional per-round failure probabilities, not sampled failures.
    """
    rates = list(attempt_rates)
    if not rates or any(not isfinite(b) or not 0 <= b <= 1 for b in rates):
        raise ValueError('attempt rates must be a nonempty finite probability sequence')
    if policy not in {'robust', 'reactive', 'private', 'fixed'}:
        raise ValueError('unknown policy')
    q = p.initial_effort
    rows = [dict(round=0, effort=q, bad_rate=rates[0],
                 failure=bad_finalization_probability(rates[0], q, p.monitors, p.correlation),
                 effort_added=0.0, envelope_valid=None, certified=None,
                 required=None, capacity_shortfall=None)]
    for t in range(len(rates)-1):
        index = max(0, t-p.delay)
        observed = rates[index]
        upper = min(1.0, observed + (t+1-index)*p.upward_bound)
        target_rate = upper if policy == 'robust' else observed
        req = sufficient_effort(target_rate, p.monitors, p.correlation, p.safety_target)
        requested = req.effort if req.attainable else 1.0
        if policy == 'private':
            requested = selected_effort(observed, p.reward, p.cost, p.correlation)
        elif policy == 'fixed':
            requested = p.initial_effort
        retained = (1-p.depreciation)*q
        ceiling = min(1.0, retained+p.capacity)
        next_q = min(ceiling, max(retained, requested))
        valid = rates[t+1] <= upper + 1e-14
        # Certification uses the robust envelope even for comparison policies.
        robust_req = sufficient_effort(upper, p.monitors, p.correlation, p.safety_target)
        required = robust_req.effort
        shortfall = None if required is None else max(0.0, required-ceiling)
        certified = (valid and required is not None and next_q+1e-14 >= required)
        rows.append(dict(round=t+1, effort=next_q, bad_rate=rates[t+1],
                         failure=bad_finalization_probability(rates[t+1], next_q, p.monitors, p.correlation),
                         effort_added=next_q-retained, envelope_valid=valid,
                         certified=certified, required=required, capacity_shortfall=shortfall))
        q = next_q
    return rows
