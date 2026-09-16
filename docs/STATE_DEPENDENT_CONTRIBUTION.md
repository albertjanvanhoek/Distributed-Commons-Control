# Experiment 6 — state-dependent participant contribution

## 1. Joining topology to reserve capacity

Experiment 3 defined participant contribution through failure topology.
Experiment 5 separated current shared state \(X\) from a slow corrective-capacity
stock \(C\).

Experiment 6 joins those results without assigning additive pieces of \(C\) to
participants.

Let

\[
\pi(S)
=
P(\text{all participants in }S\text{ that could activate correction are disabled}).
\]

If at least one corrective participant is available, the stored reserve extends
the finite-shock margin by

\[
\kappa C.
\]

If all are disabled, only the passive margin

\[
X-V
\]

remains.

## 2. Expected finite-shock margin

The expected margin is

\[
\boxed{
\bar M(S;X,C)
=
X-V+
(1-\pi(S))\kappa C.
}
\]

For a participant \(i\), compare a coalition \(S\) without \(i\) to
\(S\cup\{i\}\). Then

\[
\Delta_i \bar M
=
\bar M(S\cup\{i\};X,C)-\bar M(S;X,C).
\]

Algebra gives

\[
\boxed{
\Delta_i \bar M
=
\kappa C
\left[
\pi(S)-\pi(S\cup\{i\})
\right].
}
\]

This is machine-checked in Lean.

A participant's contribution through this channel therefore depends jointly on

- network failure topology;
- current reserve capacity;
- the declared correction effectiveness.

It is not a fixed trait of the participant.

## 3. Independent-profile example

Reuse Experiment 3's smallest failure topology:

- \(A_1,A_2\) are both disabled by cause \(A\);
- \(B_1\) is disabled by independent cause \(B\);
- \(P(A)=P(B)=\rho\).

Then

\[
\pi(\{A_1,A_2\})=\rho,
\]

while

\[
\pi(\{A_1,A_2,B_1\})=\rho^2.
\]

Therefore \(B_1\)'s expected-margin contribution is

\[
\boxed{
\Delta_{B_1}\bar M
=
\kappa C\rho(1-\rho).
}
\]

The same participant has zero contribution through this channel when \(C=0\).

At \(\rho=0.05,\kappa=0.5,C=0.5\),

\[
\Delta_{B_1}\bar M
=
0.011875.
\]

Removing one of the redundant \(A\)-profile participants from the full
coalition changes no all-disabled probability and therefore has zero
leave-one-out contribution through this channel.

## 4. Contribution changes as the state changes

Suppose quiet capacity decays as

\[
C_{t+1}
=
(1-\delta)C_t.
\]

Because

\[
\Delta_i\bar M
\propto C,
\]

the same participant's contribution obeys

\[
\boxed{
\Delta_i\bar M_{t+1}
=
(1-\delta)
\Delta_i\bar M_t.
}
\]

Thus contribution can decline during a quiet period even when

- the participant is unchanged;
- network topology is unchanged;
- current shared state \(X\) is unchanged.

This is the first exact state-dependent participant contribution in the
repository.

## 5. Certified margin

Expected margin is not the only useful attribution question.

For a declared access-failure target \(\varepsilon_a\), define a stricter
certified margin:

\[
M_{\rm cert}(S)
=
\begin{cases}
X-V+\kappa C,&\pi(S)\le\varepsilon_a,\\
X-V,&\pi(S)>\varepsilon_a.
\end{cases}
\]

Now a participant can be decisive by moving the network across the reliability
threshold.

With

\[
\rho=0.05,
\qquad
\varepsilon_a=0.01,
\]

the coalition \(\{A_1,A_2\}\) has failure probability 0.05 and therefore cannot
certify the capacity extension, whereas

\[
\{A_1,A_2,B_1\}
\]

has failure probability 0.0025 and can.

For \(X=1,V=0.7,\kappa=0.5,C=0.5\), the added participant changes certified
margin from

\[
0.30
\]

to

\[
0.55.
\]

Its certified contribution is therefore 0.25: the entire available
capacity extension.

At a much stricter target where both coalitions fail, or a loose target where
both pass, the same participant's certified contribution is zero.

So contribution depends not only on participant and network state but also on
the declared viability criterion.

## 6. Relation to JAM grounding

This structure is compatible with the JAM/ELVES lesson without making the
neutral theorem JAM-specific.

In the shared-client extension, implementation diversity changes the
probability that a corrective auditing chain can successfully activate.
Separately, spare checking capacity determines how much correction the system
can perform.

That is structurally analogous to

\[
\pi(S)
\quad\text{and}\quad
C
\]

here.

The neutral result is therefore:

\[
\boxed{
\text{failure-topology contribution is valuable in proportion to the
corrective capacity that topology makes accessible.}
}
\]

A JAM instantiation would need to replace the simple binary access model with
the actual ELVES branching bound and load/capacity mechanism.

## 7. Next step

The participant/network/shared-state stack now contains four distinct
contribution channels:

1. direct structural correction;
2. failure-topology/decorrelation;
3. induced behavioral response;
4. access to maintained reserve capacity.

The next abstraction should therefore introduce multiple viability loops
rather than another scalar mechanism.

Contribution should become a vector

\[
\boxed{
\Delta_i\mathbf M
=
(\Delta_iM_1,\ldots,\Delta_iM_k),
}
\]

allowing the same participant to contribute positively to one loop and
negatively to another without forcing a single global label.
