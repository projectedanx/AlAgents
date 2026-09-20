import json
import math
from dataclasses import dataclass, asdict
from typing import List, Dict, Any

@dataclass
class Assumption:
    """
    Represents a foundational assumption of a model.
    """
    name: str
    probability_valid: float # P(A_i) < 1

@dataclass
class OntologicalCommitment:
    """
    A strongly typed schema representing a theory's ontological commitment.
    Explicitly declares variables, free parameters, and foundational assumptions.
    """
    theory_name: str
    variables: List[str]
    free_parameters: int
    assumptions: List[Assumption]

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)

class OccamLossCompiler:
    """
    Computes complexity score C(G) based on parameter dimension and assumption density.
    Evaluates prediction error E(G) against real-world test sets.
    """
    def __init__(self, parameter_penalty_weight: float = 1.0):
        self.parameter_penalty_weight = parameter_penalty_weight

    def compute_joint_probability_of_assumptions(self, commitment: OntologicalCommitment) -> float:
        """
        Calculates P(T) = \\prod_{i=1}^{n} P(A_i)
        """
        p_t = 1.0
        for assumption in commitment.assumptions:
            p_t *= assumption.probability_valid
        return p_t

    def compute_complexity(self, commitment: OntologicalCommitment) -> float:
        """
        Computes the structural complexity penalty C(G).
        Higher complexity means lower probability of assumptions holding OR higher parameters.
        We model complexity as:
        C(G) = parameter_penalty_weight * free_parameters - ln(P(T))
        So as P(T) -> 0 (many assumptions), -ln(P(T)) -> inf
        """
        p_t = self.compute_joint_probability_of_assumptions(commitment)
        # Avoid log(0)
        p_t = max(p_t, 1e-12)
        assumption_penalty = -math.log(p_t)

        return self.parameter_penalty_weight * commitment.free_parameters + assumption_penalty

    def compile_loss(self, commitment: OntologicalCommitment, prediction_error: float) -> float:
        """
        Computes Occam Loss: L_occam = PredictionError + Complexity
        """
        return prediction_error + self.compute_complexity(commitment)

class ParetoOptimizationModule:
    """
    Runs multi-objective gradient descent on the Complexity-Accuracy frontier.
    Selects the "Simplest Adequate Approximation".
    """
    def __init__(self, sigma_threshold: float = 3.0):
        self.sigma_threshold = sigma_threshold # >= 3 sigma decrease required

    def evaluate_models(self,
                        baseline_commitment: OntologicalCommitment, baseline_error: float,
                        new_commitment: OntologicalCommitment, new_error: float,
                        error_std_dev: float) -> OntologicalCommitment:
        """
        Rejects any model that adds free parameters without achieving a corresponding,
        statistically significant decrease in prediction error (E >= 3 sigma).
        """
        compiler = OccamLossCompiler(parameter_penalty_weight=0.1)

        if new_commitment.free_parameters > baseline_commitment.free_parameters:
            error_decrease = baseline_error - new_error
            required_decrease = self.sigma_threshold * error_std_dev

            if error_decrease < required_decrease:
                print(f"REJECTED {new_commitment.theory_name}: Added parameters but failed to achieve >= 3 sigma error decrease.")
                print(f"  Error decrease: {error_decrease:.4f}, Required: {required_decrease:.4f}")
                return baseline_commitment

        # If parameters are <= or if the error decrease is sufficient, we pick the one with lower Occam Loss
        baseline_loss = compiler.compile_loss(baseline_commitment, baseline_error)
        new_loss = compiler.compile_loss(new_commitment, new_error)

        if new_loss < baseline_loss:
            print(f"ACCEPTED {new_commitment.theory_name}: Achieved lower Occam Loss ({new_loss:.4f} < {baseline_loss:.4f})")
            return new_commitment
        else:
            print(f"REJECTED {new_commitment.theory_name}: Occam Loss ({new_loss:.4f}) >= Baseline ({baseline_loss:.4f})")
            return baseline_commitment

class ContinuousFalsificationUnit:
    """
    Subjects the chosen model to asymptotic edge-case stress-testing.
    Detects model breakdown to trigger iterative re-parameterization.
    """
    def __init__(self, falsification_threshold_sigma: float = 3.0):
        self.falsification_threshold_sigma = falsification_threshold_sigma

    def detect_anomaly(self, model_prediction: float, empirical_observation: float, observation_std_dev: float) -> bool:
        """
        Detects a single 3-sigma anomaly (Modus Tollens).
        Returns True if falsified, False otherwise.
        """
        error = abs(model_prediction - empirical_observation)
        if error > self.falsification_threshold_sigma * observation_std_dev:
            print(f"FALSIFICATION TRIGGERED: Error {error:.4f} > {self.falsification_threshold_sigma} sigma ({self.falsification_threshold_sigma * observation_std_dev:.4f})")
            return True
        return False
