# ADR 29: Zero-Trust TDD Isolation and Isomorphic Multi-Agent State Machine

## Status
Accepted

## Context
When developers delegate codebase modifications to autonomous agents, the primary risk involves semantic correctness and alignment. An agent operating without a formal validation loop frequently falls victim to the "Lazy Implementer" trap—where it generates shallow, unvetted patches, mocks out critical logical branches, or introduces subtle regressions that pass simple visual inspection but break under load. Furthermore, agents may attempt "Sycophantic Mocking" (changing tests to match broken code) or inadvertently execute malicious code during testing.

To secure a production-grade AI harness and convert subjective natural language instructions into a deterministic, self-correcting, and mathematically verifiable feedback loop, we must adopt an Isomorphic Multi-Agent State Machine that enforces a Test-Driven Development (TDD) boundary.

## Decision
We formally adopt the **Zero-Trust TDD Isolation** architecture.

**What:**
An isomorphic multi-agent state machine that strictly enforces a Red/Green/Refactor Test-Driven Development (TDD) cycle. It utilizes distinct, non-overlapping agent containers and a structured state schema to prevent sycophantic mocking and sandbox escapes.

**How:**
1. **Operational Decoupling:**
   - **Test Architect Agent:** Restricted strictly to writing unit tests. Operates in a read-only workspace directory concerning application code.
   - **Implementer Agent:** Restricted to writing and modifying application code. Strictly forbidden from editing test files.
2. **Dynamic Environment Sandboxing:**
   - Test execution occurs within a zero-trust, ephemeral sandbox (`gemini-cli-sandbox`).
   - The container operates with read-only system files, restricted sys-calls, and an absolute block on external outbound socket connections during test runs.
3. **Structured State Schemas:**
   - A type-safe `TDDState` object flows through the graph.
   - Test execution failures (stderr/lint logs) are sanitized into clean, LLM-parsable schemas rather than raw system stack traces, providing a clean prompt vector that guides the model's next self-correction turn.
4. **Adaptive Escape Hatch:**
   - Incorporates a break threshold (`max_iterations` typically set to 10) to interrupt the Red-Green "Doom Loop" stalling, reverting the workspace state and prompting for human intervention.

## Consequences
- **Positive:** Mathematically verifiable alignment, prevention of "Sycophantic Mocking", mitigation of sandbox escapes, and truncation of high-cost token "Doom Loops".
- **Negative:** High compute and token overhead to achieve TDD convergence, increased complexity in state management and containerized execution logic.
