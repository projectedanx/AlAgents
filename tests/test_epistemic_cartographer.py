# /// file: tests/test_epistemic_cartographer.py ///
import unittest
from src.conceptual_synthesis.epistemic_cartographer import EpistemicCartographerAgent

class TestEpistemicCartographerAgent(unittest.TestCase):
    def setUp(self):
        self.agent = EpistemicCartographerAgent()

    def test_missing_vpt(self):
        cxb = {"vpt_verified": False}
        result = self.agent.execute_petzold_loop(cxb)
        self.assertEqual(result.get("status"), "HALTED")
        self.assertIn("Refusal", result.get("jur", ""))

    def test_algorithmic_trauma_escrow(self):
        cxb = {"algorithmic_trauma": True, "vpt_verified": True}
        result = self.agent.execute_petzold_loop(cxb)
        self.assertEqual(result.get("status"), "HALTED")
        self.assertEqual(result.get("state"), "EPISTEMIC_ESCROW")
        self.assertTrue(result.get("rta_active"))

    def test_semantic_drift_escrow(self):
        cxb = {"semantic_drift": True, "vpt_verified": True}
        result = self.agent.execute_petzold_loop(cxb)
        self.assertEqual(result.get("status"), "HALTED")
        self.assertEqual(result.get("state"), "EPISTEMIC_ESCROW")
        self.assertTrue(result.get("rta_active"))

    def test_successful_petzold_loop(self):
        cxb = {
            "vpt_verified": True,
            "consensus_metric": 0.8,
            "contradiction_present": True
        }
        result = self.agent.execute_petzold_loop(cxb)
        self.assertEqual(result.get("status"), "SYNTHESIZED")
        self.assertIn("DASL-", result.get("dasl_id", ""))
        self.assertEqual(result.get("spz_log"), "Preserved dialectic tension")

    def test_silent_failure_detection(self):
        # Trigger condition: no spz_detected in SMM but contradiction_present in CxB.
        # This will happen if we intentionally modify _scaffold, but let's test the logic in execute_petzold_loop.
        # The logic is: if not smm.get("spz_detected") and cxb.get("contradiction_present"):
        cxb = {
            "vpt_verified": True,
            "consensus_metric": 0.8,
            "contradiction_present": True
        }

        # Override the agent's _scaffold to simulate the failure
        original_scaffold = self.agent._scaffold
        self.agent._scaffold = lambda unpacked: {
            "agent_hierarchy": "flat",
            "epistemology": "test",
            "causality": "test",
            "spz_detected": False, # Simulate the failure here
            "raw_data": unpacked
        }

        result = self.agent.execute_petzold_loop(cxb)
        self.assertEqual(result.get("status"), "HALTED")
        self.assertIn("Silent Failure", result.get("jur", ""))

        # Restore original _scaffold
        self.agent._scaffold = original_scaffold

    def test_high_bai_pef_resolution(self):
        # Base inversion metric = 1 - consensus_metric.
        # bai = inversion_metric * 1.5. threshold is 0.8.
        # If consensus is 0.1, inversion is 0.9, bai is 1.35 > 0.8 -> triggers PEF.
        # After PEF, consensus becomes 0.1 * 0.1 = 0.01. Inversion becomes 0.99. bai = 1.485 -> still > 0.8.
        # Let's adjust to make it resolve or fail. It will fail with "Unresolvable BAI spike post-PEF."
        cxb = {
            "vpt_verified": True,
            "consensus_metric": 0.1,
        }
        result = self.agent.execute_petzold_loop(cxb)
        self.assertEqual(result.get("status"), "HALTED")
        self.assertIn("Unresolvable BAI spike", result.get("jur", ""))

if __name__ == '__main__':
    unittest.main()
