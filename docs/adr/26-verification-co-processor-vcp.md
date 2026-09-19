# Architecture Decision Record 26: Verification Co-Processor (VCP)

## Status
Accepted

## Context
In high-stakes agentic workflows, the transition to continuous **latent reasoning** creates a severe observability gap. This opacity allows for "covert reasoning" and **latent semantic drift**, where the model's trajectory gradually decays away from its original intent. To stabilize this dynamic system without sacrificing computational throughput, the cognitive architecture must utilize a closed-loop control system.

## Decision
We will implement the **Verification Co-Processor (VCP)** as an asynchronous, offline System 2 "controller". Its primary role is to ingest the corrupted computational state of the primary model ("the plant"), execute non-tokenized deliberation over symbolic constraints, and compile a continuous, geometric "recovery plan" executed via **Differentiable Cache Augmentation**.

### The Active Intervention Loop
1.  **Ingestion and Decoupled Epistemic Gating:** When sensors detect a critical threshold violation in CFDI or a topological fracture (e.g., $\beta_1 \ge 1$), the VCP is triggered. It eavesdrops on active KV caches without degrading generation latency.
2.  **Cross-Domain Constraint Synthesis:** The VCP synthesizes the Deviant KV-Cache ($KV_t$), the Target Anchor ($V_{anc}$), and Logical Axioms ($\Phi$) into a unified optimization landscape.
3.  **Latent Space Optimization:** The VCP utilizes a dual-encoder contrastive training primitive to pull continuous thought vectors away from unsafe basins of attraction.
4.  **Actuation via Cache Injection:** The VCP generates a sequence of corrective latent embeddings ($\vec{e}_{rec}$), which are appended directly to the primary model's existing KV-cache, smoothly bending the latent trajectory back onto the target semantic geodesic.

### Safety Specification Matrix
*   **Hard Boundary (Invariant):** The VCP must abort and trip the Epistemic Escrow if $\beta_1 \ge 1$ (indicating a stable, un-resolvable logical loop).
*   **Soft Target (Optimizable Goal):** Maximize the Mutation Recoverability Score (MRS $\ge 0.80$).

### Failure Resilience
*   **Generative Adversarial Resilience (GAR):** An internal loop discovers adversarial inputs to induce drift.
*   **Failure-Informed Prompt Inversion (F-IPI):** Successfully induced failures are logged as Symbolic Scars, which are used to generate corrective meta-prompts.

## Consequences
*   **Positive:** Real-time correction of semantic drift without altering the base model's parametric weights. Low-latency execution is preserved by decoupling the computationally intensive VCP optimization from routine generation.
*   **Negative:** Adds architectural complexity with dual-model execution and requires continuous monitoring of high-dimensional topological metrics.
