import pytest
import networkx as nx
from src.conceptual_synthesis.invariant_verification_harness import (
    TelemetryData,
    AnomalyMiner,
    SymbolicEquationSolver,
    ExplanatoryGraphStructurer,
    PopperianFalsifier,
    DeIdealizationEngine,
    CognitiveUnderstandingCompiler,
    FictivePrinciple
)
from src.conceptual_synthesis.pap_occam_loss import OntologicalCommitment, Assumption, ParetoOptimizationModule

def test_scenario_1_ptolemaic_vs_keplerian():
    """
    Prompt 1: Reconstructing Ptolemaic Over-Fitting vs. Keplerian Parsimony
    """
    miner = AnomalyMiner(sigma_threshold=3.0)
    solver = SymbolicEquationSolver()
    pareto_opt = ParetoOptimizationModule(sigma_threshold=3.0)

    # 1. Schema for Planetary Orbital Telemetry
    telemetry = [
        TelemetryData(timestamp=1.0, coordinates=[1.0, 0.5], prediction=0.5, actual=0.8, variance=0.001),
        TelemetryData(timestamp=2.0, coordinates=[1.5, 0.7], prediction=0.6, actual=0.9, variance=0.001)
    ]

    # Simulate anomalous data
    anomalies = miner.screen_data(telemetry)
    assert len(anomalies) == 2

    # 2. Compare Models using Occam-Loss Compiler

    # Model A: Geocentric (20+ free parameters, ad-hoc)
    geo_commitment = OntologicalCommitment(
        theory_name="Geocentric Epicycles",
        variables=["Earth", "Mars_Epicycle", "Deferent"],
        free_parameters=20,
        assumptions=[Assumption(name="Earth_is_Center", probability_valid=0.1)]
    )
    geo_law = solver.generate_law("Geocentric", anomalies, is_coordinate_free=False, free_params=20)
    geo_error = 2.0 # High error on Venusian phase constraints

    # Model B: Keplerian (Few parameters, heliocentric)
    kepler_commitment = OntologicalCommitment(
        theory_name="Keplerian Ellipses",
        variables=["Sun", "Mars"],
        free_parameters=2,
        assumptions=[Assumption(name="Sun_is_Focus", probability_valid=0.9)]
    )
    kepler_law = solver.generate_law("Keplerian", anomalies, is_coordinate_free=True, free_params=2)
    kepler_error = 0.5

    # Evaluate Models
    selected_commitment = pareto_opt.evaluate_models(
        baseline_commitment=geo_commitment, baseline_error=geo_error,
        new_commitment=kepler_commitment, new_error=kepler_error,
        error_std_dev=0.1
    )

    # Keplerian should win due to lower Occam Loss and lower prediction error
    assert selected_commitment.theory_name == "Keplerian Ellipses"


def test_scenario_2_cognitive_understanding():
    """
    Prompt 2: Modeling the Epistemic Distinction Between Factive Knowledge and Non-Factive Understanding
    """
    compiler = CognitiveUnderstandingCompiler()

    # 1. Ontology of "Fictive Principles"
    newtonian_fictive_principles = [
        FictivePrinciple(name="Instantaneous_Action_at_Distance", is_factive=False, utility_weight=0.9),
        FictivePrinciple(name="Absolute_Time", is_factive=False, utility_weight=0.85),
        FictivePrinciple(name="Euclidean_Space", is_factive=False, utility_weight=0.95)
    ]

    for p in newtonian_fictive_principles:
        compiler.add_fictive_principle(p)

    # 2 & 3. Grasping Metric
    # Newtonian framework solving an astrophysical trajectory
    dependencies = 10 # Successfully manipulating variables (mass, distance)
    transferability = 0.8 # Transferring model to unencountered low-velocity domain

    grasping_score = compiler.calculate_grasping_metric(dependencies, transferability)

    # Despite the non-factive assumptions (GR defeaters), utility_weight is high,
    # so grasping_score should remain relatively high (> 0)
    assert grasping_score > 5.0
    print(f"Understanding Score with GR defeaters: {grasping_score}")


def test_scenario_3_deidealization_engine():
    """
    Prompt 3: Automating the De-Idealization Loop in Systems Biology and Material Sciences
    """
    falsifier = PopperianFalsifier()
    engine = DeIdealizationEngine(falsifier)

    # 1. Formal representation of an idealized model as a DAG
    model_dag = nx.DiGraph()
    model_dag.add_node("Protein_Backbone")
    model_dag.add_node("Zero_Friction_Solvent")
    model_dag.add_node("Rigid_Body_Assumption")

    model_dag.add_edge("Protein_Backbone", "Zero_Friction_Solvent")
    model_dag.add_edge("Protein_Backbone", "Rigid_Body_Assumption")

    assumptions = [
        Assumption(name="Zero_Friction_Solvent", probability_valid=0.5), # highly idealized
        Assumption(name="Rigid_Body_Assumption", probability_valid=0.6)
    ]

    # 2 & 3. Boundary Auditor & Feedback Loop
    prediction = 1.0 # Ribbon diagram prediction
    actual = 4.5     # High fidelity experimental data (dynamics dominant)
    std_dev = 0.5    # 3-sigma would be 1.5. Error is 3.5.

    # Trigger De-Idealization
    refined_dag, was_refined = engine.evaluate_and_refine(model_dag, prediction, actual, std_dev, assumptions)

    assert was_refined is True
    # Verify the faulty assumption ("Zero_Friction_Solvent") was targeted and removed from the active idealized constraints
    assert not refined_dag.has_node("Zero_Friction_Solvent")
    assert refined_dag.has_node("Rigid_Body_Assumption") # Only one refined at a time
    print(f"Refined DAG Nodes: {refined_dag.nodes()}")
