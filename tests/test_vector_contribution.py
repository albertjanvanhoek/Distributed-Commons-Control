import unittest

from distributed_commons.vector_contribution import (
    ContributionVector,
    opposite_sign_weight_witnesses,
)


class VectorContributionTests(unittest.TestCase):
    def test_scalar_sign_depends_on_weights(self):
        vector = ContributionVector({"loop_a": 0.2, "loop_b": -0.1})
        positive_weights, negative_weights = opposite_sign_weight_witnesses(
            0.2, -0.1
        )

        positive = vector.weighted(
            {
                "loop_a": positive_weights[0],
                "loop_b": positive_weights[1],
            }
        )
        negative = vector.weighted(
            {
                "loop_a": negative_weights[0],
                "loop_b": negative_weights[1],
            }
        )

        self.assertGreater(positive, 0.0)
        self.assertLess(negative, 0.0)

    def test_exact_witness_values(self):
        a, b = 0.2, -0.1
        positive_weights, negative_weights = opposite_sign_weight_witnesses(
            a, b
        )
        self.assertEqual(positive_weights, (0.2, 0.2))
        self.assertEqual(negative_weights, (0.1, 0.4))

    def test_zero_weight_can_ignore_a_loop_but_is_explicit(self):
        vector = ContributionVector({"a": 0.2, "b": -0.1})
        self.assertAlmostEqual(
            vector.weighted({"a": 1.0, "b": 0.0}), 0.2
        )

    def test_missing_weight_is_rejected(self):
        vector = ContributionVector({"a": 0.2, "b": -0.1})
        with self.assertRaises(ValueError):
            vector.weighted({"a": 1.0})


if __name__ == "__main__":
    unittest.main()
