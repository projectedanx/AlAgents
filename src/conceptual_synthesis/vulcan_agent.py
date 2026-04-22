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
        self.build_version = "1.0.0"
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
        except Exception as e:
            logging.error(f"Failed to log symbolic scar: {e}")

    def _observe(self, context: dict) -> dict:
        """
        Phase 1: OBSERVE. Takes in raw business requirements and physical system constraints.
        """
        return {
            "requirements": context.get("requirements", []),
            "constraints": context.get("constraints", [])
        }

    def _think(self, observation: dict) -> dict:
        """
        Phase 2: THINK. Deductive breakdown of domains.
        """
        domains = []
        for req in observation.get("requirements", []):
            if "domain" in req:
                domains.append(req["domain"])

        return {
            "domains": list(set(domains)),
            "observation": observation
        }

    def _dag(self, thought: dict, context: dict) -> dict:
        """
        Phase 3: DAG (Directed Acyclic Graph). Maps data flows and microservice boundaries.
        Enforces the Mereological Mandate (No state inheritance).
        """
        microservices = context.get("microservices", [])

        # Check Mereological Mandate
        for ms in microservices:
            if ms.get("inherits_state", False):
                self._log_symbolic_scar("DAG Phase", "Mereological Mandate Violation (State Inheritance)", {"service": ms.get("name")})
                raise ValueError(f"Mereological Mandate Violation: Microservice '{ms.get('name')}' inherits state.")

        return {
            "microservices": microservices,
            "thought": thought
        }

    def _evaluate(self, dag: dict, context: dict) -> dict:
        """
        Phase 4: EVALUATE. Stress-tests the DAG against physical laws and anti-goals.
        Enforces Shared Database Anathema.
        """
        databases = context.get("databases", [])

        # Check Shared Database Anathema
        db_writers = {}
        for db in databases:
            writers = db.get("writers", [])
            if len(set(writers)) > 1:
                self._log_symbolic_scar("EVALUATE Phase", "Shared Database Anathema Violation", {"database": db.get("name"), "writers": writers})
                raise ValueError(f"Shared Database Anathema Violation: Database '{db.get('name')}' has multiple writing contexts: {writers}")

        return {
            "evaluation_status": "PASS",
            "dag": dag
        }

    def _architect(self, evaluation: dict) -> dict:
        """
        Phase 5: ARCHITECT. Extrudes the final technical deliverables.
        """
        # Generate ADR
        adr = f"""# Architecture Decision Record
ID: {uuid.uuid4()}
Title: System Topology Blueprint
Status: Proposed

## Context
Generated by VULCAN Agent based on provided business requirements.

## Decision
Implemented strict Domain-Driven boundaries.

## Consequences
High cohesion, loose coupling achieved.
"""

        # Generate C4 Model
        c4 = """```mermaid
C4Context
    title System Context diagram
    Person(user, "User", "A user of the system")
    System(system, "Software System", "The core system")
    Rel(user, system, "Uses")
```"""

        # Generate DDD Context Map
        ddd = """Domain: Primary
Bounded Contexts:
  - Context: User Management
    Responsibilities: Authentication, Authorization
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
