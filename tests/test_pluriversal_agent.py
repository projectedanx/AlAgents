# /// file: tests/test_pluriversal_agent.py ///
import unittest
from unittest.mock import MagicMock
import sys
import numpy as np

# Mock nltk to prevent download issues in CI environments
sys.modules['nltk'] = MagicMock()
sys.modules['nltk.corpus'] = MagicMock()
sys.modules['nltk.stem'] = MagicMock()
sys.modules['nltk.tokenize'] = MagicMock()

from src.conceptual_synthesis.pluriversal_agent import PluriversalFeatureDiscoveryAgent

class TestPluriversalFeatureDiscoveryAgent(unittest.TestCase):
    def setUp(self):
        self.agent = PluriversalFeatureDiscoveryAgent()

    def test_initialization(self):
        self.assertEqual(self.agent.agent_name, "AEW-SCC")
        self.assertEqual(self.agent.beta_1, 0.75)
        self.assertEqual(self.agent.beta_0, 0.95)

    def test_z_axis_routing(self):
        # Should route to phantom dimension if contradiction > 0.5
        h_k = self.agent._z_axis_routing(1.0)
        self.assertGreater(h_k, 0.0)

        # Should not route if contradiction <= 0.5
        h_k_low = self.agent._z_axis_routing(0.4)
        self.assertEqual(h_k_low, 0.0)

    def test_paraconsistent_fusion(self):
        feature_a = np.array([0.8, 0.2])
        feature_b = np.array([0.1, 0.9])
        fusion = self.agent._paraconsistent_fusion(feature_a, feature_b)
        self.assertTrue((fusion > 0).all())
        self.assertEqual(len(fusion), 2)

    def test_discover_feature_validation(self):
        # High stress should cause rejection due to beta_0 preservation loss
        hypothesis_rejected = self.agent.discover_feature(stress_pi=5.0, architectural_bias=0.1)
        self.assertEqual(hypothesis_rejected['status'], 'REJECTED_BY_EEA')

        # Normal stress should pass validation
        hypothesis_validated = self.agent.discover_feature(stress_pi=0.1, architectural_bias=0.1)
        self.assertEqual(hypothesis_validated['status'], 'VALIDATED')
        self.assertIn('phantom_dimension', hypothesis_validated)
        self.assertIn('novelty', hypothesis_validated)

if __name__ == '__main__':
    unittest.main()
