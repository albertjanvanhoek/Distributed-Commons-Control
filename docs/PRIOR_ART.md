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

## 3. Current research boundary

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

## 4. Why this distinction matters

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
