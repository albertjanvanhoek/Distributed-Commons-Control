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

## First exact result: correlated capture floor

Let \(b\) be the probability that harmful work is attempted, \(q\) each monitor's detection effort, \(n\) the number of monitors and \(\rho\) the probability of a common-mode blind spot. The probability that harmful work escapes all monitors is

\[
E_n(q,\rho)=\rho+(1-\rho)(1-q)^n,
\]

so the harmful-finalization probability is \(P_{\mathrm{bad}}=bE_n(q,\rho)\). Even perfect individual effort leaves

\[
P_{\mathrm{bad}}(q=1)=b\rho.
\]

Therefore a safety target \(\varepsilon<b\rho\) is structurally unattainable by adding effort or same-mode monitors. The architecture must reduce correlated failure. This is the first clean sense in which **distribution of control is not the same as independence of control**.

## Repository map

| Path | Purpose |
|---|---|
| [`docs/MODEL.md`](docs/MODEL.md) | Assumptions, equations, phase boundaries and dynamic extension |
| [`docs/PHASE_BOUNDARY.md`](docs/PHASE_BOUNDARY.md) | Complete piecewise phase theorem and critical-cost boundary |
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

The same checks run in GitHub Actions.

## Complete phase boundary

In the non-trivial attainable region \(b\rho\le\varepsilon<b\), selected monitoring is sufficient exactly when

\[
\frac{b(1-\rho)r}{c}
\ge
1-\left(\frac{\varepsilon/b-\rho}{1-\rho}\right)^{1/n}.
\]

Equivalently, \(c\le c_{crit}=b(1-\rho)r/q_{suff}\). Increasing correlation therefore creates a double squeeze: it raises sufficient effort while lowering the private return to supplying it. The [full derivation](docs/PHASE_BOUNDARY.md) states all boundary cases.

## Scientific boundary

The current model proves conditional statements about a declared toy architecture. It does **not** establish that consensus equals truth about the external world, every persistent organism benefits its ecosystem, ecosystems optimize a global objective, JAM currently violates a safety or liveness requirement, or economic incentives alone guarantee protocol viability.

Those stronger statements require additional theory or evidence. The purpose of the repository is to make the boundary between result and interpretation inspectable.

## Relationship to Evolution by Emergence

This project is an out-of-domain test of the abstractions developed in [Evolution by Emergence](https://github.com/albertjanvanhoek/Evolution-by-Emergence), especially sufficient alignment, selected-versus-sufficient control and maintenance debt. Its contribution must be more than vocabulary transfer: the distributed-computation substrate must yield new, testable phase structure. The common-mode capture floor is the first such result.

## Licensing

Code and Lean sources are licensed under Apache-2.0. Research text and documentation are licensed under CC BY 4.0; see [`LICENSES.md`](LICENSES.md).
