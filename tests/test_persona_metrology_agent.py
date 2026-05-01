import sys
from unittest.mock import MagicMock
# Mock out nltk so it doesn't fail on missing tabdata
sys.modules['nltk.tabdata'] = MagicMock()

import unittest
import numpy as np
import numpy.testing as npt
from src.conceptual_synthesis.persona_metrology_agent import PersonaMetrologyAgent

class TestPersonaMetrologyAgent(unittest.TestCase):
    def setUp(self):
        self.agent = PersonaMetrologyAgent()

    def test_holographic_circular_convolution(self):
        vec_a = np.array([1, 0, -1])
        vec_b = np.array([0, 1, 0])
        # circular conv of [1, 0, -1] and [0, 1, 0]
        # [1, 0, -1] shifted right by 1 is [-1, 1, 0]
        expected = np.array([-1, 1, 0])
        result = self.agent._holographic_circular_convolution(vec_a, vec_b)
        npt.assert_array_almost_equal(result, expected)

    def test_compute_cfdi_from_sdf_success(self):
        # A matrix where the gradient magnitude is exactly 1
        # d = x
        spatial_matrix = np.array([0.0, 1.0, 2.0, 3.0])
        cfdi = self.agent._compute_cfdi_from_sdf(spatial_matrix, epsilon_tolerance=0.0)
        self.assertLessEqual(cfdi, self.agent.cfdi_threshold)

    def test_compute_cfdi_from_sdf_failure(self):
        # A matrix that violates the Eikonal equation
        spatial_matrix = np.array([0.0, 5.0, 10.0])
        cfdi = self.agent._compute_cfdi_from_sdf(spatial_matrix, epsilon_tolerance=0.0)
        self.assertGreater(cfdi, self.agent.cfdi_threshold)

    def test_execute_petzold_loop_complete(self):
        context = {
            "empirical_friction": [np.array([1, -1]), np.array([-1, 1])],
            "spatial_matrix": np.array([0.0, 1.0, 2.0]),
            "epsilon_tolerance": 0.0
        }
        result = self.agent.execute_petzold_loop(context)
        self.assertEqual(result["status"], "COMPLETE")
        self.assertIn("PART_NAME: 2026_Design_Futures_Report", result["artifact"])
        self.assertLessEqual(result["cfdi"], self.agent.cfdi_threshold)

    def test_execute_petzold_loop_epistemic_escrow(self):
        context = {
            "empirical_friction": [np.array([1, -1]), np.array([-1, 1])],
            "spatial_matrix": np.array([0.0, 10.0, 20.0]), # Violates Eikonal constraint |∇d|=1
            "epsilon_tolerance": 0.0
        }
        result = self.agent.execute_petzold_loop(context)
        self.assertEqual(result["status"], "EPISTEMIC_ESCROW_TRIGGERED")
        self.assertEqual(result["reason"], "CFDI Resolution Collapse")
        self.assertIsNone(result["artifact"])

if __name__ == "__main__":
    unittest.main()
