import sys
from unittest.mock import MagicMock
# Mock out nltk so it doesn't fail on missing tabdata
sys.modules['nltk.tabdata'] = MagicMock()

import unittest
import numpy as np
import numpy.testing as npt
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from conceptual_synthesis.hybrid_system import (
    deterministic_context_engineering,
    neoclassical_compounding,
    symbolic_charge_network,
    algorithmic_photography,
    weaving_algorithm,
    hybrid_synthesis,
)

class TestHybridSystem(unittest.TestCase):

    def test_deterministic_context_engineering(self):
        text = "This is a test sentence for the context engineering function."
        expected = ['test', 'sentenc', 'context', 'engin', 'function']
        self.assertEqual(deterministic_context_engineering(text), expected)

    def test_neoclassical_compounding(self):
        self.assertAlmostEqual(
            neoclassical_compounding(100, 0.05, 1, 10), 162.88946267774415
        )
        self.assertAlmostEqual(
            neoclassical_compounding(100, 0.05, 12, 10), 164.70094976902214
        )

    def test_symbolic_charge_network(self):
        charges = [1, 2]
        interactions = np.array([[0, 1], [1, 0]])
        expected = np.array([2, 1])
        npt.assert_array_equal(
            symbolic_charge_network(2, charges, interactions), expected
        )
        with self.assertRaises(ValueError):
            symbolic_charge_network(3, charges, interactions)

    def test_algorithmic_photography(self):
        image = np.array([[[100, 150, 200]]])
        sepia_image = algorithmic_photography(image)
        self.assertEqual(sepia_image.shape, (1, 1, 3))
        self.assertTrue(np.all(sepia_image >= 0) and np.all(sepia_image <= 255))

    def test_weaving_algorithm(self):
        pattern = weaving_algorithm(10, 5, 30)
        self.assertEqual(pattern.shape, (5, 10))

    def test_hybrid_synthesis(self):
        results = hybrid_synthesis(
            text="This is a test.",
            principal=1000,
            rate=0.05,
            times_compounded=12,
            years=10,
            nodes=2,
            charges=[1, 2],
            interactions=np.array([[0, 1], [1, 0]]),
            image=np.array([[[100, 150, 200]]]),
            width=10,
            height=5,
            rule=90
        )
        self.assertIn("processed_text", results)
        self.assertIn("future_value", results)
        self.assertIn("network_state", results)
        self.assertIn("sepia_image", results)
        self.assertIn("generated_pattern", results)

    def test_weaving_algorithm_bounds(self):
        with self.assertRaises(ValueError):
            weaving_algorithm(5, 5, -1)
        with self.assertRaises(ValueError):
            weaving_algorithm(5, 5, 256)

if __name__ == "__main__":
    unittest.main()
