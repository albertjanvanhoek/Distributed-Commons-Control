# JAM two-timescale phase structure

The recurrent-maintenance extension separates two thresholds:

\[
\lambda_x=F C_x/N
\]

for fault-specific correction inside an audit, and

\[
\mathcal R_M=
\frac{k_{CO}k_{OR}k_{RC}}
{(1-r_C)(1-r_O)(1-r_R)}
\]

for the strict canonical slow maintenance loop when the deficits are positive.

| Fast correction | Slow maintenance | Interpretation |
|---|---|---|
| `lambda_x > 1` | `R_M > 1` | Current audit correction is supercritical and the declared slow corrective-capacity loop reproduces. |
| `lambda_x > 1` | `R_M <= 1` | **Correctable now, eroding later.** Current correction can work while future corrective capacity decays. |
| `lambda_x <= 1` | `R_M > 1` | The surrounding maintenance architecture persists, but the relevant fault lacks enough independent corrective capacity. |
| `lambda_x <= 1` | `R_M <= 1` | Neither declared condition is satisfied. |

Lean verifies concrete witnesses for all four cells in `jam_two_timescale_phase_cells_inhabited`.

The table is a model classification, not an assessment of production JAM.
