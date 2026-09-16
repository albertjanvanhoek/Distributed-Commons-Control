import CorrectiveCapacity

namespace DistributedCommons

/-!
# State-dependent participant contribution

This file joins failure topology to stored corrective capacity at the algebraic
level.

If pi is the probability that all participants able to activate correction are
disabled, define expected finite-shock margin

  E[M] = X - V + (1-pi) * kappa*C.

For a participant that changes all-disabled probability from pi_before to
pi_after, its expected-margin contribution is

  kappa*C * (pi_before - pi_after).

Thus participant contribution is not a fixed trait: it scales with the current
reserve-capacity state C.

In the two-independent-cause example, changing escape from rho to rho^2 gives

  Delta M = kappa*C*rho*(1-rho).
-/

noncomputable def expectedAccessMargin
    (V κ X C π : ℝ) : ℝ :=
  X - V + (1 - π) * κ * C

/-- Exact participant contribution from a change in all-disabled probability. -/
theorem access_contribution_identity
    (V κ X C πBefore πAfter : ℝ) :
    expectedAccessMargin V κ X C πAfter -
      expectedAccessMargin V κ X C πBefore =
      κ * C * (πBefore - πAfter) := by
  unfold expectedAccessMargin
  ring

/-- A participant that strictly lowers all-disabled probability has positive
expected-margin contribution whenever useful reserve capacity exists. -/
theorem access_contribution_positive
    {V κ X C πBefore πAfter : ℝ}
    (hκ : 0 < κ) (hC : 0 < C) (hπ : πAfter < πBefore) :
    0 <
      expectedAccessMargin V κ X C πAfter -
        expectedAccessMargin V κ X C πBefore := by
  rw [access_contribution_identity]
  exact mul_pos (mul_pos hκ hC) (sub_pos.mpr hπ)

/-- In the two-cause decorrelation example, the independent-profile
participant's expected contribution is kappa*C*rho*(1-rho). -/
theorem independent_profile_capacity_contribution
    (V κ X C ρ : ℝ) :
    expectedAccessMargin V κ X C (ρ * ρ) -
      expectedAccessMargin V κ X C ρ =
      κ * C * ρ * (1 - ρ) := by
  rw [access_contribution_identity]
  ring

/-- If reserve capacity is zero, topology cannot contribute through the
capacity-access channel. -/
theorem zero_capacity_zero_access_contribution
    (V κ X πBefore πAfter : ℝ) :
    expectedAccessMargin V κ X 0 πAfter -
      expectedAccessMargin V κ X 0 πBefore = 0 := by
  rw [access_contribution_identity]
  ring

/-- Under quiet multiplicative capacity decay, the same topology contribution
shrinks by exactly the surviving capacity fraction. -/
theorem quiet_decay_scales_access_contribution
    (V κ X C δ πBefore πAfter : ℝ) :
    (expectedAccessMargin V κ X (quietCapacityStep δ C) πAfter -
      expectedAccessMargin V κ X (quietCapacityStep δ C) πBefore) =
      (1 - δ) *
        (expectedAccessMargin V κ X C πAfter -
          expectedAccessMargin V κ X C πBefore) := by
  rw [access_contribution_identity, access_contribution_identity]
  unfold quietCapacityStep
  ring

#print axioms access_contribution_identity
#print axioms access_contribution_positive
#print axioms independent_profile_capacity_contribution
#print axioms zero_capacity_zero_access_contribution
#print axioms quiet_decay_scales_access_contribution

end DistributedCommons
