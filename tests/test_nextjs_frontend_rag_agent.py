# /// file: tests/test_nextjs_frontend_rag_agent.py ///
import unittest

from src.conceptual_synthesis.nextjs_frontend_rag_agent import NextjsFrontendRagAgent

class TestNextjsFrontendRagAgent(unittest.TestCase):
    def setUp(self):
        self.agent = NextjsFrontendRagAgent()

    def test_successful_rag_pipeline(self):
        context = {
            "query": "How do I start?",
            "user_id": "user123",
            "document_collection": "knowledge_base",
            "top_k": 5,
            "min_relevance_score": 0.5
        }
        result = self.agent.execute_rag_pipeline(context)

        self.assertTrue(result["success"])
        self.assertIsNotNone(result["answer"])
        self.assertEqual(result["confidence"], 1.0)
        self.assertTrue(len(result["citations"]) > 0)
        self.assertIn("retrieval_stats", result)

    def test_insufficient_context(self):
        context = {
            "query": "sim_empty_context: something completely unrelated",
            "user_id": "user123"
        }
        result = self.agent.execute_rag_pipeline(context)

        self.assertTrue(result["success"])
        self.assertIsNone(result["answer"])
        self.assertEqual(result["error"], "insufficient_context")
        self.assertIn("Try rephrasing", result["suggestion"])

    def test_unauthorized_access(self):
        context = {
            "query": "How do I start?",
            "user_id": ""  # Missing user ID
        }
        result = self.agent.execute_rag_pipeline(context)

        self.assertFalse(result["success"])
        self.assertEqual(result["error"], "UnauthorizedAccess")
        self.assertIsNone(result["answer"])

    def test_vector_db_unavailable(self):
        context = {
            "query": "sim_db_fail: trigger a db error",
            "user_id": "user123"
        }
        result = self.agent.execute_rag_pipeline(context)

        self.assertFalse(result["success"])
        self.assertEqual(result["error"], "VectorDBUnavailable")
        self.assertIsNone(result["answer"])

    def test_hallucination_detection(self):
        # We simulate hallucination in synthesize_answer if query contains a certain string,
        # but our mock is hardcoded to return a specific string.
        # Instead, we test the citation generator directly for hallucination mock logic.
        result = self.agent.generate_citations("sim_hallucination: an invented fact", [])
        self.assertTrue(len(result["unmapped_claims"]) > 0)

        # Test full pipeline confidence drop
        # The agent mock currently doesn't propagate the query string into the answer for the hallucination check.
        # Let's override synthesize_answer locally to test this path.
        original_synth = self.agent.synthesize_answer
        self.agent.synthesize_answer = lambda q, d: {"answer": "sim_hallucination", "generation_time_ms": 10}

        context = {"query": "test", "user_id": "user1"}
        res = self.agent.execute_rag_pipeline(context)
        self.assertEqual(res["confidence"], 0.5)  # Dropped due to unmapped claims

        self.agent.synthesize_answer = original_synth

if __name__ == "__main__":
    unittest.main()
