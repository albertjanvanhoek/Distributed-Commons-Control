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
