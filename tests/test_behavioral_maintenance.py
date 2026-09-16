import unittest

from distributed_commons.behavioral_maintenance import (
    MaintenanceParameters,
    boundary_is_preserved,
    correction_is_locally_stable,
    correction_multiplier,
    decentralized_boundary_is_preserved,
    effective_corrective_gain,
    noisy_correction_multiplier,
    overcorrection_threshold,
    passive_renewal_suffices,
    positive_reinforcement_is_beneficial,
    reinforcement_value_numerator,
    repair_is_worthwhile,
    replacement_gap,
    target_baseline_maintenance,
)


class BehavioralMaintenanceTests(unittest.TestCase):
    def test_universal_participant_maintenance_is_false(self):
        p = MaintenanceParameters(
            decay=0.10,
            passive_renewal=0.10,
            viability_floor=0.80,
        )
        self.assertTrue(passive_renewal_suffices(p))
        self.assertEqual(replacement_gap(p), 0.0)
        self.assertTrue(boundary_is_preserved(p, 0.0))

    def test_replacement_gap_is_exact_when_passive_renewal_is_insufficient(self):
        p = MaintenanceParameters(
            decay=0.10,
            passive_renewal=0.03,
            viability_floor=0.80,
        )
        self.assertFalse(passive_renewal_suffices(p))
        self.assertAlmostEqual(replacement_gap(p), 0.05)
        self.assertFalse(boundary_is_preserved(p, 0.049))
        self.assertTrue(boundary_is_preserved(p, 0.05))

    def test_decentralized_local_actions_can_close_gap(self):
        p = MaintenanceParameters(
            decay=0.10,
            passive_renewal=0.03,
            viability_floor=0.80,
        )
        self.assertTrue(
            decentralized_boundary_is_preserved(
                p, [0.01, 0.015, 0.025]
            )
        )
        self.assertFalse(
            decentralized_boundary_is_preserved(
                p, [0.01, 0.015, 0.024]
            )
        )

    def test_more_correction_is_not_always_better(self):
        p = MaintenanceParameters(
            decay=0.20,
            passive_renewal=0.20,
            viability_floor=0.50,
            target=1.0,
        )
        self.assertAlmostEqual(overcorrection_threshold(p), 1.8)
        self.assertTrue(correction_is_locally_stable(p, 1.0))
        self.assertFalse(correction_is_locally_stable(p, 1.9))
        self.assertLess(correction_multiplier(p, 1.9), -1.0)

    def test_signal_fidelity_can_reverse_feedback_sign(self):
        p = MaintenanceParameters(
            decay=0.20,
            passive_renewal=0.20,
            viability_floor=0.50,
            target=1.0,
        )
        self.assertAlmostEqual(effective_corrective_gain(1.0, 0.5), 0.0)
        self.assertLess(effective_corrective_gain(1.0, 0.4), 0.0)
        self.assertGreater(noisy_correction_multiplier(p, 1.0, 0.4), 0.8)
        self.assertLess(noisy_correction_multiplier(p, 1.0, 0.9), 0.8)

    def test_reinforcement_can_amplify_harm_when_signal_is_weak(self):
        bad = reinforcement_value_numerator(
            helpful_prior=0.5,
            signal_fidelity=0.4,
            helpful_benefit=1.0,
            harmful_loss=1.0,
        )
        good = reinforcement_value_numerator(
            helpful_prior=0.5,
            signal_fidelity=0.8,
            helpful_benefit=1.0,
            harmful_loss=1.0,
        )
        self.assertLess(bad, 0.0)
        self.assertGreater(good, 0.0)
        self.assertFalse(
            positive_reinforcement_is_beneficial(0.5, 0.4, 1.0, 1.0)
        )
        self.assertTrue(
            positive_reinforcement_is_beneficial(0.5, 0.8, 1.0, 1.0)
        )

    def test_repair_is_conditional_not_universal(self):
        self.assertTrue(
            repair_is_worthwhile(
                repair_probability=0.8,
                repaired_value=10.0,
                outside_value=4.0,
                repair_cost=3.0,
            )
        )
        self.assertFalse(
            repair_is_worthwhile(
                repair_probability=0.2,
                repaired_value=10.0,
                outside_value=4.0,
                repair_cost=3.0,
            )
        )

    def test_target_baseline_is_replacement_at_target(self):
        p = MaintenanceParameters(
            decay=0.10,
            passive_renewal=0.03,
            viability_floor=0.80,
            target=1.0,
        )
        self.assertAlmostEqual(target_baseline_maintenance(p), 0.07)


if __name__ == "__main__":
    unittest.main()
