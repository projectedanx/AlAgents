# /// file: src/conceptual_synthesis/whimsy_agent.py ///
# <think>
# Components: WhimsyAgent
# Dependencies: BaseAgent, json, logging, datetime, uuid
# Data Flows: UI Request -> OBSERVE -> ORIENT -> DECIDE -> ACT -> REVIEW -> Tokenized Delivery
# Function Signatures:
#   - __init__(self) -> None
#   - _trigger_epistemic_escrow(self, reason: str) -> dict
#   - _log_symbolic_scar(self, component: str, reason: str, metrics: dict) -> None
#   - _calculate_cfdi(self, text: str, function_label: str) -> float
#   - _cultural_calibration_gate(self, copy: str, locale: str) -> bool
#   - _whimsy_off_zone_check(self, component_type: str, context_tags: list) -> str
#   - _scar_proximity_search(self, component_type: str, context_tags: list) -> bool
#   - _observe(self, context: dict) -> dict
#   - _orient(self, observation: dict) -> dict
#   - _decide_phase_1(self, orientation: dict) -> dict
#   - _decide_phase_2(self, drafts: dict) -> dict
#   - _act(self, constraints: dict) -> dict
#   - _review(self, delivery: dict) -> dict
#   - execute_petzold_loop(self, context: dict) -> dict
# </think>

import json
import logging
from datetime import datetime, timezone
import uuid
from src.conceptual_synthesis.base_agent import BaseAgent

class WhimsyAgent(BaseAgent):
    """
    WhimsyAgent: WHIMSY - The Affective Topologist.
    Version: 1.0.0-Q1-2026

    A two-manifold, DCCD-native autonomous agent that injects measurable delight,
    micro-interaction specifications, Easter eggs, and brand-sovereign personality
    into digital components by decoupling high-entropy affective ideation
    from low-entropy structural code delivery.
    """

    def __init__(self):
        """Initializes the Whimsy Agent."""
        super().__init__()
        self.agent_name = "WHIMSY"
        self.designation = "The Affective Topologist"
        self.build_version = "1.0.0-Q1-2026"
        self.color_primary = "#FF3B6E"  # Neon Fuchsia
        self.color_secondary = "#1AFFD5"  # Electric Cyan
        self.color_grounding = "#0D0D0D"  # Near-black

        self.scar_log_path = "SymbolicScar.jsonl"
        self.cfdi_threshold = 0.15

        self.whimsy_off_zones = {
            "HARD_LOCKOUT": ["payment_failure", "account_deletion", "data_loss", "access_denied"],
            "RESTRICTED": ["payment_success", "subscription_cancellation", "security_alerts"],
            "CONDITIONAL": ["form_validation", "empty_search"],
            "OPEN": ["loading", "onboarding", "empty_state", "success", "easter_egg", "hover"]
        }

    def _trigger_epistemic_escrow(self, reason: str) -> dict:
        """Halts the generation and triggers Epistemic Escrow."""
        return {
            "status": "HALTED",
            "state": "EPISTEMIC_ESCROW",
            "jur": f"⚠️ WHIMSY EPISTEMIC ESCROW TRIGGERED. {reason}",
            "rta_active": True
        }

    def _log_symbolic_scar(self, component: str, attempted: str, failure_mode: str, cfdi: float, context_tags: list, rule: str) -> None:
        """Logs a Symbolic Scar for a failed whimsy injection."""
        scar_entry = {
            "scar_id": f"SCAR-{uuid.uuid4()}",
            "component": component,
            "attempted_injection": attempted,
            "failure_mode": failure_mode,
            "CFDI_at_failure": cfdi,
            "context_tag": context_tags,
            "rule_derived": rule,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        try:
            with open(self.scar_log_path, "a") as f:
                f.write(json.dumps(scar_entry) + "\n")
        except OSError as e:
            logging.error(f"Failed to log symbolic scar: {e}")

    def _calculate_cfdi(self, text: str, function_label: str) -> float:
        """
        Mock calculation for Confidence-Fidelity Divergence Index (CFDI).
        """
        # A simple mock: if text is too generic, cfdi is high
        if "generic" in text.lower():
            return 0.30
        return 0.05

    def _cultural_calibration_gate(self, copy: str, locale: str) -> bool:
        """
        Cultural Exclusion Check against locale.
        """
        if "sarcastic" in copy.lower() and locale in ["ja-JP", "ko-KR"]:
            return False
        return True

    def _whimsy_off_zone_check(self, component_type: str) -> str:
        """
        Checks if component is in a Whimsy-Off Zone.
        """
        for zone, components in self.whimsy_off_zones.items():
            if component_type in components:
                return zone
        return "OPEN"

    def _scar_proximity_search(self, component_type: str, context_tags: list) -> bool:
        """
        Searches symbolic_scars.jsonl for overlaps.
        Returns True if a relevant scar is found (suppress or restrict).
        """
        try:
            with open(self.scar_log_path, "r") as f:
                for line in f:
                    try:
                        scar = json.loads(line.strip())
                        scar_tags = set(scar.get("context_tag", []))
                        if set(context_tags).intersection(scar_tags):
                            return True
                    except json.JSONDecodeError:
                        continue
        except FileNotFoundError:
            pass
        return False

    def _observe(self, context: dict) -> dict:
        """Phase 1: OBSERVE. Developer Provides Component Brief."""
        return {
            "component_id": context.get("component_id", "unknown"),
            "component_type": context.get("component_type", "loading"),
            "locale": context.get("locale", "en-US"),
            "function_label": context.get("function_label", "unknown"),
            "context_tags": context.get("context_tags", []),
            "manifold_target": context.get("manifold_target", "alpha") # alpha for copy, beta for structural
        }

    def _orient(self, observation: dict) -> dict:
        """Phase 2: ORIENT. WHIMSY Runs Pre-Flight Checks."""
        zone = self._whimsy_off_zone_check(observation["component_type"])
        scar_found = self._scar_proximity_search(observation["component_type"], observation["context_tags"])

        if zone == "HARD_LOCKOUT" or (zone == "RESTRICTED" and observation["manifold_target"] == "alpha"):
             return {
                 "status": "SUPPRESSED",
                 "reason": f"Zone is {zone}. Affective copy forbidden."
             }

        if scar_found and observation["manifold_target"] == "alpha":
            return {
                "status": "SUPPRESSED_BY_SCAR",
                "reason": "Scar proximity overlap detected. Demoting to visual-only or full suppression."
            }

        observation["zone"] = zone
        observation["status"] = "ORIENT_COMPLETE"
        return observation

    def _decide_phase_1(self, orientation: dict) -> dict:
        """Phase 3: DECIDE (DCCD Phase 1 - Unconstrained Affective Draft)."""
        if orientation["status"] != "ORIENT_COMPLETE":
             return orientation

        manifold = orientation["manifold_target"]
        drafts = []

        if manifold == "alpha":
            drafts = [
                {"text": "Crunching the numbers. They're resisting slightly.", "tone": "warm_observational"},
                {"text": "Generic loading message.", "tone": "generic"}
            ]
        elif manifold == "beta":
            drafts = [
                {"concept": "Pataphysical Glitch - controlled violation of spatial expectation", "duration": "80ms"}
            ]

        orientation["drafts"] = drafts
        orientation["status"] = "DECIDE_PHASE_1_COMPLETE"
        return orientation

    def _decide_phase_2(self, phase_1: dict) -> dict:
        """Phase 4: DECIDE (DCCD Phase 2 - Constrained Structural Projection)."""
        if phase_1["status"] != "DECIDE_PHASE_1_COMPLETE":
             return phase_1

        manifold = phase_1["manifold_target"]
        selected_draft = None
        min_cfdi = 1.0

        if manifold == "alpha":
             for draft in phase_1["drafts"]:
                 cfdi = self._calculate_cfdi(draft["text"], phase_1["function_label"])
                 if cfdi < self.cfdi_threshold and cfdi < min_cfdi:

                     if self._cultural_calibration_gate(draft["text"], phase_1["locale"]):
                         selected_draft = draft
                         min_cfdi = cfdi

        elif manifold == "beta":
            selected_draft = phase_1["drafts"][0]
            min_cfdi = 0.05

        if not selected_draft:
            self._log_symbolic_scar(phase_1["component_id"], "All drafts failed", "CFDI_SPIKE_OR_CULTURE_GATE", 1.0, phase_1["context_tags"], "Suppress generation for this context")
            return {
                 "status": "SUPPRESSED",
                 "reason": "No valid drafts passed CFDI and Cultural Calibration gates."
            }

        phase_1["selected_draft"] = selected_draft
        phase_1["final_cfdi"] = min_cfdi
        phase_1["status"] = "DECIDE_PHASE_2_COMPLETE"
        return phase_1

    def _act(self, phase_2: dict) -> dict:
        """Phase 5: ACT. Deliver Manifold-Isolated Artifacts."""
        if phase_2["status"] != "DECIDE_PHASE_2_COMPLETE":
            return phase_2

        manifold = phase_2["manifold_target"]
        artifact = {}

        if manifold == "alpha":
             artifact = {
                 "component_id": phase_2["component_id"],
                 "manifold": "alpha",
                 "copy_variants": [phase_2["selected_draft"]]
             }
        elif manifold == "beta":
             artifact = {
                 "component_id": phase_2["component_id"],
                 "manifold": "beta",
                 "css_js": phase_2["selected_draft"]
             }

        phase_2["artifact"] = artifact
        phase_2["status"] = "ACT_COMPLETE"
        return phase_2

    def _review(self, action: dict) -> dict:
        """Phase 6: REVIEW. Human Developer Integration (Automated Mock)."""
        if action["status"] != "ACT_COMPLETE":
            return action

        action["status"] = "COMPLETE"
        return action

    def execute_petzold_loop(self, context: dict) -> dict:
        """
        Executes the full Petzold Loop (OBSERVE -> ORIENT -> DECIDE_1 -> DECIDE_2 -> ACT -> REVIEW).
        """
        try:
            obs = self._observe(context)
            ori = self._orient(obs)
            d1 = self._decide_phase_1(ori)
            d2 = self._decide_phase_2(d1)
            act = self._act(d2)
            rev = self._review(act)
            return rev
        except Exception as e:
            return self._trigger_epistemic_escrow(str(e))
