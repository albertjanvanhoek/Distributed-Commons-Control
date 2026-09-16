import math
import unittest
from dataclasses import replace

from distributed_commons import (
    DynamicsParameters,
    bad_finalization_probability,
    conditional_escape_probability,
    monitor_objective,
    selected_control_is_sufficient,
    selected_effort,
    simulate,
    sufficient_effort,
)


class StaticModelTests(unittest.TestCase):
    def test_independent_three_monitor_escape(self) -> None:
        self.assertAlmostEqual(conditional_escape_probability(0.5, 3, 0.0), 0.125)

    def test_perfect_effort_leaves_correlation_floor(self) -> None:
        self.assertAlmostEqual(
            bad_finalization_probability(0.2, 1.0, 9, 0.15), 0.03
        )

    def test_more_same_mode_monitors_cannot_cross_floor(self) -> None:
        floor = 0.2 * 0.15
        for monitors in (1, 3, 10, 100):
            observed = bad_finalization_probability(0.2, 0.999, monitors, 0.15)
            self.assertGreaterEqual(observed + 1e-15, floor)

    def test_sufficient_effort_hits_target(self) -> None:
        requirement = sufficient_effort(0.1, 3, 0.0, 0.01)
        self.assertTrue(requirement.attainable)
        assert requirement.effort is not None
        expected = 1.0 - 0.1 ** (1.0 / 3.0)
        self.assertAlmostEqual(requirement.effort, expected)
        self.assertAlmostEqual(
            bad_finalization_probability(0.1, requirement.effort, 3, 0.0),
            0.01,
        )

    def test_target_below_correlation_floor_is_unattainable(self) -> None:
        requirement = sufficient_effort(0.1, 3, 0.10, 0.005)
        self.assertFalse(requirement.attainable)
        self.assertIsNone(requirement.effort)
        self.assertAlmostEqual(requirement.correlation_floor, 0.01)

    def test_selected_effort_is_quadratic_optimum(self) -> None:
        b, reward, cost = 0.2, 1.0, 1.0
        optimum = selected_effort(b, reward, cost)
        self.assertAlmostEqual(optimum, 0.2)
        for effort in (0.0, 0.1, 0.2, 0.5, 1.0):
            self.assertLessEqual(
                monitor_objective(effort, b, reward, cost),
                monitor_objective(optimum, b, reward, cost) + 1e-12,
            )

    def test_common_mode_failure_reduces_selected_effort(self) -> None:
        independent = selected_effort(0.4, 1.0, 1.0, correlation=0.0)
        correlated = selected_effort(0.4, 1.0, 1.0, correlation=0.5)
        self.assertAlmostEqual(correlated, 0.5 * independent)

    def test_selected_control_can_underprovide(self) -> None:
        self.assertFalse(
            selected_control_is_sufficient(
                bad_attempt_rate=0.1,
                monitors=3,
                correlation=0.0,
                safety_target=0.01,
                monitor_reward=1.0,
                effort_cost=1.0,
            )
        )

    def test_invalid_probability_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            conditional_escape_probability(1.1, 3, 0.0)


class DynamicModelTests(unittest.TestCase):
    def test_simulation_is_bounded_and_deterministic(self) -> None:
        parameters = DynamicsParameters()
        first = simulate(parameters, 80)
        second = simulate(parameters, 80)
        self.assertEqual(first, second)
        self.assertEqual(len(first), 80)
        for row in first:
            self.assertGreaterEqual(row.commons_health, 0.0)
            self.assertLessEqual(row.commons_health, 1.0)
            self.assertGreaterEqual(row.monitor_effort, 0.0)
            self.assertLessEqual(row.monitor_effort, 1.0)
            self.assertGreaterEqual(row.bad_attempt_rate, 0.0)
            self.assertLessEqual(row.bad_attempt_rate, 1.0)
            self.assertGreaterEqual(row.verification_debt, 0.0)

    def test_higher_common_mode_failure_worsens_outcome(self) -> None:
        base = DynamicsParameters(effort_cost=0.5)
        low = simulate(replace(base, correlation=0.0), 300)
        high = simulate(replace(base, correlation=0.30), 300)
        low_tail = low[-50:]
        high_tail = high[-50:]
        low_bad = sum(r.bad_finalization_probability for r in low_tail) / 50
        high_bad = sum(r.bad_finalization_probability for r in high_tail) / 50
        low_health = sum(r.commons_health for r in low_tail) / 50
        high_health = sum(r.commons_health for r in high_tail) / 50
        self.assertGreater(high_bad, low_bad)
        self.assertLess(high_health, low_health)

    def test_structural_unattainability_is_recorded(self) -> None:
        parameters = DynamicsParameters(
            correlation=0.5,
            safety_target=0.001,
            initial_bad_attempt_rate=0.2,
        )
        record = simulate(parameters, 1)[0]
        self.assertFalse(record.structurally_attainable)
        self.assertTrue(math.isinf(record.required_effort))


if __name__ == "__main__":
    unittest.main()
