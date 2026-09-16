import FungalFlowMaintenance

namespace DistributedCommons

/-!
# Viability-conditioned ought: cross-substrate synthesis

This file formalizes one exact synthesis result from the grounded JAM/ELVES
branching architecture.

Let
- h > 0 be the effective share capable of correct escalation;
- u >= 0 be the share contributing to failure/no-show amplification;
- s > 0 be escalation strength.

The two viability requirements are

  1 < h*s        (corrective escalation supercritical)
  u*s < 1        (failure escalation subcritical).

There exists an escalation strength satisfying both iff

  u < h.

Thus no choice of escalation strength can compensate for an architecture in
which the failure-amplifying share is at least as large as the effective
corrective share.

This theorem is substrate-specific algebra. The philosophical label
"viability-conditioned ought" is an interpretation, not part of the theorem.
-/

theorem jam_escalation_feasible_iff_failure_lt_correction
    {h u : ℝ}
    (hh : 0 < h)
    (hu : 0 ≤ u) :
    (∃ s : ℝ, 0 < s ∧ 1 < h * s ∧ u * s < 1) ↔
      u < h := by
  constructor
  · rintro ⟨s, hs, hcorrect, hfailure⟩
    have hus_lt_hhs : u * s < h * s := lt_trans hfailure hcorrect
    by_contra hnot
    have hhu : h ≤ u := le_of_not_gt hnot
    have hmul : h * s ≤ u * s :=
      mul_le_mul_of_nonneg_right hhu (le_of_lt hs)
    linarith
  · intro huh
    have hsum : 0 < h + u := by linarith
    have hsum_ne : h + u ≠ 0 := ne_of_gt hsum
    refine ⟨2 / (h + u), ?_, ?_, ?_⟩
    · positivity
    · have hnum : h + u < 2 * h := by linarith
      calc
        1 = (h + u) / (h + u) := by
          symm
          exact div_self hsum_ne
        _ < (2 * h) / (h + u) :=
          (div_lt_div_iff_of_pos_right hsum).2 hnum
        _ = h * (2 / (h + u)) := by ring
    · have hnum : 2 * u < h + u := by linarith
      calc
        u * (2 / (h + u)) = (2 * u) / (h + u) := by ring
        _ < (h + u) / (h + u) :=
          (div_lt_div_iff_of_pos_right hsum).2 hnum
        _ = 1 := div_self hsum_ne

/-- Necessary structural condition in count form: if one positive escalation
strength can make correct branching supercritical while failure branching is
subcritical, the effective failure share must be smaller than the effective
corrective share. -/
theorem jam_feasible_implies_failure_lt_correction
    {h u s : ℝ}
    (hs : 0 < s)
    (hcorrect : 1 < h * s)
    (hfailure : u * s < 1) :
    u < h := by
  have hus_lt_hhs : u * s < h * s := lt_trans hfailure hcorrect
  by_contra hnot
  have hhu : h ≤ u := le_of_not_gt hnot
  have hmul : h * s ≤ u * s :=
    mul_le_mul_of_nonneg_right hhu (le_of_lt hs)
  linarith

#print axioms jam_escalation_feasible_iff_failure_lt_correction
#print axioms jam_feasible_implies_failure_lt_correction

end DistributedCommons
