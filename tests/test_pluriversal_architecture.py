# /// file: tests/test_pluriversal_architecture.py ///
import unittest
import numpy as np
from src.conceptual_synthesis.pluriversal_architecture import (
    AnionicFilter, RCC8Relation, HolonNode, MereologyRoute,
    SymbolicScar, hegelian_dialectical_synthesis, TopologicalMonitor
)

class TestPluriversalArchitecture(unittest.TestCase):

    def test_anionic_filter(self):
        vocab_size = 5
        forbidden = {1, 3}
        filter = AnionicFilter(vocab_size, forbidden)
        logits = np.array([1.0, 1.0, 1.0, 1.0, 1.0])
        masked = filter.apply_mask(logits)
        self.assertEqual(masked[0], 1.0)
        self.assertEqual(masked[1], -np.inf)
        self.assertEqual(masked[2], 1.0)
        self.assertEqual(masked[3], -np.inf)
        self.assertEqual(masked[4], 1.0)

    def test_mereology_route(self):
        route = MereologyRoute()
        whole = HolonNode("DB_Cluster", {"sql", "nosql"})
        part1 = HolonNode("SQLite_Module", {"sql"})
        part2 = HolonNode("Auth_Service", {"auth"})

        route.register_relation(whole, part1, RCC8Relation.NTPP)
        route.register_relation(whole, part2, RCC8Relation.DC)

        # SQL packet should route to SQLite, not Auth
        destinations = route.route_packet("sql", "DB_Cluster")
        self.assertIn("SQLite_Module", destinations)
        self.assertNotIn("Auth_Service", destinations)

    def test_symbolic_scar(self):
        scar = SymbolicScar("Auth", "TokenLeak", dimensions=10)
        traj = scar.hypervector # Exact match
        deflection = scar.calculate_deflection(traj)
        self.assertAlmostEqual(deflection, 1.0, places=5)

        traj_opp = -scar.hypervector
        deflection_opp = scar.calculate_deflection(traj_opp)
        self.assertAlmostEqual(deflection_opp, -1.0, places=5)

    def test_hegelian_synthesis(self):
        thesis = np.array([0.8, 0.2])
        antithesis = np.array([0.1, 0.9])
        synth = hegelian_dialectical_synthesis(thesis, antithesis, temperature=0.5)
        self.assertTrue(np.allclose(synth, [0.9, 1.1]))

    def test_topological_monitor(self):
        # Disconnected graph: 2 components, 0 loops
        adj_disconnected = np.array([
            [0, 1, 0],
            [1, 0, 0],
            [0, 0, 0]
        ])
        b0, b1 = TopologicalMonitor.compute_betti_numbers(adj_disconnected)
        self.assertEqual(b0, 2)
        self.assertEqual(b1, 0)

        # Cyclic graph: 1 component, 1 loop
        adj_cyclic = np.array([
            [0, 1, 1],
            [1, 0, 1],
            [1, 1, 0]
        ])
        b0, b1 = TopologicalMonitor.compute_betti_numbers(adj_cyclic)
        self.assertEqual(b0, 1)
        self.assertEqual(b1, 1)

if __name__ == '__main__':
    unittest.main()
