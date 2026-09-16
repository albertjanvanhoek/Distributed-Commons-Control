import EndogenousFloor

namespace DistributedCommons

/-!
# Closed-loop local stability

For the reduced discrete-time commons map

  X_{t+1} = X_t + γ (1 - X_t) - δ P(X_t),

an interior equilibrium satisfies

  δ P = γ (1 - X).

If P is differentiable at the equilibrium with slope dP, the local multiplier
is

  M = 1 - γ - δ dP.

Define the dimensionless loop gain

  η = -(1 - X) dP / P.

The theorems below verify the algebraic core of the stability criterion. Under
0 < γ <= 1, P > 0, X <= 1 and dP <= 0, the equilibrium relation implies

  M = 1 - γ + γ η,

and therefore |M| < 1 iff η < 1.

The standard one-dimensional linear-stability fact that |M| < 1 gives local
asymptotic stability is not itself formalized here.
-/

/-- Dimensionless closed-loop gain for the linear-regeneration reduced model. -/
noncomputable def commonsLoopGain (X P dP : ℝ) : ℝ :=
  -((1 - X) * dP) / P

/-- Derivative multiplier of the reduced one-step map at an equilibrium. -/
noncomputable def commonsMultiplier (γ δ dP : ℝ) : ℝ :=
  1 - γ - δ * dP

/-- The equilibrium relation rewrites the map multiplier in terms of loop gain. -/
theorem commonsMultiplier_eq_one_sub_gamma_add_gain
    {γ δ X P dP : ℝ} (hP : 0 < P)
    (heq : δ * P = γ * (1 - X)) :
    commonsMultiplier γ δ dP =
      1 - γ + γ * commonsLoopGain X P dP := by
  have hδ : δ = γ * (1 - X) / P := by
    exact (eq_div_iff hP.ne').2 heq
  rw [hδ]
  unfold commonsMultiplier commonsLoopGain
  field_simp [hP.ne']
  ring

/-- If protection improves with commons health, the loop gain is nonnegative. -/
theorem commonsLoopGain_nonneg
    {X P dP : ℝ} (hX : X ≤ 1) (hP : 0 < P) (hdP : dP ≤ 0) :
    0 ≤ commonsLoopGain X P dP := by
  unfold commonsLoopGain
  have hx : 0 ≤ 1 - X := sub_nonneg.mpr hX
  have hprod : (1 - X) * dP ≤ 0 :=
    mul_nonpos_of_nonneg_of_nonpos hx hdP
  have hnum : 0 ≤ -((1 - X) * dP) := neg_nonneg.mpr hprod
  exact div_nonneg hnum hP.le

/-- For the declared discrete-time reduced map, the usual local multiplier
condition is exactly the loop-gain threshold eta < 1. -/
theorem abs_commonsMultiplier_lt_one_iff_loopGain_lt_one
    {γ δ X P dP : ℝ}
    (hγ0 : 0 < γ) (hγ1 : γ ≤ 1)
    (hX : X ≤ 1) (hP : 0 < P) (hdP : dP ≤ 0)
    (heq : δ * P = γ * (1 - X)) :
    |commonsMultiplier γ δ dP| < 1 ↔
      commonsLoopGain X P dP < 1 := by
  have heta0 := commonsLoopGain_nonneg hX hP hdP
  rw [commonsMultiplier_eq_one_sub_gamma_add_gain hP heq]
  have hmult0 :
      0 ≤ 1 - γ + γ * commonsLoopGain X P dP := by
    have hγnonneg : 0 ≤ γ := hγ0.le
    have hprod :
        0 ≤ γ * commonsLoopGain X P dP :=
      mul_nonneg hγnonneg heta0
    nlinarith
  rw [abs_of_nonneg hmult0]
  constructor <;> intro h <;> nlinarith

/-- At eta = 1 the local multiplier equals one, the neutral condition at a
generic fold of the one-dimensional reduced equilibrium branch. -/
theorem commonsMultiplier_eq_one_of_loopGain_eq_one
    {γ δ X P dP : ℝ} (hP : 0 < P)
    (heq : δ * P = γ * (1 - X))
    (heta : commonsLoopGain X P dP = 1) :
    commonsMultiplier γ δ dP = 1 := by
  rw [commonsMultiplier_eq_one_sub_gamma_add_gain hP heq, heta]
  ring

#print axioms commonsMultiplier_eq_one_sub_gamma_add_gain
#print axioms commonsLoopGain_nonneg
#print axioms abs_commonsMultiplier_lt_one_iff_loopGain_lt_one
#print axioms commonsMultiplier_eq_one_of_loopGain_eq_one

end DistributedCommons
