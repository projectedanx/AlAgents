# Architecture Decision Record 39: Anomaly Learning Agent (ALA)

## Status
Accepted

## Context
Within advanced neuro-symbolic security architectures designed to monitor autonomous agent workflows, there is a critical need to adapt the defensive posture of the system in real time. Static heuristic-based security models are insufficient against "grey-zone misuse" where individual actions are authorized, but their sequence and intent indicate malicious or misaligned processes.

## Decision
We introduce the **Anomaly Learning Agent (ALA)**, a meta-learning system that evaluates a Statistical Anomaly Score to preemptively flag grey-zone misuse. The ALA Perception Pipeline is a multi-layered, hybrid neural-symbolic engine.

### I. Mathematical Formulations
1.  **Neural Sequence Modeling:** Utilizes a deep sequential architecture (e.g., RNN/Transformer) to output a probability of the current token sequence: $S_{\text{neural}} = 1 - P(tool_t \mid tool_{<t}, \text{Context})$.
2.  **First-Order Markov Transition Probability:** Computes transition probabilities $P(tool_j \mid tool_i)$ from historical logs.
3.  **Toolchain Entropy Gradient:** Uses Shannon entropy $H(X)$ to quantify behavioral surprise. A sharp, sudden spike (high positive gradient) flags anomalous behavior.
4.  **Relative Entropy (KL Divergence):** Measures contextual misalignment $D_{KL}(P \mid\mid Q)$ between observed tool transition frequencies and expected task-specific baselines.
5.  **Probabilistic Action-Behavior Model (PABM):** Uses DBN/HMM to compute the joint probability $P(T \mid PABM)$ using Viterbi-like inference.

### II. The Four Pillars of Specification Planning
1.  **Automated Discovery & Constraint Mining:**
    *   Hard Invariant: CFDI $\le 0.42$.
    *   Soft Target: Toolchain Entropy Gradient $\le 0.15$.
2.  **Isomorphic Formalization:** Employs the **PROV-AGENT Schema** to preserve causal lineage of anomaly detection decisions for strict verifiability.
3.  **Parametric Trade-off Modeling:** Standard passes are audited by low-overhead sensors. The heavy multi-vector ALA fusion engine is only triggered when entropy gradient $\ge 0.40$ or a tool on the Affordance Watchlist is invoked.
4.  **Continuous Falsification:** Utilizes a Generative Adversarial Resilience (GAR) loop with a Failure Generator agent.

### III. System-Level Stability Simulating
The threshold dynamics are modeled via ODE:
$$\frac{d\theta(t)}{dt} = -\alpha \cdot \text{Grad}_{\theta}\mathcal{L}_{\text{FalsePositive}}(t) + \beta \cdot \text{Grad}_{\theta}\mathcal{L}_{\text{TruePositive}}(t) - \eta \cdot \theta(t)$$

This allows dynamic calibration between permissive states (Under-Damped), restrictive states (Over-Damped), and Epistemic Homeostasis (Critically Damped).

### IV. Run-Time Verification Loop Algorithm (The ALA Guard)
1. Extract Action Vector.
2. Verify watchlists and entropy gradient to determine if a laminar pass is allowed or if heavy ALA synthesis is required.
3. If required, compute Risk Score $= w_1 S_{\text{neural}} + w_2 S_{BICM} + w_3 S_{\text{recon}} + w_4 F_{\text{symbolic}}$.
4. Trigger `HALT_AND_AWAIT_HITL` if Risk Score $\ge \tau_{breach}$ (0.80), otherwise allow and log.

## Consequences
*   Enhances security against complex, sequenced exploits by analyzing intent and sequence probability.
*   Introduces the need for continuous tuning of $\alpha$, $\beta$, and $\eta$ to prevent Sycophantic Blindness or Semantic Ossification.
*   Requires maintaining a reliable baseline for entropy and KL divergence calculations.
