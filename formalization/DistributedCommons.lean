import Mathlib.Tactic

namespace DistributedCommons

/-!
# Distributed commons control: first algebraic core

This file checks narrow conditional results for the three-monitor version of
the model. English labels such as "harmful" and "commons" do not enter the
proofs; the theorems establish implications of the declared equations.
-/

/-- Conditional escape probability for three symmetric monitors under a
common-mode mixture. -/
def escape3 (ρ q : ℝ) : ℝ :=
  ρ + (1 - ρ) * (1 - q)^3

/-- Unconditional probability of harmful finalization. -/
def badFinalization (b ρ q : ℝ) : ℝ :=
  b * escape3 ρ q

/-- Independent monitoring is the zero-correlation specialization. -/
theorem escape3_independent (q : ℝ) :
    escape3 0 q = (1 - q)^3 := by
  unfold escape3
  ring

/-- Perfect individual effort cannot remove the common-mode blind spot. -/
theorem escape3_perfect (ρ : ℝ) :
    escape3 ρ 1 = ρ := by
  unfold escape3
  ring

/-- Consequently, perfect effort leaves the unconditional floor b*rho. -/
theorem badFinalization_perfect (b ρ : ℝ) :
    badFinalization b ρ 1 = b * ρ := by
  unfold badFinalization
  rw [escape3_perfect]

/-- For rho <= 1 and effort q <= 1, conditional escape cannot fall below
rho. Lower bounds zero are not needed for this algebraic direction. -/
theorem escape3_correlation_floor
    {ρ q : ℝ} (hρ1 : ρ ≤ 1) (hq1 : q ≤ 1) :
    ρ ≤ escape3 ρ q := by
  have hρ : 0 ≤ 1 - ρ := sub_nonneg.mpr hρ1
  have hq : 0 ≤ 1 - q := sub_nonneg.mpr hq1
  have hcube : 0 ≤ (1 - q)^3 := pow_nonneg hq 3
  have hproduct : 0 ≤ (1 - ρ) * (1 - q)^3 :=
    mul_nonneg hρ hcube
  unfold escape3
  linarith

/-- With nonnegative harmful-attempt probability, b*rho is an unconditional
lower bound on harmful finalization. -/
theorem badFinalization_correlation_floor
    {b ρ q : ℝ}
    (hb : 0 ≤ b) (hρ1 : ρ ≤ 1) (hq1 : q ≤ 1) :
    b * ρ ≤ badFinalization b ρ q := by
  unfold badFinalization
  exact mul_le_mul_of_nonneg_left
    (escape3_correlation_floor hρ1 hq1) hb

/-- A declared safety target below the correlation floor is impossible within
this architecture, regardless of admissible effort. -/
theorem safety_impossible_below_correlation_floor
    {b ρ q ε : ℝ}
    (hb : 0 ≤ b) (hρ1 : ρ ≤ 1) (hq1 : q ≤ 1)
    (htarget : ε < b * ρ) :
    ¬ badFinalization b ρ q ≤ ε := by
  intro hsafety
  have hfloor := badFinalization_correlation_floor hb hρ1 hq1
  linarith

/-- Private quadratic objective for one monitor. -/
noncomputable def monitorObjective (b ρ reward cost q : ℝ) : ℝ :=
  b * (1 - ρ) * reward * q - (cost / 2) * q^2

/-- Unconstrained effort selected by the quadratic private objective. -/
noncomputable def selectedEffort (b ρ reward cost : ℝ) : ℝ :=
  b * (1 - ρ) * reward / cost

/-- Completing the square gives a global optimum certificate. -/
theorem monitorObjective_gap
    {b ρ reward cost q : ℝ} (hcost : cost ≠ 0) :
    monitorObjective b ρ reward cost (selectedEffort b ρ reward cost)
      - monitorObjective b ρ reward cost q
      =
    (cost / 2) * (q - selectedEffort b ρ reward cost)^2 := by
  unfold monitorObjective selectedEffort
  field_simp [hcost]
  ring

/-- Positive quadratic cost makes selectedEffort a global maximizer of the
unconstrained private objective. -/
theorem selectedEffort_global_max
    {b ρ reward cost q : ℝ} (hcost : 0 < cost) :
    monitorObjective b ρ reward cost q
      ≤ monitorObjective b ρ reward cost (selectedEffort b ρ reward cost) := by
  have hgap := monitorObjective_gap
    (b := b) (ρ := ρ) (reward := reward) (cost := cost) (q := q) hcost.ne'
  have hnonneg :
      0 ≤ (cost / 2) * (q - selectedEffort b ρ reward cost)^2 := by
    positivity
  linarith

/-- Exact selected-versus-required boundary for positive effort cost. -/
theorem selectedEffort_meets_requirement_iff
    {b ρ reward cost qRequired : ℝ} (hcost : 0 < cost) :
    qRequired ≤ selectedEffort b ρ reward cost
      ↔
    cost * qRequired ≤ b * (1 - ρ) * reward := by
  unfold selectedEffort
  rw [le_div_iff₀ hcost]
  constructor <;> intro h <;> nlinarith

/-- If private marginal return lies below the cost of required effort,
locally selected effort underprovides the declared requirement. -/
theorem selectedEffort_underprovides
    {b ρ reward cost qRequired : ℝ}
    (hcost : 0 < cost)
    (hunder : b * (1 - ρ) * reward < cost * qRequired) :
    selectedEffort b ρ reward cost < qRequired := by
  unfold selectedEffort
  apply (div_lt_iff₀ hcost).2
  nlinarith

#print axioms escape3_independent
#print axioms escape3_perfect
#print axioms badFinalization_perfect
#print axioms escape3_correlation_floor
#print axioms badFinalization_correlation_floor
#print axioms safety_impossible_below_correlation_floor
#print axioms monitorObjective_gap
#print axioms selectedEffort_global_max
#print axioms selectedEffort_meets_requirement_iff
#print axioms selectedEffort_underprovides

end DistributedCommons
