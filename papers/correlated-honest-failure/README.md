# Correlated Honest Failure in JAM/ELVES

Repo-ready LaTeX package for the technical companion paper.

## Main results

1. **Verdict attribution boundary** from the current Gray Paper rules.
2. **Fault-specific ELVES escalation** under correlated honest failure.
3. **Sampling dilution** showing that honest-but-correlated validator additions can lower corrective reproduction.
4. **Recurrent corrective capacity** separating within-audit corrective reproduction from cross-audit maintenance of the capacity required to remain corrective.
5. **Dynamic corrective resilience** coupling slow corrective capacity back to the next audit and proving both erosion and a full-state persistence region.

Result 4 introduces a declared slow `C -> O -> R -> C` loop linking independently corrective capacity, observability/attribution of genuine maintenance, and resources returned to preserve future corrective capacity. Machine-checked witnesses show that the event-level condition `lambda_x > 1` and the slow maintenance replacement condition imply neither one another. The maintenance threshold is therefore an orthogonal timescale, not a fourth nested point on the verdict/audit threshold sequence.

Result 5 adds a slow state update and the bridge `lambda_x,t = F C_t`. At current criticality, Lean verifies the exact one-step condition

\[
\lambda_{x,t+1}\ge1
\iff
F k_{RC}R_t\ge1-r_C.
\]

The reduced model proves that any finite initial correction reproduction eventually becomes subcritical when `0 <= m < 1`, and gives two systems with identical current `lambda_0 = 3/2` but opposite five-step threshold status under different maintenance multipliers.

The full three-state formalization then closes the positive side. For

\[
C^*=(1-r_O)(1-r_R),\qquad
O^*=k_{CO}(1-r_R),\qquad
R^*=k_{CO}k_{OR},
\]

the exact product condition

\[
(1-r_C)(1-r_O)(1-r_R)\le k_{CO}k_{OR}k_{RC}
\]

makes the coordinatewise cone above `(C*,O*,R*)` forward invariant under nonnegative coefficients. If `F C* > 1`, the canonical trajectory therefore remains audit-supercritical at every future cross-audit time. The model thus contains both a formal erosion mechanism and a formal persistence region.

## Literature boundary

The paper does **not** claim novelty for the general idea that resilience must be replenished over time. Proactive Byzantine recovery and reconfiguration already maintain enough nonfaulty replicas so accumulated faults do not exceed a tolerated bound. Nor does the paper claim novelty for client diversity, diversity-aware rewards, positive-systems thresholds, or geometric decay.

The narrower proposed contribution is different in the object being maintained: **fault-specific independently corrective capacity inside a sampled audit process**, including honest validators sharing a common implementation fault. The paper connects that fast audit quantity to a separately maintained slow state, makes observability/attribution and resource return part of the maintenance loop, derives an exact return-gap boundary, and proves when the resulting full-state dynamics preserve fast audit supercriticality.

## Files

- `main.tex` — manuscript entry point.
- `sections/` — modular manuscript sections.
- `figures/thresholds.tex` — TikZ threshold figure.
- `references.bib` — bibliography.
- `CLAIMS.md` — claim-status ledger.
- `reproduce.py` — dependency-free reproduction of numerical tables.
- `../../formalization/JamRecurrentMaintenance.lean` — machine-checked two-timescale separation witnesses.
- `../../formalization/JamResilienceDynamics.lean` — machine-checked slow-to-fast bridge, maintenance-return boundary and erosion/non-identifiability results.
- `../../formalization/JamMaintenancePersistence.lean` — canonical full-state threshold, forward-invariant maintenance cone and persistent-supercriticality theorem.

## Build

```bash
pdflatex main.tex
biber main
pdflatex main.tex
pdflatex main.tex
```

## Reproduce calculations

```bash
python reproduce.py
```

## Scope

This is not a JAM security audit and does not claim an observed vulnerability. Result 1 derives from the Gray Paper verdict rules under a declared correlated-fault scenario. Results 2-3 extend ELVES and therefore require review by the ELVES authors. Results 4-5 add declared slow-timescale systems dynamics motivated by the repository's grounded JAM maintenance analysis. Their coefficients and reduced multipliers are not claimed to be current Gray Paper parameters or calibrated JAM estimates. The full-state result is a conditional invariant-region theorem, not a convergence, global-stability, or empirical long-run JAM theorem.
