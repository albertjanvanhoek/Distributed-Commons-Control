# Minimal model of distributed commons control

## 1. Object of study

The commons is a state variable \(X_t\in[0,1]\) whose condition affects the future capabilities of multiple participants. No participant is assumed to contain a complete representation of \(X_t\), own it, or optimize it globally.

The minimal architecture contains a producer that may propose harmful work, \(n\) monitors that may detect it, a commitment rule that updates shared state when work passes, and return paths through rewards, penalties and future commons condition.

"Harmful" is operational: work whose commitment moves the declared shared-state variable in the adverse direction. The model does not infer a moral category from that label.

## 2. Static checking layer

Let \(b\in[0,1]\) be the probability of a harmful proposal and \(q\in[0,1]\) the symmetric effort or reliability of each monitor.

### 2.1 Independent failures

If monitor failures are conditionally independent, harmful work escapes all \(n\) monitors with probability

\[
E_n^{ind}(q)=(1-q)^n.
\]

Redundancy then drives escape toward zero whenever \(q>0\).

### 2.2 Common-mode mixture

Pure independence is too generous for validators, institutions or ecological sensors. Introduce \(\rho\in[0,1]\): with probability \(\rho\), all monitors share a blind spot and fail; with probability \(1-\rho\), their failures are independent.

Then

\[
E_n(q,\rho)=\rho+(1-\rho)(1-q)^n
\]

and

\[
P_{bad}(b,q,n,\rho)=bE_n(q,\rho).
\]

This is not offered as a universal correlation model. It is the smallest model that separates the number of monitors from diversity of failure modes.

### 2.3 Correlated capture floor

At perfect effort, \(P_{bad}(b,1,n,\rho)=b\rho\). Thus a target \(P_{bad}\le\varepsilon\) is impossible within the architecture if

\[
\varepsilon<b\rho.
\]

The limit cannot be repaired by adding monitors that retain the same common-mode vulnerability. The architecture must reduce \(b\), reduce \(\rho\), change the commitment rule, or add a genuinely different corrective channel.

### 2.4 Sufficient effort

If \(b=0\) or \(\varepsilon\ge b\), zero effort is sufficient. For \(b>0\), \(0\le\rho<1\), and \(b\rho\le\varepsilon<b\), the minimum symmetric effort is

\[
q_{suff}=1-
\left(
\frac{\varepsilon/b-\rho}{1-\rho}
\right)^{1/n}.
\]

This is a functional requirement derived from the declared safety target; it is not a prediction of what monitors will choose.

## 3. Locally selected effort

Let a monitor receive reward \(r\) per detected harmful proposal and pay quadratic effort cost \(cq^2/2\). Because the common-mode blind spot also removes the opportunity for an individual monitor to detect the proposal, its private one-round objective is

\[
U_M(q)=b(1-\rho)rq-\frac{c}{2}q^2.
\]

The unconstrained optimum is \(q_{sel}=b(1-\rho)r/c\), clipped to \([0,1]\) in the executable model. Selected monitoring is sufficient exactly when \(q_{sel}\ge q_{suff}\). For an externally supplied requirement \(q_{req}\), the interior condition is

\[
cq_{req}\le b(1-\rho)r.
\]

Low observed attack incidence \(b\), weak monitoring reward \(r\), or high checking cost \(c\) can therefore select less effort than the shared-state target requires.

## 4. Adaptive extension

The simulation adds delayed best responses. At round \(t\), the producer observes the previous detection probability and moves toward

\[
b_t^*=\sigma\!\left(\frac{g-\ell d_t}{T}\right),
\]

where \(g\) is private capture gain, \(\ell\) is the penalty if detected, \(d_t=1-E_n(q_t,\rho)\), \(T>0\) controls response smoothness, and \(\sigma\) is the logistic function.

Monitors move toward the private optimum implied by the current harmful-attempt rate:

\[
q_t^*=\operatorname{clip}_{[0,1]}\left(\frac{b_t(1-\rho)r}{c}\right).
\]

Adjustment parameters create finite response times rather than instantaneous equilibrium.

### 4.1 Endogenous common-mode floor

The common-mode mixture also caps collective detection. Since

\[
d_t=1-E_n(q_t,\rho)\le 1-\rho,
\]

and the producer target decreases as detection increases,

\[
b_t^*
\ge
\sigma\!\left(
\frac{g-\ell(1-\rho)}{T}
\right)
\equiv m(\rho).
\]

Let the producer adjustment rate be \(\alpha_b\in(0,1]\), so before the
numerically redundant probability clipping,

\[
b_{t+1}
=
b_t+\alpha_b(b_t^*-b_t).
\]

If every target obeys \(b_t^*\ge m\), repeated partial adjustment gives the
finite-time lower envelope

\[
\boxed{
b_t\ge
m+(1-\alpha_b)^t(b_0-m).
}
\]

Therefore

\[
\liminf_{t\to\infty} b_t\ge m,
\qquad
\liminf_{t\to\infty}P_{bad,t}\ge \rho m.
\]

For the default response parameters \(g=0.8\), \(\ell=1.8\),
\(T=0.25\) and the 3% sweep target, \(\rho=0.30\) gives

\[
m\approx0.1370513,
\qquad
\rho m\approx0.0411154>0.03.
\]

Thus the entire \(\rho=0.30\) block is asymptotically unsafe even with
arbitrarily many same-mode monitors and arbitrarily cheap monitoring. This is
stronger than treating \(b\rho\) as a floor at externally fixed \(b\):
the producer response sustains a positive \(b\) endogenously.

The finite-time adjustment theorem and the detection-cap argument are
machine-checked in `formalization/EndogenousFloor.lean`. The Lean theorem is
stated for any producer response antitone in detection; the logistic response
above is the executable model's specialization.

Commons condition evolves as

\[
X_{t+1}=\operatorname{clip}_{[0,1]}
\left[X_t+\gamma(1-X_t)-\delta P_{bad,t}\right],
\]

where \(\gamma\) is regeneration and \(\delta\) is damage per harmful finalization.

The candidate verification-debt stock is

\[
D_{t+1}=\max\{0,(1-\mu)D_t+P_{bad,t}-\varepsilon\}.
\]

This accumulates safety-target overshoot and permits repayment when the system has safety margin. It is deliberately labelled a candidate: alternative debt definitions must be compared before treating it as an observable.

## 5. Phase variables

The first sweep varies monitor count \(n\), common-mode correlation \(\rho\), and effort cost \(c\). Primary outcomes are long-run harmful-finalization probability, commons health, selected effort, safety margin and verification debt.

The expected qualitative regions are:

1. **Sufficient distributed control:** selected effort reaches the safety boundary.
2. **Underprovided control:** the target is attainable but selected effort remains below it.
3. **Structural insufficiency:** \(\varepsilon<b\rho\); no amount of same-mode effort suffices.
4. **Debt-hidden deterioration:** current commons health remains high while verification debt is positive.

Only the first three follow directly from the static equations. The fourth depends on time scales and must be demonstrated, not assumed.
