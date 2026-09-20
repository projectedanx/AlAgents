import unittest
import torch
import torch.nn.functional as F
from src.conceptual_synthesis.action_alignment_loss import ActionAlignmentLoss

class TestActionAlignmentLoss(unittest.TestCase):
    def setUp(self):
        # Rock, Paper, Scissors payoff matrix
        # R=0, P=1, S=2
        self.payoff_matrix = torch.tensor([
            [ 0.0, -1.0,  1.0],
            [ 1.0,  0.0, -1.0],
            [-1.0,  1.0,  0.0]
        ])

    def test_nash_trap_hard(self):
        """Test Action Alignment Loss with a hard Best-Response (use_smooth=False)."""
        loss_fn = ActionAlignmentLoss(payoff_matrix=self.payoff_matrix, use_smooth=False)

        # Predicted opponent plays Rock with 100% confidence
        # p_hat = [1, 0, 0] -> logits can be [10.0, -10.0, -10.0]
        predicted_opponent_logits = torch.tensor([[10.0, -10.0, -10.0]])

        # Agent plays Nash equilibrium [1/3, 1/3, 1/3] -> logits [0.0, 0.0, 0.0]
        agent_logits_nash = torch.tensor([[0.0, 0.0, 0.0]])
        loss_nash = loss_fn(agent_logits_nash, predicted_opponent_logits)

        # As per the proof, L_align(p_nash, p_hat) = 1.0
        self.assertAlmostEqual(loss_nash.item(), 1.0, places=4)

        # Agent plays optimal Best Response (Paper) -> [0, 1, 0] -> logits [-10.0, 10.0, -10.0]
        agent_logits_optimal = torch.tensor([[-10.0, 10.0, -10.0]])
        loss_optimal = loss_fn(agent_logits_optimal, predicted_opponent_logits)

        # L_align(p_optimal, p_hat) approx 0.0
        self.assertAlmostEqual(loss_optimal.item(), 0.0, places=4)

    def test_smooth_approximation(self):
        """Test Action Alignment Loss with smooth Boltzmann approximation (use_smooth=True)."""
        loss_fn = ActionAlignmentLoss(payoff_matrix=self.payoff_matrix, use_smooth=True, temperature=0.1)

        predicted_opponent_logits = torch.tensor([[10.0, -10.0, -10.0]])
        agent_logits_nash = torch.tensor([[0.0, 0.0, 0.0]])

        loss_nash = loss_fn(agent_logits_nash, predicted_opponent_logits)

        # With smooth approximation, it should be close to 1.0 but slightly different due to temperature
        # Actually: expected action utilities = [0, 1, -1]
        # v_optimal = 0.1 * logsumexp([0, 10, -10]) = 0.1 * log(exp(0) + exp(10) + exp(-10))
        # exp(10) dominates, so logsumexp ~= 10.000045, v_optimal ~= 1.0000045
        # expected_policy_utility = 1/3 * 0 + 1/3 * 1 + 1/3 * (-1) = 0
        # regret = v_optimal - 0 ~= 1.0000045
        self.assertAlmostEqual(loss_nash.item(), 1.0, places=3)

if __name__ == '__main__':
    unittest.main()
