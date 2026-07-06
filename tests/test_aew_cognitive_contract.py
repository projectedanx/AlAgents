import unittest
from src.conceptual_synthesis.aew_cognitive_contract import AEWCognitiveContractSimulator

class TestAEWCognitiveContractSimulator(unittest.TestCase):
    def setUp(self):
        self.simulator = AEWCognitiveContractSimulator()

    def test_run_simulation_validation(self):
        # Using stress_pi=0.5 and architectural_bias=0.8
        # Should result in VALIDATED with the correct beta bounds
        result = self.simulator.run_simulation(stress_pi=0.5, architectural_bias=0.8)
        self.assertEqual(result.get('status'), 'VALIDATED')
        self.assertTrue(result.get('novelty') > self.simulator.agent.beta_1)

        relational_vector = abs(result.get('z_prime') - self.simulator.agent.z_0_star)
        self.assertTrue(relational_vector <= (1 - self.simulator.agent.beta_0))

    def test_run_simulation_rejection(self):
        # Force a large stress that breaks the beta_0 conservation (z_prime drops too low)
        # 1 - (10.0 * 0.1) = 0.0. Relational vector = 1.0 > 0.05
        result = self.simulator.run_simulation(stress_pi=10.0, architectural_bias=0.8)
        self.assertEqual(result.get('status'), 'REJECTED_BY_EEA')

if __name__ == '__main__':
    unittest.main()
