"""Thin wrapper around the Anthropic API, shared by every agent.

Centralized so trajectory logging (hackathon deliverable #4) happens in one
place instead of being bolted onto each agent separately.
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any

import anthropic

DEFAULT_MODEL = os.environ.get("S2S_MODEL", "claude-sonnet-4-5")
TRAJECTORY_DIR = Path(__file__).resolve().parent.parent / "trajectories"


class LLMClient:
    def __init__(self, model: str = DEFAULT_MODEL) -> None:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY is not set. See REPRODUCE.md for setup."
            )
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def call(
        self,
        agent_name: str,
        system: str,
        user: str,
        max_tokens: int = 4096,
    ) -> str:
        """Single-turn call. Logs the full trajectory for deliverable #4."""
        started = time.time()
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        text = "".join(
            block.text for block in response.content if block.type == "text"
        )
        self._log_trajectory(
            agent_name=agent_name,
            system=system,
            user=user,
            response_text=text,
            usage=response.usage.model_dump() if response.usage else {},
            duration_s=time.time() - started,
        )
        return text

    def call_json(
        self,
        agent_name: str,
        system: str,
        user: str,
        max_tokens: int = 4096,
    ) -> Any:
        """Call the model and parse a JSON object/array out of the reply.

        Prompts must instruct the model to return raw JSON only. This does
        not use tool-use forced schemas on purpose, to keep the trajectory
        log readable end-to-end for the judges (deliverable #4).
        """
        text = self.call(agent_name, system, user, max_tokens=max_tokens)
        return _extract_json(text)

    def _log_trajectory(
        self,
        agent_name: str,
        system: str,
        user: str,
        response_text: str,
        usage: dict,
        duration_s: float,
    ) -> None:
        TRAJECTORY_DIR.mkdir(parents=True, exist_ok=True)
        record = {
            "agent": agent_name,
            "model": self.model,
            "system_prompt": system,
            "user_input": user,
            "response": response_text,
            "usage": usage,
            "duration_s": round(duration_s, 2),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        }
        out_path = TRAJECTORY_DIR / f"{agent_name}_{int(time.time() * 1000)}.json"
        out_path.write_text(json.dumps(record, indent=2), encoding="utf-8")


def _extract_json(text: str) -> Any:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```", 2)[1]
        if text.startswith("json"):
            text = text[len("json"):]
    return json.loads(text.strip())
