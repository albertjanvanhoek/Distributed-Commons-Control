# Implementation scope

Branch: `jam/recurrent-maintenance-20260917`

This branch intentionally adds a narrow fourth layer to the JAM/ELVES correlated-honest-failure work rather than replacing the existing paper.

Implemented:

- new Lean target `JamRecurrentMaintenance`;
- exact canonical product replacement threshold;
- deterministic slow trajectory and all-time positivity result;
- separation theorems between fast correction and slow maintenance;
- a witness separating local compute selection from slow maintenance;
- four-cell phase non-vacuity theorem;
- Experiment 13 documentation;
- Result 4 in the technical paper;
- updated paper claim ledger and conclusion.

Deferred until the formal target compiles cleanly:

- broader top-level README restructuring;
- numerical estimation of slow-loop coefficients;
- any claim that production JAM occupies a particular fast/slow phase;
- general arbitrary-network spectral-radius formalization.
