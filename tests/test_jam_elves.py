import unittest

from distributed_commons.jam_elves import (
    attack_success_bound,
    critical_client_bug_share,
    economic_soundness_threshold,
    expected_committee_bound,
    honest_reproduction,
    max_client_bug_share_for_target,
    required_collateral_share,
)


class ElvesGroundingTests(unittest.TestCase):
    def test_economic_target_for_jam_example(self):
        epsilon = economic_soundness_threshold(1023, 0.05)
        self.assertAlmostEqual(epsilon, 1.0 / 20461.0)

    def test_jam_branching_bounds(self):
        expected = {
            1.0 / 3.0: 1.1302520977443587e-4,
            0.20: 2.035098121646621e-7,
            0.10: 2.5796577568577908e-9,
            0.05: 3.188047427928563e-10,
        }
        for gamma, target in expected.items():
            self.assertAlmostEqual(
                attack_success_bound(gamma, 30.0, 2.0),
                target,
                places=14,
            )

    def test_worst_case_collateral_requirement(self):
        p = attack_success_bound(1.0 / 3.0, 30.0, 2.0)
        self.assertAlmostEqual(
            required_collateral_share(1023, p),
            0.11563785959258621,
        )
        self.assertAlmostEqual(
            required_collateral_share(
                1023, p, collateral_units_lost=2
            ),
            0.057818929796293106,
        )

    def test_honest_and_faulty_reproduction_constraints(self):
        self.assertGreater(
            honest_reproduction(1.0 / 3.0, 2.0), 1.0
        )
        self.assertLess(
            (1.0 / 3.0) * 2.0, 1.0
        )
        self.assertAlmostEqual(
            expected_committee_bound(30.0, 0.1, 0.05, 2.0),
            30.0 / 0.7,
        )

    def test_client_bug_criticality_thresholds(self):
        self.assertAlmostEqual(
            critical_client_bug_share(1.0 / 3.0, 2.0),
            0.25,
        )
        self.assertAlmostEqual(
            critical_client_bug_share(0.20, 2.0),
            0.375,
        )
        self.assertAlmostEqual(
            critical_client_bug_share(0.05, 2.0),
            0.4736842105263158,
        )

    def test_client_share_meeting_economic_target(self):
        epsilon = economic_soundness_threshold(1023, 0.05)
        self.assertIsNone(
            max_client_bug_share_for_target(
                1.0 / 3.0, 30.0, 2.0, epsilon
            )
        )
        self.assertAlmostEqual(
            max_client_bug_share_for_target(
                0.20, 30.0, 2.0, epsilon
            ),
            0.14555924403201406,
        )
        self.assertAlmostEqual(
            max_client_bug_share_for_target(
                0.05, 30.0, 2.0, epsilon
            ),
            0.2804709423427486,
        )


if __name__ == "__main__":
    unittest.main()
