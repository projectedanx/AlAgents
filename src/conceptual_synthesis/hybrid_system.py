# /// file: src/conceptual_synthesis/hybrid_system.py ///
import numpy as np
from src.conceptual_synthesis.base_agent import BaseAgent

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


def hybrid_synthesis(
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
    return _agent.run(
        text,
        principal,
        rate,
        times_compounded,
        years,
        nodes,
        charges,
        interactions,
        image,
        width,
        height,
        rule,
    )
