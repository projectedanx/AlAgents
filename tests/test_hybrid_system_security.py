import unittest
from unittest.mock import MagicMock
import sys
import os

# Mock nltk and numpy to avoid dependency issues during tests
sys.modules['nltk'] = MagicMock()
sys.modules['nltk.corpus'] = MagicMock()
sys.modules['nltk.stem'] = MagicMock()
sys.modules['nltk.tokenize'] = MagicMock()
sys.modules['numpy'] = MagicMock()

# Import the function after mocking
from src.conceptual_synthesis.hybrid_system import neoclassical_compounding

class TestHybridSystemSecurity(unittest.TestCase):
    def test_neoclassical_compounding_zero_times_compounded(self):
        """Test that neoclassical_compounding raises ValueError when times_compounded is 0."""
        with self.assertRaisesRegex(ValueError, "times_compounded must be greater than zero"):
            neoclassical_compounding(1000, 0.05, 0, 5)

    def test_neoclassical_compounding_negative_times_compounded(self):
        """Test that neoclassical_compounding raises ValueError when times_compounded is negative."""
        with self.assertRaisesRegex(ValueError, "times_compounded must be greater than zero"):
            neoclassical_compounding(1000, 0.05, -1, 5)

    def test_neoclassical_compounding_positive_times_compounded(self):
        """Test that neoclassical_compounding works with positive times_compounded."""
        # principal * (1 + rate / times_compounded) ** (times_compounded * years)
        # 1000 * (1 + 0.05 / 1) ** (1 * 1) = 1000 * 1.05 = 1050
        result = neoclassical_compounding(1000, 0.05, 1, 1)
        self.assertEqual(result, 1050.0)

if __name__ == '__main__':
    unittest.main()
