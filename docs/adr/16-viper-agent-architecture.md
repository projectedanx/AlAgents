# ADR-16: V.I.P.E.R. (Visual Intent & Physical Execution Router) Agent Architecture

## Status
Accepted

## Context
Standard AI text-to-image workflows suffer from "Semantic Saponification"—when users provide evaluative, aesthetic prompt tokens (e.g., "cinematic", "masterpiece"), the underlying model's diffusion manifold activates multiple conflicting aesthetic attractors. The statistical averaging of these attractors produces overly smoothed, plastic results that lack physical realism and structural coherence.

Furthermore, human users typically struggle to articulate spatial relationships (often resulting in Occlusion Confusion) or accurate optical mechanics. The current paradigm forces the AI to "guess" what "moody" means in terms of physical light.

## Decision
Implement the `ViperAgent` ("The Gaffer") to serve as an uncompromising translation layer between human affective desire and machine physical specification.

V.I.P.E.R. operates under the following strict tenets:
1. **Analytic-to-Generative Inversion**: The user provides intent; the agent provides the exact physical physics required to manifest it (hardware settings, lighting diagrams).
2. **Lattice of Refusal**: Employs a Banned Token Protocol to explicitly reject (and diagnose) aesthetic descriptors, demanding mechanical parameters instead.
3. **Hardware Grounding Index (HGI)**: Mandates that 100% of generated prompts contain explicit Lens, Film Stock/Aperture, and Lighting configurations.
4. **RCC-8 Topological Binding**: Prevents spatial generation failures by formally declaring spatial relationship bounds (`+++SpatialBind`).
5. **Symbolic Scar Archive**: Employs Failure-Informed Prompt Inversion (FIPI), remembering past failure modes via hypervectors and preempting them.

The agent operates on the `+++PetzoldSequence` (THINK -> DENOISE -> PHYSICALIZE -> EXTRUDE), strictly formatted using PDL v1.0 syntax into an Optical State Matrix (OSM).

## Consequences

### Positive
* Deterministic control over visual output geometry and optics.
* Complete eradication of Semantic Saponification and vague generation.
* Re-trains user behavior via "Positive Friction" to provide robust inputs.

### Negative
* High barrier to entry for users unwilling to define physical parameters.
* May frustrate users expecting immediate, simple text-to-image completions.
