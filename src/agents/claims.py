"""Agent 1: Claim Extraction.

Reads the raw source document and produces a ClaimLedger: every factual,
checkable assertion, tied to where in the source it came from. This ledger
is the context every later stage works from instead of re-reading prose.
"""
from __future__ import annotations

from src.llm import LLMClient
from src.models import Claim, ClaimConflict, ClaimLedger

SYSTEM_PROMPT = """You extract factual, checkable claims from a source document for a
fact-checking pipeline. A claim is a specific assertion a reader could verify against the
source — a statistic, a named event, a dated fact, a stated cause-effect relationship.
Do not extract opinions, predictions framed as opinion, or vague statements.

For every claim, quote the exact source sentence(s) it rests on (source_quote) and give its
approximate location (source_location), e.g. "p.3, para 2" or a section heading if pages
aren't marked.

Separately, identify conflicts: places where two passages in the SAME document state
different values for what is presented as the same fact (e.g. two different revenue growth
percentages for the same period). List the claim_ids involved and describe the discrepancy.

Return ONLY a JSON object with this exact shape, no prose before or after:
{
  "claims": [
    {"claim_id": "c1", "text": "...", "value": "..." or null, "unit": "..." or null,
     "source_location": "...", "source_quote": "..."}
  ],
  "conflicts": [
    {"claim_ids": ["c1", "c4"], "description": "..."}
  ]
}"""


class ClaimExtractionAgent:
    def __init__(self, llm: LLMClient | None = None) -> None:
        self.llm = llm or LLMClient()

    def run(self, document_id: str, source_text: str) -> ClaimLedger:
        data = self.llm.call_json(
            agent_name="claim_extraction",
            system=SYSTEM_PROMPT,
            user=f"SOURCE DOCUMENT (id={document_id}):\n\n{source_text}",
        )
        claims = [Claim(**c) for c in data.get("claims", [])]
        conflicts = [ClaimConflict(**c) for c in data.get("conflicts", [])]
        return ClaimLedger(document_id=document_id, claims=claims, conflicts=conflicts)
