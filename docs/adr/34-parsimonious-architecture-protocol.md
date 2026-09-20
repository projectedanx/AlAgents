# ADR 34: Parsimonious Architecture Protocol (PAP)

## Status
Accepted

## Context
In automated scientific reasoning and computational modeling, machine learning systems have a natural bias toward maximum likelihood over-fitting. Models tend to achieve lower residual errors by endlessly multiplying free parameters—a dynamic isomorphic to the "epicyclic curve-fitting" of Ptolemaic geocentrism.

Without structural checks, an AI agent will endlessly complexify its models (adding "Dark Energy" style ad-hoc parameters) to explain anomalies rather than searching for simpler, fundamentally correct coordinate transformations. This results in models that capture localized noise rather than underlying generative signals, severely limiting generalizability.

## Decision
We implement the **Parsimonious Architecture Protocol (PAP)** to enforce **Occam's Razor** programmatically at the structural level.

The protocol utilizes an `OccamLossCompiler` that explicitly penalizes complexity.

### Architecture Specifications
1. **Ontological Commitment Schema**: Every theory must declare its variables, free parameters, and explicit foundational assumptions ($A_i$) along with their validity probability ($P(A_i)$).
2. **Occam Loss Calculation**:
   - A theory's structural joint probability is calculated as $P(T) = \prod_{i=1}^{n} P(A_i)$.
   - Complexity $C(G)$ is defined as a function of the number of free parameters and the assumption penalty ($-ln(P(T))$).
   - Occam Loss is defined as the empirical Prediction Error + Complexity $C(G)$.
3. **Pareto Optimization**: The system performs a gradient descent on the Complexity-Accuracy frontier. Any model that adds free parameters is strictly rejected unless it achieves a statistically significant decrease in prediction error ($\ge 3\sigma$).
4. **Continuous Falsification**: The selected "Simplest Adequate Approximation" is subjected to asymptotic edge-case stress testing, triggering a Modus Tollens anomaly detection if error bounds exceed $3\sigma$.

## Consequences
### Positive
- **Prevents Over-fitting**: Systematically blocks the AI from multiplying parameters to fit noisy data.
- **Enforces Structural Elegance**: Rewards models that explain phenomena through fundamental transformations (e.g., Copernican heliocentrism) over those that rely on nested heuristics.
- **Promotes Generalizability**: Simplest adequate approximations naturally generalize better to unseen data boundaries.

### Negative
- **Risk of Under-fitting**: If the parameter penalty weight is set excessively high, the system may suffer from "greedy reductionism," selecting idealized models that lack predictive veridicality in complex real-world environments.
- **Computational Overhead**: Evaluating the theoretical probability of every independent assumption requires rigorous mapping and increases the computational cost of model selection.
