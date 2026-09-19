import numpy as np
from typing import List
from .staged_advantage_estimation import TreeOPOGroup

class EWARDiagnosticHarness:
    """
    Entropy-Weighted Advantage Recovery (EWAR) Diagnostic Harness.
    Monitors advantage variance across depths and detects 'Semantic Saponification'
    (where advantage variance collapses, destroying multi-step interception).
    """
    def __init__(self, chi_threshold: float = 0.05):
        self.chi_threshold = chi_threshold

    def calculate_saponification_index(self, advantages: np.ndarray, mixed_partials: np.ndarray) -> float:
        """
        Calculates chi = Corr(|a*|, d^2A / (dm dtheta)).
        mixed_partials represents the simulated mixed partial derivative.
        Returns correlation coefficient.
        """
        if len(advantages) < 2:
            return 1.0

        abs_adv = np.abs(advantages)

        # Add slight noise to avoid division by zero in perfect uniform cases
        abs_adv = abs_adv + np.random.normal(0, 1e-8, size=abs_adv.shape)
        mixed_partials = mixed_partials + np.random.normal(0, 1e-8, size=mixed_partials.shape)

        corr_matrix = np.corrcoef(abs_adv, mixed_partials)
        return float(corr_matrix[0, 1])

    def apply_ewar_hook(self, group: TreeOPOGroup, advantages: np.ndarray, parent_logprobs: np.ndarray, chi: float) -> np.ndarray:
        """
        Entropy-Weighted Advantage Recovery (EWAR) hook.
        If chi -> 0 (below threshold), override standard normalization, force c=1,
        and scale advantages by the inverse log-probability of the parent prefix.
        """
        if np.isnan(chi) or chi > self.chi_threshold:
            # Saponification not detected, return standard advantages
            return advantages

        # Saponification detected. Apply EWAR.
        # Force variance c=1 (which we implicitly handle if we rescale based on inverse logprob and re-normalize)
        # Parent logprob scaling: scale by 1 / abs(logprob). High entropy (low prob) gets higher scale.

        safe_logprobs = np.minimum(parent_logprobs, -1e-6) # prevent div by zero
        inverse_logprobs = 1.0 / np.abs(safe_logprobs)

        # Scale advantages
        scaled_adv = advantages * inverse_logprobs

        # Force c=1 (unit variance) and zero mean
        mean_scaled = np.mean(scaled_adv)
        zero_mean_adv = scaled_adv - mean_scaled

        std_scaled = np.std(zero_mean_adv)
        if std_scaled > 1e-6:
            ewar_adv = zero_mean_adv / std_scaled
        else:
            ewar_adv = zero_mean_adv

        return ewar_adv
