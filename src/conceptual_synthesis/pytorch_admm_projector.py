import torch
import math
import numpy as np

def point_to_segment_dist(x, y, x1, y1, x2, y2):
    """
    Returns the minimum distance from point (x, y) to a line segment defined by (x1, y1) and (x2, y2).
    """
    A = x - x1
    B = y - y1
    C = x2 - x1
    D = y2 - y1

    dot = A * C + B * D
    len_sq = C * C + D * D
    param = -1

    if len_sq != 0:
        param = dot / len_sq

    if param < 0:
        xx = x1
        yy = y1
    elif param > 1:
        xx = x2
        yy = y2
    else:
        xx = x1 + param * C
        yy = y1 + param * D

    dx = x - xx
    dy = y - yy

    return math.sqrt(dx * dx + dy * dy)

def generate_kinematic_constraints(trajectories, masses, solar_center=(50.0, 50.0), solar_radius=10.0):
    """
    Kinematic-Economic Coupling:
    v(m) = 1 + 5 * (ln(m) / ln(1000))^1.5
    The required launch angle and fleet mass are coupled through travel time.
    If travel time is too long due to high mass, and the trajectory intersects the solar zone,
    it means higher exposure, thus higher penalty.
    """
    constraints = []

    for i in range(len(trajectories)):
        traj = trajectories[i]
        m = masses[i].item()

        # Calculate velocity based on mass formula
        v = 1.0 + 5.0 * ((math.log(m) / math.log(1000.0)) ** 1.5)

        # Calculate distance of trajectory
        traj_dist = math.sqrt((traj[1][0] - traj[0][0])**2 + (traj[1][1] - traj[0][1])**2)

        # Calculate travel time (t = d / v)
        travel_time = traj_dist / max(v, 0.001)

        # Check intersection with solar exclusion zone
        dist = point_to_segment_dist(solar_center[0], solar_center[1], traj[0][0], traj[0][1], traj[1][0], traj[1][1])

        if dist <= solar_radius:
            # Trajectory intersects!
            # Incur penalty margin delta_ij, scaled by the exposure (travel time).
            # This explicitly couples launch angle (derived from trajectory endpoints), mass, and travel time.
            if i != 0:
                constraints.append((0, i, 0.5 + 0.1 * travel_time)) # explicit penalty margin
        else:
            if i != 0:
                constraints.append((0, i, 0.0))

    return constraints


class PyTorchADMMProjector:
    """
    High-speed Alternating Direction Method of Multipliers (ADMM) solver in PyTorch
    to compute prefix-aware, scale-preserving advantages under strict hierarchical constraints.
    """
    def __init__(self, rho=1.0, max_iter=1000, tol=1e-5, device=None):
        self.rho = rho
        self.max_iter = max_iter
        self.tol = tol
        self.device = device if device else torch.device('cpu')

    @torch.compile(fullgraph=True)
    def _compiled_admm_step(self, r_0, M_inv, L, L_T, m, radius_sq, rho_scalar):
        n = r_0.shape[0]
        num_constraints = L.shape[0]

        v = torch.zeros(num_constraints, dtype=torch.float32, device=r_0.device)
        u = torch.zeros(num_constraints, dtype=torch.float32, device=r_0.device)

        sqrt_rad = math.sqrt(radius_sq)
        mean_scale = 1.0 / n

        a = r_0.clone()
        primal_res = torch.tensor(float('inf'), device=r_0.device)

        for _ in range(self.max_iter):
            rhs = r_0 + rho_scalar * torch.matmul(L_T, v - u)
            a = torch.matmul(M_inv, rhs)

            a = a - a.sum() * mean_scale

            norm_sq = torch.sum(a**2)
            a = torch.where(norm_sq > radius_sq, a * (sqrt_rad / torch.sqrt(norm_sq)), a)

            L_a = torch.matmul(L, a)
            v_unconstrained = L_a + u
            v = torch.minimum(v_unconstrained, -m)

            diff = L_a - v
            u = u + diff

            primal_res = torch.norm(diff)
            if primal_res < self.tol:
                break

        return a, primal_res

    def solve_admm(self, r_0: torch.Tensor, constraints, radius_sq: float):
        r_0 = r_0.to(self.device)
        n = r_0.size(0)
        num_constraints = len(constraints)

        if num_constraints == 0:
            a = r_0 - torch.mean(r_0)
            norm_sq = torch.sum(a**2)
            if norm_sq > radius_sq:
                a = a * math.sqrt(radius_sq / norm_sq.item())
            return a, 0.0

        L = torch.zeros((num_constraints, n), dtype=torch.float32, device=self.device)
        m = torch.zeros(num_constraints, dtype=torch.float32, device=self.device)

        for k, (i, j, margin) in enumerate(constraints):
            L[k, i] = 1.0
            L[k, j] = -1.0
            m[k] = margin

        L_T = L.t()

        M = torch.eye(n, device=self.device)
        M.addmm_(L_T, L, alpha=self.rho)
        M_inv = torch.linalg.inv(M)

        try:
            a, primal_res = self._compiled_admm_step(r_0, M_inv, L, L_T, m, radius_sq, self.rho)
            return a, primal_res.item()
        except Exception:
            return self._solve_admm_uncompiled(r_0, M_inv, L, L_T, m, radius_sq, n, num_constraints)

    def _solve_admm_uncompiled(self, r_0, M_inv, L, L_T, m, radius_sq, n, num_constraints):
        a = r_0.clone()
        v = torch.zeros(num_constraints, dtype=torch.float32, device=self.device)
        u = torch.zeros(num_constraints, dtype=torch.float32, device=self.device)

        primal_res = float('inf')
        sqrt_rad = math.sqrt(radius_sq)
        mean_scale = 1.0 / n

        for _ in range(self.max_iter):
            rhs = r_0 + self.rho * torch.matmul(L_T, (v - u))
            a = torch.matmul(M_inv, rhs)

            a -= a.sum() * mean_scale

            norm_sq = torch.sum(a**2)
            if norm_sq > radius_sq:
                a *= sqrt_rad / torch.sqrt(norm_sq)

            L_a = torch.matmul(L, a)
            v = torch.minimum(L_a + u, -m)

            L_a_minus_v = L_a - v
            u += L_a_minus_v

            primal_res = torch.norm(L_a_minus_v).item()
            if primal_res < self.tol:
                break

        return a, primal_res
