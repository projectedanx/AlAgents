import unittest
import numpy as np
import os
import json
from src.conceptual_synthesis.vcp_agent import VerificationCoProcessor

class TestVerificationCoProcessor(unittest.TestCase):
    def setUp(self):
        self.scar_log_path = "test_vcp_scars.jsonl"
        self.vcp = VerificationCoProcessor(scar_log_path=self.scar_log_path)

        # Setup dummy vectors
        self.v_anc = np.array([1.0, 0.0, 0.0, 0.0])

    def tearDown(self):
        if os.path.exists(self.scar_log_path):
            os.remove(self.scar_log_path)

    def test_laminar_geodesic(self):
        # Create an h_t very close to v_anc (SDC will be close to 0)
        h_t = np.array([0.99, 0.01, 0.0, 0.0])
        kv_cache = []

        result = self.vcp.execute_guard_loop(
            h_t=h_t, kv_cache=kv_cache, v_anc=self.v_anc,
            cfdi=0.1, betti_0=0.9, betti_1=0
        )

        self.assertEqual(result["status"], "LAMINAR")
        self.assertLessEqual(result["sdc"], self.vcp.drift_threshold_xi)

    def test_surgical_repair(self):
        # Create an h_t far from v_anc to trigger SDC > 0.30
        h_t = np.array([0.5, 0.8, 0.0, 0.0]) # cos sim ~ 0.5, SDC ~ 0.5
        kv_cache = []

        result = self.vcp.execute_guard_loop(
            h_t=h_t, kv_cache=kv_cache, v_anc=self.v_anc,
            cfdi=0.3, betti_0=0.9, betti_1=0
        )

        self.assertEqual(result["status"], "SURGICAL_REPAIR")
        self.assertIn("state_mapping", result)

        state_mapping = result["state_mapping"]
        self.assertEqual(state_mapping["triggering_anomaly"]["metric"], "SDC")
        self.assertGreater(state_mapping["triggering_anomaly"]["value"], self.vcp.drift_threshold_xi)
        self.assertEqual(state_mapping["remediation_plan"]["intervention_type"], "differentiable_cache_augmentation")

    def test_constitutional_crisis_cfdi(self):
        h_t = np.array([0.5, 0.8, 0.0, 0.0]) # SDC > 0.30
        kv_cache = []

        # High CFDI
        result = self.vcp.execute_guard_loop(
            h_t=h_t, kv_cache=kv_cache, v_anc=self.v_anc,
            cfdi=0.8, betti_0=0.9, betti_1=0
        )

        self.assertEqual(result["status"], "EPISTEMIC_ESCROW")
        self.assertIn("CFDI", result["reason"])

        # Check if scar was logged
        self.assertTrue(os.path.exists(self.scar_log_path))
        with open(self.scar_log_path, 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 1)
            scar = json.loads(lines[0])
            self.assertEqual(scar["failure_mode"], "Constitutional Crisis - Logic Breach")

    def test_constitutional_crisis_betti1(self):
        h_t = np.array([0.5, 0.8, 0.0, 0.0]) # SDC > 0.30
        kv_cache = []

        # Betti_1 >= 1 (logical contradiction)
        result = self.vcp.execute_guard_loop(
            h_t=h_t, kv_cache=kv_cache, v_anc=self.v_anc,
            cfdi=0.3, betti_0=0.9, betti_1=1
        )

        self.assertEqual(result["status"], "EPISTEMIC_ESCROW")
        self.assertIn("betti_1", result["reason"])

        # Check if scar was logged
        self.assertTrue(os.path.exists(self.scar_log_path))
        with open(self.scar_log_path, 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 1)
            scar = json.loads(lines[0])
            self.assertEqual(scar["failure_mode"], "Constitutional Crisis - Logic Breach")

if __name__ == '__main__':
    unittest.main()
