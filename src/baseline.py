"""Baseline: one direct prompt, no claim ledger, no verification.

This is the "reasonable basic way to handle the task" the brief asks for —
a general-purpose approach with basic instructions, rendered through the
exact same Remotion pipeline as the agent solution so the comparison isolates
what the agent architecture contributes, not production values.
"""
from __future__ import annotations

from src.llm import LLMClient
from src.models import Script

SYSTEM_PROMPT = """Read the source document and write a short explainer video script of
about {target_seconds} seconds: a scene list with a narration line and a one-line visual
description per scene.

Return ONLY a JSON object with this exact shape, no prose before or after:
{{
  "title": "...",
  "scenes": [
    {{"scene_id": "s1", "narration": "...", "visual_type": "kinetic_type",
      "visual_prompt": "...", "supporting_claim_ids": [], "duration_s": 5}}
  ]
}}"""


class BaselineAgent:
    """Named 'Agent' loosely for symmetry with the pipeline — it is in fact a
    single unstructured prompt, which is the point of the comparison."""

    def __init__(self, llm: LLMClient | None = None) -> None:
        self.llm = llm or LLMClient()

    def run(self, document_id: str, source_text: str, target_seconds: int = 90) -> Script:
        data = self.llm.call_json(
            agent_name="baseline",
            system=SYSTEM_PROMPT.format(target_seconds=target_seconds),
            user=f"SOURCE DOCUMENT (id={document_id}):\n\n{source_text}",
        )
        return Script(**data)
