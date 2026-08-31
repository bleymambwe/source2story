# Source2Story — Solution Design

## 1. Who has this problem, and what's the bottleneck

**User:** a solo or small-team creator making knowledge-heavy explainer videos
(economics, tech, science, business, policy) from a written source — a report,
paper, article, or dataset. Think Vox/Cleo Abram-style shorts, not vlogs.

**Bottleneck:** turning a dense source into a short, accurate, well-paced video
eats hours of research, fact-checking, scripting, scene planning, and editing.
Generic AI video tools make this *worse*, not better, because they generate
confident-sounding claims and visuals that aren't actually tied to the source —
the creator still has to fact-check the AI's output line by line, which can
cost more time than writing it themselves.

**What "solved" looks like:** given a source document, produce a short
narrated video where every factual statement and every data visual is
traceable to a specific place in the source — and where anything that
*can't* be verified is flagged instead of rendered, rather than the creator
finding out after publishing.

## 2. Baseline (Ground Rules require this to be fair and simple)

One direct prompt to a general-purpose LLM with basic tools:

> "Read this source document and write a ~90 second explainer video script:
> a scene list with narration text and a one-line visual description per
> scene."

The baseline's output is rendered through the *same* Remotion pipeline as the
agent solution (same fonts, same transitions, same TTS voice) so the
comparison isolates the difference agents make, not production values.
No verification step, no claim ledger, no conflict detection.

## 3. Agent solution — three purposeful agents, not six

The original brainstorm (research/story/script/visual-director/composer/critic)
was cut down. Rubric criterion 2 explicitly rewards *purposeful* design over
component count, and every extra agent is another point of failure inside a
short build window. What's kept:

```
SOURCE DOCUMENT
      │
      ▼
┌─────────────────────┐
│ 1. Claim Extraction  │  reads the source, produces a claim ledger:
│    Agent             │  {claim_id, text, value, unit, source_location}
└──────────┬───────────┘
           │ claim ledger
           ▼
┌─────────────────────┐
│ 2. Script/Storyboard │  writes narration + scene list; every factual
│    Agent             │  line is tagged with the claim_id it rests on
└──────────┬───────────┘
           │ draft script (scenes, each tagged)
           ▼
┌─────────────────────┐
│ 3. Verification      │  checks each tagged line against the claim
│    Agent             │  ledger and the raw source text:
└──────────┬───────────┘  - unsupported claim → block scene, flag
           │               - numeric/unit mismatch → block scene, flag
           │               - two source passages disagree → block,
  verified script          surface the conflict instead of picking one
           ▼
┌─────────────────────┐
│ Video Composer        │  deterministic, not an "agent": TTS narration +
│ (Remotion)             │  programmatic charts from the *extracted* numbers
└──────────┬───────────┘  + kinetic typography + a few illustrative stills
           ▼
     FINAL VIDEO (+ a flagged-scenes report if anything was blocked)
```

Why this maps to the brief's "how agents can help" list:
- **Context/tools:** the claim ledger is better context handed forward, not
  regenerated from scratch at each stage.
- **Verification:** the whole point of agent 3 — catches errors before they
  reach the user, which the brief calls out by name.
- **Orchestration:** a simple linear pipeline (script → verify → render),
  not a framework for its own sake.
- **Memory / skills:** deliberately **not** used in the MVP (no cross-video
  creator-memory, no specialized retrieval skill). Cutting them is itself a
  documented decision in the changelog, not an oversight.

### Why Remotion for rendering, not a text-to-video model

Full generative video (Sora-style) is hard to make source-grounded, hard to
make deterministic, and hard for a judge to reproduce cheaply. Remotion
renders locally from a script + asset JSON: same input always produces the
same output, no flaky third-party video-gen API in the reproduction path.
Visual truth is enforced by construction — a chart scene is only allowed to
show numbers that came from the claim ledger.

## 4. Evaluation

**Primary metric — source-grounded claim accuracy:**
`supported factual claims / total factual claims in the rendered script`,
scored by checking each tagged claim against the source text.

**Secondary metrics (brief's own table format):**

| Metric | Simple baseline | Agent solution | Change |
|---|---|---|---|
| Source-grounded claim accuracy | [value] | [value] | [change] |
| Human time per task (est. review/fix minutes) | [value] | [value] | [change] |
| Cost per task | [value] | [value] | [change] |

**Cases:** aim for 10 source documents (public/synthetic per Ground Rule 07).
One is deliberately adversarial: two passages in the same document give
different figures for the same fact (e.g. a revenue restatement). The
baseline is expected to silently pick one; the agent solution is expected to
flag the conflict and hold that scene rather than render an unverified
number. This is the anchor for the Hot Take.

## 5. Ground rules checklist (from the brief)

- Sandbox/human approval: rendering only proceeds on **verified** scenes;
  flagged scenes stop for human review instead of auto-resolving. This is
  the "consequential action → human checkpoint" control for this project.
- Data: source documents for eval are public or synthetic — no private data.
- Every claim in the changelog/report must cite the eval evidence that
  produced it (results table + saved trajectories), not a vibe.

## 5a. Render implementation (built)

`src/render/` is a Remotion (TypeScript) project. Composition `Explainer` takes a
`{title, scenes[]}` JSON prop (the same shape as `Script`/`VerifiedScript` from the Python
pipeline) and renders it deterministically:

- `factual_chart` scenes animate the scene's own `value`/`unit` — there is no code path by
  which this component can display a number it wasn't handed, which is the "visual truth"
  property enforced by construction rather than by prompting.
- `kinetic_type` / `transition` scenes render styled on-screen typography.
- `illustrative` scenes render a stylised, explicitly-labelled "ILLUSTRATIVE" placeholder
  panel rather than a photorealistic image, so a generated visual can never be mistaken for
  archival/factual footage (see Ground Rule 06).
- Any scene whose verification `status` isn't `verified` is wrapped in a blur/greyscale
  `FlaggedOverlay` with the block reason on screen, instead of being silently rendered —
  this is the "verification catches errors before they reach the user" idea made visible in
  the actual output, not just logged to a file.
- Narration is shown as animated captions rather than synthesized audio for now — adding
  real TTS is one more external API dependency, and no TTS key is available yet. Noted as a
  gap, not hidden.

Sample props for both a naive baseline render and a verified agent render (hand-authored
from the `revenue_conflict` eval case, matching the Verification Agent's actual tested
output) live in `src/render/sample-data/`.

## 6. What's explicitly out of scope for the MVP (candidates for "discarded experiment" writeup)

- Six-agent studio (Research/Story/Visual-Director/Composer/Critic split) —
  replaced by 3 agents + a deterministic renderer.
- Per-scene AI-generated photorealistic B-roll for every shot — replaced by
  programmatic charts/typography, with AI stills reserved for a few
  explicitly "illustrative" (non-factual) scenes only.
- Cross-video creator memory — real idea, cut for time; noted as future work.
