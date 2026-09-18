# ADR-25: Reflexive Repair Loop

## Status
Accepted

## Context
Standard agentic workflows rely on probabilistic generation (System 1) which often produces syntactically invalid or logically contradictory outputs. When error handling is treated as an exceptional state or relies on manual human debugging, the system becomes fragile. To enforce technical determinism, logical consistency, and semantic alignment within autonomous agentic systems, we need a formalized, self-correcting cognitive architecture.

## Decision
We formally adopt the **Reflexive Repair Loop** architecture and implement the `ReflexiveRepairAgent`.

**What:** The Reflexive Repair Loop is a dual-system, two-speed cybernetic control loop bridging the probabilistic, pattern-matching nature of LLMs (System 1) and the rigid, rule-based verification of deterministic engines (System 2). It integrates active interdiction, automated feedback injection, and bounded self-correction into the agent's execution lifecycle.

**Why:** It systematically strips away stochastic volatility to produce validated, production-ready outcomes by transforming errors into Logic Violation Reports (LVRs) and applying Reflexive Prompt Injection to steer generation away from failed coordinates.

**How:**
1. **Hypothesis Generation (System 1):** The LLM proposes a candidate solution.
2. **Symbolic Interdiction (System 2):** Deterministic verifiers (linters, SAT solvers) intercept the payload.
3. **Fault Detection:** If a Semantic Integrity Constraint (SIC) is violated, execution halts and a Logic Violation Report (LVR) is generated.
4. **Reflexive Prompt Injection:** The LVR is converted into an explicit Negative Constraint and re-injected to the model.
5. **Bounded Iteration:** The agent attempts a repair, bounded to a maximum of 3 iterations.
6. **Epistemic Escrow:** If unresolved after 3 attempts, or if the Confidence-Fidelity Divergence (CFD) threshold is exceeded, the system halts, locks the state, logs a Symbolic Scar to the Scar Tissue Archive (STA), and escalates to Human-in-the-Loop (HITL).
7. **Dynamic CFD Thresholding:** The threshold adjusts based on context (e.g., tightened to 0.1 for state-mutating actions, relaxed to 0.8 for read-only actions).

## Consequences
- **Positive:** Eradicates recurring logical/syntax errors, prevents "agent thrashing" (via the 3-attempt limit), and immunizes the system against repetitive failures through Failure-Informed Prompt Inversion (F-IPI).
- **Negative:** Increased complexity in error handling and potential latency overhead during the repair iterations. Requires sophisticated deterministic verifiers tailored to the execution context.
