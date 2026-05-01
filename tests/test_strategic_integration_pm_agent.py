import sys
from unittest.mock import MagicMock
# Mock out nltk so it doesn't fail on missing tabdata
sys.modules['nltk.tabdata'] = MagicMock()

import unittest
import numpy as np
import numpy.testing as npt
from src.conceptual_synthesis.strategic_integration_pm_agent import StrategicIntegrationProjectManagerAgent

class TestStrategicIntegrationProjectManagerAgent(unittest.TestCase):
    def setUp(self):
        self.agent = StrategicIntegrationProjectManagerAgent()

    def test_calculate_topological_derivative_of_dissonance(self):
        conflict_a = np.array([1.0, 2.0, 3.0])
        conflict_b = np.array([0.5, 1.0, 1.5])

        # Manually compute expected:
        # a_anchored = [1.618, 3.236, 4.854]
        # b_anchored = [0.5, 1.0, 1.5]
        # gradient of a_anchored: [(3.236-1.618), (4.854-1.618)/2, (4.854-3.236)] = [1.618, 1.618, 1.618]
        # gradient of b_anchored: [0.5, 0.5, 0.5]
        # sum: [2.118, 2.118, 2.118]

        expected = np.array([2.118, 2.118, 2.118])
        result = self.agent._calculate_topological_derivative_of_dissonance(conflict_a, conflict_b)
        npt.assert_array_almost_equal(result, expected)

    def test_epsilon_tolerance_paraconsistency_transition_fit(self):
        # deviation = |1.1 - 1.0| = 0.1 <= 0.15
        result = self.agent._epsilon_tolerance_paraconsistency(1.1, 0.15)
        self.assertEqual(result, "TRANSITION_FIT")

    def test_epsilon_tolerance_paraconsistency_eikonal_violation(self):
        # deviation = |1.5 - 1.0| = 0.5 > 0.15
        result = self.agent._epsilon_tolerance_paraconsistency(1.5, 0.15)
        self.assertEqual(result, "EIKONAL_VIOLATION")

    def test_epsilon_tolerance_paraconsistency_resolution_collapse(self):
        # deviation = |0.0 - 1.0| = 1.0 > 0.15 AND debt_state == 0.0
        result = self.agent._epsilon_tolerance_paraconsistency(0.0, 0.15)
        self.assertEqual(result, "RESOLUTION_COLLAPSE")

    def test_execute_petzold_loop_complete(self):
        context = {
            "dominant_stakeholder_vector": np.array([1.0, 2.0, 3.0]),
            "subordinate_stakeholder_vector": np.array([0.5, 1.0, 1.5]),
            "technical_debt_gradient": 1.05,
            "epsilon_tolerance": 0.15
        }
        result = self.agent.execute_petzold_loop(context)
        self.assertEqual(result["status"], "COMPLETE")
        self.assertEqual(result["debt_status"], "TRANSITION_FIT")
        self.assertIn("PART_NAME: 2026_Operational_Workflow", result["artifact"])

    def test_execute_petzold_loop_eikonal_violation(self):
        context = {
            "dominant_stakeholder_vector": np.array([1.0, 2.0]),
            "subordinate_stakeholder_vector": np.array([0.5, 1.0]),
            "technical_debt_gradient": 1.5,
            "epsilon_tolerance": 0.15
        }
        result = self.agent.execute_petzold_loop(context)
        self.assertEqual(result["status"], "EPISTEMIC_ESCROW_TRIGGERED")
        self.assertEqual(result["reason"], "EIKONAL_VIOLATION")
        self.assertIsNone(result["artifact"])

if __name__ == "__main__":
    unittest.main()
