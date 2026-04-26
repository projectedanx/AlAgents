# /// file: tests/test_whimsy_agent.py ///
import unittest
import os
import json
from src.conceptual_synthesis.whimsy_agent import WhimsyAgent

class TestWhimsyAgent(unittest.TestCase):
    def setUp(self):
        self.agent = WhimsyAgent()
        # Ensure we have a clean slate for the log file
        self.test_scar_path = "test_SymbolicScar.jsonl"
        self.agent.scar_log_path = self.test_scar_path
        if os.path.exists(self.test_scar_path):
            os.remove(self.test_scar_path)

    def tearDown(self):
        if os.path.exists(self.test_scar_path):
            os.remove(self.test_scar_path)

    def test_observe_and_orient_open_zone(self):
        context = {
            "component_id": "dash_loader",
            "component_type": "loading",
            "locale": "en-US",
            "function_label": "Loading data",
            "context_tags": ["data_load"],
            "manifold_target": "alpha"
        }
        obs = self.agent._observe(context)
        ori = self.agent._orient(obs)
        self.assertEqual(ori["status"], "ORIENT_COMPLETE")
        self.assertEqual(ori["zone"], "OPEN")

    def test_hard_lockout_suppression(self):
        context = {
            "component_id": "payment_err",
            "component_type": "payment_failure",
            "locale": "en-US",
            "function_label": "Payment failed",
            "context_tags": ["payment", "error"],
            "manifold_target": "alpha"
        }
        res = self.agent.execute_petzold_loop(context)
        self.assertEqual(res["status"], "SUPPRESSED")
        self.assertIn("Zone is HARD_LOCKOUT", res["reason"])

    def test_restricted_zone_beta_manifold_allowed(self):
        context = {
            "component_id": "payment_success",
            "component_type": "payment_success",
            "locale": "en-US",
            "function_label": "Payment successful",
            "context_tags": ["payment", "success"],
            "manifold_target": "beta"
        }
        res = self.agent.execute_petzold_loop(context)
        self.assertEqual(res["status"], "COMPLETE")
        self.assertIn("artifact", res)
        self.assertEqual(res["artifact"]["manifold"], "beta")

    def test_restricted_zone_alpha_manifold_suppressed(self):
        context = {
            "component_id": "payment_success",
            "component_type": "payment_success",
            "locale": "en-US",
            "function_label": "Payment successful",
            "context_tags": ["payment", "success"],
            "manifold_target": "alpha"
        }
        res = self.agent.execute_petzold_loop(context)
        self.assertEqual(res["status"], "SUPPRESSED")
        self.assertIn("Zone is RESTRICTED", res["reason"])

    def test_scar_proximity_search_suppression(self):
        # Create a mock scar
        scar_entry = {
            "scar_id": "SCAR-123",
            "component": "some_component",
            "attempted_injection": "test",
            "failure_mode": "test",
            "CFDI_at_failure": 0.5,
            "context_tag": ["toxic_tag"],
            "rule_derived": "test",
            "timestamp": "2026-01-01T00:00:00Z"
        }
        with open(self.test_scar_path, "w") as f:
            f.write(json.dumps(scar_entry) + "\n")

        context = {
            "component_id": "toxic_loader",
            "component_type": "loading",
            "locale": "en-US",
            "function_label": "Loading data",
            "context_tags": ["toxic_tag", "data_load"],
            "manifold_target": "alpha"
        }

        res = self.agent.execute_petzold_loop(context)
        self.assertEqual(res["status"], "SUPPRESSED_BY_SCAR")

    def test_cultural_calibration_gate(self):
        context = {
            "component_id": "dash_loader",
            "component_type": "loading",
            "locale": "ja-JP", # Should block sarcastic text
            "function_label": "Loading data",
            "context_tags": ["data_load"],
            "manifold_target": "alpha"
        }

        # We manually inject a sarcastic draft in phase 1 by mocking it
        obs = self.agent._observe(context)
        ori = self.agent._orient(obs)
        d1 = self.agent._decide_phase_1(ori)
        # Override drafts to only have a sarcastic one that passes CFDI
        d1["drafts"] = [{"text": "Very sarcastic text", "tone": "sarcastic"}]

        d2 = self.agent._decide_phase_2(d1)
        self.assertEqual(d2["status"], "SUPPRESSED")
        self.assertIn("No valid drafts passed", d2["reason"])

        # Verify scar was minted
        self.assertTrue(os.path.exists(self.test_scar_path))
        with open(self.test_scar_path, "r") as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 1)
            scar = json.loads(lines[0])
            self.assertEqual(scar["failure_mode"], "CFDI_SPIKE_OR_CULTURE_GATE")

    def test_full_petzold_loop_alpha_success(self):
        context = {
            "component_id": "dash_loader",
            "component_type": "loading",
            "locale": "en-US",
            "function_label": "Loading data",
            "context_tags": ["data_load"],
            "manifold_target": "alpha"
        }
        res = self.agent.execute_petzold_loop(context)
        self.assertEqual(res["status"], "COMPLETE")
        self.assertIn("artifact", res)
        self.assertEqual(res["artifact"]["manifold"], "alpha")
        self.assertTrue(len(res["artifact"]["copy_variants"]) > 0)

    def test_full_petzold_loop_beta_success(self):
        context = {
            "component_id": "dash_loader",
            "component_type": "hover",
            "locale": "en-US",
            "function_label": "Hover state",
            "context_tags": ["hover_ui"],
            "manifold_target": "beta"
        }
        res = self.agent.execute_petzold_loop(context)
        self.assertEqual(res["status"], "COMPLETE")
        self.assertIn("artifact", res)
        self.assertEqual(res["artifact"]["manifold"], "beta")
        self.assertIn("css_js", res["artifact"])

if __name__ == "__main__":
    unittest.main()
