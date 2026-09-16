# Claim ledger

This ledger prevents mathematical results, simulation behavior and cross-domain interpretations from being reported as the same kind of evidence.

| ID | Claim | Status | Evidence |
|---|---|---|---|
| C1 | In the declared common-mode mixture, conditional escape is \(E_n=\rho+(1-\rho)(1-q)^n\). | Model definition | `model.py`; `DistributedCommons.lean` for \(n=3\) |
| C2 | For every positive monitor count, perfect effort leaves harmful-finalization probability \(b\rho\). | Exact theorem | Lean: `badFinalizationN_perfect` |
| C3 | For arbitrary monitor count and admissible effort, \(b\rho\) is a lower bound on harmful finalization. | Exact theorem | Lean: `badFinalizationN_correlation_floor` |
| C4 | For arbitrary monitor count, a target \(\varepsilon<b\rho\) is unattainable within this architecture. | Exact theorem | Lean: `safety_impossible_below_correlation_floor_N` |
| C5 | When the target is attainable, the minimum symmetric effort is \(1-((\varepsilon/b-\rho)/(1-\rho))^{1/n}\). | Exact algebra implemented and numerically tested; general real-root proof not yet in Lean | `sufficient_effort`; unit tests |
| C6 | With private objective \(b(1-\rho)rq-cq^2/2\), selected effort is \(b(1-\rho)r/c\) before clipping to the feasible interval. | Exact theorem for the unconstrained quadratic | Lean: `selectedEffort_global_max` |
| C7 | Selected monitoring meets a declared effort requirement iff \(cq_{req}\le b(1-\rho)r\), for \(c>0\). | Exact theorem | Lean: `selectedEffort_meets_requirement_iff` |
| C8 | Higher common-mode correlation can produce lower long-run commons health in the declared adaptive simulation. | Computational result, parameter dependent | Parameter sweep and tests |
| C9 | Verification debt can precede visible commons collapse. | Hypothesis instantiated by one bookkeeping definition | Dynamic model; requires robustness analysis |
| C10 | JAM can be analyzed as distributed maintenance of protocol-valid shared state. | Structural interpretation | `docs/JAM_MAPPING.md` |
| C11 | Ecological roles can sometimes be represented as positions in distributed feedback loops. | Research hypothesis, not established here | `docs/ECOLOGY_MAPPING.md` |
| C12 | In the non-trivial attainable region, clipped selected effort is sufficient iff \(c\le b(1-\rho)r/q_{suff}\). | Exact theorem | Python classifier; Lean: `feasibleSelectedEffort_meets_iff_cost_le_critical` |
| C13 | Correlation simultaneously raises required effort and lowers detection-contingent private return in the declared model. | Exact comparative result from the model equations; numerically tested | `docs/PHASE_BOUNDARY.md`; `test_correlation_double_squeeze` |

## Explicit non-claims

This repository does not claim that consensus establishes external truth, that every species performs a net ecosystem service, that all persistent networks are cooperative, or that the present toy model constitutes a security analysis of JAM.
