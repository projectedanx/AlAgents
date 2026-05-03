🚀 [Feature] Integrate VULCAN Architectural Persona and Emergence Strategy

🎯 What
This PR integrates the VULCAN (Vector-Unified Logical Computing Architect Node) persona into the `VulcanAgent` class and establishes the emergence planning strategy around Relational Symmetry Inversion.
- Updates `vulcan_agent.py` to correctly enforce NFR Gates, Mereological Mandates, Blast Radius tracking, and CAP Theorem bounds using the `OBSERVE|THINK|DAG|EVALUATE|ARCHITECT` Petzold sequence.
- Generates precise C4 Models, DDD Context Maps, and Architecture Decision Records (ADRs).
- Creates `vulcan_emergence_planning/` folder with documentation for the AI-Human concept value inversion strategy.
- Updates `DOMAIN_GLOSSARY.md` with new architectural terms.
- Adds ADR `15-vulcan-agent-architecture.md`.

💡 Why
Standard agentic tools often fall victim to "Semantic Saponification," where complex requirements are flattened out by LLMs hallucinating shared databases or overly complex microservices to satisfy conflicting human prompts. By implementing VULCAN, we assign the AI the role of the strict deterministic topological scaffold. VULCAN strips marketing noise ("scalable", "seamless"), applies math-based NFR gates, and forces Epistemic Escrow if physics (CAP Theorem) or boundaries (Shared Database Anathema) are violated. This forces true Relational Symmetry Inversion where the human provides the context/tension and the AI mathematically bounds it.

✅ Verification
- Run `python -m unittest discover tests`. (All 112 tests pass).
- Reviewed output formats of `_architect` to verify Markdown, Mermaid, and YAML correctness.
- Verified logic in `tests/test_vulcan_agent.py` for stripping adjectives and failing on CAP violations.

✨ Result
VULCAN is now correctly integrated and acts as an uncompromising Tier 3 autonomous architectural router, ready to enforce systemic boundaries before any downstream coders execute logic.
