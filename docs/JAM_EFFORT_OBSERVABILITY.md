# Experiment 11 — maintenance of maintenance: effort observability and return-loop closure

## 1. Why Experiment 10 is not the end

Experiment 10 showed that actual audit computation is privately selected
against rubber-stamping only if

\[
R_C-R_R+bdL_F\ge c.
\]

But the Gray Paper does not simply say "pay auditors more."

It proposes a second-order information channel: auditing effort cannot be
directly tracked on-chain, so validators may report their impression of other
validators' effort and a median may be used by a higher-level staking system.

That suggests a deeper maintenance question:

> Can the network observe maintenance well enough to selectively return value
> to the processes actually performing it?

Experiment 11 models exactly that interface.

---

## 2. Effective effort observability

Let

- \(s\in[0,1]\): effective discrimination/observability of actual computation
  versus cheap imitation;
- \(W\ge0\): maximum reward differential the higher layer can return when the
  effort signal successfully distinguishes real maintenance.

Then the expected compute reward advantage supplied by the effort channel is

\[
\boxed{
\Delta R_{CR}=sW.
}
\]

This is intentionally abstract.

The current Gray Paper prose describes peer impressions and median
oraclization, but its formal validator-statistics tuple does not yet close an
effort-score implementation. Therefore \(s\) is not claimed to be a known JAM
parameter.

It is the parameter that a completed effort-oracle/staking design would need
to determine.

---

## 3. Maintenance-selection margin

Combine the effort channel with Experiment 10's fault deterrence:

\[
\boxed{
\Phi
=
sW+bdL_F-c.
}
\]

Actual computation is selected against rubber-stamping when

\[
\boxed{\Phi\ge0.}
\]

For \(W>0\), the required effort observability is

\[
\boxed{
s_{\min}
=
\frac{c-bdL_F}{W}.
}
\]

This threshold is machine-checked in Lean.

It gives three regimes.

### 3.1 Penalty closes the gap alone

If

\[
c-bdL_F\le0,
\]

then

\[
s_{\min}\le0.
\]

No positive effort-reward signal is needed to make compute dominate
rubber-stamp in this simplified game.

### 3.2 Observability can close the remaining gap

If

\[
0<s_{\min}\le1,
\]

a sufficiently informative effort channel can make actual computation privately
selected.

### 3.3 The reward budget is insufficient

If

\[
s_{\min}>1,
\]

then even perfect discrimination cannot close the gap at the available reward
budget.

---

## 4. Falsification: reward without observability

Set

\[
s=0.
\]

Then

\[
\boxed{
\Phi=bdL_F-c,
}
\]

independent of \(W\).

Therefore:

> increasing a reward budget does nothing to select actual maintenance if the
> reward layer cannot distinguish maintenance from imitation.

This is machine-checked.

In human-language SCAP terms, "praise/reward" without a sufficiently faithful
signal can become non-selective reinforcement.

The functional principle is not "reward good behavior."

It is:

\[
\boxed{
\text{return value through a channel correlated with true contribution.}
}
\]

---

## 5. Falsification: observability without enough returned value

Suppose

\[
W+bdL_F<c.
\]

Even with

\[
s=1,
\]

we obtain

\[
\Phi<0.
\]

So perfect effort observability does not make maintenance self-sustaining when
the maximum available return is too small.

This gives a direct return-loop condition:

\[
\boxed{
\text{observable maintenance must receive enough return to cover its residual
private cost.}
}
\]

That is the substrate-neutral function underneath the SCAP term
"reciprocity."

---

## 6. Verifier-dilemma example as an observability threshold

Take

\[
c=1,\qquad
b=0.001,\qquad
d=1,\qquad
L_F=10,\qquad
W=2.
\]

Fault deterrence supplies only

\[
bdL_F=0.01.
\]

Therefore

\[
\boxed{
s_{\min}
=
\frac{0.99}{2}
=
0.495.
}
\]

The effort channel must recover almost half of the available reward
differential in expectation before actual compute weakly dominates
rubber-stamping.

By contrast, if the reward budget were only

\[
W=0.5,
\]

then

\[
s_{\min}=1.98>1.
\]

No feasible effort-observation fidelity can close the gap.

---

## 7. Structural correction and second-order observability interact

Experiment 10 used

\[
d_{\rm cert}=1-P_{\rm bound}
\]

as a conservative exposure lower bound under the declared ELVES extension.

Substitute this into the effort threshold:

\[
\boxed{
s_{\min}^{\rm cert}
=
\frac{
c-b(1-P_{\rm bound})L_F
}{W}.
}
\]

If structural correction weakens,

\[
P_{\rm bound}\uparrow,
\]

then

\[
s_{\min}^{\rm cert}\uparrow.
\]

This is machine-checked in the more general variable \(d\).

So the system contains a recursive coupling:

\[
\boxed{
\begin{array}{c}
\text{weaker structural correction}\\
\downarrow\\
\text{lower exposure of false judgments}\\
\downarrow\\
\text{weaker fault deterrence}\\
\downarrow\\
\text{greater effort-observability requirement}
\end{array}
}
\]

The maintenance process therefore depends on the reliability of the process
that observes maintenance.

---

## 8. Concrete JAM-extension contrast

Use the same fixed population as Experiments 9–10:

\[
n=1023,\qquad H=818.
\]

### Stronger correction architecture

Take

\[
B=82
\]

validators on the shared vulnerable client profile.

The pessimistic acceptance bound is very small, so

\[
d_{\rm cert}\approx1.
\]

With

\[
c=1,\quad
b=0.1,\quad
L_F=10,\quad
W=2,
\]

fault deterrence nearly closes the whole cost and the required effort
observability is near zero.

### Structurally collapsed correction

Take instead

\[
B=400.
\]

Then

\[
\lambda_f<1,
\]

so the pessimistic branching model has extinction probability one and supplies
no certified exposure:

\[
d_{\rm cert}=0.
\]

The same behavioral parameters now require

\[
\boxed{
s_{\min}=0.5.
}
\]

Nothing about the compute cost or reward budget changed.

Only the surrounding correction architecture did.

So the "virtue" of doing the work cannot be modeled independently from the
network that makes doing the work observable and consequential.

---

## 9. A second-order maintenance operator

Experiment 8 originally compressed the maintenance cycle to

\[
\text{sense}
\rightarrow
\text{correct/reinforce}
\rightarrow
\text{repair/exit}
\rightarrow
\text{revise}.
\]

JAM forces one more distinction.

The network may also need to **sense whether maintenance itself happened**.

Call this

\[
\boxed{
\text{maintenance observability}.
}
\]

The expanded cycle becomes

\[
\boxed{
\text{sense state}
\rightarrow
\text{perform maintenance}
\rightarrow
\text{sense maintenance}
\rightarrow
\text{return/suppress}
\rightarrow
\text{retain capacity}.
}
\]

This is genuinely recursive.

A process is maintaining the process that maintains the commons.

---

## 10. Relation to SCAP

Several human-language terms now separate functionally.

### Honesty / signal fidelity

Reliable information about the commons state.

### Accountability

Negative return when a judgment is proven incompatible with the final verdict.

### Recognition / praise

Positive return conditional on evidence that maintenance was actually supplied.

### Reciprocity

Enough return to the maintenance process to prevent its private extinction.

### Corrigibility

The observation/reward rule must itself remain revisable when it selects the
wrong behavior.

The important point is not that these are "really morality."

It is that JAM generates the same functional decomposition without moral
vocabulary.

---

## 11. Falsification ledger

| Hypothesis | Result |
|---|---|
| More reward is sufficient to select maintenance | **Falsified:** if \(s=0\), reward budget has no differential effect |
| Perfect effort observability is sufficient | **Falsified:** if \(W+bdL_F<c\), compute remains privately dominated |
| Effort observability is always required | **Falsified:** sufficiently strong fault deterrence can close the gap alone |
| Maintenance selection depends only on the individual's cost/reward | **Falsified in the extension:** structural correction changes exposure and therefore \(s_{\min}\) |
| Reinforcement can be modeled independently of evidence quality | **Falsified:** the effective returned value is \(sW\) |
| The maintenance architecture ends once a corrective act is specified | **Falsified conceptually by JAM:** maintenance behavior itself may need a monitoring/selection layer |

---

## 12. What remains grounded and what remains open

Grounded in the current Gray Paper:

- auditing requires real reconstruction/re-execution;
- audit completion/no-show is partly observable through announcements and
  judgments;
- faults can be recorded;
- chain rewards are delegated;
- auditing effort is not directly on-chain observable;
- peer impressions/median are proposed in prose as an effort-information path.

Still open:

- the completed formal effort-score representation;
- the staking mapping from effort score to economic return \(W\);
- actual empirical discrimination fidelity \(s\);
- fault-loss magnitude \(L_F\);
- audit compute cost \(c\);
- relevant invalid-report opportunity \(b\).

Experiment 11 therefore defines the interface those future mechanisms must
close, rather than pretending they are already specified.

---

## 13. Research consequence

JAM has now forced a refinement of the behavioral-maintenance hypothesis.

A decentralized commons does not merely require maintenance action.

For costly maintenance to persist, the architecture may require

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

Each term can fail separately.

That is now the strongest candidate abstraction to carry forward—but only as a
candidate until it survives another substrate.
