import DynamicSafety

namespace DistributedCommons

/-!
# Endogenous common-mode floor

The static common-mode theorem bounds harmful finalization below by b * rho for
an externally supplied harmful-attempt rate b. This file closes one more loop:
if a producer responds monotonically to detection and collective detection has
a common-mode cap, then the producer's own target has a floor. Partial
adjustment preserves a finite-time lower envelope toward that floor.

The logistic response used by the Python model is one concrete antitone
response; the proofs here keep that behavioral response abstract.
-/

/-- Collective detection in the declared mixture. -/
def detectionN (n : ℕ) (ρ q : ℝ) : ℝ :=
  1 - escapeN n ρ q

/-- Common-mode correlation caps collective detection at 1-rho. -/
theorem detectionN_le_commonModeCap
    (n : ℕ) {ρ q : ℝ} (hρ1 : ρ ≤ 1) (hq1 : q ≤ 1) :
    detectionN n ρ q ≤ 1 - ρ := by
  have hfloor := escapeN_correlation_floor n hρ1 hq1
  unfold detectionN
  linarith

/-- Any producer response that is antitone in detection therefore has a
minimum target at the common-mode detection cap. -/
theorem response_floor_of_commonModeCap
    (response : ℝ → ℝ) (hresponse : Antitone response)
    (n : ℕ) {ρ q : ℝ} (hρ1 : ρ ≤ 1) (hq1 : q ≤ 1) :
    response (1 - ρ) ≤ response (detectionN n ρ q) := by
  exact hresponse (detectionN_le_commonModeCap n hρ1 hq1)

/-- One partial-adjustment step toward a producer target. -/
def producerUpdate (α b target : ℝ) : ℝ :=
  b + α * (target - b)

/-- If the current producer target is at least m and adjustment is
nonnegative, the next attempt rate is bounded by the affine envelope toward m. -/
theorem producerUpdate_lowerEnvelope
    {α b target m : ℝ} (hα0 : 0 ≤ α) (htarget : m ≤ target) :
    m + (1 - α) * (b - m) ≤ producerUpdate α b target := by
  have hprod : 0 ≤ α * (target - m) :=
    mul_nonneg hα0 (sub_nonneg.mpr htarget)
  unfold producerUpdate
  nlinarith

/-- Finite-time lower envelope for repeated partial adjustment toward targets
that never fall below m. This is stronger than a steady-state statement and
immediately yields convergence toward m from either side when the target
sequence approaches the floor. -/
theorem producerPath_lowerEnvelope
    (b target : ℕ → ℝ) (α m : ℝ)
    (hα0 : 0 ≤ α) (hα1 : α ≤ 1)
    (htarget : ∀ t, m ≤ target t)
    (hevolve : ∀ t, b (t + 1) = producerUpdate α (b t) (target t)) :
    ∀ t, m + (1 - α)^t * (b 0 - m) ≤ b t := by
  intro t
  induction t with
  | zero =>
      simp
  | succ t ih =>
      have hcoef : 0 ≤ 1 - α := sub_nonneg.mpr hα1
      have hshift : (1 - α)^t * (b 0 - m) ≤ b t - m := by
        linarith
      have hmul :
          (1 - α) * ((1 - α)^t * (b 0 - m))
            ≤ (1 - α) * (b t - m) :=
        mul_le_mul_of_nonneg_left hshift hcoef
      have hstep := producerUpdate_lowerEnvelope
        (α := α) (b := b t) (target := target t) (m := m)
        hα0 (htarget t)
      rw [hevolve t]
      rw [pow_succ]
      nlinarith

/-- Once a lower bound m on harmful-attempt probability is established,
common-mode correlation converts it into a lower bound rho*m on harmful
finalization. -/
theorem badFinalizationN_floor_from_attempt_floor
    (n : ℕ) {m b ρ q : ℝ}
    (hmb : m ≤ b) (hb0 : 0 ≤ b) (hρ0 : 0 ≤ ρ)
    (hρ1 : ρ ≤ 1) (hq1 : q ≤ 1) :
    ρ * m ≤ badFinalizationN n b ρ q := by
  have hattempt : ρ * m ≤ ρ * b :=
    mul_le_mul_of_nonneg_left hmb hρ0
  have hfloor := badFinalizationN_correlation_floor n hb0 hρ1 hq1
  nlinarith

#print axioms detectionN_le_commonModeCap
#print axioms response_floor_of_commonModeCap
#print axioms producerUpdate_lowerEnvelope
#print axioms producerPath_lowerEnvelope
#print axioms badFinalizationN_floor_from_attempt_floor

end DistributedCommons
