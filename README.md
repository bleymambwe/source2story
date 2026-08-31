# Source2Story

**An agentic workflow that turns a source document into a source-grounded explainer video** —
built for the micro1 Agentic Workflows Hackathon.

## Who this is for

Solo and small-team creators making knowledge-heavy explainer videos — economics, tech,
science, business, policy — from a written source (a report, paper, article, or dataset).

## The bottleneck

Turning a dense source into a short, accurate, well-paced video eats hours: research,
fact-checking, scripting, scene planning, and editing. Generic AI video tools make this
*worse*, because they generate confident-sounding claims and visuals that aren't actually
tied to the source — the creator ends up fact-checking the AI's output line by line, which
can cost more time than writing it from scratch.

## What this solves

Given a source document, produce a short narrated video where every factual statement and
every data visual is traceable to a specific place in the source — and anything that can't
be verified is flagged instead of rendered, rather than the creator finding out after
publishing.

Full design, rubric mapping, and what was deliberately cut for time: [`docs/architecture.md`](docs/architecture.md).

## Status

Built against the hackathon deadline. The agent pipeline, eval harness, and Remotion
renderer are complete and real (see `CHANGELOG.md`). What *is* real and verified without
any LLM call: the Verification Agent's programmatic conflict/unsupported-claim detection,
tested against `eval/cases/revenue_conflict.txt` and visible directly in the rendered
sample video at `src/render/out/agent_sample.mp4` (compare against `baseline_sample.mp4`,
same input). See `CHANGELOG.md` for the exact state and `REPRODUCE.md` for how to run the
live pipeline yourself.

## Model configuration

`src/llm.py` is provider-agnostic — swap the LLM backend with an environment variable, no
code change:

| | Default | Alternative |
|---|---|---|
| Provider | `openai`-compatible, pointed at local **Ollama** | `S2S_PROVIDER=anthropic`, or any other OpenAI-compatible endpoint via `OPENAI_BASE_URL` |
| Model | `qwen3:7b` (free, runs locally, no API key) | any Claude/GPT/open model you have access to |

Why open-source-by-default: the rules state micro1 does not provide API keys or model
credits, which means a judge reproducing this project has none either. A free local model
means `python eval/run_eval.py` works on a clean machine with nothing but
`ollama pull qwen3:7b` — see `docs/architecture.md` for the model-selection reasoning and
`REPRODUCE.md` for exact setup of all three options.

## Coding-agent disclosure

This solution was built using Claude Code (Anthropic, Sonnet 5) as the coding agent, per
the challenge's disclosure requirement. The runtime agents inside Source2Story itself
(Claim Extraction, Script/Storyboard, Verification) are a separate system, built by Claude
Code, that runs at inference time on whichever model backend is configured (open-source by
default — see "Model configuration" above).

## Repository layout

```
docs/architecture.md   full solution design, rubric mapping, scope decisions
src/agents/            claim extraction, script/storyboard, verification agents
src/render/            Remotion project that composes the verified script into video
eval/cases/            source documents used for evaluation (public/synthetic)
eval/results/          baseline vs. agent evaluation output
trajectories/          saved agent run logs (deliverable #4)
CHANGELOG.md           improvement changelog, baseline through final
REPRODUCE.md           reproduction guide for a clean environment
```
