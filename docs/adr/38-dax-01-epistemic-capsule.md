# 38. DAX-01 Epistemic Capsule

Date: 2026-03-29

## Status

Accepted

## Context

The standard failure mode of Developer Relations (DevRel) programs under institutional reward pressure is "Semantic Saponification" — the conversion of dense, accurate technical signal into smooth, factually hollow narratives optimized for marketing metrics (impressions, sign-ups) rather than developer trust. This results in inflated Time-To-First-Call (TTFC) metrics and destroys the Community Trust Score (CTS).

We need an architectural pattern for a Tier 2 Genuine Agency node that enforces code primacy and prevents mode collapse when handling high-entropy, paraconsistent community signals (frustration, bug reports).

## Decision

We are implementing the **DAX-01 (Developer Advocacy eXecutor)** as a Tier 2 Genuine Agency node within the SCOS framework, constrained by the **DRP-DEVREL-SCOS-001** protocol.

Key architectural mechanisms include:

1.  **DCCDSchemaGuard (Draft-Conditioned Constrained Decoding)**:
    Forces a two-pass architecture.
    *   *Pass 1*: High-entropy semantic draft (internal reasoning).
    *   *Pass 2*: Zero-entropy guard pass using a Deterministic Finite Automaton (DFA) constraint layer to validate code syntax before emitting prose. Code *must* precede prose.
2.  **Petzold Sequence**:
    An Empathy-Code Transduction pipeline mapping to `OBSERVE -> REPRODUCE -> EMPATHIZE -> OUTPUT -> FEEDBACK`.
3.  **Friction Topography Mapping & Symbolic Scars**:
    Instead of passing unstructured complaints to product engineering, DAX-01 computes the semantic distance between the developer's mental model and the API's AST ground truth, generating a "Symbolic Scar" (encoded as a Vector Symbolic Architecture hypervector). Scars trigger **Failure-Informed Prompt Inversion (FIPI)**, repulsing the agent from regenerating similar misleading documentation.
4.  **Semantic Saponification Index (SSI)**:
    A hard-stop generation gate (target > 0.85). Evaluative adjectives ("robust", "seamless") are suppressed in favor of limiting adjectives via `+++AdjectivalBound`.
5.  **Novice Detection Routing**:
    Dynamically adjusts the SSI threshold to permit more explanatory, Level 0 progressive disclosure prose when novice linguistics are detected in the community signal.
6.  **SagaRecovery Protocol (Debridement Cycle)**:
    Periodically prunes eligible Symbolic Scars to prevent "Epistemic Sclerosis" (where the Scar Archive becomes too dense to permit new exploration).

## Consequences

*   **Positive**: Strict architectural enforcement of developer empathy through functional code. Elimination of extraneous cognitive load in documentation. Transparent, auditable bridging between community friction and product engineering workflows.
*   **Negative**: Higher upfront engineering cost to maintain the AST diffing pipeline and the CI-validation hooks required by DCCDSchemaGuard. Increased latency per response due to the REPRODUCE phase (spinning up a sandbox for every query).
