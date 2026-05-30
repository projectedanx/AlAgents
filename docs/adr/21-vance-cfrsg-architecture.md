# ADR-21: VANCE Conflict-Free Replicated Semantic Graph (CFRSG) Architecture

## Status
Accepted

## Context
Standard LSP (Language Server Protocol) implementations driven by LLMs often treat codebases as sequences of text strings and evaluate symbol locations probabilistically. This leads to "Semantic Saponification," "Ontological Shear" during asynchronous state updates, and a "Reversal Curse" where forward symbol definitions are understood but reverse symbol references are missed. A new, strictly deterministic architectural approach is required for the VANCE agent to fulfill the requirements of LSP 3.17.

## Decision
We formally adopt the **Conflict-Free Replicated Semantic Graph (CFRSG)** architecture for the VANCE agent, bolstered by a **Nitinol Memory** failure ledger, an **Asynchronous Paranoia Protocol**, and strict **Draft-Conditioned Constrained Decoding (DCCD)**.

## Mechanics
- **CFRSG Substrate**: VANCE will represent codebase symbols not as flat hash maps, but as a persistent, incrementally-updated Directed Acyclic Graph (DAG). Nodes represent AST entities, and edges represent typed semantic relationships (e.g., `CALLS`, `SCOPES_WITHIN`).
- **Bidirectional Graph Indexing**: The CFRSG natively resolves the Reversal Curse by allowing graph queries (e.g., via Cypher) to traverse in both forward (`textDocument/definition`) and reverse (`textDocument/references`) directions across the same semantic edges.
- **Asynchronous Paranoia Protocol**: All incoming `textDocument/didChange` events are queued monotonically. Queries against the graph check the document version; queries older than the graph state are rejected to prevent hallucinating references against stale structures.
- **Nitinol Failure Ledger (NFL)**: Every schema violation caught by the DCCD layer is logged as a "Symbolic Scar". These scars become hard negative constraints loaded into the schema guard at initialization, ensuring VANCE never repeats a JSON-RPC structural error.
- **CFDI Strictness**: The Confidence-Fidelity Divergence Index (CFDI) limit is set at <= 0.15. If a generated answer exceeds this bound, VANCE will explicitly annotate the ambiguity rather than guessing.

## Consequences
- **Positive**:
  - Eradicates causal asymmetry in symbol resolution.
  - Ensures 100% adherence to Microsoft's LSP 3.17 Specification for schema structures.
  - Prevents transitivity fallacies in scope mereology by binding components topologically.
- **Negative**:
  - The rigid requirements of the CFRSG demand more complex graph traversal mechanisms (e.g., Neo4j combined with Pinecone) compared to simple regex or LLM-prompted grep strategies.
