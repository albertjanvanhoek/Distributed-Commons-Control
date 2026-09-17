# Recurrent-maintenance extension

This branch adds a fourth analytical layer to the JAM/ELVES correlated-honest-failure paper.

The existing paper separates:

1. verdict attribution;
2. event-level corrective reproduction;
3. sampling dilution.

The extension adds:

4. **cross-time reproduction of corrective capacity**.

The new section deliberately does not claim that the slow-loop coefficients are specified by the Gray Paper. It uses them as explicit interface parameters for delegated staking, operator, client, and ecosystem functions.

The main formal distinction is:

\[
\lambda_x>1
\quad\not\Leftrightarrow\quad
\mathcal R_M>1.
\]

See `sections/08_recurrent_maintenance.tex`, the paper `CLAIMS.md`, and `formalization/JamRecurrentMaintenance.lean`.
