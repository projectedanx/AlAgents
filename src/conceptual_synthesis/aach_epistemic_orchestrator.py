"""
Epistemic Action & Extended Mind Orchestrator.

This module implements the Active Externalism Cognitive Orchestrator
for joint Human-AI active coupling systems. It models the output buffer
as an active epistemic scratchpad, applying optimal feedback control
and present-at-hand algorithmic reparation on error detection.
"""

from typing import Dict, List, Tuple, Any, Optional

class EpistemicActionOrchestrator:
    """
    Manages the epistemic scratchpad for complex multi-variable constraint satisfaction,
    shifting from ready-to-hand to present-at-hand upon error detection.
    """

    def __init__(self):
        """Initializes the orchestrator with an empty epistemic matrix/scratchpad."""
        self.scratchpad: Dict[str, Any] = {}
        self.state_trace: List[Dict[str, Any]] = []
        self.reparation_trace: List[str] = []
        self.mode: str = "READY_TO_HAND"  # Or "PRESENT_AT_HAND"

    def initialize_matrix(self, variables: List[str], constraints: List[str]) -> None:
        """
        Executes Step 0: Exploratory Epistemic Action Cycle.
        Writes down a physical matrix representing all current variables and relationships.

        Args:
            variables: List of variable identifiers.
            constraints: List of logical constraints.
        """
        self.scratchpad = {
            "variables": {var: None for var in variables},
            "constraints": constraints,
            "task_irrelevant_dimensions": ["color", "formatting", "exact_phrasing"],
            "status": "INITIALIZED"
        }
        self.state_trace.append(self._snapshot())

    def _snapshot(self) -> Dict[str, Any]:
        """Takes a deep copy snapshot of the current scratchpad."""
        import copy
        return copy.deepcopy(self.scratchpad)

    def update_state(self, updates: Dict[str, Any]) -> None:
        """
        Updates the epistemic scratchpad with new assignments, mimicking external offloading.

        Args:
            updates: Dictionary of variable assignments.
        """
        if self.mode == "PRESENT_AT_HAND":
            self.reparation_trace.append("Cannot update state while in PRESENT_AT_HAND mode. Resolve errors first.")
            return

        for var, value in updates.items():
            if var in self.scratchpad["variables"]:
                self.scratchpad["variables"][var] = value

        self.state_trace.append(self._snapshot())
        self.check_constraints()

    def check_constraints(self) -> None:
        """
        Applies Optimal Feedback Control. Checks for task-interfering anomalies (constraint violations).
        Ignores task-irrelevant dimensions. Triggers present-at-hand on violation.
        """
        # Simplified constraint check mock
        # For example, if two variables are assigned the same coordinate when they shouldn't be
        values = [val for val in self.scratchpad["variables"].values() if val is not None]
        if len(values) != len(set(values)):
            self._trigger_present_at_hand("Constraint Violation: Coordinate overlap detected (duplicate values).")

    def _trigger_present_at_hand(self, reason: str) -> None:
        """
        Triggers a present-at-hand review due to a logical contradiction.

        Args:
            reason: The reason for the failure.
        """
        self.mode = "PRESENT_AT_HAND"
        self.reparation_trace.append(f"TRANSITION TO PRESENT-AT-HAND: {reason}")
        self._execute_algorithmic_reparation()

    def _execute_algorithmic_reparation(self) -> None:
        """
        Diagnoses the error and re-samples the strategy (Algorithmic Reparation).
        """
        self.reparation_trace.append("Executing Algorithmic Reparation...")

        # Diagnostic: Find duplicates
        values_seen = set()
        duplicates = set()
        for var, val in self.scratchpad["variables"].items():
            if val is not None:
                if val in values_seen:
                    duplicates.add(val)
                else:
                    values_seen.add(val)

        self.reparation_trace.append(f"Diagnosis: Duplicate values found: {duplicates}")

        # Re-sampling strategy: Reset conflicting variables to None
        for var, val in self.scratchpad["variables"].items():
            if val in duplicates:
                self.scratchpad["variables"][var] = None
                self.reparation_trace.append(f"Re-sampling: Resetting variable {var}")

        self.reparation_trace.append("Reparation complete. Returning to READY-TO-HAND.")
        self.mode = "READY_TO_HAND"
        self.state_trace.append(self._snapshot())

    def get_final_solution(self) -> Dict[str, Any]:
        """Returns the final verified solution."""
        return self.scratchpad["variables"]

if __name__ == "__main__":
    orchestrator = EpistemicActionOrchestrator()
    orchestrator.initialize_matrix(variables=["A", "B", "C"], constraints=["A != B", "B != C", "A != C"])

    print("Initial State:")
    print(orchestrator.state_trace[0])

    print("\nUpdating state with valid values...")
    orchestrator.update_state({"A": 1, "B": 2})
    print("State:", orchestrator.scratchpad["variables"])

    print("\nUpdating state with a conflict (B=2, C=2)...")
    orchestrator.update_state({"C": 2})
    print("Reparation Trace:")
    for trace in orchestrator.reparation_trace:
        print(f"  {trace}")

    print("\nFinal State after Reparation:")
    print(orchestrator.scratchpad["variables"])
