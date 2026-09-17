# Claim status — Correlated Honest Failure in JAM/ELVES

| ID | Claim | Status | Boundary |
|---|---|---|---|
| A1 | A bad verdict remains constructible against adversarial positive voting iff independently correct negative judges satisfy `C_x >= floor(2N/3)+1`. | Exact consequence of Gray Paper verdict rule + declared fault model | Assumes enough judgments are available. |
| A2 | A good verdict becomes constructible if `A+B_x >= floor(2N/3)+1`. | Exact consequence of Gray Paper verdict rule + declared fault model | Does not establish real-world existence of such a fault. |
| A3 | Large-N robust bad-verdict attribution requires `gamma + (1-gamma) f_x < 1/3`. | Asymptotic form of A1 | `f_x` is fault-domain share among otherwise-honest validators. |
| A4 | For N=1023, `K=683`, wonky requires 341 positive + 342 negative judgments, and the literal 682-positive/341-negative population composition contains no allowed verdict subset. | Exact count observation | Needs confirmation from JAM authors; may be resolved by intended semantics elsewhere. |
| B1 | Under the shared-fault extension, ELVES corrective reproduction becomes `lambda_x = F C_x/N = F(1-gamma)(1-f_x)`. | Model extension | Outside the original ELVES proof assumptions. |
| B2 | Supercritical correction requires `f_x < 1 - 1/((1-gamma)F)`. | Exact consequence of B1 | Branching threshold, not exact protocol frontier. |
| B3 | Larger F tolerates a larger fault domain but worsens the static no-show committee bound `s0/(1-uF)`. | Comparative result from ELVES equations + extension | No claim that one F is globally optimal for JAM. |
| B4 | At s0=30 and gamma=1/3, the pessimistic bound at F=2 is about 2.49 times the bound at F=2.0794. | Computational specialization | Not “2.49x less secure.” |
| C1 | Holding independently correct count C_x fixed, adding validators outside C_x strictly lowers `lambda_x=F C_x/N`. | Exact identity | Sampling architecture only; not all-participant coverage. |
| C2 | Baseline N=1023,A=205,B=164,C=654: adding 200 buggy honest validators raises the extended bound from 4.52e-4 to 0.130 with fixed s0=30 and to 0.0874 with fixed 341 cores. | Computational specialization | A fixed; adversarial share therefore falls as N grows. |
| C3 | Validator-growth concern depends on core scaling: if cores scale as N/3, expected sample stays 30; if 341 cores stay fixed, expected sample grows roughly 10N/341. | Gray Paper parameter interpretation + arithmetic | Future scaling policy is not specified by this paper. |
| D1 | Slashable collateral need not equal attacker-attributable collateral when honest buggy guarantors sign the invalid report. | Economic mapping observation | Does not prove attacker has zero cost. |
| D2 | Wonky has no ordinary Gray Paper culprit/fault offender record. | Gray Paper rule interpretation | Staking layer may add consequences; requires author confirmation. |
| D3 | Guarantor diversity, announcement monitoring, effort proofs and load-feedback controls are design hypotheses. | Future work | No protocol recommendation is claimed. |
| E1 | In the declared slow three-process loop `correction -> observability -> resources -> correction`, the canonical correction coordinate reaches replacement iff `(1-r_C)(1-r_O)(1-r_R) <= k_CO k_OR k_RC`. | Exact theorem; machine checked | Generic positive-system algebra; not claimed as novel mathematics or a measured JAM law. |
| E2 | With nonnegative slow update coefficients and the replacement threshold, the cone above the canonical witness is forward invariant; with positive deficits/couplings and the strict threshold, all three capacities remain positive at every time step. | Exact deterministic theorem; machine checked | Starts from the declared canonical witness and linear update rule. |
| E3 | Event-level supercritical correction `lambda_x>1` does not imply slow recurrent-maintenance supercriticality. | Exact logical separation; machine-checked witness | Slow-loop coefficients are independent higher-layer interface parameters. |
| E4 | Slow recurrent-maintenance supercriticality does not imply fault-specific event-level correction `lambda_x>1`. | Exact logical separation; machine-checked witness | A persistent architecture can still be concentrated in the relevant fault domain. |
| E5 | All four fast/slow phase cells are inhabited; in particular, current correction and local compute selection can both satisfy their declared boundaries while the slow maintenance loop remains subcritical. | Exact non-vacuity/separation result; machine checked | Does not establish which cell production JAM occupies. |

## Explicit non-claims

The paper does not claim:
- that JAM currently has an exploitable shared client bug;
- that the extended branching probability is an exact JAM attack probability;
- that the attacker can freely choose a favorable core assignment;
- that a wonky verdict is economically cost-free in a production staking layer;
- that client count equals fault-domain diversity;
- that F=2 is incorrectly chosen without a complete re-optimization under the revised threat model;
- that the slow-loop coefficients are specified by the current Gray Paper;
- that the three-process product threshold is new positive-systems or reproduction-number mathematics;
- that satisfying the slow-maintenance threshold guarantees correctness for every fault.
