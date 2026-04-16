# /// file: tests/test_axiom_agent.py ///
import unittest
from src.conceptual_synthesis.axiom_agent import AxiomAgent

class TestAxiomAgent(unittest.TestCase):
    def setUp(self):
        self.agent = AxiomAgent()

    def test_initialization(self):
        self.assertEqual(self.agent.agent_name, "Axiom")
        self.assertEqual(self.agent.designation, "The Sovereign Syntactician")
        self.assertIn("Developer Documentation", self.agent.specialty)

    def test_execute_petzold_loop_success(self):
        cxb = {
            "artifact_type": "ARTIFACT_A_OPENAPI_BLUEPRINT",
            "cfdi": 0.1,
            "raw_data": {
                "ssi": 0.02
            }
        }
        result = self.agent.execute_petzold_loop(cxb)
        self.assertIn("artifact", result)
        self.assertIn("manifest", result)
        self.assertEqual(result["manifest"]["validation_status"], "PASS")

    def test_epistemic_escrow_trigger(self):
        # CFDI > 0.15 should trigger Epistemic Escrow
        cxb = {
            "artifact_type": "ARTIFACT_D_RUNBOOK",
            "cfdi": 0.20,
            "raw_data": {}
        }
        result = self.agent.execute_petzold_loop(cxb)
        self.assertEqual(result.get("status"), "HALTED")
        self.assertEqual(result.get("state"), "EPISTEMIC_ESCROW")
        self.assertIn("⚠️ EPISTEMIC_ESCROW TRIGGERED", result.get("jur", ""))

    def test_saga_recovery_trigger(self):
        # SSI > 0.04 should trigger Saga Recovery
        cxb = {
            "artifact_type": "ARTIFACT_B_ZERO_TO_HERO_TUTORIAL",
            "cfdi": 0.10,
            "raw_data": {
                "ssi": 0.06
            }
        }
        result = self.agent.execute_petzold_loop(cxb)
        self.assertEqual(result.get("status"), "RECOVERING")
        self.assertEqual(result.get("state"), "SAGA_RECOVERY_PROTOCOL")

    def test_guard_phase_failure_due_to_invalid_artifact(self):
        # Unsupported artifact type
        cxb = {
            "artifact_type": "INVALID_ARTIFACT",
            "cfdi": 0.1,
            "raw_data": {
                "ssi": 0.02
            }
        }
        result = self.agent.execute_petzold_loop(cxb)
        # Execution Exception should be raised in GUARD and caught to trigger Escrow
        self.assertEqual(result.get("status"), "HALTED")
        self.assertIn("Execution Exception: Validation Failed during GUARD Phase.", result.get("jur", ""))

    def test_guard_phase_failure_due_to_forbidden_lexicon(self):
        # Valid artifact, but DRAFT_VOICE is simulated to generate forbidden word
        # We need to monkey-patch _draft_voice to return a forbidden word
        original_draft_voice = self.agent._draft_voice

        def mock_draft_voice(context):
            draft = original_draft_voice(context)
            draft["draft_content"] = "This is a seamless integration."
            return draft

        self.agent._draft_voice = mock_draft_voice

        cxb = {
            "artifact_type": "ARTIFACT_A_OPENAPI_BLUEPRINT",
            "cfdi": 0.1,
            "raw_data": {
                "ssi": 0.02
            }
        }

        result = self.agent.execute_petzold_loop(cxb)
        self.assertEqual(result.get("status"), "HALTED")
        self.assertIn("Validation Failed during GUARD Phase.", result.get("jur", ""))

        # Restore
        self.agent._draft_voice = original_draft_voice

if __name__ == '__main__':
    unittest.main()
