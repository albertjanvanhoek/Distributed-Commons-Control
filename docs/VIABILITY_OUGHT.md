# Viability-conditioned ought — the cross-substrate synthesis

## 1. Why use the word "ought" carefully?

The experiments in this repository repeatedly produce statements of the form

\[
\boxed{
\text{if a declared organization/property is to persist, some process or
parameter must lie in a particular region.}
}
\]

Examples include:

- replacement must cover loss;
- corrective escalation must be strong enough but failure amplification weak
  enough;
- actual costly verification must receive enough expected return;
- redundant fungal transport is stable only below a positive-feedback gain
  boundary.

These statements are **conditional necessities**.

They are not, by themselves, categorical moral obligations.

For that reason this repository uses the conservative term

\[
\boxed{\textbf{viability-conditioned ought}.}
\]

The broader phrase "ontological ought" may be philosophically useful, but it
carries stronger claims that are not established by the mathematics here.

---

## 2. The relation to established theory

The mathematical core is not new.

### Viability theory

Aubin and collaborators developed viability theory to study whether dynamical
systems can remain inside prescribed constraint sets and to characterize the
states and controls from which continued viability is possible.

The central object is the viability kernel.

So the move

\[
\text{declare constraint set}
\rightarrow
\text{derive admissible controls}
\]

is established mathematics.

### Biological normativity and adaptivity

Autopoietic and enactive approaches, particularly Di Paolo's work on
adaptivity, explicitly connect self-maintenance, viability conditions and
organism-relative normativity.

Organizational accounts of biological autonomy similarly emphasize
self-maintaining networks of constraints.

There is an active philosophical debate about how far such organizational
accounts objectively ground function or normativity.

### Distributed control

Decentralized multi-agent control already studies how local agents can preserve
collective constraints such as connectivity or safety.

Therefore this repository does **not** claim novelty for:

- viability constraints;
- self-maintenance as a source of biological normativity;
- decentralized control;
- network connectivity maintenance.

The research question here is narrower.

---

## 3. What the present programme adds

The experiments ask:

> What local processes keep a distributed network within a declared viability
> region when there is no central maintainer?

And then:

> What keeps those maintenance processes themselves functioning?

Across JAM and fungal transport, the same functional problem appears with very
different implementations.

JAM uses:

- judgments;
- escalation;
- independent clients;
- fault records;
- effort observation;
- staking/economic return.

Fungal transport can use:

- physical flow;
- local growth responses;
- route reinforcement;
- regression/recycling;
- network topology.

The interesting commonality is therefore **not a particular behaviour**.

It is the organization of maintenance relations.

---

## 4. A minimal formal statement

Let

\[
z_{t+1}=F(z_t,\theta,d_t)
\]

describe a system, where

- \(z_t\) is state;
- \(\theta\) is an architecture, policy or parameter set;
- \(d_t\) is a disturbance.

Let

\[
\mathcal V
\]

be a declared viability region and

\[
\mathcal D
\]

a declared disturbance class.

A one-step admissible maintenance region can be written

\[
\boxed{
\mathcal A_{\mathcal V}(z)
=
\left\{
\theta:
F(z,\theta,d)\in\mathcal V
\quad
\forall d\in\mathcal D
\right\}.
}
\]

A full-horizon version asks whether a policy keeps the trajectory inside
\(\mathcal V\) indefinitely; that is the domain of viability/invariance theory.

The repository's "ought" language means only:

\[
\boxed{
\text{if continuation within }\mathcal V\text{ is stipulated, then }
\theta\text{ ought to lie in }\mathcal A_{\mathcal V}.
}
\]

This is a conditional statement.

---

## 5. "Before the is" means logical order

The phrase

\[
\text{ought before is}
\]

should not be read here as a temporal claim that norms physically existed
before the system.

It is a **modeling order**.

### Step 1 — declare continuation

What must remain possible for the organization/property under study to count
as continuing?

### Step 2 — derive necessary conditions

Before looking at the observed implementation, derive what any candidate
mechanism must satisfy.

### Step 3 — measure the "is"

Measure the actual architecture, behavior and parameter values.

### Step 4 — compare

If the observed system lies outside the predicted viable region, then at least
one of the following must be true:

1. the system will lose the declared property;
2. a compensating process is missing from the model;
3. the disturbance class was wrong;
4. the declared viability criterion does not match what the system actually
   maintains.

That is a falsification procedure.

---

## 6. Four exact examples already in the repository

### 6.1 Replacement

For

\[
K_{t+1}=(1-\delta)K_t+e+m_t
\]

at viability boundary \(V\),

\[
\boxed{
e+m_t\ge\delta V.
}
\]

If passive renewal is insufficient,

\[
\boxed{
m_t\ge\delta V-e.
}
\]

This is the simplest viability-conditioned ought:

> if the maintained stock is to persist at the boundary, replacement must
> cover loss.

---

### 6.2 JAM — simultaneous correction and scalability

Let

\[
h
\]

be the effective share capable of correct escalation and

\[
u
\]

the share contributing to no-show/failure amplification.

With escalation strength

\[
s_\delta,
\]

the two requirements are

\[
\boxed{
h s_\delta>1
}
\]

for corrective escalation to be supercritical, and

\[
\boxed{
u s_\delta<1
}
\]

for failure escalation to remain subcritical.

The new synthesis theorem proves:

\[
\boxed{
\exists\,s_\delta>0:
\left(
h s_\delta>1
\land
u s_\delta<1
\right)
\iff
u<h,
}
\]

for

\[
h>0,\qquad u\ge0.
\]

A constructive feasible value when \(u<h\) is

\[
\boxed{
s_\delta=\frac{2}{h+u}.
}
\]

So before selecting the protocol parameter \(s_\delta\), the architecture
already has a structural viability requirement:

\[
\boxed{
u<h.
}
\]

No amount of tuning \(s_\delta\) can fix an architecture in which the
failure-amplifying share is at least the effective corrective share.

This is machine-checked in Lean.

For the shared-client JAM extension,

\[
h=(1-\gamma)(1-f).
\]

Thus implementation correlation changes not only the preferred escalation
strength but whether a feasible escalation interval exists at all.

---

### 6.3 JAM — behavior selection

For actual compute to dominate silent rubber-stamping,

\[
\boxed{
sW+bdL_F\ge c.
}
\]

This says:

> if costly verification is to persist as the selected behavior, enough return
> must pass through a sufficiently discriminating channel, after accounting for
> fault deterrence.

"Reciprocity" in human language is one possible realization.

The substrate-neutral function is **return-loop closure**.

---

### 6.4 Fungal redundant transport

For the two-route fungal-inspired reinforcement model,

\[
M
=
1-\delta+\delta\beta s.
\]

Equal redundant allocation is locally stable iff

\[
\boxed{
\beta s<1.
}
\]

So:

> if this redundant transport architecture is the property to be maintained,
> effective use-dependent positive-feedback gain must remain subunit.

The fungus is not "wrong" if it operates outside this region.

It may be maintaining another property such as low construction cost,
unidirectional transport or exploration.

The condition is indexed to the declared viability loop.

---

## 7. There is no single global ought

Experiment 7 remains essential.

Real networks maintain several properties simultaneously.

Let

\[
\mathbf M
=
(M_1,\ldots,M_k).
\]

A process can raise one margin and lower another.

For fungi, higher connectivity may increase robustness while increasing
construction cost.

For JAM, stronger escalation can improve the correction channel while reducing
the no-show scalability margin.

Therefore:

\[
\boxed{
\text{viability-conditioned oughts form a constraint region, not one scalar
commandment.}
}
\]

Conflicting constraints may have:

- a feasible intersection;
- a narrow boundary;
- or no simultaneous solution.

This is where trade-offs become structural rather than moral.

---

## 8. The deeper abstraction after the fungal test

The JAM analysis initially suggested the stack

\[
\text{state sensing}
\rightarrow
\text{maintenance}
\rightarrow
\text{maintenance sensing}
\rightarrow
\text{return}
\rightarrow
\text{capacity}.
\]

The fungal test compresses this.

Flow can simultaneously be:

- functional transport;
- a local signal of network role;
- an input to structural reinforcement.

So the more general loop is

\[
\boxed{
\text{network state}
\rightarrow
\text{function-sensitive local coupling}
\rightarrow
\text{structural/behavioral change}
\rightarrow
\text{future network state}.
}
\]

Explicit monitoring is only one implementation.

Explicit reward is only one implementation.

Autonomous individual agents are only one implementation.

The deeper object is the coupling.

---

## 9. A candidate cross-substrate maintenance decomposition

The current results suggest the following candidate functions.

### 9.1 Viability criterion

Some continuation property is defined, explicitly or implicitly.

### 9.2 Informative coupling

Local processes must receive information correlated with the network state or
with their functional role.

### 9.3 Corrective / reinforcing response

The local state changes future dynamics.

### 9.4 Return-loop closure

Processes that are costly or consumptive must receive enough resources,
persistence, reproduction or structural allocation to continue supplying their
function.

### 9.5 Diversity / independent correction

Some viability properties require non-correlated routes or models.

### 9.6 Capacity renewal

The ability to perform future maintenance must itself be replenished.

### 9.7 Recursive corrigibility

The maintenance architecture may itself need to change when its own response
becomes maladaptive.

These are candidate functions.

They are not yet asserted as necessary in all networks.

---

## 10. How human ethical vocabulary may enter

The present programme permits a precise but limited hypothesis.

Human terms such as

- honesty;
- accountability;
- reciprocity;
- forgiveness;
- humility;
- reinforcement;
- dissent;

may sometimes name socially/cognitively elaborate implementations of more
general maintenance functions.

For example:

\[
\text{honesty}
\leadsto
\text{signal fidelity},
\]

\[
\text{accountability}
\leadsto
\text{negative return on damaging action},
\]

\[
\text{reciprocity}
\leadsto
\text{return-loop closure},
\]

\[
\text{forgiveness}
\leadsto
\text{conditional edge repair}.
\]

But the mapping is not identity.

The fungal substrate is useful precisely because it shows the same kind of
function without moral cognition.

That makes the functional hypothesis more plausible while simultaneously
preventing anthropomorphic interpretation.

---

## 11. Relation to biological normativity

This programme overlaps directly with established work.

Di Paolo's adaptivity framework treats organisms as regulating themselves with
respect to conditions of viability, providing a route from self-maintenance to
organism-relative value and normativity.

Organizational accounts of biological autonomy similarly describe living
systems in terms of mutually maintaining constraints.

The present framework differs in emphasis:

1. it does not require the system to be alive;
2. it does not require an autonomous agent as the local unit;
3. it explicitly includes engineered protocols;
4. it decomposes decentralized maintenance into testable network processes;
5. it keeps multiple viability loops vector-valued;
6. it asks which maintenance functions survive cross-substrate falsification.

This may provide a bridge between viability theory, organizational biology,
distributed control and social normativity.

That bridge is a research programme, not yet an established field.

---

## 12. Why this matters for "ought before is"

A careful version of the idea is now:

\[
\boxed{
\text{VIABILITY-CONDITIONED OUGHT}
\rightarrow
\text{RELIABLE IS}
\rightarrow
\text{PRACTICAL OUGHT}
\rightarrow
\text{ACTION}.
}
\]

### Viability-conditioned ought

What must hold if a declared organization/property is to persist?

### Reliable is

What actually happens, with uncertainty and measurement error made explicit?

### Practical ought

If an agent or institution chooses to preserve that property, what action now
follows from the discrepancy?

### Action

Intervene, learn, repair, redesign—or revise the declared goal/model.

This ordering avoids deriving a categorical moral claim from a descriptive
fact.

But it also avoids the opposite error of treating all normative structure as
arbitrary.

Some conditional "oughts" are consequences of dynamics.

---

## 13. Strong falsifiers of the programme

The framework should be revised if cross-substrate work shows that:

1. persistent decentralized networks regularly maintain declared properties
   without any identifiable state/function-sensitive coupling;
2. maintenance processes persist despite systematic failure of all return or
   renewal paths;
3. network-level viability constraints cannot be related to local process
   constraints even probabilistically;
4. the proposed maintenance decomposition adds no predictive discrimination
   beyond existing viability/control descriptions;
5. human normative terms fail to map to maintenance functions in ways that
   generate independently testable predictions.

These are real failure modes.

---

## 14. Prior-art boundary

Do not claim novelty for:

- viability kernels or controlled invariance;
- self-maintenance-based biological normativity;
- autopoiesis or adaptivity;
- organizational closure;
- distributed multi-agent control;
- reputation/monitoring as cooperation mechanisms;
- adaptive fungal transport networks.

Potential contribution, if it survives further work:

\[
\boxed{
\text{a cross-substrate, vector-valued and recursively testable decomposition
of distributed maintenance processes that links viability constraints to local
network behavior.}
}
\]

That is the claim to test next.

---

## 15. Sources and neighboring traditions

- Aubin, J.-P. (1991/2009), *Viability Theory*.
- Aubin, J.-P., Bayen, A. M. & Saint-Pierre, P. (2011),
  *Viability Theory: New Directions*.
- Di Paolo, E. A. (2005), *Autopoiesis, adaptivity, teleology, agency*,
  Phenomenology and the Cognitive Sciences.
  DOI: 10.1007/s11097-005-9002-y.
- Moreno, A. & Mossio, M. (2015), *Biological Autonomy: A Philosophical and
  Theoretical Enquiry*.
- Bolton, D. & Sustar, P. (2022), *Regulation and the Normativity Problem*.
  DOI: 10.1080/02698595.2022.2149050.
- Cusimano, S. & Sterner, B. (2020), *The Objectivity of Organizational
  Functions*. Acta Biotheoretica.
  DOI: 10.1007/s10441-019-09365-9.
- The fungal and JAM sources listed in the corresponding grounding documents.
