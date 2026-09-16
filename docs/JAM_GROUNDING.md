# JAM / ELVES grounding

This document is substrate-specific. It maps the neutral theory onto JAM only
where there is an explicit Gray Paper or ELVES referent.

Tags:
- **[GP]** stated in the Gray Paper;
- **[ELVES]** stated/proved in Burdges et al. (2024), ePrint 2024/961;
- **[extension]** derived here by modifying ELVES assumptions;
- **[absent]** not specified by those sources.

## 1. Economic safety target

ELVES Corollary 1 sets collateral per party to

\[
C=\nu M/n,
\]

where \(M\) bounds the adversary's gain from acceptance of an invalid block.
The rational-adversary soundness condition is

\[
\frac1\varepsilon>\frac n\nu+1.
\]

Therefore the strict upper boundary is

\[
\boxed{
\varepsilon_*=\frac{\nu}{n+\nu}.
}
\]

For \(n=1023\) and \(\nu=0.05\),

\[
\varepsilon_*=1/20461\approx4.887\times10^{-5}.
\]

Thus the neutral theory's probability threshold \(\varepsilon\) does have a
possible JAM referent, but it is economically derived rather than freely
chosen. The Gray Paper does not fix \(\nu\).

## 2. ELVES escalation as a branching process

[ELVES] Let \(s_0\) be expected initial committee size and \(s_\delta\) the
expected tranche size opened by a no-show. Under the pessimistic adaptive-crash
analysis, an honest tranche has Poisson mean

\[
\lambda=(1-\gamma)s_\delta,
\]

where \(\gamma<1/3\) bounds the adversarial share. The extinction probability
\(q\) solves

\[
q=e^{-\lambda(1-q)}.
\]

Security requires

\[
\boxed{\lambda>1}
\]

and the soundness failure probability is bounded by

\[
\boxed{
P_{\rm accept}\le q^{s_0/s_\delta}.
}
\]

For scalability, faulty/no-show-prone validators have reproduction number

\[
A=(\alpha+\beta)s_\delta,
\]

which must satisfy

\[
\boxed{A<1}.
\]

In the static bound, expected final committee size is at most

\[
\boxed{
s_f\le\frac{s_0}{1-A}.
}
\]

Together these imply

\[
\frac1{1-\gamma}<s_\delta<\frac1\gamma.
\]

At \(\gamma=1/3\), this is \(1.5<s_\delta<3\). ELVES reports an optimum near
2.0794; JAM uses \(F=s_\delta=2\).

## 3. JAM parameter check

Using \(s_0=30\), \(s_\delta=2\), \(n=1023\):

| adversarial share \(\gamma\) | \(\lambda\) | branching bound |
|---:|---:|---:|
| 1/3 | 1.333 | \(1.13\times10^{-4}\) |
| 0.20 | 1.600 | \(2.04\times10^{-7}\) |
| 0.10 | 1.800 | \(2.58\times10^{-9}\) |
| 0.05 | 1.900 | \(3.19\times10^{-10}\) |

At the worst-case boundary \(\gamma\to1/3\), the bound is above
\(\varepsilon_*\) for \(\nu=0.05\). The same expected-profit inequality would
require

\[
\nu_{\min}
=
\frac{nP}{1-P}
\approx0.1156
\]

when one collateral unit is lost.

If **two equal guarantor collaterals** are both lost, the analogous scenario
calculation halves this to about 0.0578. That two-collateral calculation is a
JAM mapping extension, not ELVES Corollary 1 itself.

## 4. Shared-client extension

ELVES assumes honest auditors who audit an invalid block detect it. Correlated
honest client failure is therefore outside the ELVES model.

**[extension]** Let \(f\) be the fraction of otherwise-honest validators whose
client accepts one particular crafted invalid report. The effective honest
branching mean becomes

\[
\boxed{
\lambda_f=(1-\gamma)(1-f)s_\delta.
}
\]

The same pessimistic extinction calculation then gives

\[
P_{\rm accept}(f)\le q_f^{s_0/s_\delta},
\qquad
q_f=e^{-\lambda_f(1-q_f)}.
\]

### 4.1 Structural criticality

Honest escalation ceases to be supercritical at

\[
\lambda_f=1,
\]

hence

\[
\boxed{
f_{\rm crit}
=
1-\frac1{(1-\gamma)s_\delta}.
}
\]

For JAM \(s_\delta=2\):

| \(\gamma\) | \(f_{\rm crit}\) |
|---:|---:|
| 1/3 | 0.250 |
| 0.20 | 0.375 |
| 0.05 | 0.474 |

This is a branching-process threshold, not a Gray Paper or ELVES theorem.

### 4.2 Client-share viability margin for a target epsilon

For a target \(\varepsilon\), define

\[
q_*=\varepsilon^{s_\delta/s_0}.
\]

The required branching mean is

\[
\lambda_*
=
-\frac{\ln q_*}{1-q_*}.
\]

Therefore the largest shared-client fraction **certified by this branching bound** is

\[
\boxed{
f_{\max}
=
1-
\frac{\lambda_*}{(1-\gamma)s_\delta},
}
\]

provided the target is already met at \(f=0\).

For JAM with \(\nu=0.05\), hence
\(\varepsilon_*=1/20461\):

- at \(\gamma=1/3\), the target is already missed at \(f=0\);
- at \(\gamma=0.20\), \(f_{\max}\approx0.1456\);
- at \(\gamma=0.05\), \(f_{\max}\approx0.2805\).

This is a JAM-native candidate **certified viability margin**: the largest shared-client fraction for which this pessimistic bound certifies the chosen target. It is not an exact protocol security frontier.

## 5. Collateral blind spot

[ELVES] The rational-adversary argument charges the attacker's/backer's
collateral when an invalid block is caught.

**[extension]** If a crafted bug causes otherwise-honest guarantors to sign the
invalid report, those guarantors may be the parties slashed. In that scenario
the specific ELVES expected-profit argument does not automatically assign the
collateral loss to the actor benefiting from the bug. This does **not** prove
that an attacker has zero total cost; it means Corollary 1 no longer supplies
that cost without an additional economic mapping.

The remaining protection is then the probability of detection/final rejection,
evaluated per exploitable bug.

## 6. Dispute-layer correlated-fault extension

The shared-client extension above concerns whether a negative judgment is found.
JAM has a second layer after detection: the Gray Paper dispute/verdict rules.

**[GP]** For a verdict validator-set size \(N\), define

\[
K=\left\lfloor\frac{2N}{3}\right\rfloor+1,
\qquad
W=\left\lfloor\frac{N}{3}\right\rfloor.
\]

Each verdict contains exactly \(K\) judgments. It is:

- good when all \(K\) are positive;
- bad when zero are positive;
- wonky when exactly \(W\) are positive.

Bad and wonky verdicts are non-positive and remove the report from the
availability path. The ordinary culprit/fault offense paths refer to good or
bad reports; a wonky report is recorded in the wonky set but does not, through
those rules, add guarantors or judges to the punish set. Whether an external
staking layer separately acts on a wonky record is **[absent]** from this
audited Gray Paper layer.

### 6.1 Exact verdict feasibility

Let \(P\) be the number of validators that would judge the crafted invalid
report as valid. Then a verdict of each type can be assembled iff:

\[
\boxed{\text{bad possible}\iff N-P\ge K,}
\]

\[
\boxed{\text{good possible}\iff P\ge K,}
\]

and

\[
\boxed{
\text{wonky possible}
\iff
P\ge W
\ \land\
N-P\ge K-W.
}
\]

For \(N=1023\),

\[
K=683,\qquad W=341,\qquad K-W=342.
\]

Hence bad is possible for \(P\le340\), wonky for
\(341\le P\le681\), and good for \(P\ge683\).

Under the literal three-count rule, \(P=682\) is a one-vote edge case for
which no 683-judgment subset has an allowed positive count. This is a
specification question, not a claimed protocol flaw.

### 6.2 Robust bad-verdict attribution under a shared fault

**[extension]** Let

- \(A\) validators be adversarial;
- \(B_x\) otherwise-honest validators share fault \(x\) and judge the invalid
  report as valid;
- \(C_x=N-A-B_x\) independently judge it as invalid.

If the adversary votes positive, the maximum positive population is
\(A+B_x\). A bad verdict remains constructible regardless of adversarial
voting iff

\[
\boxed{C_x\ge K.}
\]

Writing

\[
\gamma=A/N,
\qquad
f_x=B_x/(N-A),
\]

the maximum wrong-positive share is

\[
p_x=\gamma+(1-\gamma)f_x.
\]

For large \(N\), robust availability of the bad-verdict/offender-attribution
path therefore requires

\[
\boxed{
\gamma+(1-\gamma)f_x<\frac13.
}
\]

Equivalently,

\[
\boxed{
f_x<
\frac{1/3-\gamma}{1-\gamma}.
}
\]

At \(\gamma=0.20\), this is approximately

\[
f_x<1/6\approx0.167.
\]

This boundary binds before the \(F=2\) branching threshold
\(f_{\rm crit}=0.375\).

### 6.3 Three large-population boundaries for \(F=2\)

The same wrong-positive share \(p_x\) appears in three distinct conditions:

\[
\boxed{
\begin{array}{rcl}
p_x<1/3
&:&
\text{bad-verdict attribution robust to adversarial voting},
\\[2pt]
p_x<1/2
&:&
\text{fault-specific ELVES escalation supercritical for }F=2,
\\[2pt]
p_x<2/3
&:&
\text{false-good verdict not yet eligible}.
\end{array}}
\]

Thus attribution can disappear while audit escalation is still
supercritical.

### 6.4 Wonky is not the same as economic impunity

When the adversarial and buggy-positive bloc is large enough to prevent a bad
verdict but not large enough to form a good verdict, a wonky verdict may remain
constructible. The report is stopped, but the Gray Paper's ordinary
culprit/fault paths do not create offender records from that wonky verdict.

This does **not** establish that an attacker has zero total cost. A staking
subsystem could act on wonky records. The precise claim is only:

\[
\boxed{
\text{report rejection}
\neq
\text{ordinary offender attribution}.
}
\]

### 6.5 Offline extension

If \(o\) is a disjoint offline fraction and \(f_x\) is the buggy share among
the remaining non-adversarial online validators, the independently correct
online share is

\[
(1-\gamma-o)(1-f_x).
\]

Robust bad-verdict attribution requires

\[
\boxed{
(1-\gamma-o)(1-f_x)\ge K/N,
}
\]

approaching \(>2/3\) for large \(N\).

This is distinct from ELVES no-shows: a validator that never announces is not
the same event as an announced auditor failing to judge.

## 7. Relation to the neutral viability theory

The neutral Experiment 3 remains unchanged.

Its generic object is a declared viability margin \(M(S)\). A JAM
instantiation can now use, for example,

\[
M_{\rm client}
=
f_{\max},
\]

or a security-strength quantity such as

\[
-\ln P_{\rm accept}.
\]

A validator can affect at least two distinct JAM-native reproduction numbers:

1. **effective honest correction**, through implementation diversity and
   therefore \(\lambda_f\);
2. **fault/no-show amplification**, through reliability and therefore \(A\).

This already indicates that a faithful JAM contribution measure is
multi-component: safety and liveness/scalability need not move in the same
direction.

## 8. Candidate grounded feedback loop

ELVES treats \(\alpha\) and \(\beta\) as exogenous adversarial budgets.
A later **[extension]** may ask what happens if ordinary load also causes
otherwise-honest validators to become no-shows.

Then \(A\) becomes state-dependent and the static committee-size relation

\[
s_f=\frac{s_0}{1-A}
\]

becomes an implicit feedback equation

\[
\boxed{
s_f=\frac{s_0}{1-A(s_f)}.
}
\]

Multiple solutions are possible only if a specified load-to-no-show response is
strong enough. This is a grounded candidate for revisiting the generic
closed-loop/fold mathematics, but no JAM fold is claimed yet.

A second channel is non-announcement under overload. Because escalation is
triggered by announced auditors that fail to judge, failure to announce can
shrink effective committee size without opening a compensating tranche.

## Sources

- Gavin Wood, *JAM: Join-Accumulate Machine*, Gray Paper draft 0.8.0,
  3 June 2026.
- Jeff Burdges et al., *Efficient Execution Auditing for Blockchains under
  Byzantine Assumptions*, IACR ePrint 2024/961, 14 June 2024.
