# Reproduction guide

Written for someone starting from a clean environment with no prior context on this repo.

## Requirements

- Python 3.12 (tested with 3.12.6)
- An Anthropic API key with access to `claude-sonnet-4-5` (or set `S2S_MODEL` to another
  Claude model you have access to)
- Node.js 18+ / npm (only needed once the Remotion render step is wired up — see status note
  in `docs/architecture.md`)

Approximate cost and runtime per case: _to be filled in after the first real eval run —
see `eval/results/summary.md`._

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

export ANTHROPIC_API_KEY=sk-...  # Windows (PowerShell): $env:ANTHROPIC_API_KEY = "sk-..."
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
