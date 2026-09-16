# Experiment 12 — fungal flow-coupled maintenance

## 1. Why fungi are the second substrate

The JAM return test was deliberately artificial in one useful sense: it is a
designed protocol with explicit roles, messages, judgments and higher-layer
incentives.

A stronger cross-substrate challenge is a network with:

- no central controller;
- no human moral vocabulary;
- no need to assume cognition;
- continuous physical reconfiguration;
- experimentally observed trade-offs between transport, construction cost and
  resilience.

Cord-forming fungal mycelia provide such a substrate.

The purpose of Experiment 12 is **not** to claim that fungi instantiate SCAP.

It is to ask which parts of the maintenance architecture survive when the
substrate is a self-organised transport network rather than a protocol.

---

## 2. Grounding from fungal network biology

The following are empirical/literature-grounded statements.

### 2.1 Mycelia are adaptive transport networks

Fricker, Heaton, Jones, Boddy and colleagues describe fungal mycelia as
interconnected networks whose structure is tightly linked to resource flows.
Network architecture changes through growth, branching, fusion and regression
in response to local nutritional/environmental conditions, damage and
predation.

The network therefore is not a fixed pipe system.

It is a transport system whose structure changes while it operates.

### 2.2 Flow and structural reinforcement are coupled

Heaton et al. (2010), studying *Phanerochaete velutina*, reconstructed
growth-induced mass flows from measured network development.

Cords predicted to carry faster-moving or larger currents were significantly
more likely to increase in size.

The authors explicitly propose that fluid velocity can act as a **local signal
carrying quasi-global information about the role of a cord within the
mycelium**.

This is the key substrate fact used here.

### 2.3 Networks reinforce routes and recycle material

Fricker et al. describe fungal networks as adapting by selective reinforcement
of major transport routes and recycling redundant intervening mycelium to
support further extension.

Measured nutrient movement is dynamic and may switch between pre-existing
routes.

### 2.4 Robustness is a real network function

The same literature analyses resilience to simulated damage and experimental
attack by grazing invertebrates.

A later comparative network-trait analysis by Aguilar-Trigueros et al. (2022)
found a connectivity gradient:

- highly interconnected networks provide more alternative transport paths and
  greater robustness to damage, at higher construction cost;
- sparsely connected networks occupy the opposite side of that trade-off.

Thus redundancy is not an invented objective for the present model.

It is one experimentally motivated network property among several.

---

## 3. The mapping deliberately changes the "individual"

JAM mapped the local participant to a validator.

That mapping does not transfer literally.

For the fungal substrate:

| Neutral object | Fungal instantiation |
|---|---|
| local participant | cord, hyphal region, or local growth/transport process |
| network | connected mycelium |
| shared enabling state | internal transport/resource-distribution capacity |
| local signal | flow/resource/pressure-related local state |
| maintenance action | growth, thickening, persistence, fusion or regression |
| network-level viability property | continued transport, access, redundancy, resilience, growth |

This gives an immediate conceptual falsification:

\[
\boxed{
\text{the local unit of maintenance need not be an autonomous individual.}
}
\]

The more general primitive is a **local process or network element whose state
changes future network viability**.

That is why the repository continues to use "participant" operationally rather
than biologically.

---

## 4. Minimal two-route model

The empirical data motivate flow-dependent reconfiguration, but do not specify
one universal nonlinear reinforcement law.

The following is therefore a **model extension** used to challenge the neutral
framework.

Consider two equivalent transport routes.

Let

\[
z\in[0,1]
\]

be the fraction of a fixed route-maintenance/allocation budget in route 1.

Route 2 has share

\[
1-z.
\]

The equal state

\[
z=\frac12
\]

is maximally redundant.

---

## 5. Local flow signal

Let

\[
s\in[0,1]
\]

represent the effective contrast sensitivity of the local flow-coupled
maintenance signal.

Define

\[
u_1
=
\frac12+s\left(z-\frac12\right),
\]

\[
u_2=1-u_1.
\]

Interpretation:

- \(s=1\): the local return signal tracks relative route use exactly;
- \(s=0\): route-specific contrast is absent;
- intermediate \(s\): use differences are attenuated.

This is not claimed to be a measured fungal parameter.

It lets us separate route-use contrast from the nonlinearity of reinforcement.

---

## 6. Flow-coupled return

Let

\[
\beta>0
\]

be the elasticity of maintenance allocation to the local use signal.

The preferred new allocation is

\[
\boxed{
A_1(z)
=
\frac{u_1^\beta}
{u_1^\beta+u_2^\beta}.
}
\]

With adjustment fraction

\[
0<\delta\le1,
\]

the route share updates as

\[
\boxed{
z_{t+1}
=
(1-\delta)z_t
+
\delta A_1(z_t).
}
\]

There is no explicit observer and no external reward.

The return loop is physically embedded:

\[
\boxed{
\text{flow/use}
\rightarrow
\text{local signal}
\rightarrow
\text{future structural allocation}.
}
\]

That is the central fungal contrast with JAM.

---

## 7. Exact local result

At

\[
z^*=\frac12,
\]

the derivative of the preferred allocation is

\[
A_1'(z^*)=\beta s.
\]

Therefore the local multiplier of the full update is

\[
\boxed{
M
=
1-\delta+\delta\beta s.
}
\]

Define the effective reinforcement gain

\[
\boxed{
\chi=\beta s.
}
\]

Under

\[
0<\delta\le1,\qquad
\beta\ge0,\qquad
s\ge0,
\]

the multiplier is nonnegative.

Hence

\[
\boxed{
|M|<1
\iff
\chi<1.
}
\]

This is machine-checked in Lean.

So:

\[
\boxed{
\begin{array}{rcl}
\beta s<1
&\Rightarrow&
\text{equal redundancy locally restored},
\\[3pt]
\beta s=1
&\Rightarrow&
\text{neutral local allocation},
\\[3pt]
\beta s>1
&\Rightarrow&
\text{small route asymmetries amplified}.
\end{array}}
\]

---

## 8. Reinforcement can destroy redundancy

For a unit total route allocation, define worst-case backup after loss of the
stronger route as

\[
\boxed{
B(z)=\min(z,1-z).
}
\]

This is maximized at

\[
z=\frac12,
\]

where

\[
B=\frac12.
\]

The maximum result is machine-checked.

A superunit effective reinforcement loop,

\[
\beta s>1,
\]

moves a small perturbed state away from equal allocation.

Consequently the smaller backup route shrinks locally.

Thus the proposition

> stronger positive reinforcement of the most-used route is always better

is false even in this extremely small fungal-inspired model.

The correct statement is viability-indexed:

- concentration may be useful for one objective;
- redundancy is useful for another;
- a scalar global sign requires an explicit objective or weighting.

This is the fungal version of Experiment 7.

---

## 9. Numerical counterexamples

Start from

\[
z_0=0.51,
\qquad
\delta=0.5.
\]

### Sublinear return

\[
\beta=0.8,\quad s=1.
\]

Then

\[
\chi=0.8<1
\]

and the perturbation decays toward

\[
z=\frac12.
\]

Worst-case backup is restored.

### Linear return

\[
\beta=1,\quad s=1.
\]

Then

\[
\chi=1.
\]

The allocation is neutral: the initial imbalance persists.

### Superlinear return

\[
\beta=1.3,\quad s=1.
\]

Then

\[
\chi=1.3>1.
\]

The initially slightly stronger route receives an increasing fraction of future
allocation and backup redundancy declines.

### Same nonlinearity, weaker route contrast

\[
\beta=1.3,\quad s=0.6.
\]

Now

\[
\chi=0.78<1.
\]

The redundant state is again locally stable.

This last comparison is important:

\[
\boxed{
\text{more sensitive selection is not intrinsically better.}
}
\]

A high-gain positive-feedback loop can be stabilised by attenuating its
effective contrast.

---

## 10. Falsification of a separate maintenance-observer requirement

Experiment 11 suggested the candidate stack

\[
\text{state observability}
+
\text{maintenance observability}
+
\text{return-loop closure}.
\]

Fungi force a refinement.

In the Heaton et al. picture, transport flow itself can carry information about
a cord's role in the network, and that same flow is associated with future cord
growth.

So the architecture can be

\[
\boxed{
\text{function}
=
\text{signal}
=
\text{return-coupling input}.
}
\]

A **separate architectural layer** that observes maintenance is therefore not
necessary.

What survives is the more general requirement:

\[
\boxed{
\text{future maintenance must be sufficiently coupled to information about
functional use/contribution.}
}
\]

In JAM this coupling is mediated through judgments, fault records, effort
observation and staking.

In fungi it may be embodied directly in physics and metabolism.

---

## 11. The recursion survives, but in compressed form

The fungal loop is

\[
\boxed{
\text{network structure}
\rightarrow
\text{flow}
\rightarrow
\text{local structural change}
\rightarrow
\text{network structure}.
}
\]

The network's operation supplies information that changes the network.

So there is still a recursive maintenance relation.

But unlike JAM, no explicit meta-agent is required.

This is a useful abstraction correction:

> recursive maintenance does not imply a hierarchy of explicit observers.

Recursion can be embodied in direct dynamical coupling.

---

## 12. What happens to the SCAP-like functions?

### Signal fidelity

Survives, but as a physical coupling rather than propositional honesty.

The relevant question is whether local state carries information useful for
network-level reconfiguration.

### Correction

Survives as reallocation, regression, rerouting, growth and fusion.

There need not be a discrete "error message."

### Reinforcement

Survives strongly as use-dependent persistence/thickening.

But Experiment 12 shows why its gain matters.

### Repair

Exists empirically as network reconfiguration after damage, but is **not**
formalized by the two-route model.

### Reciprocity / return

Survives in transformed form.

There need not be an agent paying another agent.

Resource/flow can return directly into the process maintaining the transport
route.

So "reciprocity" is too anthropomorphic as a primitive.

The more general term is

\[
\boxed{\text{return-loop closure}.}
\]

---

## 13. The "ought before is" interpretation

Experiment 12 gives a particularly clean version of the idea.

Suppose the declared viability property is:

> maintain a locally stable redundant two-route transport architecture.

Before asking what the fungus actually does, the model gives a condition that
any implementation of this particular reinforcement architecture must satisfy:

\[
\boxed{
\beta s<1.
}
\]

That is an **ought-like constraint generated by viability**.

It is not moral.

It means:

> if this property is to persist under this architecture, the effective
> positive-feedback gain must lie in this region.

The logical order is

\[
\boxed{
\text{declared persistence property}
\rightarrow
\text{necessary dynamical condition}
\rightarrow
\text{candidate mechanisms}
\rightarrow
\text{observed implementation}.
}
\]

In the language used elsewhere in Evolution by Emergence:

\[
\boxed{
\text{ONTOLOGICAL / VIABILITY OUGHT}
\rightarrow
\text{RELIABLE IS}
\rightarrow
\text{PRACTICAL OUGHT}.
}
\]

Experiment 12 does **not** establish that \(\beta s<1\) is universally favored
by fungi.

It establishes the conditional statement for the declared redundancy
property.

Other fungal objectives may favor another part of parameter space.

---

## 14. Relation to real fungal trade-offs

This qualification matters because fungal networks do not maximize one thing.

Empirical network-trait work identifies trade-offs involving:

- construction cost;
- transport efficiency;
- connectivity;
- robustness to damage;
- exploration/foraging strategy.

Therefore the relevant biological object is again a viability vector rather
than one scalar optimum.

Experiment 12 isolates only the **redundancy-restoration component**.

A later fungal model could add resource acquisition or construction cost, but
that should be grounded in a specific dataset or experiment rather than added
generically.

---

## 15. Falsification ledger

| Hypothesis | Fungal result |
|---|---|
| Maintenance requires autonomous individual participants | **Falsified as a primitive requirement:** local cords/processes can be the operative units |
| Maintenance observability requires a separate monitoring layer | **Falsified as an architectural requirement:** flow can itself be the local functional signal |
| Stronger positive reinforcement is always better | **Falsified in the model:** \(\beta s>1\) destabilizes equal redundancy |
| Higher signal contrast is always better | **Falsified in the model:** when reinforcement is superlinear, lower contrast can restore redundant stability |
| A maintenance return loop must be social/economic reciprocity | **Falsified by substrate:** return can be physical/metabolic |
| Recursive maintenance requires explicit higher-order observers | **Not supported:** direct flow-structure coupling is recursive without a meta-agent |
| Fungal networks optimize redundancy alone | **Explicitly not claimed:** empirical fungi occupy cost-efficiency-resilience trade-offs |
| The exact nonlinear law \(A\propto u^\beta\) is established fungal physiology | **Not claimed:** it is the falsification model extension |

---

## 16. Prior-art boundary

The following ideas are established and are **not** repository novelty claims:

- fungal mycelia as adaptive transport networks;
- selective reinforcement of major routes;
- recycling/regression of redundant mycelium;
- dynamic switching of transport routes;
- resilience to damage and grazing;
- flow-associated cord thickening;
- nonlinear flux-reinforcement models in adaptive biological networks,
  particularly the related *Physarum* literature;
- efficiency/cost/robustness trade-offs in network architecture.

The contribution of Experiment 12 is the cross-substrate test:

> Does the same viability-maintenance language survive when explicit agents,
> rewards and monitoring are removed?

The answer is partially yes, but only after replacing explicit monitoring and
reciprocity by the more general ideas of **functional signal coupling** and
**return-loop closure**.

---

## 17. Sources

- Heaton, L. L. M., López, E., Maini, P. K., Fricker, M. D. & Jones, N. S.
  (2010). *Growth-induced mass flows in fungal networks*. Proceedings of the
  Royal Society B. DOI: 10.1098/rspb.2010.0735.
- Fricker, M. D., Lee, J. A., Bebber, D. P. & Boddy, L. (2008).
  *The interplay between structure and function in fungal networks*.
  Topologica 1:004. DOI: 10.3731/TOPOLOGICA.1.004.
- Fricker, M. D., Heaton, L. L. M., Jones, N. S. & Boddy, L. (2017).
  *The Mycelium as a Network*. Microbiology Spectrum.
  DOI: 10.1128/microbiolspec.FUNK-0033-2017.
- Aguilar-Trigueros, C. A., Boddy, L., Rillig, M. C. & Fricker, M. D. (2022).
  *Network traits predict ecological strategies in fungi*.
  ISME Communications 2:2. DOI: 10.1038/s43705-021-00085-1.
- Fricker, M. D., Boddy, L., Nakagaki, T. & Bebber, D. P. (2009).
  *Adaptive Biological Networks*. In: Adaptive Networks.
  DOI: 10.1007/978-3-642-01284-6_4.
