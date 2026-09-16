import ViabilityContribution

namespace DistributedCommons

/-!
# Selected viability reversal

A substrate-neutral two-participant shared-reward game.

Let z = b*r/c denote the interior one-participant selected checking effort.
With one participant,

  q₁ = z.

With two participants sharing a fixed reward equally among successful
checkers, a participant facing peer effort q has best-response first-order
condition

  qᵢ = z * (1 - q/2).

The symmetric fixed point is

  q₂ = 2z / (2+z).

For harmful-attempt rate b and declared target epsilon, define viability
margin as epsilon minus harmful-finalization probability.

Adding a second participant while freezing both efforts at z has positive
direct contribution for 0<z<1. But after re-equilibration the selected
contribution is negative whenever

  z^2 + 4z - 4 > 0.

The positive root is 2*(sqrt 2 - 1) ~= 0.8284. The Lean theorem uses the
equivalent polynomial condition to avoid importing square-root machinery.

This is a possibility theorem for a neutral behavioral mechanism, not a JAM
incentive model.
-/

noncomputable def twoSelectedEffort (z : ℝ) : ℝ :=
  2 * z / (2 + z)

noncomputable def oneSelectedMargin (b ε z : ℝ) : ℝ :=
  ε - b * (1 - z)

noncomputable def twoFrozenMargin (b ε z : ℝ) : ℝ :=
  ε - b * (1 - z)^2

noncomputable def twoSelectedMargin (b ε z : ℝ) : ℝ :=
  ε - b * (1 - twoSelectedEffort z)^2

/-- The declared two-participant effort is exactly the symmetric best-response
fixed point of the shared-reward game. -/
theorem twoSelectedEffort_fixedPoint
    {z : ℝ} (hden : 2 + z ≠ 0) :
    twoSelectedEffort z =
      z * (1 - twoSelectedEffort z / 2) := by
  unfold twoSelectedEffort
  field_simp [hden]
  ring

/-- Direct/frozen addition improves margin by b*z*(1-z). -/
theorem direct_addition_identity
    (b ε z : ℝ) :
    twoFrozenMargin b ε z - oneSelectedMargin b ε z =
      b * z * (1 - z) := by
  unfold twoFrozenMargin oneSelectedMargin
  ring

/-- Hence the direct effect is strictly positive in the interior. -/
theorem direct_addition_positive
    {b ε z : ℝ} (hb : 0 < b) (hz0 : 0 < z) (hz1 : z < 1) :
    0 < twoFrozenMargin b ε z - oneSelectedMargin b ε z := by
  rw [direct_addition_identity]
  exact mul_pos (mul_pos hb hz0) (sub_pos.mpr hz1)

/-- Exact total selected contribution after the two participants re-equilibrate. -/
theorem selected_addition_identity
    {b ε z : ℝ} (hden : 2 + z ≠ 0) :
    twoSelectedMargin b ε z - oneSelectedMargin b ε z =
      -b * z * (z^2 + 4*z - 4) / (2 + z)^2 := by
  unfold twoSelectedMargin oneSelectedMargin twoSelectedEffort
  field_simp [hden]
  ring

/-- Behavioral re-equilibration reverses the positive direct contribution once
z^2 + 4z - 4 is positive. -/
theorem selected_addition_negative
    {b ε z : ℝ}
    (hb : 0 < b) (hz0 : 0 < z)
    (hreversal : 0 < z^2 + 4*z - 4) :
    twoSelectedMargin b ε z - oneSelectedMargin b ε z < 0 := by
  have hden : 2 + z ≠ 0 := by nlinarith
  rw [selected_addition_identity hden]
  have hnum : -b * z * (z^2 + 4*z - 4) < 0 := by
    have hneg : -b * z < 0 := by nlinarith [mul_pos hb hz0]
    exact mul_neg_of_neg_of_pos hneg hreversal
  have hdenpos : 0 < (2 + z)^2 := by positivity
  exact div_neg_of_neg_of_pos hnum hdenpos

#print axioms twoSelectedEffort_fixedPoint
#print axioms direct_addition_identity
#print axioms direct_addition_positive
#print axioms selected_addition_identity
#print axioms selected_addition_negative

end DistributedCommons
