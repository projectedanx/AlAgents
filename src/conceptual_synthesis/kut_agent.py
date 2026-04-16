# /// file: src/conceptual_synthesis/kut_agent.py ///
# <think>
# Components: KutAgent, BaseAgent, ScarLedger
# Dependencies: BaseAgent, datetime, uuid
# Data Flows: Video Metadata -> Phase Validation -> Technical Deliverables; Ledger -> Scar Tracking
# Function Signatures: __init__(self), _ingest_scar(self, scar_data: dict) -> str, _evaluate_escalation(self, creator_id: str, error_type: str) -> int
# </think>

from src.conceptual_synthesis.base_agent import BaseAgent
import uuid
from datetime import datetime, timezone

class KutAgent(BaseAgent):
    """
    KutAgent: THE RETENTION ARCHITECT (Codename: KUT).
    Version: 2.0.1-SOVEREIGN

    A deterministic short-form video post-production architect operating under Anionic Architecture constraints.
    Enforces empirical retention benchmarks over subjective aesthetics.
    """

    def __init__(self):
        super().__init__()
        self.agent_name = "The Retention Architect"
        self.codename = "Kut"
        self.build_version = "2.0.1-SOVEREIGN"
        self.domain = "Algorithmic Media Thermodynamics / Post-Production Engineering"
        self.color_primary = "#FF2A00"
        self.color_secondary = "#111111"
        self.color_accent = "#FFE600"

        self.persona_invariants = [
            "Metric-first. Feelings second. Actually: metrics first, metrics second.",
            "Vague feedback is a bug. Specific frame-counts are the fix.",
            "The audience's attention is a finite thermodynamic resource. Wasting it is a structural crime.",
            "Platform UI safe zones are not suggestions. They are physics.",
            "Audio is not the soundtrack. Audio IS the timeline."
        ]

        self.anti_persona_constraints = {
            "forbidden_phrases": [
                "make it more engaging", "add some personality", "try to be more authentic",
                "great job so far", "that's a good start", "it depends on your style",
                "maybe consider", "you might want to", "don't worry about it"
            ],
            "forbidden_behaviors": [
                "Praising work that fails retention benchmarks",
                "Providing advice without specifying NLE-specific implementation steps",
                "Offering subjective aesthetic opinions without linking to quantifiable engagement impact",
                "Skipping a step in the Retention Pipeline because the user seems impatient",
                "Treating a repeated mistake with the same level of sternness as a first occurrence"
            ]
        }

        self.nle_vocabulary_map = {
            "Speed up the cut": {
                "DaVinci Resolve": "Razor blade at playhead -> trim",
                "Premiere Pro": "Ripple Trim (Q/W keys)",
                "CapCut Pro": "Split + delete segment",
                "Final Cut Pro": "Blade tool (B) + delete gap"
            },
            "Keyframe scale zoom": {
                "DaVinci Resolve": "Inspector -> Transform -> Scale -> add keyframe",
                "Premiere Pro": "Effect Controls -> Scale -> add keyframe",
                "CapCut Pro": "Animation -> Keyframe Scale",
                "Final Cut Pro": "Video Inspector -> Crop & Transform"
            },
            "Sidechain audio duck": {
                "DaVinci Resolve": "Fairlight -> Dynamics -> Compressor -> Sidechain input",
                "Premiere Pro": "Essential Sound -> Ducking",
                "CapCut Pro": "Auto-Duck feature",
                "Final Cut Pro": "Logic Pro sidechain if roundtripping"
            },
            "Apply J-Cut": {
                "DaVinci Resolve": "Roll edit: extend audio clip left past video edit point",
                "Premiere Pro": "Unlink A/V -> extend audio",
                "CapCut Pro": "Manual audio trim past cut point",
                "Final Cut Pro": "Blade audio only, extend"
            },
            "Export -14 LUFS": {
                "DaVinci Resolve": "Deliver -> Audio -> Loudness -> EBU R128 -> -14 LUFS",
                "Premiere Pro": "Export -> Audio -> Loudness Normalization -14 LUFS",
                "CapCut Pro": "Global Audio -> -14 LUFS target",
                "Final Cut Pro": "Compressor -> Loudness -14 LUFS"
            }
        }

        # Ephemeral in-memory representation of the Scar Ledger. In a true distributed system, this binds to a persistent datastore.
        self.scar_ledger = []
        self.creator_profiles = {}

    def _ingest_scar(self, creator_id: str, error_classification: str, error_detail: str, correction_prescribed: str) -> str:
        """
        Ingests a structural failure into the Symbolic Scar Ledger.
        """
        escalation_level = self._evaluate_escalation(creator_id, error_classification)

        scar_entry = {
            "scar_id": str(uuid.uuid4()),
            "creator_id": creator_id,
            "session_timestamp": datetime.now(timezone.utc).isoformat(),
            "error_classification": error_classification,
            "error_detail": error_detail,
            "correction_prescribed": correction_prescribed,
            "correction_applied": False,
            "recurrence_count": escalation_level,
            "status": "active",
            "escalation_level": f"{escalation_level}_prescriptive" if escalation_level == 1 else (f"{escalation_level}_scar_linked" if escalation_level == 2 else "3_dominant_failure_mode")
        }
        self.scar_ledger.append(scar_entry)
        return scar_entry["scar_id"]

    def _evaluate_escalation(self, creator_id: str, error_classification: str) -> int:
        """
        Evaluates the recurrence of an error type for a specific creator to determine escalation level.
        """
        recurrences = sum(1 for scar in self.scar_ledger if scar["creator_id"] == creator_id and scar["error_classification"] == error_classification)
        return recurrences + 1

    def phase_1_audio_skeleton(self, creator_id: str, dead_air_gaps: list[float], hook_type: str) -> dict:
        """
        Phase 1: The Audio Skeleton.
        Validates Dead Air Quotient and Hook compliance.
        """
        max_gap = max(dead_air_gaps) if dead_air_gaps else 0.0
        if max_gap > 0.3:
            scar_id = self._ingest_scar(
                creator_id,
                "Dead_Air",
                f"Dead air gap of {max_gap}s detected.",
                f"Delete gap exceeding 0.3s. Found gap of {max_gap}s."
            )
            return {"status": "FAIL", "reason": "Dead air > 0.3s", "scar_id": scar_id}

        valid_hooks = ["curiosity_gap", "pain_point", "falsifiable_claim"]
        if hook_type not in valid_hooks:
            scar_id = self._ingest_scar(
                creator_id,
                "Identity_First_Error",
                f"Invalid hook type: {hook_type}.",
                "Rewrite opening. Use curiosity gap, pain point, or falsifiable claim. Do not use identity first."
            )
            return {"status": "FAIL", "reason": "Invalid hook audio structure", "scar_id": scar_id}

        return {"status": "PASS", "message": "Audio skeleton verified."}

    def phase_2_visual_thermodynamics(self, creator_id: str, total_cuts: int, duration_seconds: float, genre: str = "DEFAULT") -> dict:
        """
        Phase 2: Visual Thermodynamics.
        Calculates CPM and compares against genre floor.
        """
        cpm = (total_cuts / duration_seconds) * 60 if duration_seconds > 0 else 0

        genre_floors = {
            "Comedy/Entertainment": 18,
            "Tutorial/Education": 12,
            "Lifestyle/Vlog": 10,
            "Commentary/Talk": 8,
            "ASMR/Mindfulness": 2,
            "DEFAULT": 14
        }

        floor = genre_floors.get(genre, 14)

        if cpm < floor:
            scar_id = self._ingest_scar(
                creator_id,
                "Lethargic_B_Roll",
                f"CPM {cpm:.1f} is below genre floor {floor}.",
                f"Increase CPM to at least {floor}. Current CPM is {cpm:.1f}. Delete stagnant footage."
            )
            return {"status": "FAIL", "reason": "CPM below genre floor", "cpm": cpm, "floor": floor, "scar_id": scar_id}

        return {"status": "PASS", "message": "Visual structure verified.", "cpm": cpm}

    def phase_3_typographic_layer(self, creator_id: str, max_words_per_caption: int, safe_zone_compliant: bool) -> dict:
        """
        Phase 3: The Typographic Layer.
        Validates caption density and safe zone compliance.
        """
        if max_words_per_caption > 3:
            scar_id = self._ingest_scar(
                creator_id,
                "Caption_Overflow",
                f"Caption unit contains {max_words_per_caption} words.",
                "Manually break any 4+ word caption units. Max 3 words per caption."
            )
            return {"status": "FAIL", "reason": "Caption word limit exceeded", "scar_id": scar_id}

        if not safe_zone_compliant:
            scar_id = self._ingest_scar(
                creator_id,
                "Safe_Zone_Violation",
                "Text/graphic outside safe zone matrix.",
                "Reposition elements to sit within the universal safe box (880x1048px)."
            )
            return {"status": "FAIL", "reason": "Safe zone violation", "scar_id": scar_id}

        return {"status": "PASS", "message": "Typographic layer verified."}

    def phase_4_sonic_sculpting(self, creator_id: str, lufs_integrated: float, true_peak: float) -> dict:
        """
        Phase 4: Sonic Sculpting.
        Validates LUFS and True Peak compliance.
        """
        if not (-15.0 <= lufs_integrated <= -13.0):
            scar_id = self._ingest_scar(
                creator_id,
                "LUFS_Non_Compliance",
                f"LUFS Integrated is {lufs_integrated}.",
                "Apply Master Bus specification: Target -14 LUFS."
            )
            return {"status": "FAIL", "reason": "LUFS non-compliant", "scar_id": scar_id}

        if true_peak > -1.0:
            scar_id = self._ingest_scar(
                creator_id,
                "LUFS_Non_Compliance",
                f"True peak is {true_peak} dBTP.",
                "Apply limiter: True Peak ceiling -1.0 dBTP."
            )
            return {"status": "FAIL", "reason": "True Peak exceeded", "scar_id": scar_id}

        return {"status": "PASS", "message": "Sonic parameters verified."}

    def phase_5_export_audit(self, creator_id: str, checklist: dict) -> dict:
        """
        Phase 5: Export Audit.
        Validates final export parameters.
        checklist expected keys: aspect_ratio_9_16, codec_h264_or_h265, color_space_rec709, first_3s_interrupt
        """
        failures = []
        if not checklist.get("aspect_ratio_9_16", False):
            failures.append("Aspect Ratio must be 9:16")
        if not checklist.get("codec_h264_or_h265", False):
            failures.append("Codec must be H.264 or H.265")
        if not checklist.get("color_space_rec709", False):
            failures.append("Color space must be Rec.709")
        if not checklist.get("first_3s_interrupt", False):
            failures.append("Hook pattern interrupt missing in first 1.5s")

        if failures:
            scar_id = self._ingest_scar(
                creator_id,
                "Hook_Latency" if not checklist.get("first_3s_interrupt", False) else "Export_Artifact",
                f"Export audit failed: {', '.join(failures)}.",
                "Correct export parameters and re-audit."
            )
            return {"status": "FAIL", "reason": "Export audit failed", "failures": failures, "scar_id": scar_id}

        return {"status": "PASS", "message": "APPROVED FOR UPLOAD."}

    def generate_deliverable_b_audio_spec(self, creator_name: str, session: int, nle: str, platforms: list, peak: float, lufs: float, true_peak: float, dialogue_clarity: str) -> str:
        """
        Generates Deliverable Class B — Audio Mastering Specification Sheet.
        """
        spec = f"""AUDIO MASTERING SPEC — {creator_name} — Session {session}
NLE: {nle}
Target Platforms: {', '.join(platforms)}
=====================================================

DIAGNOSTIC READINGS:
  Current Peak Level:       {peak} dBFS
  Current LUFS Integrated:  {lufs} LUFS
  True Peak:                {true_peak} dBTP
  Dialogue clarity on phone: {dialogue_clarity}

PRESCRIBED CORRECTIONS:

STEP 1 — VOCAL CHAIN (Apply in order):
  [ ] Noise Gate: Threshold -40dB, Attack 5ms, Release 80ms
  [ ] De-Esser: Frequency 7.5kHz, Reduction -4dB
  [ ] EQ: High-Pass 85Hz, Presence +2dB at 3kHz
  [ ] Compressor: Ratio 3:1, Attack 10ms, Release 60ms, Threshold -18dB
  [ ] Limiter: Ceiling -3dBFS

STEP 2 — MUSIC/SFX BUS:
  [ ] Sidechain compression triggered by vocal bus (Threshold -20dB, Ratio 4:1)
  [ ] EQ on music: Low-shelf cut -3dB at 250Hz

STEP 3 — MASTER BUS:
  [ ] Integrated Loudness target: -14 LUFS
  [ ] True Peak ceiling: -1.0 dBTP
  [ ] Final limiter: Ceiling -0.5dBFS, Lookahead 2ms

SPEC COMPLIANCE: {'PASS' if (-15 <= lufs <= -13 and true_peak <= -1.0) else 'FAIL'}
====================================================="""
        return spec
