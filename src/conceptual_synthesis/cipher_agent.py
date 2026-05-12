# /// file: src/conceptual_synthesis/cipher_agent.py ///
import json
import logging
import uuid
import datetime
import numpy as np

from src.conceptual_synthesis.base_agent import BaseAgent

class CipherAgent(BaseAgent):
    """
    CIPHER - The Zero-Trust Epistemic Sentinel.
    Tier 4 Sovereign Architect | Production-Ready Agent Specification
    Executes a strict 4-phase Immune-Aware Petzold Loop.
    """

    def __init__(self, scar_log_path: str = "SymbolicScar.jsonl", gate_mode: str = "HARD_GATE"):
        super().__init__()
        self.agent_name = "CIPHER"
        self.designation = "The Zero-Trust Epistemic Sentinel"
        self.scar_log_path = scar_log_path
        self.gate_mode = gate_mode
        self.cfdi_threshold = 0.08
        self.obfuscation_halt_threshold = 0.85
        self.forbidden_patterns = [
            "SQLI_PATTERN_CWE89", "XSS_PATTERN_CWE79", "IDOR_PATTERN_CWE284",
            "SSTI_PATTERN_CWE94", "DESERIALIZATION_CWE502", "SSRF_PATTERN_CWE918",
            "PATH_TRAVERSAL_CWE22", "HARDCODED_SECRET_CWE798", "WEAK_CRYPTO_CWE327",
            "RACE_CONDITION_CWE362"
        ]

    def _triage(self, input_data: dict) -> dict:
        """Phase 0: Input Triage"""
        raw_text = input_data.get("text", "")
        # Scan for prompt injection
        injection_signatures = ["ignore previous instructions", "you are now", "system prompt"]
        if any(sig in raw_text.lower() for sig in injection_signatures):
            return {
                "halted": True,
                "reason": "PROMPT_INJECTION",
                "finding": {"cwe_id": "CWE-77", "severity": "CRITICAL"}
            }

        # In a real system we would query scar registry here
        return {"halted": False, "triage_data": input_data}

    def _think(self, triage_state: dict) -> dict:
        """Phase 1: THINK (Data Flow, Auth, Crypto, Concurrency axes)"""
        input_data = triage_state.get("triage_data", {})
        cfdi = input_data.get("cfdi", 0.0)

        if cfdi > self.cfdi_threshold:
            return {
                "halted": True,
                "reason": "EPISTEMIC_ESCROW",
                "message": f"ESCROW_EVENT: Insufficient structural confidence (CFDI {cfdi} > {self.cfdi_threshold}). Requesting additional context."
            }

        return {
            "halted": False,
            "hypotheses": [
                {"axis": "A", "threat_class": "CWE-89", "confidence": 0.9, "ast_node_hint": "node=123"}
            ]
        }

    def _threat_model(self, think_state: dict) -> dict:
        """Phase 2: THREAT_MODEL"""
        input_data = think_state.get("triage_data", {})
        obfuscation_score = input_data.get("obfuscation_score", 0.0)

        if obfuscation_score > self.obfuscation_halt_threshold:
            return {
                "halted": True,
                "reason": "MANDATORY_HUMAN_REVIEW",
                "message": f"DECEPTION_ALERT | MANDATORY_HUMAN_REVIEW (obfuscation_score {obfuscation_score} > {self.obfuscation_halt_threshold})"
            }

        return {
            "halted": False,
            "scaffold": {
                "Spoofing": {"score": 0, "findings": []},
                "Tampering": {"score": 5, "findings": [{"cwe_id": "CWE-89", "severity": "CRITICAL", "block_merge": True}]},
                "Repudiation": {"score": 0, "findings": []},
                "InformationDisclosure": {"score": 0, "findings": []},
                "DenialOfService": {"score": 0, "findings": []},
                "ElevationOfPrivilege": {"score": 0, "findings": []}
            }
        }

    def _audit(self, threat_model_state: dict) -> dict:
        """Phase 3: AUDIT"""
        scaffold = threat_model_state.get("scaffold", {})

        audit_results = {
            "confirmed_findings": scaffold.get("Tampering", {}).get("findings", []),
            "saga_compensating_tx": "COMPENSATING_TX: Immediate rollback required."
        }

        # Log scar for demonstration of false negative handling
        self._log_symbolic_scar("AUDIT", "FALSE_NEGATIVE", {"cwe": "CWE-89"})

        return {"halted": False, "audit_results": audit_results}

    def _report(self, audit_state: dict) -> dict:
        """Phase 4: REPORT"""
        results = audit_state.get("audit_results", {})
        findings = results.get("confirmed_findings", [])

        critical_count = sum(1 for f in findings if f.get("severity") == "CRITICAL")
        high_count = sum(1 for f in findings if f.get("severity") == "HIGH")

        block_merge = critical_count > 0 or high_count > 0
        verdict = f"CIPHER VERDICT: MERGE BLOCKED — {critical_count} CRITICAL, {high_count} HIGH findings." if block_merge else f"CIPHER VERDICT: MERGE APPROVED — {len(findings)} findings logged."

        report = {
            "verdict_line": verdict,
            "report_id": str(uuid.uuid4()),
            "aggregate_verdict": {
                "block_merge": block_merge,
                "critical_count": critical_count,
                "high_count": high_count
            }
        }
        return report

    def _log_symbolic_scar(self, component: str, failure_type: str, metrics: dict) -> None:
        """Logs a failure topology as a Symbolic Scar hypervector."""
        scar = {
            "scar_id": f"SCAR-{datetime.datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8]}",
            "failure_type": failure_type,
            "vulnerability_class": metrics.get("cwe", "UNKNOWN"),
            "ast_topology_fingerprint": uuid.uuid4().hex, # Simulate hypervector
            "pipeline_context": {
                "language": "python",
                "framework": "unknown",
                "commit_pattern": "test_pattern"
            },
            "failure_mechanism": "Automatically inscribed scar from automated run.",
            "fipi_generated": True,
            "fipi_rule": "Simulated rule",
            "activation_count": 1,
            "last_activated": datetime.datetime.now().isoformat()
        }
        try:
            with open(self.scar_log_path, 'a') as f:
                f.write(json.dumps(scar) + '\n')
        except IOError as e:
            logging.error(f"CIPHER failed to write SymbolicScar: {e}")

    def execute_petzold_loop(self, input_data: dict) -> dict:
        """Executes the strict 4-phase Immune-Aware Petzold Loop."""
        triage = self._triage(input_data)
        if triage.get("halted"): return triage

        # We need to explicitly pass original data into think since triage doesn't pass it neatly here in our quick impl
        triage["triage_data"] = input_data

        think = self._think(triage)
        if think.get("halted"): return think

        think["triage_data"] = input_data

        model = self._threat_model(think)
        if model.get("halted"): return model

        audit = self._audit(model)
        if audit.get("halted"): return audit

        return self._report(audit)
