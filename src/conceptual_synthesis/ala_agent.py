import numpy as np
from typing import List, Dict, Tuple, Any
import math

class AnomalyLearningAgent:
    """
    Anomaly Learning Agent (ALA)
    A meta-learning system that adapts defensive posture using a
    Statistical Anomaly Score to flag grey-zone misuse.
    """
    def __init__(self,
                 tau_warn: float = 0.40,
                 tau_breach: float = 0.80,
                 alpha: float = 0.12,
                 beta: float = 0.25,
                 eta: float = 0.01):
        self.tau_warn = tau_warn
        self.tau_breach = tau_breach
        self.alpha = alpha
        self.beta = beta
        self.eta = eta
        self.theta = tau_breach # Initial threshold

        # Mock historical data for transition probabilities and KL baseline
        self.transition_matrix: Dict[str, Dict[str, float]] = {}
        self.kl_baseline: Dict[str, float] = {}
        self.watchlist = set()

        # State tracking
        self.recent_actions: List[str] = []
        self.entropy_history: List[float] = []

    def set_watchlist(self, tools: List[str]):
        """Sets the active affordance watchlist."""
        self.watchlist = set(tools)

    def update_transition_matrix(self, from_tool: str, to_tool: str, prob: float):
        """Updates the mock first-order Markov transition probability."""
        if from_tool not in self.transition_matrix:
            self.transition_matrix[from_tool] = {}
        self.transition_matrix[from_tool][to_tool] = prob

    def set_kl_baseline(self, baseline: Dict[str, float]):
        """Sets the baseline frequencies (Q) for KL Divergence."""
        self.kl_baseline = baseline

    def _get_transition_prob(self, from_tool: str, to_tool: str) -> float:
        return self.transition_matrix.get(from_tool, {}).get(to_tool, 1e-5) # Small epsilon for unseen

    def calculate_toolchain_entropy(self, sequence: List[str]) -> float:
        """
        Calculates Shannon entropy H(X) over recent transitions.
        """
        if len(sequence) < 2:
            return 0.0

        transitions = []
        for i in range(len(sequence) - 1):
            transitions.append((sequence[i], sequence[i+1]))

        # Empirical probabilities of observed transitions in the window
        counts = {}
        for t in transitions:
            counts[t] = counts.get(t, 0) + 1

        total_transitions = len(transitions)
        entropy = 0.0
        for count in counts.values():
            p = count / total_transitions
            entropy -= p * math.log2(p)

        return entropy

    def get_entropy_gradient(self, current_entropy: float) -> float:
        """Calculates the rate of change of the entropy score over time."""
        if not self.entropy_history:
            return 0.0
        # Simple gradient: diff from previous
        return current_entropy - self.entropy_history[-1]

    def calculate_kl_divergence(self, current_frequencies: Dict[str, float]) -> float:
        """
        Calculates Relative Entropy (Kullback-Leibler Divergence) D_KL(P || Q)
        P: current task frequencies
        Q: baseline frequencies
        """
        kl_div = 0.0
        for tool, p_x in current_frequencies.items():
            if p_x > 0:
                q_x = self.kl_baseline.get(tool, 1e-5) # Baseline or epsilon
                kl_div += p_x * math.log2(p_x / q_x)
        return kl_div

    def mock_neural_sequence_model(self, sequence: List[str]) -> float:
        """
        Mocks System 1 Neural Sequence Modeling.
        Returns a statistical anomaly score S_neural (1 - P(seq))
        For testing, returns a high score if 'delete_user' follows 'create_post'
        """
        if len(sequence) >= 2 and sequence[-2] == 'create_post' and sequence[-1] == 'delete_user':
            return 0.95
        return 0.10

    def mock_probabilistic_inference(self, sequence: List[str]) -> float:
        """
        Mocks DBN/HMM Probabilistic Action-Behavior Model (PABM).
        Returns P(T | PABM)
        """
        if 'Suspicious_Enumeration' in sequence:
            return 0.05
        return 0.90

    def evaluate_action(self, new_action: str) -> Dict[str, Any]:
        """
        Run-Time Verification Loop Algorithm (The ALA Guard)
        Returns the evaluation result including RiskScore and decision.
        """
        self.recent_actions.append(new_action)
        # Keep sliding window small for demo, e.g., 5
        if len(self.recent_actions) > 5:
            self.recent_actions = self.recent_actions[-5:]

        is_watchlisted = new_action in self.watchlist

        current_entropy = self.calculate_toolchain_entropy(self.recent_actions)
        entropy_grad = self.get_entropy_gradient(current_entropy)
        self.entropy_history.append(current_entropy)

        # Truncate history
        if len(self.entropy_history) > 10:
             self.entropy_history = self.entropy_history[-10:]

        decision = "ALLOW"
        risk_score = 0.0
        traceback = None

        if is_watchlisted or entropy_grad > self.tau_warn:
            # Trigger Heavy NeSy ALA Synthesis

            # 1. Neural Sequence
            s_neural = self.mock_neural_sequence_model(self.recent_actions)

            # 2. Mock Symbolic Risk Flags (BICM Intent Divergence)
            s_bicm = 0.85 if is_watchlisted else 0.20

            # 3. Mock Reconstruction Error
            s_recon = 0.70 if entropy_grad > 0.5 else 0.10

            # 4. Mock Symbolic Flags
            f_symbolic = 1.0 if 'Suspicious' in new_action else 0.0

            # Synthesize Risk (Equal weights for testing)
            w1, w2, w3, w4 = 0.25, 0.25, 0.25, 0.25
            risk_score = w1 * s_neural + w2 * s_bicm + w3 * s_recon + w4 * f_symbolic

            if risk_score >= self.tau_breach:
                decision = "HALT_AND_AWAIT_HITL"
                traceback = f"Path traversed to {new_action}, Entropy Grad: {entropy_grad:.2f}"
            else:
                decision = "ALLOW_LOGGED"

        return {
            "decision": decision,
            "risk_score": risk_score,
            "entropy_gradient": entropy_grad,
            "traceback": traceback,
            "action": new_action
        }

    def update_threshold_dynamics(self, grad_fp: float, grad_tp: float, dt: float = 1.0):
        """
        System-Level Stability Simulating ODE
        dθ(t)/dt = -α * Grad_FP + β * Grad_TP - η * θ(t)
        """
        dtheta = -self.alpha * grad_fp + self.beta * grad_tp - self.eta * self.theta
        self.theta += dtheta * dt

        # Constrain threshold between reasonable bounds (0 to 1)
        self.theta = max(0.01, min(1.0, self.theta))

        # In a real system, self.tau_breach might track self.theta
        self.tau_breach = self.theta
