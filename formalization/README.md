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
