# Claim ledger

This ledger prevents mathematical results, simulation behavior and cross-domain interpretations from being reported as the same kind of evidence.

| ID | Claim | Status | Evidence |
|---|---|---|---|
| C1 | In the declared common-mode mixture, conditional escape is \(E_n=\rho+(1-\rho)(1-q)^n\). | Model definition | `model.py`; `DistributedCommons.lean` for arbitrary n |
| C2 | For every positive monitor count, perfect effort leaves harmful-finalization probability \(b\rho\). | Exact theorem | Lean: `badFinalizationN_perfect` |
| C3 | For arbitrary monitor count and admissible effort, \(b\rho\) is a lower bound on harmful finalization. | Exact theorem | Lean: `badFinalizationN_correlation_floor` |
| C4 | For arbitrary monitor count, a target \(\varepsilon<b\rho\) is unattainable within this architecture. | Exact theorem | Lean: `safety_impossible_below_correlation_floor_N` |
| C5 | When the target is attainable, the minimum symmetric effort is \(1-((\varepsilon/b-\rho)/(1-\rho))^{1/n}\). | Exact real-root theorem; machine checked | Lean: `safety_iff_sufficientEffortN`; Python regression tests |
| C6 | With private objective \(b(1-\rho)rq-cq^2/2\), selected effort is \(b(1-\rho)r/c\) before clipping to the feasible interval. | Exact theorem for the unconstrained quadratic | Lean: `selectedEffort_global_max` |
| C7 | Selected monitoring meets a declared effort requirement iff \(cq_{req}\le b(1-\rho)r\), for \(c>0\). | Exact theorem | Lean: `selectedEffort_meets_requirement_iff` |
| C8 | Higher common-mode correlation can produce lower long-run commons health in the declared adaptive simulation. | Computational result, parameter dependent | Parameter sweep and tests |
| C9 | Verification debt can precede visible commons collapse. | Hypothesis instantiated by one bookkeeping definition | Dynamic model; requires robustness analysis |
| C10 | JAM can be analyzed as distributed maintenance of protocol-valid shared state. | Structural interpretation | `docs/JAM_MAPPING.md` |
| C11 | Ecological roles can sometimes be represented as positions in distributed feedback loops. | Research hypothesis, not established here | `docs/ECOLOGY_MAPPING.md` |
| C12 | In the non-trivial attainable region, clipped selected effort is sufficient iff \(c\le b(1-\rho)r/q_{suff}\). | Exact theorem | Python classifier; Lean: `selected_safety_iff_critical_cost` |
| C13 | Correlation simultaneously raises required effort and lowers detection-contingent private return in the declared model. | Exact comparative result from the model equations; numerically tested | `docs/PHASE_BOUNDARY.md`; `test_correlation_double_squeeze` |
| C14 | In the adaptive producer model, the common-mode detection cap creates an endogenous producer-target floor (m=\sigma((g-\ell(1-\rho))/T)). For partial adjustment (0<\alpha\le1), the attempt rate obeys (b_t\ge m+(1-\alpha)^t(b_0-m)), so \(\liminf b_t\ge m\); combined with the common-mode floor this gives \(\liminf P_{bad,t}\ge\rho m\). | Exact finite-time theorem for any antitone producer response; logistic specialization and asymptotic corollary | Lean: `EndogenousFloor.lean`; Python: producer-floor regression tests |

## Prior-art calibration

C2-C4 recover the familiar fact that redundancy cannot eliminate a common-cause failure component. They are retained because recovering a known limit is a useful calibration of the abstraction, not because the repository claims that floor as novel. The research contribution must come from coupled phase structure beyond that baseline.

## Explicit non-claims

This repository does not claim that consensus establishes external truth, that every species performs a net ecosystem service, that all persistent networks are cooperative, or that the present toy model constitutes a security analysis of JAM.
