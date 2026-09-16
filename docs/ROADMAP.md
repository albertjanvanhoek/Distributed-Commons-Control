# Research roadmap

## Phase 1 — Minimal distributed controller

- Define harmful-attempt, monitoring and commitment probabilities.
- Derive the common-mode floor.
- Separate selected from sufficient control.
- Close the exact safety boundary with Lean.

**Status:** complete baseline/calibration layer.

## Phase 2 — Closed shared-state feedback

- Add delayed observations and finite monitoring adjustment.
- Close the return path from commons condition to future control.
- Derive the reduced loop-gain criterion.
- Test folds under multiple return-path closures.
- Separate current-state slowing from basin fragility due to mobilisation.

**Status:** complete first closed-loop layer. Concrete fold locations remain
computational; the multiplier identities are formalized.

## Phase 3 — Viability contribution of heterogeneous participants

- Replace interchangeable participants with heterogeneous vulnerability
  profiles.
- Declare a disturbance class and a viability margin M(S).
- Compute leave-one-out, Shapley and explicit interaction contributions.
- Prove the smallest decorrelation example exactly.
- Keep the model substrate-neutral.

**Exit criterion:** contribution is defined against network viability rather
than current shared-state level, and the exact topology results reproduce.

## Phase 4 — Structural versus selected viability

**Status:** exact two-participant reversal established in Experiment 4.

- Add participant behavior and shared/reward-coupled incentives.
- Let remaining participants re-equilibrate after addition/removal.
- Distinguish structural margin from realized/selected margin.
- Seek a clean counterexample with

[
Delta_i M_{structural}>0
quad	ext{and}quad
Delta_i M_{selected}<0.
]

**Exit criterion:** achieved for the minimal direct-versus-induced-response decomposition. Richer mechanisms can be revisited only if needed for a substrate mapping.

## Phase 5 — Slow corrective capacity

Introduce a separate slow stock C:

[
	ext{state}=(X,C),
]

where X is current shared state and C is built, maintained and lost over a
slower time scale than effort.

- Define M(X,C) operationally as disturbance tolerance/recoverability.
- Distinguish fast effort from slow readiness.
- Redefine maintenance debt as capacity shortfall relative to required margin,
  rather than accumulated realized failure.
- Test whether capacity decay creates fragility without a current-state early
  warning in X.

**Exit criterion:** two systems with the same X but different C have
demonstrably different disturbance margins, and C has a non-definitional
dynamics.

## Phase 6 — Multiple loops

- Replace the scalar shared-state requirement with multiple declared
  viability loops.
- Allow each participant to have signed, delayed effects on several loops.
- Represent contribution as a vector rather than a global good/bad score.
- Study cross-loop tradeoffs and shared failure causes.

**Exit criterion:** the framework can represent a participant that is
positive for one viability loop, negative for another, and neutral for a
third without collapsing those signs into one moral or functional label.

## Phase 7 — Substrate return tests

Only after the neutral theory is stable, map it to concrete substrates.

### Distributed computation / JAM

- Map abstract variables to exact protocol stages and failure modes.
- Identify what cryptography/quorums already guarantee.
- Keep generic results separate from protocol-specific claims.

### Ecology

- Select an empirically tractable interaction network.
- Declare the relevant viability variables and disturbance classes.
- Estimate participant vulnerability profiles, delays and corrective
  capacities.
- Test whether viability-margin contribution predicts perturbation outcomes
  beyond ordinary service-flow or interaction-network descriptions.

**Exit criterion:** at least one substrate mapping produces a discriminating
prediction without changing the neutral mathematical definitions.

## Publication discipline

At every phase, maintain separate ledgers for definitions, exact mathematical
results, computational observations, substrate mappings, prior art, and
speculative cross-domain hypotheses.
