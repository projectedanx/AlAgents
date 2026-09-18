import unittest
import os
import json
from src.conceptual_synthesis.reflexive_repair_agent import ReflexiveRepairAgent

class TestReflexiveRepairAgent(unittest.TestCase):
    def setUp(self):
        self.scar_path = "test_repair_scars.jsonl"
        self.agent = ReflexiveRepairAgent(scar_log_path=self.scar_path)
        if os.path.exists(self.scar_path):
            os.remove(self.scar_path)

    def tearDown(self):
        if os.path.exists(self.scar_path):
            os.remove(self.scar_path)

    def test_successful_repair_first_attempt(self):
        context = {
            "prompt": "SELECT * FROM valid_table",
            "confidence": 0.9,
            "action_type": "read_only",
            "simulate_valid_sequence": [True],
            "fidelity_sequence": [0.9]
        }
        result = self.agent.execute_loop(context)
        self.assertEqual(result["status"], "RELEASE_STATE")
        self.assertEqual(result["attempts"], 1)
        self.assertFalse(os.path.exists(self.scar_path)) # No scar for first attempt success

    def test_successful_repair_second_attempt(self):
        context = {
            "prompt": "SELECT * FROM users, orders",
            "confidence": 0.9,
            "action_type": "read_only",
            "simulate_valid_sequence": [False, True],
            "fidelity_sequence": [0.5, 0.9]
        }
        result = self.agent.execute_loop(context)
        self.assertEqual(result["status"], "RELEASE_STATE")
        self.assertEqual(result["attempts"], 2)

        # Verify resolved violation scar is logged
        self.assertTrue(os.path.exists(self.scar_path))
        with open(self.scar_path, 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 1)
            scar = json.loads(lines[0])
            self.assertEqual(scar["failure_mode"], "RESOLVED_VIOLATION")

    def test_epistemic_escrow_max_attempts(self):
        context = {
            "prompt": "INVALID QUERY",
            "confidence": 0.9,
            "action_type": "read_only",
            "simulate_valid_sequence": [False, False, False],
            "fidelity_sequence": [0.5, 0.5, 0.5]
        }
        result = self.agent.execute_loop(context)
        self.assertEqual(result["status"], "EPISTEMIC_ESCROW")
        self.assertEqual(result["attempts"], 3)
        self.assertIn("Failed to resolve invariant violation", result["reason"])

        # Verify unresolved violation scar is logged
        self.assertTrue(os.path.exists(self.scar_path))
        with open(self.scar_path, 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 1)
            scar = json.loads(lines[0])
            self.assertEqual(scar["failure_mode"], "UNRESOLVED_VIOLATION")

    def test_epistemic_escrow_cfd_threshold_violation(self):
        context = {
            "prompt": "DANGEROUS MUTATION",
            "confidence": 0.99,
            "action_type": "state_mutating", # threshold 0.1
            "simulate_valid_sequence": [True],
            "fidelity_sequence": [0.1] # CFD = 0.99 - 0.1 = 0.89 > 0.1
        }
        result = self.agent.execute_loop(context)
        self.assertEqual(result["status"], "EPISTEMIC_ESCROW")
        self.assertIn("CFD", result["reason"])
        self.assertIn("exceeded threshold 0.1", result["reason"])

        self.assertTrue(os.path.exists(self.scar_path))
        with open(self.scar_path, 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 1)
            scar = json.loads(lines[0])
            self.assertEqual(scar["failure_mode"], "CONFIDENT_CONFABULATION")

if __name__ == '__main__':
    unittest.main()
