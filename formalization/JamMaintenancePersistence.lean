import JamResilienceDynamics

namespace DistributedCommons

/-!
# JAM: persistent corrective resilience from a closed maintenance loop

`JamRecurrentMaintenance.lean` gives the static three-process replacement
threshold, while `JamResilienceDynamics.lean` couples slow corrective capacity
to the fast audit reproduction number. This module closes the remaining gap:
it proves directly on the full C -> O -> R -> C state dynamics that the cone
above a canonical maintenance witness is forward invariant when the closed-loop
product meets replacement.

Consequently, if the canonical corrective coordinate is already sufficient to
make the fast audit reproduction number supercritical, then every future point
on the canonical slow trajectory remains audit-supercritical.

The mathematics is the finite directed-three-cycle specialization of standard
positive-systems / reproduction-number reasoning. The JAM-facing contribution
is the explicit bridge from a closed cross-audit maintenance loop to persistent
within-audit corrective reproduction.
-/

/-- Canonical corrective coordinate for the C -> O -> R -> C witness. -/
noncomputable def jamCanonicalCorrective (rO rR : ℝ) : ℝ :=
  (1 - rO) * (1 - rR)

/-- Canonical observability coordinate. -/
noncomputable def jamCanonicalObservability (kCO rR : ℝ) : ℝ :=
  kCO * (1 - rR)

/-- Canonical returned-resource coordinate. -/
noncomputable def jamCanonicalResources (kCO kOR : ℝ) : ℝ :=
  kCO * kOR

/-- Canonical state exposing the exact three-cycle maintenance threshold. -/
noncomputable def jamCanonicalMaintenanceState
    (rO rR kCO kOR : ℝ) : JamCorrectiveState :=
  { corrective := jamCanonicalCorrective rO rR
    observability := jamCanonicalObservability kCO rR
    resources := jamCanonicalResources kCO kOR }

/-- Coordinatewise order above the canonical maintenance witness. -/
def jamAtOrAboveCanonical
    (rO rR kCO kOR : ℝ)
    (x : JamCorrectiveState) : Prop :=
  jamCanonicalCorrective rO rR ≤ x.corrective ∧
  jamCanonicalObservability kCO rR ≤ x.observability ∧
  jamCanonicalResources kCO kOR ≤ x.resources

/-- Exact canonical-state form of the slow replacement threshold. O and R are
exactly replaced at the witness; C is at least replaced iff the cycle-gain
product covers the product of autonomous deficits. -/
theorem jam_canonical_threshold_iff
    (rC rO rR kCO kOR kRC : ℝ) :
    let x := jamCanonicalMaintenanceState rO rR kCO kOR
    (x.corrective ≤
        (jamCorrectiveStateStep rC rO rR kCO kOR kRC x).corrective ∧
      x.observability =
        (jamCorrectiveStateStep rC rO rR kCO kOR kRC x).observability ∧
      x.resources =
        (jamCorrectiveStateStep rC rO rR kCO kOR kRC x).resources)
      ↔
    (1 - rC) * (1 - rO) * (1 - rR) ≤ kCO * kOR * kRC := by
  dsimp [jamCanonicalMaintenanceState, jamCanonicalCorrective,
    jamCanonicalObservability, jamCanonicalResources,
    jamCorrectiveStateStep]
  constructor
  · rintro ⟨hC, hO, hR⟩
    nlinarith
  · intro h
    constructor
    · nlinarith
    constructor <;> ring

/-- The cone above the canonical witness is forward invariant for nonnegative
retention/coupling coefficients when the closed maintenance loop meets the
replacement threshold. -/
theorem jam_step_preserves_canonical_lower_bound
    {rC rO rR kCO kOR kRC : ℝ}
    (hrC : 0 ≤ rC) (hrO : 0 ≤ rO) (hrR : 0 ≤ rR)
    (hkCO : 0 ≤ kCO) (hkOR : 0 ≤ kOR) (hkRC : 0 ≤ kRC)
    (hloop :
      (1 - rC) * (1 - rO) * (1 - rR) ≤ kCO * kOR * kRC)
    {x : JamCorrectiveState}
    (hx : jamAtOrAboveCanonical rO rR kCO kOR x) :
    jamAtOrAboveCanonical rO rR kCO kOR
      (jamCorrectiveStateStep rC rO rR kCO kOR kRC x) := by
  rcases hx with ⟨hxC, hxO, hxR⟩
  have hcanon :=
    (jam_canonical_threshold_iff rC rO rR kCO kOR kRC).2 hloop
  change
    jamCanonicalCorrective rO rR ≤
        rC * x.corrective + kRC * x.resources ∧
    jamCanonicalObservability kCO rR ≤
        rO * x.observability + kCO * x.corrective ∧
    jamCanonicalResources kCO kOR ≤
        rR * x.resources + kOR * x.observability
  constructor
  · have hCself := mul_le_mul_of_nonneg_left hxC hrC
    have hCreturn := mul_le_mul_of_nonneg_left hxR hkRC
    have hmono :
        rC * jamCanonicalCorrective rO rR +
            kRC * jamCanonicalResources kCO kOR
          ≤ rC * x.corrective + kRC * x.resources := by
      linarith
    exact le_trans hcanon.1 hmono
  constructor
  · have hOself := mul_le_mul_of_nonneg_left hxO hrO
    have hOcross := mul_le_mul_of_nonneg_left hxC hkCO
    have hmono :
        rO * jamCanonicalObservability kCO rR +
            kCO * jamCanonicalCorrective rO rR
          ≤ rO * x.observability + kCO * x.corrective := by
      linarith
    exact le_trans (le_of_eq hcanon.2.1) hmono
  · have hRself := mul_le_mul_of_nonneg_left hxR hrR
    have hRcross := mul_le_mul_of_nonneg_left hxO hkOR
    have hmono :
        rR * jamCanonicalResources kCO kOR +
            kOR * jamCanonicalObservability kCO rR
          ≤ rR * x.resources + kOR * x.observability := by
      linarith
    exact le_trans (le_of_eq hcanon.2.2) hmono

/-- Deterministic slow trajectory initialized at the canonical witness. -/
noncomputable def jamCanonicalMaintenanceTrajectory
    (rC rO rR kCO kOR kRC : ℝ) : ℕ → JamCorrectiveState
  | 0 => jamCanonicalMaintenanceState rO rR kCO kOR
  | n + 1 =>
      jamCorrectiveStateStep rC rO rR kCO kOR kRC
        (jamCanonicalMaintenanceTrajectory rC rO rR kCO kOR kRC n)

/-- Every point of the canonical trajectory remains at or above the canonical
witness when the slow loop meets replacement. -/
theorem jam_canonical_trajectory_stays_above_witness
    {rC rO rR kCO kOR kRC : ℝ}
    (hrC : 0 ≤ rC) (hrO : 0 ≤ rO) (hrR : 0 ≤ rR)
    (hkCO : 0 ≤ kCO) (hkOR : 0 ≤ kOR) (hkRC : 0 ≤ kRC)
    (hloop :
      (1 - rC) * (1 - rO) * (1 - rR) ≤ kCO * kOR * kRC) :
    ∀ n : ℕ,
      jamAtOrAboveCanonical rO rR kCO kOR
        (jamCanonicalMaintenanceTrajectory rC rO rR kCO kOR kRC n) := by
  intro n
  induction n with
  | zero =>
      exact ⟨le_rfl, le_rfl, le_rfl⟩
  | succ n ih =>
      change jamAtOrAboveCanonical rO rR kCO kOR
        (jamCorrectiveStateStep rC rO rR kCO kOR kRC
          (jamCanonicalMaintenanceTrajectory rC rO rR kCO kOR kRC n))
      exact jam_step_preserves_canonical_lower_bound
        hrC hrO hrR hkCO hkOR hkRC hloop ih

/-- **Persistent corrective-resilience theorem.** If the closed slow
maintenance loop meets replacement and the canonical corrective coordinate is
already sufficient for fast audit supercriticality, then every future point on
the canonical slow trajectory remains audit-supercritical.

This directly links the Result-4 maintenance threshold to the Result-5 fast
audit threshold without introducing the reduced multiplier `m`. -/
theorem jam_closed_maintenance_loop_preserves_supercritical_correction
    {F rC rO rR kCO kOR kRC : ℝ}
    (hF : 0 ≤ F)
    (hrC : 0 ≤ rC) (hrO : 0 ≤ rO) (hrR : 0 ≤ rR)
    (hkCO : 0 ≤ kCO) (hkOR : 0 ≤ kOR) (hkRC : 0 ≤ kRC)
    (hloop :
      (1 - rC) * (1 - rO) * (1 - rR) ≤ kCO * kOR * kRC)
    (hfast : 1 < F * jamCanonicalCorrective rO rR) :
    ∀ n : ℕ,
      jamStateCorrectionSupercritical F
        (jamCanonicalMaintenanceTrajectory rC rO rR kCO kOR kRC n) := by
  intro n
  have habove := jam_canonical_trajectory_stays_above_witness
    hrC hrO hrR hkCO hkOR hkRC hloop n
  have hC :
      jamCanonicalCorrective rO rR ≤
        (jamCanonicalMaintenanceTrajectory rC rO rR kCO kOR kRC n).corrective :=
    habove.1
  have hmul :
      F * jamCanonicalCorrective rO rR ≤
        F * (jamCanonicalMaintenanceTrajectory rC rO rR kCO kOR kRC n).corrective :=
    mul_le_mul_of_nonneg_left hC hF
  unfold jamStateCorrectionSupercritical jamStateCorrectionReproduction
  exact lt_of_lt_of_le hfast hmul

/-- Under positive O and R deficits and positive C->O and O->R gains, the
canonical corrective coordinate is strictly positive. -/
theorem jam_canonical_corrective_positive
    {rO rR : ℝ}
    (hdO : 0 < 1 - rO)
    (hdR : 0 < 1 - rR) :
    0 < jamCanonicalCorrective rO rR := by
  unfold jamCanonicalCorrective
  exact mul_pos hdO hdR

/-- Deleting the immediate R->C return edge makes any positive corrective
coordinate with subunit autonomous retention strictly decline on the next
cross-audit update. -/
theorem jam_deleting_return_edge_makes_corrective_capacity_decline
    {rC rO rR kCO kOR : ℝ}
    {x : JamCorrectiveState}
    (hrC : rC < 1)
    (hxC : 0 < x.corrective) :
    (jamCorrectiveStateStep rC rO rR kCO kOR 0 x).corrective < x.corrective := by
  simp [jamCorrectiveStateStep]
  nlinarith

#print axioms jam_canonical_threshold_iff
#print axioms jam_step_preserves_canonical_lower_bound
#print axioms jam_canonical_trajectory_stays_above_witness
#print axioms jam_closed_maintenance_loop_preserves_supercritical_correction
#print axioms jam_canonical_corrective_positive
#print axioms jam_deleting_return_edge_makes_corrective_capacity_decline

end DistributedCommons
