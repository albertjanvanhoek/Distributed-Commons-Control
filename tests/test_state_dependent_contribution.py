import unittest

from distributed_commons.corrective_capacity import (
    CapacityParameters,
    quiet_step,
)
from distributed_commons.state_dependent_contribution import (
    certified_access_margin,
    certified_participant_contribution,
    expected_access_margin,
    expected_participant_contribution,
)
from distributed_commons.viability import two_cause_example


class StateDependentContributionTests(unittest.TestCase):
    def setUp(self):
        self.topology = two_cause_example(0.05)
        self.p = CapacityParameters(
            regeneration=0.10,
            capacity_decay=0.05,
            correction_efficiency=0.50,
            viability_floor=0.70,
        )

    def test_independent_profile_unlocks_expected_capacity_margin(self):
        before = expected_access_margin(
            self.topology, {"A1", "A2"}, 1.0, 0.5, self.p
        )
        after = expected_access_margin(
            self.topology, {"A1", "A2", "B1"}, 1.0, 0.5, self.p
        )
        self.assertAlmostEqual(before, 0.5375)
        self.assertAlmostEqual(after, 0.549375)
        self.assertAlmostEqual(after - before, 0.011875)

    def test_expected_contribution_matches_topology_difference(self):
        value = expected_participant_contribution(
            self.topology,
            "B1",
            {"A1", "A2"},
            1.0,
            0.5,
            self.p,
        )
        expected = (
            self.p.correction_efficiency
            * 0.5
            * (0.05 - 0.05**2)
        )
        self.assertAlmostEqual(value, expected)

    def test_redundant_profile_has_zero_full_network_contribution(self):
        value = expected_participant_contribution(
            self.topology,
            "A2",
            {"A1", "B1"},
            1.0,
            0.5,
            self.p,
        )
        self.assertAlmostEqual(value, 0.0)

    def test_same_participant_contribution_scales_with_capacity_state(self):
        low = expected_participant_contribution(
            self.topology, "B1", {"A1", "A2"}, 1.0, 0.1, self.p
        )
        high = expected_participant_contribution(
            self.topology, "B1", {"A1", "A2"}, 1.0, 0.5, self.p
        )
        self.assertAlmostEqual(high, 5.0 * low)

    def test_zero_capacity_means_zero_access_contribution(self):
        value = expected_participant_contribution(
            self.topology, "B1", {"A1", "A2"}, 1.0, 0.0, self.p
        )
        self.assertAlmostEqual(value, 0.0)

    def test_certified_margin_has_threshold_contribution(self):
        target = 0.01
        before = certified_access_margin(
            self.topology, {"A1", "A2"}, 1.0, 0.5, target, self.p
        )
        after = certified_access_margin(
            self.topology,
            {"A1", "A2", "B1"},
            1.0,
            0.5,
            target,
            self.p,
        )
        self.assertAlmostEqual(before, 0.30)
        self.assertAlmostEqual(after, 0.55)
        self.assertAlmostEqual(
            certified_participant_contribution(
                self.topology,
                "B1",
                {"A1", "A2"},
                1.0,
                0.5,
                target,
                self.p,
            ),
            0.25,
        )

    def test_certified_contribution_depends_on_declared_target(self):
        low_target = certified_participant_contribution(
            self.topology,
            "B1",
            {"A1", "A2"},
            1.0,
            0.5,
            0.001,
            self.p,
        )
        high_target = certified_participant_contribution(
            self.topology,
            "B1",
            {"A1", "A2"},
            1.0,
            0.5,
            0.10,
            self.p,
        )
        self.assertEqual(low_target, 0.0)
        self.assertEqual(high_target, 0.0)

    def test_quiet_capacity_decay_reduces_same_participant_contribution(self):
        initial = expected_participant_contribution(
            self.topology, "B1", {"A1", "A2"}, 1.0, 0.5, self.p
        )
        _, c_next = quiet_step(1.0, 0.5, self.p)
        later = expected_participant_contribution(
            self.topology, "B1", {"A1", "A2"}, 1.0, c_next, self.p
        )
        self.assertAlmostEqual(
            later, (1.0 - self.p.capacity_decay) * initial
        )


if __name__ == "__main__":
    unittest.main()
