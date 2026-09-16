# Mapping the neutral theory to JAM

## Boundary of the mapping

JAM is a substrate-specific test case, not the ontology of the theory. Neutral
results about participants, networks, viability margins, structural coverage
and selected behavior stand independently of any JAM interpretation.

For JAM-facing work, every primitive is tagged by provenance:
- **[GP]** Gray Paper;
- **[ELVES]** Burdges et al. (2024), ePrint 2024/961;
- **[extension]** introduced in this repository;
- **[absent]** not specified by those sources.

See [JAM / ELVES grounding](JAM_GROUNDING.md) for derivations and numerical
checks.

## Grounded correspondences

| Neutral object | JAM-facing referent | Status |
|---|---|---|
| participant | validator in a declared role | [GP] |
| harmful proposal | invalid work-report | [GP] |
| checking action | reconstruct / re-execute / judge | [GP] |
| initial checking set | private VRF-selected auditing committee | [GP]/[ELVES] |
| visible missing correction | announced auditor with no judgment | [GP]/[ELVES] |
| protocol compensation | new tranches; full audit after a negative judgment | [GP]/[ELVES] |
| failure cause | implementation, operator, Byzantine or crash-able status | implementation/operator [GP]; Byzantine/crash [ELVES] |
| safety threshold | economically derived invalid-acceptance probability target | [ELVES] |
| liveness threshold | at least two-thirds plus one live | [GP] |

## ELVES economic target

With collateral \(C=\nu M/n\), ELVES requires

\[
\frac1\varepsilon>\frac n\nu+1,
\]

so the strict boundary is

\[
\boxed{\varepsilon_*=\frac{\nu}{n+\nu}}.
\]

For \(n=1023\) and illustrative \(\nu=0.05\),
\(\varepsilon_*=1/20461\). The Gray Paper does not fix \(\nu\).

## ELVES escalation

The pessimistic adaptive-crash analysis has honest reproduction number

\[
\lambda=(1-\gamma)s_\delta,
\]

with security requiring \(\lambda>1\). If \(q\) solves

\[
q=e^{-\lambda(1-q)},
\]

then

\[
P_{\rm accept}\le q^{s_0/s_\delta}.
\]

Fault/no-show amplification is

\[
A=(\alpha+\beta)s_\delta,
\]

and scalability requires \(A<1\), with static bound

\[
s_f\le\frac{s_0}{1-A}.
\]

This is the JAM-native escalation structure.

## What is not grounded

The earlier private monitor objective
\(b(1-\rho)rq-cq^2/2\) and its selected-effort theorem remain valid abstract
model results. They are not JAM's auditing incentive rule.

Experiment 2's closure \(r(X)\propto X\) likewise remains a generic
distributed-commons mechanism study; it has no Gray Paper referent.

## Shared-client extension

ELVES assumes honest auditors detect invalid blocks. Correlated honest client
failure is outside its model.

**[extension]** Let \(f\) be the share of otherwise-honest validators whose
client accepts one crafted invalid report. Then

\[
\lambda_f=(1-\gamma)(1-f)s_\delta.
\]

The structural supercriticality boundary is

\[
f_{\rm crit}=1-\frac1{(1-\gamma)s_\delta}.
\]

For JAM \(s_\delta=2\), this is 0.25 at \(\gamma=1/3\).

For a target \(\varepsilon\), the branching equation can be inverted to define
the largest tolerable client share \(f_{\max}\). This is a natural JAM
instantiation of the neutral viability-margin idea.

## Behavior still needing grounding

A more plausible JAM action set than continuous rewarded effort is:
- compute;
- issue a judgment without full re-execution ("rubber-stamp");
- no-show after announcement.

Only no-shows are explicitly compensated by the escalation rule. Whether
rubber-stamping is strategically relevant depends on staking reward, slashing
and peer-effort-vote details not yet fully grounded.

No selected-behavior JAM theorem is claimed until those details are supplied.

## Commons interpretation

The shared object is protocol-valid state plus the architecture capable of
maintaining it. A faithful JAM contribution measure will likely be
multi-component,

\[
\mathbf M=(M_{\rm safety},M_{\rm liveness/scalability},\ldots),
\]

because correlated outages can preserve eventual safety while increasing
latency or checking load.

## Sources

- Gavin Wood, *JAM: Join-Accumulate Machine*, Gray Paper draft 0.8.0,
  3 June 2026.
- Jeff Burdges et al., *Efficient Execution Auditing for Blockchains under
  Byzantine Assumptions*, IACR ePrint 2024/961, 14 June 2024.


## Behavioral maintenance operator audit

Experiment 9 returns the neutral maintenance-operator framework to JAM without
changing the neutral definitions.

See [JAM maintenance operators](JAM_MAINTENANCE_OPERATORS.md).

The audited assurance layer implements validity sensing and compensatory
correction directly. Other functions are split across layers: auditing
reinforcement/funding is delegated to staking/economic mechanisms; validator
and client capacity are maintained by operators and the implementation
ecosystem; protocol revision lies outside the ELVES assurance theorem.

The resulting JAM viability vector keeps at least two components separate:

[
mathbf M_{m JAM}
=
(M_{m safety},M_{m scale}),
]

where (M_{m safety}) is a log certificate margin against the economically
derived ELVES target and (M_{m scale}=1-A) is distance from no-show
criticality.

Increasing escalation strength improves the first correction channel while
reducing the second margin when no-show-prone validators exist. The repository
therefore does not assign a scalar global sign to "more correction."


## Audit behavior selection boundary

Experiment 10 does not assign a made-up reward function to JAM auditing.

The core protocol identifies compute obligations, visible no-shows, judgments
and faults, while the staking layer determines the economic reward/punishment
magnitudes. The resulting partial-identification conditions are

[
R_C-R_R+bdL_Fge c
]

for compute to dominate rubber-stamping, and

[
R_C-R_Nge c
]

for compute to dominate no-show.

See [JAM behavior selection](JAM_BEHAVIOR_SELECTION.md). The unresolved
quantities are now explicit design inputs rather than hidden assumptions.


## Maintenance observability

Experiment 11 adds a second-order interface required by the Gray Paper's
delegation of audit incentives.

If (s) is the effective ability of the effort-information channel to
distinguish actual computation from imitation and (W) is the available reward
differential, then compute-selection against rubber-stamping requires

[
sW+bdL_Fge c.
]

The current specification does not provide numeric (s) or (W). The model
therefore treats them as explicit higher-layer design inputs rather than JAM
constants. See [JAM effort observability](JAM_EFFORT_OBSERVABILITY.md).
