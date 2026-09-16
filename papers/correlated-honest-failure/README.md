# Correlated Honest Failure in JAM/ELVES

Repo-ready LaTeX package for the technical companion paper.

## Main results

1. **Verdict attribution boundary** from the current Gray Paper rules.
2. **Fault-specific ELVES escalation** under correlated honest failure.
3. **Sampling dilution** showing that honest-but-correlated validator additions can lower corrective reproduction.

## Files

- `main.tex` — manuscript entry point.
- `sections/` — modular manuscript sections.
- `figures/thresholds.tex` — TikZ threshold figure.
- `references.bib` — bibliography.
- `CLAIMS.md` — claim-status ledger.
- `reproduce.py` — dependency-free reproduction of numerical tables.

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

This is not a JAM security audit and does not claim an observed vulnerability. Result 1 derives from the Gray Paper verdict rules under a declared correlated-fault scenario. Results 2-3 extend ELVES and therefore require review by the ELVES authors.
