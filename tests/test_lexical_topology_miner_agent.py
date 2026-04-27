import sys
from unittest.mock import MagicMock
# Mock out nltk so it doesn't fail on missing tabdata
sys.modules['nltk.tabdata'] = MagicMock()

import unittest
from src.conceptual_synthesis.lexical_topology_miner_agent import LexicalTopologyMinerAgent

class TestLexicalTopologyMinerAgent(unittest.TestCase):
    def setUp(self):
        self.agent = LexicalTopologyMinerAgent()

    def test_remove_evaluative_adjectives(self):
        text = "This is a robust and powerful system."
        cleaned = self.agent._remove_evaluative_adjectives(text)
        self.assertEqual(cleaned, "This is a and system.")

    def test_execute_petzold_loop_success(self):
        cxb = {
            "query": "A seamless topological manifold",
            "semantic_drift_metric": 0.5, # cfdi will be 0.0
            "grounding_density": 0.8,
            "betti_1": 0,
            "polysemy": True,
            "target_domain": "DomainA",
            "source_domain": "DomainB"
        }
        result = self.agent.execute_petzold_loop(cxb)
        self.assertEqual(result["status"], "COMPLETE")
        self.assertEqual(result["data"]["semantic_lock"], "PAL2v_FROZEN")
        self.assertEqual(result["data"]["latent_bridge"], "DomainA x DomainB")

    def test_clarification_gate_trigger(self):
        cxb = {
            "query": "An innovative concept",
            "grounding_density": 0.3 # < 0.5 triggers clarification gate
        }
        result = self.agent.execute_petzold_loop(cxb)
        self.assertEqual(result["status"], "HALTED")
        self.assertIn("Clarification Gate", result["jur"])

    def test_cfdi_threshold_exceeded(self):
        cxb = {
            "query": "Concept X",
            "semantic_drift_metric": 1.0, # cfdi will be |1.0 - 0.5| * 0.5 = 0.25 > 0.15
            "grounding_density": 0.9,
            "betti_1": 0
        }
        result = self.agent.execute_petzold_loop(cxb)
        self.assertEqual(result["status"], "HALTED")
        self.assertIn("CFDI 0.2500 > 0.15", result["jur"])

    def test_topological_obstruction(self):
        cxb = {
            "query": "Concept Y",
            "semantic_drift_metric": 0.5, # cfdi = 0.0
            "grounding_density": 0.9,
            "betti_1": 1 # Obstruction
        }
        result = self.agent.execute_petzold_loop(cxb)
        self.assertEqual(result["status"], "HALTED")
        self.assertIn("Topological Obstruction", result["jur"])

if __name__ == "__main__":
    unittest.main()
