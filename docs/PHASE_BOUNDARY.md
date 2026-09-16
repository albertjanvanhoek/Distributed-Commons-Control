# Complete selected-versus-sufficient phase boundary

## 1. Parameters

Let:

- \(b\in[0,1]\): harmful-proposal probability;
- \(\rho\in[0,1]\): common-mode blind-spot probability;
- \(n\ge1\): monitor count;
- \(r\ge0\): reward per individual detection;
- \(c>0\): quadratic effort-cost coefficient;
- \(\varepsilon\in[0,1]\): maximum acceptable harmful-finalization probability.

For symmetric monitor effort \(q\in[0,1]\),

\[
P_{bad}(q)=b\left[\rho+(1-\rho)(1-q)^n\right].
\]

The feasible private optimum under the declared monitor objective is

\[
q_{sel}=\min\left\{1,\frac{b(1-\rho)r}{c}\right\}.
\]

## 2. The four exhaustive regimes

### Regime 0: no monitoring required

If

\[
\varepsilon\ge b,
\]

then even an unchecked proposal stream satisfies the declared target. Thus \(q_{suff}=0\). This does not mean monitoring has no other function; only that it is unnecessary for this one inequality.

### Regime 1: structural impossibility

If

\[
\varepsilon<b\rho,
\]

then the target lies below the common-mode floor. No amount of effort and no increase in the number of monitors with the same blind spot can satisfy it.

### Regimes 2 and 3: attainable non-trivial control

For

\[
b\rho\le\varepsilon<b
\quad\text{and}\quad \rho<1,
\]

the minimum symmetric effort is

\[
q_{suff}=
1-left(
\frac{\varepsilon/b-\rho}{1-\rho}
\right)^{1/n}.
\]

The target is maintained by selected behavior exactly when

\[
\boxed{
\frac{b(1-\rho)r}{c}
\ge
1-left(
\frac{\varepsilon/b-\rho}{1-\rho}
\right)^{1/n}
}
\]

or, equivalently, when

\[
\boxed{
c\le c_{crit}
=
\frac{b(1-\rho)r}{q_{suff}}.
}
\]

Equality belongs to the sufficient-control region. Therefore:

- \(c\le c_{crit}\): **sufficient selected control**;
- \(c>c_{crit}\): **underprovided control**.

Because \(q_{suff}\le1\), clipping the private optimum at one does not change this boundary.

## 3. The correlation double squeeze

Within the non-trivial attainable region, increasing \(\rho\) has two aligned effects:

1. it raises \(q_{suff}\), because a larger fraction of failure cannot be repaired by ordinary monitor effort;
2. it lowers the private marginal return \(b(1-\rho)r\), because blind spots remove opportunities to detect and be rewarded.

Consequently,

\[
c_{crit}=\frac{b(1-\rho)r}{q_{suff}}
\]

falls from both numerator and denominator effects. Correlation does not merely leave a residual risk. It shrinks the economic region in which distributed checking selects enough effort.

At \(\varepsilon=b\rho\), the target sits exactly at the floor and \(q_{suff}=1\). Any slack loss makes the target impossible.

## 4. What redundancy can and cannot do

For a fixed attainable target with normalized residual

\[
x=\frac{\varepsilon/b-\rho}{1-\rho}\in[0,1),
\]

we have \(q_{suff}=1-x^{1/n}\). Increasing \(n\) lowers the required effort per monitor. It does not lower the floor \(b\rho\). Thus:

> More monitors compensate for independent weakness; only diversity of failure mode changes the correlated limit.

## 5. Verification status

`formalization/RootSafety.lean` defines the nonnegative root explicitly as
`Real.rpow x ((n : ℝ)⁻¹)`. The machine-checked chain includes:

- `nthRoot_pow`: the constructed root has nth power equal to its argument;
- `nthRoot_unique`: uniqueness among nonnegative roots;
- `nthRoot_monotone`: monotonicity in the argument;
- `sufficientEffortN_bounds`: the threshold lies in (0,1] in the non-trivial attainable region;
- `sufficientEffortN_hits_target`: the explicit threshold reaches epsilon exactly;
- `safety_iff_sufficientEffortN`: actual safety holds exactly at or above this threshold;
- `selected_safety_iff_critical_cost`: actual safety at clipped selected effort holds exactly when cost is at most the explicit critical cost.

These theorems apply for every positive natural monitor count. The earlier
root-substitution lemma remains as a component of the proof, but its root
hypothesis is now discharged by the constructed real root.

This verifies the conditional mathematics, not the suitability of the failure
mixture or reward assumptions for a real protocol. The Python implementation
uses floating-point arithmetic: structural floor comparisons are not relaxed,
and effort equality uses only a relative tolerance (no absolute tolerance).
`expm1(log(x)/n)` avoids cancellation in small positive effort requirements.
The model parameter `correlation` is a common-mode mixture weight, not generally
a Pearson correlation coefficient. The cost here is per monitor; increasing n
also increases potential total monitoring costs and reward expenditure.
