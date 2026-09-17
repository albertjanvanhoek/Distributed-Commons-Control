import JamRecurrentMaintenance

namespace DistributedCommons

/-!
# JAM recurrent maintenance dynamics

This module lifts the static separation between within-audit corrective
reproduction and cross-audit maintenance viability into a time-indexed state
model.

The slow state is intentionally abstract:

* `corrective` = independently corrective capacity available to auditing;
* `observable` = capacity to observe or attribute genuine maintenance;
* `resources` = resources returned to sustain future corrective capacity.

The update is the directed cycle

  C -> O -> R -> C

with autonomous retention on each component. The model is not claimed to be a
literal Gray Paper state machine. Its purpose is to ask whether two systems
that are equally corrective now can have different future corrective capacity
because their maintenance return loops differ.
-/

structure JamMaintenanceState where
  corrective : ℝ
  observable : ℝ
  resources : ℝ
  deriving Repr

/-- One slow-timescale maintenance update. -/
noncomputable def jamMaintenanceStep
    (rC rO rR kCO kOR kRC : ℝ)
    (s : JamMaintenanceState) : JamMaintenanceState :=
  { corrective := rC * s.corrective + kRC * s.resources
    observable := rO * s.observable + kCO * s.corrective
    resources := rR * s.resources + kOR * s.observable }

/-- Time-indexed slow maintenance trajectory. -/
noncomputable def jamMaintenancePath
    (rC rO rR kCO kOR kRC : ℝ)
    (s0 : JamMaintenanceState) : ℕ → JamMaintenanceState
  | 0 => s0
  | n + 1 => jamMaintenanceStep rC rO rR kCO kOR kRC
      (jamMaintenancePath rC rO rR kCO kOR kRC s0 n)

/-- ELVES-style audit reproduction when current independent corrective
capacity is represented as an effective count C out of population N. -/
noncomputable def jamAuditReproductionFromCapacity
    (F N C : ℝ) : ℝ :=
  F * C / N

/-- A state is audit-supercritical for `(F,N)` when its currently available
independent corrective capacity gives reproduction greater than one. -/
def jamStateCorrectionSupercritical
    (F N : ℝ) (s : JamMaintenanceState) : Prop :=
  1 < jamAuditReproductionFromCapacity F N s.corrective

@[simp] theorem jamMaintenancePath_zero
    (rC rO rR kCO kOR kRC : ℝ) (s0 : JamMaintenanceState) :
    jamMaintenancePath rC rO rR kCO kOR kRC s0 0 = s0 := by
  rfl

@[simp] theorem jamMaintenancePath_succ
    (rC rO rR kCO kOR kRC : ℝ)
    (s0 : JamMaintenanceState) (n : ℕ) :
    jamMaintenancePath rC rO rR kCO kOR kRC s0 (n + 1) =
      jamMaintenanceStep rC rO rR kCO kOR kRC
        (jamMaintenancePath rC rO rR kCO kOR kRC s0 n) := by
  rfl

/-- In the absence of a resource-return edge, next-period corrective capacity
is just autonomous retention of current corrective capacity. -/
theorem corrective_step_without_return
    (rC rO rR kCO kOR : ℝ) (s : JamMaintenanceState) :
    (jamMaintenanceStep rC rO rR kCO kOR 0 s).corrective =
      rC * s.corrective := by
  simp [jamMaintenanceStep]

/-- Dynamic erosion witness.

Both the initial effective population and escalation factor are normalized to
one and two respectively. The state begins with C=1, hence lambda_0=2. With
50% autonomous retention and no R->C return edge, C falls to 1/4 by t=2 and
lambda_2=1/2. Thus an audit-supercritical system can become subcritical without
any change in F or N. -/
theorem initially_supercritical_later_subcritical_witness :
    let s0 : JamMaintenanceState :=
      { corrective := 1, observable := 0, resources := 0 }
    jamStateCorrectionSupercritical 2 1 s0 ∧
    ¬ jamStateCorrectionSupercritical 2 1
      (jamMaintenancePath (1 / 2) 0 0 1 1 0 s0 2) := by
  dsimp
  constructor
  · norm_num [jamStateCorrectionSupercritical,
      jamAuditReproductionFromCapacity]
  · norm_num [jamStateCorrectionSupercritical,
      jamAuditReproductionFromCapacity, jamMaintenancePath,
      jamMaintenanceStep]

/-- A closed unit return loop has the all-ones maintenance state as a fixed
point. -/
theorem unit_return_loop_fixed_point :
    jamMaintenanceStep 0 0 0 1 1 1
      { corrective := 1, observable := 1, resources := 1 } =
    ({ corrective := 1, observable := 1, resources := 1 } : JamMaintenanceState) := by
  norm_num [jamMaintenanceStep]

/-- Therefore the unit return loop preserves the all-ones state for every slow
time step. -/
theorem unit_return_loop_path_constant (n : ℕ) :
    jamMaintenancePath 0 0 0 1 1 1
      { corrective := 1, observable := 1, resources := 1 } n =
    ({ corrective := 1, observable := 1, resources := 1 } : JamMaintenanceState) := by
  induction n with
  | zero => rfl
  | succ n ih =>
      rw [jamMaintenancePath_succ, ih]
      exact unit_return_loop_fixed_point

/-- A viable return loop can preserve audit-supercritical corrective capacity
at every time step for this witness. -/
theorem recurrent_maintenance_can_preserve_supercriticality (n : ℕ) :
    jamStateCorrectionSupercritical 2 1
      (jamMaintenancePath 0 0 0 1 1 1
        { corrective := 1, observable := 1, resources := 1 } n) := by
  rw [unit_return_loop_path_constant]
  norm_num [jamStateCorrectionSupercritical, jamAuditReproductionFromCapacity]

/-- Matched-initial-state counterexample.

The two systems have exactly the same initial corrective capacity and therefore
the same initial audit reproduction. Their future audit reproduction differs
because one has no return edge into corrective capacity while the other closes
the maintenance cycle. Current lambda is therefore not a sufficient state
variable for future corrective resilience in the declared model. -/
theorem same_current_correction_different_future_resilience :
    let decaying0 : JamMaintenanceState :=
      { corrective := 1, observable := 0, resources := 0 }
    let maintained0 : JamMaintenanceState :=
      { corrective := 1, observable := 1, resources := 1 }
    jamAuditReproductionFromCapacity 2 1 decaying0.corrective =
      jamAuditReproductionFromCapacity 2 1 maintained0.corrective ∧
    jamStateCorrectionSupercritical 2 1 decaying0 ∧
    jamStateCorrectionSupercritical 2 1 maintained0 ∧
    ¬ jamStateCorrectionSupercritical 2 1
      (jamMaintenancePath (1 / 2) 0 0 1 1 0 decaying0 2) ∧
    jamStateCorrectionSupercritical 2 1
      (jamMaintenancePath 0 0 0 1 1 1 maintained0 2) := by
  dsimp
  constructor
  · norm_num [jamAuditReproductionFromCapacity]
  constructor
  · norm_num [jamStateCorrectionSupercritical,
      jamAuditReproductionFromCapacity]
  constructor
  · norm_num [jamStateCorrectionSupercritical,
      jamAuditReproductionFromCapacity]
  constructor
  · norm_num [jamStateCorrectionSupercritical,
      jamAuditReproductionFromCapacity, jamMaintenancePath,
      jamMaintenanceStep]
  · exact recurrent_maintenance_can_preserve_supercriticality 2

#print axioms initially_supercritical_later_subcritical_witness
#print axioms unit_return_loop_fixed_point
#print axioms unit_return_loop_path_constant
#print axioms recurrent_maintenance_can_preserve_supercriticality
#print axioms same_current_correction_different_future_resilience

end DistributedCommons
