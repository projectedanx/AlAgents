import unittest
import sys
from unittest.mock import patch, MagicMock

# Mock NLTK entirely before anything else
sys.modules['nltk'] = MagicMock()
sys.modules['nltk.corpus'] = MagicMock()
sys.modules['nltk.corpus.util'] = MagicMock()
sys.modules['nltk.stem'] = MagicMock()
sys.modules['nltk.tokenize'] = MagicMock()

class TestViperAgent(unittest.TestCase):
    @patch('src.conceptual_synthesis.base_agent.nltk', MagicMock())
    @patch('src.conceptual_synthesis.base_agent.stopwords', MagicMock())
    @patch('src.conceptual_synthesis.base_agent.PorterStemmer', MagicMock())
    @patch('src.conceptual_synthesis.base_agent.word_tokenize', MagicMock())
    def test_viper_execution(self):
        from src.conceptual_synthesis.viper_agent import ViperAgent

        agent = ViperAgent()

        # Override the _calculate_ads for testing
        def mock_ads(text):
            if "beautiful" in text:
                return 0.5
            return 0.1
        agent._calculate_ads = mock_ads

        context = {
            "hardware": {
                "lens": "Cooke S4/i 40mm",
                "aperture": "T2.8",
                "film_stock": "CineStill 800T",
                "lighting": "Practical tungsten sconce lamps, 2700K",
                "sensor": "Super35 spherical"
            },
            "rcc8_bindings": [
                {
                    "subject_a": "Espresso_Cup",
                    "subject_b": "Marble_Table_Surface",
                    "rcc8": "Externally_Connected",
                    "contact_normal": "horizontal_plane",
                    "parallax_z": "0cm"
                }
            ],
            "base_syntax": "Medium close-up, aged female subject. Parisian brasserie interior.",
            "negative_space": "No overhead lighting."
        }

        prompt = "I want a nostalgic, beautiful portrait of an old woman in a Parisian cafe, very cinematic and emotional, masterpiece quality, 8k"

        result = agent.execute_petzold_loop(prompt, context)

        self.assertEqual(result["status"], "COMPLETE")
        self.assertIn("OSM_ID", result["osm"])
        self.assertEqual(result["osm"]["ADS_Final"], 0.1)
        self.assertIn("diagnostic", result)
        self.assertIn("beautiful", result["diagnostic"])
        self.assertIn("cinematic", result["diagnostic"])

if __name__ == '__main__':
    unittest.main()
