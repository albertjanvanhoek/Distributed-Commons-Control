import unittest

from distributed_commons.fungal_flow_maintenance import (
    FungalFlowParameters,
    backup_trajectory,
    effective_reinforcement_gain,
    iterate_route_share,
    preferred_maintenance_share,
    simulate_parameter_cases,
    symmetric_locally_stable,
    symmetric_multiplier,
    update_route_share,
    worst_case_backup_share,
)


class FungalFlowMaintenanceTests(unittest.TestCase):
    def test_symmetric_state_is_fixed(self):
        for beta in (0.5, 1.0, 2.0):
            for sensitivity in (0.2, 1.0):
                params = FungalFlowParameters(
                    beta=beta,
                    adjustment=0.4,
                    sensitivity=sensitivity,
                )
                self.assertAlmostEqual(
                    update_route_share(0.5, params),
                    0.5,
                )

    def test_local_multiplier_matches_finite_difference(self):
        params = FungalFlowParameters(
            beta=1.3,
            adjustment=0.4,
            sensitivity=0.7,
        )
        eps = 1e-7
        numerical = (
            update_route_share(0.5 + eps, params)
            - update_route_share(0.5 - eps, params)
        ) / (2.0 * eps)
        self.assertAlmostEqual(
            numerical,
            symmetric_multiplier(params),
            places=6,
        )

    def test_subunit_effective_gain_restores_redundancy(self):
        params = FungalFlowParameters(
            beta=0.8,
            adjustment=0.5,
            sensitivity=1.0,
        )
        self.assertLess(effective_reinforcement_gain(params), 1.0)
        self.assertTrue(symmetric_locally_stable(params))

        trajectory = iterate_route_share(0.51, params, 50)
        self.assertLess(abs(trajectory[-1] - 0.5), abs(trajectory[0] - 0.5))
        self.assertGreater(
            worst_case_backup_share(trajectory[-1]),
            worst_case_backup_share(trajectory[0]),
        )

    def test_unit_effective_gain_is_neutral_for_exact_signal(self):
        params = FungalFlowParameters(
            beta=1.0,
            adjustment=0.5,
            sensitivity=1.0,
        )
        self.assertAlmostEqual(symmetric_multiplier(params), 1.0)
        self.assertFalse(symmetric_locally_stable(params))
        self.assertAlmostEqual(
            preferred_maintenance_share(0.63, 1.0, 1.0),
            0.63,
        )
        self.assertAlmostEqual(update_route_share(0.63, params), 0.63)

    def test_superunit_effective_gain_amplifies_small_asymmetry(self):
        params = FungalFlowParameters(
            beta=1.3,
            adjustment=0.5,
            sensitivity=1.0,
        )
        self.assertGreater(effective_reinforcement_gain(params), 1.0)
        self.assertFalse(symmetric_locally_stable(params))

        trajectory = iterate_route_share(0.51, params, 20)
        self.assertGreater(trajectory[-1], trajectory[0])

        backups = backup_trajectory(0.51, params, 20)
        self.assertLess(backups[-1], backups[0])

    def test_lower_signal_contrast_can_stabilize_same_nonlinearity(self):
        high = FungalFlowParameters(
            beta=1.3,
            adjustment=0.5,
            sensitivity=1.0,
        )
        low = FungalFlowParameters(
            beta=1.3,
            adjustment=0.5,
            sensitivity=0.6,
        )
        self.assertFalse(symmetric_locally_stable(high))
        self.assertTrue(symmetric_locally_stable(low))

        high_z = iterate_route_share(0.51, high, 30)[-1]
        low_z = iterate_route_share(0.51, low, 30)[-1]
        self.assertGreater(abs(high_z - 0.5), 0.01)
        self.assertLess(abs(low_z - 0.5), 0.01)

    def test_backup_share_is_maximal_at_equal_redundancy(self):
        self.assertEqual(worst_case_backup_share(0.5), 0.5)
        for z in (0.0, 0.1, 0.25, 0.75, 0.9, 1.0):
            self.assertLessEqual(worst_case_backup_share(z), 0.5)

    def test_case_summary_exposes_stability_boundary(self):
        cases = [
            (
                "sublinear",
                FungalFlowParameters(0.8, 0.5, 1.0),
            ),
            (
                "neutral",
                FungalFlowParameters(1.0, 0.5, 1.0),
            ),
            (
                "superlinear",
                FungalFlowParameters(1.3, 0.5, 1.0),
            ),
            (
                "attenuated",
                FungalFlowParameters(1.3, 0.5, 0.6),
            ),
        ]
        result = simulate_parameter_cases(cases, z0=0.51, steps=30)
        self.assertLess(result["sublinear"]["multiplier"], 1.0)
        self.assertAlmostEqual(result["neutral"]["multiplier"], 1.0)
        self.assertGreater(result["superlinear"]["multiplier"], 1.0)
        self.assertLess(result["attenuated"]["multiplier"], 1.0)


if __name__ == "__main__":
    unittest.main()
