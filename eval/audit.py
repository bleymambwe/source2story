"""Independent scoring for the primary metric: source-grounded claim accuracy.

Deliberately does NOT reuse the agent pipeline's own VerificationAgent
verdicts to score the agent's output — grading your own homework would bias
the comparison. Instead this is a separate, blind auditor that only sees the
rendered narration lines and the raw source text, and applies the same check
to the baseline and the agent so the comparison is fair.
"""
from __future__ import annotations

from dataclasses import dataclass

from src.llm import LLMClient
from src.models import Script

SYSTEM_PROMPT = """You are an independent fact-checking auditor. You are given a source
document and a list of narration lines from a video script derived from it. For each line,
decide:
  - is_factual: does this line assert a specific, checkable fact (a number, a named event,
    a dated claim, a stated cause-effect)? Purely narrative/transitional lines are not
    factual.
  - if is_factual, is it fully supported by the source document, with no invented numbers,
    no stronger claim than the source makes, and no resolution of an ambiguity the source
    itself leaves unresolved?

Return ONLY a JSON array, no prose before or after:
[{"scene_id": "s1", "is_factual": true, "supported": true, "detail": "..."}, ...]"""


@dataclass
class AuditResult:
    total_factual: int
    supported_factual: int
    per_scene: list[dict]

    @property
    def accuracy(self) -> float:
        return self.supported_factual / self.total_factual if self.total_factual else 1.0


def audit_script(source_text: str, script: Script, rendered_only_scene_ids=None) -> AuditResult:
    llm = LLMClient()
    scenes = script.scenes
    if rendered_only_scene_ids is not None:
        scenes = [s for s in scenes if s.scene_id in rendered_only_scene_ids]

    lines = "\n".join(f'{s.scene_id}: "{s.narration}"' for s in scenes)
    data = llm.call_json(
        agent_name="eval_audit",
        system=SYSTEM_PROMPT,
        user=f"SOURCE DOCUMENT:\n\n{source_text}\n\nSCRIPT LINES:\n\n{lines}",
    )
    total = sum(1 for item in data if item.get("is_factual"))
    supported = sum(1 for item in data if item.get("is_factual") and item.get("supported"))
    return AuditResult(total_factual=total, supported_factual=supported, per_scene=data)
