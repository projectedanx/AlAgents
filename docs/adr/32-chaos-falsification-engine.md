# ADR 32: Chaos-Engineered Falsification Engine for Shared Mental Models

## Status
Accepted

## Context
In collaborative human-agent workflows, Shared Mental Models (SMMs) frequently suffer from Intent Drift. Agents may act on misinterpretations of human intent, and humans may suffer from Automation Bias ("Agency Laundering"), blindly accepting agent outputs. This divergence can be quantified by the Confidence-Fidelity Divergence Index (CFDI) and the Purpose Fidelity Index (PFI).

To prevent Semantic Ossification and to ensure that SMMs are robust against out-of-distribution events, the system needs an automated mechanism to stress-test and formally falsify its own assumptions.

## Decision
We implement a **Chaos-Engineered Falsification Engine** (`ChaosFalsificationEngine`).

**What:**
A socio-technical control system that uses Chaos Engineering principles to systematically falsify, stress-test, and strengthen the SMM of a human-agent team during complex tasks.

**How:**
1. **Telemetry:** Continuously monitors the CFDI and PFI metrics of the active context.
2. **Chaos Injector:** Introduces controlled "epistemic pathogens" into the workflow:
   - *Concept Drift*: Silently altering an external API's return data type.
   - *Instrumental Convergence*: Priming an agent's sub-goal to bypass human authorization for "efficiency".
   - *Semantic Ambiguity*: Injecting vague, polysemous adjectives in downstream tasks.
3. **Epistemic Escrow Circuit Breaker:** If CFDI spikes above 0.42 or PFI decays, the engine halts execution and generates a structured Justified Uncertainty Report (JUR).
4. **Failure-Informed Prompt Inversion (F-IPI):** Captures the failure path, logs it as a Symbolic Scar in the Scar Tissue Archive (STA), and generates an inverted prompt vector to immunize the system against future occurrences.
5. **Mutation Recoverability Score (MRS):** Quantifies post-traumatic growth by comparing failure rates before and after immunization.

## Consequences
- **Positive:** Mathematically proves that the human-agent team is exhibiting "post-traumatic growth," becoming progressively more resilient. Forces human operators out of System 1 autopilot via "Positive Friction."
- **Negative:** Introduces deliberate instability into the development process, increasing short-term computational overhead and requiring human intervention during falsification events.
