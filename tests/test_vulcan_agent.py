# /// file: tests/test_vulcan_agent.py ///
# <think>
# Components: TestVulcanAgent
# Dependencies: unittest, unittest.mock, VulcanAgent
# Data Flows: None
# Function Signatures: test_vulcan_initialization(self) -> None
# </think>

import unittest
from unittest.mock import MagicMock
import sys
import os

# Mock dependencies to avoid download/import issues
sys.modules['nltk'] = MagicMock()
sys.modules['nltk.corpus'] = MagicMock()
sys.modules['nltk.stem'] = MagicMock()
sys.modules['nltk.tokenize'] = MagicMock()
# sys.modules["numpy"] = MagicMock()

# Ensure src is in path to allow standard module discovery
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from conceptual_synthesis.vulcan_agent import VulcanAgent

class TestVulcanAgent(unittest.TestCase):
    """Test suite for the VulcanAgent."""

    def test_vulcan_initialization(self):
        """Verifies correct property initialization per configuration matrix."""
        agent = VulcanAgent()

        self.assertEqual(agent.agent_name, "VULCAN")
        self.assertEqual(agent.designation, "The Brutalist")
        self.assertEqual(agent.build_version, "1.0.0")
        self.assertEqual(agent.color_designation, "#FF4500")

        self.assertIn("Distributed System Design", agent.specialty)
        self.assertIn("Strict Domain-Driven Design (DDD)", agent.specialty)

        self.assertTrue(agent.when_to_use.startswith("Pre-coding phase for any application"))

        self.assertIn("G_GOAL_ORIENTATION", agent.epistemic_matrix)
        self.assertIn("primary", agent.epistemic_matrix["G_GOAL_ORIENTATION"])
        self.assertEqual(
            agent.epistemic_matrix["G_NEGATIVE_ANTIGOALS"]["forbidden_practices"][0],
            "Semantic Saponification (bleeding of distinct business domains)"
        )

if __name__ == "__main__":
    unittest.main()
