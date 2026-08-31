"""Provider-agnostic LLM client shared by every agent.

Centralized so trajectory logging (hackathon deliverable #4) happens in one
place instead of being bolted onto each agent separately, and so the whole
pipeline can swap models with an environment variable instead of a code
change.

Why an open-source model is the default, not Anthropic: the rules state
"micro1 does not provide API keys or model credits — participants must use
their own agent setup." That cuts both ways — it also means a judge
reproducing this project has no free Anthropic credits either. Defaulting to
a small open-source model served locally through Ollama (OpenAI-compatible
API, no key, no cost) means `python eval/run_eval.py` works on a clean
machine with nothing but `ollama pull <model>` — no one has to pay to
reproduce the main result. Anthropic/OpenAI hosted models stay one env var
away for anyone who wants higher quality and is willing to pay for it.

Model choice: Qwen3 7B, chosen after a quick survey of small open-source
models on function-calling / structured-output reliability (2026). Smaller
models (1-3B) emit malformed or wrong-tool function calls often enough to be
a liability for a verification pipeline that has to parse strict JSON on
every call; Qwen3 7B is close to the smallest size that stays reliable at
that, while still running on an 8GB-VRAM machine via Ollama.

Swap providers/models with env vars, no code change:
    S2S_PROVIDER=openai|anthropic          (default: openai)
    S2S_MODEL=<model name>                 (default depends on provider)
    OPENAI_BASE_URL=<url>                  (default: local Ollama, http://localhost:11434/v1)
    OPENAI_API_KEY=<key>                   (default: dummy value; Ollama ignores it)
    ANTHROPIC_API_KEY=<key>                (required only when S2S_PROVIDER=anthropic)
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any, Protocol

PROVIDER = os.environ.get("S2S_PROVIDER", "openai")
TRAJECTORY_DIR = Path(__file__).resolve().parent.parent / "trajectories"

DEFAULT_MODELS = {
    "openai": "qwen3:7b",  # served locally via `ollama pull qwen3:7b` / `ollama serve`
    "anthropic": "claude-sonnet-4-5",
}
DEFAULT_OPENAI_BASE_URL = "http://localhost:11434/v1"  # Ollama's OpenAI-compatible endpoint


class _Backend(Protocol):
    def complete(self, system: str, user: str, max_tokens: int) -> tuple[str, dict]: ...


class _AnthropicBackend:
    def __init__(self, model: str) -> None:
        import anthropic  # local import: only required for this provider

        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError(
                "S2S_PROVIDER=anthropic requires ANTHROPIC_API_KEY. "
                "Unset S2S_PROVIDER to use the free local open-source default instead."
            )
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def complete(self, system: str, user: str, max_tokens: int) -> tuple[str, dict]:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        text = "".join(block.text for block in response.content if block.type == "text")
        usage = response.usage.model_dump() if response.usage else {}
        return text, usage


class _OpenAICompatBackend:
    """Works for OpenAI itself, and for any OpenAI-compatible server:
    Ollama (default), vLLM, LM Studio, Together, Groq, etc. — just change
    OPENAI_BASE_URL."""

    def __init__(self, model: str) -> None:
        import openai  # local import: only required for this provider

        base_url = os.environ.get("OPENAI_BASE_URL", DEFAULT_OPENAI_BASE_URL)
        api_key = os.environ.get("OPENAI_API_KEY", "ollama")  # Ollama ignores the key
        self.client = openai.OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        self.base_url = base_url

    def complete(self, system: str, user: str, max_tokens: int) -> tuple[str, dict]:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
            )
        except Exception as exc:
            raise RuntimeError(
                f"Could not reach an OpenAI-compatible model at {self.base_url} "
                f"(model={self.model}). If using the local default: install Ollama, run "
                f"`ollama pull {self.model}`, and make sure `ollama serve` is running. "
                f"Original error: {exc}"
            ) from exc
        text = response.choices[0].message.content or ""
        usage = response.usage.model_dump() if response.usage else {}
        return text, usage


def _make_backend(provider: str, model: str) -> _Backend:
    if provider == "anthropic":
        return _AnthropicBackend(model)
    if provider == "openai":
        return _OpenAICompatBackend(model)
    raise ValueError(f"Unknown S2S_PROVIDER={provider!r}; expected 'openai' or 'anthropic'")


class LLMClient:
    def __init__(self, model: str | None = None, provider: str | None = None) -> None:
        self.provider = provider or PROVIDER
        self.model = model or os.environ.get("S2S_MODEL") or DEFAULT_MODELS[self.provider]
        self._backend = _make_backend(self.provider, self.model)

    def call(
        self,
        agent_name: str,
        system: str,
        user: str,
        max_tokens: int = 4096,
    ) -> str:
        """Single-turn call. Logs the full trajectory for deliverable #4."""
        started = time.time()
        text, usage = self._backend.complete(system, user, max_tokens)
        self._log_trajectory(
            agent_name=agent_name,
            system=system,
            user=user,
            response_text=text,
            usage=usage,
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
        not use provider-specific structured-output/tool-schema features on
        purpose, so the same prompt works unmodified across providers and the
        trajectory log stays readable end-to-end for the judges.
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
            "provider": self.provider,
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
