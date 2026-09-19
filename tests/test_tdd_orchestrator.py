import unittest
from src.conceptual_synthesis.tdd_orchestrator import TDDOrchestrator, TDDState, TestArchitectAgent, ImplementerAgent

class TestTDDOrchestrator(unittest.TestCase):
    def test_successful_tdd_loop(self):
        orchestrator = TDDOrchestrator()
        final_state = orchestrator.execute_loop("Implement a fast sorting algorithm")

        self.assertEqual(final_state.phase, "DONE")
        self.assertIsNotNone(final_state.test_code)
        self.assertIsNotNone(final_state.application_code)
        self.assertTrue(final_state.iterations <= final_state.max_iterations)

    def test_sycophantic_mock_detection(self):
        orchestrator = TDDOrchestrator()

        # Override the mock behavior to simulate a test that passes initially
        def mock_execute_pass_initially(state):
            return {"exit_code": 0, "failures": []}

        orchestrator._execute_tests_in_sandbox = mock_execute_pass_initially

        final_state = orchestrator.execute_loop("Implement simple feature")

        # Test Architect wrote a test that passed without any implementation code
        self.assertEqual(final_state.phase, "ESCROW")
        self.assertIsNone(final_state.application_code)

    def test_doom_loop_prevention(self):
         orchestrator = TDDOrchestrator()

         # Override mock to always fail
         def mock_execute_always_fail(state):
             return {"exit_code": 1, "failures": [{"message": "Always fails"}]}

         orchestrator._execute_tests_in_sandbox = mock_execute_always_fail

         final_state = orchestrator.execute_loop("Impossible task")

         self.assertEqual(final_state.phase, "ESCROW")
         self.assertEqual(final_state.iterations, final_state.max_iterations)

if __name__ == '__main__':
    unittest.main()
