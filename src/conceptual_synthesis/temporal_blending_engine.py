from typing import Dict, List, Any

class DiscreteState:
    def __init__(self, fluents: Dict[str, Any]):
        self.fluents = fluents

    def __getitem__(self, key: str) -> Any:
        return self.fluents.get(key, None)

    def contains(self, key: str) -> bool:
        return key in self.fluents

class CausalAction:
    def __init__(self, name: str, preconditions: Dict[str, Any], effects: Dict[str, Any]):
        self.name = name
        self.preconditions = preconditions
        self.effects = effects

class Trace:
    def __init__(self, states: List[DiscreteState], actions: List[CausalAction]):
        if len(states) != len(actions) + 1:
            raise ValueError("A trace must have exactly one more state than actions.")
        self.states = states
        self.actions = actions

class SystemAssuranceAgent:
    def __init__(self, cpi_threshold: float = 0.95):
        self.cpi_threshold = cpi_threshold

    def calculate_cpi(self, trace: Trace) -> float:
        N = len(trace.states)
        if N <= 1:
            return 1.0

        valid_transitions = 0

        for k in range(N - 1):
            s_k = trace.states[k]
            s_k1 = trace.states[k + 1]
            a_k = trace.actions[k]

            # Check preconditions: s_k |= Pre(a_k)
            preconditions_met = True
            for f_name, f_val in a_k.preconditions.items():
                if not s_k.contains(f_name) or s_k[f_name] != f_val:
                    preconditions_met = False
                    break

            # Check effects: s_{k+1} |= Eff(a_k)
            effects_applied = True
            for f_name, f_val in a_k.effects.items():
                if not s_k1.contains(f_name) or s_k1[f_name] != f_val:
                    effects_applied = False
                    break

            # Check frame operator: Frame(s_k, s_{k+1}, a_k)
            frame_operator_valid = True
            for f_name in s_k.fluents.keys():
                if f_name not in a_k.effects:
                    # If not in effects, it must remain invariant
                    if not s_k1.contains(f_name) or s_k1[f_name] != s_k[f_name]:
                        frame_operator_valid = False
                        break

            # Indicator function logic
            if preconditions_met and effects_applied and frame_operator_valid:
                valid_transitions += 1

        cpi = valid_transitions / (N - 1)
        return cpi

    def verify_trace(self, trace: Trace) -> bool:
        return self.calculate_cpi(trace) >= self.cpi_threshold

    def enforce(self, trace: Trace) -> None:
        if not self.verify_trace(trace):
            raise Exception("Epistemic Escrow: Causal Path Integrity (CPI) threshold breached. Triggering Reflexive Repair Loop.")
