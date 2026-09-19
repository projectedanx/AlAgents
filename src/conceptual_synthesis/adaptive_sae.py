import numpy as np
from typing import Dict, List, Tuple
from .staged_advantage_estimation import TreeOPOGroup

class AdaptiveSAEHarness:
    """
    Adaptive Staged Advantage Estimation (SAE) harness that dynamically interpolates
    between the O(N) expectation heuristic and the formal QP projection based on
    the 'Spectral Information Discrepancy' (Psi).
    """
    def __init__(self, tau_equilibrium: float = 0.12):
        self.tau_equilibrium = tau_equilibrium

    def compute_spectral_information_discrepancy(self, group: TreeOPOGroup, student_logprobs: np.ndarray, teacher_logprobs: np.ndarray) -> float:
        """
        Computes Psi = rho(D_parent - D_children) * D_KL(pi_student || pi_teacher)
        D_parent, D_children are degree matrices of the prefix adjacency graph.
        """
        # KL divergence (discrete sample approximation using sum or mean over sequence length)
        # Assuming logprobs are provided per step. Standard KL is sum(p * log(p/q)).
        # Since we just have sample logprobs, we can approximate the expected difference in logprobs.
        # Alternatively, D_KL ~ mean(teacher_logprobs - student_logprobs) if teacher is the reference distribution.
        # Let's use a simpler proxy for D_KL to ensure positiveness and stability:
        kl_div = np.mean(np.abs(teacher_logprobs - student_logprobs))

        # Build adjacency matrix A to compute degree matrices D_parent, D_children
        # In a directed tree, D_parent is out-degree (children count), D_children is in-degree (always 1 for non-root)
        num_nodes = len(group.nodes)
        if num_nodes == 0:
            return 0.0

        node_ids = list(group.nodes.keys())
        id_to_idx = {nid: i for i, nid in enumerate(node_ids)}

        A = np.zeros((num_nodes, num_nodes))
        for nid, node in group.nodes.items():
            if node.parent_id and node.parent_id in id_to_idx:
                p_idx = id_to_idx[node.parent_id]
                c_idx = id_to_idx[nid]
                A[p_idx, c_idx] = 1.0 # edge from parent to child

        D_parent_diag = np.sum(A, axis=1) # out-degree
        D_children_diag = np.sum(A, axis=0) # in-degree

        D_diff = np.diag(D_parent_diag - D_children_diag)

        # Spectral radius of D_diff (which is diagonal, so max absolute eigenvalue)
        if D_diff.size > 0:
            rho = np.max(np.abs(np.linalg.eigvals(D_diff)))
        else:
            rho = 0.0

        psi = rho * kl_div
        return float(psi)

    def calculate_shannon_entropy(self, logprobs: np.ndarray) -> float:
        """
        Calculates Shannon entropy given log probabilities.
        H(P) = -sum(P(x) * log P(x))
        """
        probs = np.exp(logprobs)
        # Avoid log(0)
        safe_logprobs = np.where(probs > 0, logprobs, 0.0)
        return -np.sum(probs * safe_logprobs) / len(logprobs)

    def compute_advantages(self, group: TreeOPOGroup, student_logprobs: np.ndarray, teacher_logprobs: np.ndarray) -> np.ndarray:
        """
        Adaptive computation of SAE advantages.
        If Psi < tau_equilibrium, use heuristic.
        If Psi >= tau_equilibrium, dynamically scale margin and use QP.
        """
        psi = self.compute_spectral_information_discrepancy(group, student_logprobs, teacher_logprobs)

        if psi < self.tau_equilibrium:
            # Low non-stationarity: bypass SLSQP optimizer, use O(N) expectation heuristic
            return group.compute_heuristic_advantages(alpha=0.5)
        else:
            # High non-stationarity: deploy QP with dynamic margin scaling
            entropy = self.calculate_shannon_entropy(student_logprobs)
            # Scale margin proportionally to local Shannon entropy
            margin = 0.01 + 0.1 * entropy
            return group.compute_sae_qp_advantages(margin=margin, soft=True)
