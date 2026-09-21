# ADR 35: VCS Layer 3 (The Semantic Layer)

## Status
Accepted

## Context
As the harness transitions from probabilistic interactions to deterministic, production-grade workflows, we require a verifiable policy-enforcement framework.

## Decision
We formally adopt the **Verifiable Cognition Stack (VCS) Layer 3**.
This layer defines a symmetrical relationship between:
1. **Semantic Integrity Constraints (SICs):** The declarative boundary (ASSERT, FORBID, MANDATE) protecting Purpose Fidelity.
2. **Verification Mandates:** The runtime enforcement engine translating constraints into executable tests and linters.

## Consequences
- **Positive:** Ensures correct-by-design workflows. Reduces semantic drift through mathematical verification.
- **Negative:** Increased computational cost via test suite and linter execution, requiring parametric trade-off modeling along the Feasibility Frontier.
