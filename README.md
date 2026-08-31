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
renderer are complete and real (see `CHANGELOG.md`). A full live LLM run over the whole
eval set was not completed before the deadline — no `ANTHROPIC_API_KEY` was available in
the build environment during the build window. What *is* real and verified without any LLM
call: the Verification Agent's programmatic conflict/unsupported-claim detection, tested
against `eval/cases/revenue_conflict.txt` and visible directly in the rendered sample video
at `src/render/out/agent_sample.mp4` (compare against `baseline_sample.mp4`, same input).
See `CHANGELOG.md` for the exact state and `REPRODUCE.md` to run the live LLM path yourself.

## Coding-agent disclosure

This solution was built using Claude Code (Anthropic, Sonnet 5) as the coding agent, per
the challenge's disclosure requirement. The runtime agents inside Source2Story itself
(Claim Extraction, Script/Storyboard, Verification) are a separate system, built by Claude
Code, that runs on the Anthropic API at inference time.

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
