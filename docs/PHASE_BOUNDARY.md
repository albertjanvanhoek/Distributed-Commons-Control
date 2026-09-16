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

The Python implementation classifies all four regimes and directly checks the boundary. The Lean formalization proves for arbitrary \(n\):

- the common-mode floor;
- impossibility below that floor;
- exact arrival at \(\varepsilon\) for any root satisfying the normalized boundary equation;
- the quadratic selected optimum;
- invariance of the sufficiency boundary under probability clipping;
- equivalence between sufficient selected effort and \(c\le c_{crit}\).

Lean does not yet prove existence, uniqueness or monotonicity of the real \(n\)-th root. Those analytic facts remain outside the machine-checked core and are not needed for the finite Python classifier.
