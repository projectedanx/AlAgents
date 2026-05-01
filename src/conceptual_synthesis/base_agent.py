# /// file: src/conceptual_synthesis/base_agent.py ///
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import string
import numpy as np

from dataclasses import dataclass

@dataclass
class SynthesisPayload:
    text: str
    principal: float
    rate: float
    times_compounded: int
    years: int
    nodes: int
    charges: list[float]
    interactions: np.ndarray
    image: np.ndarray
    width: int
    height: int
    rule: int


class BaseAgent:
    """A base agent that integrates multiple functionalities to produce a complex, layered result."""

    def __init__(self):
        """
        Initializes the BaseAgent, ensuring required NLTK data is downloaded.
        """
        try:
            stopwords.words("english")
        except LookupError:
            nltk.download("stopwords", quiet=True)
        try:
            nltk.data.find("tokenizers/punkt")
        except LookupError:
            nltk.download("punkt", quiet=True)
        try:
            nltk.data.find("tokenizers/punkt_tab")
        except LookupError:
            nltk.download("punkt_tab", quiet=True)

        # Setup translation table, stopwords, and stemmer
        self.table = str.maketrans("", "", string.punctuation)
        self.stop_words = set(stopwords.words("english"))
        self.porter = PorterStemmer()

    def _deterministic_context_engineering(self, text: str) -> list[str]:
        """
        Processes text by applying deterministic rules to engineer a specific context.

        This function tokenizes the input text, removes punctuation and stopwords,
        and applies stemming to the remaining words.

        Args:
            text: The input string to process.

        Returns:
            A list of processed tokens.
        """
        # Tokenize the text
        tokens = word_tokenize(text)

        # Consolidate lowering, punctuation removal, filtering, and stemming
        # into a single list comprehension to avoid intermediate lists.
        # Use a generator expression for the inner loop to save memory.
        stemmed = [
            self.porter.stem(w_clean)
            for w_clean in (w.lower().translate(self.table) for w in tokens)
            if w_clean.isalpha() and w_clean not in self.stop_words
        ]

        return stemmed

    def _neoclassical_compounding(
        self, principal: float, rate: float, times_compounded: int, years: int
    ) -> float:
        """
        Calculates the future value of an investment with compound interest.

        Args:
            principal: The initial principal amount.
            rate: The annual interest rate (in decimal form).
            times_compounded: The number of times that interest is compounded per year.
            years: The number of years the money is invested for.

        Returns:
            The future value of the investment.
        """
        return principal * (1 + rate / times_compounded) ** (times_compounded * years)

    def _symbolic_charge_network(
        self, nodes: int, charges: list[float], interactions: np.ndarray
    ) -> np.ndarray:
        """
        Simulates a network of nodes with symbolic "charges" and their interactions.

        Args:
            nodes: The number of nodes in the network.
            charges: A list of charges for each node.
            interactions: An adjacency matrix representing the interactions between nodes.

        Returns:
            A numpy array representing the final state of the network.
        """
        if len(charges) != nodes or interactions.shape != (nodes, nodes):
            raise ValueError("Input dimensions do not match the number of nodes.")

        return np.dot(interactions, charges)

    def _algorithmic_photography(self, image: np.ndarray) -> np.ndarray:
        """
        Applies a sepia filter to an image represented as a NumPy array.

        Args:
            image: A NumPy array representing the image (in RGB format).

        Returns:
            A NumPy array representing the image with the sepia filter applied.
        """
        sepia_filter = np.array(
            [[0.393, 0.769, 0.189], [0.349, 0.686, 0.168], [0.272, 0.534, 0.131]]
        )

        # Apply the sepia filter
        sepia_image = np.dot(image, sepia_filter.T)

        # Clip the values to be in the valid range [0, 255]
        return np.clip(sepia_image, 0, 255)

    def _weaving_algorithm(self, width: int, height: int, rule: int) -> np.ndarray:
        """
        Generates a textile-like pattern based on a computational rule.

        Args:
            width: The width of the pattern.
            height: The height of the pattern.
            rule: The rule to generate the pattern (an integer from 0 to 255).

        Returns:
            A NumPy array representing the generated pattern.
        """
        if not 0 <= rule <= 255:
            raise ValueError("Rule must be between 0 and 255.")

        # Create an initial random row
        grid = np.zeros((height, width), dtype=int)
        grid[0, :] = np.random.randint(2, size=width)

        # Generate the pattern
        for i in range(1, height):
            prev = grid[i - 1]
            left = np.roll(prev, 1)
            right = np.roll(prev, -1)
            idx = (left << 2) | (prev << 1) | right
            grid[i] = (rule >> idx) & 1

        return grid


    # <think>
    # Components: TopologicalCognition (Triangle, Square, Hexagon)
    # Dependencies: numpy
    # Data Flows:
    #   - Logic Premises -> Triangle Logic Core -> Deductive Closure
    #   - State Matrix -> Square State Preservation -> Immutable State
    #   - Parallel Streams -> Hexagon Combinatory Synthesis -> Synthesized Output
    # Function Signatures:
    #   - _triangle_logic_core(self, premises: list[bool]) -> bool
    #   - _square_state_preservation(self, state: np.ndarray, update: np.ndarray) -> np.ndarray
    #   - _hexagon_combinatory_synthesis(self, streams: list[np.ndarray]) -> np.ndarray
    # </think>

    def _triangle_logic_core(self, premises: list[bool]) -> bool:
        """
        Triangle Archetype: Minimal logic and deductive closure.
        Provides a foundational, indivisible unit of deductive reasoning.
        Evaluates a list of logical premises for strict boolean consistency (AND logic).
        """
        if not premises:
            return False
        return all(premises)

    def _square_state_preservation(self, state: np.ndarray, update: np.ndarray) -> np.ndarray:
        """
        Square Archetype: Stability, state-preservation, and memory.
        Applies a stable update mechanism to preserve the homeostasis of the state matrix.
        Blends the new update using a golden ratio weighting to prevent volatile state shifts.
        """
        stability_factor = 0.618  # Inverse of Golden Ratio for stability
        return (state * stability_factor) + (update * (1.0 - stability_factor))

    def _hexagon_combinatory_synthesis(self, streams: list[np.ndarray]) -> np.ndarray:
        """
        Hexagon Archetype: Combinatory computation and efficient parallelism.
        Synthesizes diverse parallel processing streams into a coherent optimal output
        by utilizing a harmonic mean equivalent to prevent overconvergence.
        """
        if not streams:
            raise ValueError("Hexagon synthesis requires at least one data stream.")

        stacked_streams = np.stack(streams)
        # Avoid division by zero in harmonic mean equivalent; use a safe combination
        # For simplicity, we use weighted average with penalty on variance to simulate efficient synthesis
        mean_stream = np.mean(stacked_streams, axis=0)
        variance_penalty = np.var(stacked_streams, axis=0) * 0.1
        return mean_stream - variance_penalty

    def run(self, payload: SynthesisPayload) -> dict:
        """
        Integrates the outputs of the five individual functions to create a complex, layered result.

        Args:
            payload (SynthesisPayload): The configuration object containing all synthesis parameters.

        Returns:
            A dictionary containing the results of each of the five functions.
        """
        processed_text = self._deterministic_context_engineering(payload.text)
        future_value = self._neoclassical_compounding(
            payload.principal, payload.rate, payload.times_compounded, payload.years
        )
        network_state = self._symbolic_charge_network(payload.nodes, payload.charges, payload.interactions)
        sepia_image = self._algorithmic_photography(payload.image)
        generated_pattern = self._weaving_algorithm(payload.width, payload.height, payload.rule)

        return {
            "processed_text": processed_text,
            "future_value": future_value,
            "network_state": network_state,
            "sepia_image": sepia_image,
            "generated_pattern": generated_pattern,
        }
