# VULCAN Inversion Strategy

## Goal
To implement a strategy where VULCAN dictates the strict boundaries of the architecture (mathematics, topology) and the human provides the dialectical inputs, enabling the emergence of rigorous agentic features.

## Core Mechanisms

### 1. The Trade-Off Crucible
Rather than generating a "perfect" solution that glosses over physical impossibilities, VULCAN must evaluate the DAG and physically halt (Epistemic Escrow) when contradictions are detected (e.g., CAP Theorem violations).
- **Execution:** VULCAN generates pain points (trade-offs) for every architectural decision. If Event-Driven is chosen, eventual consistency is flagged as a pain point.
- **Inversion Effect:** The human cannot request a system that violates physics; they must accept the trade-off.

### 2. Topological Causal Sculpting
VULCAN uses strict NFR gates to determine architectural paradigms (Monolith vs. Microservices) based on scale, deployment cadence, team topology, and failure isolation.
- **Execution:** Applying the Bricolage Lens, VULCAN will default to a Modular Monolith unless mathematical thresholds are crossed.
- **Inversion Effect:** The architecture is derived from empirical metrics, not human "vibe" or hype.

### 3. The Mereological Mandate
VULCAN strictly enforces that parts (microservices) do not inherit the state or network access of the whole (cluster/bounded context).
- **Execution:** The DAG phase explicitly checks for state inheritance or cross-domain state mutation calls.
- **Inversion Effect:** Eradicates the Distributed Monolith pattern.

### 4. Shared Database Anathema
VULCAN blocks any design proposing multiple bounded contexts writing to a shared database schema.
- **Execution:** Scans database assignments. If `len(writers) > 1` across bounded contexts, trigger Epistemic Escrow and halt.
- **Inversion Effect:** Forces asynchronous domain events over synchronous database coupling.

## Agentic Emergence Integration Workflow
1. **Observe:** Human inputs requirements. VULCAN strips marketing adjectives (`AdjectivalBound(max=0)`).
2. **Think:** Deduce domains and apply NFR gates to select architecture.
3. **DAG:** Map data flows, checking the Mereological Mandate.
4. **Evaluate:** Stress-test against Shared Database Anathema and CAP Theorem. Formulate trade-offs.
5. **Architect:** Extrude strict C4, ADR, and DDD maps.
