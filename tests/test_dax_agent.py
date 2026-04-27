import unittest
from unittest.mock import patch, mock_open
import json

from src.conceptual_synthesis.dax_agent import DaxAgent

class TestDaxAgent(unittest.TestCase):
    def setUp(self):
        self.agent = DaxAgent()

    @patch("builtins.open", new_callable=mock_open)
    def test_quickstart_generation(self, mock_file):
        context = {
            "community_signal": "How do I make my first call?",
            "artifact_type": "Quickstart",
            "cfdi": 0.05,
            "ssi": 0.90,
            "endpoint": "/api/v1/init"
        }

        result = self.agent.execute_petzold_loop(context)

        self.assertEqual(result["status"], "COMPLETE")
        self.assertIn("## Quickstart: API in 3 Steps", result["artifact"])
        self.assertIn("```bash", result["artifact"])
        self.assertIn("```python", result["artifact"])

        # Verify Symbolic Scar was written
        mock_file.assert_called_once_with("SymbolicScar.jsonl", "a")
        handle = mock_file()
        handle.write.assert_called_once()
        written_data = json.loads(handle.write.call_args[0][0].strip())
        self.assertEqual(written_data["component"], "/api/v1/init")
        self.assertEqual(written_data["metrics"]["cfdi"], 0.05)

    @patch("builtins.open", new_callable=mock_open)
    def test_triage_response_generation(self, mock_file):
        context = {
            "community_signal": "I'm getting a 401 on the new auth endpoint.",
            "artifact_type": "TriageResponse",
            "cfdi": 0.10,
            "ssi": 0.88,
            "endpoint": "/api/v2/auth",
            "error_pattern": "401 Unauthorized"
        }

        result = self.agent.execute_petzold_loop(context)

        self.assertEqual(result["status"], "COMPLETE")
        self.assertIn("We reproduced this issue.", result["artifact"])
        self.assertIn("```\n# Validated code snippet\n```", result["artifact"])
        self.assertIn("Scar ID:", result["artifact"])

    @patch("builtins.open", new_callable=mock_open)
    def test_friction_report_generation(self, mock_file):
        context = {
            "community_signal": "Batch endpoint missing required param in docs",
            "artifact_type": "FrictionReport",
            "cfdi": 0.02,
            "ssi": 0.95,
            "endpoint": "/api/v1/batch"
        }

        result = self.agent.execute_petzold_loop(context)

        self.assertEqual(result["status"], "COMPLETE")

        # Artifact should be a JSON string
        report = json.loads(result["artifact"])
        self.assertEqual(report["@type"], "FrictionTopographyReport")
        self.assertEqual(report["critical_nodes"][0]["endpoint"], "/api/v1/batch")

    def test_anionic_veto_trigger(self):
        context = {
            "community_signal": "This is a revolutionary new feature!",
            "artifact_type": "TriageResponse",
            "cfdi": 0.05,
            "ssi": 0.90
        }

        result = self.agent.execute_petzold_loop(context)

        self.assertEqual(result["status"], "HALTED")
        self.assertEqual(result["state"], "EPISTEMIC_ESCROW")
        self.assertIn("Anionic Veto Triggered", result["jur"])

    def test_cfdi_threshold_exceeded(self):
        context = {
            "community_signal": "Getting weird errors",
            "artifact_type": "TriageResponse",
            "cfdi": 0.25, # Above 0.15 threshold
            "ssi": 0.90
        }

        result = self.agent.execute_petzold_loop(context)

        self.assertEqual(result["status"], "HALTED")
        self.assertEqual(result["state"], "EPISTEMIC_ESCROW")
        self.assertIn("exceeds threshold", result["jur"])

    def test_ssi_threshold_violation(self):
        context = {
            "community_signal": "How to auth?",
            "artifact_type": "TriageResponse",
            "cfdi": 0.05,
            "ssi": 0.50 # Below 0.85 threshold
        }

        result = self.agent.execute_petzold_loop(context)

        self.assertEqual(result["status"], "HALTED")
        self.assertEqual(result["state"], "EPISTEMIC_ESCROW")
        self.assertIn("SSI", result["jur"])
        self.assertIn("below target threshold", result["jur"])

    def test_invalid_artifact_schema(self):
        context = {
            "community_signal": "Write me a blog post",
            "artifact_type": "MarketingCopy", # Invalid schema
            "cfdi": 0.05,
            "ssi": 0.90
        }

        result = self.agent.execute_petzold_loop(context)

        self.assertEqual(result["status"], "HALTED")
        self.assertEqual(result["state"], "EPISTEMIC_ESCROW")
        self.assertIn("DCCDSchemaGuard Failure", result["jur"])

if __name__ == "__main__":
    unittest.main()
