# /// file: src/conceptual_synthesis/hybrid_system.py ///
import numpy as np
from src.conceptual_synthesis.base_agent import BaseAgent, SynthesisPayload

_agent = BaseAgent()


def deterministic_context_engineering(text: str) -> list[str]:
    """
    Processes text by applying deterministic rules to engineer a specific context.

    This function tokenizes the input text, removes punctuation and stopwords,
    and applies stemming to the remaining words.

    Args:
        text: The input string to process.

    Returns:
        A list of processed tokens.
    """
    return _agent._deterministic_context_engineering(text)


def neoclassical_compounding(
    principal: float, rate: float, times_compounded: int, years: int
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

    Raises:
        ValueError: If times_compounded is less than or equal to zero.
    """
    if times_compounded <= 0:
        raise ValueError(
            "times_compounded must be greater than zero to avoid division by zero."
        )

    return _agent._neoclassical_compounding(principal, rate, times_compounded, years)


def symbolic_charge_network(
    nodes: int, charges: list[float], interactions: np.ndarray
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
    return _agent._symbolic_charge_network(nodes, charges, interactions)


def algorithmic_photography(image: np.ndarray) -> np.ndarray:
    """
    Applies a sepia filter to an image represented as a NumPy array.

    Args:
        image: A NumPy array representing the image (in RGB format).

    Returns:
        A NumPy array representing the image with the sepia filter applied.
    """
    return _agent._algorithmic_photography(image)


def weaving_algorithm(width: int, height: int, rule: int) -> np.ndarray:
    """
    Generates a textile-like pattern based on a computational rule.

    Args:
        width: The width of the pattern.
        height: The height of the pattern.
        rule: The rule to generate the pattern (an integer from 0 to 255).

    Returns:
        A NumPy array representing the generated pattern.
    """
    return _agent._weaving_algorithm(width, height, rule)



def triangle_logic_core(premises: list[bool]) -> bool:
    """
    Triangle Archetype: Minimal logic and deductive closure.
    Provides a foundational, indivisible unit of deductive reasoning.
    Evaluates a list of logical premises for strict boolean consistency (AND logic).

    Args:
        premises: A list of boolean logical premises to evaluate.

    Returns:
        The boolean consistency of the premises.
    """
    return _agent._triangle_logic_core(premises)


def square_state_preservation(state: np.ndarray, update: np.ndarray) -> np.ndarray:
    """
    Square Archetype: Stability, state-preservation, and memory.
    Applies a stable update mechanism to preserve the homeostasis of the state matrix.
    Blends the new update using a golden ratio weighting to prevent volatile state shifts.

    Args:
        state: The current state array.
        update: The update array.

    Returns:
        The newly preserved state array.
    """
    return _agent._square_state_preservation(state, update)


def hexagon_combinatory_synthesis(streams: list[np.ndarray]) -> np.ndarray:
    """
    Hexagon Archetype: Combinatory computation and efficient parallelism.
    Synthesizes diverse parallel processing streams into a coherent optimal output
    by utilizing a harmonic mean equivalent to prevent overconvergence.

    Args:
        streams: A list of stream arrays to be combined.

    Returns:
        The final synthesized stream array.
    """
    return _agent._hexagon_combinatory_synthesis(streams)


def hybrid_synthesis(payload: SynthesisPayload) -> dict:
    """
    Integrates the outputs of the five individual functions to create a complex, layered result.

    Args:
        payload (SynthesisPayload): The configuration object containing all synthesis parameters.

    Returns:
        A dictionary containing the results of each of the five functions.
    """
    return _agent.run(payload)
