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
        self.assertIn("## Quickstart: [API Name] in 3 Steps", result["artifact"])
        self.assertIn("```bash", result["artifact"])

        self.assertIn("Expected output:", result["artifact"])

        # Verify Symbolic Scar was written
        mock_file.assert_called_once_with("SymbolicScar.jsonl", "a")
        handle = mock_file()
        handle.write.assert_called_once()
        written_data = json.loads(handle.write.call_args[0][0].strip())
        self.assertEqual(written_data["endpoint_affected"], "/api/v1/init")
        self.assertEqual(written_data["cfdi_score"], 0.05)
        self.assertIn("VSA_HV_", written_data["scar_id"])

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
        self.assertIn("Doc PR: #123", result["artifact"])

        # verify scar
        handle = mock_file()
        written_data = json.loads(handle.write.call_args[0][0].strip())
        self.assertEqual(written_data["error_code"], "401 Unauthorized")

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
        self.assertEqual(report["@context"], "https://schema.dax-01.internal/FrictionReport/v2")

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
            "community_signal": "I got an error",
            "artifact_type": "TriageResponse",
            "cfdi": 0.05,
            "ssi": 0.50 # Below 0.85 threshold, and not novice
        }

        result = self.agent.execute_petzold_loop(context)

        self.assertEqual(result["status"], "HALTED")
        self.assertEqual(result["state"], "EPISTEMIC_ESCROW")
        self.assertIn("SSI", result["jur"])
        self.assertIn("below target threshold", result["jur"])

    @patch("builtins.open", new_callable=mock_open)
    def test_novice_detection(self, mock_file):
        context = {
            "community_signal": "what does this error mean? how to fix it?",
            "artifact_type": "TriageResponse",
            "cfdi": 0.05,
            "ssi": 0.75 # Below normal 0.85, but above adjusted 0.70
        }

        result = self.agent.execute_petzold_loop(context)
        self.assertEqual(result["status"], "COMPLETE")

    def test_run_debridement_cycle(self):
        import os
        mock_scars = [
            json.dumps({"scar_id": "1", "debridement_eligible": True, "status": "OPEN"}) + "\n",
            json.dumps({"scar_id": "2", "debridement_eligible": False, "status": "OPEN"}) + "\n"
        ]
        test_path = "test_debridement_scar.jsonl"
        with open(test_path, "w") as f:
            f.writelines(mock_scars)

        old_path = self.agent.scar_log_path
        self.agent.scar_log_path = test_path

        self.agent.run_debridement_cycle()

        with open(test_path, "r") as f:
            lines = f.readlines()
            scar1 = json.loads(lines[0].strip())
            scar2 = json.loads(lines[1].strip())

        self.assertEqual(scar1["status"], "CLOSED")
        self.assertEqual(scar2["status"], "OPEN")

        os.remove(test_path)
        self.agent.scar_log_path = old_path

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