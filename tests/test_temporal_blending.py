import unittest
from typing import Dict, List, Set, Optional

from src.conceptual_synthesis.temporal_blending_engine import (
    DiscreteState,
    CausalAction,
    SystemAssuranceAgent,
    Trace
)

class TestTemporalBlendingEngine(unittest.TestCase):
    def setUp(self):
        self.saa = SystemAssuranceAgent(cpi_threshold=0.95)

    def test_cpi_calculation_perfect_trace(self):
        s1 = DiscreteState(fluents={"f_cam": 1, "f_door_open": 0})
        a1 = CausalAction(
            name="open_door",
            preconditions={"f_cam": 1},
            effects={"f_door_open": 1}
        )
        s2 = DiscreteState(fluents={"f_cam": 1, "f_door_open": 1})

        trace = Trace(states=[s1, s2], actions=[a1])
        cpi = self.saa.calculate_cpi(trace)
        self.assertEqual(cpi, 1.0)
        self.assertTrue(self.saa.verify_trace(trace))

    def test_cpi_calculation_precondition_failure(self):
        s1 = DiscreteState(fluents={"f_cam": 0, "f_door_open": 0})
        a1 = CausalAction(
            name="open_door",
            preconditions={"f_cam": 1}, # Contradiction: f_cam is 0
            effects={"f_door_open": 1}
        )
        s2 = DiscreteState(fluents={"f_cam": 0, "f_door_open": 1})

        trace = Trace(states=[s1, s2], actions=[a1])
        cpi = self.saa.calculate_cpi(trace)
        self.assertEqual(cpi, 0.0)
        self.assertFalse(self.saa.verify_trace(trace))

    def test_cpi_calculation_effect_failure(self):
        s1 = DiscreteState(fluents={"f_cam": 1, "f_door_open": 0})
        a1 = CausalAction(
            name="open_door",
            preconditions={"f_cam": 1},
            effects={"f_door_open": 1}
        )
        # Contradiction: effect f_door_open: 1 was not applied
        s2 = DiscreteState(fluents={"f_cam": 1, "f_door_open": 0})

        trace = Trace(states=[s1, s2], actions=[a1])
        cpi = self.saa.calculate_cpi(trace)
        self.assertEqual(cpi, 0.0)
        self.assertFalse(self.saa.verify_trace(trace))

    def test_cpi_calculation_frame_operator_failure(self):
        s1 = DiscreteState(fluents={"f_cam": 1, "f_door_open": 0})
        a1 = CausalAction(
            name="open_door",
            preconditions={"f_cam": 1},
            effects={"f_door_open": 1}
        )
        # Contradiction: f_cam changed even though it was not in effects
        s2 = DiscreteState(fluents={"f_cam": 0, "f_door_open": 1})

        trace = Trace(states=[s1, s2], actions=[a1])
        cpi = self.saa.calculate_cpi(trace)
        self.assertEqual(cpi, 0.0)
        self.assertFalse(self.saa.verify_trace(trace))

    def test_cascading_contradiction_boundary(self):
        # Create a trace with length N=20 (19 transitions)
        states = []
        actions = []

        # Initial state
        states.append(DiscreteState(fluents={"f_cam": 1, "f_step": 0}))

        # Step 1: disable camera
        actions.append(CausalAction(
            name="disable_cam",
            preconditions={"f_cam": 1},
            effects={"f_cam": 0, "f_step": 1}
        ))
        states.append(DiscreteState(fluents={"f_cam": 0, "f_step": 1}))

        # Steps 2-18: valid actions
        for i in range(2, 19):
            actions.append(CausalAction(
                name=f"step_{i}",
                preconditions={"f_step": i-1},
                effects={"f_step": i}
            ))
            states.append(DiscreteState(fluents={"f_cam": 0, "f_step": i}))

        # Step 19: contradiction action requires camera to be 1, but frame operator says it is 0
        actions.append(CausalAction(
            name="require_cam",
            preconditions={"f_cam": 1}, # This will fail
            effects={"f_step": 19}
        ))
        states.append(DiscreteState(fluents={"f_cam": 0, "f_step": 19}))

        trace = Trace(states=states, actions=actions)

        # We have 19 transitions, 1 fails. Score = 18/19 = ~0.947
        cpi = self.saa.calculate_cpi(trace)
        self.assertLess(cpi, 0.95)
        self.assertFalse(self.saa.verify_trace(trace))

        # Epistemic escrow exception should be raised or logged
        with self.assertRaises(Exception) as context:
            self.saa.enforce(trace)

        self.assertTrue("Epistemic Escrow" in str(context.exception))

if __name__ == '__main__':
    unittest.main()
