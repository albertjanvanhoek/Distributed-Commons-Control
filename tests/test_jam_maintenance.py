import math
import unittest

from distributed_commons.jam_maintenance import (
    JamMaintenanceState,
    escalation_vector_change,
    one_validator_correction_gain,
    one_validator_scalability_gain,
)


class JamMaintenanceOperatorTests(unittest.TestCase):
    def test_one_validator_client_diversification_has_exact_lambda_gain(self):
        state = JamMaintenanceState(
            validator_count=1023,
            adversarial_count=205,
            vulnerable_honest_count=119,
            no_show_share=0.15,
        )
        self.assertAlmostEqual(
            one_validator_correction_gain(state),
            state.s_delta / state.validator_count,
        )

    def test_one_validator_reliability_has_exact_scalability_gain(self):
        state = JamMaintenanceState(
            validator_count=1023,
            adversarial_count=205,
            vulnerable_honest_count=82,
            no_show_share=0.15,
        )
        self.assertAlmostEqual(
            one_validator_scalability_gain(state),
            state.s_delta / state.validator_count,
        )

    def test_one_validator_client_switch_can_cross_certification_boundary(self):
        state = JamMaintenanceState(
            validator_count=1023,
            adversarial_count=205,
            vulnerable_honest_count=119,
            no_show_share=0.15,
            s0=30.0,
            s_delta=2.0,
            collateral_share=0.05,
        )
        after = state.diversify_one_honest_validator()

        self.assertLess(state.safety_log_margin, 0.0)
        self.assertGreater(after.safety_log_margin, 0.0)

        self.assertAlmostEqual(
            state.safety_log_margin,
            -0.013217114970080239,
            places=12,
        )
        self.assertAlmostEqual(
            after.safety_log_margin,
            0.0349504844431776,
            places=12,
        )

    def test_escalation_strength_has_mixed_sign_vector(self):
        state = JamMaintenanceState(
            validator_count=1023,
            adversarial_count=205,
            vulnerable_honest_count=82,
            no_show_share=0.15,
            s_delta=2.0,
        )
        d_safety, d_scale = escalation_vector_change(state, 2.08)
        self.assertGreater(d_safety, 0.0)
        self.assertLess(d_scale, 0.0)

    def test_escalation_numbers_reproduce_parameter_slice(self):
        state = JamMaintenanceState(
            validator_count=1023,
            adversarial_count=205,
            vulnerable_honest_count=82,
            no_show_share=0.15,
            s_delta=2.0,
        )
        after = state.with_escalation(2.08)

        self.assertAlmostEqual(state.correction_reproduction, 1.4389051808406648)
        self.assertAlmostEqual(state.scalability_margin, 0.70)
        self.assertAlmostEqual(state.safety_log_margin, 1.7429220392040146)

        self.assertAlmostEqual(after.correction_reproduction, 1.4964613880742914)
        self.assertAlmostEqual(after.scalability_margin, 0.688)
        self.assertAlmostEqual(after.safety_log_margin, 2.603090255069031)

    def test_more_escalation_is_not_a_weight_free_improvement(self):
        state = JamMaintenanceState(
            validator_count=1023,
            adversarial_count=205,
            vulnerable_honest_count=82,
            no_show_share=0.15,
            s_delta=2.0,
        )
        d_safety, d_scale = escalation_vector_change(state, 2.08)
        self.assertTrue(math.isfinite(d_safety))
        self.assertGreater(d_safety, 0.0)
        self.assertLess(d_scale, 0.0)


if __name__ == "__main__":
    unittest.main()
