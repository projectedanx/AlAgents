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
        self.assertEqual(agent.build_version, "1.0.0-SCOS-STRICT")
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
        self.assertIn("# ADR-", result["adr"])
        self.assertIn("C4Context", result["c4_model"])
        self.assertIn("context_map:", result["ddd_context_map"])

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


    def test_observe_adjective_stripping(self):
        """Tests that marketing adjectives are stripped from requirements."""
        agent = VulcanAgent()
        context = {
            "requirements": ["We need a seamless and scalable database", {"domain": "A robust simple system"}],
            "constraints": ["Must be enterprise-grade and simple"]
        }
        result = agent._observe(context)
        self.assertEqual(result["requirements"][0], "We need a and database")
        self.assertEqual(result["requirements"][1]["domain"], "A system")
        self.assertEqual(result["constraints"][0], "Must be and")

    def test_think_nfr_gate(self):
        """Tests the NFR gate logic for architecture selection."""
        agent = VulcanAgent()
        # Test Event-Driven
        obs_event = {
            "nfrs": {"scale_diff_order_of_magnitude": 2, "latency_sensitivity": "low"}
        }
        res_event = agent._think(obs_event)
        self.assertEqual(res_event["selected_architecture"], "Event-Driven")

        # Test RESTful
        obs_rest = {
            "nfrs": {"deploy_cadence_diff_factor": 3.0, "latency_sensitivity": "high"}
        }
        res_rest = agent._think(obs_rest)
        self.assertEqual(res_rest["selected_architecture"], "RESTful Synchronous")

        # Test Modular Monolith
        obs_mono = {
            "nfrs": {"scale_diff_order_of_magnitude": 0, "deploy_cadence_diff_factor": 1.0}
        }
        res_mono = agent._think(obs_mono)
        self.assertEqual(res_mono["selected_architecture"], "Modular Monolith")

    def test_dag_blast_radius(self):
        """Tests the calculation of Gravity Wells and Blast Radius."""
        agent = VulcanAgent()
        context = {
            "microservices": [{"name": "A"}, {"name": "B"}, {"name": "C"}, {"name": "D"}, {"name": "E"}], # 5 services. >20% means >1 dependency.
            "dependencies": {
                "A": ["B", "C"], # A depends on B and C. In-degree: B=1, C=1
                "D": ["C"],      # D depends on C. In-degree: C=2
                "E": ["C"]       # E depends on C. In-degree: C=3
            }
        }
        # In-degree: B:1, C:3. C affects 3/5 = 60% > 20%. B affects 1/5 = 20% <= 20%.
        res = agent._dag({}, context)
        self.assertIn("C", res["gravity_wells"])
        self.assertIn("C", res["blast_radius_flags"])
        self.assertNotIn("B", res["blast_radius_flags"])

    def test_evaluate_cap_theorem_violation(self):
        """Tests that a CAP theorem violation triggers a ValueError."""
        agent = VulcanAgent()
        context = {
            "cap_requirements": {
                "consistency": "perfect",
                "availability": "perfect",
                "partition_tolerance": "required"
            }
        }
        with self.assertRaisesRegex(ValueError, "CAP Theorem Violation"):
            agent._evaluate({}, context)

if __name__ == "__main__":
    unittest.main()
