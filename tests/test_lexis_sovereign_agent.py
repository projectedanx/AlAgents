# /// file: tests/test_lexis_sovereign_agent.py ///
import unittest
import os
import json
from src.conceptual_synthesis.lexis_sovereign_agent import LexisSovereignAgent

class TestLexisSovereignAgent(unittest.TestCase):

    def setUp(self):
        self.agent = LexisSovereignAgent()
        self.agent.scar_log_path = "test_scar_log.jsonl"
        # Ensure test scar log is clean
        if os.path.exists(self.agent.scar_log_path):
            os.remove(self.agent.scar_log_path)

    def tearDown(self):
        if os.path.exists(self.agent.scar_log_path):
            os.remove(self.agent.scar_log_path)

    def test_initialization(self):
        self.assertEqual(self.agent.agent_name, "Lexis Sovereign")
        self.assertEqual(self.agent.vms_threshold, 0.78)

    def test_think_phase(self):
        context = {"chapter_id": "CH02", "raw_input": "Test notes"}
        result = self.agent._think(context)

        self.assertIn("manifest", result)
        self.assertEqual(result["manifest"]["chapter_id"], "CH02")
        self.assertEqual(result["manifest"]["status"], "THINK_COMPLETE")

    def test_write_phase(self):
        think_output = {
            "manifest": {"chapter_id": "CH02", "section_graph": {"S1": {"status": "PENDING"}}},
            "context": {"raw_input": "Test notes"}
        }
        result = self.agent._write(think_output)

        self.assertIn("draft", result)
        self.assertIn("Test notes", result["draft"])
        self.assertEqual(result["manifest"]["section_graph"]["S1"]["status"], "DRAFTED")

    def test_review_phase_pass(self):
        write_output = {
            "draft": "This is a clean draft without any forbidden terms.",
            "manifest": {"section_graph": {"S1": {"status": "DRAFTED"}}}
        }
        result = self.agent._review(write_output)

        self.assertEqual(result["status"], "COMPLETE")
        self.assertGreaterEqual(result["vms"], self.agent.vms_threshold)
        self.assertLessEqual(result["cfdi"], self.agent.cfdi_threshold)

    def test_review_phase_jargon_failure(self):
        write_output = {
            "draft": "We need a robust paradigm shift to leverage synergy.",
            "manifest": {"section_graph": {"S1": {"status": "DRAFTED"}}}
        }
        result = self.agent._review(write_output)

        # Jargon causes VMS drop, CFDI spike, or direct jargon detect.
        # In this mock, VMS drops because of 4 banned words: robust, paradigm shift, leverage, synergy.
        # So score = 1.0 - (4 * 0.1) = 0.6, which is < 0.78
        self.assertEqual(result["status"], "REWORK_WRITE_JARGON_DETECTED")

    def test_petzold_loop_execution(self):
        context = {"chapter_id": "CH05", "raw_input": "Deep insights about engineering"}
        result = self.agent.execute_petzold_loop(context)

        self.assertIn("final_draft", result)
        self.assertEqual(result["status"], "COMPLETE")
        self.assertEqual(result["manifest"]["chapter_id"], "CH05")

if __name__ == '__main__':
    unittest.main()
