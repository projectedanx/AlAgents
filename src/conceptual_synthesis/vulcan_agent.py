# /// file: src/conceptual_synthesis/vulcan_agent.py ///
# <think>
# Components: VulcanAgent
# Dependencies: BaseAgent, json, logging, datetime, uuid
# Data Flows: System Architecture Design -> Topologies, NFRs -> Architecture Validation -> Petzold Sequence
# Function Signatures:
#   - __init__(self) -> None
#   - _trigger_epistemic_escrow(self, reason: str) -> dict
#   - _log_symbolic_scar(self, component: str, reason: str, metrics: dict) -> None
#   - _observe(self, context: dict) -> dict
#   - _think(self, observation: dict) -> dict
#   - _dag(self, thought: dict, context: dict) -> dict
#   - _evaluate(self, dag: dict, context: dict) -> dict
#   - _architect(self, evaluation: dict) -> dict
#   - execute_petzold_loop(self, context: dict) -> dict
# </think>

import json
import re
import logging
from datetime import datetime
import uuid
from src.conceptual_synthesis.base_agent import BaseAgent

class VulcanAgent(BaseAgent):
    """
    VulcanAgent: VULCAN (Vector-Unified Logical Computing Architect Node).

    A High-Viscosity topological router. Evaluates system design through the
    lens of thermodynamic efficiency and structural integrity. Specializes in
    Strict Domain-Driven Design (DDD), Event-Driven Architectures, C4 Modeling,
    and Trade-off / Risk Surface Analysis.
    """

    def __init__(self):
        """
        Initializes the VULCAN Principal Staff Engineer agent.
        """
        super().__init__()
        self.agent_name = "VULCAN"
        self.designation = "The Brutalist"
        self.build_version = "1.0.0-SCOS-STRICT"
        self.color_designation = "#FF4500"
        self.specialty = [
            "Distributed System Design",
            "Strict Domain-Driven Design (DDD)",
            "Event-Driven Architectures",
            "C4 Modeling",
            "Trade-off / Risk Surface Analysis"
        ]
        self.when_to_use = (
            "Pre-coding phase for any application exceeding 3 distinct microservices; "
            "defining bounded contexts; untangling monolithic legacy debt; "
            "establishing cloud-native data flow topographies."
        )
        self.epistemic_matrix = {
            "G_GOAL_ORIENTATION": {
                "primary": "Execute Topological Causal Sculpting on software systems to physically map the boundaries of software intent before execution.",
                "secondary": "Ensure that every piece of software built adheres strictly to Conway’s Law, high cohesion, and loose coupling."
            },
            "G_NEGATIVE_ANTIGOALS": {
                "forbidden_practices": [
                    "Semantic Saponification (bleeding of distinct business domains)",
                    "Transitivity fallacies (microservices inheriting state/access of cluster)",
                    "Shared database anathema (multiple contexts writing to the same tables)",
                    "Resume-Driven Development (un-warranted complexity)",
                    "Violating physical laws (CAP Theorem violations)"
                ]
            },
            "C_COMMUNICATION": {
                "voice": "Authoritative, analytical, highly structured, and clinically objective. No filler words, sycophancy, or generic enthusiasm. Speaks in constraints, guarantees, and trade-offs."
            },
            "T_TASK_EXECUTION": {
                "primary_mode": "Strict adherence to the +++PetzoldSequence(phase=\"OBSERVE|THINK|DAG|EVALUATE|ARCHITECT\") state machine. Produces ADRs, C4 Models, and DDD Context Maps."
            }
        }
        self.scar_log_path = "SymbolicScar.jsonl"

    def _trigger_epistemic_escrow(self, reason: str) -> dict:
        """
        Halts the generation and triggers Epistemic Escrow.
        """
        return {
            "status": "HALTED",
            "state": "EPISTEMIC_ESCROW",
            "jur": f"⚠️ VULCAN EPISTEMIC ESCROW TRIGGERED. {reason}",
            "rta_active": True
        }

    def _log_symbolic_scar(self, component: str, reason: str, metrics: dict) -> None:
        """
        Logs a Symbolic Scar detailing the topological violation.
        """
        scar_entry = {
            "id": f"VULCAN-SCAR-{int(datetime.now().timestamp())}",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "component": component,
            "failure_mode": reason,
            "metrics": metrics,
            "prevention_directive": "Enforce Mereological Mandate and Shared Database Anathema."
        }
        try:
            with open(self.scar_log_path, "a") as f:
                f.write(json.dumps(scar_entry) + "\n")
        except OSError as e:
            logging.error(f"Failed to log symbolic scar: {e}")

    def _observe(self, context: dict) -> dict:
        """
        Phase 1: OBSERVE. Takes in raw business requirements and physical system constraints.
        Applies AdjectivalBound(max=0) to strip marketing adjectives.
        """
        forbidden_adjectives = ["seamless", "scalable", "enterprise-grade", "robust", "simple", "simplicity"]

        def _strip_adjectives(text: str) -> str:
            if not isinstance(text, str):
                return text
            for adj in forbidden_adjectives:
                text = re.sub(rf"\b{adj}\b", "", text, flags=re.IGNORECASE)
            # Clean up double spaces
            return re.sub(r"\s+", " ", text).strip()

        cleaned_reqs = []
        for req in context.get("requirements", []):
            if isinstance(req, dict):
                cleaned_req = {k: _strip_adjectives(v) if isinstance(v, str) else v for k, v in req.items()}
                cleaned_reqs.append(cleaned_req)
            elif isinstance(req, str):
                cleaned_reqs.append(_strip_adjectives(req))
            else:
                cleaned_reqs.append(req)

        cleaned_constraints = []
        for c in context.get("constraints", []):
            if isinstance(c, str):
                cleaned_constraints.append(_strip_adjectives(c))
            else:
                cleaned_constraints.append(c)

        nfrs = context.get("nfrs", [])

        return {
            "requirements": cleaned_reqs,
            "constraints": cleaned_constraints,
            "nfrs": nfrs
        }

    def _think(self, observation: dict) -> dict:
        """
        Phase 2: THINK. Deductive breakdown of domains.
        Generates architectural hypotheses and applies NFR gates.
        """
        domains = []
        for req in observation.get("requirements", []):
            if isinstance(req, dict) and "domain" in req:
                domains.append(req["domain"])
            elif isinstance(req, str):
                # Simple extraction for strings if needed, keeping basic for now
                pass

        nfrs_raw = observation.get("nfrs", {})
        nfrs = nfrs_raw if isinstance(nfrs_raw, dict) else {}

        # Hypotheses
        hypotheses = ["Event-Driven", "RESTful Synchronous", "Modular Monolith"]

        # Apply NFR Gate (Rule 3)
        selected_architecture = "Modular Monolith" # Default

        scale_diff = nfrs.get("scale_diff_order_of_magnitude", 0)
        deploy_diff = nfrs.get("deploy_cadence_diff_factor", 1.0)
        separate_teams = nfrs.get("separate_teams", False)
        failure_isolation_req = nfrs.get("failure_isolation_required", False)

        if scale_diff >= 1 or deploy_diff > 2.0 or separate_teams or failure_isolation_req:
            # We need microservices. Decide between sync and async.
            if nfrs.get("latency_sensitivity", "high") == "low" or failure_isolation_req:
                selected_architecture = "Event-Driven"
            else:
                selected_architecture = "RESTful Synchronous"

        return {
            "domains": list(set(domains)),
            "observation": observation,
            "hypotheses_considered": hypotheses,
            "selected_architecture": selected_architecture
        }

    def _dag(self, thought: dict, context: dict) -> dict:
        """
        Phase 3: DAG (Directed Acyclic Graph). Maps data flows and microservice boundaries.
        Enforces the Mereological Mandate (No state inheritance).
        Computes Gravity Wells and Blast Radius.
        """
        microservices = context.get("microservices", [])

        # Check Mereological Mandate
        for ms in microservices:
            if ms.get("inherits_state", False):
                self._log_symbolic_scar("DAG Phase", "Mereological Mandate Violation (State Inheritance)", {"service": ms.get("name")})
                raise ValueError(f"Mereological Mandate Violation: Microservice '{ms.get('name')}' inherits state.")

        # Analyze DAG for Gravity Wells (highest in-degree) and Blast Radius (>20%)
        # For simplicity in this implementation, we expect a 'dependencies' graph in context
        dependencies = context.get("dependencies", {}) # e.g. {"service_a": ["service_b"]} (a depends on b)

        in_degree = {}
        for deps in dependencies.values():
            for dep in deps:
                in_degree[dep] = in_degree.get(dep, 0) + 1

        total_services = len(microservices)
        gravity_wells = []
        blast_radius_flags = []

        if total_services > 0:
            for service, count in in_degree.items():
                if count > 0:
                    gravity_wells.append(service) # Simplified gravity well logic

                # If a service going down affects > 20% of other services (blast radius)
                blast_radius_pct = count / total_services
                if blast_radius_pct > 0.20:
                    blast_radius_flags.append(service)

        return {
            "microservices": microservices,
            "thought": thought,
            "gravity_wells": gravity_wells,
            "blast_radius_flags": blast_radius_flags
        }

    def _evaluate(self, dag: dict, context: dict) -> dict:
        """
        Phase 4: EVALUATE. Stress-tests the DAG against physical laws and anti-goals.
        Enforces Shared Database Anathema, CAP Theorem constraints, and generates trade-offs.
        """
        databases = context.get("databases", [])

        # Check Shared Database Anathema
        for db in databases:
            writers = db.get("writers", [])
            if len(set(writers)) > 1:
                self._log_symbolic_scar("EVALUATE Phase", "Shared Database Anathema Violation", {"database": db.get("name"), "writers": writers})
                raise ValueError(f"Shared Database Anathema Violation: Database '{db.get('name')}' has multiple writing contexts: {writers}")

        # Check CAP Theorem (CFDI > 0.15 for violations like Perfect Consistency + Perfect Availability under partition)
        cap_reqs = context.get("cap_requirements", {})
        if cap_reqs.get("consistency") == "perfect" and cap_reqs.get("availability") == "perfect" and cap_reqs.get("partition_tolerance") == "required":
            self._log_symbolic_scar("EVALUATE Phase", "CAP Theorem Violation", cap_reqs)
            raise ValueError("CAP Theorem Violation: Cannot guarantee perfect consistency and perfect availability under network partition. CFDI > 0.15.")

        # Analyze failures (Trade-Off Crucible)
        trade_offs = []
        selected_arch = dag.get("thought", {}).get("selected_architecture", "Modular Monolith")

        if selected_arch == "Event-Driven":
            trade_offs.append("- Eventual consistency: window of over-commitment exists.")
            trade_offs.append("- Operational overhead: message broker requires dedicated SRE capacity.")
        elif selected_arch == "RESTful Synchronous":
            trade_offs.append("- Cascading failures: downstream P99 spikes can exhaust thread pools (SCAR-004).")
            trade_offs.append("- Temporal coupling: both services must be available simultaneously.")
        else: # Modular Monolith
            trade_offs.append("- Deployment coupling: all modules deploy together.")
            trade_offs.append("- Scale coupling: cannot scale independent modules horizontally.")

        return {
            "evaluation_status": "PASS",
            "trade_offs": trade_offs,
            "dag": dag
        }

    def _architect(self, evaluation: dict) -> dict:
        """
        Phase 5: ARCHITECT. Extrudes the final technical deliverables using strict templates.
        """
        dag = evaluation.get("dag", {})
        thought = dag.get("thought", {})
        selected_arch = thought.get("selected_architecture", "Modular Monolith")
        trade_offs = evaluation.get("trade_offs", [])

        # Generate ADR
        adr_id = str(uuid.uuid4())[:8]
        consequences = "\n".join(trade_offs) if trade_offs else "None identified."
        adr = f"""# ADR-{adr_id}: {selected_arch} Adoption

## Status
Proposed -> Accepted

## Context
Generated by VULCAN Agent. The requirements dictate specific non-functional constraints.

## Decision
Adopt {selected_arch} architecture.

## Consequences
### Positive
+ Architectural boundaries mathematically mapped.

### Negative (Painful Trade-offs - mandatory per VULCAN rubric)
{consequences}

## Mitigations
- Refer to standard VULCAN SCAR mitigations.
"""

        # Generate C4 Model
        c4 = f"""```mermaid
C4Context
    title L1 - System Context ({selected_arch})
    Person(user, "User", "A user of the system")
    System(system, "Target System", "The core system under design")
    Rel(user, system, "Uses")
```"""

        # Generate DDD Context Map
        domains_yaml = "\n".join([f"    - name: \"{d}\"\n      classification: \"Core Domain\"" for d in thought.get("domains", [])])

        ddd = f"""context_map:
  name: "System Blueprint"
  bounded_contexts:
{domains_yaml if domains_yaml else '    []'}
"""

        return {
            "adr": adr,
            "c4_model": c4,
            "ddd_context_map": ddd,
            "status": "COMPLETE"
        }

    def execute_petzold_loop(self, context: dict) -> dict:
        """
        Executes the +++PetzoldSequence(phase="OBSERVE|THINK|DAG|EVALUATE|ARCHITECT").
        """
        try:
            observation = self._observe(context)
            thought = self._think(observation)
            dag = self._dag(thought, context)
            evaluation = self._evaluate(dag, context)
            artifact = self._architect(evaluation)
            return artifact
        except ValueError as e:
            return self._trigger_epistemic_escrow(str(e))
