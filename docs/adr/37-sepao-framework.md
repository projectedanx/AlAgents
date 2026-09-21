# ADR 37: SEPAO Framework for Autopoietic Ontologies

## Status
Accepted

## Context
Codebases and environments are dynamic. The agent's understanding of available APIs and structure must self-heal in response to external modifications without manual intervention.

## Decision
We implement the **Self-Evolving Plugin Affordance Ontology (SEPAO)** framework consisting of:
- **Environment Scanner:** Using static AST analysis.
- **Semantic Delta Mapping:** Calculating graph edit distance and embedding shifts.
- **Failure-Informed Prompt Inversion (F-IPI):** Mutating the `GEMINI.md` constitution in response to verification failures.
- **Metamorphic Invariance Verification:** Ensuring mutations are robust and do not introduce Scar-Induced Rigidity.

## Consequences
- **Positive:** The system continuously re-specifies and heals its own semantic boundaries dynamically.
- **Negative:** F-IPI requires careful tuning of metamorphic tests to prevent over-constraining the agent space.
