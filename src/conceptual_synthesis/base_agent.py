# /// file: src/conceptual_synthesis/base_agent.py ///
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import string
import numpy as np


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

        # Setup translation table, stopwords, and stemmer
        table = str.maketrans("", "", string.punctuation)
        stop_words = set(stopwords.words("english"))
        porter = PorterStemmer()

        # Consolidate lowering, punctuation removal, filtering, and stemming
        # into a single list comprehension to avoid intermediate lists.
        stemmed = [
            porter.stem(w_clean)
            for w_clean in [w.lower().translate(table) for w in tokens]
            if w_clean.isalpha() and w_clean not in stop_words
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
            for j in range(width):
                left = grid[i - 1, (j - 1 + width) % width]
                center = grid[i - 1, j]
                right = grid[i - 1, (j + 1) % width]

                # Apply the rule
                grid[i, j] = (rule >> ((left << 2) | (center << 1) | right)) & 1

        return grid

    def run(
        self,
        text: str,
        principal: float,
        rate: float,
        times_compounded: int,
        years: int,
        nodes: int,
        charges: list[float],
        interactions: np.ndarray,
        image: np.ndarray,
        width: int,
        height: int,
        rule: int,
    ) -> dict:
        """
        Integrates the outputs of the five individual functions to create a complex, layered result.

        Args:
            text (str): The input text to process.
            principal (float): The initial investment amount.
            rate (float): The annual interest rate.
            times_compounded (int): The number of times interest is compounded per year.
            years (int): The investment duration in years.
            nodes (int): The number of nodes in the network.
            charges (list[float]): The charges for each node.
            interactions (np.ndarray): The adjacency matrix for node interactions.
            image (np.ndarray): The input image array.
            width (int): The width of the weaving pattern.
            height (int): The height of the weaving pattern.
            rule (int): The cellular automaton rule to apply.

        Returns:
            A dictionary containing the results of each of the five functions.
        """
        processed_text = self._deterministic_context_engineering(text)
        future_value = self._neoclassical_compounding(
            principal, rate, times_compounded, years
        )
        network_state = self._symbolic_charge_network(nodes, charges, interactions)
        sepia_image = self._algorithmic_photography(image)
        generated_pattern = self._weaving_algorithm(width, height, rule)

        return {
            "processed_text": processed_text,
            "future_value": future_value,
            "network_state": network_state,
            "sepia_image": sepia_image,
            "generated_pattern": generated_pattern,
        }
