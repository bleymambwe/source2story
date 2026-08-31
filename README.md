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

Scaffolding in progress — this README will be filled in with real results as the pipeline
is built. See [`CHANGELOG.md`](CHANGELOG.md) for the improvement changelog (baseline →
final) and [`REPRODUCE.md`](REPRODUCE.md) for how to run it from a clean environment.

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
