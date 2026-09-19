"""
Disequilibratory Goal-Setting Engine.

This module implements the Internal Model Control (IMC) Feed-Forward
Goal Tuner for multi-agent dynamic strategic planning. It leverages a
dual cyclic loop combining equilibratory reduction and disequilibratory
production, adjusting goals based on Subjective Well-Being modifiers.
"""

from typing import Dict, Any, List

class DisequilibratoryGoalEngine:
    """
    Manages dynamic strategic planning by applying Model Predictive Control principles
    to avoid 'death by equilibrium' via artificial goal spikes when variance drops.
    """

    def __init__(self, initial_goal: float = 10.0, variance_threshold: float = 0.5):
        """
        Initializes the engine.

        Args:
            initial_goal: The starting numerical representation of the goal.
            variance_threshold: The threshold below which a disequilibratory spike is triggered.
        """
        self.current_goal = initial_goal
        self.variance_threshold = variance_threshold
        self.performance_history: List[float] = []
        self.strategy_log: List[str] = []

        self.strategy_log.append(f"Initialized Goal Engine with Goal: {self.current_goal}")

    def _calculate_variance(self) -> float:
        """Calculates variance over the recent performance history."""
        if len(self.performance_history) < 3:
            return float('inf')  # Not enough data to be 'stagnant'

        recent = self.performance_history[-3:]
        mean = sum(recent) / len(recent)
        variance = sum((x - mean) ** 2 for x in recent) / len(recent)
        return variance

    def apply_subjective_modifier(self, stakeholder_values: Dict[str, float]) -> float:
        """
        Adjusts the objective function to incorporate subjective well-being (e.g., reducing burnout).

        Args:
            stakeholder_values: Dict containing modifiers (e.g., {"well_being": 0.8})

        Returns:
            The modifier multiplier.
        """
        well_being = stakeholder_values.get("well_being", 1.0)
        # If well being is low, we might not spike the goal as hard
        self.strategy_log.append(f"Applied Subjective Modifier: {well_being}")
        return well_being

    def execute_cycle(self, current_performance: float, stakeholder_values: Dict[str, float] = None) -> float:
        """
        Executes one loop of Equilibratory Reduction / Disequilibratory Production.

        Args:
            current_performance: The latest performance metric.
            stakeholder_values: Optional subjective values.

        Returns:
            The new current_goal for the next cycle.
        """
        self.performance_history.append(current_performance)
        self.strategy_log.append(f"Cycle Step - Performance: {current_performance}, Goal: {self.current_goal}")

        # A. Equilibratory Reduction (Feedback Controller)
        deviation = self.current_goal - current_performance
        self.strategy_log.append(f"Equilibratory Reduction: Deviation is {deviation}")

        variance = self._calculate_variance()

        # B. Disequilibratory Production (Feed-Forward Controller)
        if variance < self.variance_threshold:
            # System has converged on a local peak (variance is low).
            # We must spike the goal difficulty to create new discrepancy.
            self.strategy_log.append(f"Disequilibratory Production Triggered (Variance: {variance:.3f} < {self.variance_threshold})")

            modifier = 1.0
            if stakeholder_values:
                modifier = self.apply_subjective_modifier(stakeholder_values)

            # Spike the goal difficulty by 50%, adjusted by subjective modifier
            spike_amount = (self.current_goal * 0.5) * modifier
            self.current_goal += spike_amount
            self.strategy_log.append(f"Goal spiked by {spike_amount:.2f}. New Goal: {self.current_goal:.2f}")

        return self.current_goal

    def export_living_plan(self) -> Dict[str, Any]:
        """Returns the compiled dynamic living plan."""
        return {
            "final_goal": self.current_goal,
            "performance_history": self.performance_history,
            "strategy_log": self.strategy_log
        }


if __name__ == "__main__":
    engine = DisequilibratoryGoalEngine(initial_goal=100.0, variance_threshold=2.0)

    performances = [50.0, 75.0, 95.0, 96.0, 95.5]
    stakeholder_context = {"well_being": 0.8}

    for p in performances:
        engine.execute_cycle(p, stakeholder_context)

    print("Living Plan Export:")
    plan = engine.export_living_plan()
    for log in plan["strategy_log"]:
        print(f"  {log}")
