import BehavioralMaintenance

namespace DistributedCommons

/-!
# JAM maintenance-operator perturbations

This file formalizes count-based identities used in Experiment 9.

Let
- n = total validator count,
- H = honest validator count,
- B = honest validators on a vulnerable client profile,
- U = validators contributing to the no-show/fault reproduction term,
- sδ = tranche/escalation parameter.

Then the grounded/extended reproduction quantities can be written as

  λ = sδ * (H - B) / n
  A = sδ * U / n
  L = 1 - A.

Moving one validator from the vulnerable client profile to a correct/independent
profile changes B -> B-1 and therefore raises λ by exactly sδ/n.

Moving one validator out of the no-show-prone count changes U -> U-1 and raises
the scalability margin L by exactly sδ/n.

Increasing sδ has opposite signs on the two loop margins whenever H>B and U>0:
it raises λ but lowers L.

These are substrate-specific algebraic identities. They do not formalize the
full ELVES extinction-probability theorem.
-/

noncomputable def jamCorrectionReproduction
    (n H B sδ : ℝ) : ℝ :=
  sδ * (H - B) / n

noncomputable def jamFailureReproduction
    (n U sδ : ℝ) : ℝ :=
  sδ * U / n

noncomputable def jamScalabilityMargin
    (n U sδ : ℝ) : ℝ :=
  1 - jamFailureReproduction n U sδ

/-- Diversifying exactly one validator raises the honest-correction reproduction
number by sδ/n. -/
theorem one_validator_diversification_gain
    {n H B sδ : ℝ} (hn : n ≠ 0) :
    jamCorrectionReproduction n H (B - 1) sδ -
      jamCorrectionReproduction n H B sδ =
      sδ / n := by
  unfold jamCorrectionReproduction
  field_simp [hn]
  ring

/-- Making exactly one validator reliable raises the scalability margin by the
same amount sδ/n. -/
theorem one_validator_reliability_gain
    {n U sδ : ℝ} (hn : n ≠ 0) :
    jamScalabilityMargin n (U - 1) sδ -
      jamScalabilityMargin n U sδ =
      sδ / n := by
  unfold jamScalabilityMargin jamFailureReproduction
  field_simp [hn]
  ring

/-- Increasing escalation strength by d raises correction reproduction by
d*(H-B)/n. -/
theorem escalation_correction_change
    {n H B sδ d : ℝ} (hn : n ≠ 0) :
    jamCorrectionReproduction n H B (sδ + d) -
      jamCorrectionReproduction n H B sδ =
      d * (H - B) / n := by
  unfold jamCorrectionReproduction
  field_simp [hn]
  ring

/-- Increasing escalation strength by d lowers the scalability margin by
d*U/n. -/
theorem escalation_scalability_change
    {n U sδ d : ℝ} (hn : n ≠ 0) :
    jamScalabilityMargin n U (sδ + d) -
      jamScalabilityMargin n U sδ =
      -(d * U / n) := by
  unfold jamScalabilityMargin jamFailureReproduction
  field_simp [hn]
  ring

/-- Under positive population, useful honest correction, and a positive
escalation increase, stronger escalation raises λ. -/
theorem escalation_improves_correction
    {n H B sδ d : ℝ}
    (hn : 0 < n) (hHB : B < H) (hd : 0 < d) :
    jamCorrectionReproduction n H B sδ <
      jamCorrectionReproduction n H B (sδ + d) := by
  have hn0 : n ≠ 0 := ne_of_gt hn
  rw [← sub_pos]
  rw [escalation_correction_change hn0]
  positivity

/-- Under a positive no-show-prone population, the same escalation increase
reduces the scalability margin. -/
theorem escalation_harms_scalability
    {n U sδ d : ℝ}
    (hn : 0 < n) (hU : 0 < U) (hd : 0 < d) :
    jamScalabilityMargin n U (sδ + d) <
      jamScalabilityMargin n U sδ := by
  have hn0 : n ≠ 0 := ne_of_gt hn
  rw [← sub_neg]
  rw [escalation_scalability_change hn0]
  have hpos : 0 < d * U / n := by positivity
  linarith

#print axioms one_validator_diversification_gain
#print axioms one_validator_reliability_gain
#print axioms escalation_correction_change
#print axioms escalation_scalability_change
#print axioms escalation_improves_correction
#print axioms escalation_harms_scalability

end DistributedCommons
