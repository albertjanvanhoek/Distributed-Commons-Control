import DistributedCommons
import Mathlib.Analysis.SpecialFunctions.Pow.Real

namespace DistributedCommons

noncomputable def nthRoot (n : ℕ) (x : ℝ) : ℝ := x ^ ((n : ℝ)⁻¹)

noncomputable def sufficientEffortN (n : ℕ) (b ρ ε : ℝ) : ℝ :=
  1 - nthRoot n (normalizedResidual b ρ ε)

theorem nthRoot_nonneg (n : ℕ) {x : ℝ} (hx : 0 ≤ x) :
    0 ≤ nthRoot n x := Real.rpow_nonneg hx _

theorem nthRoot_pow {n : ℕ} (hn : 0 < n) {x : ℝ} (hx : 0 ≤ x) :
    (nthRoot n x)^n = x := by
  exact Real.rpow_inv_natCast_pow hx (Nat.ne_of_gt hn)

/-- Order equivalence supplies both uniqueness and leastness. -/
theorem pow_le_iff_le_nthRoot {n : ℕ} (hn : 0 < n)
    {x y : ℝ} (hx : 0 ≤ x) (hy : 0 ≤ y) :
    y^n ≤ x ↔ y ≤ nthRoot n x := by
  have hnR : 0 < (n : ℝ) := by exact_mod_cast hn
  have h := Real.rpow_le_rpow_iff hy (nthRoot_nonneg n hx) hnR
  rw [Real.rpow_natCast, Real.rpow_natCast, nthRoot_pow hn hx] at h
  exact h

theorem nthRoot_unique {n : ℕ} (hn : 0 < n)
    {x y : ℝ} (hx : 0 ≤ x) (hy : 0 ≤ y) (heq : y^n = x) :
    y = nthRoot n x := by
  have hnR : 0 < (n : ℝ) := by exact_mod_cast hn
  apply le_antisymm
  · exact (pow_le_iff_le_nthRoot hn hx hy).mp heq.le
  · have h := Real.rpow_le_rpow_iff (nthRoot_nonneg n hx) hy hnR
    rw [Real.rpow_natCast, Real.rpow_natCast, nthRoot_pow hn hx, heq] at h
    exact h.mp le_rfl

theorem nthRoot_monotone (n : ℕ) {x y : ℝ} (hx : 0 ≤ x) (hxy : x ≤ y) :
    nthRoot n x ≤ nthRoot n y := by
  exact Real.rpow_le_rpow hx hxy (by positivity)

theorem residual_bounds {b ρ ε : ℝ} (hb : 0 < b) (hρ : ρ < 1)
    (hfloor : b * ρ ≤ ε) (htarget : ε < b) :
    0 ≤ normalizedResidual b ρ ε ∧ normalizedResidual b ρ ε < 1 := by
  have hd : 0 < 1 - ρ := sub_pos.mpr hρ
  have hlow : ρ ≤ ε / b := (le_div_iff₀ hb).mpr (by nlinarith)
  have hhigh : ε / b < 1 := (div_lt_iff₀ hb).mpr (by simpa using htarget)
  unfold normalizedResidual
  constructor
  · exact div_nonneg (sub_nonneg.mpr hlow) hd.le
  · apply (div_lt_iff₀ hd).mpr
    linarith

/-- Rewrites the actual safety inequality, without assuming a root. -/
theorem safety_iff_residual (n : ℕ) {b ρ ε q : ℝ}
    (hb : 0 < b) (hρ : ρ < 1) :
    badFinalizationN n b ρ q ≤ ε ↔
      (1-q)^n ≤ normalizedResidual b ρ ε := by
  unfold badFinalizationN escapeN normalizedResidual
  rw [le_div_iff₀ (sub_pos.mpr hρ)]
  have houter : b * (ρ + (1 - ρ) * (1 - q)^n) ≤ ε ↔
      ρ + (1 - ρ) * (1 - q)^n ≤ ε / b := by
    rw [le_div_iff₀ hb]
    constructor <;> intro h <;> nlinarith
  rw [houter]
  constructor <;> intro h <;> nlinarith

theorem sufficientEffortN_bounds {n : ℕ} (hn : 0 < n)
    {b ρ ε : ℝ} (hb : 0 < b) (hρ : ρ < 1)
    (hfloor : b * ρ ≤ ε) (htarget : ε < b) :
    0 < sufficientEffortN n b ρ ε ∧ sufficientEffortN n b ρ ε ≤ 1 := by
  obtain ⟨hx0, hx1⟩ := residual_bounds hb hρ hfloor htarget
  have hnR : 0 < (n : ℝ) := by exact_mod_cast hn
  have hr0 := nthRoot_nonneg n hx0
  have hr1 : nthRoot n (normalizedResidual b ρ ε) < 1 := by
    have h := Real.rpow_lt_rpow hx0 hx1 (inv_pos.mpr hnR)
    simpa [nthRoot] using h
  unfold sufficientEffortN
  constructor <;> linarith

/-- The closed form reaches the target exactly for every positive n. -/
theorem sufficientEffortN_hits_target {n : ℕ} (hn : 0 < n)
    {b ρ ε : ℝ} (hb : 0 < b) (hρ : ρ < 1)
    (hfloor : b * ρ ≤ ε) (htarget : ε < b) :
    badFinalizationN n b ρ (sufficientEffortN n b ρ ε) = ε := by
  apply sufficientEffort_hits_target_from_root n hb.ne' (ne_of_gt (sub_pos.mpr hρ))
  exact nthRoot_pow hn (residual_bounds hb hρ hfloor htarget).1

/-- End-to-end minimum-effort theorem: all feasible safe efforts are exactly
those at or above the explicit real-root threshold. -/
theorem safety_iff_sufficientEffortN {n : ℕ} (hn : 0 < n)
    {b ρ ε q : ℝ} (hb : 0 < b) (hρ : ρ < 1)
    (hfloor : b * ρ ≤ ε) (htarget : ε < b) (hq1 : q ≤ 1) :
    badFinalizationN n b ρ q ≤ ε ↔ sufficientEffortN n b ρ ε ≤ q := by
  rw [safety_iff_residual n hb hρ]
  rw [pow_le_iff_le_nthRoot hn (residual_bounds hb hρ hfloor htarget).1
    (sub_nonneg.mpr hq1)]
  unfold sufficientEffortN
  constructor <;> intro h <;> linarith

/-- Connects selected behavior, actual safety and the closed-form critical cost. -/
theorem selected_safety_iff_critical_cost {n : ℕ} (hn : 0 < n)
    {b ρ ε reward cost : ℝ} (hb : 0 < b) (hρ : ρ < 1)
    (hfloor : b * ρ ≤ ε) (htarget : ε < b)
    (hr : 0 ≤ reward) (hc : 0 < cost) :
    badFinalizationN n b ρ (feasibleSelectedEffort b ρ reward cost) ≤ ε ↔
      cost ≤ criticalEffortCost b ρ reward (sufficientEffortN n b ρ ε) := by
  have hq1 : feasibleSelectedEffort b ρ reward cost ≤ 1 := min_le_left _ _
  rw [safety_iff_sufficientEffortN hn hb hρ hfloor htarget hq1]
  obtain ⟨hq0, hq1'⟩ := sufficientEffortN_bounds hn hb hρ hfloor htarget
  exact feasibleSelectedEffort_meets_iff_cost_le_critical hb.le hρ.le hr hc hq0 hq1'

#print axioms nthRoot_nonneg
#print axioms nthRoot_pow
#print axioms pow_le_iff_le_nthRoot
#print axioms nthRoot_unique
#print axioms nthRoot_monotone
#print axioms residual_bounds
#print axioms safety_iff_residual
#print axioms sufficientEffortN_bounds
#print axioms sufficientEffortN_hits_target
#print axioms safety_iff_sufficientEffortN
#print axioms selected_safety_iff_critical_cost
end DistributedCommons
