import unittest

from distributed_commons.selected_viability import (
    REVERSAL_THRESHOLD,
    critical_cost_ratio,
    direct_addition_contribution,
    induced_response_effect,
    one_selected_margin,
    reversal_occurs,
    reversal_polynomial,
    selected_addition_contribution,
    two_frozen_margin,
    two_participant_effort,
    two_selected_margin,
)


class SelectedViabilityTests(unittest.TestCase):
    def test_two_participant_fixed_point(self):
        for z in (0.1, 0.5, 0.9):
            q = two_participant_effort(z)
            self.assertAlmostEqual(q, z * (1.0 - q / 2.0))

    def test_direct_addition_is_positive_interior(self):
        for z in (0.1, 0.5, 0.9):
            direct = direct_addition_contribution(0.2, 0.025, z)
            self.assertGreater(direct, 0.0)
            self.assertAlmostEqual(direct, 0.2 * z * (1.0 - z))

    def test_exact_reversal_threshold(self):
        self.assertAlmostEqual(
            REVERSAL_THRESHOLD, 0.8284271247461903
        )
        self.assertFalse(reversal_occurs(0.8))
        self.assertTrue(reversal_occurs(0.9))
        self.assertLess(reversal_polynomial(0.8), 0.0)
        self.assertGreater(reversal_polynomial(0.9), 0.0)

    def test_positive_direct_but_negative_selected_contribution(self):
        b = 0.2
        epsilon = 0.025
        z = 0.9

        self.assertAlmostEqual(one_selected_margin(b, epsilon, z), 0.005)
        self.assertAlmostEqual(two_frozen_margin(b, epsilon, z), 0.023)
        self.assertAlmostEqual(
            two_selected_margin(b, epsilon, z),
            -0.003775267538644468,
        )

        self.assertGreater(
            direct_addition_contribution(b, epsilon, z), 0.0
        )
        self.assertLess(
            selected_addition_contribution(b, epsilon, z), 0.0
        )
        self.assertAlmostEqual(
            selected_addition_contribution(b, epsilon, z),
            direct_addition_contribution(b, epsilon, z)
            + induced_response_effect(b, epsilon, z),
        )

    def test_target_can_flip_from_safe_to_unsafe_after_addition(self):
        b = 0.2
        epsilon = 0.025
        z = 0.9
        self.assertGreater(one_selected_margin(b, epsilon, z), 0.0)
        self.assertLess(two_selected_margin(b, epsilon, z), 0.0)

    def test_critical_cost_ratio_boundary(self):
        boundary = (2.0**0.5 - 1.0) ** 2
        self.assertAlmostEqual(boundary, 0.1715728752538099)
        self.assertLess(critical_cost_ratio(0.10), 1.0)
        self.assertGreater(critical_cost_ratio(0.25), 1.0)
        self.assertAlmostEqual(critical_cost_ratio(boundary), 1.0)

    def test_below_reversal_threshold_addition_remains_positive(self):
        b = 0.2
        epsilon = 0.025
        z = 0.5
        self.assertGreater(
            selected_addition_contribution(b, epsilon, z), 0.0
        )


if __name__ == "__main__":
    unittest.main()
