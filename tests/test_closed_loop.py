import unittest
from dataclasses import replace

from distributed_commons.closed_loop import (
    ClosedLoopParameters,
    _monitor_response,
    _producer_response,
    basin_threshold,
    behavioural_equilibrium,
    effective_capture_gain,
    effective_effort_cost,
    equilibrium_damage,
    final_health,
    hysteresis_window,
    loop_gain,
)


class BehaviouralEquilibriumTests(unittest.TestCase):
    def test_fixed_point_residual(self):
        for kappa in (0.0, 0.05, 1.0):
            p = ClosedLoopParameters(baseline_funding=kappa)
            for x in (0.0, 0.1, 0.5, 1.0):
                e = behavioural_equilibrium(x, p)
                self.assertAlmostEqual(
                    e.effort,
                    _monitor_response(e.bad_attempt_rate, x, p),
                    12,
                )
                self.assertAlmostEqual(
                    e.bad_attempt_rate,
                    _producer_response(e.effort, x, p),
                    9,
                )

    def test_no_reward_means_no_monitoring_at_zero_health(self):
        e = behavioural_equilibrium(0.0, ClosedLoopParameters())
        self.assertEqual(e.effort, 0.0)

    def test_alternative_closure_functions_move_in_expected_direction(self):
        cost = ClosedLoopParameters(
            baseline_funding=1.0,
            reward_health_weight=0.0,
            cost_stress=3.0,
        )
        capture = ClosedLoopParameters(
            baseline_funding=1.0,
            reward_health_weight=0.0,
            capture_stress=1.2,
        )
        self.assertGreater(
            effective_effort_cost(0.0, cost),
            effective_effort_cost(1.0, cost),
        )
        self.assertGreater(
            effective_capture_gain(0.0, capture),
            effective_capture_gain(1.0, capture),
        )


class FoldTests(unittest.TestCase):
    def test_commons_funded_monitoring_is_bistable(self):
        w = hysteresis_window(ClosedLoopParameters(), points=400)
        self.assertIsNotNone(w)
        assert w is not None
        self.assertAlmostEqual(w.fold_damage, 0.5468, places=3)
        self.assertGreater(w.ratio, 10.0)

    def test_damage_curve_is_unimodal_for_reported_sets(self):
        for kappa in (0.0, 0.05, 0.2, 0.5):
            p = ClosedLoopParameters(baseline_funding=kappa)
            ds = [equilibrium_damage(i / 200, p) for i in range(200)]
            peak = max(range(200), key=ds.__getitem__)
            self.assertTrue(
                all(a <= b for a, b in zip(ds[:peak], ds[1 : peak + 1]))
            )
            self.assertTrue(
                all(a >= b for a, b in zip(ds[peak:], ds[peak + 1 :]))
            )

    def test_baseline_funding_shrinks_then_removes_window(self):
        ratios = []
        for kappa in (0.0, 0.05, 0.2, 0.5, 1.0):
            w = hysteresis_window(
                ClosedLoopParameters(baseline_funding=kappa), points=400
            )
            self.assertIsNotNone(w)
            assert w is not None
            ratios.append(w.ratio)
        self.assertEqual(ratios, sorted(ratios, reverse=True))
        self.assertIsNone(
            hysteresis_window(
                ClosedLoopParameters(baseline_funding=1.5), points=400
            )
        )

    def test_loop_gain_separates_branches(self):
        p = ClosedLoopParameters()
        w = hysteresis_window(p, points=400)
        assert w is not None
        self.assertGreater(loop_gain(0.5 * w.fold_health, p), 1.0)
        self.assertLess(
            loop_gain(0.5 * (1.0 + w.fold_health), p), 1.0
        )
        self.assertAlmostEqual(
            loop_gain(w.fold_health, p), 1.0, places=2
        )

    def test_fold_survives_exponential_cost_closure(self):
        p = ClosedLoopParameters(
            baseline_funding=1.0,
            reward_health_weight=0.0,
            cost_stress=3.0,
        )
        w = hysteresis_window(p, points=400)
        self.assertIsNotNone(w)
        assert w is not None
        self.assertAlmostEqual(w.collapse_damage, 0.1202, places=3)
        self.assertAlmostEqual(w.fold_damage, 0.2619, places=3)
        self.assertGreater(w.ratio, 2.0)

    def test_fold_survives_capture_gain_closure(self):
        p = ClosedLoopParameters(
            baseline_funding=1.0,
            reward_health_weight=0.0,
            capture_stress=1.2,
        )
        w = hysteresis_window(p, points=400)
        self.assertIsNotNone(w)
        assert w is not None
        self.assertAlmostEqual(w.collapse_damage, 1.0508, places=3)
        self.assertAlmostEqual(w.fold_damage, 1.8528, places=3)
        self.assertGreater(w.ratio, 1.7)


class FullModelTests(unittest.TestCase):
    def setUp(self):
        self.p = ClosedLoopParameters(baseline_funding=0.05)
        self.w = hysteresis_window(self.p, points=400)
        assert self.w is not None

    def outcomes(self, p, damage):
        p = replace(p, damage=damage)
        b_collapsed = behavioural_equilibrium(
            0.0, p
        ).bad_attempt_rate
        top = final_health(
            p,
            initial_health=1.0,
            initial_bad_attempt_rate=0.2,
            steps=1500,
        )
        bottom = final_health(
            p,
            initial_health=0.0,
            initial_bad_attempt_rate=b_collapsed,
            steps=1500,
        )
        return top, bottom

    def test_bistable_inside_window(self):
        top, bottom = self.outcomes(
            self.p,
            0.5 * (self.w.collapse_damage + self.w.fold_damage),
        )
        self.assertGreater(top, 0.5)
        self.assertEqual(bottom, 0.0)

    def test_recovers_below_window_and_collapses_above_fold(self):
        top, bottom = self.outcomes(
            self.p, 0.5 * self.w.collapse_damage
        )
        self.assertGreater(min(top, bottom), 0.5)
        top, bottom = self.outcomes(
            self.p, 1.2 * self.w.fold_damage
        )
        self.assertEqual(max(top, bottom), 0.0)

    def test_basin_is_set_by_monitor_mobilisation(self):
        p = replace(ClosedLoopParameters(), damage=0.2942)
        kw = dict(
            initial_health=0.15,
            initial_bad_attempt_rate=0.2,
            steps=1500,
        )
        self.assertGreater(
            final_health(p, initial_effort=0.3, **kw), 0.5
        )
        self.assertEqual(
            final_health(p, initial_effort=0.05, **kw), 0.0
        )

    def test_quiet_history_is_more_fragile(self):
        p = replace(ClosedLoopParameters(), damage=0.2942)
        quiet = basin_threshold(p, 0.02, steps=1500)
        attacked = basin_threshold(p, 0.8, steps=1500)
        assert quiet is not None and attacked is not None
        self.assertGreater(quiet, 2.0 * attacked)

    def test_alternative_closures_are_bistable_in_full_model(self):
        cases = (
            ClosedLoopParameters(
                baseline_funding=1.0,
                reward_health_weight=0.0,
                cost_stress=3.0,
            ),
            ClosedLoopParameters(
                baseline_funding=1.0,
                reward_health_weight=0.0,
                capture_stress=1.2,
            ),
        )
        for p in cases:
            w = hysteresis_window(p, points=400)
            assert w is not None
            damage = 0.5 * (w.collapse_damage + w.fold_damage)
            top, bottom = self.outcomes(p, damage)
            self.assertGreater(top, 0.5)
            self.assertEqual(bottom, 0.0)


if __name__ == "__main__":
    unittest.main()
