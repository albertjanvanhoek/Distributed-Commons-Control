# Lean formalization

The Lean source checks only the algebraic core of the declared model. It does not validate the empirical suitability of the common-mode mixture or any mapping to JAM or ecology.

| Result | Lean declaration |
|---|---|
| Arbitrary-\(n\) independent-failure specialization | `escapeN_independent` |
| Perfect effort leaves common-mode escape for every \(n>0\) | `escapeN_perfect` |
| Harmful finalization at perfect effort is \(b\rho\) | `badFinalizationN_perfect` |
| Arbitrary-\(n\) common-mode lower bound | `escapeN_correlation_floor`; `badFinalizationN_correlation_floor` |
| Target below the floor is impossible for arbitrary \(n\) | `safety_impossible_below_correlation_floor_N` |
| Root substitution reaches the exact safety boundary | `sufficientEffort_hits_target_from_root` |
| Quadratic private optimum | `monitorObjective_gap`; `selectedEffort_global_max` |
| Selected-versus-required boundary | `selectedEffort_meets_requirement_iff`; `selectedEffort_underprovides` |
| Probability clipping preserves the sufficiency test | `feasibleSelectedEffort_meets_iff` |
| Exact critical-cost phase boundary | `feasibleSelectedEffort_meets_iff_cost_le_critical` |
| Common-mode cap on collective detection | `detectionN_le_commonModeCap` |
| Producer-response floor under an antitone response | `response_floor_of_commonModeCap` |
| Finite-time producer lower envelope under partial adjustment | `producerPath_lowerEnvelope` |
| Closed-loop multiplier identity | `commonsMultiplier_eq_one_sub_gamma_add_gain` |
| Loop-gain nonnegativity under protective response | `commonsLoopGain_nonneg` |
| Loop-gain nonpositivity when failure rises with commons health | `commonsLoopGain_nonpos` |
| Critical-slowing recovery identity \(1-M=\gamma(1-\eta)\) | `one_sub_commonsMultiplier_eq_recovery_gap` |
| Local multiplier threshold iff loop gain < 1 | `abs_commonsMultiplier_lt_one_iff_loopGain_lt_one` |
| Fold-neutral multiplier at loop gain = 1 | `commonsMultiplier_eq_one_of_loopGain_eq_one` |
| Independent failure profile lowers escape from rho to rho^2 | `independent_profile_lowers_escape` |
| Independent failure profile raises uncapped viability margin | `independent_profile_increases_margin` |
| Exact viability-margin gain from independent profile | `independent_profile_margin_gain` |
| Margin ratio is 1/rho in the uncapped regime | `independent_profile_margin_ratio` |
| Shared-reward two-participant fixed point | `twoSelectedEffort_fixedPoint` |
| Positive frozen/direct participant contribution | `direct_addition_positive` |
| Exact selected-contribution identity | `selected_addition_identity` |
| Direct-positive selected-negative reversal | `selected_addition_negative` |
| Shock viable iff below (M(X,C)) | `shock_viable_iff_below_margin` |
| Margin difference from capacity difference | `capacity_margin_difference` |
| Higher capacity raises finite-shock margin | `higher_capacity_higher_margin` |
| Full shared state fixed during quiet period | `quietSharedStep_full` |
| Quiet capacity decay lowers shock margin | `quiet_capacity_erodes_margin_at_full_state` |
| Access-mediated participant contribution identity | `access_contribution_identity` |
| Positive contribution from lower all-disabled probability | `access_contribution_positive` |
| Independent-profile contribution \(\kappa C\rho(1-\rho)\) | `independent_profile_capacity_contribution` |
| Zero reserve means zero access contribution | `zero_capacity_zero_access_contribution` |
| Quiet capacity decay scales contribution | `quiet_decay_scales_access_contribution` |
| Positive scalarization witness for mixed-sign vector | `positive_scalarization_witness` |
| Negative scalarization witness for same vector | `negative_scalarization_witness` |
| Replacement closure iff viability boundary preserved | `boundary_preserved_iff_replacement_closed` |
| Passive renewal can eliminate active-maintenance necessity | `passive_renewal_can_suffice` |
| Active maintenance must close passive replacement gap | `participant_maintenance_must_close_gap` |
| Excess correction produces multiplier below -1 | `overcorrection_multiplier_lt_neg_one` |
| Low-fidelity signal reverses correction | `low_fidelity_reverses_correction` |
| Reinforcement can be net harmful | `reinforcement_can_be_harmful` |
| Conditional repair inequality | `repair_nonnegative_iff` |
| One-validator client-diversification gain \(s_\delta/n\) | `one_validator_diversification_gain` |
| One-validator reliability gain \(s_\delta/n\) | `one_validator_reliability_gain` |
| Escalation raises correction reproduction | `escalation_improves_correction` |
| Escalation lowers scalability margin | `escalation_harms_scalability` |
| Compute dominates rubber iff incentive gap closes | `compute_dominates_rubber_iff` |
| Compute dominates no-show iff reward gap covers cost | `compute_dominates_noshow_iff` |
| Lower exposure raises required compute reward advantage | `lower_exposure_raises_required_advantage` |
| Zero exposure requires full compute-cost reward advantage | `zero_exposure_requires_full_cost` |
| Zero invalid opportunity + equal rewards favors rubber-stamp | `zero_invalid_equal_reward_rubber_dominates` |
| Effort-observability threshold iff selection margin closes | `observability_threshold_iff` |
| Zero observability removes reward channel | `zero_observability_removes_reward_channel` |
| Perfect observability may still be insufficient | `perfect_observability_insufficient` |
| More effort observability improves selection | `higher_observability_improves_selection` |
| Lower exposure raises observability requirement | `lower_exposure_raises_observability_threshold` |
| Current correction can be supercritical while slow maintenance is subcritical | `correction_supercritical_maintenance_subcritical_witness` |
| Slow maintenance can be viable while fault-specific correction is subcritical | `maintenance_viable_correction_subcritical_witness` |
| Event-level correction does not imply maintenance viability | `correction_supercritical_does_not_imply_maintenance_viable` |
| Maintenance viability does not imply event-level correction | `maintenance_viable_does_not_imply_correction_supercritical` |
| Jointly viable and jointly non-viable phase cells are inhabited | `both_reproduction_conditions_can_hold`; `neither_reproduction_condition_need_hold` |
| Next audit reproduction from slow-state update | `jam_next_reproduction_identity` |
| Exact return boundary at current criticality | `jam_critical_return_boundary` |
| Return shortfall/surplus determines next-step threshold direction | `jam_return_shortfall_makes_next_audit_subcritical`; `jam_return_surplus_makes_next_audit_supercritical` |
| Reduced cross-audit recurrence | `jamReducedCorrectionPath_succ` |
| Exact correction-margin recursion | `jamCorrectionMargin_step` |
| Subunit maintenance multiplier strictly erodes positive reproduction | `jamReducedCorrection_strictly_declines` |
| Same current reproduction can imply opposite five-step resilience | `event_level_success_not_sufficient_statistic_for_five_step_resilience` |
| Current supercritical state can cross below threshold next round | `current_supercritical_can_cross_subcritical_next_round` |
| Fungal redundant-state stability iff effective gain < 1 | `fungal_stable_iff_effective_gain_lt_one` |
| Unit fungal effective gain is neutral | `fungal_neutral_iff_effective_gain_eq_one` |
| Superunit fungal effective gain is unstable | `fungal_unstable_iff_effective_gain_gt_one` |
| Equal route allocation maximizes worst-case backup | `fungal_backup_share_le_half`, `fungal_backup_share_at_half` |
| JAM escalation feasible iff failure share < corrective share | `jam_escalation_feasible_iff_failure_lt_correction` |
| Feasible JAM escalation implies failure share < corrective share | `jam_feasible_implies_failure_lt_correction` |
| Attempt-rate floor implies harmful-finalization floor | `badFinalizationN_floor_from_attempt_floor` |

Build with:

```bash
lake update
lake exe cache get
lake build
```

The toolchain and Mathlib commit match the current formalization convention used by the companion Evolution-by-Emergence repository.

## End-to-end real-root proof

`RootSafety.lean` is a default Lake build target. It adds 11 declarations covering
root construction, its power identity, uniqueness, monotonicity, residual bounds,
threshold feasibility, exact target attainment, least sufficient effort and the
selected-safety/critical-cost equivalence. Every declaration prints its axioms.
See `docs/PHASE_BOUNDARY.md` for the exact claim map. No root existence or
leastness hypothesis remains assumed in `selected_safety_iff_critical_cost`.

## Endogenous producer floor

`EndogenousFloor.lean` is also a default Lake build target. It keeps the producer response abstract and assumes only that it is antitone in collective detection. The executable logistic response is therefore one specialization rather than an extra axiom in the proof. The machine-checked result is the finite-time lower envelope; the liminf statement in the model documentation is its analytic corollary for strictly positive adjustment.

## Closed-loop stability

`ClosedLoopStability.lean` formalizes the algebraic core of Experiment 2 for the declared reduced discrete-time map. It does not formalize the numerical existence of a fold or the general theorem connecting a one-dimensional differentiable map to local asymptotic stability; it verifies that, under the model assumptions and the equilibrium relation, the usual multiplier condition `|M| < 1` is exactly equivalent to loop gain `eta < 1`.

## Viability contribution

`ViabilityContribution.lean` formalizes the algebraic core of Experiment 3. The executable Python model supports arbitrary small failure topologies and coalition attribution; the Lean file isolates the exact two-cause result so the topology effect is separated from numerical enumeration and from any substrate-specific interpretation.

## Selected viability reversal

`SelectedViability.lean` formalizes the minimal Experiment 4 counterexample: adding a participant improves viability at frozen effort but can reduce realized viability after shared-reward re-equilibration. The formal theorem uses the exact polynomial reversal condition (z^2+4z-4>0); the equivalent square-root threshold is reported by the executable model.

## Corrective capacity

`CorrectiveCapacity.lean` formalizes the minimal Experiment 5 separation between current shared condition and a slower corrective-capacity stock. The key result is that the shared state can remain exactly at its quiet fixed point while capacity decay strictly lowers the derived finite-shock viability margin.

## State-dependent participant contribution

`StateDependentContribution.lean` joins the heterogeneous failure-topology model to the slow-capacity model. It proves that a participant's contribution through this channel scales with both the topology change it causes and the current reserve-capacity state.

## Vector-valued contribution

`VectorContribution.lean` formalizes the Experiment 7 representation result: for a two-loop contribution vector with opposite signs, admissible positive scalarization weights can produce either sign. A scalar global contribution therefore requires an explicit aggregation rule.

## Behavioral maintenance operators

`BehavioralMaintenance.lean` formalizes Experiment 8's falsification layer. It proves the exact replacement-gap condition, a passive-renewal counterexample to universal active-maintenance necessity, an overcorrection instability boundary, sign reversal under low signal fidelity, a harmful-reinforcement region, and the conditional repair criterion. The model uses "behavior" operationally and does not assume cognition or moral agency.

## JAM maintenance operators

`JamMaintenance.lean` formalizes the count-based substrate identities used in Experiment 9. It proves the exact one-validator correction/reliability increments and the opposite-signed effect of stronger escalation on correction reproduction versus scalability margin. It does not formalize the ELVES extinction-probability theorem itself; safety-certificate changes from that theorem remain executable calculations in Python.

## JAM audit behavior selection

`JamBehaviorSelection.lean` formalizes Experiment 10's partially identified three-action game. It proves the exact compute-versus-rubber and compute-versus-no-show boundaries and the monotonic effect of exposure on the reward differential needed to select real computation. It deliberately leaves reward and fault-loss magnitudes as higher-layer parameters because the Gray Paper delegates them.

## JAM effort observability

`JamEffortObservability.lean` formalizes Experiment 11's second-order maintenance channel. It proves that selective reinforcement depends jointly on effort observability and returned reward, and that structural loss of false-positive exposure raises the observability burden needed to select real computation.

## JAM recurrent corrective capacity

`JamRecurrentMaintenance.lean` adds a second timescale to the JAM analysis. It keeps the ELVES-style fault-specific reproduction mean `lambda_x` separate from a declared slow `C -> O -> R -> C` maintenance loop linking independently corrective capacity, maintenance observability/attribution and returned resources. The file machine-checks explicit witnesses showing that event-level supercritical correction and slow maintenance viability imply neither one another, and it inhabits all four phase cells. The slow-loop coefficients are model parameters rather than claimed Gray Paper variables; no novelty is claimed for the underlying positive-systems/reproduction-number threshold mathematics.

## JAM dynamic corrective resilience

`JamResilienceDynamics.lean` couples the slow corrective-capacity coordinate back to the next audit. For the declared state update `C' = r_C C + k_RC R` and `lambda = F C`, it proves the exact identity `lambda' = r_C lambda + F k_RC R`. At current criticality it then proves the one-step maintenance-return boundary `lambda' >= 1` iff `F k_RC R >= 1-r_C`, including strict shortfall and surplus corollaries. A reduced cross-audit path separately proves that the same current `lambda` can lead to opposite finite-horizon threshold status under different maintenance multipliers. These are dynamic model implications, not calibrated JAM forecasts.

## Fungal flow-coupled maintenance

`FungalFlowMaintenance.lean` formalizes Experiment 12's two-route local stability boundary. The nonlinear flow-reinforcement rule is a falsification model extension motivated by empirical fungal flow/cord-growth coupling; the file does not claim that this exact power-law is fungal physiology.

## Viability-conditioned ought synthesis

`ViabilityOught.lean` formalizes one exact structural synthesis result: the grounded JAM correction/failure branching requirements admit a common positive escalation strength iff the effective failure-amplifying share is smaller than the effective corrective share. The philosophical interpretation of such admissible regions as "viability-conditioned oughts" is kept outside the theorem.
