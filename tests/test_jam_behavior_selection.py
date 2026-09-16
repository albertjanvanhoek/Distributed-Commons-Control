import unittest

from distributed_commons.jam_behavior_selection import (
    AuditBehaviorPayoffs,
    certified_exposure_lower_bound,
    certified_required_reward_advantage_over_rubber,
    required_compute_reward_advantage_over_no_show,
    required_compute_reward_advantage_over_rubber,
    rubber_stamp_beats_no_show,
)
from distributed_commons.jam_maintenance import JamMaintenanceState


class JamBehaviorSelectionTests(unittest.TestCase):
    def test_compute_selection_inequalities(self):
        game = AuditBehaviorPayoffs(
            compute_cost=1.0,
            reward_compute=1.2,
            reward_rubber_stamp=0.3,
            reward_no_show=0.1,
            invalid_rate=0.1,
            exposure_probability=0.9,
            fault_loss=2.0,
        )
        self.assertGreaterEqual(game.compute_vs_rubber_margin, 0.0)
        self.assertGreaterEqual(game.compute_vs_no_show_margin, 0.0)
        self.assertTrue(game.compute_selected)

    def test_low_invalid_rate_recreates_verifier_dilemma(self):
        threshold = required_compute_reward_advantage_over_rubber(
            compute_cost=1.0,
            invalid_rate=0.001,
            exposure_probability=1.0,
            fault_loss=10.0,
        )
        self.assertAlmostEqual(threshold, 0.99)

    def test_fault_penalty_can_substitute_for_reward_advantage(self):
        threshold = required_compute_reward_advantage_over_rubber(
            compute_cost=1.0,
            invalid_rate=0.5,
            exposure_probability=1.0,
            fault_loss=3.0,
        )
        self.assertLess(threshold, 0.0)

    def test_no_show_gap_equals_compute_cost(self):
        self.assertEqual(
            required_compute_reward_advantage_over_no_show(1.25),
            1.25,
        )

    def test_silent_rubber_stamp_can_beat_visible_no_show_when_invalid_is_rare(self):
        self.assertTrue(
            rubber_stamp_beats_no_show(
                reward_rubber_stamp=0.0,
                reward_no_show=-0.2,
                invalid_rate=0.001,
                exposure_probability=1.0,
                fault_loss=10.0,
            )
        )

    def test_certified_exposure_comes_from_attack_bound(self):
        state = JamMaintenanceState(
            validator_count=1023,
            adversarial_count=205,
            vulnerable_honest_count=82,
            no_show_prone_count=153,
            s_delta=2.0,
        )
        exposure = certified_exposure_lower_bound(state)
        self.assertAlmostEqual(exposure, 1.0 - state.attack_bound)
        self.assertGreater(exposure, 0.999)

    def test_structural_failure_weakens_penalty_deterrence(self):
        safe = JamMaintenanceState(
            validator_count=1023,
            adversarial_count=205,
            vulnerable_honest_count=82,
            no_show_prone_count=153,
            s_delta=2.0,
        )
        weak = JamMaintenanceState(
            validator_count=1023,
            adversarial_count=205,
            vulnerable_honest_count=300,
            no_show_prone_count=153,
            s_delta=2.0,
        )

        required_safe = certified_required_reward_advantage_over_rubber(
            safe,
            compute_cost=1.0,
            invalid_rate=0.1,
            fault_loss=10.0,
        )
        required_weak = certified_required_reward_advantage_over_rubber(
            weak,
            compute_cost=1.0,
            invalid_rate=0.1,
            fault_loss=10.0,
        )

        self.assertGreater(weak.attack_bound, safe.attack_bound)
        self.assertGreater(required_weak, required_safe)


if __name__ == "__main__":
    unittest.main()
