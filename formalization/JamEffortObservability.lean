import JamBehaviorSelection

namespace DistributedCommons

/-!
# JAM effort observability and maintenance return-loop closure

Let
- s be effective observability/discrimination of real compute versus
  rubber-stamping,
- W be the available higher-layer reward differential,
- c be compute cost,
- b*d*L be expected fault deterrence.

The maintenance-selection margin is

  s*W + b*d*L - c.

Compute can be selected only if this margin is nonnegative.

For W>0 the minimum observability required is

  (c - b*d*L) / W.

This formalizes the second-order maintenance requirement suggested by the
Gray Paper's peer-impression mechanism: reward can only selectively reinforce
maintenance to the extent that maintenance is observable.
-/

noncomputable def maintenanceSelectionMargin
    (s W c b d L : ℝ) : ℝ :=
  s * W + b * d * L - c

noncomputable def requiredEffortObservability
    (W c b d L : ℝ) : ℝ :=
  (c - b * d * L) / W

theorem observability_threshold_iff
    {s W c b d L : ℝ}
    (hW : 0 < W) :
    0 ≤ maintenanceSelectionMargin s W c b d L ↔
      requiredEffortObservability W c b d L ≤ s := by
  unfold maintenanceSelectionMargin requiredEffortObservability
  constructor
  · intro h
    have hmul : c - b * d * L ≤ s * W := by linarith
    exact (div_le_iff₀ hW).2 hmul
  · intro h
    have hmul : c - b * d * L ≤ s * W := (div_le_iff₀ hW).1 h
    linarith

/-- With zero effort observability, reward budget has no selection effect. -/
theorem zero_observability_removes_reward_channel
    (W c b d L : ℝ) :
    maintenanceSelectionMargin 0 W c b d L =
      b * d * L - c := by
  unfold maintenanceSelectionMargin
  ring

/-- If even the full reward budget plus fault deterrence is below compute cost,
perfect observability cannot select real computation. -/
theorem perfect_observability_insufficient
    {W c b d L : ℝ}
    (h : W + b * d * L < c) :
    maintenanceSelectionMargin 1 W c b d L < 0 := by
  unfold maintenanceSelectionMargin
  linarith

/-- Higher effort observability strictly raises the selection margin when the
reward budget is positive. -/
theorem higher_observability_improves_selection
    {s₁ s₂ W c b d L : ℝ}
    (hW : 0 < W) (hs : s₁ < s₂) :
    maintenanceSelectionMargin s₁ W c b d L <
      maintenanceSelectionMargin s₂ W c b d L := by
  unfold maintenanceSelectionMargin
  nlinarith

/-- Lower structural exposure raises the observability threshold required to
close the same return loop, provided reward budget, invalid opportunity and
fault loss are positive. -/
theorem lower_exposure_raises_observability_threshold
    {W c b d₁ d₂ L : ℝ}
    (hW : 0 < W) (hb : 0 < b) (hL : 0 < L) (hd : d₁ < d₂) :
    requiredEffortObservability W c b d₂ L <
      requiredEffortObservability W c b d₁ L := by
  unfold requiredEffortObservability
  have hnum :
      c - b * d₂ * L <
        c - b * d₁ * L := by
    nlinarith [mul_lt_mul_of_pos_right
      (mul_lt_mul_of_pos_left hd hb) hL]
  exact (div_lt_div_iff_of_pos_right hW).2 hnum

#print axioms observability_threshold_iff
#print axioms zero_observability_removes_reward_channel
#print axioms perfect_observability_insufficient
#print axioms higher_observability_improves_selection
#print axioms lower_exposure_raises_observability_threshold

end DistributedCommons
