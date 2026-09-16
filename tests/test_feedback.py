import unittest
from dataclasses import replace
from distributed_commons.feedback import FeedbackParameters, simulate_feedback

class FeedbackTests(unittest.TestCase):
    def setUp(self):
        self.p = FeedbackParameters()
        self.ramp = [0.1]*20 + [0.1+0.02*k for k in range(1,26)] + [0.6]*30

    def test_envelope_feedback_preserves_safety(self):
        rows = simulate_feedback(self.ramp, self.p)
        self.assertTrue(all(r['certified'] for r in rows[1:]))
        self.assertLessEqual(max(r['failure'] for r in rows), self.p.safety_target+1e-12)
        for r in rows[1:]:
            self.assertGreaterEqual(r['effort_added'], -1e-14)
            self.assertLessEqual(r['effort_added'], self.p.capacity+1e-14)

    def test_stale_target_is_not_enough(self):
        reactive = simulate_feedback(self.ramp, self.p, 'reactive')
        self.assertTrue(any(r['failure'] > self.p.safety_target+1e-12 for r in reactive))

    def test_insufficient_capacity_is_reported(self):
        rows = simulate_feedback(self.ramp, replace(self.p, capacity=0.015))
        self.assertTrue(any(r['capacity_shortfall'] and r['capacity_shortfall'] > 0 for r in rows[1:]))
        self.assertTrue(any(r['failure'] > self.p.safety_target+1e-12 for r in rows))
        self.assertFalse(any(r['certified'] and r['failure'] > self.p.safety_target+1e-12 for r in rows))

    def test_unbounded_jump_invalidates_envelope(self):
        rows = simulate_feedback([0.1]*20+[0.6]*10, self.p)
        self.assertFalse(rows[20]['envelope_valid'])
        self.assertFalse(rows[20]['certified'])
        self.assertGreater(rows[20]['failure'], self.p.safety_target)

    def test_structural_floor_is_not_repaired_by_feedback(self):
        rows = simulate_feedback(self.ramp, replace(self.p, correlation=0.1))
        self.assertIsNone(rows[-1]['required'])
        self.assertFalse(rows[-1]['certified'])
        self.assertGreater(rows[-1]['failure'], self.p.safety_target)
