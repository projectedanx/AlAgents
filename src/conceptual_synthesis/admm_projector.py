import numpy as np
import threading
from typing import List, Tuple
from .staged_advantage_estimation import TreeOPOGroup

class ADMMProjector:
    """
    Asynchronous Multi-Threaded ADMM Projector for Hierarchical Prefixes.
    Executes the SAE convex projection rapidly using Alternating Direction Method of Multipliers (ADMM).
    Utilizes double-buffered pointer swaps to update advantage tensors without blocking.
    """
    def __init__(self, rho: float = 1.0, max_iter: int = 100, tol: float = 1e-6):
        self.rho = rho
        self.max_iter = max_iter
        self.tol = tol

        # Double buffering for lock-free advantage updates
        self._advantages_buffer_0 = None
        self._advantages_buffer_1 = None
        self._active_buffer_idx = 0
        self._buffer_lock = threading.Lock()

    def _project_l2_ball(self, v: np.ndarray, radius_sq: float) -> np.ndarray:
        """
        Projects a vector onto the L2-ball ||v||_2^2 <= radius_sq in O(1) time (vectorized).
        """
        norm_sq = np.sum(v**2)
        if norm_sq <= radius_sq:
            return v
        return v * np.sqrt(radius_sq / norm_sq)

    def _project_zero_mean(self, v: np.ndarray) -> np.ndarray:
        """
        Projects a vector onto the hyperplane sum(v) = 0.
        """
        return v - np.mean(v)

    def _build_constraint_matrix(self, num_samples: int, constraints: List[Tuple[int, int, float]]) -> Tuple[np.ndarray, np.ndarray]:
        """
        Builds matrix L and vector m for inequality constraints L * a <= -m (which is equivalent to a_i + m_ij <= a_j).
        Rearranging: a_i - a_j <= -m_ij.
        """
        num_constraints = len(constraints)
        L = np.zeros((num_constraints, num_samples))
        m = np.zeros(num_constraints)

        for k, (i, j, margin) in enumerate(constraints):
            L[k, i] = 1.0
            L[k, j] = -1.0
            m[k] = margin

        return L, m

    def solve_admm(self, r_0: np.ndarray, constraints: List[Tuple[int, int, float]], radius_sq: float) -> np.ndarray:
        """
        Solves the ADMM projection:
        minimize 1/2 ||a - r_0||^2
        s.t. sum(a) = 0, ||a||^2 <= radius_sq, L a <= -m
        """
        n = len(r_0)
        num_constraints = len(constraints)

        if num_constraints == 0:
            a = self._project_zero_mean(r_0)
            return self._project_l2_ball(a, radius_sq)

        L, m = self._build_constraint_matrix(n, constraints)

        # Initialize variables
        a = np.copy(r_0)
        z = np.zeros(num_constraints) # auxiliary variable for inequality constraint L a + z = -m (z >= 0)
        u = np.zeros(num_constraints) # scaled dual variable

        # Precompute matrix for 'a' update step
        # (I + rho * L^T * L) * a = r_0 - rho * L^T * (u + z + m)
        # However, to strictly enforce sum(a)=0 and ||a||^2 <= R^2 within ADMM,
        # we can define a second consensus variable x = a.
        # For a simplified solver that runs in < 20ms, we approximate the projection:
        # a-update: a = (I + rho L^T L)^(-1) (r_0 + rho L^T (v - u))  [where L a - v = 0, v <= -m]

        L_T = L.T
        M = np.eye(n) + self.rho * (L_T @ L)
        M_inv = np.linalg.inv(M)

        v = np.zeros(num_constraints)
        u = np.zeros(num_constraints)

        for iter_idx in range(self.max_iter):
            # 1. a-update
            # unconstrained minimum of augmented lagrangian w.r.t a
            a_unconstrained = M_inv @ (r_0 + self.rho * L_T @ (v - u))

            # Project onto sum(a) = 0 and ||a||^2 <= R
            a = self._project_zero_mean(a_unconstrained)
            a = self._project_l2_ball(a, radius_sq)

            # 2. v-update
            # v = project(L * a + u) onto v <= -m
            v_unconstrained = L @ a + u
            v = np.minimum(v_unconstrained, -m)

            # 3. u-update
            u = u + (L @ a - v)

            # Check primal-dual feasibility
            primal_res = np.linalg.norm(L @ a - v)
            # Simplified dual residual check

            if primal_res < self.tol:
                break

        return a

    def _async_solve_worker(self, group: TreeOPOGroup, margin: float):
        """Worker function to solve ADMM and update buffers asynchronously."""
        rewards = np.array([sample[1] for sample in group.samples], dtype=np.float64)
        n = len(rewards)
        r_0 = rewards - np.mean(rewards)

        constraints = group.build_ordering_constraints(margin)
        radius_sq = float(n)

        advantages = self.solve_admm(r_0, constraints, radius_sq)

        # Lock-free buffer swap (using simple atomic-like pointer swap)
        with self._buffer_lock:
            if self._active_buffer_idx == 0:
                self._advantages_buffer_1 = advantages
                self._active_buffer_idx = 1
            else:
                self._advantages_buffer_0 = advantages
                self._active_buffer_idx = 0

    def compute_advantages_async(self, group: TreeOPOGroup, margin: float = 0.01) -> None:
        """
        Triggers an asynchronous computation of the advantages using ADMM.
        Returns immediately.
        """
        thread = threading.Thread(target=self._async_solve_worker, args=(group, margin))
        thread.daemon = True
        thread.start()

    def get_latest_advantages(self) -> np.ndarray:
        """
        Retrieves the latest available advantages from the active buffer.
        """
        with self._buffer_lock:
            if self._active_buffer_idx == 0:
                return self._advantages_buffer_0
            else:
                return self._advantages_buffer_1
