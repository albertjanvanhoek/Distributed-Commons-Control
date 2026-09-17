# Experiment 13 — recurrent corrective capacity across audits

## 1. Question

The existing JAM/ELVES extension asks whether correction reproduces strongly enough **inside one audit**. For fault `x`,

\[
\lambda_x=F\frac{C_x}{N}.
\]

The new question is slower:

> Does the surrounding architecture reproduce the capacity required to remain independently corrective across future audits?

These are not the same question.

## 2. Fast and slow reproduction

The fast condition is

\[
\boxed{\lambda_x>1.}
\]

It concerns escalation of independently correct judgments during a particular audit.

The slow model tracks three abstract capacities:

- `C_t`: future independently corrective capacity;
- `O_t`: capacity to observe/discriminate genuine maintenance;
- `R_t`: resources returned to preserve future corrective capacity.

The minimal return loop is

\[
C\to O\to R\to C,
\]

with update rule

\[
\begin{aligned}
C_{t+1}&=r_C C_t+k_{RC}R_t,\\
O_{t+1}&=r_O O_t+k_{CO}C_t,\\
R_{t+1}&=r_R R_t+k_{OR}O_t.
\end{aligned}
\]

Define deficits

\[
d_i=1-r_i.
\]

For the canonical three-process witness, the exact replacement boundary is

\[
\boxed{d_Cd_Od_R\le k_{CO}k_{OR}k_{RC}.}
\]

When all deficits are positive, define the slow reproduction ratio

\[
\mathcal R_M=
\frac{k_{CO}k_{OR}k_{RC}}{d_Cd_Od_R}.
\]

Strict slow maintenance corresponds to

\[
\boxed{\mathcal R_M>1.}
\]

The product-loop algebra is not claimed as new mathematics. The repository contribution is the separation and composition of this slow maintenance condition with the JAM/ELVES event-level correction condition.

## 3. Machine-checked result

`formalization/JamRecurrentMaintenance.lean` checks:

1. the exact canonical replacement equivalence;
2. forward invariance of the cone above the canonical witness for nonnegative coefficients;
3. positivity of the canonical trajectory for all time under positive deficits/couplings and the strict loop threshold;
4. a witness with event-level correction supercritical but slow maintenance subcritical;
5. a witness with slow maintenance supercritical but event-level correction subcritical;
6. a witness in which current correction is supercritical and local compute selection is viable while slow maintenance still fails;
7. non-vacuity of all four cells of the fast/slow phase diagram.

## 4. Two-timescale phase diagram

| | Slow maintenance `R_M > 1` | Slow maintenance `R_M <= 1` |
|---|---|---|
| Fast correction `lambda_x > 1` | current correction works and corrective capacity is maintained | **correctable now, eroding later** |
| Fast correction `lambda_x <= 1` | maintenance persists but fault-specific independent correction is insufficient | neither condition holds |

The upper-right cell is the main new structural warning. A system can satisfy the event-level branching threshold today without reproducing the capacity needed to satisfy it tomorrow.

The lower-left cell is the complementary warning. Economic or operational persistence of a validator ecosystem is not evidence that it contains enough independently correct validators for a particular fault.

## 5. Relation to Experiment 11

Experiment 11 derived the local compute-selection margin

\[
\Phi=sW+bdL_F-c.
\]

Closing `Phi >= 0` can make genuine checking selected against rubber-stamping in the declared local game. But this is still not a slow maintenance theorem.

A system can have:

\[
\lambda_x>1,
\qquad
\Phi\ge0,
\]

while

\[
\mathcal R_M\le1.
\]

The Lean file contains an explicit witness.

This separates three questions:

1. **Can the current audit correct?** — `lambda_x`.
2. **Is real checking locally selected?** — `Phi`.
3. **Does the architecture reproduce future corrective capacity?** — `R_M`.

## 6. JAM interpretation boundary

The slow variables are interface variables, not claimed Gray Paper state variables.

A possible functional interpretation is:

- `C -> O`: genuine corrective work creates enough evidence to be distinguishable from cheap imitation;
- `O -> R`: the staking/accountability layer returns value or suppression conditional on that evidence;
- `R -> C`: returned resources preserve independent client implementations, compute, operator participation, testing, maintenance, and other future corrective capacity.

The current audited JAM layer does not numerically identify `k_CO`, `k_OR`, or `k_RC`. Therefore the model does **not** say which slow phase production JAM occupies.

## 7. Falsification boundaries

The model would be weakened or falsified as a useful JAM abstraction if, for example:

- future independently corrective capacity does not depend materially on any returned resource/selection process;
- genuine checking need not be distinguishable for its capacity to persist;
- the proposed three-process loop omits a dominant maintenance route that changes the relevant threshold topology;
- the higher-layer staking/operator architecture directly enforces a different recurrence condition;
- empirical operator/client dynamics show no relation between current selection/return and future independent corrective capacity.

The intended contribution is therefore not “JAM needs this exact three-node loop.” It is the narrower claim:

> **event-level corrective reproduction and cross-time reproduction of corrective capacity are distinct conditions and must not be inferred from one another.**
