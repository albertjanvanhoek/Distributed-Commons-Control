import VectorContribution

namespace DistributedCommons

/-!
# Behavioral maintenance operators

"Behavior" here means any state-contingent participant process that changes
future network/commons viability. No intention or cognition is assumed.

For a maintenance-dependent enabling stock K with decay delta, passive renewal
e, participant maintenance m, and viability boundary V,

  K' = (1-delta)K + e + m.

At K=V the boundary is preserved iff

  delta*V <= e + m.

This immediately falsifies universal participant-maintenance necessity:
passive renewal can suffice. When it does not, participant maintenance must
close the replacement gap.

A local deficit-responsive correction has multiplier

  1 - delta - g.

If delta+g>2 the multiplier is below -1, so more correction is not always
better.

Under symmetric sign-flip signal noise with fidelity p, expected signed
corrective gain is (2p-1)g. For p<1/2 and g>0 the intended correction reverses
sign.

Positive reinforcement and repair are likewise conditional operators rather
than unconditional virtues.
-/

noncomputable def maintenanceBoundaryNext
    (δ e m V : ℝ) : ℝ :=
  (1 - δ) * V + e + m

theorem boundary_preserved_iff_replacement_closed
    (δ e m V : ℝ) :
    V ≤ maintenanceBoundaryNext δ e m V ↔
      δ * V ≤ e + m := by
  unfold maintenanceBoundaryNext
  constructor <;> intro h <;> linarith

/-- Passive/exogenous renewal alone can preserve the viability boundary. -/
theorem passive_renewal_can_suffice
    {δ e V : ℝ} (h : δ * V ≤ e) :
    V ≤ maintenanceBoundaryNext δ e 0 V := by
  rw [boundary_preserved_iff_replacement_closed]
  linarith

/-- If passive renewal is insufficient, any boundary-preserving participant
maintenance must close at least the exact replacement gap. -/
theorem participant_maintenance_must_close_gap
    {δ e m V : ℝ}
    (hpassive : e < δ * V)
    (hpreserve : V ≤ maintenanceBoundaryNext δ e m V) :
    δ * V - e ≤ m := by
  rw [boundary_preserved_iff_replacement_closed] at hpreserve
  linarith

noncomputable def correctionMultiplier
    (δ g : ℝ) : ℝ :=
  1 - δ - g

/-- Excessive corrective gain creates a flip-direction multiplier below -1. -/
theorem overcorrection_multiplier_lt_neg_one
    {δ g : ℝ} (h : 2 < δ + g) :
    correctionMultiplier δ g < -1 := by
  unfold correctionMultiplier
  linarith

noncomputable def expectedSignedCorrectiveGain
    (g p : ℝ) : ℝ :=
  (2 * p - 1) * g

/-- With worse-than-random sign fidelity, intended correction becomes
anti-correction in expectation. -/
theorem low_fidelity_reverses_correction
    {g p : ℝ} (hg : 0 < g) (hp : p < 1 / 2) :
    expectedSignedCorrectiveGain g p < 0 := by
  unfold expectedSignedCorrectiveGain
  have hfactor : 2 * p - 1 < 0 := by linarith
  exact mul_neg_of_neg_of_pos hfactor hg

noncomputable def reinforcementScore
    (h p benefit loss : ℝ) : ℝ :=
  h * p * benefit - (1 - h) * (1 - p) * loss

/-- Reinforcing positively signalled processes is net harmful when expected
misclassified harm exceeds expected correctly identified benefit. -/
theorem reinforcement_can_be_harmful
    {h p benefit loss : ℝ}
    (hbad :
      h * p * benefit <
        (1 - h) * (1 - p) * loss) :
    reinforcementScore h p benefit loss < 0 := by
  unfold reinforcementScore
  linarith

noncomputable def repairNetValue
    (r V W cost : ℝ) : ℝ :=
  r * (V - W) - cost

/-- The SCAP repair condition is exactly the nonnegative-value condition. -/
theorem repair_nonnegative_iff
    (r V W cost : ℝ) :
    0 ≤ repairNetValue r V W cost ↔
      cost ≤ r * (V - W) := by
  unfold repairNetValue
  constructor <;> intro h <;> linarith

#print axioms boundary_preserved_iff_replacement_closed
#print axioms passive_renewal_can_suffice
#print axioms participant_maintenance_must_close_gap
#print axioms overcorrection_multiplier_lt_neg_one
#print axioms low_fidelity_reverses_correction
#print axioms reinforcement_can_be_harmful
#print axioms repair_nonnegative_iff

end DistributedCommons
