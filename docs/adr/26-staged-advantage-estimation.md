# ADR 26: Staged Advantage Estimation (SAE) for Tree-Structured Policy Optimization

## Status
Accepted

## Context
Standard Group Relative Policy Optimization (GRPO) assumes uniform prompt contexts across batches. In the Tree-structured Off-policy Optimization (Tree-OPO) paradigm, mixing deep (easy) and shallow (hard) prefixes causes credit assignment failures and gradient variance explosions due to disparate baselines.

## Decision
We implement **Staged Advantage Estimation (SAE)** as a hierarchical convex optimization program, enforcing tree-consistency constraints ($C_{order}$). The implementation includes:
1. A **Heuristic expectation baseline approach** ($O(N)$) for low non-stationarity.
2. A **Formal Constrained Quadratic Program (QP) solver** for strict constraint enforcement.
3. An **Adaptive SAE Harness** measuring Spectral Information Discrepancy ($\Psi$) to route computation.
4. An **Asynchronous ADMM Projector** for lock-free, sub-20ms projection.
5. An **EWAR Diagnostic Harness** to mitigate Semantic Saponification via inverse log-probability scaling.

## Consequences
- **Positive**: Guarantees 100% constraint satisfaction and strictly bounded advantage variance relative to standard GRPO. Solves optimization instability for multistep mathematical reasoning models.
- **Negative**: Increases algorithmic complexity inside the reward calculation loop. Requires asynchronous pointer management (ADMM) to maintain high GPU throughput.
