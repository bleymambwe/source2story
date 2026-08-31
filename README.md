# Source2Story

**An agentic workflow that turns a source document into a source-grounded explainer video** —
built for the micro1 Agentic Workflows Hackathon.

## Who this is for

People who have to **stand behind what they show**:

- **Teachers** turning a textbook chapter, paper, or report into a 90-second explainer for
  a lesson — and who are accountable to a room of students and their parents for every
  number on screen.
- **Students** building study aids or presentations from their own course readings, where a
  hallucinated statistic doesn't just look bad, it teaches them something false.
- **Creators** making knowledge-heavy explainers — economics, science, policy — whose
  credibility is the entire product.

## The bottleneck

The reason AI video hasn't landed in classrooms isn't that the videos look bad. **It's that
nobody can vouch for them.**

Turning a dense source into a short, accurate video already eats hours: research,
fact-checking, scripting, scene planning, editing. Generic AI video tools appear to collapse
that to minutes — but they generate confident-sounding claims and visuals that aren't
actually tied to the source. So the human re-checks every line by hand before they dare show
it to anyone, which costs *more* time than writing the script themselves. The tool that was
supposed to save time added a verification chore instead.

A teacher can't show a class a figure that might be wrong. A student can't cite it. That
accountability gap — not visual quality — is what keeps these tools out of the places that
would benefit most.

## What this solves

Given a source document, produce a short explainer video where every factual statement and
every data visual is traceable to a specific place in the source — and anything that can't
be verified is **visibly flagged instead of silently rendered**.

### A blocked scene is a finding, not a failure

The adversarial eval case (`eval/cases/revenue_conflict.txt`) states +24% growth on page 3
and +17% for the same quarter on page 37. The baseline picks one and sounds certain.
Source2Story refuses to render either, and says why, on screen.

For a teacher, **that blocked scene is the lesson**: here is exactly where this source
contradicts itself. The verification layer doubles as source criticism — it hands back a map
of where the material is unreliable, which is the thing a student most needs to learn to see
and the thing a rushed reader most often misses.

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
