import unittest
import numpy as np
from src.conceptual_synthesis.infomorphism_agent import InfomorphismAgent

class TestInfomorphismAgent(unittest.TestCase):

    def setUp(self):
        self.agent = InfomorphismAgent()

    def test_calculate_inverse_safety_state(self):
        human_tension = 3.0
        ai_determinism = 4.0
        # Expected calculation:
        # vec_h = [3.0, 0.0]
        # vec_ai = [0.0, 4.0]
        # superposition = [3.0, 4.0]
        # norm = sqrt(3^2 + 4^2) = 5.0
        # inverse_safety_magnitude = 5.0 * 1.618 = 8.09
        expected_result = 8.09
        result = self.agent._calculate_inverse_safety_state(human_tension, ai_determinism)
        self.assertAlmostEqual(result, expected_result, places=2)

    def test_execute_infomorphism_loop_success(self):
        context = {
            'human_tension': 3.0,
            'ai_determinism': 4.0
        }
        result = self.agent.execute_infomorphism_loop(context)

        self.assertEqual(result["status"], "SUPERPOSITION_MAINTAINED")
        self.assertAlmostEqual(result["inverse_safety_state"], 8.09, places=2)
        self.assertTrue(result["epistemic_markers"]["uncertainty_present"])
        self.assertTrue(result["epistemic_markers"]["contradiction_present"])
        self.assertTrue(result["epistemic_markers"]["resonance_achieved"])

    def test_execute_infomorphism_loop_default_context(self):
        context = {}
        result = self.agent.execute_infomorphism_loop(context)

        self.assertEqual(result["status"], "SUPERPOSITION_MAINTAINED")
        self.assertEqual(result["inverse_safety_state"], 0.0)

if __name__ == '__main__':
    unittest.main()
