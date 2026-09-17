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
| E1 | The slow three-process model `C -> O -> R -> C` meets its canonical replacement condition when `k_CO k_OR k_RC >= (1-r_C)(1-r_O)(1-r_R)`. | Declared maintenance-loop model; algebraic threshold | The variables and couplings are not claimed to be current Gray Paper state variables. General product/spectral threshold mathematics is prior art. |
| E2 | Event-level supercritical correction (`lambda_x > 1`) does not imply slow maintenance viability. | Machine-checked separation witness | Witness uses `F=2, gamma=f=0` and a subcritical slow loop. |
| E3 | Slow maintenance viability does not imply event-level supercritical correction for a particular fault. | Machine-checked separation witness | Witness uses a strong slow loop but `f=3/4`, giving `lambda_x=1/2` at `F=2, gamma=0`. |
| E4 | All four cells of the two-threshold phase structure are jointly inhabitable in the declared model. | Machine-checked witnesses | This is logical/model non-equivalence, not an empirical statement about JAM deployment. |
| E5 | A system can therefore be correctable in the current audit while the modeled capacity supporting future correction is below replacement, or operationally persistent while fault-specific correction is subcritical. | Interpretation of E2–E4 | Requires empirical/protocol mapping before any claim about actual JAM long-run dynamics. |
| F1 | Under the declared state update `C' = r_C C + k_RC R` and fast coupling `lambda = F C`, next reproduction satisfies `lambda' = r_C lambda + F k_RC R`. | Machine-checked exact identity | `C`, `R`, and their update coefficients are declared slow-state variables, not Gray Paper variables. |
| F2 | At current criticality `lambda=1`, next reproduction is at least critical iff `F k_RC R >= 1-r_C`. | Machine-checked exact equivalence | Local one-step maintenance-return boundary; not a general stability theorem for the full three-dimensional loop. |
| F3 | At current criticality, strict return shortfall makes the next audit subcritical; strict return surplus makes it supercritical. | Machine-checked corollaries of F2 | Same declared state model. |
| F4 | In the reduced path `lambda_t=m^t lambda_0`, the correction margin obeys `mu_{t+1}=m mu_t-(1-m)`. | Machine-checked identity | `m` is a reduced net cross-audit multiplier and is not identified with the three-process loop ratio `R_M`. |
| F5 | The same current supercritical reproduction number can correspond to different finite-horizon threshold status: with `lambda_0=3/2`, `m=1` remains supercritical at step 5 whereas `m=9/10` is subcritical. | Machine-checked counterexample | Numerical witness demonstrates non-identifiability; it is not a calibrated JAM forecast. |
| F6 | Current `lambda_x` is therefore not a sufficient statistic for finite-horizon corrective resilience in the declared dynamic model. | Interpretation of F4–F5 | Forecasting actual JAM resilience requires empirical identification of slow-state dynamics. |
| F7 | For the full three-state dynamics, the canonical witness `C*=(1-r_O)(1-r_R)`, `O*=k_CO(1-r_R)`, `R*=k_CO k_OR` is componentwise nondecreasing after one update iff the three-cycle product threshold is met, with `O*` and `R*` exactly at replacement. | Machine-checked exact finite-cycle theorem | Finite three-cycle result; no novelty claim for general positive-systems or Perron–Frobenius theory. |
| F8 | Under nonnegative retention and coupling coefficients and the product threshold, the coordinatewise cone above the canonical witness is forward invariant. | Machine-checked dynamic theorem | Applies to the declared linear slow-state model. It is not a global stability or convergence theorem. |
| F9 | If the canonical corrective coordinate already satisfies `F C* > 1`, then every point of the canonical maintenance trajectory remains audit-supercritical for all future cross-audit times. | Machine-checked persistent-resilience theorem | Conditional on the declared slow dynamics, nonnegative coefficients and canonical initial state. |
| F10 | Deleting the immediate `R -> C` return edge with `r_C<1` makes any positive corrective coordinate decline in the next slow update. | Machine-checked return-edge theorem | One-step erosion result; later system behavior may depend on other mechanisms not represented here. |

## Explicit non-claims

The paper does not claim:
- that JAM currently has an exploitable shared client bug;
- that the extended branching probability is an exact JAM attack probability;
- that the attacker can freely choose a favorable core assignment;
- that a wonky verdict is economically cost-free in a production staking layer;
- that client count equals fault-domain diversity;
- that F=2 is incorrectly chosen without a complete re-optimization under the revised threat model;
- that the Gray Paper already specifies numerical coefficients for the slow `C -> O -> R -> C` maintenance loop;
- that `lambda_x > 1` guarantees preservation of corrective capacity across future audits;
- that persistence of a validator/economic ecosystem guarantees independent correction for every correlated fault;
- that the reduced multiplier `m=9/10` or any other numerical slow-dynamics parameter is an estimate for JAM;
- that a single current observation of `lambda_x` is sufficient to estimate a future failure probability;
- that the full three-state forward-invariance result establishes convergence, global stability, or calibrated long-run JAM behavior;
- novelty for the underlying positive-systems, spectral-radius, reproduction-number, software-rejuvenation, or geometric-decay mathematics used in the declared slow models.
