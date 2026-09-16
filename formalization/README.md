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

Build with:

```bash
lake update
lake exe cache get
lake build
```

The toolchain and Mathlib commit match the current formalization convention used by the companion Evolution-by-Emergence repository.
