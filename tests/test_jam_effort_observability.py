import unittest

from distributed_commons.jam_effort_observability import (
    certified_required_effort_observability,
    effort_channel_can_close_gap,
    maintenance_selection_margin,
    required_effort_observability,
)
from distributed_commons.jam_maintenance import JamMaintenanceState


class JamEffortObservabilityTests(unittest.TestCase):
    def test_observability_threshold_closes_selection_gap(self):
        threshold = required_effort_observability(
            reward_budget=2.0,
            compute_cost=1.0,
            invalid_rate=0.001,
            exposure_probability=1.0,
            fault_loss=10.0,
        )
        self.assertAlmostEqual(threshold, 0.495)

        below = maintenance_selection_margin(
            0.49, 2.0, 1.0, 0.001, 1.0, 10.0
        )
        above = maintenance_selection_margin(
            0.50, 2.0, 1.0, 0.001, 1.0, 10.0
        )
        self.assertLess(below, 0.0)
        self.assertGreaterEqual(above, 0.0)

    def test_reward_budget_can_be_too_small_even_with_perfect_observability(self):
        self.assertFalse(
            effort_channel_can_close_gap(
                reward_budget=0.5,
                compute_cost=1.0,
                invalid_rate=0.001,
                exposure_probability=1.0,
                fault_loss=10.0,
            )
        )
        self.assertGreater(
            required_effort_observability(
                0.5, 1.0, 0.001, 1.0, 10.0
            ),
            1.0,
        )

    def test_zero_observability_removes_reward_effect(self):
        margin_small_reward = maintenance_selection_margin(
            0.0, 1.0, 1.0, 0.001, 1.0, 10.0
        )
        margin_huge_reward = maintenance_selection_margin(
            0.0, 1000.0, 1.0, 0.001, 1.0, 10.0
        )
        self.assertAlmostEqual(margin_small_reward, -0.99)
        self.assertAlmostEqual(margin_huge_reward, -0.99)

    def test_structural_collapse_raises_observability_requirement(self):
        strong = JamMaintenanceState(
            validator_count=1023,
            adversarial_count=205,
            vulnerable_honest_count=82,
            no_show_prone_count=153,
            s_delta=2.0,
        )
        weak = JamMaintenanceState(
            validator_count=1023,
            adversarial_count=205,
            vulnerable_honest_count=400,
            no_show_prone_count=153,
            s_delta=2.0,
        )

        strong_req = certified_required_effort_observability(
            strong,
            reward_budget=2.0,
            compute_cost=1.0,
            invalid_rate=0.1,
            fault_loss=10.0,
        )
        weak_req = certified_required_effort_observability(
            weak,
            reward_budget=2.0,
            compute_cost=1.0,
            invalid_rate=0.1,
            fault_loss=10.0,
        )

        self.assertGreater(weak.attack_bound, strong.attack_bound)
        self.assertGreater(weak_req, strong_req)

    def test_fault_deterrence_can_make_effort_observability_unnecessary(self):
        threshold = required_effort_observability(
            reward_budget=1.0,
            compute_cost=1.0,
            invalid_rate=0.5,
            exposure_probability=1.0,
            fault_loss=3.0,
        )
        self.assertLessEqual(threshold, 0.0)


if __name__ == "__main__":
    unittest.main()
