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

if __name__ == '__main__':
    unittest.main()
