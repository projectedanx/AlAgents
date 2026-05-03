# Architecture Decision Record: 15 - VULCAN Agent Architecture

## Context
Standard agentic workflows often fail to maintain strict architectural boundaries when designing distributed systems. They tend to resolve contradictions by hallucinating shared databases or overly complex microservices ("Semantic Saponification"). We need a system that enforces rigid structural boundaries (Mereological Mandate, Shared Database Anathema, NFR Gates) prior to any code generation.

## Decision
We formally integrate the **VULCAN (Vector-Unified Logical Computing Architect Node)** agent into the conceptual synthesis pipeline. VULCAN operates at Tier 3 Autonomy, serving as the topological router and architectural enforcer.

## Mechanics
- **Adjectival Bounds:** VULCAN actively strips marketing noise ("scalable", "seamless") from requirements to evaluate raw Non-Functional Requirements (NFRs).
- **NFR Gates:** The agent defaults to a Modular Monolith architecture unless the NFRs (scale diff, deploy cadence diff, team separation, failure isolation) mathematically justify microservices.
- **Topology Mapping:** VULCAN computes Directed Acyclic Graphs (DAGs) to identify Gravity Wells (high in-degree) and Blast Radius (nodes affecting >20% of system).
- **Epistemic Escrow:** Violations of physical laws (e.g., CAP Theorem) or strict anti-patterns (Shared Databases) trigger a halt and request for human context instead of allowing hallucinated resolutions.

## Consequences
- Upstream requirements must be clear on NFR constraints.
- Prevents the Sycophantic Attractor from suggesting unnecessary cloud-native Bricolage.
- Mandates the generation of rigid ADRs, C4 Models, and DDD Context Maps before downstream agents begin coding.
