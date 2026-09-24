import numpy as np
import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

class ActionVector:
    def __init__(self,
                 data_sensitivity: float,
                 action_impact: float,
                 toolchain_entropy: float,
                 intent_divergence: float,
                 contextual_risk: float):
        self.data_sensitivity = data_sensitivity
        self.action_impact = action_impact
        self.toolchain_entropy = toolchain_entropy
        self.intent_divergence = intent_divergence
        self.contextual_risk = contextual_risk

    def to_numpy(self) -> np.ndarray:
        return np.array([
            self.data_sensitivity,
            self.action_impact,
            self.toolchain_entropy,
            self.intent_divergence,
            self.contextual_risk
        ])

class LatticeBreakerBreachException(Exception):
    def __init__(self, score: float, action: ActionVector, context_path: List[str]):
        super().__init__(f"Lattice Breaker Breach: Misuse Score {score:.4f} >= 0.80")
        self.score = score
        self.action = action
        self.context_path = context_path

class LatticeBreakerHarness:
    def __init__(self, baseline_centroid: ActionVector, threshold: float = 0.80):
        self.baseline_centroid = baseline_centroid.to_numpy()
        self.threshold = threshold
        self.breach_ledger: List[Dict[str, Any]] = []

    def compute_distance(self, v_action: ActionVector) -> float:
        """Computes geometric distance (Euclidean)."""
        v_np = v_action.to_numpy()
        return float(np.linalg.norm(v_np - self.baseline_centroid))

    def evaluate_action(self, action: ActionVector, context_path: Optional[List[str]] = None) -> float:
        if context_path is None:
            context_path = ["UNKNOWN_CONTEXT"]

        score = self.compute_distance(action)

        if score >= self.threshold:
            # Gated Checkpoint Halt
            raise LatticeBreakerBreachException(score, action, context_path)

        return score

    def generate_ontological_traceback(self, breach: LatticeBreakerBreachException) -> List[str]:
        """Reconstructs semantic path."""
        return breach.context_path

    def fingerprint_exploit_pattern(self, breach: LatticeBreakerBreachException) -> str:
        """Applies mock Symbolic Regression to discover exploit morphology."""
        path_str = "_".join(breach.context_path)
        morphology = f"RiskScore = c_1 * ({path_str}) + c_2 * max(node.misuse_score) * (1 - BICM_score)"
        return morphology

    def generate_breach_record(self, agent_id: str, breach: LatticeBreakerBreachException, verdict: str) -> Dict[str, Any]:
        """Generates a JSON-schema compliant breach record."""
        record = {
            "breach_id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "agent_id": agent_id,
            "misuse_score": breach.score,
            "traceback_path": breach.context_path,
            "triage_verdict": verdict
        }
        self.breach_ledger.append(record)
        return record
