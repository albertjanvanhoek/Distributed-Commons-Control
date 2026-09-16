import JamEffortObservability

namespace DistributedCommons

/-!
# Fungal flow-coupled maintenance

This file formalizes the local stability boundary for Experiment 12.

The empirical grounding is substrate-specific: fungal cords can thicken in
association with transport flow, and local flow can carry information about a
cord's role in the wider network.

The nonlinear two-route reinforcement law itself is a model extension.

Let
- δ in (0,1] be the adjustment rate,
- β >= 0 be reinforcement elasticity,
- s >= 0 be effective sensitivity of the local flow-coupled signal.

The local multiplier at equal route allocation is

  M = 1 - δ + δ(βs).

Because M is nonnegative under the declared bounds,

  |M| < 1  iff  βs < 1.

Thus subunit effective reinforcement restores equal redundancy, unit gain is
neutral, and superunit gain destabilizes the symmetric redundant state.
-/

noncomputable def fungalMultiplier
    (δ β s : ℝ) : ℝ :=
  1 - δ + δ * (β * s)

theorem fungal_multiplier_nonnegative
    {δ β s : ℝ}
    (hδ0 : 0 < δ)
    (hδ1 : δ ≤ 1)
    (hβ : 0 ≤ β)
    (hs : 0 ≤ s) :
    0 ≤ fungalMultiplier δ β s := by
  unfold fungalMultiplier
  have hbase : 0 ≤ 1 - δ := by linarith
  have hprod : 0 ≤ δ * (β * s) := by positivity
  linarith

theorem fungal_stable_iff_effective_gain_lt_one
    {δ β s : ℝ}
    (hδ0 : 0 < δ)
    (hδ1 : δ ≤ 1)
    (hβ : 0 ≤ β)
    (hs : 0 ≤ s) :
    |fungalMultiplier δ β s| < 1 ↔
      β * s < 1 := by
  have hM : 0 ≤ fungalMultiplier δ β s :=
    fungal_multiplier_nonnegative hδ0 hδ1 hβ hs
  rw [abs_of_nonneg hM]
  constructor
  · intro h
    unfold fungalMultiplier at h
    by_contra hnot
    have hgain : 1 ≤ β * s := le_of_not_gt hnot
    have hprod : 0 ≤ δ * (β * s - 1) := by
      exact mul_nonneg (le_of_lt hδ0) (sub_nonneg.mpr hgain)
    nlinarith
  · intro h
    have hdiff : 0 < 1 - β * s := sub_pos.mpr h
    have hprod : 0 < δ * (1 - β * s) := mul_pos hδ0 hdiff
    unfold fungalMultiplier
    nlinarith

theorem fungal_neutral_iff_effective_gain_eq_one
    {δ β s : ℝ}
    (hδ0 : 0 < δ) :
    fungalMultiplier δ β s = 1 ↔
      β * s = 1 := by
  unfold fungalMultiplier
  constructor
  · intro h
    have hzero : δ * (β * s - 1) = 0 := by
      nlinarith
    rcases mul_eq_zero.mp hzero with hδ | hgain
    · exact False.elim ((ne_of_gt hδ0) hδ)
    · linarith
  · intro h
    rw [h]
    ring

theorem fungal_unstable_iff_effective_gain_gt_one
    {δ β s : ℝ}
    (hδ0 : 0 < δ) :
    1 < fungalMultiplier δ β s ↔
      1 < β * s := by
  unfold fungalMultiplier
  constructor
  · intro h
    by_contra hnot
    have hgain : β * s ≤ 1 := le_of_not_gt hnot
    have hprod : 0 ≤ δ * (1 - β * s) := by
      exact mul_nonneg (le_of_lt hδ0) (sub_nonneg.mpr hgain)
    nlinarith
  · intro h
    have hdiff : 0 < β * s - 1 := sub_pos.mpr h
    have hprod : 0 < δ * (β * s - 1) := mul_pos hδ0 hdiff
    nlinarith

noncomputable def fungalBackupShare
    (z : ℝ) : ℝ :=
  min z (1 - z)

/-- For a fixed unit total route allocation, equal redundancy maximizes the
worst surviving route share after loss of the stronger route. -/
theorem fungal_backup_share_le_half
    (z : ℝ) :
    fungalBackupShare z ≤ (1 : ℝ) / 2 := by
  unfold fungalBackupShare
  by_cases hz : z ≤ (1 : ℝ) / 2
  · exact le_trans (min_le_left _ _) hz
  · have hz' : 1 - z < (1 : ℝ) / 2 := by linarith
    exact le_trans (min_le_right _ _) (le_of_lt hz')

theorem fungal_backup_share_at_half :
    fungalBackupShare ((1 : ℝ) / 2) = (1 : ℝ) / 2 := by
  unfold fungalBackupShare
  norm_num

#print axioms fungal_multiplier_nonnegative
#print axioms fungal_stable_iff_effective_gain_lt_one
#print axioms fungal_neutral_iff_effective_gain_eq_one
#print axioms fungal_unstable_iff_effective_gain_gt_one
#print axioms fungal_backup_share_le_half
#print axioms fungal_backup_share_at_half

end DistributedCommons
