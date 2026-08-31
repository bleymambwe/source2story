# Reproduction guide

Written for someone starting from a clean environment with no prior context on this repo.

## Requirements

- Python 3.12 (tested with 3.12.6)
- Node.js 18+ / npm (for the Remotion render step)
- An LLM backend — pick one, no code change needed either way:
  - **Default, free, no API key:** [Ollama](https://ollama.com) running locally, serving
    `qwen3:7b`. Chosen after a quick survey of small open-source models on
    function-calling/structured-output reliability — see `src/llm.py` for the reasoning.
    micro1 does not provide API keys or credits, so this is also what makes the eval
    reproducible by a judge at zero cost.
  - **Higher quality, paid:** Anthropic (`S2S_PROVIDER=anthropic` + `ANTHROPIC_API_KEY`) or
    any OpenAI-compatible endpoint (`OPENAI_BASE_URL` + `OPENAI_API_KEY`, e.g. OpenAI
    itself, Together, Groq, vLLM).

Approximate cost and runtime per case: free / local with the default Ollama backend;
_paid-provider numbers to be filled in after a run against `eval/results/summary.md`._

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Option A — default: local open-source model via Ollama (free, no key)

```bash
# install Ollama (https://ollama.com/download), then:
ollama pull qwen3:7b
ollama serve   # if not already running as a background service
# nothing else to set — src/llm.py defaults to http://localhost:11434/v1
```

### Option B — Anthropic

```bash
export S2S_PROVIDER=anthropic
export ANTHROPIC_API_KEY=sk-...   # Windows (PowerShell): $env:ANTHROPIC_API_KEY = "sk-..."
# optional: export S2S_MODEL=claude-sonnet-4-5
```

### Option C — any other OpenAI-compatible endpoint

```bash
export OPENAI_BASE_URL=https://api.openai.com/v1   # or Together/Groq/vLLM/etc.
export OPENAI_API_KEY=sk-...
export S2S_MODEL=gpt-4o-mini   # or whatever model that endpoint serves
```

## Run the baseline alone

```bash
python -c "
from src.baseline import BaselineAgent
text = open('eval/cases/<case_id>.txt', encoding='utf-8').read()
script = BaselineAgent().run('<case_id>', text)
print(script.model_dump_json(indent=2))
"
```

## Run the agent solution alone

```bash
python -c "
from src.pipeline import run_agent_pipeline
text = open('eval/cases/<case_id>.txt', encoding='utf-8').read()
ledger, verified = run_agent_pipeline('<case_id>', text)
print(verified.model_dump_json(indent=2))
"
```

Every LLM call from either path is logged to `trajectories/` as it runs (deliverable #4) —
one JSON file per call, with the system prompt, input, raw response, token usage and
duration.

## Run the full evaluation (baseline + agent, same cases, same metric)

```bash
python eval/run_eval.py
```

Writes `eval/results/summary.json` (per-case detail) and `eval/results/summary.md` (the
baseline-vs-agent table from the brief's own format). Expected output: a table showing
source-grounded claim accuracy for both, plus how many scenes the verification agent
blocked before render.

## Data

Eval cases live in `eval/cases/*.txt` — plain text source documents. All cases used for
this submission are public or synthetic (Ground Rule 07: no private data).

## Known gaps at this point in the build

See `docs/architecture.md` §6 for what's intentionally out of scope for the MVP, and
`CHANGELOG.md` for what's actually been run so far.
