import JamEffortObservability

namespace DistributedCommons

/-!
# JAM: corrective reproduction versus recurrent maintenance

This module separates two timescales that are easy to conflate.

* `jamFaultCorrectionReproduction` is the within-audit reproduction mean of
  independently correct checking under the correlated-honest-failure
  extension of ELVES.
* `jamMaintenanceLoopGain` and `jamMaintenanceDeficitProduct` describe a
  slower three-process return loop that maintains the capacity to keep doing
  useful correction across audits.

The three slow processes are intentionally abstract:

  C = independently corrective capacity
  O = capacity to observe/attribute genuine maintenance
  R = resources returned to maintain future corrective capacity

with the canonical directed loop

  C -> O -> R -> C.

The product threshold used here is the finite three-cycle replacement
condition. The underlying nonnegative-matrix / reproduction-number mathematics
is classical; the contribution of this module is the explicit separation from
the ELVES event-level correction threshold and the machine-checked independence
witnesses below.
-/

/-- Fault-specific within-audit corrective reproduction. -/
noncomputable def jamFaultCorrectionReproduction
    (F gamma f : ℝ) : ℝ :=
  F * (1 - gamma) * (1 - f)

/-- Autonomous maintenance deficit of one slow maintenance process. -/
noncomputable def jamMaintenanceDeficit (r : ℝ) : ℝ :=
  1 - r

/-- Product of the three autonomous maintenance deficits. -/
noncomputable def jamMaintenanceDeficitProduct
    (rC rO rR : ℝ) : ℝ :=
  jamMaintenanceDeficit rC *
  jamMaintenanceDeficit rO *
  jamMaintenanceDeficit rR

/-- Closed-loop gain of the C -> O -> R -> C maintenance cycle. -/
noncomputable def jamMaintenanceLoopGain
    (kCO kOR kRC : ℝ) : ℝ :=
  kCO * kOR * kRC

/-- The canonical slow maintenance loop meets replacement when its closed-loop
product covers the product of its autonomous deficits. -/
def jamMaintenanceViable
    (rC rO rR kCO kOR kRC : ℝ) : Prop :=
  jamMaintenanceDeficitProduct rC rO rR ≤
    jamMaintenanceLoopGain kCO kOR kRC

/-- Event-level correction is supercritical exactly when its reproduction mean
exceeds one. This is kept as a named predicate so the two timescales can be
combined without identifying them. -/
def jamCorrectionSupercritical (F gamma f : ℝ) : Prop :=
  1 < jamFaultCorrectionReproduction F gamma f

/-- Exact substitution of the independently-correct share into the ELVES-style
fault-specific reproduction mean. -/
theorem jamFaultCorrectionReproduction_eq
    (F gamma f : ℝ) :
    jamFaultCorrectionReproduction F gamma f =
      F * (1 - gamma) * (1 - f) := by
  rfl

/-- The slow maintenance threshold depends only on the maintenance-loop
parameters, not on the current ELVES fault-specific reproduction parameters. -/
theorem jamMaintenanceViable_iff
    (rC rO rR kCO kOR kRC : ℝ) :
    jamMaintenanceViable rC rO rR kCO kOR kRC ↔
      (1 - rC) * (1 - rO) * (1 - rR) ≤ kCO * kOR * kRC := by
  rfl

/-- Separation witness 1: current correction can be strongly supercritical
while the slow maintenance return loop is subcritical.

Here the audit reproduction mean is 2, but three zero-retention maintenance
processes coupled by gains 1/2 have loop gain 1/8 against deficit product 1. -/
theorem correction_supercritical_maintenance_subcritical_witness :
    jamCorrectionSupercritical 2 0 0 ∧
    ¬ jamMaintenanceViable 0 0 0 (1 / 2) (1 / 2) (1 / 2) := by
  constructor
  · norm_num [jamCorrectionSupercritical, jamFaultCorrectionReproduction]
  · norm_num [jamMaintenanceViable, jamMaintenanceDeficitProduct,
      jamMaintenanceDeficit, jamMaintenanceLoopGain]

/-- Separation witness 2: a strongly viable slow maintenance loop does not
imply fault-specific correction is supercritical for the current audit.

Here the slow loop has unit gain against deficit product 1/8, while a fault
shared by 3/4 of otherwise-honest validators leaves the event-level correction
mean at 1/2 for F=2. -/
theorem maintenance_viable_correction_subcritical_witness :
    jamMaintenanceViable (1 / 2) (1 / 2) (1 / 2) 1 1 1 ∧
    ¬ jamCorrectionSupercritical 2 0 (3 / 4) := by
  constructor
  · norm_num [jamMaintenanceViable, jamMaintenanceDeficitProduct,
      jamMaintenanceDeficit, jamMaintenanceLoopGain]
  · norm_num [jamCorrectionSupercritical, jamFaultCorrectionReproduction]

/-- Therefore within-audit corrective reproduction does not logically imply
cross-audit maintenance viability in this declared two-timescale model. -/
theorem correction_supercritical_does_not_imply_maintenance_viable :
    ¬ (∀ F gamma f rC rO rR kCO kOR kRC : ℝ,
      jamCorrectionSupercritical F gamma f →
      jamMaintenanceViable rC rO rR kCO kOR kRC) := by
  intro h
  have hbad := h 2 0 0 0 0 0 (1 / 2) (1 / 2) (1 / 2)
    correction_supercritical_maintenance_subcritical_witness.1
  exact correction_supercritical_maintenance_subcritical_witness.2 hbad

/-- Conversely, a viable slow maintenance loop does not logically imply that
independent correction for a particular current fault is supercritical. -/
theorem maintenance_viable_does_not_imply_correction_supercritical :
    ¬ (∀ F gamma f rC rO rR kCO kOR kRC : ℝ,
      jamMaintenanceViable rC rO rR kCO kOR kRC →
      jamCorrectionSupercritical F gamma f) := by
  intro h
  have hbad := h 2 0 (3 / 4) (1 / 2) (1 / 2) (1 / 2) 1 1 1
    maintenance_viable_correction_subcritical_witness.1
  exact maintenance_viable_correction_subcritical_witness.2 hbad

/-- The two predicates therefore generate four logically distinct phase cells;
this witness inhabits the jointly viable cell. -/
theorem both_reproduction_conditions_can_hold :
    jamCorrectionSupercritical 2 0 0 ∧
    jamMaintenanceViable (1 / 2) (1 / 2) (1 / 2) 1 1 1 := by
  constructor
  · exact correction_supercritical_maintenance_subcritical_witness.1
  · exact maintenance_viable_correction_subcritical_witness.1

/-- This witness inhabits the jointly non-viable cell. -/
theorem neither_reproduction_condition_need_hold :
    ¬ jamCorrectionSupercritical 2 0 (3 / 4) ∧
    ¬ jamMaintenanceViable 0 0 0 (1 / 2) (1 / 2) (1 / 2) := by
  exact ⟨maintenance_viable_correction_subcritical_witness.2,
    correction_supercritical_maintenance_subcritical_witness.2⟩

#print axioms correction_supercritical_maintenance_subcritical_witness
#print axioms maintenance_viable_correction_subcritical_witness
#print axioms correction_supercritical_does_not_imply_maintenance_viable
#print axioms maintenance_viable_does_not_imply_correction_supercritical
#print axioms both_reproduction_conditions_can_hold
#print axioms neither_reproduction_condition_need_hold

end DistributedCommons
