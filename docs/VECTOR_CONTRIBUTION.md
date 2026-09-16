# Experiment 7 — vector-valued contribution across viability loops

## 1. Why a vector is necessary

Experiments 3–6 used one declared viability loop at a time.

A real network can participate in several loops simultaneously. The same
participant can increase one viability margin and reduce another.

The neutral object is therefore

\[
\boxed{
\Delta_i\mathbf M
=
(\Delta_iM_1,\ldots,\Delta_iM_k).
}
\]

A scalar net contribution is a secondary object that requires an explicit
aggregation rule.

## 2. Two-loop impossibility of a weight-free sign

Take the smallest nontrivial case:

\[
\Delta_i\mathbf M=(a,b),
\]

with

\[
a>0,
\qquad
b<0.
\]

Suppose someone chooses nonnegative scalarization weights and reports

\[
S=w_1a+w_2b.
\]

The sign is not intrinsic.

Choose

\[
(w_1,w_2)=(-2b,a).
\]

Both weights are positive and

\[
S=-ab>0.
\]

But choose instead

\[
(w_1,w_2)=(-b,2a).
\]

Again both weights are positive, while

\[
S=ab<0.
\]

Therefore

\[
\boxed{
\text{the same contribution vector admits both positive and negative
scalar totals under admissible positive weights.}
}
\]

The two witness constructions are machine-checked in Lean.

## 3. Consequence

A participant cannot be assigned an intrinsic global sign merely because each
loop contribution has been quantified.

Any scalar statement such as

- net beneficial;
- net harmful;
- positive total contribution;

contains an additional normative or task-specific weighting assumption.

That weighting may be legitimate. It just must be declared.

## 4. Relation to the previous experiments

The vector components can themselves be the outputs already constructed:

- direct structural margin contribution;
- failure-topology/decorrelation contribution;
- selected/re-equilibrated contribution;
- reserve-capacity access contribution;
- liveness or latency contribution;
- another declared viability loop.

The framework therefore does not require one participant category such as
"mutualist", "defector", "regulator" or "keystone".

The mathematically primitive statement is loop-indexed:

\[
\boxed{
\text{participant }i
\text{ changes viability margin }M_\ell
\text{ by }\Delta_iM_\ell.
}
\]

## 5. JAM grounding clue

JAM/ELVES already suggests at least two different margins:

1. invalid-acceptance safety;
2. liveness/scalability under no-show escalation.

A future JAM contribution vector might therefore contain quantities such as

\[
(
\Delta_i M_{\rm safety},
\Delta_i M_{\rm liveness}
).
\]

Nothing in the current grounding establishes that an actual validator has
opposite signs on those two components. Experiment 7 therefore does not invent
such a JAM tradeoff.

It only establishes the neutral representation required if such tradeoffs
exist.

## 6. Status of the programme

The neutral stack now separates:

1. what the network can structurally withstand;
2. how participant failure topology changes that margin;
3. how other participants re-equilibrate;
4. current shared state versus maintained reserve capacity;
5. state-dependent contribution to access of that reserve;
6. multiple loop-specific contribution components.

The next work should be a substrate return test rather than another generic
scalar mechanism.
