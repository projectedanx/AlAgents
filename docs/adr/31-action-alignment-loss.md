# ADR 31: Action-Alignment Loss Architecture

## Status
Accepted

## Context
When agents engage in multi-agent game-theoretic scenarios, current language models and behavioral cloning agents often exhibit a "thought-action gap." They can perfectly predict an opponent's behavior (Literal Theory of Mind) but fail to execute the optimal response, instead defaulting to unexploitative, high-entropy Nash equilibria. This creates a decoupling between representation and functional utility.

To address this, we need a loss function that causally binds the agent's expected utility based on its predictions to its selected policy.

## Decision
We implement **Action-Alignment Loss**, a bounded regret objective representing the distance between the expected utility of the selected policy and the expected utility of the optimal best response.

$$\mathcal{L}_{\text{Align}}(p, \hat{p}) = V^*(\hat{p}) - p^T U \hat{p}$$

Where:
- $p$ is the focal agent's policy (Head B).
- $\hat{p}$ is the opponent's predicted policy (Head A).
- $U$ is the game's payoff matrix.
- $V^*(\hat{p})$ is the expected utility of the absolute optimal Best Response.

To maintain gradient flow across all actions and prevent sparse subgradients, we employ a smooth Boltzmann approximation for $V^*(\hat{p})$:
$$V^*_{\tau}(\hat{p}) = \tau \log \sum_{j} \exp\left(\frac{[U \hat{p}]_j}{\tau}\right)$$

This is implemented in `src/conceptual_synthesis/action_alignment_loss.py`.

## Consequences
- **Positive:** Agents no longer collapse into Nash traps when predictable, suboptimal strategies are detected, thereby bridging the thought-action gap.
- **Positive:** Smooth gradient flow allows for stable reinforcement learning optimization during early phases.
- **Constraint:** Requires explicitly defining a payoff matrix for the game context during training.
- **Future Integration:** Will be evaluated alongside our existing Reinforcement Learning constraints, potentially integrated into the Staged Advantage Estimation pipeline or as a novel penalty in our proximal policy optimizations.
