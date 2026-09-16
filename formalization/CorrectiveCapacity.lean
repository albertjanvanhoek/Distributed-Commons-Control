import SelectedViability

namespace DistributedCommons

/-!
# Shared state and slow corrective capacity

A neutral two-state model separates current shared condition X from a slower
corrective-capacity stock C.

The uncapped finite-shock margin is

  M(X,C) = X - V + kappa*C,

derived from the viability condition after deploying the full available fast
correction:

  X - shock + kappa*C >= V.

Between shocks,

  X' = X + gamma*(1-X)
  C' = (1-delta)*C

when maintenance input is zero.

At X=1, the shared state remains exactly 1 while positive capacity decay
strictly lowers M. Thus identical current state and identical local X recovery
can coexist with different finite-shock robustness.
-/

noncomputable def capacityShockMargin
    (V κ X C : ℝ) : ℝ :=
  X - V + κ * C

noncomputable def quietSharedStep
    (γ X : ℝ) : ℝ :=
  X + γ * (1 - X)

noncomputable def quietCapacityStep
    (δ C : ℝ) : ℝ :=
  (1 - δ) * C

/-- The shock-margin formula is exactly equivalent to the post-correction
viability inequality when full available capacity is deployed. -/
theorem shock_viable_iff_below_margin
    {V κ X C s : ℝ} :
    V ≤ X - s + κ * C ↔
      s ≤ capacityShockMargin V κ X C := by
  unfold capacityShockMargin
  constructor <;> intro h <;> linarith

/-- Full shared state is a fixed point of quiet shared-state recovery. -/
theorem quietSharedStep_full
    (γ : ℝ) :
    quietSharedStep γ 1 = 1 := by
  unfold quietSharedStep
  ring

/-- At fixed shared state, the entire margin difference is the capacity
difference scaled by correction efficiency. -/
theorem capacity_margin_difference
    (V κ X C₁ C₂ : ℝ) :
    capacityShockMargin V κ X C₂ -
      capacityShockMargin V κ X C₁ =
      κ * (C₂ - C₁) := by
  unfold capacityShockMargin
  ring

/-- More capacity strictly raises finite-shock margin when correction
efficiency is positive. -/
theorem higher_capacity_higher_margin
    {V κ X C₁ C₂ : ℝ}
    (hκ : 0 < κ) (hC : C₁ < C₂) :
    capacityShockMargin V κ X C₁ <
      capacityShockMargin V κ X C₂ := by
  have hdiff : 0 < κ * (C₂ - C₁) :=
    mul_pos hκ (sub_pos.mpr hC)
  rw [← sub_pos]
  rw [capacity_margin_difference]
  exact hdiff

/-- With no maintenance, one quiet step changes the full-state shock margin by
exactly -kappa*delta*C. -/
theorem quiet_capacity_margin_change_at_full_state
    (V κ δ C : ℝ) :
    capacityShockMargin V κ 1 (quietCapacityStep δ C) -
      capacityShockMargin V κ 1 C =
      -(κ * δ * C) := by
  unfold capacityShockMargin quietCapacityStep
  ring

/-- Therefore a quiet period can hide strictly increasing fragility: X stays
at its full fixed point while positive capacity decay lowers the shock margin. -/
theorem quiet_capacity_erodes_margin_at_full_state
    {V κ δ C : ℝ}
    (hκ : 0 < κ) (hδ : 0 < δ) (hC : 0 < C) :
    capacityShockMargin V κ 1 (quietCapacityStep δ C) <
      capacityShockMargin V κ 1 C := by
  rw [← sub_neg]
  rw [quiet_capacity_margin_change_at_full_state]
  have hpos : 0 < κ * δ * C := by positivity
  linarith

#print axioms shock_viable_iff_below_margin
#print axioms quietSharedStep_full
#print axioms capacity_margin_difference
#print axioms higher_capacity_higher_margin
#print axioms quiet_capacity_margin_change_at_full_state
#print axioms quiet_capacity_erodes_margin_at_full_state

end DistributedCommons
