import JamMaintenance

namespace DistributedCommons

/-!
# Partially identified JAM audit behavior selection

The current Gray Paper does not specify the complete reward function for
auditing. This file therefore formalizes only the payoff inequalities implied
by the grounded action structure.

After announcing an audit:
- C: compute/re-execute, utility R_C - c;
- R: rubber-stamp positive, utility R_R - b*d*L;
- N: no-show, utility R_N.

Here b is invalid-report opportunity rate, d is probability a false positive is
exposed, and L is the higher-layer fault loss.

Actual compute weakly dominates rubber-stamp iff

  c <= R_C - R_R + b*d*L.

Compute weakly dominates no-show iff

  c <= R_C - R_N.

The minimum reward advantage over rubber-stamp is

  c - b*d*L.

Thus lower exposure probability raises the reward differential required to
select actual computation whenever b and L are positive.
-/

noncomputable def computeUtility
    (R_C c : ℝ) : ℝ :=
  R_C - c

noncomputable def rubberUtility
    (R_R b d L : ℝ) : ℝ :=
  R_R - b * d * L

noncomputable def noShowUtility
    (R_N : ℝ) : ℝ :=
  R_N

noncomputable def requiredComputeAdvantage
    (c b d L : ℝ) : ℝ :=
  c - b * d * L

theorem compute_dominates_rubber_iff
    (R_C R_R c b d L : ℝ) :
    rubberUtility R_R b d L ≤ computeUtility R_C c ↔
      c ≤ R_C - R_R + b * d * L := by
  unfold rubberUtility computeUtility
  constructor <;> intro h <;> linarith

theorem compute_dominates_noshow_iff
    (R_C R_N c : ℝ) :
    noShowUtility R_N ≤ computeUtility R_C c ↔
      c ≤ R_C - R_N := by
  unfold noShowUtility computeUtility
  constructor <;> intro h <;> linarith

theorem reward_advantage_threshold_identity
    (c b d L : ℝ) :
    c ≤ requiredComputeAdvantage c b d L + b * d * L := by
  unfold requiredComputeAdvantage
  linarith

/-- Lower exposure probability makes computation harder to incentivize through
fault deterrence: the required reward advantage increases. -/
theorem lower_exposure_raises_required_advantage
    {c b d₁ d₂ L : ℝ}
    (hb : 0 < b) (hL : 0 < L) (hd : d₁ < d₂) :
    requiredComputeAdvantage c b d₂ L <
      requiredComputeAdvantage c b d₁ L := by
  unfold requiredComputeAdvantage
  have hbd : b * d₁ < b * d₂ := by nlinarith
  nlinarith [mul_lt_mul_of_pos_right hbd hL]

/-- With zero exposure of false positives, penalty deterrence contributes
nothing and the full compute cost must be covered by reward advantage. -/
theorem zero_exposure_requires_full_cost
    (c b L : ℝ) :
    requiredComputeAdvantage c b 0 L = c := by
  unfold requiredComputeAdvantage
  ring

/-- With equal rewards, zero invalid-report opportunity and positive compute
cost, rubber-stamping strictly dominates actual computation. -/
theorem zero_invalid_equal_reward_rubber_dominates
    {R c d L : ℝ} (hc : 0 < c) :
    computeUtility R c < rubberUtility R 0 d L := by
  unfold computeUtility rubberUtility
  linarith

#print axioms compute_dominates_rubber_iff
#print axioms compute_dominates_noshow_iff
#print axioms reward_advantage_threshold_identity
#print axioms lower_exposure_raises_required_advantage
#print axioms zero_exposure_requires_full_cost
#print axioms zero_invalid_equal_reward_rubber_dominates

end DistributedCommons
