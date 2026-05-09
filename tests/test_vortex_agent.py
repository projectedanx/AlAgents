import unittest
import numpy as np
from src.conceptual_synthesis.vortex_agent import VortexArchitectAgent, SemanticMutexDaemon
from src.conceptual_synthesis.pluriversal_architecture import SymbolicScar

class TestVortexArchitectAgent(unittest.TestCase):
    def setUp(self):
        self.agent = VortexArchitectAgent()
        # Mock random to prevent flaky tests
        self.agent.calculate_cfdi = lambda: 0.1  # Set CFDI below threshold for normal processing

    def test_betti_1_loop_detection(self):
        # A loop where the last two actions repeat
        trace_with_loop = ["start", "A", "B", "A", "B"]
        self.assertTrue(self.agent.detect_betti_1_loop(trace_with_loop))

        trace_without_loop = ["start", "A", "B", "C", "D"]
        self.assertFalse(self.agent.detect_betti_1_loop(trace_without_loop))

    def test_evaluate_pal2v(self):
        # Test Paraconsistent Annotated Logic weighting (Golden Scar Protocol)
        result = self.agent.evaluate_pal2v(0.9, 0.4)
        self.assertEqual(result["dominant_val"], 0.9)
        self.assertEqual(result["dominant_weight"], 1.618)
        self.assertEqual(result["subordinate_val"], 0.4)
        self.assertEqual(result["subordinate_weight"], 1.0)

    def test_trigger_epistemic_escrow(self):
        jur = self.agent.trigger_epistemic_escrow("Testing JUR")
        self.assertEqual(jur["status"], "EPISTEMIC_ESCROW")
        self.assertEqual(jur["reason"], "Testing JUR")

    def test_process_intent_success(self):
        result = self.agent.process_intent("Implement topological guardrails")
        self.assertEqual(result["status"], "SUCCESS")
        self.assertTrue("ast" in result)
        self.assertEqual(result["ast"]["ast_node"], "Validated_FullStack")

    def test_process_intent_cfdi_failure(self):
        # Mock high CFDI
        self.agent.calculate_cfdi = lambda: 0.99
        result = self.agent.process_intent("Ambiguous requirement")
        self.assertEqual(result["status"], "EPISTEMIC_ESCROW")
        self.assertTrue("CFDI" in result["reason"])

    def test_process_intent_betti_loop(self):
        trace = ["A", "B", "A", "B"]
        result = self.agent.process_intent("Trigger loop", trace=trace)
        self.assertEqual(result["status"], "EPISTEMIC_ESCROW")
        self.assertEqual(result["reason"], "Betti-1 Loop Detected")

class TestSemanticMutexDaemon(unittest.TestCase):
    def setUp(self):
        self.daemon = SemanticMutexDaemon()

    def test_mutex_lock(self):
        self.assertTrue(self.daemon.acquire_ast_lock("node_1"))
        self.assertFalse(self.daemon.acquire_ast_lock("node_1"))
        self.daemon.release_ast_lock("node_1")
        self.assertTrue(self.daemon.acquire_ast_lock("node_1"))

if __name__ == "__main__":
    unittest.main()
