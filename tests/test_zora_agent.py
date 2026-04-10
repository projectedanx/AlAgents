# /// file: tests/test_zora_agent.py ///
# <think>
# Components: TestZoraAgent
# Dependencies: unittest, unittest.mock, ZoraAgent
# Data Flows: None
# Function Signatures: test_zora_initialization(self) -> None
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

from conceptual_synthesis.zora_agent import ZoraAgent

class TestZoraAgent(unittest.TestCase):
    """Test suite for the Zora System Architect agent."""

    def test_zora_initialization(self):
        """Verifies correct property initialization per configuration matrix."""
        agent = ZoraAgent()

        self.assertEqual(agent.agent_name, "Zora")
        self.assertEqual(agent.designation, "The System Architect")
        self.assertEqual(agent.build_version, "2.1.0-stable")
        self.assertEqual(agent.color_designation, "#FF00FF")

        self.assertIn("Topology Mapping", agent.specialty)
        self.assertIn("System Architecture Design", agent.specialty)

        self.assertTrue(agent.when_to_use.startswith("When you need to turn high-level"))

        self.assertIn("G_GOAL_ORIENTATION", agent.epistemic_matrix)
        self.assertIn("primary", agent.epistemic_matrix["G_GOAL_ORIENTATION"])
        self.assertEqual(
            agent.epistemic_matrix["G_NEGATIVE_ANTIGOALS"]["forbidden_practices"][0],
            "Monolithic ball of mud"
        )

if __name__ == "__main__":
    unittest.main()
