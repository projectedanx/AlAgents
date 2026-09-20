# ADR 33: Visual Context-to-Execution Pipeline (CxEP) Compiler

## Status
Accepted

## Context
Top-down architectural abstractions and static deliverables handed down by management often suffer from "Intent Drift." Practitioners exhibit a lack of buy-in, and the semantic distance between current operations and the goal vector becomes ambiguous.

The **IKEA Effect** dictates that individuals place significantly higher value on systems they actively participate in constructing. By facilitating collaborative visually-driven environments, teams can co-create their Shared Mental Models (SMMs), minimizing extraneous cognitive load and maximizing germane cognitive load.

However, these visual sketches must be formally translated into executable, mathematically sound code rather than remaining informal diagrams.

## Decision
We implement the **Visual Context-to-Execution Pipeline (CxEP) Compiler** (`VisualCxEPCompiler`).

**What:**
A compiler that translates co-created visual workflow schemas (such as RACI maps or state machines) into executable, typed Product-Requirements Prompts (PRPs) and guarantees structural soundness.

**How:**
1. **Automated Discovery and Constraint Mining:** A Vision-Language Model (VLM) parser (simulated currently as a structural parser) translates visual storyboards into a structured Domain-Specific Language (DSL).
2. **Isomorphic Formalization:** The DSL is compiled into an **Executable Cognitive Contract (PRP)** that explicitly maps every visual task block to a strict, typed output schema.
3. **Speculative Code Generation:** The PRP is passed to a multi-agent generation pipeline to produce code candidates.
4. **Formal Verification Loop:** A **Speculative Abstract Interpretation Engine (SAIE)** runs abstract interpretation sweeps over the generated code to verify compliance with global safety properties (e.g., data residency, preventing direct DB writes).

## Consequences
- **Positive:** Leverages the IKEA Effect to secure high operational buy-in while mathematically guaranteeing that the visual layout adheres to global constraints. Lowers development debt through early falsification.
- **Constraint:** Hard Boundaries (Invariants) must be strictly defined in the SAIE for validation. If a user creates a cyclic deadlock visually, the system must flag a Typological Drift error and request Socratic clarification.
