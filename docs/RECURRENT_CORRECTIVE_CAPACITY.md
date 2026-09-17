# Recurrent corrective capacity in JAM/ELVES

## Purpose

The JAM/ELVES analysis now distinguishes two reproduction questions:

1. **Within-audit corrective reproduction**: does independently correct checking reproduce during the current dispute process?
2. **Cross-audit maintenance reproduction**: does the surrounding architecture preserve the capacity required to remain independently corrective in future audits?

These are not the same condition.

## Event-level condition

Under the correlated-honest-failure extension,

\[
\lambda_x = F(1-\gamma)(1-f_x).
\]

The current audit is supercritical for independently correct checking when

\[
\lambda_x>1.
\]

## Slow maintenance condition

Introduce a declared slow three-process loop:

- `C`: independently corrective capacity;
- `O`: observability/attribution of genuine maintenance;
- `R`: resources returned to preserve future corrective capacity.

The canonical directed loop is

\[
C\rightarrow O\rightarrow R\rightarrow C.
\]

With retention factors `r_C,r_O,r_R` and coupling gains `k_CO,k_OR,k_RC`, the declared replacement condition is

\[
k_{CO}k_{OR}k_{RC}\ge(1-r_C)(1-r_O)(1-r_R).
\]

This is a model extension. The coefficients are not claimed to be current Gray Paper state variables. The underlying product/spectral threshold structure is classical; the research contribution is the explicit separation of this condition from the ELVES event-level correction threshold.

## Machine-checked separation

`formalization/JamRecurrentMaintenance.lean` proves explicit witnesses for all four cells:

| Current correction | Slow maintenance | Interpretation |
|---|---|---|
| supercritical | viable | current correction works and modeled corrective capacity is maintained |
| supercritical | subcritical | correctable now, modeled capacity erodes across time |
| subcritical | viable | ecosystem persists but is insufficiently independently corrective for fault `x` |
| subcritical | subcritical | neither condition holds |

The two key non-implications are therefore machine checked:

\[
\lambda_x>1\not\Rightarrow \text{maintenance viability},
\]

and

\[
\text{maintenance viability}\not\Rightarrow\lambda_x>1.
\]

## Empirical grounding needed next

The mathematical separation is useful only if the slow-loop terms can be grounded. The next protocol-facing work should therefore identify measurable proxies for:

- how current independently corrective capacity is replenished or lost;
- how actual audit effort and useful independent correction are observed;
- how staking/operator/client economics return resources to those capacities;
- how implementation concentration changes over time;
- whether these return paths are fast enough to offset attrition.

This suggests a concrete empirical question for JAM deployments or testnets: can the system estimate a time-dependent maintenance margin for independent corrective capacity, separately from the current ELVES audit reproduction number?
