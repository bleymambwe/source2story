"""Agent 2: Script / Storyboard.

Turns a ClaimLedger into a scene-by-scene explainer script. Every scene whose
narration states a fact must tag the claim_id(s) it rests on — that tagging
is what makes the Verification Agent's job possible.
"""
from __future__ import annotations

from src.llm import LLMClient
from src.models import ClaimLedger, Script

SYSTEM_PROMPT = """You write short explainer video scripts from a claim ledger.

You will receive a list of claims, each with a claim_id, its text, and (if numeric) a value
and unit. Write a scene-by-scene script for a video of about {target_seconds} seconds
total, aimed at a general audience who has not read the source.

Rules:
- Every scene whose narration states a fact from the ledger must include that claim's
  claim_id in supporting_claim_ids. Do not invent claim_ids that were not given to you.
- A scene may also be purely narrative/transitional with no supporting_claim_ids — mark its
  visual_type as "kinetic_type" or "transition" in that case, never "factual_chart".
- visual_type must be one of: factual_chart, kinetic_type, illustrative, transition.
  Use factual_chart only when the visual shows a number that is in supporting_claim_ids.
  Use illustrative only for a stylised, clearly non-factual visual (never claim it depicts
  real footage or a real event).
- Do not state any number or fact that is not in the claim ledger.

Return ONLY a JSON object with this exact shape, no prose before or after:
{{
  "title": "...",
  "scenes": [
    {{"scene_id": "s1", "narration": "...", "visual_type": "...", "visual_prompt": "...",
      "supporting_claim_ids": ["c1"], "duration_s": 5}}
  ]
}}"""


class ScriptAgent:
    def __init__(self, llm: LLMClient | None = None) -> None:
        self.llm = llm or LLMClient()

    def run(self, ledger: ClaimLedger, target_seconds: int = 90) -> Script:
        claims_text = "\n".join(
            f"- {c.claim_id}: {c.text}"
            + (f" (value={c.value} {c.unit or ''})".strip() if c.value else "")
            for c in ledger.claims
        )
        data = self.llm.call_json(
            agent_name="script",
            system=SYSTEM_PROMPT.format(target_seconds=target_seconds),
            user=f"CLAIM LEDGER for document {ledger.document_id}:\n\n{claims_text}",
        )
        return Script(**data)
