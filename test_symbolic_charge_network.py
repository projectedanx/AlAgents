import unittest
import numpy as np
from symbolic_charge_network import NeuroSymbolicParticle, SymbolicChargeNetwork

class TestSymbolicChargeNetwork(unittest.TestCase):

    def setUp(self):
        self.scn = SymbolicChargeNetwork()
        self.p1 = NeuroSymbolicParticle(embedding=[1, 0], charge=1.0, activation_potential=1.0)
        self.p2 = NeuroSymbolicParticle(embedding=[0.9, 0.1], charge=-1.0, activation_potential=1.0)
        self.p3 = NeuroSymbolicParticle(embedding=[0, 1], charge=0.5, activation_potential=1.0)

    def test_particle_creation(self):
        self.assertTrue(np.array_equal(self.p1.embedding, [1, 0]))
        self.assertEqual(self.p1.charge, 1.0)
        self.assertEqual(self.p1.activation_potential, 1.0)
        self.assertEqual(self.p1.coherence, 1.0)

    def test_add_particle(self):
        self.scn.add_particle(self.p1)
        self.assertIn(self.p1, self.scn.particles)

    def test_cosine_similarity(self):
        similarity = self.scn._cosine_similarity(np.array([1, 0]), np.array([0.9, 0.1]))
        self.assertAlmostEqual(similarity, 0.99388, places=5)

        ortho_similarity = self.scn._cosine_similarity(self.p1.embedding, self.p3.embedding)
        self.assertAlmostEqual(ortho_similarity, 0.0, places=5)

    def test_fusion_potential(self):
        potential = self.scn._cosine_similarity(self.p1.embedding, self.p2.embedding)
        self.assertAlmostEqual(potential, 0.99388, places=5)

    def test_successful_fusion(self):
        fused_particle = self.scn.fuse(self.p1, self.p2, fusion_threshold=0.9)
        self.assertIsNotNone(fused_particle)
        self.assertTrue(np.allclose(fused_particle.embedding, [0.95, 0.05]))
        self.assertAlmostEqual(fused_particle.charge, 0.0)
        self.assertAlmostEqual(fused_particle.activation_potential, 1.0)
        # Check inhibition
        self.assertAlmostEqual(self.p1.activation_potential, 1.5)
        self.assertAlmostEqual(self.p2.activation_potential, 1.5)

    def test_unsuccessful_fusion(self):
        fused_particle = self.scn.fuse(self.p1, self.p3, fusion_threshold=0.5)
        self.assertIsNone(fused_particle)
         # Check that inhibition did not occur
        self.assertAlmostEqual(self.p1.activation_potential, 1.0)
        self.assertAlmostEqual(self.p3.activation_potential, 1.0)

    def test_inhibit(self):
        initial_potential = self.p1.activation_potential
        self.scn.inhibit(self.p1, inhibition_factor=2.0)
        self.assertEqual(self.p1.activation_potential, initial_potential * 2.0)

if __name__ == '__main__':
    unittest.main()
