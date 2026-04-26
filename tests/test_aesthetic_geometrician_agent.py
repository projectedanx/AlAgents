# /// file: tests/test_aesthetic_geometrician_agent.py ///
import sys
from unittest.mock import MagicMock
# Mock out nltk so it doesn't fail on missing tabdata
sys.modules['nltk.tabdata'] = MagicMock()

import unittest
from src.conceptual_synthesis.aesthetic_geometrician_agent import AestheticGeometricianAgent

class TestAestheticGeometricianAgent(unittest.TestCase):
    def setUp(self):
        self.agent = AestheticGeometricianAgent()

    def test_observe_and_orient(self):
        context = {"metric": "conversion"}
        result = self.agent._observe_and_orient(context)
        self.assertEqual(result["status"], "OBSERVE_COMPLETE")
        self.assertIn("scribble", result)

    def test_decide(self):
        scribble = {"status": "OBSERVE_COMPLETE"}
        context = {}
        result = self.agent._decide(scribble, context)
        self.assertEqual(result["status"], "DECIDE_COMPLETE")
        self.assertEqual(result["tokens"]["grid_base"], 8)
        self.assertEqual(result["tokens"]["type_ratio"], 1.250)

    def test_act(self):
        tokens = {"grid_base": 8, "type_ratio": 1.250}
        context = {}
        result = self.agent._act(tokens, context)
        self.assertEqual(result["status"], "ACT_COMPLETE")
        self.assertIn("draft", result)

    def test_critique(self):
        draft = {"draft": "Component structure"}
        context = {}
        result = self.agent._critique(draft, context)
        self.assertEqual(result["status"], "COMPLETE")
        self.assertIn("final_artifact", result)

    def test_execute_petzold_loop(self):
        context = {"metric": "conversion"}
        result = self.agent.execute_petzold_loop(context)
        self.assertEqual(result["status"], "COMPLETE")
        self.assertIn("final_artifact", result)

if __name__ == "__main__":
    unittest.main()
