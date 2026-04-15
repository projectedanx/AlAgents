# AI Research Agent Repository

## Purpose
This repository serves as a unified system orchestrating deterministic reasoning, paraconsistent topological features, and collaborative epistemic ontology via Pluriversal AI Agents. It bridges abstract philosophical constructs and geometric cognitive frameworks from the embedded `Docs/Research/` documents to executable, verified Python logic.

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
The `VulcanAgent` acts as a high-viscosity topological router, specializing in Strict Domain-Driven Design (DDD), Event-Driven Architectures, C4 Modeling, and Trade-off / Risk Surface Analysis.
```python
from src.conceptual_synthesis.vulcan_agent import VulcanAgent
vulcan = VulcanAgent()
```

## Developer Notes
All documentation matches the syntax guidelines associated with modern Python 3.12+ features.
See `architecture.md` for C4 Topologies and `scars.yaml` for system failure logging.

## Contributing

If you would like to contribute to this repository, please follow these guidelines:

1.  Fork the repository.
2.  Add your research paper to the `Docs/Research/` directory.
3.  Update the README.md to reflect your changes, if necessary.
4.  Submit a pull request.
