import JamEffortObservability
import JamMaintenance

namespace DistributedCommons

/-!
# JAM recurrent maintenance across audits

The existing JAM/ELVES formalization contains fast-timescale quantities for
one audit/dispute process: corrective reproduction, no-show reproduction, and
selection of costly checking.  This file adds a deliberately separate slow
maintenance layer.

We track three abstract capacities:

* `correction`: independently corrective capacity available for future audits;
* `observability`: capacity to distinguish genuine maintenance from imitation;
* `resources`: resources returned to sustain future corrective capacity.

The canonical directed return loop is

    correction -> observability -> resources -> correction.

This is not claimed to be a complete model of JAM staking or operations.  The
couplings are interface parameters for the higher layers that the audited JAM
assurance mechanism delegates.  The algebra is a three-process positive-system
replacement calculation.  Its purpose here is to distinguish event-level
corrective reproduction from cross-time reproduction of corrective capacity.
-/

/-- Autonomous one-step maintenance deficit of a slow capacity. -/
noncomputable def jamMaintenanceDeficit (r : ℝ) : ℝ :=
  1 - r

/-- Slow state of the recurrent-maintenance interface. -/
structure JamRecurrentState where
  correction : ℝ
  observability : ℝ
  resources : ℝ

/-- One slow maintenance update.

`kCO` maps corrective activity into maintenance observability,
`kOR` maps observability into returned resources, and
`kRC` maps returned resources into future corrective capacity. -/
noncomputable def jamRecurrentStep
    (rC rO rR kCO kOR kRC : ℝ)
    (x : JamRecurrentState) : JamRecurrentState :=
  { correction := rC * x.correction + kRC * x.resources
    observability := rO * x.observability + kCO * x.correction
    resources := rR * x.resources + kOR * x.observability }

/-- Canonical positive-loop witness used for the exact replacement boundary. -/
noncomputable def jamRecurrentCanonical
    (rO rR kCO kOR : ℝ) : JamRecurrentState :=
  { correction := jamMaintenanceDeficit rO * jamMaintenanceDeficit rR
    observability := kCO * jamMaintenanceDeficit rR
    resources := kCO * kOR }

/-- Strict slow-timescale maintenance reproduction condition. -/
def jamMaintenanceSupercritical
    (rC rO rR kCO kOR kRC : ℝ) : Prop :=
  jamMaintenanceDeficit rC *
      jamMaintenanceDeficit rO *
      jamMaintenanceDeficit rR
    < kCO * kOR * kRC

/-- Fast event-level corrective reproduction condition from the JAM/ELVES
shared-fault extension. -/
def jamEventCorrectionSupercritical
    (n H B F : ℝ) : Prop :=
  1 < jamCorrectionReproduction n H B F

/-- The canonical correction coordinate reaches replacement exactly when the
closed-loop gain covers the product of autonomous maintenance deficits. -/
theorem jam_recurrent_canonical_correction_replacement_iff
    (rC rO rR kCO kOR kRC : ℝ) :
    (jamRecurrentCanonical rO rR kCO kOR).correction ≤
      (jamRecurrentStep rC rO rR kCO kOR kRC
        (jamRecurrentCanonical rO rR kCO kOR)).correction
      ↔
    jamMaintenanceDeficit rC *
        jamMaintenanceDeficit rO *
        jamMaintenanceDeficit rR
      ≤ kCO * kOR * kRC := by
  simp [jamRecurrentCanonical, jamRecurrentStep, jamMaintenanceDeficit]
  constructor <;> intro h <;> nlinarith

/-- At the canonical witness the observability coordinate is exactly at
replacement, independently of the return edge into correction. -/
theorem jam_recurrent_canonical_observability_replacement
    (rO rR kCO kOR : ℝ) :
    (jamRecurrentStep 0 rO rR kCO kOR 0
      (jamRecurrentCanonical rO rR kCO kOR)).observability =
      (jamRecurrentCanonical rO rR kCO kOR).observability := by
  simp [jamRecurrentCanonical, jamRecurrentStep, jamMaintenanceDeficit]
  ring

/-- At the canonical witness the resource coordinate is exactly at
replacement. -/
theorem jam_recurrent_canonical_resources_replacement
    (rO rR kCO kOR : ℝ) :
    (jamRecurrentStep 0 rO rR kCO kOR 0
      (jamRecurrentCanonical rO rR kCO kOR)).resources =
      (jamRecurrentCanonical rO rR kCO kOR).resources := by
  simp [jamRecurrentCanonical, jamRecurrentStep, jamMaintenanceDeficit]
  ring

/-- Coordinatewise order above the canonical recurrent-maintenance witness. -/
def jamAtOrAboveCanonical
    (rO rR kCO kOR : ℝ)
    (x : JamRecurrentState) : Prop :=
  (jamRecurrentCanonical rO rR kCO kOR).correction ≤ x.correction ∧
  (jamRecurrentCanonical rO rR kCO kOR).observability ≤ x.observability ∧
  (jamRecurrentCanonical rO rR kCO kOR).resources ≤ x.resources

/-- Once the product replacement threshold is met, the cone above the
canonical witness is forward invariant for nonnegative retention and coupling
coefficients. -/
theorem jam_recurrent_step_preserves_canonical_lower_bound
    {rC rO rR kCO kOR kRC : ℝ}
    (hrC : 0 ≤ rC) (hrO : 0 ≤ rO) (hrR : 0 ≤ rR)
    (hkCO : 0 ≤ kCO) (hkOR : 0 ≤ kOR) (hkRC : 0 ≤ kRC)
    (hloop :
      jamMaintenanceDeficit rC *
          jamMaintenanceDeficit rO *
          jamMaintenanceDeficit rR
        ≤ kCO * kOR * kRC)
    {x : JamRecurrentState}
    (hx : jamAtOrAboveCanonical rO rR kCO kOR x) :
    jamAtOrAboveCanonical rO rR kCO kOR
      (jamRecurrentStep rC rO rR kCO kOR kRC x) := by
  rcases hx with ⟨hxC, hxO, hxR⟩
  have hcanonC :=
    (jam_recurrent_canonical_correction_replacement_iff
      rC rO rR kCO kOR kRC).2 hloop
  have hcanonO := jam_recurrent_canonical_observability_replacement
    rO rR kCO kOR
  have hcanonR := jam_recurrent_canonical_resources_replacement
    rO rR kCO kOR
  constructor
  · have hself := mul_le_mul_of_nonneg_left hxC hrC
    have hreturn := mul_le_mul_of_nonneg_left hxR hkRC
    have hmono :
        (jamRecurrentStep rC rO rR kCO kOR kRC
          (jamRecurrentCanonical rO rR kCO kOR)).correction ≤
        (jamRecurrentStep rC rO rR kCO kOR kRC x).correction := by
      simp [jamRecurrentStep, jamRecurrentCanonical] at hself hreturn ⊢
      linarith
    exact le_trans hcanonC hmono
  constructor
  · have hself := mul_le_mul_of_nonneg_left hxO hrO
    have hsignal := mul_le_mul_of_nonneg_left hxC hkCO
    have hmono :
        (jamRecurrentStep rC rO rR kCO kOR kRC
          (jamRecurrentCanonical rO rR kCO kOR)).observability ≤
        (jamRecurrentStep rC rO rR kCO kOR kRC x).observability := by
      simp [jamRecurrentStep, jamRecurrentCanonical] at hself hsignal ⊢
      linarith
    have hcanonO' :
        (jamRecurrentCanonical rO rR kCO kOR).observability =
        (jamRecurrentStep rC rO rR kCO kOR kRC
          (jamRecurrentCanonical rO rR kCO kOR)).observability := by
      simp [jamRecurrentCanonical, jamRecurrentStep, jamMaintenanceDeficit]
      ring
    exact hcanonO'.trans_le hmono
  · have hself := mul_le_mul_of_nonneg_left hxR hrR
    have hsignal := mul_le_mul_of_nonneg_left hxO hkOR
    have hmono :
        (jamRecurrentStep rC rO rR kCO kOR kRC
          (jamRecurrentCanonical rO rR kCO kOR)).resources ≤
        (jamRecurrentStep rC rO rR kCO kOR kRC x).resources := by
      simp [jamRecurrentStep, jamRecurrentCanonical] at hself hsignal ⊢
      linarith
    have hcanonR' :
        (jamRecurrentCanonical rO rR kCO kOR).resources =
        (jamRecurrentStep rC rO rR kCO kOR kRC
          (jamRecurrentCanonical rO rR kCO kOR)).resources := by
      simp [jamRecurrentCanonical, jamRecurrentStep, jamMaintenanceDeficit]
      ring
    exact hcanonR'.trans_le hmono

/-- Deterministic slow trajectory started at the canonical witness. -/
noncomputable def jamRecurrentTrajectory
    (rC rO rR kCO kOR kRC : ℝ) : ℕ → JamRecurrentState
  | 0 => jamRecurrentCanonical rO rR kCO kOR
  | n + 1 =>
      jamRecurrentStep rC rO rR kCO kOR kRC
        (jamRecurrentTrajectory rC rO rR kCO kOR kRC n)

/-- The canonical slow trajectory never falls below the canonical witness once
replacement is closed. -/
theorem jam_recurrent_trajectory_stays_above_canonical
    {rC rO rR kCO kOR kRC : ℝ}
    (hrC : 0 ≤ rC) (hrO : 0 ≤ rO) (hrR : 0 ≤ rR)
    (hkCO : 0 ≤ kCO) (hkOR : 0 ≤ kOR) (hkRC : 0 ≤ kRC)
    (hloop :
      jamMaintenanceDeficit rC *
          jamMaintenanceDeficit rO *
          jamMaintenanceDeficit rR
        ≤ kCO * kOR * kRC) :
    ∀ n : ℕ,
      jamAtOrAboveCanonical rO rR kCO kOR
        (jamRecurrentTrajectory rC rO rR kCO kOR kRC n) := by
  intro n
  induction n with
  | zero =>
      exact ⟨le_rfl, le_rfl, le_rfl⟩
  | succ n ih =>
      exact jam_recurrent_step_preserves_canonical_lower_bound
        hrC hrO hrR hkCO hkOR hkRC hloop ih

/-- Positivity of the canonical slow witness under positive deficits and the
two forward couplings. -/
theorem jam_recurrent_canonical_positive
    {rO rR kCO kOR : ℝ}
    (hdO : 0 < jamMaintenanceDeficit rO)
    (hdR : 0 < jamMaintenanceDeficit rR)
    (hkCO : 0 < kCO) (hkOR : 0 < kOR) :
    0 < (jamRecurrentCanonical rO rR kCO kOR).correction ∧
    0 < (jamRecurrentCanonical rO rR kCO kOR).observability ∧
    0 < (jamRecurrentCanonical rO rR kCO kOR).resources := by
  simp [jamRecurrentCanonical]
  constructor
  · positivity
  constructor <;> positivity

/-- Under a strict closed maintenance loop and positive/nonnegative
coefficients, all three slow capacities remain positive at every time. -/
theorem jam_strict_maintenance_loop_positive_for_all_time
    {rC rO rR kCO kOR kRC : ℝ}
    (hrC : 0 ≤ rC) (hrO : 0 ≤ rO) (hrR : 0 ≤ rR)
    (hdC : 0 < jamMaintenanceDeficit rC)
    (hdO : 0 < jamMaintenanceDeficit rO)
    (hdR : 0 < jamMaintenanceDeficit rR)
    (hkCO : 0 < kCO) (hkOR : 0 < kOR) (hkRC : 0 < kRC)
    (hloop : jamMaintenanceSupercritical rC rO rR kCO kOR kRC) :
    ∀ n : ℕ,
      0 < (jamRecurrentTrajectory rC rO rR kCO kOR kRC n).correction ∧
      0 < (jamRecurrentTrajectory rC rO rR kCO kOR kRC n).observability ∧
      0 < (jamRecurrentTrajectory rC rO rR kCO kOR kRC n).resources := by
  intro n
  have habove := jam_recurrent_trajectory_stays_above_canonical
    hrC hrO hrR (le_of_lt hkCO) (le_of_lt hkOR) (le_of_lt hkRC)
    (le_of_lt hloop) n
  have hpositive := jam_recurrent_canonical_positive hdO hdR hkCO hkOR
  rcases habove with ⟨hC, hO, hR⟩
  rcases hpositive with ⟨hpC, hpO, hpR⟩
  exact ⟨lt_of_lt_of_le hpC hC, lt_of_lt_of_le hpO hO,
    lt_of_lt_of_le hpR hR⟩

/-- Event-level correction can be supercritical even while the slow
maintenance return loop is subcritical. -/
theorem event_correction_does_not_imply_recurrent_maintenance :
    jamEventCorrectionSupercritical 1 1 0 2 ∧
    ¬ jamMaintenanceSupercritical 0 0 0 0 0 0 := by
  norm_num [jamEventCorrectionSupercritical, jamCorrectionReproduction,
    jamMaintenanceSupercritical, jamMaintenanceDeficit]

/-- Conversely, the slow maintenance loop can be supercritical while a
particular fault-specific audit is subcritical. -/
theorem recurrent_maintenance_does_not_imply_event_correction :
    jamMaintenanceSupercritical
        (1 / 2 : ℝ) (1 / 2 : ℝ) (1 / 2 : ℝ) 1 1 1 ∧
    ¬ jamEventCorrectionSupercritical 2 1 0 1 := by
  norm_num [jamEventCorrectionSupercritical, jamCorrectionReproduction,
    jamMaintenanceSupercritical, jamMaintenanceDeficit]

/-- Even a locally selected compute action and supercritical current correction
do not by themselves close the slow return loop.  This witness separates the
existing short-run JAM conditions from cross-time maintenance reproduction. -/
theorem local_audit_viability_does_not_imply_slow_maintenance :
    jamEventCorrectionSupercritical 1 1 0 2 ∧
    0 ≤ maintenanceSelectionMargin 1 2 1 0 0 0 ∧
    ¬ jamMaintenanceSupercritical 0 0 0 0 0 0 := by
  norm_num [jamEventCorrectionSupercritical, jamCorrectionReproduction,
    maintenanceSelectionMargin, jamMaintenanceSupercritical,
    jamMaintenanceDeficit]

/-- The four cells of the two-timescale phase diagram are all non-vacuous. -/
theorem jam_two_timescale_phase_cells_inhabited :
    (jamEventCorrectionSupercritical 1 1 0 2 ∧
      jamMaintenanceSupercritical
        (1 / 2 : ℝ) (1 / 2 : ℝ) (1 / 2 : ℝ) 1 1 1) ∧
    (jamEventCorrectionSupercritical 1 1 0 2 ∧
      ¬ jamMaintenanceSupercritical 0 0 0 0 0 0) ∧
    (¬ jamEventCorrectionSupercritical 2 1 0 1 ∧
      jamMaintenanceSupercritical
        (1 / 2 : ℝ) (1 / 2 : ℝ) (1 / 2 : ℝ) 1 1 1) ∧
    (¬ jamEventCorrectionSupercritical 2 1 0 1 ∧
      ¬ jamMaintenanceSupercritical 0 0 0 0 0 0) := by
  norm_num [jamEventCorrectionSupercritical, jamCorrectionReproduction,
    jamMaintenanceSupercritical, jamMaintenanceDeficit]

#print axioms jam_recurrent_canonical_correction_replacement_iff
#print axioms jam_recurrent_canonical_observability_replacement
#print axioms jam_recurrent_canonical_resources_replacement
#print axioms jam_recurrent_step_preserves_canonical_lower_bound
#print axioms jam_recurrent_trajectory_stays_above_canonical
#print axioms jam_recurrent_canonical_positive
#print axioms jam_strict_maintenance_loop_positive_for_all_time
#print axioms event_correction_does_not_imply_recurrent_maintenance
#print axioms recurrent_maintenance_does_not_imply_event_correction
#print axioms local_audit_viability_does_not_imply_slow_maintenance
#print axioms jam_two_timescale_phase_cells_inhabited

end DistributedCommons
