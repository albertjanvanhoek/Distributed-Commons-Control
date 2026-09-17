# JAM recurrent maintenance — formal verification note

The dedicated proof target is:

```text
JamRecurrentMaintenance.lean
```

It extends the existing JAM formalization without changing the semantics of `JamMaintenance.lean` or `JamEffortObservability.lean`.

## Exact declarations

| Claim | Lean declaration |
|---|---|
| Canonical slow-loop replacement iff product threshold | `jam_recurrent_canonical_correction_replacement_iff` |
| Canonical observability replacement identity | `jam_recurrent_canonical_observability_replacement` |
| Canonical resource replacement identity | `jam_recurrent_canonical_resources_replacement` |
| Cone above canonical witness is forward invariant | `jam_recurrent_step_preserves_canonical_lower_bound` |
| Canonical trajectory stays above the witness | `jam_recurrent_trajectory_stays_above_canonical` |
| Canonical witness is positive under positive deficits/couplings | `jam_recurrent_canonical_positive` |
| Strict loop remains positive for all time | `jam_strict_maintenance_loop_positive_for_all_time` |
| Event correction does not imply recurrent maintenance | `event_correction_does_not_imply_recurrent_maintenance` |
| Recurrent maintenance does not imply event correction | `recurrent_maintenance_does_not_imply_event_correction` |
| Local audit viability does not imply slow maintenance | `local_audit_viability_does_not_imply_slow_maintenance` |
| All four fast/slow phase cells are inhabited | `jam_two_timescale_phase_cells_inhabited` |

## Scope

Machine checking establishes implications of the declared linear slow-loop model. It does not establish that JAM's production staking/operator ecosystem has these exact coefficients, that the slow variables are directly observable on chain, or that the product threshold is novel mathematics.

The scientific use of the module is the formally explicit separation

```text
event-level correction reproduction
    !=
cross-time reproduction of corrective capacity.
```
