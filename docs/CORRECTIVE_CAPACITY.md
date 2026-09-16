# Experiment 5 — shared state and slow corrective capacity

## 1. Why a second state is needed

Experiments 1–4 distinguish current shared-state condition, structural
coverage and behavioral response. They still lack a slow stock representing
how much corrective action can be deployed when a finite shock arrives.

Experiment 5 introduces that stock explicitly.

The state is

\[
\boxed{(X,C)}
\]

where

- \(X\) is current shared-state condition;
- \(C\) is corrective capacity/readiness.

Fast effort is an action constrained by \(C\); it is not the same variable.

The model remains substrate-neutral. In a later JAM mapping, \(C\) could
represent spare checking/re-execution capacity. In another substrate it could
represent another slowly maintained corrective stock.

## 2. Quiet dynamics

Between shocks,

\[
X_{t+1}
=
X_t+\gamma(1-X_t),
\]

and

\[
C_{t+1}
=
(1-\delta)C_t+I_t,
\]

where \(I_t\) is maintenance/investment.

With no maintenance,

\[
I_t=0,
\]

capacity decays independently of the current shared-state recovery process.

The local recovery multiplier of \(X\) around \(X=1\) is

\[
\boxed{1-\gamma.}
\]

It contains no \(C\).

## 3. Operational finite-shock margin

Let \(V\) be the declared viability floor. A shock of size \(s\) lowers the
shared state. Up to \(\kappa C\) units of immediate correction can be deployed.

After using full available corrective capacity,

\[
X^+
=
X-s+\kappa C.
\]

Viability requires

\[
X^+\ge V,
\]

so

\[
s
\le
X-V+\kappa C.
\]

Therefore the uncapped finite-shock margin is

\[
\boxed{
M(X,C)=X-V+\kappa C.
}
\]

This is not a bookkeeping definition. It is the largest shock satisfying the
declared post-correction viability inequality in this model.

The equivalence

\[
X-s+\kappa C\ge V
\iff
s\le M(X,C)
\]

is machine-checked in Lean.

## 4. Same state, different future

At fixed \(X\),

\[
M(X,C_2)-M(X,C_1)
=
\boxed{
\kappa(C_2-C_1).
}
\]

Thus two systems with the same current shared state can have different
finite-shock margins.

With

\[
V=0.70,
\qquad
\kappa=0.50,
\qquad
X=1,
\]

capacity \(C=0.1\) gives

\[
M=0.35,
\]

whereas \(C=0.5\) gives

\[
M=0.55.
\]

Both have identical \(X\), and both have the same local \(X\)-recovery
multiplier \(1-\gamma\).

## 5. Quiet-period fragility

The strongest exact example starts at the quiet shared-state fixed point:

\[
X_0=1.
\]

Then

\[
X_t=1
\]

for every shock-free step, regardless of \(C\).

With zero maintenance,

\[
C_t=(1-\delta)^t C_0.
\]

Hence

\[
M_t
=
1-V+\kappa(1-\delta)^t C_0.
\]

So

\[
\boxed{
X_t\text{ can remain exactly unchanged while }M_t\text{ declines.}
}
\]

For one quiet step,

\[
M_{t+1}-M_t
=
-\kappa\delta C_t.
\]

With \(\kappa>0,\delta>0,C_t>0\), this is strictly negative. That result is
machine-checked.

This separates two kinds of fragility:

1. **local state fragility**, detectable through slowing of \(X\);
2. **reserve-capacity fragility**, which can change without altering the
   current \(X\) trajectory.

## 6. Maintenance requirement

A constant capacity target \(C^*\) is stationary when maintenance equals the
decay loss:

\[
\boxed{
I^*=\delta C^*.
}
\]

This gives a non-definitional maintenance requirement.

If a declared application requires a minimum finite-shock margin \(M_{\rm req}\),
one can then define a derived shortfall

\[
D
=
\max(0,M_{\rm req}-M(X,C)).
\]

Unlike the earlier provisional "verification debt" bookkeeping, this shortfall
is anchored to an independently defined capacity stock and an operational
disturbance margin.

The repository does not yet promote \(D\) to a general debt theorem; it is a
derived diagnostic.

## 7. Relation to critical slowing down

Experiment 2 gave

\[
1-M_{\rm local}
=
\gamma(1-\eta)
\]

for the reduced one-dimensional feedback model near a fold.

Experiment 5 addresses a different failure channel. Even if the local
\(X\)-multiplier is unchanged, \(C\) can decay.

Therefore a system can be far from a local fold in \(X\) yet become less able
to absorb a finite perturbation.

This is the precise version of the earlier statement:

\[
\boxed{
\text{present persistence does not prove present self-maintenance.}
}
\]

## 8. Grounding clue from JAM

This neutral model was introduced only after the JAM/ELVES grounding pass.

ELVES distinguishes the current accepted protocol state from the auditing
process capable of responding to invalid work. JAM also allocates a substantial
share of validator compute to auditing and escalates checking after visible
no-shows.

Those observations motivate a later substrate mapping in which \(C\) is spare
corrective/checking capacity.

No such mapping is assumed in the theorem above. In particular, the neutral
capacity-decay law

\[
C_{t+1}=(1-\delta)C_t+I_t
\]

is not claimed to be a JAM protocol equation.

## 9. Next step

The next stage should join participant contribution to state-dependent
capacity:

\[
\boxed{
\Delta_i M(X,C).
}
\]

A participant may contribute by

- changing direct correction;
- changing failure topology;
- changing other participants' selected effort;
- building or maintaining \(C\);
- changing the rate at which \(C\) decays or can be rebuilt.

Only after that should multiple shared-state loops be introduced.
