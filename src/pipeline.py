"""Orchestration: source document -> verified, render-ready script.

Deliberately a plain linear pipeline, not a framework — the brief rewards
purposeful orchestration, not orchestration for its own sake, and three
sequential stages don't need a graph engine.
"""
from __future__ import annotations

from src.agents.claims import ClaimExtractionAgent
from src.agents.script import ScriptAgent
from src.agents.verify import VerificationAgent
from src.llm import LLMClient
from src.models import ClaimLedger, VerifiedScript


def run_agent_pipeline(
    document_id: str, source_text: str, target_seconds: int = 90
) -> tuple[ClaimLedger, VerifiedScript]:
    llm = LLMClient()
    ledger = ClaimExtractionAgent(llm).run(document_id, source_text)
    script = ScriptAgent(llm).run(ledger, target_seconds=target_seconds)
    verified = VerificationAgent(llm).run(script, ledger)
    return ledger, verified
