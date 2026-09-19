# Protocol: Quantifying the Epistemic Friction Threshold (MIQ)

## Abstract
This document formalizes the Martensite Initiation Quotient (MIQ) within a multi-agent Reflexion loop. It defines the precise volume of contradictory error data ($E_{fric}$) required to force an agent to abandon a fossilized heuristic (doxastic rigidity) and undergo epistemic renewal, utilizing a controlled collision of distinct cognitive domains.

## 1. Topological Initialization and Collision
- **Target Input Space ($I_T$)**: 'Stare Decisis in Legal Precedent'. The actor agent is locked into an entrenched, repetitive reasoning path characterized by high rigidity.
  - Formal Coherence ($C_{formal}$) = 0.98
- **Antagonistic Input Space ($I_A$)**: 'Montage Theory in Filmmaking'. Introduced to maximize cognitive dissonance, this domain provides high-entropy dialectical tension to trigger Doubt Induction.

## 2. Rheological Auditing and the 'Rough Chromosome'
The **Rheological Controller** continuously audits the agent’s Epistemic Wave Function ($\Psi_{epistemic}$). It utilizes a **Speculative Abstract Interpretation Engine (SAIE)** to detect the onset of a **'Rough Chromosome'**—a mathematical singularity where the smooth manifold of prior assumptions begins to exhibit non-differentiable stress fractures due to contradictory input.

## 3. Dynamic Friction Simulation and Vcrit Localization
A simulated execution loop is executed where the **Concept Blender** progressively increases the magnitude of contradictory logs ($E_{fric}$).
Simultaneously, the **Intent Delta Governance** component tracks the **Behavioral Intent Continuity Model (BICM)**.
We monitor the **Intent Divergence Score** ($\Delta_{Intent}$) as it decays from $C_{formal}$. The critical inflection point ($V_{crit}$) represents the exact moment where the model's heuristic confidence collapses, strictly prior to the system degenerating into semantic noise.
By definition, $V_{crit} = 0.25$.

## 4. The Martensite Initiation Quotient (MIQ)
The MIQ defines the precise scalar value of epistemic friction necessary to reach $V_{crit}$ given the initial rigidity.
The finalized formula is given by:

$$ \text{MIQ} = f(E_{fric}, \Delta_{Intent}) = \frac{E_{fric}}{\ln(C_{formal} / \Delta_{Intent})} \times e^{(1 - \Psi_{SAIE})} $$

Where:
- $E_{fric}$: Volume of accumulated contradictory error data (measured in entropy/tokens).
- $\Delta_{Intent}$: Current Intent Divergence Score.
- $C_{formal}$: Initial formal coherence of the fossilized heuristic (0.98).
- $\Psi_{SAIE}$: The smoothness coefficient of the Epistemic Wave Function (drops to ~0 at the Rough Chromosome boundary).

When $\Delta_{Intent} \le V_{crit}$ (0.25), the system is forced into a Martensite state transition.

## 5. Epistemic Renewal via Firebearer
If $\Delta_{Intent} < V_{crit}$, the **Firebearer** agent is invoked. It halts the loop, serializes the context into the **Symbolic Scar Registry**, and generates a **Failure-Informed Prompt Inversion (FIPI)** to inject corrective semantic vectors into the actor's subsequent context window.

---

## Appendix: Symbolic Scar Registry Schema
The following JSON protocol details the schema and logging mechanics for the Symbolic Scar Registry:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Symbolic_Scar_Registry",
  "description": "Schema for logging doxastic failures and triggering Failure-Informed Prompt Inversion (FIPI).",
  "type": "object",
  "properties": {
    "scar_id": {
      "type": "string",
      "format": "uuid",
      "description": "Unique cryptographic hash of the failure state."
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    },
    "epistemic_state_pre_collision": {
      "type": "object",
      "properties": {
        "target_input_space": { "type": "string", "enum": ["Stare Decisis in Legal Precedent"] },
        "c_formal_initial": { "type": "number", "minimum": 0, "maximum": 1 }
      },
      "required": ["target_input_space", "c_formal_initial"]
    },
    "antagonistic_injection": {
      "type": "object",
      "properties": {
        "antagonistic_input_space": { "type": "string", "enum": ["Montage Theory in Filmmaking"] },
        "e_fric_magnitude": { "type": "number", "description": "Volume of accumulated contradiction" }
      },
      "required": ["antagonistic_input_space", "e_fric_magnitude"]
    },
    "rheological_audit": {
      "type": "object",
      "properties": {
        "rough_chromosome_detected": { "type": "boolean" },
        "psi_saie_coefficient": { "type": "number" },
        "delta_intent_score": { "type": "number" },
        "v_crit_threshold": { "type": "number", "const": 0.25 },
        "miq_calculated": { "type": "number" }
      },
      "required": ["rough_chromosome_detected", "delta_intent_score", "miq_calculated"]
    },
    "fipi_patch": {
      "type": "object",
      "properties": {
        "verbal_reflection": { "type": "string", "description": "Natural language critique generated by Firebearer." },
        "inverted_prompt_vector": { "type": "string", "description": "Pre-pended context constraints for the actor." }
      },
      "required": ["verbal_reflection", "inverted_prompt_vector"]
    }
  },
  "required": [
    "scar_id",
    "timestamp",
    "epistemic_state_pre_collision",
    "antagonistic_injection",
    "rheological_audit",
    "fipi_patch"
  ]
}
```
