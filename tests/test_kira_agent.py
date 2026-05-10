import unittest
from src.conceptual_synthesis.kira_agent import KiraAgent

class TestKiraAgent(unittest.TestCase):
    def setUp(self):
        self.agent = KiraAgent()

    def test_scope_isolation_gate_failure(self):
        context = {"event_trigger": "im.message.receive_v1"} # Missing scopes and environment
        result = self.agent.execute_petzold_loop("Build a bot", context)
        self.assertEqual(result["status"], "HALTED_EPISTEMIC_ESCROW")
        self.assertIn("REJECTED", result["artifacts"]["gate_rejection"])

    def test_petzold_loop_success(self):
        context = {
            "event_trigger": "im.message.receive_v1",
            "required_scopes": ["im:message"],
            "environment": "ngrok",
            "card_intent": "Server down."
        }
        result = self.agent.execute_petzold_loop("Build a monitoring bot", context)
        self.assertEqual(result["status"], "COMPLETE")
        self.assertIn("webhook_ingress", result["artifacts"]["code"])
        self.assertEqual(result["artifacts"]["code"]["card_json"]["msg_type"], "interactive")

if __name__ == '__main__':
    unittest.main()
