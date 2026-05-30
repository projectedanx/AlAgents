import unittest
import os
import json
from unittest.mock import patch, mock_open
from src.conceptual_synthesis.vance_agent import VanceAgent

class TestVanceAgent(unittest.TestCase):
    def setUp(self):
        self.agent = VanceAgent()
        # Clean up any scar log created during tests
        if os.path.exists(self.agent.scar_log_path):
            os.remove(self.agent.scar_log_path)

    def tearDown(self):
        if os.path.exists(self.agent.scar_log_path):
            os.remove(self.agent.scar_log_path)

    def test_initialization(self):
        self.assertEqual(self.agent.agent_name, "VANCE")
        self.assertEqual(self.agent.color_designation, "#4B0082")
        self.assertIn("Language Server Protocol", self.agent.specialty)

    def test_observe_missing_version_triggers_escrow(self):
        context = {
            "method": "textDocument/didChange",
            "params": {
                "textDocument": {
                    "uri": "file:///src/app.py"
                    # missing version
                }
            }
        }
        result = self.agent.execute_semantic_cartography_loop(context)
        self.assertEqual(result.get("status"), "HALTED")
        self.assertEqual(result.get("state"), "EPISTEMIC_ESCROW")
        self.assertIn("VersionedTextDocumentIdentifier requires 'version", result.get("jur", ""))

    def test_cfdi_violation_returns_ambiguity(self):
        context = {
            "method": "textDocument/definition",
            "id": 101,
            "cfdi": 0.2, # greater than 0.15 threshold
            "candidates": ["file:///a.py", "file:///b.py"]
        }
        result = self.agent.execute_semantic_cartography_loop(context)
        self.assertIn("jsonrpc", result)
        self.assertEqual(result["jsonrpc"], "2.0")
        self.assertIsNone(result.get("result"))
        self.assertIn("_vance_meta", result)
        self.assertTrue(result["_vance_meta"]["cfdi_flag"])
        self.assertEqual(result["_vance_meta"]["candidates"], ["file:///a.py", "file:///b.py"])

    def test_betti_cycle_detection(self):
        context = {
            "method": "betti_cycle_check",
            "dependencies": ["A", "B", "A"] # Cycle!
        }
        result = self.agent.execute_semantic_cartography_loop(context)
        self.assertIn("method", result)
        self.assertEqual(result["method"], "textDocument/publishDiagnostics")
        self.assertEqual(result["params"]["diagnostics"][0]["code"], "BETTI1-CYCLE")

    def test_successful_payload_resolution(self):
        context = {
            "method": "textDocument/hover",
            "id": 200,
            "cfdi": 0.05,
            "expected_result": {"contents": "def my_func() -> bool:"}
        }
        result = self.agent.execute_semantic_cartography_loop(context)
        self.assertEqual(result["jsonrpc"], "2.0")
        self.assertEqual(result["id"], 200)
        self.assertEqual(result["result"], {"contents": "def my_func() -> bool:"})
        self.assertNotIn("_vance_meta", result)


    def test_compute_cfdi_check_missing_node(self):
        context = {
            "method": "textDocument/definition",
            "id": 300,
            "cfdi": 0.05,
            "expected_result": {"uri": "file:///src/main.py"},
            "simulate_missing_node": True
        }
        result = self.agent.execute_semantic_cartography_loop(context)
        self.assertIn("_vance_meta", result)
        self.assertTrue(result["_vance_meta"]["cfdi_flag"])
        self.assertEqual(result["_vance_meta"]["reason"], "No AST node exists at proposed location")

    def test_compute_cfdi_check_symbol_mismatch(self):
        context = {
            "method": "textDocument/definition",
            "id": 301,
            "cfdi": 0.05,
            "expected_result": {"uri": "file:///src/main.py"},
            "expected_symbol": "MyClass",
            "found_symbol": "OtherClass"
        }
        result = self.agent.execute_semantic_cartography_loop(context)
        self.assertIn("_vance_meta", result)
        self.assertTrue(result["_vance_meta"]["cfdi_flag"])
        self.assertEqual(result["_vance_meta"]["reason"], "Symbol mismatch: expected MyClass, found OtherClass")

    def test_dccd_guard_invalid_jsonrpc(self):
        # We simulate this by monkey-patching the act phase since it constructs the base payload
        payload = {"jsonrpc": "1.0", "id": 1, "result": {}}
        is_valid, reason = self.agent._dccd_guard(payload, "response")
        self.assertFalse(is_valid)
        self.assertIn("jsonrpc must be '2.0'", reason)

    def test_dccd_guard_missing_id_and_method(self):
        payload = {"jsonrpc": "2.0", "result": {}}
        is_valid, reason = self.agent._dccd_guard(payload, "response")
        self.assertFalse(is_valid)
        self.assertIn("Must include 'id'", reason)

    def test_dccd_guard_cfdi_violation_range(self):
        context = {
            "method": "textDocument/definition",
            "id": 302,
            "cfdi": 0.05,
            "expected_result": {"uri": "file:///src/main.py", "range": {}},
            "_simulate_cfdi_violation": True
        }
        result = self.agent.execute_semantic_cartography_loop(context)
        self.assertEqual(result.get("status"), "HALTED")
        self.assertEqual(result.get("state"), "EPISTEMIC_ESCROW")
        self.assertIn("CFDI_VIOLATION: Range not found in AST", result.get("jur", ""))

if __name__ == '__main__':
    unittest.main()
