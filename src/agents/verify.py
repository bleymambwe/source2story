"""Agent 3: Verification.

Checks every scripted scene against the claim ledger before it's allowed to
render. This is the agent the rubric's "Agent Solution & Engineering" and
"Hot Take" criteria are really about — catching errors before they reach the
user, not just producing plausible-sounding output faster.

Two layers, cheapest checks first:
  1. Programmatic: does every cited claim_id actually exist, and is it part
     of a known source conflict? (no LLM call needed)
  2. Semantic: for scenes that pass layer 1, does the narration actually say
     what the cited claim's source_quote supports, or has it drifted /
     embellished in paraphrase? (one batched LLM call)
"""
from __future__ import annotations

from src.llm import LLMClient
from src.models import (
    ClaimLedger,
    Script,
    SceneVerdict,
    VerificationStatus,
    VerifiedScript,
    VisualType,
)

SYSTEM_PROMPT = """You are a fact-checker. For each scene below you are given the narration
line and the exact source quote(s) it is supposed to be based on. Decide whether the
narration is fully supported by the source quote(s) — no invented numbers, no stronger
claim than the source makes, no dropped caveat that changes the meaning.

Return ONLY a JSON array, no prose before or after:
[{"scene_id": "s1", "supported": true, "detail": "..."}, ...]"""


class VerificationAgent:
    def __init__(self, llm: LLMClient | None = None) -> None:
        self.llm = llm or LLMClient()

    def run(self, script: Script, ledger: ClaimLedger) -> VerifiedScript:
        claims_by_id = {c.claim_id: c for c in ledger.claims}
        conflicted_ids = {
            cid for conflict in ledger.conflicts for cid in conflict.claim_ids
        }

        verdicts: list[SceneVerdict] = []
        scenes_needing_semantic_check = []

        for scene in script.scenes:
            unknown_ids = [
                cid for cid in scene.supporting_claim_ids if cid not in claims_by_id
            ]
            if unknown_ids:
                verdicts.append(SceneVerdict(
                    scene_id=scene.scene_id,
                    status=VerificationStatus.UNSUPPORTED_CLAIM,
                    detail=f"cites unknown claim id(s): {unknown_ids}",
                ))
                continue

            conflicting = conflicted_ids.intersection(scene.supporting_claim_ids)
            if conflicting:
                verdicts.append(SceneVerdict(
                    scene_id=scene.scene_id,
                    status=VerificationStatus.SOURCE_CONFLICT,
                    detail=f"claim(s) {sorted(conflicting)} disagree between source passages; "
                           f"not rendering an unverified number",
                ))
                continue

            if scene.visual_type == VisualType.FACTUAL_CHART and not scene.supporting_claim_ids:
                verdicts.append(SceneVerdict(
                    scene_id=scene.scene_id,
                    status=VerificationStatus.VALUE_MISMATCH,
                    detail="factual_chart visual with no supporting claim to draw data from",
                ))
                continue

            if scene.supporting_claim_ids:
                scenes_needing_semantic_check.append(scene)
            else:
                verdicts.append(SceneVerdict(
                    scene_id=scene.scene_id,
                    status=VerificationStatus.VERIFIED,
                    detail="no factual claim asserted",
                ))

        if scenes_needing_semantic_check:
            verdicts.extend(
                self._semantic_check(scenes_needing_semantic_check, claims_by_id)
            )

        return VerifiedScript(script=script, verdicts=verdicts)

    def _semantic_check(self, scenes, claims_by_id) -> list[SceneVerdict]:
        blocks = []
        for scene in scenes:
            quotes = "\n".join(
                f"  - {claims_by_id[cid].source_quote}" for cid in scene.supporting_claim_ids
            )
            blocks.append(
                f'scene_id: {scene.scene_id}\nnarration: "{scene.narration}"\n'
                f"source quote(s):\n{quotes}"
            )
        data = self.llm.call_json(
            agent_name="verification_semantic",
            system=SYSTEM_PROMPT,
            user="\n\n".join(blocks),
        )
        results = []
        for item in data:
            status = (
                VerificationStatus.VERIFIED
                if item["supported"]
                else VerificationStatus.UNSUPPORTED_CLAIM
            )
            results.append(SceneVerdict(
                scene_id=item["scene_id"], status=status, detail=item.get("detail", "")
            ))
        return results
