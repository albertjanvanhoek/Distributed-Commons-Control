import itertools
import unittest

from distributed_commons.viability import (
    FailureCause,
    FailureTopology,
    Participant,
    two_cause_example,
)


class ViabilityTopologyTests(unittest.TestCase):
    def test_two_cause_structural_escape(self):
        topology = two_cause_example(0.05)
        self.assertAlmostEqual(
            topology.escape_probability({"A1", "A2"}), 0.05
        )
        self.assertAlmostEqual(
            topology.escape_probability({"A1", "A2", "B1"}), 0.05**2
        )

    def test_independent_profile_changes_margin_twentyfold(self):
        topology = two_cause_example(0.05)
        epsilon = 0.001
        redundant = topology.viability_margin({"A1", "A2"}, epsilon)
        diverse = topology.viability_margin(
            {"A1", "A2", "B1"}, epsilon
        )
        self.assertAlmostEqual(redundant, 0.02)
        self.assertAlmostEqual(diverse, 0.4)
        self.assertAlmostEqual(diverse / redundant, 20.0)

    def test_adding_participant_never_reduces_structural_margin(self):
        topology = FailureTopology(
            causes=(
                FailureCause("A", 0.2),
                FailureCause("B", 0.3),
                FailureCause("C", 0.1),
            ),
            participants=(
                Participant("p1", frozenset({"A"})),
                Participant("p2", frozenset({"A", "B"})),
                Participant("p3", frozenset({"C"})),
                Participant("p4", frozenset({"B"})),
            ),
        )
        names = sorted(topology.participant_names)
        epsilon = 0.01
        for size in range(len(names) + 1):
            for subset_tuple in itertools.combinations(names, size):
                subset = frozenset(subset_tuple)
                for participant in set(names) - subset:
                    self.assertLessEqual(
                        topology.escape_probability(
                            subset | {participant}
                        ),
                        topology.escape_probability(subset) + 1e-15,
                    )
                    self.assertGreaterEqual(
                        topology.viability_margin(
                            subset | {participant}, epsilon
                        )
                        + 1e-15,
                        topology.viability_margin(subset, epsilon),
                    )

    def test_failure_free_participant_closes_structural_escape(self):
        topology = FailureTopology(
            causes=(FailureCause("A", 0.4),),
            participants=(
                Participant("vulnerable", frozenset({"A"})),
                Participant("independent", frozenset()),
            ),
        )
        self.assertEqual(
            topology.escape_probability(
                {"vulnerable", "independent"}
            ),
            0.0,
        )
        self.assertEqual(
            topology.viability_margin(
                {"vulnerable", "independent"}, 0.001
            ),
            1.0,
        )


class ContributionTests(unittest.TestCase):
    def setUp(self):
        self.topology = two_cause_example(0.05)
        self.epsilon = 0.001

    def test_leave_one_out_distinguishes_redundancy_and_independence(self):
        self.assertAlmostEqual(
            self.topology.leave_one_out_contribution(
                "A1", self.epsilon
            ),
            0.0,
        )
        self.assertAlmostEqual(
            self.topology.leave_one_out_contribution(
                "A2", self.epsilon
            ),
            0.0,
        )
        self.assertAlmostEqual(
            self.topology.leave_one_out_contribution(
                "B1", self.epsilon
            ),
            0.38,
        )

    def test_shapley_values_are_efficient(self):
        values = self.topology.shapley_values(self.epsilon)
        total = sum(values.values())
        margin_gain = (
            self.topology.viability_margin(
                self.topology.participant_names, self.epsilon
            )
            - self.topology.viability_margin(set(), self.epsilon)
        )
        self.assertAlmostEqual(total, margin_gain)
        self.assertAlmostEqual(values["A1"], 0.06966666666666667)
        self.assertAlmostEqual(values["A2"], 0.06966666666666667)
        self.assertAlmostEqual(values["B1"], 0.25966666666666666)

    def test_harsanyi_dividends_expose_nonadditivity(self):
        dividends = self.topology.harsanyi_dividends(self.epsilon)
        self.assertAlmostEqual(
            dividends[frozenset({"A1", "A2"})], -0.019
        )
        self.assertAlmostEqual(
            dividends[frozenset({"A1", "B1"})], 0.361
        )
        self.assertAlmostEqual(
            dividends[frozenset({"A2", "B1"})], 0.361
        )
        self.assertAlmostEqual(
            dividends[frozenset({"A1", "A2", "B1"})], -0.361
        )
        self.assertAlmostEqual(
            sum(dividends.values()),
            self.topology.viability_margin(
                self.topology.participant_names, self.epsilon
            )
            - self.topology.viability_margin(set(), self.epsilon),
        )

    def test_shapley_has_no_leftover_by_construction(self):
        shapley = self.topology.shapley_values(self.epsilon)
        dividends = self.topology.harsanyi_dividends(self.epsilon)
        interaction_total = sum(
            value
            for coalition, value in dividends.items()
            if len(coalition) >= 2
        )
        self.assertNotAlmostEqual(interaction_total, 0.0)
        self.assertAlmostEqual(
            sum(shapley.values()),
            self.topology.viability_margin(
                self.topology.participant_names, self.epsilon
            )
            - self.topology.viability_margin(set(), self.epsilon),
        )


class ValidationTests(unittest.TestCase):
    def test_unknown_failure_cause_is_rejected(self):
        with self.assertRaises(ValueError):
            FailureTopology(
                causes=(FailureCause("A", 0.1),),
                participants=(
                    Participant("p", frozenset({"B"})),
                ),
            )

    def test_unknown_participant_is_rejected(self):
        topology = two_cause_example()
        with self.assertRaises(ValueError):
            topology.escape_probability({"missing"})


if __name__ == "__main__":
    unittest.main()
