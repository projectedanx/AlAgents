import sys
import os

# Ensure the root of the project is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.conceptual_synthesis.pap_occam_loss import (
    Assumption,
    OntologicalCommitment,
    OccamLossCompiler,
    ParetoOptimizationModule
)

def run_simulation():
    print("--- PARSIMONIOUS ARCHITECTURE PROTOCOL (PAP) SIMULATION ---")
    print("Scenario: Ptolemaic Geocentrism vs. Copernican Heliocentrism\n")

    # 1. Define Ptolemaic Geocentrism (High Complexity, Many Assumptions)
    # Assumes Earth is center, requires epicycles, equants, deferents.
    ptolemy_assumptions = [
        Assumption(name="Earth is stationary at the center", probability_valid=0.5),
        Assumption(name="Planets move in perfect circles (epicycles)", probability_valid=0.6),
        Assumption(name="Epicycles move along larger circles (deferents)", probability_valid=0.7),
        Assumption(name="Motion is uniform around an offset point (equant)", probability_valid=0.4),
        Assumption(name="Stars are fixed on an outer sphere", probability_valid=0.8)
    ]

    ptolemy_model = OntologicalCommitment(
        theory_name="Ptolemaic Geocentrism",
        variables=["planet_position", "time"],
        free_parameters=40, # Dozens of epicycle parameters
        assumptions=ptolemy_assumptions
    )

    # 2. Define Copernican Heliocentrism (Lower Complexity, Fewer Assumptions)
    # Assumes Sun is center, Earth moves.
    copernicus_assumptions = [
        Assumption(name="Sun is stationary near the center", probability_valid=0.9),
        Assumption(name="Earth and planets orbit the Sun", probability_valid=0.9),
        Assumption(name="Earth rotates on its axis", probability_valid=0.95)
    ]

    copernicus_model = OntologicalCommitment(
        theory_name="Copernican Heliocentrism",
        variables=["planet_position", "time"],
        free_parameters=7, # Fewer parameters (orbital radii, speeds)
        assumptions=copernicus_assumptions
    )

    # Simulate prediction errors
    # Let's say Ptolemy is highly curve-fitted and has a low error on past data
    ptolemy_error = 0.05
    # Copernicus might have slightly higher error initially (due to circular orbits assumption before Kepler)
    # or let's say it's equivalent for this simulation
    copernicus_error = 0.06

    error_std_dev = 0.02

    # Analyze
    compiler = OccamLossCompiler(parameter_penalty_weight=0.1)

    print("--- MODEL COMPILER ANALYSIS ---")
    ptolemy_complexity = compiler.compute_complexity(ptolemy_model)
    ptolemy_loss = compiler.compile_loss(ptolemy_model, ptolemy_error)
    print(f"[{ptolemy_model.theory_name}]")
    print(f"  Free Parameters: {ptolemy_model.free_parameters}")
    print(f"  Complexity: {ptolemy_complexity:.4f}")
    print(f"  Occam Loss: {ptolemy_loss:.4f}\n")

    copernicus_complexity = compiler.compute_complexity(copernicus_model)
    copernicus_loss = compiler.compile_loss(copernicus_model, copernicus_error)
    print(f"[{copernicus_model.theory_name}]")
    print(f"  Free Parameters: {copernicus_model.free_parameters}")
    print(f"  Complexity: {copernicus_complexity:.4f}")
    print(f"  Occam Loss: {copernicus_loss:.4f}\n")

    # Optimize
    print("--- PARETO OPTIMIZATION (THEORY SELECTION) ---")
    optimizer = ParetoOptimizationModule(sigma_threshold=3.0)

    # Does Copernicus replace Ptolemy?
    # In this context, we treat Ptolemy as the baseline (the established theory)
    selected_model = optimizer.evaluate_models(
        baseline_commitment=ptolemy_model, baseline_error=ptolemy_error,
        new_commitment=copernicus_model, new_error=copernicus_error,
        error_std_dev=error_std_dev
    )

    print(f"\nFINAL SELECTION: {selected_model.theory_name}")

if __name__ == "__main__":
    run_simulation()
