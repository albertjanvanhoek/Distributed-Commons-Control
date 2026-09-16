# Experiment 9 — JAM as a falsification substrate for behavioral maintenance

## 1. Purpose

Experiment 8 proposed a substrate-neutral family of behavioral maintenance
operators:

1. sense;
2. correct;
3. reinforce;
4. repair or exit;
5. reproduce maintenance capacity;

with signal fidelity, resource return, and corrigibility as cross-cutting
conditions.

Experiment 9 asks a harder question:

> Does a real decentralized protocol actually instantiate these operators, and
> what happens when the grounded operators are perturbed?

JAM/ELVES is used because it supplies an explicit decentralized correction
architecture without moral vocabulary.

No ecological analogy is used in this experiment.

---

## 2. Provenance rule

Every JAM-facing statement retains the grounding tags:

- **[GP]** Gray Paper;
- **[ELVES]** Burdges et al. (2024);
- **[extension]** introduced here;
- **[delegated]** required function lies outside the audited JAM/ELVES layer;
- **[absent]** no mechanism was identified in the audited sources.

The neutral theory is not changed to fit JAM.

---

## 3. Operator audit

| Maintenance function | JAM / ELVES mechanism | Status in audited layer |
|---|---|---|
| sense state relevant to validity | selected validators reconstruct/re-execute and issue judgments/assurances | **implemented [GP]/[ELVES]** |
| compensate missing correction | announced no-show opens further audit tranches | **implemented [GP]/[ELVES]** |
| escalate detected error | one negative judgment obliges broad/full checking | **implemented [GP]** |
| preserve independent corrective channels | Gray Paper warns against one shared implementation; multiple clients reduce structural centralization | **recognized [GP], but not protocol-enforced** |
| accountability / suppress damaging action | culprits and contradictory judges are punishable | **implemented [GP], economic magnitude delegated** |
| reinforce demonstrated useful checking | auditing effort is not directly tracked; validators report impressions; rewards are external | **partially measured, reinforcement delegated** |
| return resources to maintenance process | chain itself issues no validator reward in the audited mechanism | **delegated to staking/economic layer** |
| repair/re-entry after a fault | no explicit repair operator identified in the audited assurance mechanism | **absent or delegated** |
| reproduce checking capacity | validator operation, spare compute and client implementation diversity must continue to exist | **delegated to operators/ecosystem** |
| revise the correction architecture itself | protocol/specification change is outside the ELVES assurance theorem | **outside audited layer** |

The first falsification is therefore immediate:

\[
\boxed{
\text{a viable decentralized maintenance architecture need not implement
every maintenance operator inside one protocol layer.}
}
\]

JAM is better represented as a **stack of maintenance loops** whose functions
are split across protocol, client, operator and staking layers.

This does not show that the delegated functions are optional at system level.

---

## 4. A grounded JAM viability vector

Two ELVES quantities already give distinct viability loops.

### 4.1 Safety certification

The economically derived ELVES target is

\[
\varepsilon_*=\frac{\nu}{n+\nu}.
\]

For the pessimistic branching bound \(P_{\rm bound}\), define

\[
\boxed{
M_{\rm safety}
=
\ln\frac{\varepsilon_*}{P_{\rm bound}}.
}
\]

Thus

\[
M_{\rm safety}>0
\]

means the bound certifies the economic target,

\[
M_{\rm safety}=0
\]

is the certification boundary, and negative values are not certified by this
bound.

This is a **certificate margin**, not an exact protocol failure probability.

### 4.2 Scalability / liveness of escalation

Let \(U/n\) be the population share contributing to the no-show/fault
reproduction term. Then

\[
A=s_\delta\frac{U}{n}.
\]

Define

\[
\boxed{
M_{\rm scale}=1-A.
}
\]

Positive values mean the ELVES no-show amplification remains subcritical.

The JAM viability object used here is therefore

\[
\boxed{
\mathbf M_{\rm JAM}
=
(M_{\rm safety},M_{\rm scale}).
}
\]

The two coordinates are deliberately **not added**. They have different
semantics and scales.

---

## 5. Individual maintenance contribution: one validator, fixed population

Write

- \(n\): total validator count;
- \(H\): otherwise-honest validators;
- \(B\): honest validators sharing a client failure for the crafted invalid report.

The shared-client extension can be rewritten exactly as

\[
\lambda_f
=
s_\delta\frac{H-B}{n}.
\]

### 5.1 Change one validator's client profile

Move one validator from the vulnerable client class to an
independent/correct implementation:

\[
B\rightarrow B-1.
\]

Then

\[
\boxed{
\Delta\lambda_f
=
\frac{s_\delta}{n}.
}
\]

The result is independent of the starting values of \(B\) and \(H\), provided
the fixed-population interpretation applies.

This is machine-checked in Lean.

For JAM's

\[
n=1023,\qquad s_\delta=2,
\]

one validator contributes

\[
\boxed{
\Delta\lambda_f
=
\frac2{1023}
\approx0.001955.
}
\]

This does **not** imply a constant change in the safety certificate because the
branching extinction map is nonlinear.

---

## 6. One validator can change certification status

Use an integer-count parameterization:

\[
n=1023,\qquad
H=818,\qquad
n-H=205.
\]

Take

\[
B=119
\]

honest validators on the vulnerable client profile.

With

\[
s_0=30,\quad
s_\delta=2,\quad
\nu=0.05,
\]

the pessimistic ELVES extension gives approximately

\[
M_{\rm safety}(B=119)
=
-0.01322.
\]

The target is not certified.

Move **one** validator to an independent/correct client:

\[
B=118.
\]

Then

\[
M_{\rm safety}(B=118)
=
+0.03495.
\]

So

\[
\boxed{
\text{one fixed-population profile change crosses the certification boundary.}
}
\]

Nothing magical happened to the absolute \(\Delta\lambda_f\); it remained
\(2/1023\).

What changed is the participant's importance **relative to the remaining
certificate margin**.

This is the precise form of the earlier intuition that diversity can become
decisive near a boundary.

---

## 7. Individual reliability contribution

Let \(U\) be the number of validators represented in the no-show/fault
amplification term:

\[
A=s_\delta\frac{U}{n}.
\]

Then

\[
M_{\rm scale}
=
1-s_\delta\frac{U}{n}.
\]

If one validator-equivalent is made reliable,

\[
U\rightarrow U-1,
\]

then

\[
\boxed{
\Delta M_{\rm scale}
=
\frac{s_\delta}{n}.
}
\]

For \(n=1023,s_\delta=2\),

\[
\Delta M_{\rm scale}\approx0.001955.
\]

This is also machine-checked.

The identical algebraic increment has a different meaning from
\(\Delta\lambda_f\):

- client-profile improvement increases effective corrective reproduction;
- reliability improvement creates more distance from no-show explosion.

This is exactly why contribution remains vector-valued.

---

## 8. Falsification: stronger correction is not globally "better"

Increase the escalation strength

\[
s_\delta\rightarrow s_\delta+d,
\qquad d>0.
\]

For correction reproduction,

\[
\Delta\lambda_f
=
d\frac{H-B}{n}>0.
\]

For the scalability margin,

\[
\Delta M_{\rm scale}
=
-d\frac{U}{n}<0
\]

when \(U>0\).

Therefore

\[
\boxed{
\Delta\mathbf M_{\rm escalation}
=
(+,-).
}
\]

Stronger compensatory correction has opposite signs on two grounded viability
loops.

This is not a generic toy result. It follows directly from the ELVES
supercritical-correction/subcritical-failure architecture.

The sign identities are machine-checked in Lean.

### Numerical JAM slice

Take

\[
n=1023,\ H=818,\ B=82,\ U=153,\ s_0=30,\ \nu=0.05.
\]

At

\[
s_\delta=2,
\]

the model gives approximately

\[
\lambda_f=1.43891,
\]

\[
M_{\rm safety}=1.74292,
\]

and

\[
M_{\rm scale}=0.70088.
\]

Increase escalation to the neighborhood of ELVES' reported optimum,

\[
s_\delta=2.08.
\]

Then

\[
\lambda_f=1.49646,
\]

\[
M_{\rm safety}=2.60309,
\]

but

\[
M_{\rm scale}=0.68891.
\]

The same protocol change therefore gives

\[
\boxed{
\Delta M_{\rm safety}>0,
\qquad
\Delta M_{\rm scale}<0.
}
\]

Experiment 7's warning is now instantiated in the chosen substrate: there is
no weight-free scalar statement that this change is simply "better."

---

## 9. Visible versus silent maintenance failure

The grounding pass exposed an asymmetry.

### Visible failure

An auditor that announced its obligation and then supplies no judgment is
observable.

The protocol responds:

\[
\text{no-show}
\rightarrow
\text{new tranche}
\rightarrow
\text{additional correction}.
\]

Its cost appears in the no-show reproduction/scalability channel.

### Silent failure

A validator whose implementation accepts the crafted invalid report can issue
a positive judgment. Unless another corrective channel contradicts it, this
does not itself trigger the no-show escalation mechanism.

In the shared-client extension it instead reduces

\[
\lambda_f.
\]

Thus the architecture distinguishes two failures with different vectors:

\[
\boxed{
\text{visible missing correction}
\neq
\text{silent wrong correction}.
}
\]

The first is compensated at a scalability cost.

The second attacks the fidelity/independence of the sensing-correction layer.

This supplies a substrate-specific reason that **observability and signal
fidelity are separate maintenance functions**.

---

## 10. What Experiment 8 survives JAM?

### Sense

**Survives strongly.**

Correction requires judgments that carry information about execution validity.
The shared-client extension shows why nominal participation without
independent signal fidelity may not provide equivalent maintenance.

### Correct

**Survives strongly but conditionally.**

JAM explicitly recruits more correction after visible failure, but the
\(s_\delta\) perturbation proves that stronger correction has a scalability
cost.

### Reinforce

**Not yet testable inside the audited layer.**

JAM core does not supply the complete economic reinforcement rule for auditing
effort. The peer impression mechanism exists, but the reward mapping is
external.

This operator is therefore **delegated**, not falsified.

### Repair

**Not identified inside the assurance mechanism.**

The absence of an explicit repair/re-entry operator falsifies a stronger claim
that every viable layer must internally repair damaged participants.

It does not establish that repair is unnecessary at the whole-system level.

### Reproduce maintenance capacity

**Delegated.**

JAM requires validators, compute and implementations to continue to exist, but
the assurance theorem does not itself reproduce those resources.

This is a direct real-world example of Experiment 8's return-loop distinction.

---

## 11. Revised maintenance architecture

The result is no longer well represented as a list of "virtues."

For JAM, the maintenance architecture is layered:

\[
\boxed{
\begin{array}{c}
\text{client implementations}
\\
\downarrow
\\
\text{validity sensing / execution}
\\
\downarrow
\\
\text{audit judgments}
\\
\downarrow
\\
\text{escalatory correction}
\\
\downarrow
\\
\text{protocol state}
\end{array}
}
\]

while other loops feed this architecture:

\[
\text{staking/economics}
\rightarrow
\text{validator participation},
\]

\[
\text{operator/client ecosystem}
\rightarrow
\text{implementation diversity and compute},
\]

and eventually

\[
\text{governance/development}
\rightarrow
\text{protocol/client revision}.
\]

The decentralized commons is therefore maintained by a **network of
maintenance processes**, some of which maintain other maintenance processes.

That recursive structure is a substrate-grounded observation worth carrying
back into the neutral theory.

---

## 12. Falsification ledger

| Hypothesis | JAM/ELVES result |
|---|---|
| Every maintenance operator must be inside one decentralized layer | **Falsified:** core assurance delegates reward, resource reproduction and revision |
| More compensatory correction is globally better | **Falsified:** increasing \(s_\delta\) improves safety/correction and worsens scalability margin |
| Every active validator contributes equally to corrective reliability | **Falsified in shared-client extension:** client profile changes effective independent correction |
| Diversity matters only through a vague redundancy benefit | **Falsified:** one-validator profile change has exact \(\Delta\lambda_f=s_\delta/n\) |
| A participant's absolute structural contribution necessarily diverges near criticality | **Falsified:** \(\Delta\lambda_f=s_\delta/n\) is constant; decisiveness can instead arise from small remaining certificate margin |
| Visible and silent correction failures are equivalent | **Falsified by architecture:** no-show invokes compensation; silent shared-client error acts through signal/correction fidelity |
| Reinforcement is implemented by the same mechanism as correction | **Not supported:** reinforcement economics are delegated |
| Repair is necessary inside every viable maintenance layer | **Not supported:** no explicit repair operator is required inside the audited assurance mechanism |

---

## 13. Tautology guard

This is a stronger substrate test than merely renaming protocol steps.

The discriminating predictions are numeric:

1. changing one client profile changes \(\lambda_f\) by \(s_\delta/n\);
2. the same change can cross the economic certification boundary for a
   specified count configuration;
3. changing one reliability count changes the scalability margin by
   \(s_\delta/n\);
4. changing escalation strength has a mixed-sign viability vector.

These predictions can be wrong under a more faithful JAM/ELVES mapping.

Therefore the operator language remains falsifiable.

---

## 14. Next test

The strongest remaining behavioral question is the one not yet grounded:

\[
\boxed{
\text{compute versus rubber-stamp versus no-show}.
}
\]

Before modelling its selection dynamics, the staking/reward, slashing and
peer-effort-vote mechanisms must be grounded sufficiently to determine what a
validator gains or loses from each action.

Until then, the current result should stand:

> JAM supports the existence of substrate-general maintenance functions, but
> it also falsifies the idea that these functions are necessarily co-located,
> uniformly beneficial, or reducible to one scalar contribution.
