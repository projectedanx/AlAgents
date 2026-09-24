# ADR 42: Invariant Verification Harness (IVH)

## Status
Accepted

## Context
When building production-grade AI reasoning harnesses to automate scientific discovery, relying on vague natural language to define "laws" introduces severe over-fitting risks and false consensus loops. A cognitive architecture tends to favor simplicity over high-dimensional accuracy, confusing descriptive laws (the "What") with explanatory theories (the "Why").

Furthermore, models frequently use Fictive Principles (idealized assumptions like "zero friction") that provide non-factive understanding but break down at asymptotic limits.

## Decision
We implement the **Invariant Verification Harness (IVH)** and auxiliary modules to programmatically mine, formalize, and stress-test candidate scientific laws.

1. **Invariant Verification Harness (IVH)**
   - **AnomalyMiner**: Ingests raw data streams and screens for structural anomalies exceeding $3\sigma$ prediction drift.
   - **SymbolicEquationSolver**: Generates parsimonious descriptive laws represented as strongly typed mathematical schemas.
   - **ExplanatoryGraphStructurer**: Builds causal DAGs mapping theories, explicitly penalizing parameter bloat via the `OccamLossCompiler` (Pareto Optimization).
   - **PopperianFalsifier**: Subjects candidate laws to asymptotic edge-case testing, triggering automated model breaking.

2. **Systemic De-Idealization Engine**
   - Formalizes an idealized model as a DAG of simplifying assumptions.
   - Triggers a feedback loop upon $3\sigma$ prediction error divergence from high-fidelity empirical data.
   - Automatically locates the faulty "Fictive Principle" (e.g., zero friction) and "de-idealizes" the model by re-injecting variables to form a higher-dimensional representation.

3. **Cognitive Understanding Compiler**
   - Maintains an ontology of **Fictive Principles** (e.g., Instantaneous Action at a Distance) tracking their utility weight.
   - Calculates a quantitative **Grasping Metric** evaluating the agent's capacity to maintain explanatory utility and manipulate variables despite underlying non-factive approximations.

## Consequences

### Positive
- **Mitigates Over-fitting**: Pareto optimization utilizing Occam Loss forces a selection between epicyclic curve-fitting (Ptolemaic) and fundamental transformations (Keplerian).
- **Automates De-Idealization**: The agent can smoothly transition from an idealized model to a more complex, accurate model at edge cases without full system collapse.
- **Formalizes Epistemology**: Replaces vague natural language science myths with rigorous schemas separating empirical data, descriptive laws, and explanatory theories.

### Negative
- **Computational Overhead**: Simulating causal graphs, continuous falsification limits, and grasping metrics introduces computational complexity during the validation loop.
