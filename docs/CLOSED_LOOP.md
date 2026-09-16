# Experiment 2 — closing the commons loop

## 1. Why this experiment

In the original adaptive model, commons health \(X_t\) is updated but never
read. That model studies distributed *prevention of damage to* a commons, but
not yet a distributed *commons controller*. The original programme asks how a
network keeps a shared enabling state inside a viable region when the state
itself shapes future control:

\[
X_t
\rightarrow
\text{capacity/incentives}
\rightarrow
\text{monitoring/capture}
\rightarrow
X_{t+1}.
\]

This experiment closes that return path and asks whether doing so creates phase
structure that the open-loop model cannot have.

## 2. Primary closure: commons-funded monitoring

The first closure makes monitoring reward depend on commons health:

\[
r(X)=r_0(\kappa+X),
\]

where \(\kappa\ge0\) is baseline funding independent of the commons. The
producer and monitor responses remain

\[
b^*=\sigma\!\left(\frac{g-\ell d}{T}\right),
\qquad
q^*=\operatorname{clip}_{[0,1]}
\left(\frac{b(1-\rho)r(X)}{c}\right),
\]

and commons health evolves as

\[
X_{t+1}=
\operatorname{clip}_{[0,1]}
\left[
X_t+\gamma(1-X_t)-\delta P_{bad,t}
\right].
\]

A degraded commons can therefore finance less checking, which can increase
harmful finalization and further degrade the commons. This is a toy closure,
not a claim that JAM rewards have this form.

## 3. Reduced analysis

For fixed \(X\), the producer-monitor subsystem has a unique behavioural
fixed point \((b^*(X),q^*(X))\). Monitor effort is nondecreasing in \(b\),
detection is nondecreasing in effort, and producer response is nonincreasing
in detection. Therefore target\((b)-b\) is strictly decreasing from positive
at \(b=0\) to negative at \(b=1\).

Write the resulting harmful-finalization probability as \(P^*(X)>0\).
Interior commons equilibria satisfy

\[
\gamma(1-X)=\delta P^*(X),
\]

so the equilibrium branch is

\[
\boxed{
\delta^*(X)=\frac{\gamma(1-X)}{P^*(X)}.
}
\]

### 3.1 Exact local stability criterion for the declared discrete map

Let \(P'(X)\le0\) and define

\[
\eta(X)
=
-(1-X)\frac{P'(X)}{P^*(X)}
=
-(1-X)\frac{d\ln P^*}{dX}.
\]

The derivative of the reduced one-step map at an interior equilibrium is

\[
M=1-\gamma-\delta P'(X).
\]

Using \(\delta P^*=\gamma(1-X)\),

\[
\boxed{
M=1-\gamma+\gamma\eta.
}
\]

Because \(0<\gamma\le1\) and \(\eta\ge0\), \(M\ge0\). Therefore the
standard one-dimensional local linear-stability condition \(|M|<1\) is
equivalent to

\[
\boxed{\eta(X)<1.}
\]

At \(\eta=1\), \(M=1\), the neutral condition at a generic fold of this
one-dimensional equilibrium branch. The algebraic equivalence is
machine-checked in formalization/ClosedLoopStability.lean.

This scope matters. For a completely general discrete-time regeneration law
\(R(X)\), the local condition is
\(|1+R'(X)-\delta P'(X)|<1\); a single comparison of logarithmic slopes is
not by itself the full discrete-time stability criterion.

### 3.2 Collapsed boundary and hysteresis window

At \(X=0\), clipping makes the collapsed state locally stable once

\[
\delta>\delta^*(0)=\frac{\gamma}{P^*(0)}.
\]

If \(\delta^*(X)\) is unimodal with an interior maximum
\(\delta_{fold}\), the collapsed state and a healthy stable branch coexist
for

\[
\boxed{
\delta^*(0)<\delta<\delta_{fold}.
}
\]

## 4. Results for commons-funded monitoring

Default parameters are
\(n=5,\rho=0.05,c=0.25,r_0=1,g=0.8,\ell=1.8,T=0.25,\gamma=0.04\).

### 4.1 Baseline funding

| \(\kappa\) | collapse onset | fold | \(X\) at fold | window ratio |
|---:|---:|---:|---:|---:|
| 0 | 0.042 | 0.547 | 0.524 | 13.13 |
| 0.01 | 0.053 | 0.558 | 0.519 | 10.58 |
| 0.05 | 0.121 | 0.606 | 0.501 | 5.02 |
| 0.10 | 0.217 | 0.668 | 0.479 | 3.08 |
| 0.20 | 0.420 | 0.803 | 0.435 | 1.91 |
| 0.50 | 1.091 | 1.295 | 0.304 | 1.19 |
| 1.00 | 2.402 | 2.423 | 0.092 | 1.009 |
| 1.20 | 2.991 | 2.992 | 0.009 | 1.00007 |
| 1.50 | — | — | — | monostable |

For this parameter family the fold disappears near

\[
\kappa_c\approx1.221.
\]

The coexistence window narrows much earlier as external funding decouples
monitoring from commons health.

### 4.2 Parameter robustness at \(\kappa=0.05\)

A fold exists for every one-at-a-time variation tested:

| varied | values → fold damage (window ratio) |
|---|---|
| \(\rho\) | 0: 0.72 (5.4); 0.05: 0.61 (5.0); 0.15: 0.43 (4.3); 0.30: 0.24 (3.1) |
| \(n\) | 1: 0.16 (3.0); 3: 0.38 (4.4); 5: 0.61 (5.0); 9: 1.09 (5.7) |
| \(c\) | 0.1: 1.78 (6.7); 0.25: 0.61 (5.0); 0.5: 0.29 (3.8); 1.0: 0.15 (2.6) |
| \(T\) | 0.1: 0.58 (4.9); 0.25: 0.61 (5.0); 0.5: 0.83 (6.8); 1.0: 1.17 (9.4) |
| \(\ell\) | 1.0: 1.16 (10.7); 1.8: 0.61 (5.0); 3.0: 0.61 (4.2) |

Increasing common-mode correlation and weakening the detection penalty show
interesting effects in this slice, but these remain parameter-specific
observations rather than general theorems.

### 4.3 Full model without time-scale separation

With producer and monitor adjustment rate 0.15:

| \(\kappa\) | below window | inside window | above fold |
|---:|---|---|---|
| 0 | both recover (~0.99) | healthy ~0.85 / collapsed 0 | both collapse |
| 0.05 | both recover (~0.98) | healthy ~0.82 / collapsed 0 | both collapse |
| 0.20 | both recover (~0.92) | healthy ~0.72 / collapsed 0 | both collapse |

The reduced phase structure therefore survives finite response times in these
checks.

## 5. Basin structure: monitor mobilisation is a state variable

The full system has state \((X,b,q)\), not just \(X\). At
\(\kappa=0,\delta\approx0.294\), \(X_0=0.15\) recovers when initial
monitor effort is around 0.3 or above and collapses when it is around 0.1 or
below across the tested attack rates.

With monitors starting at their private optimum:

| initial \(b_0\) | 0.02 | 0.05 | 0.10 | 0.20 | 0.40 | 0.60 | 0.80 | 0.95 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| \(X_{crit}\), \(\kappa=0\) | 0.29 | 0.27 | 0.23 | 0.19 | 0.14 | 0.12 | 0.11 | 0.10 |
| \(X_{crit}\), \(\kappa=0.05\) | 0.30 | 0.27 | 0.22 | 0.17 | 0.11 | 0.09 | 0.07 | 0.06 |

The same commons is therefore roughly three to five times more fragile after a
quiet period than after a high-attack period in these runs. Low attack
incidence demobilizes monitors because reward is detection-contingent. The
early-warning implication is:

\[
\boxed{
\text{commons condition and corrective mobilisation are both state variables.}
}
\]

## 6. Second-closure test

The fold should not be treated as meaningful if it depends uniquely on
\(r(X)\propto X\). The analysis was repeated with constant reward and two
different return paths.

### 6.1 Checking becomes more costly as the commons degrades

\[
c(X)=c_0\exp\!\left[3(1-X)\right].
\]

The reduced model gives collapse onset 0.1202, fold 0.2619 and window ratio
2.18. Inside that window, the full finite-adjustment model ends near
\(X=0.879\) from a healthy start and at \(X=0\) from the collapsed start.

### 6.2 Capture becomes more attractive as the commons degrades

\[
g(X)=g_0+1.2(1-X).
\]

The reduced model gives collapse onset 1.051, fold 1.853 and window ratio 1.76.
Inside that window, the full model ends near \(X=0.643\) from a healthy start
and at \(X=0\) from the collapsed start.

The damage scales are not directly comparable across closures. The repeated
result is the existence of a fold and coexisting attractors.

The interpretation is therefore broader than commons-funded monitoring:

\[
\boxed{
\max_X\eta(X)>1
\quad\text{is the local condition that permits the equilibrium branch to fold.}
}
\]

The return path may act through monitoring reward, checking cost, capture
incentive, or another mechanism.

## 7. Status and limits

- The reduced analysis assumes behavioural equilibration is fast relative to
  commons health; the full model checks selected cases at adjustment 0.15.
- The numerical fold finder assumes a unimodal equilibrium-damage curve; tests
  verify this for the reported reward-funded parameter families.
- Fold existence and location for the concrete closures are numerical.
- The multiplier/loop-gain equivalence is exact for the declared discrete-time
  linear-regeneration map and its algebraic core is machine-checked.
- The closure functions are deliberately minimal and are not asserted to be
  realistic descriptions of JAM.
