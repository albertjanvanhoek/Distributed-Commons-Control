# Experiment 8 — behavioral maintenance operators

## 1. Hypothesis under test

The motivating hypothesis is stronger than ordinary "cooperation":

> Persistent decentralized commons may depend on participant-level processes
> that maintain the conditions under which the network can continue to
> function.

The purpose of this experiment is to **challenge** that statement rather than
encode it as an assumption.

The strongest version is false.

Participant-supplied maintenance is not universally necessary. A commons may
have enough passive or exogenous renewal to replace its losses without any
participant action.

The narrower statement that survives is conditional:

\[
\boxed{
\text{when passive renewal is below replacement, participant-generated
maintenance must close the replacement gap for the maintained stock to persist.}
}
\]

This is a statement about dynamics, not ethics.

---

## 2. What "behavior" means here

A **behavioral maintenance operator** is defined as

\[
\boxed{
\text{a state-contingent participant process that changes future
network/commons viability.}
}
\]

This definition does **not** require:

- consciousness;
- intention;
- a nervous system;
- moral concepts;
- agency in the human legal or philosophical sense.

The participant may be a person, animal, plant, fungus, cell, software
process, institution or other organized process.

The word "behavior" is therefore operational. If that terminology becomes
misleading in a particular substrate, "participant process" is equivalent.

---

## 3. Minimal replacement model

Let \(K_t\) be an enabling stock whose continued presence matters to a declared
viability condition.

Examples could include physical structure, relationship quality, transport
capacity, nutrient state, checking capacity, or some other maintained
condition.

Let

- \(\delta\) = fractional decay/loss;
- \(e\) = passive or exogenous renewal;
- \(m_t\) = aggregate participant-generated maintenance.

Then

\[
\boxed{
K_{t+1}
=
(1-\delta)K_t+e+m_t.
}
\]

Let \(V\) be the declared viability boundary.

At \(K_t=V\),

\[
K_{t+1}\ge V
\]

if and only if

\[
\boxed{
e+m_t\ge\delta V.
}
\]

This is machine-checked.

Define the replacement gap

\[
\boxed{
G_{\rm repl}
=
\max(0,\delta V-e).
}
\]

---

## 4. Falsification 1 — participant maintenance is not universally necessary

If

\[
e\ge\delta V,
\]

then with

\[
m_t=0
\]

the boundary is still preserved.

Therefore the universal proposition

> every persistent commons requires active participant maintenance

is false in this model.

This matters conceptually. The theory should not redefine every persistent
environmental process as "maintenance behavior."

Participant behavior becomes functionally necessary only when passive renewal
does not already close the replacement balance.

---

## 5. Conditional necessity — the replacement-gap theorem

If

\[
e<\delta V,
\]

then any participant behavior that preserves the boundary must satisfy

\[
\boxed{
m_t\ge\delta V-e.
}
\]

This is also machine-checked.

In the additive version,

\[
m_t=\sum_i m_{i,t}.
\]

No central coordinator is mathematically required. Local contributions may
close the same aggregate replacement gap:

\[
\boxed{
\sum_i m_{i,t}
\ge
\delta V-e.
}
\]

This is the minimal sense in which commons maintenance can be decentralized.

The model does **not** say such maintenance will be selected, correctly
targeted or stably coordinated. Earlier experiments already show why those are
separate questions.

---

## 6. Correction is maintenance — but more correction is not always better

Let \(K^\star\) be a target state. Write a local correction policy as

\[
m(K)
=
m_0+g(K^\star-K).
\]

Choose \(m_0\) so that \(K^\star\) is an equilibrium.

The local multiplier is

\[
\boxed{
\mu=1-\delta-g.
}
\]

Stable local correction requires

\[
|\mu|<1.
\]

For nonnegative \(g\),

\[
\boxed{
g<2-\delta.
}
\]

If

\[
g>2-\delta,
\]

then

\[
\mu<-1.
\]

The intended negative feedback has become an oscillatory/flip instability.

So the proposition

> more correction is always better

is false.

This is the behavioral analogue of the earlier finding that control itself can
become excessive or capturing.

---

## 7. Signal fidelity determines whether correction is actually corrective

Suppose the participant tries to respond to the sign of the deficit, but the
signal is sign-inverted with probability

\[
1-p.
\]

For nominal corrective gain \(g\), expected signed gain becomes

\[
\boxed{
g_{\rm eff}
=
(2p-1)g.
}
\]

Therefore

\[
p=\frac12
\]

gives zero expected correction, while

\[
\boxed{
p<\frac12
\Longrightarrow
g_{\rm eff}<0.
}
\]

The process is now anti-corrective in expectation.

This supplies a functional interpretation of the SCAP "signal fidelity"
principle:

> reliable corrective behavior requires not merely action, but a sufficiently
> reliable relation between the sensed state and the direction of response.

It is the function underneath human-language terms such as honesty or faithful
reporting; the theorem itself contains no moral vocabulary.

---

## 8. Reinforcement is also conditional

Positive feedback is required to retain useful processes, but "reinforce what
looks good" is not safe by itself.

Let

- \(h\) = prior probability a candidate process is actually helpful;
- \(p\) = accuracy of the evaluation signal;
- \(a>0\) = contribution of a helpful process;
- \(b>0\) = loss caused by a harmful process.

Reinforce candidates receiving a positive signal.

The sign of the expected true contribution among positively signalled
candidates is determined by

\[
\boxed{
R
=
hpa-(1-h)(1-p)b.
}
\]

Reinforcement is beneficial only when

\[
\boxed{
hpa>(1-h)(1-p)b.
}
\]

If the inequality reverses, positive feedback preferentially maintains enough
misclassified harmful processes to have negative expected value.

So:

> reinforcement without sufficiently informative evaluation can amplify
> failure.

This links reinforcement back to signal fidelity and corrigibility.

---

## 9. Repair / forgiveness remains conditional

SCAP's repair model already gives

\[
\boxed{
C_R\le r(V-W)
}
\]

as the region in which repair weakly dominates termination.

In neutral operator language:

- \(C_R\) = repair cost;
- \(r\) = probability repair succeeds;
- \(V\) = value if the relation is restored;
- \(W\) = outside value after exit.

Repair is not a universal maintenance rule.

Too little repair destroys recoverable infrastructure.

Too much repair retains persistently destructive edges.

The operator must remain conditional.

The same inequality is reproduced in this repository as

\[
r(V-W)-C_R\ge0.
\]

---

## 10. The SCAP principles as network-maintenance functions

The sufficient-alignment work distinguishes the human-language implementation
from the narrower network function. Experiment 8 adopts that distinction.

| Human-language implementation | Neutral maintenance function |
|---|---|
| honesty | preserve task-relevant signal fidelity |
| humility / corrigibility | remain reachable by discriminating information |
| tolerate dissent | preserve nonredundant information channels |
| contribute | close enough of the replacement/control gap |
| redundancy | keep correction from depending on one fallible channel |
| forgiveness | repair a damaged but recoverable edge |
| accountability | apply negative feedback to damaging processes |
| praise / reinforcement | increase persistence of processes with demonstrated positive contribution |
| reciprocity | return enough value to processes that pay maintenance costs |
| teach / transmit | reproduce correction and maintenance capacity |
| revise the protocol | keep the maintenance architecture itself corrigible |

These are not claimed to be universal moral rules.

They are candidate **behavioral maintenance operators** whose relevance is
defined by their effect on declared viability margins.

---

## 11. Five primitive operators

The ten SCAP principles can be compressed functionally into a smaller
maintenance cycle.

### 11.1 Sense

Preserve enough signal fidelity to distinguish states that require different
responses.

### 11.2 Correct

Apply negative feedback to departures that reduce declared viability.

### 11.3 Reinforce

Increase the persistence/capacity of processes supported by evidence of
positive contribution.

### 11.4 Repair or exit

Restore recoverable valuable edges; terminate or suppress edges for which
repair has negative expected value.

### 11.5 Reproduce the maintenance capacity

Maintain and transmit the ability to sense, correct, reinforce and repair.

The return loop that supplies resources to these operators is a sixth
cross-cutting condition.

Schematically,

\[
\boxed{
\text{sense}
\rightarrow
\{\text{correct},\text{reinforce}\}
\rightarrow
\text{repair/exit}
\rightarrow
\text{observe consequences}
\rightarrow
\text{revise}
}
\]

while resources and inheritance maintain the ability to repeat the loop.

---

## 12. Relation to the existing neutral stack

The current framework can now be read as

\[
(X,C,G,\beta),
\]

where

- \(X\) = current shared-state condition;
- \(C\) = maintained corrective capacity;
- \(G\) = interaction/network architecture;
- \(\beta_i\) = participant maintenance policy/operator set.

The viability object becomes

\[
\boxed{
\mathbf M(X,C,G;\beta).
}
\]

Participant contribution has at least two distinct forms:

\[
\Delta_i^{\rm presence}\mathbf M
\]

and

\[
\boxed{
\Delta_i^{\rm behavior}\mathbf M.
}
\]

The latter compares different policies of the *same* participant while holding
its identity/presence fixed.

This prevents a common conceptual mistake:

> a participant is not "good" or "bad"; a participant can perform processes
> that raise or lower different viability margins in different states.

---

## 13. Falsification ledger

| Hypothesis | Result |
|---|---|
| Participant maintenance is universally necessary for persistence | **Falsified**: passive renewal can close replacement balance |
| When passive renewal is insufficient, some participant-generated maintenance is required at the boundary | **Supported within model**: exact replacement-gap condition |
| A central regulator is necessary to close the replacement gap | **Falsified constructively** in additive model: distributed local contributions can sum to threshold |
| More corrective gain is always better | **Falsified**: gain above \(2-\delta\) creates flip instability |
| Nominal correction remains corrective despite arbitrary signal corruption | **Falsified**: below 50% sign fidelity expected feedback reverses |
| Positive reinforcement of positively signalled processes is always beneficial | **Falsified**: depends on classifier fidelity, prior and harm/benefit magnitudes |
| Repair/forgiveness is always better than termination | **Falsified**: exact conditional repair inequality |
| These operators require human cognition | **Not required by the mathematics**; empirical substrate question |
| Human ethical labels and maintenance operators are identical | **Not claimed**; the mapping is many-to-many and implementation-specific |

---

## 14. Tautology guard

The replacement equation is an accounting constraint. By itself it does not
show that a biologically or socially interesting "maintenance behavior" exists.

The statement

> persistence requires enough replacement to offset loss

is nearly definitional once decay and the maintained stock are declared.

A **behavioral maintenance claim** therefore requires additional empirical
content:

1. identify a participant process independently of the persistence outcome;
2. show that the process is state-contingent or otherwise mechanistically
   linked to the maintained condition;
3. perturb, remove or alter that process;
4. predict a change in the replacement balance or viability margin that is not
   already explained by passive/exogenous renewal;
5. test that prediction.

In symbols, it is not enough to observe

\[
K_{t+1}\approx K_t.
\]

One needs a discriminating prediction such as

\[
\boxed{
M(\beta_i)-M(\beta_i')
\neq0
}
\]

for a specified change in participant process \(\beta_i\), with passive
renewal held fixed or separately estimated.

This is the standard by which the proposed cross-substrate operator family
should be falsified.

## 15. Empirical grounding outside humans

This model was motivated by the possibility that functions humans describe in
moral or social language may have non-human implementations.

The relevant empirical question is therefore not

> does a plant "forgive"?

but

> is there a state-contingent process that repairs or preserves a useful
> interaction or enabling condition?

Likewise, rather than asking whether fungi "reward good behavior," ask whether
network paths are selectively reinforced when they continue to carry useful
resource flows.

Established ecological literatures already contain neighboring phenomena:

- **ecosystem engineering / niche construction:** organisms create, modify and
  maintain environmental conditions;
- **plant hydraulic redistribution and facilitation:** roots can redistribute
  water across soil layers, with water becoming available for the same or
  neighboring plants;
- **fungal mycelial networks:** network architecture changes through growth,
  branching, fusion and regression in response to resource distribution,
  damage and predation; transport routes can be selectively reinforced while
  redundant mycelium is recycled.

These are empirical analogues, not proof that the full SCAP operator stack is
present in nature.

Experiment 8 therefore proposes a research language in which such processes
can be compared without attributing human moral cognition to them.

---

## 16. JAM as the next falsification substrate

JAM remains useful because it implements maintenance functions without moral
language.

Candidate mappings include:

- auditing judgments → sensing/correction;
- tranche escalation after no-show → compensatory correction;
- implementation diversity → preservation of independent corrective channels;
- slashing/accountability → negative feedback on damaging behavior;
- staking/effort mechanisms → possible return/reinforcement layer.

But several operators remain ungrounded or delegated:

- repair/re-entry after fault;
- positive reinforcement of demonstrated useful checking;
- inheritance/change of the corrective protocol itself.

The next JAM-facing question should therefore be:

\[
\boxed{
\text{which behavioral maintenance operators are actually implemented,
which are delegated, and which are absent?}
}
\]

Then perturb each one and measure its effect on the grounded JAM viability
vector rather than assuming the operator is beneficial.

---

## 17. Substrate-derived refinement: maintenance observability

The JAM return test adds one candidate operator that Experiment 8 did not
separate explicitly:

\[
\boxed{\text{maintenance observability}}
\]

A decentralized system may need not only to sense the commons state but also
to distinguish whether costly maintenance was actually performed rather than
cheaply imitated.

The JAM analysis suggests the candidate maintenance conditions

\[
\boxed{
\text{capacity}
+
\text{state observability}
+
\text{maintenance observability}
+
\text{return-loop closure}.
}
\]

This is **not yet promoted to a universal theorem**. It is a substrate-derived
refinement that should be challenged in another domain before being folded into
the neutral primitive operator list.

## 18. Research boundary

Experiment 8 does **not** establish that ethics is reducible to network
maintenance.

It establishes something narrower:

\[
\boxed{
\text{several behaviors described by SCAP in human normative language have
substrate-neutral functional counterparts that can be modeled as maintenance
operators of decentralized viable networks.}
}
\]

Whether the recurrence of those functions helps explain recurring ethical
norms is a separate hypothesis.

That hypothesis should be tested only after the functional operators
themselves survive cross-substrate falsification.
