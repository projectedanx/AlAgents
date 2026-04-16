# /// file: tests/test_kut_agent.py ///
import sys
from unittest.mock import MagicMock
sys.modules['nltk.tabdata'] = MagicMock()

import unittest
from src.conceptual_synthesis.kut_agent import KutAgent

class TestKutAgent(unittest.TestCase):
    def setUp(self):
        self.agent = KutAgent()
        self.creator_id = "test_creator_123"

    def test_initialization(self):
        self.assertEqual(self.agent.codename, "Kut")
        self.assertEqual(self.agent.build_version, "2.0.1-SOVEREIGN")
        self.assertTrue("Metric-first. Feelings second." in self.agent.persona_invariants[0])
        self.assertIn("DaVinci Resolve", self.agent.nle_vocabulary_map["Export -14 LUFS"])

    def test_ingest_scar_escalation(self):
        # First offense
        scar_id_1 = self.agent._ingest_scar(self.creator_id, "Dead_Air", "Gap", "Fix")
        self.assertEqual(self.agent.scar_ledger[-1]["recurrence_count"], 1)
        self.assertEqual(self.agent.scar_ledger[-1]["escalation_level"], "1_prescriptive")

        # Second offense
        scar_id_2 = self.agent._ingest_scar(self.creator_id, "Dead_Air", "Gap", "Fix")
        self.assertEqual(self.agent.scar_ledger[-1]["recurrence_count"], 2)
        self.assertEqual(self.agent.scar_ledger[-1]["escalation_level"], "2_scar_linked")

        # Third offense
        scar_id_3 = self.agent._ingest_scar(self.creator_id, "Dead_Air", "Gap", "Fix")
        self.assertEqual(self.agent.scar_ledger[-1]["recurrence_count"], 3)
        self.assertEqual(self.agent.scar_ledger[-1]["escalation_level"], "3_dominant_failure_mode")

    def test_phase_1_audio_skeleton(self):
        # Pass condition
        result_pass = self.agent.phase_1_audio_skeleton(self.creator_id, [0.1, 0.2], "curiosity_gap")
        self.assertEqual(result_pass["status"], "PASS")

        # Fail condition - Dead Air
        result_fail_gap = self.agent.phase_1_audio_skeleton(self.creator_id, [0.4], "curiosity_gap")
        self.assertEqual(result_fail_gap["status"], "FAIL")
        self.assertIn("scar_id", result_fail_gap)

        # Fail condition - Hook
        result_fail_hook = self.agent.phase_1_audio_skeleton(self.creator_id, [0.1], "identity_first")
        self.assertEqual(result_fail_hook["status"], "FAIL")
        self.assertIn("scar_id", result_fail_hook)

    def test_phase_2_visual_thermodynamics(self):
        # Pass condition
        result_pass = self.agent.phase_2_visual_thermodynamics(self.creator_id, 20, 60, "DEFAULT") # 20 CPM > 14
        self.assertEqual(result_pass["status"], "PASS")

        # Fail condition
        result_fail = self.agent.phase_2_visual_thermodynamics(self.creator_id, 10, 60, "Comedy/Entertainment") # 10 CPM < 18
        self.assertEqual(result_fail["status"], "FAIL")
        self.assertEqual(result_fail["floor"], 18)

    def test_phase_4_sonic_sculpting(self):
        # Pass condition
        result_pass = self.agent.phase_4_sonic_sculpting(self.creator_id, -14.0, -1.5)
        self.assertEqual(result_pass["status"], "PASS")

        # Fail condition - LUFS
        result_fail_lufs = self.agent.phase_4_sonic_sculpting(self.creator_id, -10.0, -1.5)
        self.assertEqual(result_fail_lufs["status"], "FAIL")

        # Fail condition - True Peak
        result_fail_peak = self.agent.phase_4_sonic_sculpting(self.creator_id, -14.0, 0.0)
        self.assertEqual(result_fail_peak["status"], "FAIL")

if __name__ == "__main__":
    unittest.main()
