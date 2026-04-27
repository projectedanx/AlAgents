# /// file: tests/test_vulcan_agent.py ///
# <think>
# Components: TestVulcanAgent
# Dependencies: unittest, unittest.mock, VulcanAgent
# Data Flows: None
# Function Signatures:
#   - test_vulcan_initialization(self) -> None
#   - test_execute_petzold_loop_success(self) -> None
#   - test_mereological_mandate_violation(self) -> None
#   - test_shared_database_anathema_violation(self) -> None
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

    def test_execute_petzold_loop_success(self):
        """Tests successful architecture generation loop."""
        agent = VulcanAgent()
        context = {
            "requirements": [{"domain": "Billing"}],
            "microservices": [{"name": "BillingService", "inherits_state": False}],
            "databases": [{"name": "BillingDB", "writers": ["BillingService"]}]
        }
        result = agent.execute_petzold_loop(context)

        self.assertEqual(result["status"], "COMPLETE")
        self.assertIn("Architecture Decision Record", result["adr"])
        self.assertIn("C4Context", result["c4_model"])
        self.assertIn("Domain:", result["ddd_context_map"])

    def test_mereological_mandate_violation(self):
        """Tests failure during DAG phase due to Mereological Mandate violation."""
        agent = VulcanAgent()
        context = {
            "requirements": [{"domain": "Billing"}],
            "microservices": [{"name": "BillingService", "inherits_state": True}],
            "databases": [{"name": "BillingDB", "writers": ["BillingService"]}]
        }
        result = agent.execute_petzold_loop(context)

        self.assertEqual(result["status"], "HALTED")
        self.assertEqual(result["state"], "EPISTEMIC_ESCROW")
        self.assertIn("Mereological Mandate Violation", result["jur"])

    def test_shared_database_anathema_violation(self):
        """Tests failure during EVALUATE phase due to Shared Database Anathema violation."""
        agent = VulcanAgent()
        context = {
            "requirements": [{"domain": "Billing"}],
            "microservices": [{"name": "BillingService", "inherits_state": False}],
            "databases": [{"name": "SharedDB", "writers": ["BillingService", "AuthService"]}]
        }
        result = agent.execute_petzold_loop(context)

        self.assertEqual(result["status"], "HALTED")
        self.assertEqual(result["state"], "EPISTEMIC_ESCROW")
        self.assertIn("Shared Database Anathema Violation", result["jur"])


    def test_observe_method(self):
        """Tests the _observe method correctly extracts requirements and constraints."""
        agent = VulcanAgent()

        # Test with provided context
        context_full = {
            "requirements": [{"domain": "Billing"}],
            "constraints": ["No shared DBs", "Strict DDD"],
            "extra_field": "should be ignored"
        }
        result_full = agent._observe(context_full)
        self.assertEqual(result_full["requirements"], [{"domain": "Billing"}])
        self.assertEqual(result_full["constraints"], ["No shared DBs", "Strict DDD"])
        self.assertNotIn("extra_field", result_full)

        # Test with missing keys (defaults to empty list)
        context_empty = {}
        result_empty = agent._observe(context_empty)
        self.assertEqual(result_empty["requirements"], [])
        self.assertEqual(result_empty["constraints"], [])

if __name__ == "__main__":
    unittest.main()
