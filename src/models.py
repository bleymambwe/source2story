"""Shared data structures passed between pipeline stages.

Kept in one place because the whole point of the agent solution (vs. the
baseline) is that later stages get *structured* context from earlier ones —
a claim ledger, not a wall of prose re-read from scratch each time.
"""
from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Claim(BaseModel):
    """One factual assertion extracted from the source document."""

    claim_id: str
    text: str
    value: Optional[str] = None  # e.g. "820000" for a numeric claim
    unit: Optional[str] = None  # e.g. "tonnes"
    source_location: str  # e.g. "p.17, para 3" or a quoted anchor string
    source_quote: str  # the exact source sentence(s) this claim rests on


class ClaimLedger(BaseModel):
    document_id: str
    claims: list[Claim]
    conflicts: list["ClaimConflict"] = Field(default_factory=list)


class ClaimConflict(BaseModel):
    """Two source passages disagree about the same fact."""

    claim_ids: list[str]
    description: str


class VisualType(str, Enum):
    FACTUAL_CHART = "factual_chart"       # numbers must come from a Claim
    KINETIC_TYPE = "kinetic_type"          # on-screen text, no factual load
    ILLUSTRATIVE = "illustrative"          # AI-generated still, clearly non-factual
    TRANSITION = "transition"


class Scene(BaseModel):
    scene_id: str
    narration: str
    visual_type: VisualType
    visual_prompt: str
    supporting_claim_ids: list[str] = Field(default_factory=list)
    duration_s: float = 5.0


class VerificationStatus(str, Enum):
    VERIFIED = "verified"
    UNSUPPORTED_CLAIM = "unsupported_claim"
    VALUE_MISMATCH = "value_mismatch"
    SOURCE_CONFLICT = "source_conflict"


class SceneVerdict(BaseModel):
    scene_id: str
    status: VerificationStatus
    detail: str


class Script(BaseModel):
    title: str
    scenes: list[Scene]


class VerifiedScript(BaseModel):
    script: Script
    verdicts: list[SceneVerdict]

    @property
    def blocked_scene_ids(self) -> list[str]:
        return [v.scene_id for v in self.verdicts if v.status != VerificationStatus.VERIFIED]

    @property
    def renderable_scenes(self) -> list[Scene]:
        blocked = set(self.blocked_scene_ids)
        return [s for s in self.script.scenes if s.scene_id not in blocked]
