# Verification record

On 16 September 2026, GitHub Actions run
[35056765190](https://github.com/albertjanvanhoek/Distributed-Commons-Control/actions/runs/35056765190)
compiled `DistributedCommons` and `RootSafety` at commit
`cb263d2075c059373de1d2e24f726348876453a0` using Lean 4.33.0 and pinned Mathlib
`db584cd6d46c92f209a44c0f1c829460d327499d`.

All 11 RootSafety declarations printed only `propext`, `Classical.choice` and
`Quot.sound`; no `sorryAx` or custom axiom occurred. The new proof file compiled
without warnings. The imported prior module has an unused-variable warning
for `hq0`, which does not affect proof checking.

The central result is `selected_safety_iff_critical_cost`. For positive n, b,
and cost, rho < 1, nonnegative reward, and b*rho <= epsilon < b, it proves
actual safety at clipped selected effort iff cost <= the critical cost
computed from the explicit real nth root. Physical assumptions, stochastic
independence, common-mode mixture suitability, and incentive adequacy remain
model assumptions; this proof checks their mathematical consequences.

The final PR revision additionally contains 20 Python tests, including the
regressions for tiny probabilities, exact floor equality, very large monitor
counts, and zero reward. CI reruns both proof targets and the static/dynamic
sweeps after each revision.
