import Mathlib.Tactic

namespace DistributedCommons

/-!
# Distributed commons control: first algebraic core

This file checks narrow conditional results for arbitrary positive monitor
count n. English labels such as "harmful" and "commons" do not enter the
proofs; the theorems establish implications of the declared equations.
-/

/-- Conditional escape probability for n symmetric monitors under a
common-mode mixture. -/
def escapeN (n : ℕ) (ρ q : ℝ) : ℝ :=
  ρ + (1 - ρ) * (1 - q)^n

/-- Unconditional probability of harmful finalization. -/
def badFinalizationN (n : ℕ) (b ρ q : ℝ) : ℝ :=
  b * escapeN n ρ q

/-- Independent monitoring is the zero-correlation specialization. -/
theorem escapeN_independent (n : ℕ) (q : ℝ) :
    escapeN n 0 q = (1 - q)^n := by
  unfold escapeN
  ring

/-- With at least one monitor, perfect individual effort cannot remove the
common-mode blind spot. -/
theorem escapeN_perfect
    {n : ℕ} (hn : 0 < n) (ρ : ℝ) :
    escapeN n ρ 1 = ρ := by
  have hn0 : n ≠ 0 := Nat.ne_of_gt hn
  simp [escapeN, hn0]

/-- Consequently, perfect effort leaves the unconditional floor b*rho. -/
theorem badFinalizationN_perfect
    {n : ℕ} (hn : 0 < n) (b ρ : ℝ) :
    badFinalizationN n b ρ 1 = b * ρ := by
  unfold badFinalizationN
  rw [escapeN_perfect hn]

/-- For rho <= 1 and effort q <= 1, conditional escape cannot fall below
rho. Lower bounds zero are not needed for this algebraic direction. -/
theorem escapeN_correlation_floor
    (n : ℕ) {ρ q : ℝ} (hρ1 : ρ ≤ 1) (hq1 : q ≤ 1) :
    ρ ≤ escapeN n ρ q := by
  have hρ : 0 ≤ 1 - ρ := sub_nonneg.mpr hρ1
  have hq : 0 ≤ 1 - q := sub_nonneg.mpr hq1
  have hpower : 0 ≤ (1 - q)^n := pow_nonneg hq n
  have hproduct : 0 ≤ (1 - ρ) * (1 - q)^n :=
    mul_nonneg hρ hpower
  unfold escapeN
  linarith

/-- With nonnegative harmful-attempt probability, b*rho is an unconditional
lower bound on harmful finalization. -/
theorem badFinalizationN_correlation_floor
    (n : ℕ) {b ρ q : ℝ}
    (hb : 0 ≤ b) (hρ1 : ρ ≤ 1) (hq1 : q ≤ 1) :
    b * ρ ≤ badFinalizationN n b ρ q := by
  unfold badFinalizationN
  exact mul_le_mul_of_nonneg_left
    (escapeN_correlation_floor n hρ1 hq1) hb

/-- A declared safety target below the correlation floor is impossible within
this architecture for any monitor count, regardless of admissible effort. -/
theorem safety_impossible_below_correlation_floor_N
    (n : ℕ) {b ρ q ε : ℝ}
    (hb : 0 ≤ b) (hρ1 : ρ ≤ 1) (hq1 : q ≤ 1)
    (htarget : ε < b * ρ) :
    ¬ badFinalizationN n b ρ q ≤ ε := by
  intro hsafety
  have hfloor := badFinalizationN_correlation_floor n hb hρ1 hq1
  linarith

/-- Normalized independent-branch escape at the safety boundary. -/
noncomputable def normalizedResidual (b ρ ε : ℝ) : ℝ :=
  (ε / b - ρ) / (1 - ρ)

/-- For arbitrary n, any root s satisfying the normalized boundary equation
yields q = 1-s whose harmful-finalization probability is exactly epsilon.
This checks the algebraic substitution underlying the executable nth-root
formula without claiming root existence or leastness. -/
theorem sufficientEffort_hits_target_from_root
    (n : ℕ) {b ρ ε s : ℝ}
    (hb : b ≠ 0) (hρ : 1 - ρ ≠ 0)
    (hroot : s^n = normalizedResidual b ρ ε) :
    badFinalizationN n b ρ (1 - s) = ε := by
  unfold badFinalizationN escapeN
  have hsimplify : 1 - (1 - s) = s := by ring
  rw [hsimplify, hroot]
  unfold normalizedResidual
  field_simp [hb, hρ]
  ring

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

/-- The executable model clips the unconstrained optimum to the probability
interval. -/
noncomputable def feasibleSelectedEffort
    (b ρ reward cost : ℝ) : ℝ :=
  min 1 (max 0 (selectedEffort b ρ reward cost))

/-- Under probability-domain assumptions, the unconstrained selected effort
is nonnegative. -/
theorem selectedEffort_nonneg
    {b ρ reward cost : ℝ}
    (hb : 0 ≤ b) (hρ1 : ρ ≤ 1) (hreward : 0 ≤ reward)
    (hcost : 0 < cost) :
    0 ≤ selectedEffort b ρ reward cost := by
  unfold selectedEffort
  have hbranch : 0 ≤ 1 - ρ := sub_nonneg.mpr hρ1
  have hnum : 0 ≤ b * (1 - ρ) * reward := by positivity
  exact div_nonneg hnum (le_of_lt hcost)

/-- Clipping at zero and one does not change whether selected effort reaches
a required effort already known to lie in the probability interval. -/
theorem feasibleSelectedEffort_meets_iff
    {b ρ reward cost qRequired : ℝ}
    (hq0 : 0 ≤ qRequired) (hq1 : qRequired ≤ 1)
    (hselected0 : 0 ≤ selectedEffort b ρ reward cost) :
    qRequired ≤ feasibleSelectedEffort b ρ reward cost
      ↔
    qRequired ≤ selectedEffort b ρ reward cost := by
  unfold feasibleSelectedEffort
  rw [max_eq_right hselected0]
  constructor
  · intro h
    exact le_trans h (min_le_right 1 (selectedEffort b ρ reward cost))
  · intro h
    exact le_min hq1 h

/-- Critical effort cost at which private selection exactly reaches a
positive required effort. -/
noncomputable def criticalEffortCost
    (b ρ reward qRequired : ℝ) : ℝ :=
  b * (1 - ρ) * reward / qRequired

theorem cost_le_criticalEffortCost_iff
    {b ρ reward cost qRequired : ℝ}
    (hq : 0 < qRequired) :
    cost ≤ criticalEffortCost b ρ reward qRequired
      ↔
    cost * qRequired ≤ b * (1 - ρ) * reward := by
  unfold criticalEffortCost
  rw [le_div_iff₀ hq]

/-- Complete non-trivial phase boundary, including the executable model's
probability clipping: feasible selected effort reaches qRequired exactly when
effort cost is no greater than the critical cost. -/
theorem feasibleSelectedEffort_meets_iff_cost_le_critical
    {b ρ reward cost qRequired : ℝ}
    (hb : 0 ≤ b) (hρ1 : ρ ≤ 1) (hreward : 0 ≤ reward)
    (hcost : 0 < cost) (hq : 0 < qRequired) (hq1 : qRequired ≤ 1) :
    qRequired ≤ feasibleSelectedEffort b ρ reward cost
      ↔
    cost ≤ criticalEffortCost b ρ reward qRequired := by
  have hselected0 := selectedEffort_nonneg hb hρ1 hreward hcost
  rw [feasibleSelectedEffort_meets_iff (le_of_lt hq) hq1 hselected0]
  exact (selectedEffort_meets_requirement_iff hcost).trans
    (cost_le_criticalEffortCost_iff hq).symm

#print axioms escapeN_independent
#print axioms escapeN_perfect
#print axioms badFinalizationN_perfect
#print axioms escapeN_correlation_floor
#print axioms badFinalizationN_correlation_floor
#print axioms safety_impossible_below_correlation_floor_N
#print axioms sufficientEffort_hits_target_from_root
#print axioms monitorObjective_gap
#print axioms selectedEffort_global_max
#print axioms selectedEffort_meets_requirement_iff
#print axioms selectedEffort_underprovides
#print axioms selectedEffort_nonneg
#print axioms feasibleSelectedEffort_meets_iff
#print axioms cost_le_criticalEffortCost_iff
#print axioms feasibleSelectedEffort_meets_iff_cost_le_critical

end DistributedCommons
