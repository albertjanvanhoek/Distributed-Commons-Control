"""Neutral participant-to-network viability contribution model.

The model deliberately contains no ecological, protocol, institutional, or
biological semantics. It studies one declared corrective loop:

    participants -> failure topology -> structural escape -> viability margin.

A participant is characterized only by the failure causes that disable its
corrective action. Failure causes are independent Bernoulli events in this
first exact model. A disturbance escapes when every present participant is
disabled by at least one active cause.

For coalition S, let pi(S) be structural escape probability and let epsilon be
the declared maximum acceptable harmful-finalization probability. If b is the
disturbance-attempt rate, safety requires

    b * pi(S) <= epsilon.

The viability margin is therefore

    M(S) = max b in [0,1] satisfying the inequality
         = min(1, epsilon / pi(S)),

with M(S)=1 when pi(S)=0.

This is a capacity-to-withstand-disturbance measure, not a measure of current
shared-state level. Dynamic models may later condition M on a state (X, C),
where X is current shared state and C is a slow corrective-capacity stock.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from math import factorial, isfinite
from typing import Iterable


@dataclass(frozen=True)
class FailureCause:
    name: str
    probability: float

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("failure-cause name must be nonempty")
        if not isfinite(self.probability) or not 0.0 <= self.probability <= 1.0:
            raise ValueError("failure-cause probability must lie in [0,1]")


@dataclass(frozen=True)
class Participant:
    name: str
    vulnerabilities: frozenset[str]

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("participant name must be nonempty")


@dataclass(frozen=True)
class FailureTopology:
    causes: tuple[FailureCause, ...]
    participants: tuple[Participant, ...]

    def __post_init__(self) -> None:
        cause_names = [cause.name for cause in self.causes]
        participant_names = [participant.name for participant in self.participants]
        if len(cause_names) != len(set(cause_names)):
            raise ValueError("failure-cause names must be unique")
        if len(participant_names) != len(set(participant_names)):
            raise ValueError("participant names must be unique")
        known = set(cause_names)
        for participant in self.participants:
            unknown = participant.vulnerabilities - known
            if unknown:
                raise ValueError(
                    f"participant {participant.name} has unknown causes: "
                    f"{sorted(unknown)}"
                )

    @property
    def participant_names(self) -> frozenset[str]:
        return frozenset(p.name for p in self.participants)

    def _coalition(self, coalition: Iterable[str]) -> frozenset[str]:
        selected = frozenset(coalition)
        unknown = selected - self.participant_names
        if unknown:
            raise ValueError(f"unknown participants: {sorted(unknown)}")
        return selected

    def escape_probability(self, coalition: Iterable[str]) -> float:
        """Exact probability that every participant in the coalition is disabled."""

        selected = self._coalition(coalition)
        if not selected:
            return 1.0

        participants = {
            p.name: p for p in self.participants if p.name in selected
        }
        causes = self.causes
        total = 0.0
        for mask in range(1 << len(causes)):
            active: set[str] = set()
            probability = 1.0
            for index, cause in enumerate(causes):
                if mask & (1 << index):
                    active.add(cause.name)
                    probability *= cause.probability
                else:
                    probability *= 1.0 - cause.probability

            all_disabled = all(
                bool(participant.vulnerabilities & active)
                for participant in participants.values()
            )
            if all_disabled:
                total += probability
        return total

    def viability_margin(
        self, coalition: Iterable[str], safety_target: float
    ) -> float:
        """Largest disturbance-attempt rate compatible with the safety target."""

        if not isfinite(safety_target) or not 0.0 <= safety_target <= 1.0:
            raise ValueError("safety_target must lie in [0,1]")
        escape = self.escape_probability(coalition)
        if escape == 0.0:
            return 1.0
        return min(1.0, safety_target / escape)

    def marginal_contribution(
        self,
        participant: str,
        coalition_without: Iterable[str],
        safety_target: float,
    ) -> float:
        """Change in viability margin from adding one participant to a coalition."""

        coalition = self._coalition(coalition_without)
        if participant not in self.participant_names:
            raise ValueError(f"unknown participant: {participant}")
        if participant in coalition:
            raise ValueError("participant must not already be in coalition")
        return (
            self.viability_margin(coalition | {participant}, safety_target)
            - self.viability_margin(coalition, safety_target)
        )

    def leave_one_out_contribution(
        self,
        participant: str,
        safety_target: float,
        coalition: Iterable[str] | None = None,
    ) -> float:
        """Loss of viability margin when a participant is removed."""

        selected = (
            self.participant_names
            if coalition is None
            else self._coalition(coalition)
        )
        if participant not in selected:
            raise ValueError("participant must belong to the selected coalition")
        return (
            self.viability_margin(selected, safety_target)
            - self.viability_margin(selected - {participant}, safety_target)
        )

    def shapley_values(self, safety_target: float) -> dict[str, float]:
        """Shapley attribution of total margin above the empty-coalition baseline."""

        names = sorted(self.participant_names)
        n = len(names)
        if n == 0:
            return {}

        result: dict[str, float] = {}
        for participant in names:
            others = [name for name in names if name != participant]
            value = 0.0
            for size in range(len(others) + 1):
                weight = (
                    factorial(size)
                    * factorial(n - size - 1)
                    / factorial(n)
                )
                for subset_tuple in combinations(others, size):
                    subset = frozenset(subset_tuple)
                    value += weight * self.marginal_contribution(
                        participant, subset, safety_target
                    )
            result[participant] = value
        return result

    def harsanyi_dividends(
        self, safety_target: float
    ) -> dict[frozenset[str], float]:
        """Exact inclusion-exclusion interaction decomposition of M(S).

        The empty-coalition baseline is omitted. The sum of all returned
        dividends equals M(N)-M(empty). Terms of size >=2 are non-additive
        interaction contributions; unlike Shapley values they are not allocated
        back to individuals.
        """

        names = sorted(self.participant_names)
        dividends: dict[frozenset[str], float] = {}
        for size in range(1, len(names) + 1):
            for coalition_tuple in combinations(names, size):
                coalition = frozenset(coalition_tuple)
                value = 0.0
                coalition_list = sorted(coalition)
                for sub_size in range(size + 1):
                    for subset_tuple in combinations(coalition_list, sub_size):
                        subset = frozenset(subset_tuple)
                        sign = -1.0 if (size - sub_size) % 2 else 1.0
                        value += sign * self.viability_margin(
                            subset, safety_target
                        )
                dividends[coalition] = value
        return dividends


def two_cause_example(
    rho: float = 0.05,
) -> FailureTopology:
    """Two shared-mode participants plus one independent-mode participant.

    Participants A1 and A2 are disabled only by cause A. Participant B1 is
    disabled only by independent cause B. With both cause probabilities rho:

      pi({A1,A2}) = rho
      pi({A1,A2,B1}) = rho^2.
    """

    if not isfinite(rho) or not 0.0 <= rho <= 1.0:
        raise ValueError("rho must lie in [0,1]")
    return FailureTopology(
        causes=(
            FailureCause("A", rho),
            FailureCause("B", rho),
        ),
        participants=(
            Participant("A1", frozenset({"A"})),
            Participant("A2", frozenset({"A"})),
            Participant("B1", frozenset({"B"})),
        ),
    )
