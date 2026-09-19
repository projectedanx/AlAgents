import unittest
import numpy as np
import time
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from conceptual_synthesis.staged_advantage_estimation import TreeOPOGroup
from conceptual_synthesis.adaptive_sae import AdaptiveSAEHarness
from conceptual_synthesis.admm_projector import ADMMProjector
from conceptual_synthesis.ewar_diagnostic import EWARDiagnosticHarness

class TestStagedAdvantageEstimation(unittest.TestCase):

    def test_core_sae_heuristic(self):
        group = TreeOPOGroup("group1")
        group.add_node("root", None)
        group.add_node("A", "root")

        group.register_sample("root", 0.0)
        group.register_sample("A", 1.0)

        adv = group.compute_heuristic_advantages(alpha=0.5)
        self.assertEqual(len(adv), 2)
        self.assertTrue(np.isclose(np.sum(adv), 0.0, atol=1e-5))

    def test_core_sae_qp(self):
        group = TreeOPOGroup("group2")
        group.add_node("root", None)
        group.add_node("A", "root")
        group.add_node("B", "root")

        # B is sibling of A.
        # A succeeds, B fails.
        group.register_sample("root", 0.0)
        group.register_sample("A", 1.0)
        group.register_sample("B", 0.0)

        adv = group.compute_sae_qp_advantages(margin=0.01)
        self.assertTrue(np.isclose(np.sum(adv), 0.0, atol=1e-5))

        # Constraint C_pair: a_root + 0.01 <= a_A
        self.assertLessEqual(adv[0] + 0.009, adv[1])

    def test_adaptive_harness(self):
        group = TreeOPOGroup("group3")
        group.add_node("root", None)
        group.add_node("A", "root")
        group.register_sample("root", 0.0)
        group.register_sample("A", 1.0)

        student_logprobs = np.array([-1.0, -1.0])
        teacher_logprobs = np.array([-1.0, -1.0])

        harness = AdaptiveSAEHarness(tau_equilibrium=0.12)
        psi = harness.compute_spectral_information_discrepancy(group, student_logprobs, teacher_logprobs)
        self.assertLess(psi, 0.12)

        teacher_logprobs_diff = np.array([-3.0, -3.0])
        psi_high = harness.compute_spectral_information_discrepancy(group, student_logprobs, teacher_logprobs_diff)
        self.assertGreater(psi_high, 0.12)

        adv = harness.compute_advantages(group, student_logprobs, teacher_logprobs_diff)
        self.assertTrue(np.isclose(np.sum(adv), 0.0, atol=1e-5))

    def test_admm_projector(self):
        group = TreeOPOGroup("group4")
        group.add_node("root", None)
        group.add_node("A", "root")
        group.register_sample("root", 0.0)
        group.register_sample("A", 1.0)

        projector = ADMMProjector(max_iter=50)

        start_time = time.time()
        projector.compute_advantages_async(group)
        time.sleep(0.05)
        duration = time.time() - start_time

        adv = projector.get_latest_advantages()
        self.assertIsNotNone(adv)
        self.assertTrue(np.isclose(np.sum(adv), 0.0, atol=1e-5))

    def test_ewar_diagnostic(self):
        harness = EWARDiagnosticHarness(chi_threshold=0.1)
        group = TreeOPOGroup("group5")

        advantages = np.array([0.001, -0.001, 0.0005, -0.0005])
        parent_logprobs = np.array([-0.1, -1.0, -2.0, -0.01])

        chi = 0.05 # below threshold -> saponification detected
        ewar_adv = harness.apply_ewar_hook(group, advantages, parent_logprobs, chi)

        self.assertTrue(np.isclose(np.mean(ewar_adv), 0.0, atol=1e-5))
        self.assertTrue(np.isclose(np.std(ewar_adv), 1.0, atol=1e-5))

        # Test non-saponification
        chi_high = 0.5
        std_adv = harness.apply_ewar_hook(group, advantages, parent_logprobs, chi_high)
        self.assertTrue(np.array_equal(advantages, std_adv))

if __name__ == '__main__':
    unittest.main()
