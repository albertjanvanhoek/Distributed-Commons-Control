import ClosedLoopStability

namespace DistributedCommons

/-!
# Viability contribution under heterogeneous failure causes

This file formalizes the algebraic core of the first neutral participant model.
The executable model allows arbitrary participants and independent failure
causes. Here we isolate the smallest exact example.

Two existing participants share one failure cause with activation probability
rho, so their structural escape probability is rho. Adding one participant
whose corrective action is disabled only by an independent cause with the same
activation probability changes structural escape to rho^2.

In the nontrivial uncapped regime, viability margin is epsilon / escape.
Thus the independent-profile participant changes the margin by a factor 1/rho.

The theorem is about failure topology, not any ecological or protocol mapping.
-/

/-- Viability margin before the probability-one cap is reached. -/
noncomputable def uncappedMargin (ε p : ℝ) : ℝ :=
  ε / p

/-- An independent second failure cause lowers structural escape whenever the
single-cause probability lies strictly between zero and one. -/
theorem independent_profile_lowers_escape
    {ρ : ℝ} (hρ0 : 0 < ρ) (hρ1 : ρ < 1) :
    ρ * ρ < ρ := by
  nlinarith [mul_pos hρ0 (sub_pos.mpr hρ1)]

/-- In the uncapped regime, changing escape from rho to rho^2 strictly raises
the declared viability margin. -/
theorem independent_profile_increases_margin
    {ε ρ : ℝ} (hε : 0 < ε) (hρ0 : 0 < ρ) (hρ1 : ρ < 1) :
    uncappedMargin ε ρ < uncappedMargin ε (ρ * ρ) := by
  have hρne : ρ ≠ 0 := ne_of_gt hρ0
  have hdiff :
      uncappedMargin ε (ρ * ρ) - uncappedMargin ε ρ =
        ε * (1 - ρ) / (ρ * ρ) := by
    unfold uncappedMargin
    field_simp [hρne]
  have hpos : 0 < ε * (1 - ρ) / (ρ * ρ) := by
    positivity
  linarith

/-- Exact gain in uncapped viability margin from the independent failure
profile. -/
theorem independent_profile_margin_gain
    {ε ρ : ℝ} (hρ : ρ ≠ 0) :
    uncappedMargin ε (ρ * ρ) - uncappedMargin ε ρ =
      ε * (1 - ρ) / (ρ * ρ) := by
  unfold uncappedMargin
  field_simp [hρ]

/-- The new margin is exactly the old margin divided by rho. -/
theorem independent_profile_margin_ratio
    {ε ρ : ℝ} (hρ : ρ ≠ 0) :
    uncappedMargin ε (ρ * ρ) =
      uncappedMargin ε ρ / ρ := by
  unfold uncappedMargin
  field_simp [hρ]

#print axioms independent_profile_lowers_escape
#print axioms independent_profile_increases_margin
#print axioms independent_profile_margin_gain
#print axioms independent_profile_margin_ratio

end DistributedCommons
