# Lean formalization

The Lean source checks only the algebraic core of the declared model. It does not validate the empirical suitability of the common-mode mixture or any mapping to JAM or ecology.

| Result | Lean declaration |
|---|---|
| Independent-failure specialization | `escape3_independent` |
| Perfect effort leaves common-mode escape | `escape3_perfect` |
| Harmful finalization at perfect effort is \(b\rho\) | `badFinalization_perfect` |
| Common-mode lower bound | `escape3_correlation_floor`; `badFinalization_correlation_floor` |
| Safety target below the floor is impossible | `safety_impossible_below_correlation_floor` |
| Quadratic private optimum | `monitorObjective_gap`; `selectedEffort_global_max` |
| Selected-versus-required boundary | `selectedEffort_meets_requirement_iff`; `selectedEffort_underprovides` |

Build with:

```bash
lake update
lake exe cache get
lake build
```

The toolchain and Mathlib commit match the current formalization convention used by the companion Evolution-by-Emergence repository.
