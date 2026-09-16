import StateDependentContribution

namespace DistributedCommons

/-!
# Vector-valued contribution across viability loops

If a participant has positive contribution a to one declared viability loop and
negative contribution b to another, there is no weight-free scalar sign.

For positive scalarization weights:
- weights (-2b, a) give scalar -a*b > 0;
- weights (-b, 2a) give scalar a*b < 0.

Thus any scalar "net contribution" requires an explicit weighting choice.
-/

noncomputable def weightedTwo
    (w₁ w₂ a b : ℝ) : ℝ :=
  w₁ * a + w₂ * b

theorem positive_scalarization_witness
    {a b : ℝ} (ha : 0 < a) (hb : b < 0) :
    0 < -2 * b ∧
    0 < a ∧
    0 < weightedTwo (-2 * b) a a b := by
  constructor
  · nlinarith
  constructor
  · exact ha
  · unfold weightedTwo
    have hab : a * b < 0 := mul_neg_of_pos_of_neg ha hb
    nlinarith

theorem negative_scalarization_witness
    {a b : ℝ} (ha : 0 < a) (hb : b < 0) :
    0 < -b ∧
    0 < 2 * a ∧
    weightedTwo (-b) (2 * a) a b < 0 := by
  constructor
  · nlinarith
  constructor
  · nlinarith
  · unfold weightedTwo
    have hab : a * b < 0 := mul_neg_of_pos_of_neg ha hb
    nlinarith

#print axioms positive_scalarization_witness
#print axioms negative_scalarization_witness

end DistributedCommons
