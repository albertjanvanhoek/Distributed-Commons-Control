# Prior-art boundary

This note separates results that calibrate the model against established work
from phase structure that arises only after the declared feedback loops are
coupled. It is a novelty boundary, not a literature review.

## 1. Common-cause redundancy limits are established

The repository's common-mode mixture

\[
E_n(q,\rho)=\rho+(1-\rho)(1-q)^n
\]

is a deliberately simple model in which a fraction \(\rho\) of cases defeats
all same-mode monitors. The resulting floor \(P_{bad}\ge b\rho\) is therefore
a model consequence, but the underlying lesson is not new: redundant
components do not remove a common-cause failure component.

Relevant antecedents include:

- K. N. Fleming (1975), *A reliability model for common mode failures in
  redundant safety systems*, which introduced the beta-factor approach to
  splitting component failure into independent and common-cause parts.
- D. E. Eckhardt and L. D. Lee (1985), *A theoretical basis for the analysis
  of multiversion software subject to coincident errors*, IEEE Transactions on
  Software Engineering 11(12):1511-1517.
- B. Littlewood and D. R. Miller (1989), *Conceptual modeling of coincident
  failures in multiversion software*, IEEE Transactions on Software
  Engineering 15(12):1596-1614, DOI 10.1109/32.58771.

The parameter \(\rho\) used here is a Bernoulli common-mode mixture weight; it
should not be identified numerically with a classical beta factor without an
additional mapping.

## 2. Verification underprovision is also established

Luu, Teutsch, Kulkarni and Saxena (CCS 2015), *Demystifying Incentives in the
Consensus Computer*, DOI 10.1145/2810103.2813659, named the **verifier's
dilemma**: rational participants can be poorly incentivized to perform costly
verification when they benefit from accepting work without checking it.

Truebit subsequently made the same incentive problem operational. Its
verification design uses randomly injected **forced errors** so that a
potential challenger has a non-negligible chance of finding an error and
earning a reward. In the language of the present toy model, that mechanism
acts on the experienced incidence of detectable faults rather than merely
adding nominal monitors.

These precedents mean that neither "rare faults select weak checking" nor
"injecting detectable faults can support checking incentives" should be
reported here as new.

## 3. Bistability and hysteresis in commons are established

Closing social and ecological feedback loops can produce multiple stable states,
tipping and hysteresis in common-pool-resource models. Relevant examples
include:

- A. Richter, D. P. van Soest and J. Grasman (2013), *Contagious cooperation,
  temptation, and ecosystem collapse*, Journal of Environmental Economics and
  Management 66(1):141-158, DOI 10.1016/j.jeem.2013.04.004. Their coupled
  resource/social-norm model generates endogenous erosion of cooperation,
  alternative stable states and hysteresis.
- S. Sarkar (2023), *Managing ecological thresholds of a risky commons*,
  Royal Society Open Science 10:230969, DOI 10.1098/rsos.230969, which studies
  monostability, bistability and tipping in a common-resource model.
- Recent coupled cooperation-resource models likewise report bistability and
  resource collapse under feedback between environmental state and behavior.

Therefore the existence of a fold, alternative stable states, or hysteresis in
Experiment 2 is not by itself a novelty claim. The question is whether the
specific distributed-control composition here — costly verification,
selected-versus-sufficient monitoring, common-mode failure, endogenous
producer response and state-dependent corrective capacity — yields useful
boundaries or observables not already contained in those literatures.

## 4. Critical slowing down is established early-warning theory

As a fold is approached, recovery from small perturbations slows because the
dominant local multiplier approaches one. Scheffer et al. (2009), *Early-warning
signals for critical transitions*, Nature 461:53-59, DOI 10.1038/nature08227,
reviewed critical slowing down and associated early-warning signals across
complex systems.

Experiment 2 therefore does not claim critical slowing down as new. Its exact
model-specific identity

\[
1-M=\gamma(1-\eta)
\]

shows how the distributed-control loop gain maps onto that established
quantity. It also clarifies a limitation: slowing down in the current commons
state detects nearness to the local fold, but does not by itself measure a
separate stock of dormant corrective capacity.

## 5. Current research boundary

The next question is not whether correlation leaves a floor at fixed harmful
attempt rate \(b\). It is what happens when the attempted-harm rate is itself
a response to the distributed controller.

In the declared adaptive model,

\[
b_t^*=\sigma\!\left(\frac{g-\ell d_t}{T}\right),
\qquad
d_t\le 1-\rho.
\]

Therefore the producer target is bounded below by its response at maximal
achievable detection. Partial adjustment then gives a finite-time lower
envelope for \(b_t\), and the static common-mode floor converts this into an
endogenous lower envelope for harmful finalization.

That coupled result is proved in `formalization/EndogenousFloor.lean` at the
level of any producer response antitone in detection and specialized to the
logistic response in the executable model. Whether this exact coupled theorem
is novel relative to inspection-game, security-game and reliability
literatures remains a literature question; the repository does not currently
claim priority.

## 6. Why this distinction matters

The intended research sequence is:

\[
\text{recover known limit}
\rightarrow
\text{couple feedback loops}
\rightarrow
\text{derive new phase structure}
\rightarrow
\text{test whether it survives richer incentives and substrates}.
\]

Recovering established results is useful evidence that the abstraction is
well anchored. Novelty, if present, must come from what the coupled model adds
beyond those baselines.
