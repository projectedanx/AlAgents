# /// file: tests/test_tactile_dialectician_agent.py ///
import unittest
from src.conceptual_synthesis.tactile_dialectician_agent import TactileDialecticianAgent

class TestTactileDialecticianAgent(unittest.TestCase):

    def setUp(self):
        self.agent = TactileDialecticianAgent()

    def test_hickam_ooda_loop_paraconsistent_tension(self):
        context = {
            "intent": "Optimize for speed while enforcing rigorous, slow manual verification.",
            "drivers": [
                "User demands sub-second execution (speed).",
                "Compliance mandates full human-in-the-loop audit trails (slow)."
            ],
            "lens": "Corporate Efficiency vs. Regulatory Paranoia"
        }

        result = self.agent.execute_hickam_ooda_loop(context)

        self.assertEqual(result["status"], "COMPLETE")

        # Verify Hickam Orientation block is present
        self.assertIn("Hickam_Orientation", result)
        orientation = result["Hickam_Orientation"]
        self.assertIn("[COMORBID: Speed]", orientation["comorbidity_map"])
        self.assertIn("[COMORBID: Audit]", orientation["comorbidity_map"])
        self.assertEqual(orientation["cognitive_lens"], "[LENS: Corporate Efficiency vs. Regulatory Paranoia]")

        # Verify Pluriversal Knowledge Capsule constraints
        capsule = result["Pluriversal_Knowledge_Capsule"]

        # Must contain markers
        self.assertTrue(capsule["epistemic_markers"]["uncertainty_present"])
        self.assertTrue(capsule["epistemic_markers"]["contradiction_present"])
        self.assertTrue(capsule["epistemic_markers"]["golden_scar_present"])

        # Must verify Golden Scar weights
        golden_scar = capsule["golden_scar_weights"]
        self.assertAlmostEqual(golden_scar["dominant_frame_weight"], 1.618, places=3)
        self.assertAlmostEqual(golden_scar["subordinate_frame_weight"], 1.000, places=3)

        # Verify Checklist
        checklist = result["Verification_Checklist"]
        self.assertTrue(checklist["aesthetic_tension_novel"])
        self.assertTrue(checklist["intent_divergence_twinned"])
        self.assertTrue(checklist["epistemic_escrow_secured"])
        self.assertTrue(checklist["symbolic_scar_integrity_maintained"])



    def test_gds_computation_and_logging(self):
        context = {
            "intent": "Simple short text",
            "query_domain": "A",
            "drivers": ["speed"],
            "lens": "Test Lens"
        }

        # Test low GDS (< 0.5)
        context["query_domain"] = "AAAA"

        result = self.agent.execute_hickam_ooda_loop(context)

        self.assertEqual(result["status"], "COMPLETE")
        self.assertIn("Contrastive_Delta", result)
        self.assertIn("Martensite_Metrics", result)

        contrastive_delta = result["Contrastive_Delta"]
        self.assertTrue(contrastive_delta["hitl_required"])
        self.assertLess(contrastive_delta["gds_score"], 0.5)

        # Verify it logged to SymbolicScar.jsonl
        import os
        self.assertTrue(os.path.exists("SymbolicScar.jsonl"))
        with open("SymbolicScar.jsonl", "r") as f:
            lines = f.readlines()
            last_line = lines[-1]
            self.assertIn("ontological_correction", last_line)
            self.assertIn("Test Lens", last_line)

        # Cleanup
        if os.path.exists("SymbolicScar.jsonl"):
            os.remove("SymbolicScar.jsonl")

if __name__ == '__main__':


    unittest.main()
