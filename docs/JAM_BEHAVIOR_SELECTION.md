# Experiment 10 — partially identified JAM audit behavior selection

## 1. Why this experiment is only partially identified

Experiment 9 showed that JAM/ELVES contains concrete maintenance operators and
that their effects are vector-valued.

The next behavioral question is narrower:

> Once a validator has announced an audit, what makes it actually compute
> rather than rubber-stamp a positive judgment or simply fail to complete?

The current Gray Paper does **not** close this game numerically.

At the official Gray Paper source revision checked for this experiment
(gavofyork/graypaper, commit e5375148597a45a99d31c9aa6bce6c7bf3a48998):

- the chain explicitly states that it does not itself issue validator rewards;
- reward handling is delegated to the staking subsystem;
- auditing activity is not directly observable on-chain;
- prose says validators may vote on their impression of each other's audit
  effort and a median may be used as an oracle;
- the formal per-validator statistics tuple contains six objective counters;
  the audit-announcement statistic is currently commented out;
- culprits and faults are recorded so that a higher-level system can punish
  offending validators.

Therefore a fully numeric private-utility model for audit behavior would require
inventing external staking parameters.

Experiment 10 does not do that.

Instead it derives the **exact incentive inequalities that the delegated layer
must satisfy**.

---

## 2. Three behavioral actions after an audit announcement

The action set is:

### Compute \(C\)

Fetch/reconstruct the data, re-execute the relevant computation and issue the
judgment implied by the result.

### Rubber-stamp \(R\)

Issue a positive judgment without paying the full computation/re-execution
cost.

This is a model extension: the Gray Paper specifies what validators should do,
not that validators actually choose this deviation.

### No-show \(N\)

Fail to supply the announced judgment.

This failure is explicitly visible and participates in the tranche-escalation
mechanism.

---

## 3. Partially identified payoffs

Let

- \(c>0\): private cost of doing the actual audit computation;
- \(R_C\): expected higher-layer reward/effort-score value for compute;
- \(R_R\): expected value for rubber-stamp;
- \(R_N\): expected value for no-show;
- \(b\): probability/opportunity rate that the audited report is invalid;
- \(d\): probability a false positive judgment is exposed and ultimately
  contradicted by the verdict;
- \(L_F\): higher-layer loss from being recorded/punished as a fault.

Then

\[
\boxed{U_C=R_C-c}
\]

\[
\boxed{U_R=R_R-bdL_F}
\]

and

\[
\boxed{U_N=R_N.}
\]

The Gray Paper fixes the existence and observability structure of several terms,
but not the numerical values of the reward and punishment magnitudes.

---

## 4. Exact compute-selection conditions

Compute weakly dominates rubber-stamping iff

\[
\boxed{R_C-R_R+bdL_F\ge c.}
\]

Equivalently,

\[
\boxed{R_C-R_R\ge c-bdL_F.}
\]

Compute weakly dominates no-show iff

\[
\boxed{R_C-R_N\ge c.}
\]

Therefore actual computation is privately selected only if **both** incentive
gaps are closed.

These equivalences are machine-checked in Lean.

---

## 5. The delegated staking layer has a measurable design obligation

Define

\[
\Delta R_{CR}=R_C-R_R
\]

and

\[
\Delta R_{CN}=R_C-R_N.
\]

Then the minimum required differentials are

\[
\boxed{\Delta R_{CR}^{\min}=c-bdL_F}
\]

and

\[
\boxed{\Delta R_{CN}^{\min}=c.}
\]

So JAM core alone does not solve the behavioral-selection problem.

It creates the observations and fault records from which an external layer can
solve it.

The maintenance architecture is therefore genuinely cross-layer:

\[
\boxed{
\text{core correction architecture}
+
\text{external selection/incentive architecture}.
}
\]

---

## 6. Low invalid-report frequency recreates the verifier's dilemma

Even a severe fault punishment contributes little expected deterrence when the
audited report is almost always valid.

For example,

\[
c=1,\quad b=0.001,\quad d=1,\quad L_F=10
\]

gives

\[
bdL_F=0.01
\]

and therefore

\[
\boxed{\Delta R_{CR}^{\min}=0.99.}
\]

Almost the full compute cost must still be covered by a reward/effort
differential.

Thus fault punishment by itself does not generally solve under-computation when
invalid reports are rare.

---

## 7. Structural correction and behavioral selection are coupled

The shared-client extension gives a pessimistic upper bound

\[
P_{\rm accept}\le P_{\rm bound}.
\]

Within the declared attack model, rejection/exposure is therefore at least

\[
\boxed{d_{\rm cert}=1-P_{\rm bound}.}
\]

Using this lower bound yields the conservative sufficient condition

\[
\boxed{
R_C-R_R
\ge
c-b(1-P_{\rm bound})L_F.
}
\]

If structural correction weakens,

\[
P_{\rm bound}\uparrow
\]

so

\[
d_{\rm cert}\downarrow
\]

and consequently

\[
\boxed{\Delta R_{CR}^{\min}\uparrow.}
\]

So a common-mode structural failure has two effects:

1. it weakens the network's ability to catch the invalid report;
2. it weakens the expected private deterrence against issuing a false positive.

The second effect is machine-checked algebraically as monotonicity in \(d\).

This is a new cross-layer squeeze:

\[
\boxed{
\text{weaker correction architecture}
\rightarrow
\text{weaker exposure}
\rightarrow
\text{weaker incentive to compute}.
}
\]

---

## 8. Visible no-show versus silent rubber-stamp

### No-show

The protocol sees

\[
\text{announcement without judgment}.
\]

That directly recruits compensatory auditing.

But the core protocol does not specify the private reward loss associated with
the no-show; that is delegated.

### Rubber-stamp

The protocol sees a judgment.

On valid reports it is observationally indistinguishable from a genuine audit
at the protocol-validity layer.

On invalid reports it becomes punishable only if independent correction
eventually produces the contradictory verdict.

Rubber-stamp dominates no-show iff

\[
\boxed{R_R-R_N\ge bdL_F.}
\]

When \(b\) is small, even a modest no-show penalty can make silent
rubber-stamping the preferred deviation.

This is the precise behavioral reason observability matters.

---

## 9. Falsification results

| Hypothesis | Result |
|---|---|
| JAM core fully determines auditor incentives | **Falsified:** reward and punishment magnitudes are delegated |
| A recorded fault penalty is automatically enough to select actual computation | **Falsified:** compute requires \(R_C-R_R+bdL_F\ge c\) |
| Very severe punishment always solves the verifier dilemma | **Falsified:** expected deterrence is scaled by invalid-report opportunity \(b\) and exposure \(d\) |
| Visible no-show and silent under-computation are behaviorally equivalent | **Falsified:** their observability and penalty channels differ |
| Structural safety and behavioral incentive are independent layers | **Falsified in the extension:** lower exposure raises the reward differential required for compute |
| A numerical JAM audit-effort equilibrium can be derived from the Gray Paper alone | **Not supported:** external staking/payoff parameters are missing |

---

## 10. What would close the model empirically

A fully grounded selection model needs:

1. the staking rule mapping validator activity/effort information to reward;
2. the economic loss associated with a recorded fault;
3. the economic consequence of an announced no-show or poor effort score;
4. an estimate/model for actual audit computation cost \(c\);
5. the relevant invalid-report opportunity rate \(b\);
6. how reliably the peer-impression mechanism distinguishes real audit effort
   from cheap imitation.

Once supplied, Experiment 10 becomes a closed game rather than a
partially-identified design boundary.

---

## 11. Consequence for behavioral maintenance theory

This substrate test adds an important refinement to Experiment 8.

A maintenance operator has at least three distinct requirements:

\[
\boxed{
\text{capacity}
+
\text{observability}
+
\text{selection}.
}
\]

It is not enough that a participant **can** perform correction.

The network must:

1. make the relevant state sufficiently observable;
2. make actual corrective behavior distinguishable enough from cheap
   imitation;
3. close the private incentive gap sufficiently that the corrective behavior
   persists.

That yields a stronger maintenance cycle:

\[
\boxed{
\text{sense}
\rightarrow
\text{act}
\rightarrow
\text{verify the action}
\rightarrow
\text{reinforce/suppress}
\rightarrow
\text{maintain capacity}.
}
\]

JAM's assurance system implements much of the first two steps.

The staking/effort layer is responsible for closing the selection loop.

That cross-layer interface is now the most important unresolved behavioral
part of the JAM case.
