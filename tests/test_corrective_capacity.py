import unittest

from distributed_commons.corrective_capacity import (
    CapacityParameters,
    local_shared_state_multiplier,
    maintenance_shortfall,
    post_shock_state,
    quiet_step,
    quiet_trajectory,
    required_maintenance_for_capacity,
    shock_is_viable,
    shock_margin,
    uncapped_shock_margin,
)


class CorrectiveCapacityTests(unittest.TestCase):
    def setUp(self):
        self.p = CapacityParameters(
            regeneration=0.10,
            capacity_decay=0.05,
            correction_efficiency=0.50,
            viability_floor=0.70,
        )

    def test_margin_matches_shock_boundary(self):
        x = 0.90
        c = 0.20
        margin = uncapped_shock_margin(x, c, self.p)
        self.assertAlmostEqual(margin, 0.30)
        self.assertTrue(shock_is_viable(x, c, 0.30, self.p))
        self.assertFalse(shock_is_viable(x, c, 0.31, self.p))

    def test_same_state_different_capacity_different_margin(self):
        x = 1.0
        low = shock_margin(x, 0.1, self.p)
        high = shock_margin(x, 0.5, self.p)
        self.assertAlmostEqual(low, 0.35)
        self.assertAlmostEqual(high, 0.55)
        self.assertGreater(high, low)

    def test_full_shared_state_stays_full_while_capacity_decays(self):
        x, c = 1.0, 0.5
        x2, c2 = quiet_step(x, c, self.p)
        self.assertEqual(x2, 1.0)
        self.assertAlmostEqual(c2, 0.475)
        self.assertLess(
            shock_margin(x2, c2, self.p),
            shock_margin(x, c, self.p),
        )

    def test_quiet_period_erodes_shock_margin_at_constant_state(self):
        rows = quiet_trajectory(1.0, 0.5, self.p, steps=20)
        self.assertTrue(all(x == 1.0 for _, x, _, _ in rows))
        self.assertEqual(
            local_shared_state_multiplier(self.p), 0.90
        )
        self.assertLess(rows[-1][2], rows[0][2])
        self.assertLess(rows[-1][3], rows[0][3])

    def test_same_state_and_recovery_multiplier_can_hide_fragility(self):
        x = 1.0
        c_high = 0.5
        c_low = 0.05
        self.assertEqual(
            local_shared_state_multiplier(self.p),
            local_shared_state_multiplier(self.p),
        )
        shock = 0.50
        self.assertTrue(shock_is_viable(x, c_high, shock, self.p))
        self.assertFalse(shock_is_viable(x, c_low, shock, self.p))

    def test_stationary_maintenance_offsets_decay(self):
        c = 0.5
        maintenance = required_maintenance_for_capacity(c, self.p)
        x2, c2 = quiet_step(
            1.0, c, self.p, maintenance=maintenance
        )
        self.assertEqual(x2, 1.0)
        self.assertAlmostEqual(c2, c)

    def test_maintenance_shortfall_is_margin_based(self):
        required = 0.50
        self.assertAlmostEqual(
            maintenance_shortfall(required, 1.0, 0.5, self.p),
            0.0,
        )
        self.assertAlmostEqual(
            maintenance_shortfall(required, 1.0, 0.1, self.p),
            0.15,
        )

    def test_post_shock_correction_is_capacity_bounded(self):
        self.assertAlmostEqual(
            post_shock_state(1.0, 0.2, 0.25, self.p),
            0.85,
        )


if __name__ == "__main__":
    unittest.main()
