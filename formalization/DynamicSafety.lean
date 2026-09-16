import RootSafety

namespace DistributedCommons

/-- Effort after depreciation a, with additive capacity u and requested z. -/
def feedback (a u z : ℝ) : ℝ := min (min 1 (a+u)) (max a z)

theorem feedback_bounds {a u z : ℝ} (ha0 : 0 ≤ a) (ha1 : a ≤ 1)
    (hu : 0 ≤ u) :
    0 ≤ feedback a u z ∧ feedback a u z ≤ 1 ∧
    a ≤ feedback a u z ∧ feedback a u z ≤ a+u := by
  have hlo : a ≤ feedback a u z := by
    unfold feedback
    exact le_min (le_min ha1 (by linarith)) (le_max_left _ _)
  have hhi : feedback a u z ≤ min 1 (a+u) := min_le_left _ _
  exact ⟨ha0.trans hlo, hhi.trans (min_le_left _ _), hlo,
    hhi.trans (min_le_right _ _)⟩

/-- Exact capacity boundary for reaching a target in [0,1]. -/
theorem feedback_reaches_iff {a u z : ℝ} (hz1 : z ≤ 1) :
    z ≤ feedback a u z ↔ z ≤ a+u := by
  unfold feedback
  constructor
  · intro h
    exact h.trans ((min_le_left _ _).trans (min_le_right _ _))
  · intro h
    exact le_min (le_min hz1 h) (le_max_right _ _)

theorem badFinalizationN_mono_attempt (n : ℕ) {b B ρ q : ℝ}
    (hbB : b ≤ B) (hr0 : 0 ≤ ρ) (hr1 : ρ ≤ 1) (hq1 : q ≤ 1) :
    badFinalizationN n b ρ q ≤ badFinalizationN n B ρ q := by
  have hescape : 0 ≤ escapeN n ρ q := by
    unfold escapeN
    have : 0 ≤ (1-ρ)*(1-q)^n :=
      mul_nonneg (sub_nonneg.mpr hr1) (pow_nonneg (sub_nonneg.mpr hq1) n)
    linarith
  exact mul_le_mul_of_nonneg_right hbB hescape

/-- Valid load envelope plus enough actuator capacity implies actual safety. -/
theorem robust_feedback_safe {n : ℕ} (hn : 0 < n)
    {b B ρ ε a u : ℝ} (hB : 0 < B) (hr0 : 0 ≤ ρ) (hr1 : ρ < 1)
    (hfloor : B*ρ ≤ ε) (htarget : ε < B) (hbB : b ≤ B)
    (hcapacity : sufficientEffortN n B ρ ε ≤ a+u) :
    badFinalizationN n b ρ (feedback a u (sufficientEffortN n B ρ ε)) ≤ ε := by
  have hz1 := (sufficientEffortN_bounds hn hB hr1 hfloor htarget).2
  have hq1 : feedback a u (sufficientEffortN n B ρ ε) ≤ 1 :=
    (min_le_left _ _).trans (min_le_left _ _)
  have hsafe : badFinalizationN n B ρ
      (feedback a u (sufficientEffortN n B ρ ε)) ≤ ε :=
    (safety_iff_sufficientEffortN hn hB hr1 hfloor htarget hq1).mpr
      ((feedback_reaches_iff hz1).mpr hcapacity)
  exact (badFinalizationN_mono_attempt n hbB hr0 hr1.le hq1).trans hsafe

/-- If capacity misses the robust target, every reachable effort fails at the
upper-envelope load B. This does not assert failure at every smaller load. -/
theorem capacity_shortfall_no_robust_action {n : ℕ} (hn : 0 < n)
    {B ρ ε a u q : ℝ} (hB : 0 < B) (hr1 : ρ < 1)
    (hfloor : B*ρ ≤ ε) (htarget : ε < B) (hq1 : q ≤ 1)
    (hreachable : q ≤ a+u) (hshort : a+u < sufficientEffortN n B ρ ε) :
    ε < badFinalizationN n B ρ q := by
  by_contra h
  have hsafe : badFinalizationN n B ρ q ≤ ε := le_of_not_gt h
  have hz := (safety_iff_sufficientEffortN hn hB hr1 hfloor htarget hq1).mp hsafe
  linarith

/-- A per-step rise bound implies a delayed-observation envelope. -/
theorem delayed_envelope (b : ℕ → ℝ) (v : ℝ)
    (hstep : ∀ t, b (t+1) ≤ b t + v) (t k : ℕ) :
    b (t+k) ≤ b t + (k : ℝ)*v := by
  induction k with
  | zero => simp
  | succ k ih =>
    have hs := hstep (t + k)
    rw [show t + Nat.succ k = t + k + 1 by omega]
    push_cast
    linarith

/-- Safety and feasible effort persist under repeated feedback, provided the
load-envelope, structural and capacity conditions hold at every transition. -/
theorem feedback_path_safe {n : ℕ} (hn : 0 < n)
    (b B q u : ℕ → ℝ) (ρ ε d : ℝ)
    (hr0 : 0 ≤ ρ) (hr1 : ρ < 1) (hd0 : 0 ≤ d) (hd1 : d ≤ 1)
    (hinit : 0 ≤ q 0 ∧ q 0 ≤ 1 ∧ badFinalizationN n (b 0) ρ (q 0) ≤ ε)
    (hB : ∀ t, 0 < B t) (hfloor : ∀ t, B t*ρ ≤ ε)
    (htarget : ∀ t, ε < B t) (henvelope : ∀ t, b (t+1) ≤ B t)
    (hu : ∀ t, 0 ≤ u t)
    (hcapacity : ∀ t, sufficientEffortN n (B t) ρ ε ≤ (1-d)*q t + u t)
    (hevolution : ∀ t, q (t+1) = feedback ((1-d)*q t) (u t)
      (sufficientEffortN n (B t) ρ ε)) :
    ∀ t, 0 ≤ q t ∧ q t ≤ 1 ∧ badFinalizationN n (b t) ρ (q t) ≤ ε := by
  intro t
  induction t with
  | zero => exact hinit
  | succ t ih =>
    have ha0 : 0 ≤ (1-d)*q t := mul_nonneg (sub_nonneg.mpr hd1) ih.1
    have ha1 : (1-d)*q t ≤ 1 := by nlinarith [mul_nonneg hd0 ih.1]
    have hbds := feedback_bounds (z := sufficientEffortN n (B t) ρ ε) ha0 ha1 (hu t)
    have hs := robust_feedback_safe hn (hB t) hr0 hr1 (hfloor t) (htarget t)
      (henvelope t) (hcapacity t)
    rw [hevolution t]
    exact ⟨hbds.1, hbds.2.1, hs⟩

#print axioms feedback_bounds
#print axioms feedback_reaches_iff
#print axioms badFinalizationN_mono_attempt
#print axioms robust_feedback_safe
#print axioms capacity_shortfall_no_robust_action
#print axioms delayed_envelope
#print axioms feedback_path_safe
end DistributedCommons
