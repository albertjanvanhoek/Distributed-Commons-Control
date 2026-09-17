# Correlated Honest Failure in JAM/ELVES

Repo-ready LaTeX package for the technical companion paper.

## Main results

1. **Verdict attribution boundary** from the current Gray Paper rules.
2. **Fault-specific ELVES escalation** under correlated honest failure.
3. **Sampling dilution** showing that honest-but-correlated validator additions can lower corrective reproduction.
4. **Recurrent corrective capacity** separating within-audit corrective reproduction from cross-audit maintenance of the capacity required to remain corrective.
5. **Dynamic corrective resilience** coupling slow corrective capacity back to the next audit and showing that current `lambda_x` alone does not determine finite-horizon resilience.

Result 4 introduces a declared slow `C -> O -> R -> C` loop linking independently corrective capacity, observability/attribution of genuine maintenance, and resources returned to preserve future corrective capacity. Machine-checked witnesses show that the event-level condition `lambda_x > 1` and the slow maintenance replacement condition imply neither one another. The maintenance threshold is therefore an orthogonal timescale, not a fourth nested point on the verdict/audit threshold sequence.

Result 5 adds a slow state update and the bridge `lambda_x,t = F C_t`. At current criticality, Lean verifies the exact one-step condition

\[
\lambda_{x,t+1}\ge1
\iff
F k_{RC}R_t\ge1-r_C.
\]

The same formalization gives two systems with identical current `lambda_0 = 3/2` but opposite five-step threshold status under different reduced maintenance multipliers. This is the paper's central dynamic claim: current audit reproduction is not a sufficient statistic for future corrective resilience in the declared model.

## Files

- `main.tex` — manuscript entry point.
- `sections/` — modular manuscript sections.
- `figures/thresholds.tex` — TikZ threshold figure.
- `references.bib` — bibliography.
- `CLAIMS.md` — claim-status ledger.
- `reproduce.py` — dependency-free reproduction of numerical tables.
- `../../formalization/JamRecurrentMaintenance.lean` — machine-checked two-timescale separation witnesses.
- `../../formalization/JamResilienceDynamics.lean` — machine-checked slow-to-fast bridge, maintenance-return boundary and finite-horizon non-identifiability witness.

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

This is not a JAM security audit and does not claim an observed vulnerability. Result 1 derives from the Gray Paper verdict rules under a declared correlated-fault scenario. Results 2-3 extend ELVES and therefore require review by the ELVES authors. Results 4-5 add declared slow-timescale systems dynamics motivated by the repository's grounded JAM maintenance analysis. Their coefficients and reduced multipliers are not claimed to be current Gray Paper parameters or calibrated JAM estimates, and novelty is not claimed for the underlying positive-systems, reproduction-number or geometric-decay mathematics.
