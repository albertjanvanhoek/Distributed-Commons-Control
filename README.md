# Distributed Commons Control

**How can a network maintain shared state without requiring a central controller or perfectly reliable nodes?**

This repository develops a minimal, executable and formally checked theory of distributed control of a commons. Here a **commons** is not assumed to be external truth or a morally good resource. It is a jointly produced or maintained state whose condition changes the future capabilities of multiple participants.

The initial test case is a small computation protocol:

\[
\text{producer} \longrightarrow \text{distributed monitors} \longrightarrow \text{commit to shared state}.
\]

A producer can obtain a local benefit from proposing harmful work. Monitoring is costly. Monitors can fail independently or through a correlated blind spot. The network declares a maximum acceptable probability of harmful finalization. This lets us distinguish:

\[
\boxed{\text{locally selected control} \neq \text{control sufficient for the commons}}.
\]

The project was prompted by the architecture of the [Join-Accumulate Machine (JAM)](https://graypaper.com/) and by the broader *Evolution by Emergence* programme. It is not an implementation, security audit or official analysis of JAM. JAM is used first as an engineered system in which proposal, checking, availability and commitment are explicit enough to study. Ecological interpretations are treated as hypotheses to be earned after the generic model works.

## Baseline exact result: correlated capture floor

Let \(b\) be the probability that harmful work is attempted, \(q\) each monitor's detection effort, \(n\) the number of monitors and \(\rho\) the probability of a common-mode blind spot. The probability that harmful work escapes all monitors is

\[
E_n(q,\rho)=\rho+(1-\rho)(1-q)^n,
\]

so the harmful-finalization probability is \(P_{\mathrm{bad}}=bE_n(q,\rho)\). Even perfect individual effort leaves

\[
P_{\mathrm{bad}}(q=1)=b\rho.
\]

Therefore a safety target \(\varepsilon<b\rho\) is structurally unattainable by adding effort or same-mode monitors. The architecture must reduce correlated failure. This is a useful calibration of the model, not a novelty claim: common-cause limits on redundancy are established in reliability engineering and in work on dependent failures in multiversion software. See [the prior-art boundary](docs/PRIOR_ART.md).

The first coupled extension goes one step further. Because the common-mode branch also caps collective detection at \(1-\rho\), the adaptive producer response cannot drive the harmful-attempt target below

\[
m(\rho)=\sigma\!\left(\frac{g-\ell(1-\rho)}{T}\right).
\]

For producer adjustment \(0<\alpha_b\le1\),

\[
\boxed{b_t\ge m+(1-\alpha_b)^t(b_0-m)}
\]

and hence \(\liminf P_{\mathrm{bad},t}\ge\rho m\). This turns the static floor into an **endogenous floor**: common-mode weakness changes the producer response that determines the floor itself. The finite-time theorem is machine-checked in `formalization/EndogenousFloor.lean`.

## Repository map

| Path | Purpose |
|---|---|
| [`docs/MODEL.md`](docs/MODEL.md) | Assumptions, equations, phase boundaries and dynamic extension |
| [`docs/PHASE_BOUNDARY.md`](docs/PHASE_BOUNDARY.md) | Complete piecewise phase theorem and critical-cost boundary |
| [`docs/PRIOR_ART.md`](docs/PRIOR_ART.md) | Prior-art calibration and current novelty boundary |
| [`docs/CLOSED_LOOP.md`](docs/CLOSED_LOOP.md) | Experiment 2: closed commons loop, folds, hysteresis and recovery basins |
| [`docs/VIABILITY_CONTRIBUTION.md`](docs/VIABILITY_CONTRIBUTION.md) | Experiment 3: neutral participant contribution to a declared viability margin |
| [`docs/SELECTED_VIABILITY.md`](docs/SELECTED_VIABILITY.md) | Experiment 4: direct-positive but selected-negative participant contribution |
| [`docs/CORRECTIVE_CAPACITY.md`](docs/CORRECTIVE_CAPACITY.md) | Experiment 5: current shared state versus slow corrective capacity |
| [`docs/STATE_DEPENDENT_CONTRIBUTION.md`](docs/STATE_DEPENDENT_CONTRIBUTION.md) | Experiment 6: participant contribution to access of stored capacity |
| [`docs/VECTOR_CONTRIBUTION.md`](docs/VECTOR_CONTRIBUTION.md) | Experiment 7: vector-valued contribution across viability loops |
| [`CLAIMS.md`](CLAIMS.md) | Claim ledger separating proofs, computations and hypotheses |
| [`src/distributed_commons/`](src/distributed_commons/) | Dependency-free executable model |
| [`scripts/run_experiment.py`](scripts/run_experiment.py) | Reproducible parameter sweep |
| [`tests/`](tests/) | Numerical and behavioral tests |
| [`formalization/`](formalization/) | Lean 4 formalization and proof map |
| [`docs/JAM_MAPPING.md`](docs/JAM_MAPPING.md) | Restricted mapping from the generic model to JAM concepts |
| [`docs/ECOLOGY_MAPPING.md`](docs/ECOLOGY_MAPPING.md) | Ecological translation and its inferential limits |
| [`docs/ROADMAP.md`](docs/ROADMAP.md) | Staged research programme |

## Run the model

Python 3.10 or later is sufficient; the model has no runtime dependencies.

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python scripts/run_experiment.py --output results/phase_sweep.csv
python scripts/phase_boundary.py --output results/static_phase_boundary.csv
```

To compile the formalization:

```bash
cd formalization
lake update
lake exe cache get
lake build
```

The same checks run in GitHub Actions. The real-root formula is now connected end-to-end to actual safety by `RootSafety.lean`, including construction, uniqueness and leastness; see the [verification record](formalization/VERIFICATION.md).

## Complete phase boundary

In the non-trivial attainable region \(b\rho\le\varepsilon<b\), selected monitoring is sufficient exactly when

\[
\frac{b(1-\rho)r}{c}
\ge
1-\left(\frac{\varepsilon/b-\rho}{1-\rho}\right)^{1/n}.
\]

Equivalently, \(c\le c_{crit}=b(1-\rho)r/q_{suff}\). Increasing correlation therefore creates a double squeeze: it raises sufficient effort while lowering the private return to supplying it. The [full derivation](docs/PHASE_BOUNDARY.md) states all boundary cases.

## Closed-loop commons control

The next experiment closes the return path that was missing from the original adaptive model: commons condition now changes future control. Under commons-funded monitoring, the reduced equilibrium branch develops a fold and a coexistence region with both a healthy attractor and the clipped collapsed state. The same topology also appears in two alternative closures where degradation raises checking cost or capture gain.

For the declared discrete-time linear-regeneration map, the local equilibrium multiplier can be written

\[
M=1-\gamma+\gamma\eta,
\qquad
\eta=-(1-X)\frac{d\ln P^*}{dX},
\]

so local linear stability is equivalent to \(\eta<1\). The algebraic equivalence is machine-checked in `formalization/ClosedLoopStability.lean`; concrete fold locations remain numerical. See [Experiment 2](docs/CLOSED_LOOP.md).

## Participant contribution to viability

Experiment 3 moves from anonymous same-mode monitors to heterogeneous
participants with different failure profiles. For a coalition (S), define
(pi(S)) as the probability that every participant is disabled, and define
the viability margin

[
M(S)=sup{bin[0,1]:bpi(S)learepsilon}.
]

The first exact example has two participants sharing failure cause (A) and a
third participant vulnerable only to independent cause (B). Adding the third
participant changes structural escape from (ho) to (ho^2), and in the
uncapped regime multiplies the viability margin by (1/ho). At
(ho=0.05), that is a twentyfold increase.

The model is deliberately substrate-neutral. Leave-one-out contribution,
Shapley attribution and higher-order interaction terms are all computed from
the same declared margin; no participant is assigned a globally positive or
negative role. See [Experiment 3](docs/VIABILITY_CONTRIBUTION.md).

## Scientific boundary

The current model proves conditional statements about a declared toy architecture. It does **not** establish that consensus equals truth about the external world, every persistent organism benefits its ecosystem, ecosystems optimize a global objective, JAM currently violates a safety or liveness requirement, or economic incentives alone guarantee protocol viability.

Those stronger statements require additional theory or evidence. The purpose of the repository is to make the boundary between result and interpretation inspectable.

## Relationship to Evolution by Emergence

This project is an out-of-domain test of the abstractions developed in [Evolution by Emergence](https://github.com/albertjanvanhoek/Evolution-by-Emergence), especially sufficient alignment, selected-versus-sufficient control and maintenance debt. Its contribution must be more than vocabulary transfer: the distributed-computation substrate must yield new, testable phase structure. The common-mode capture floor is treated as a known calibration result; the endogenous producer-floor result is the first coupled phase constraint produced by the adaptive model. The repository does not yet claim literature priority for that theorem.

## Licensing

Code and Lean sources are licensed under Apache-2.0. Research text and documentation are licensed under CC BY 4.0; see [`LICENSES.md`](LICENSES.md).
