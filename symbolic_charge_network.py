import numpy as np

class NeuroSymbolicParticle:
    """
    Represents a single neuro-symbolic particle in the Symbolic Charge Network.
    """
    def __init__(self, embedding, charge=0.0, activation_potential=1.0, semantic_inertia=1.0):
        """
        Initializes a new NeuroSymbolicParticle.

        Args:
            embedding: The dense vector representation of the concept.
            charge: The scalar charge representing the conceptual mass.
            activation_potential: The activation potential representing the potential for fusion.
            semantic_inertia: The semantic inertia representing resistance to change.
        """
        self.embedding = np.array(embedding, dtype=float)
        self.charge = float(charge)
        self.activation_potential = float(activation_potential)
        self.semantic_inertia = float(semantic_inertia)
        self.coherence = np.linalg.norm(self.embedding)

    def __repr__(self):
        """
        Returns a string representation of the NeuroSymbolicParticle.

        Returns:
            A string containing the particle's embedding, charge, and activation potential.
        """
        return (f"NeuroSymbolicParticle(embedding={self.embedding}, charge={self.charge}, "
                f"activation_potential={self.activation_potential})")

class SymbolicChargeNetwork:
    """
    Manages a collection of NeuroSymbolicParticles and their interactions.
    """
    def __init__(self):
        """
        Initializes a new, empty SymbolicChargeNetwork.
        """
        self.particles = []

    def add_particle(self, particle):
        """
        Adds a NeuroSymbolicParticle to the network.

        Args:
            particle: The NeuroSymbolicParticle to add to the network.
        """
        self.particles.append(particle)

    @staticmethod
    def _cosine_similarity(vec1, vec2):
        """Calculates the cosine similarity between two vectors."""
        dot_product = np.dot(vec1, vec2)
        norm_product = np.linalg.norm(vec1) * np.linalg.norm(vec2)
        if norm_product == 0:
            return 0.0
        return dot_product / norm_product

    def fuse(self, particle1, particle2, fusion_threshold=0.5):
        """
        Fuses two particles if their fusion potential is above a threshold,
        creating a new emergent concept.

        Args:
            particle1 (NeuroSymbolicParticle): The first particle.
            particle2 (NeuroSymbolicParticle): The second particle.
            fusion_threshold (float, optional): The minimum potential required for fusion. Defaults to 0.5.

        Returns:
            NeuroSymbolicParticle | None: The fused particle if successful, otherwise None.
        """
        potential = self._cosine_similarity(particle1.embedding, particle2.embedding)
        if potential > fusion_threshold:
            # New embedding is the average of the two source embeddings
            new_embedding = (particle1.embedding + particle2.embedding) / 2
            # New charge is the sum of the source charges
            new_charge = particle1.charge + particle2.charge
            # New activation potential is the average
            new_activation_potential = (particle1.activation_potential + particle2.activation_potential) / 2
            # New semantic inertia is the sum
            new_inertia = particle1.semantic_inertia + particle2.semantic_inertia

            fused_particle = NeuroSymbolicParticle(
                embedding=new_embedding,
                charge=new_charge,
                activation_potential=new_activation_potential,
                semantic_inertia=new_inertia
            )

            # Inhibition: temporarily increase the activation potential of the source particles
            self.inhibit(particle1)
            self.inhibit(particle2)

            return fused_particle
        return None

    def inhibit(self, particle, inhibition_factor=1.5):
        """
        Temporarily increases the activation potential of a particle, making it
        less likely to be re-selected immediately (semantic refractoriness).

        Args:
            particle (NeuroSymbolicParticle): The particle to inhibit.
            inhibition_factor (float, optional): The factor by which to multiply the activation potential. Defaults to 1.5.
        """
        particle.activation_potential *= inhibition_factor
