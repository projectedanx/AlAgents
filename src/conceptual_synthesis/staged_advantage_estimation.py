import numpy as np
from scipy.optimize import minimize
from typing import List, Dict, Tuple, Set, Union, Optional

class StagedTrajectoryNode:
    """
    Represents a node (prefix state) within the MCTS trajectory hierarchy.
    """
    def __init__(self, prefix_id: str, parent_id: Optional[str] = None):
        self.prefix_id = prefix_id
        self.parent_id = parent_id
        self.children_ids: Set[str] = set()

        # Rollout metrics for expectation baseline calculations
        self.total_rollouts: int = 0
        self.successful_rollouts: int = 0
        self.has_success_completion: bool = False

class TreeOPOGroup:
    """
    Manages a group of completions originating from different prefixes
    within a shared MCTS reasoning tree. Calculates SAE advantages.
    """
    def __init__(self, group_id: str):
        self.group_id = group_id
        self.nodes: Dict[str, StagedTrajectoryNode] = {}

        # Maps index in the batch to metadata: (prefix_id, reward)
        self.samples: List[Tuple[str, float]] = []

    def add_node(self, prefix_id: str, parent_id: Optional[str] = None) -> None:
        if prefix_id not in self.nodes:
            self.nodes[prefix_id] = StagedTrajectoryNode(prefix_id, parent_id)
            if parent_id and parent_id in self.nodes:
                self.nodes[parent_id].children_ids.add(prefix_id)

    def register_sample(self, prefix_id: str, reward: float) -> int:
        """Registers an online completion rollout, updating tree metadata."""
        sample_idx = len(self.samples)
        self.samples.append((prefix_id, reward))

        # Propagate statistics upward through the prefix chain
        curr_id = prefix_id
        is_success = (reward > 0.5)

        while curr_id is not None:
            node = self.nodes[curr_id]
            node.total_rollouts += 1
            if is_success:
                node.successful_rollouts += 1
                node.has_success_completion = True
            curr_id = node.parent_id

        return sample_idx

    def get_empirical_expectation(self, prefix_id: str) -> float:
        """Computes V_E(p) -- the empirical subtree success rate."""
        node = self.nodes.get(prefix_id)
        if not node or node.total_rollouts == 0:
            return 0.0
        return node.successful_rollouts / node.total_rollouts

    # --- APPROACH 1: HEURISTIC EXPECTATION BASELINE (ANALYTIC & O(N)) ---
    def compute_heuristic_advantages(self, alpha: float = 0.5) -> np.ndarray:
        """
        Computes advantages as a'_i = r_i - alpha * V_E(p_i), followed by
        mean-centering to stabilize training and maintain tree consistency.
        """
        rewards = np.array([sample[1] for sample in self.samples], dtype=np.float64)
        raw_advantages = np.zeros_like(rewards)

        for i, (prefix_id, r_i) in enumerate(self.samples):
            v_e = self.get_empirical_expectation(prefix_id)
            # Subtract the prefix-conditioned baseline to capture local surprise
            raw_advantages[i] = r_i - alpha * v_e

        # Mean-center raw advantages to satisfy sum(a) = 0
        mean_offset = np.mean(raw_advantages)
        final_advantages = raw_advantages - mean_offset
        return final_advantages

    # --- APPROACH 2: FORMAL CONSTRAINED QUADRATIC PROGRAM (SAE QP) ---
    def build_ordering_constraints(self, margin: float = 0.01) -> List[Tuple[int, int, float]]:
        """
        Extracts C_order = C_pair U C_triplet constraint boundaries.
        Returns list of tuples: (idx_i, idx_j, margin_ij) enforcing a_i + margin <= a_j.
        """
        constraints = []
        num_samples = len(self.samples)

        # Auxiliary structures for quick lookup
        prefix_to_idxs: Dict[str, List[int]] = {}
        for idx, (prefix_id, _) in enumerate(self.samples):
            prefix_to_idxs.setdefault(prefix_id, []).append(idx)

        # Compile constraints by pairwise cross-comparison of batch samples
        for i in range(num_samples):
            p_i, r_i = self.samples[i]
            node_i = self.nodes[p_i]

            for j in range(num_samples):
                if i == j:
                    continue
                p_j, r_j = self.samples[j]
                node_j = self.nodes[p_j]

                # Helper: checks if prefix A contains prefix B
                is_prefix_relation = p_i.startswith(p_j) and p_i != p_j
                is_sibling_relation = (node_i.parent_id == node_j.parent_id) and (node_i.parent_id is not None)

                # 1. Pair-wise (Parent-Child) Consistency (C_pair)
                # If prefix_j is a prefix of prefix_i, and r_j = 0, r_i = 1, then a_j + margin <= a_i
                if is_prefix_relation and r_j < 0.5 and r_i > 0.5:
                    constraints.append((j, i, margin))

                # 2. Triplet Consistency (C_triplet)
                # If siblings are both failing (r_i = 0, r_j = 0) and neither has success completions,
                # but sibling_i has a successful deeper descendant path in the tree,
                # prioritize exploration of sibling_j by forcing a_i + margin <= a_j
                if is_sibling_relation and r_i < 0.5 and r_j < 0.5:
                    if not node_i.has_success_completion and not node_j.has_success_completion:
                        # Scan the rest of the tree for any successful descendant of prefix_i
                        has_succ_descendant = False
                        for p_k, node_k in self.nodes.items():
                            if p_k.startswith(p_i) and p_k != p_i and node_k.has_success_completion:
                                has_succ_descendant = True
                                break
                        if has_succ_descendant:
                            constraints.append((i, j, margin))

        return constraints

    def compute_sae_qp_advantages(self, margin: float = 0.01, soft: bool = True) -> np.ndarray:
        """
        Solves the constrained convex Quadratic Program for SAE advantages
        via scipy.optimize (SLSQP). Warm-started from mean-centered rewards.
        """
        rewards = np.array([sample[1] for sample in self.samples], dtype=np.float64)
        n = len(rewards)

        # Center rewards to construct r_0 seed
        r_0 = rewards - np.mean(rewards)

        # Build constraint matrix from C_order
        ordering_relations = self.build_ordering_constraints(margin)

        # Objective: minimize 0.5 * ||a - r_0||^2
        def objective(a):
            diff = a - r_0
            return 0.5 * np.dot(diff, diff)

        def jacobian(a):
            return a - r_0

        # Equational Constraint: sum(a) = 0
        eq_cons = {
            'type': 'eq',
            'fun': lambda a: np.sum(a),
            'jac': lambda a: np.ones_like(a)
        }

        # Norm Constraint: ||a||^2 <= N (soft) or ||a||^2 = N (hard)
        if soft:
            norm_cons = {
                'type': 'ineq',
                'fun': lambda a: n - np.dot(a, a),
                'jac': lambda a: -2 * a
            }
        else:
            norm_cons = {
                'type': 'eq',
                'fun': lambda a: np.dot(a, a) - n,
                'jac': lambda a: 2 * a
            }

        constraints = [eq_cons, norm_cons]

        # Add Linear Inequalities from C_order: a_j - a_i - margin >= 0
        for i_idx, j_idx, margin_val in ordering_relations:
            # We capture local indexes within lambda scoping
            ineq_fun = lambda a, i=i_idx, j=j_idx, m=margin_val: a[j] - a[i] - m
            # Derivative: sparse vector with -1 at i and +1 at j
            def ineq_jac(a, i=i_idx, j=j_idx):
                grad = np.zeros_like(a)
                grad[j] = 1.0
                grad[i] = -1.0
                return grad

            constraints.append({
                'type': 'ineq',
                'fun': ineq_fun,
                'jac': ineq_jac
            })

        # Warm start using the mean-centered reward vector
        x0 = np.copy(r_0)

        # Solve the QP using sequential least squares programming
        res = minimize(
            fun=objective,
            x0=x0,
            jac=jacobian,
            constraints=constraints,
            method='SLSQP',
            options={'ftol': 1e-9, 'maxiter': 100}
        )

        # Fallback to heuristic values in case of optimizer divergence or infeasibility
        if not res.success:
            return self.compute_heuristic_advantages(alpha=0.5)

        return res.x
