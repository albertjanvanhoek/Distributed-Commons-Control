# Experiment 4 — when induced behavior reverses participant contribution

## 1. Question

Experiment 3 established a structural monotonicity result: in a one-loop
coverage model, adding a participant cannot reduce the viability margin if the
existing action profile is held fixed.

Experiment 4 asks the next question:

> Can adding a participant improve the network directly, yet reduce realized
> viability after the participants adjust their behavior to one another?

The model is deliberately substrate-neutral. It is a possibility theorem for
participant/network interaction, not a JAM incentive model.

## 2. Minimal shared-reward game

Harmful events occur with rate \(b\). A participant who checks a harmful event
shares a fixed reward \(r\) equally with any other participants who also check.
Participant \(i\) pays quadratic effort cost

\[
\frac c2 q_i^2.
\]

Define the dimensionless one-participant selection intensity

\[
\boxed{
z=\frac{br}{c}.
}
\]

We work first in the interior regime \(0<z<1\).

### 2.1 One participant

The utility is

\[
U_1(q)=brq-\frac c2q^2,
\]

so

\[
\boxed{q_1^*=z.}
\]

### 2.2 Two participants

If the other participant checks with probability \(q\), then conditional on
checking oneself:

- with probability \(1-q\), one receives the whole reward;
- with probability \(q\), one receives half.

Expected reward share is therefore

\[
1-\frac q2.
\]

The interior best response is

\[
q_i=z\left(1-\frac q2\right).
\]

At a symmetric equilibrium,

\[
q_2^*=z\left(1-\frac{q_2^*}{2}\right),
\]

hence

\[
\boxed{
q_2^*=\frac{2z}{2+z}.
}
\]

The fixed-point identity is machine-checked in
\`formalization/SelectedViability.lean\`.

## 3. Declared viability margin

For safety target \(\varepsilon\), define

\[
\boxed{
M=\varepsilon-P_{\rm harm}.
}
\]

Thus \(M>0\) is safe, \(M=0\) is the declared boundary, and \(M<0\) violates
the target.

With independent checking decisions,

\[
P_{\rm harm}=b\prod_i(1-q_i).
\]

### 3.1 Existing one-participant network

\[
M_1^*
=
\varepsilon-b(1-z).
\]

### 3.2 Add a participant, freeze behavior

If a second participant is added and both participants continue checking at
the incumbent effort \(z\),

\[
M_{2,\mathrm{frozen}}
=
\varepsilon-b(1-z)^2.
\]

Therefore the direct contribution is

\[
\Delta M_{\rm direct}
=
M_{2,\mathrm{frozen}}-M_1^*
=
\boxed{
bz(1-z)>0.
}
\]

So the participant is unambiguously beneficial at the direct structural layer.

### 3.3 Let both participants re-equilibrate

After reward sharing changes their incentives,

\[
M_2^*
=
\varepsilon
-
b\left(
\frac{2-z}{2+z}
\right)^2.
\]

The total addition effect is

\[
\Delta M_{\rm selected}
=
M_2^*-M_1^*
=
-\frac{
bz(z^2+4z-4)
}{
(2+z)^2
}.
\]

Therefore

\[
\boxed{
\Delta M_{\rm selected}<0
\iff
z^2+4z-4>0.
}
\]

The positive root is

\[
\boxed{
z_c=2(\sqrt2-1)\approx0.828427.
}
\]

Thus, for sufficiently strong one-participant selection, adding another
participant is directly helpful but reduces realized viability after
re-equilibration.

The polynomial form and sign reversal are machine-checked in Lean.

## 4. Exact decomposition

Define the induced-response term

\[
\Delta M_{\rm induced}
=
M_2^*-M_{2,\mathrm{frozen}}.
\]

Then

\[
\boxed{
\Delta M_{\rm selected}
=
\Delta M_{\rm direct}
+
\Delta M_{\rm induced}.
}
\]

In the reversal region,

\[
\Delta M_{\rm direct}>0
\quad\text{but}\quad
\Delta M_{\rm induced}<-\Delta M_{\rm direct}.
\]

The participant is therefore not "harmful" in itself. The negative total
contribution is produced by the network response to its presence.

## 5. Concrete counterexample

Take

\[
b=0.2,\qquad
\varepsilon=0.025,\qquad
z=0.9.
\]

Then

\[
q_1^*=0.9,
\qquad
q_2^*=\frac{1.8}{2.9}\approx0.62069.
\]

The margins are

| state | margin |
|---|---:|
| one participant, selected | \(+0.00500\) |
| two participants, frozen at \(q=0.9\) | \(+0.02300\) |
| two participants, selected after re-equilibration | \(-0.003775\) |

So the added participant has

\[
\Delta M_{\rm direct}=+0.018,
\]

but

\[
\Delta M_{\rm selected}\approx-0.008775.
\]

The system moves from safe to unsafe only because the behavioral response
more than cancels the direct benefit.

## 6. Equivalent cost-robustness boundary

Let

\[
x=\frac{\varepsilon}{b}.
\]

At the safety boundary, the maximum effort-cost coefficient compatible with
selected safety is

\[
c_{\rm crit,1}
=
\frac{br}{1-x}
\]

for one participant, and

\[
c_{\rm crit,2}
=
\frac{br(1+\sqrt{x})}{2(1-\sqrt{x})}
\]

for two participants.

Hence

\[
\boxed{
\frac{c_{\rm crit,2}}{c_{\rm crit,1}}
=
\frac{(1+\sqrt{x})^2}{2}.
}
\]

Therefore the two-participant selected system tolerates less effort cost than
the one-participant system when

\[
\boxed{
x<(\sqrt2-1)^2
\approx0.171573.
}
\]

This is the same reversal boundary expressed in target space.

## 7. What is and is not being claimed

The mechanism is an abstract shared-reward game. It is **not** JAM's auditing
incentive mechanism.

The result is a possibility theorem:

\[
\boxed{
\text{positive direct participant contribution need not imply positive
re-equilibrated contribution.}
}
\]

The contribution sign is therefore a property of the participant-network
relation under a declared response rule, not a fixed property of the
participant.

This is consistent with the broader prior-art lesson that indirect and
behavioral responses can change removal/addition effects. The new role of this
experiment inside the repository is narrower: it connects that idea to the
same declared viability margin used in Experiment 3 and supplies an exact
sign-reversal boundary.

## 8. Next step

The next neutral dynamic extension can now introduce a slow corrective-capacity
stock \(C\) without conflating it with fast effort.

The intended state becomes

\[
(X,C),
\]

with viability margin

\[
M(X,C).
\]

The key test will be whether capacity can decay while \(X\) remains apparently
healthy, so two systems with the same current shared state and similar local
recovery rate can nevertheless tolerate different shocks.
