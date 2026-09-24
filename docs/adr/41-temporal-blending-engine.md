# ADR 41: Temporal Blending Engine and Causal Path Integrity (CPI)

## Context
The **Temporal Blending Engine (TBE)** is a multi-agent orchestration architecture designed to resolve **Chronotopological Drift** when fusing temporally divergent conceptual spaces under the governance of the Verifiable Cognition Stack (VCS).

## Decision
We implement a mathematically formal constraint known as **Causal Path Integrity (CPI)** to govern semantic flows in LLM-generated trajectories. The TBE utilizes the **System Assurance Agent (SAA)** to enforce a non-negotiable threshold of `CPI >= 0.95`.

## Mathematical Formalization

### 1. Isomorphic Formalization of the Temporal Blending State-Space
To model **Epistemic Rheology**—the continuous flow of concepts—we define a continuous trajectory $\mathbf{S}_t \in \mathcal{M}$ (the latent space) using a Double-Scope Blend (DSCB):
$$\mathbf{S}_t = \mathbf{\Phi}\big(\mathbf{X}_N(t), \mathbf{X}_C(t), \mathbf{W}_t\big)$$

A discrete state $s_k$ is defined by a valuation vector over a finite set of Boolean fluents $F = \{f_1, f_2, \dots, f_m\}$, such that $s_k \in \{0, 1\}^m$.

Causal Actions have:
1. **Preconditions ($\operatorname{Pre}(a)$):** Required fluent states.
2. **Effects ($\operatorname{Eff}(a)$):** Changes to fluent states.

We enforce the **Frame Operator** $\operatorname{Frame}(s_k, s_{k+1}, a)$ to ensure fluents not in $\operatorname{Eff}(a)$ remain invariant.

### 2. Causal Path Integrity (CPI)
For a trace $\tau = (s_1, a_1, s_2, a_2, \dots, a_{N-1}, s_N)$, the CPI is defined as:
$$\operatorname{CPI}(\tau) = \frac{1}{N-1} \sum_{k=1}^{N-1} \mathbb{I}\Big( s_k \models \operatorname{Pre}(a_k) \;\wedge\; s_{k+1} \models \operatorname{Eff}(a_k) \;\wedge\; \operatorname{Frame}(s_k, s_{k+1}, a_k) \Big)$$
The SAA enforces the constraint:
$$\operatorname{CPI}(\tau) \geq 0.95$$

### 3. Cascading Contradiction Boundary
If an action disabled a fluent (e.g., $f_{cam} = 0$), and a subsequent action requires it ($f_{cam} = 1$), a contradiction occurs. For a sequence length $N < 21$, a single contradiction will drop the CPI below 0.95, mathematically preventing the violation from passing the SAA gate. For longer sequences ($N \geq 21$), execution is halted via an Epistemic Escrow / Reflexive Repair Loop.

### 4. Epistemic Rheological Stability
The latent trajectory velocity is governed by the Epistemic Rheology Equation:
$$\mu \nabla^2 \mathbf{u} - \nabla p + \mathbf{f}_{\text{constraint}} = 0$$
By increasing semantic viscosity $\mu$, we establish a Lipschitz continuity bound to guarantee that the transition does not jump disjoint semantic territories, thereby preventing **Chronotopological Drift**.

### 5. Tension Frontier Parameters
- **Cost of Coherence Overhead (CCH):** Verification Depth $\times$ Tokens.
- **Cost of Structural Discovery (CSD):** Temperature ($T$) $\times$ Variance.
Over-allocating CSD drops viscosity $\mu$, leading to high CFDI (Confidence-Fidelity Divergence Index) and triggering Epistemic Escrow.

## Status
Accepted.
