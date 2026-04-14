import sys
from unittest.mock import MagicMock
# Mock out nltk so it doesn't fail on missing tabdata
sys.modules['nltk.tabdata'] = MagicMock()

import unittest
import numpy as np
import numpy.testing as npt
from src.conceptual_synthesis.base_agent import BaseAgent

class TestBaseAgent(unittest.TestCase):
    def setUp(self):
        self.agent = BaseAgent()

    def test_run(self):
        # Sample inputs
        text = "This is a test sentence."
        principal = 1000
        rate = 0.05
        times_compounded = 12
        years = 10
        nodes = 3
        charges = [1.0, 2.0, 3.0]
        interactions = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
        image = np.array([[[100, 150, 200]]])
        width = 5
        height = 5
        rule = 30

        # Run the agent
        result = self.agent.run(
            text,
            principal,
            rate,
            times_compounded,
            years,
            nodes,
            charges,
            interactions,
            image,
            width,
            height,
            rule,
        )

        # Assertions
        self.assertIsInstance(result, dict)
        self.assertEqual(result["processed_text"], ['test', 'sentenc'])
        self.assertAlmostEqual(result["future_value"], 1647.0094976902204)
        npt.assert_array_equal(result["network_state"], np.array([2., 4., 2.]))
        npt.assert_array_almost_equal(result["sepia_image"], np.array([[[192.45, 171.4 , 133.5 ]]]))
        self.assertEqual(result["generated_pattern"].shape, (5, 5))

    def test_symbolic_charge_network(self):
        charges = [1, 2]
        interactions = np.array([[0, 1], [1, 0]])
        expected = np.array([2, 1])
        npt.assert_array_equal(
            self.agent._symbolic_charge_network(2, charges, interactions), expected
        )
        with self.assertRaises(ValueError):
            self.agent._symbolic_charge_network(3, charges, interactions)
        with self.assertRaises(ValueError):
            self.agent._symbolic_charge_network(2, charges, np.array([[0, 1, 0], [1, 0, 0]]))

    def test_weaving_algorithm_bounds(self):
        with self.assertRaises(ValueError):
            self.agent._weaving_algorithm(5, 5, -1)
        with self.assertRaises(ValueError):
            self.agent._weaving_algorithm(5, 5, 256)


    def test_triangle_logic_core(self):
        self.assertTrue(self.agent._triangle_logic_core([True, True, True]))
        self.assertFalse(self.agent._triangle_logic_core([True, False, True]))
        self.assertFalse(self.agent._triangle_logic_core([]))

    def test_square_state_preservation(self):
        state = np.array([10.0, 20.0])
        update = np.array([30.0, 40.0])
        expected = np.array([10.0 * 0.618 + 30.0 * (1.0 - 0.618), 20.0 * 0.618 + 40.0 * (1.0 - 0.618)])
        npt.assert_array_almost_equal(self.agent._square_state_preservation(state, update), expected)

    def test_hexagon_combinatory_synthesis(self):
        streams = [np.array([1.0, 2.0]), np.array([3.0, 4.0]), np.array([5.0, 6.0])]
        result = self.agent._hexagon_combinatory_synthesis(streams)

        stacked_streams = np.stack(streams)
        mean_stream = np.mean(stacked_streams, axis=0)
        variance_penalty = np.var(stacked_streams, axis=0) * 0.1
        expected = mean_stream - variance_penalty

        npt.assert_array_almost_equal(result, expected)

        with self.assertRaises(ValueError):
            self.agent._hexagon_combinatory_synthesis([])

if __name__ == "__main__":
    unittest.main()
