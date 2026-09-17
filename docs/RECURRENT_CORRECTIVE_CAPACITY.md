# Recurrent corrective capacity in JAM/ELVES

## Purpose

The JAM/ELVES analysis now distinguishes three questions:

1. **Within-audit corrective reproduction**: does independently correct checking reproduce during the current dispute process?
2. **Cross-audit maintenance reproduction**: does the surrounding architecture preserve the capacities required to remain independently corrective?
3. **Finite-horizon corrective resilience**: can current supercritical correction persist under the measured replenishment and attrition dynamics?

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

## Dynamic bridge to the next audit

`formalization/JamResilienceDynamics.lean` adds an explicit slow state

\[
X_t=(C_t,O_t,R_t)
\]

with update

\[
C_{t+1}=r_CC_t+k_{RC}R_t,
\]
\[
O_{t+1}=r_OO_t+k_{CO}C_t,
\]
\[
R_{t+1}=r_RR_t+k_{OR}O_t.
\]

The fast audit reproduction supplied by this state is

\[
\lambda_{x,t}=FC_t.
\]

Hence

\[
\lambda_{x,t+1}=r_C\lambda_{x,t}+Fk_{RC}R_t.
\]

At current criticality, `lambda_x,t = 1`, Lean verifies the exact maintenance-return boundary

\[
\boxed{\lambda_{x,t+1}\ge1\iff Fk_{RC}R_t\ge1-r_C.}
\]

This motivates the local return margin

\[
M_t=Fk_{RC}R_t-(1-r_C).
\]

- `M_t < 0`: a currently critical system crosses below the audit threshold on the next slow update;
- `M_t = 0`: replacement exactly closes the local corrective-capacity gap;
- `M_t > 0`: a currently critical system moves above the audit threshold.

This is a one-step boundary, not a general stability theorem for the full slow system.

## Why current audit success is not enough

For a reduced effective cross-audit multiplier `m`, define

\[
\lambda_t=m^t\lambda_0.
\]

The correction margin `mu_t=lambda_t-1` obeys

\[
\mu_{t+1}=m\mu_t-(1-m).
\]

A machine-checked counterexample starts two systems at the same current value `lambda_0=3/2`:

- with `m=1`, the system is still at `3/2` after five steps;
- with `m=9/10`, it is below one after five steps.

Thus a snapshot of current `lambda_x` does not identify finite-horizon resilience in the declared dynamic model. The reduced multiplier is a diagnostic abstraction, not a calibrated JAM parameter and not the same object as the three-process loop ratio.

## Empirical grounding needed next

A protocol-facing resilience assessment would need measurable proxies for:

- the current fault-specific independently corrective share `C_x,t`;
- rates at which independent implementations/operators enter, exit, converge, or become correlated;
- real audit effort versus nominal participation;
- observability/attribution of useful independent maintenance;
- economic and development resources returned to independently corrective implementations/operators;
- the time scale on which those returns affect future corrective capacity;
- the current maintenance-return margin and its uncertainty;
- horizon forecasts under plausible ranges rather than a single point estimate.

Client identity or diversity proofs can help make part of this state observable, but observability alone does not establish that the return loop closes. The operational target is stronger: estimate whether the processes that produce independent correction are themselves above replacement before the current audit margin is exhausted.

A concrete testnet/deployment question is therefore:

> Can JAM estimate both the current fault-specific audit reproduction margin and a separate cross-audit maintenance-return margin, and detect a projected threshold crossing before event-level correction becomes subcritical?
