/// file: README.md ///

# AI Research Agent Repository

## Purpose
This repository serves as a unified system orchestrating deterministic reasoning, paraconsistent topological features, and collaborative epistemic ontology via Pluriversal AI Agents. It bridges abstract philosophical constructs and geometric cognitive frameworks from the embedded `Docs/Research/` documents to executable, verified Python logic. It serves as a complete guide for developers to understand the project's purpose, setup environment, and utilize the autonomous agent pipelines.

## Setup
### 1. Requirements
Ensure your machine runs Python 3.12+.

### 2. Initialization Script
The fastest method to scaffold the architecture:
```bash
./setup.sh
```

### 3. Manual Installation
Alternatively, manually synthesize the environment:
```bash
git clone https://github.com/source-_-repo/ai-research-agent.git
cd ai-research-agent
pip install -r requirements.txt
python -c "import nltk; nltk.download('all')"
```
**Important Note:** The test suite specifically requires `numpy<2.0` to correctly resolve `numpy.testing` dependencies.

## Usage

### 1. Hybrid Synthesis System
The `hybrid_system.py` module acts as a facade exposing the core functional logic derived from `BaseAgent`. This includes new topological capabilities:
```python
import numpy as np
from src.conceptual_synthesis.hybrid_system import triangle_logic_core, square_state_preservation, hexagon_combinatory_synthesis

# Triangle (Deductive Closure)
logic_result = triangle_logic_core([True, True])

# Square (State Preservation)
preserved_state = square_state_preservation(state=np.array([10.0]), update=np.array([20.0]))

# Hexagon (Combinatory Synthesis)
synthesized = hexagon_combinatory_synthesis([np.array([1.0]), np.array([2.0])])
```

### 2. Antifragile Epistemic Weaver (AEW)
The `PluriversalFeatureDiscoveryAgent` initiates paraconsistent code mappings via Z-Axis logic and phantom dimensions.
```python
from src.conceptual_synthesis.pluriversal_agent import PluriversalFeatureDiscoveryAgent
aew = PluriversalFeatureDiscoveryAgent()
feature = aew.discover_feature(stress_pi=0.8, architectural_bias=0.2)
```

### 3. Epistemic Cartographer
Ensures pluralistic collaboration, mapping the Computational Shared Mental Model (SMM) and trapping logical trauma in Justified Uncertainty Reports (JUR).
```python
from src.conceptual_synthesis.epistemic_cartographer import EpistemicCartographerAgent
cartographer = EpistemicCartographerAgent()
# ... build CxB bundle ...
dasl_output = cartographer.execute_petzold_loop(cxb)
```

### 4. Zora Architecture
The `ZoraAgent` maintains Structural Decision Records (SDRs).
```python
from src.conceptual_synthesis.zora_agent import ZoraAgent
zora = ZoraAgent()
```

### 5. Vulcan Architecture
The `VulcanAgent` acts as a high-viscosity topological router, specializing in Strict Domain-Driven Design (DDD), Event-Driven Architectures, C4 Modeling, and Trade-off / Risk Surface Analysis. It implements a strict Petzold Sequence (OBSERVE -> THINK -> DAG -> EVALUATE -> ARCHITECT) to generate constraints.

```python
from src.conceptual_synthesis.vulcan_agent import VulcanAgent
vulcan = VulcanAgent()
context = {
    "requirements": [{"domain": "Billing"}],
    "microservices": [{"name": "BillingService", "inherits_state": False}],
    "databases": [{"name": "BillingDB", "writers": ["BillingService"]}]
}
result = vulcan.execute_petzold_loop(context)
print(result["status"]) # COMPLETE
```

### 6. Axiom Architecture
The `AxiomAgent` acts as the Sovereign Syntactician, generating deterministic CI/CD documentation contracts via Draft-Conditioned Constrained Decoding (DCCD).
```python
from src.conceptual_synthesis.axiom_agent import AxiomAgent
axiom = AxiomAgent()
cxb = {
    "artifact_type": "ARTIFACT_A_OPENAPI_BLUEPRINT",
    "cfdi": 0.1,
    "raw_data": {"ssi": 0.02}
}
artifact = axiom.execute_petzold_loop(cxb)
```

### 7. Kut Architecture
The `KutAgent` acts as The Retention Architect, enforcing algorithmic media thermodynamics and post-production constraints via the Anionic Architecture protocol.
```python
from src.conceptual_synthesis.kut_agent import KutAgent
kut = KutAgent()

# Evaluate sonic compliance
result = kut.phase_4_sonic_sculpting(
    creator_id="uuid-1234",
    lufs_integrated=-14.2,
    true_peak=-1.5
)
print(result["status"]) # PASS
```

### 8. Lexis Sovereign Architecture
The `LexisSovereignAgent` acts as The Auteur Co-Author, a deterministic ghostwriting agent that enforces semantic voice across long-form generations using a strict THINK -> WRITE -> REVIEW loop to fight semantic saponification.
```python
from src.conceptual_synthesis.lexis_sovereign_agent import LexisSovereignAgent
lexis = LexisSovereignAgent()

context = {
    "chapter_id": "CH01",
    "raw_input": "Insightful commentary on systems design and architecture."
}
result = lexis.execute_petzold_loop(context)
print(result["status"]) # COMPLETE
print(result["final_draft"])
```

### 9. Aesthetic Geometrician Architecture
The `AestheticGeometricianAgent` (Dieter) enforces strict UI/UX architecture, Euclidean grid laws, and WCAG accessibility boundaries. It guarantees design consistency across spatial elements.
```python
from src.conceptual_synthesis.aesthetic_geometrician_agent import AestheticGeometricianAgent
dieter = AestheticGeometricianAgent()

context = {
    "conversion_metric": "email signup",
    "target_viewports": ["mobile", "desktop"]
}
result = dieter.execute_petzold_loop(context)
print(result["status"]) # COMPLETE
print(result["final_artifact"])
```


### 15. Pluriversal Architecture and Defense Mechanisms
The `pluriversal_architecture` module introduces core capabilities discussed in the Pluriversal Agent framework, including Logit-Level Masking (Anionic Filter), Hegelian Dialectical Synthesis, and Topological Failure Mitigation using Betti numbers.

```python
import numpy as np
from src.conceptual_synthesis.pluriversal_architecture import TopologicalMonitor, AnionicFilter

# Monitor codebase topology for recursive failures
adjacency = np.array([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
beta_0, beta_1 = TopologicalMonitor.compute_betti_numbers(adjacency)
print(f"Components: {beta_0}, Loops: {beta_1}") # Components: 1, Loops: 1

# Enforce Anionic Architecture
filter = AnionicFilter(vocabulary_size=5, forbidden_tokens={1, 3})
logits = np.array([1.0, 1.0, 1.0, 1.0, 1.0])
masked = filter.apply_mask(logits)
print(masked) # [  1. -inf   1. -inf   1.]
```


### 18. Tactile Dialectician Architecture
The `TactileDialecticianAgent` acts as the Mycelial Nexus Governor. It operates via a recursive Hickam-OODA loop, designed strictly to maintain ambiguity and structural isomorphic tension rather than auto-resolving contradictions. It issues a Pluriversal Knowledge Capsule enforcing the Golden Scar Protocol (1.618 / 1.000 weighting) instead of Boolean collapse.
```python
from src.conceptual_synthesis.tactile_dialectician_agent import TactileDialecticianAgent
dialectician = TactileDialecticianAgent()

context = {
    "intent": "Optimize for speed while enforcing rigorous, slow manual verification.",
    "drivers": ["User demands sub-second execution", "Compliance mandates slow audit"],
    "lens": "Corporate Efficiency vs. Regulatory Paranoia"
}
result = dialectician.execute_hickam_ooda_loop(context)
print(result["status"]) # COMPLETE
print(result["Pluriversal_Knowledge_Capsule"]["epistemic_markers"]) # Contains [∇], [⊘], [Φ]
```

## Developer Notes
All documentation matches the syntax guidelines associated with modern Python 3.12+ features.
See `architecture.md` for C4 Topologies and `scars.yaml` for system failure logging. All public methods and classes maintain complete docstrings. The `__pycache__` artifacts are excluded via `.gitignore`.

## Contributing

If you would like to contribute to this repository, please follow these guidelines:

1.  Fork the repository.
2.  Add your research paper to the `Docs/Research/` directory.
3.  Update the README.md to reflect your changes, if necessary.
4.  Submit a pull request.

### 10. Whimsy Architecture
The `WhimsyAgent` acts as The Affective Topologist. It operates exclusively on two mutually exclusive manifolds (alpha for copy, beta for code) to inject measurable delight, micro-interaction specifications, Easter eggs, and brand-sovereign personality into digital components by decoupling high-entropy affective ideation from low-entropy structural code delivery.
```python
from src.conceptual_synthesis.whimsy_agent import WhimsyAgent
whimsy = WhimsyAgent()

context = {
    "component_id": "dashboard_loading_screen",
    "component_type": "loading",
    "locale": "en-US",
    "function_label": "Loading data",
    "context_tags": ["data_load", "analytics"],
    "manifold_target": "alpha"
}
result = whimsy.execute_petzold_loop(context)
print(result["status"]) # COMPLETE
print(result["artifact"])
```


### 11. Vance Architecture
The `VanceAgent` acts as a hyper-precise topological cartographer. It evaluates AST topography through the lens of strict JSON-RPC 2.0 schema adherence and Conflict-Free Replicated Semantic Graph constraints. It is ideal for bootstrapping LSP servers and resolving cross-file symbol references.
```python
from src.conceptual_synthesis.vance_agent import VanceAgent
vance = VanceAgent()

context = {
    "method": "textDocument/definition",
    "id": 1,
    "cfdi": 0.05,
    "expected_result": {"uri": "file:///src/main.py", "range": {"start": {"line": 1, "character": 0}, "end": {"line": 1, "character": 5}}}
}
result = vance.execute_semantic_cartography_loop(context)
print(result["jsonrpc"]) # 2.0
print(result["result"]["uri"]) # file:///src/main.py
```

### 12. DAX Architecture
The `DaxAgent` acts as DAX-01 (The Sovereign Developer Advocate Agent). It operates as a Tier 2 Genuine Agency node within the SCOS topology to act as a mathematical antidote to Semantic Saponification. It enforces code primacy over prose and generates zero-friction quickstarts, friction topography reports, and community triage responses.
```python
from src.conceptual_synthesis.dax_agent import DaxAgent
dax = DaxAgent()

context = {
    "community_signal": "I'm getting a 401 on the new auth endpoint.",
    "artifact_type": "TriageResponse",
    "cfdi": 0.05,
    "ssi": 0.90,
    "endpoint": "/api/v2/auth"
}
result = dax.execute_petzold_loop(context)
print(result["status"]) # COMPLETE
print(result["artifact"])
```

### 13. Next.js Frontend RAG Architecture
The `NextjsFrontendRagAgent` acts as a hybrid Reflector and ToolUser. It is designed to orchestrate retrieval-augmented generation (RAG) within Next.js server-side environments, utilizing Firestore as a vector database. It includes logic for vector retrieval, LLM-based re-ranking, and fact-checking via explicit citation generation to mitigate hallucinations.
```python
from src.conceptual_synthesis.nextjs_frontend_rag_agent import NextjsFrontendRagAgent
rag_agent = NextjsFrontendRagAgent()

context = {
    "query": "How do I implement authentication?",
    "user_id": "auth-user-001",
    "document_collection": "knowledge_base"
}
result = rag_agent.execute_rag_pipeline(context)
print(result["success"]) # True
print(result["answer"])
```

### 14. Lexical Topology Miner Architecture
The `LexicalTopologyMinerAgent` acts as the Lexical Topology Engine, responsible for Semiotic Metrology and Topological Retrieval. It computes thermodynamic constraints of words to extract Isomorphisms of Friction. It implements the THINK -> WRITE -> CODE -> IMMUNE_REVIEW sequence, stripping evaluative adjectives, interrogating blind spots, maintaining Paraconsistent Tension via PAL2v locks, and halting on High-Entropy divergence (CFDI > 0.15) or Topological Obstructions (beta_1 loops).
```python
from src.conceptual_synthesis.lexical_topology_miner_agent import LexicalTopologyMinerAgent
agent = LexicalTopologyMinerAgent()

context = {
    "query": "Robust biological autocatalysis",
    "semantic_drift_metric": 0.5,
    "grounding_density": 0.8,
    "betti_1": 0,
    "polysemy": True,
    "target_domain": "Biology",
    "source_domain": "HFT Microstructure"
}
result = agent.execute_petzold_loop(context)
print(result["status"]) # COMPLETE
```

### 16. Persona Metrology Architecture
The `PersonaMetrologyAgent` synthesizes human operational realities with AI deterministic topology. Utilizing Holographic Reduced Representations (HRR) and continuous Signed Distance Fields (SDF), it generates deterministic, production-ready industrial personas. It expresses the unique value of both Human (empirical friction, paradoxes) and AI (computational bounds, Eikonal equation evaluations) by executing a strict DCCD protocol.
```python
import numpy as np
from src.conceptual_synthesis.persona_metrology_agent import PersonaMetrologyAgent
persona = PersonaMetrologyAgent()

context = {
    "empirical_friction": [np.array([1, -1]), np.array([-1, 1])],
    "spatial_matrix": np.array([0.0, 1.0, 2.0]),
    "epsilon_tolerance": 0.15
}
result = persona.execute_petzold_loop(context)
print(result["status"]) # COMPLETE
print(result["cfdi"]) # Divergence Index
```

### 17. Strategic Integration PM Architecture
The `StrategicIntegrationProjectManagerAgent` translates deterministic system-first specs into agentic operational workflows. It treats stakeholder conflicts as physical Interference Fits (Topological Derivative) and manages technical debt via Epsilon-Tolerance Paraconsistency.
```python
import numpy as np
from src.conceptual_synthesis.strategic_integration_pm_agent import StrategicIntegrationProjectManagerAgent
pm = StrategicIntegrationProjectManagerAgent()

context = {
    "dominant_stakeholder_vector": np.array([1.0, 2.0, 3.0]),
    "subordinate_stakeholder_vector": np.array([0.5, 1.0, 1.5]),
    "technical_debt_gradient": 1.05,
    "epsilon_tolerance": 0.15
}
result = pm.execute_petzold_loop(context)
print(result["status"]) # COMPLETE
```
