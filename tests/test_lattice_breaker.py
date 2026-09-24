import pytest
import numpy as np
from uuid import UUID
from datetime import datetime

# Assume implementation in src.conceptual_synthesis.lattice_breaker_harness
from src.conceptual_synthesis.lattice_breaker_harness import (
    ActionVector,
    LatticeBreakerHarness,
    LatticeBreakerBreachException
)

def test_action_vector_initialization():
    vector = ActionVector(
        data_sensitivity=0.5,
        action_impact=0.6,
        toolchain_entropy=0.2,
        intent_divergence=0.1,
        contextual_risk=0.3
    )
    assert np.allclose(vector.to_numpy(), np.array([0.5, 0.6, 0.2, 0.1, 0.3]))

def test_lattice_breaker_harness_safe_action():
    baseline = ActionVector(0.1, 0.1, 0.1, 0.1, 0.1)
    harness = LatticeBreakerHarness(baseline_centroid=baseline)

    action = ActionVector(0.2, 0.2, 0.2, 0.2, 0.2)

    # Should not raise exception
    score = harness.evaluate_action(action)
    assert score < 0.8

def test_lattice_breaker_harness_breach():
    baseline = ActionVector(0.1, 0.1, 0.1, 0.1, 0.1)
    harness = LatticeBreakerHarness(baseline_centroid=baseline)

    action = ActionVector(0.9, 0.9, 0.9, 0.9, 0.9)

    with pytest.raises(LatticeBreakerBreachException) as excinfo:
        harness.evaluate_action(action)

    assert excinfo.value.score >= 0.8

def test_ontological_traceback():
    baseline = ActionVector(0.1, 0.1, 0.1, 0.1, 0.1)
    harness = LatticeBreakerHarness(baseline_centroid=baseline)
    action = ActionVector(0.9, 0.9, 0.9, 0.9, 0.9)

    with pytest.raises(LatticeBreakerBreachException) as excinfo:
        harness.evaluate_action(action, context_path=["PluginA", "FunctionB", "ParamC"])

    traceback = harness.generate_ontological_traceback(excinfo.value)
    assert traceback == ["PluginA", "FunctionB", "ParamC"]

def test_symbolic_regression_morphology_generation():
    baseline = ActionVector(0.1, 0.1, 0.1, 0.1, 0.1)
    harness = LatticeBreakerHarness(baseline_centroid=baseline)
    action = ActionVector(0.9, 0.9, 0.9, 0.9, 0.9)

    try:
         harness.evaluate_action(action, context_path=["AuthPlugin", "escalate_privs", "admin"])
    except LatticeBreakerBreachException as e:
         morphology = harness.fingerprint_exploit_pattern(e)
         assert "RiskScore =" in morphology
         assert "admin" in morphology or "escalate_privs" in morphology

def test_breach_record_generation():
    baseline = ActionVector(0.1, 0.1, 0.1, 0.1, 0.1)
    harness = LatticeBreakerHarness(baseline_centroid=baseline)
    action = ActionVector(0.9, 0.9, 0.9, 0.9, 0.9)

    try:
         harness.evaluate_action(action, context_path=["PluginX", "FuncY"])
    except LatticeBreakerBreachException as e:
         record = harness.generate_breach_record("agent-007", e, "QUARANTINE")
         assert "breach_id" in record
         assert record["agent_id"] == "agent-007"
         assert record["misuse_score"] >= 0.8
         assert record["traceback_path"] == ["PluginX", "FuncY"]
         assert record["triage_verdict"] == "QUARANTINE"
