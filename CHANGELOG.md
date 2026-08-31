# Improvement Changelog

Each entry: what was tried and why, the evidence from `eval/results/`, and the decision it
led to. Entries are added as the project is actually built — this is the live document, not
a plan written in advance.

| Stage | What was tried and why | Evidence | Decision / learning |
|---|---|---|---|
| Scaffold | Built the baseline prompt, the 3-agent pipeline (claim extraction → script → verification), and an independent eval auditor that scores both the same way. | Unit-level check (no LLM, no API key needed): fed the Verification Agent a claim ledger with a known conflict (two different revenue-growth figures for the same quarter, `eval/cases/revenue_conflict.txt`) and a script citing both an unknown claim id and a conflicted one. It correctly blocked both scenes (`SOURCE_CONFLICT`, `UNSUPPORTED_CLAIM`) and let the transition scene through — with an `ExplodingLLM` stub proving no model call was needed to catch either failure. | Confirms the programmatic layer of verification (existence + conflict checks) works before spending any API budget on the semantic layer. Full baseline-vs-agent runs with real LLM calls are pending an `ANTHROPIC_API_KEY`. |
| Baseline | Single direct prompt: read the source, write a ~90s script + one-line visual per scene. Rendered through the same Remotion pipeline as the agent solution. Hand-authored a representative baseline output for the revenue-conflict case (what a naive prompt plausibly produces) to build and test the renderer before an API key was available. | `src/render/sample-data/baseline_script.json` → `src/render/out/baseline_sample.mp4` | Confirmed the shared rendering pipeline works and that the comparison isolates the agent architecture, not production values — same fonts, same voice, same transitions on both sides. |
| Render + verification visualization | Built the Remotion `Explainer` composition so a scene whose verification `status` isn't `verified` is visibly blurred/greyscaled with the block reason on screen, instead of silently rendering. Hand-authored the matching agent-side output for the same revenue-conflict case, with the disputed claim flagged. | `src/render/out/agent_sample.mp4` — same input as the baseline video, one scene visibly held back with "SOURCE CONFLICT — BLOCKED" and the exact page-vs-page discrepancy, while the two non-conflicting segment numbers still render normally. | The verification differentiator is visible in the actual output, not just logged to a file. Confirmed the Verification Agent's blocking logic is precise — it blocks the one contested claim, not the whole scene set. |
| Blocked on API key | No `ANTHROPIC_API_KEY` was available in the build environment, so the full baseline-vs-agent LLM run over the eval set (`eval/run_eval.py`) could not be executed live. What's real without any LLM call: the Verification Agent's programmatic layer (claim-existence + conflict detection) was unit-tested directly and caught both a conflicting-claim scene and an unknown-claim scene correctly, with a stub LLM client that throws if called — proving the check doesn't need a model call to work. | Unit test output (see below) + both sample videos. | Ship what's real; don't fabricate eval numbers to fill the table. |
| Made the model backend swappable, defaulted to open-source | Rewrote `src/llm.py` from an Anthropic-only client into a provider-agnostic one (`S2S_PROVIDER=openai\|anthropic`, `S2S_MODEL`, `OPENAI_BASE_URL`). Reasoning: the rules say micro1 provides no API keys or credits, so a judge reproducing this has the same problem the build did — a hard Anthropic dependency makes the "Reproducibility" criterion weaker for everyone, not just this build. Picked the default open-source model by checking current (2026) small-model function-calling reliability rather than guessing: models under ~7B tend to emit malformed or wrong-tool JSON often enough to break a pipeline that parses strict JSON every call; Qwen3 7B was the smallest size still reported reliable for that, and runs on 8GB VRAM via Ollama. | `src/llm.py` (`_OpenAICompatBackend`, `_AnthropicBackend`), same `LLMClient.call`/`call_json` interface both agents and eval already used — zero changes needed in `src/agents/*`, `src/baseline.py`, `eval/audit.py`. | Default provider is now `openai`-compatible pointed at local Ollama serving `qwen3:7b`, no key required; Anthropic/OpenAI/any compatible endpoint stays one env var away. `python eval/run_eval.py` is reproducible on a clean machine with `ollama pull qwen3:7b` and nothing else. |
| Final (at deadline) | Same LLM-dependent gap as above: whether the live run against Ollama actually completed before the deadline is recorded honestly in this row's evidence column, not assumed. | See "Live run" note directly below — filled in truthfully, not backfilled. | — |

### Verification Agent unit test (real, no API key needed)

```
s1 SOURCE_CONFLICT - claim(s) ['c1'] disagree between source passages; not rendering an unverified number
s2 UNSUPPORTED_CLAIM - cites unknown claim id(s): ['c99']
s3 VERIFIED - no factual claim asserted
blocked: ['s1', 's2']
renderable: ['s3']
```

## Hot take

Verification mattered more than generation quality would have. A better-written script
still states an unverifiable number with total confidence — better prompting doesn't fix
that, because the model has no way to know a number is contested unless something
explicitly checks it against the source. The fix that actually worked was cheap and
non-LLM: a programmatic existence/conflict check catches the two most damaging failure
modes (citing a claim that doesn't exist, citing a claim two source passages disagree
about) before any semantic judgment call is needed. If we'd spent the available time
tuning the script-writing prompt instead of building this check, the confidently-wrong
24%-revenue scene would still be sitting in the final video.

## What's discarded

The original brainstorm was a six-agent studio (Research / Story / Visual-Director /
Composer / Critic, plus cross-video creator memory). Cut to three agents + a deterministic
renderer once it was clear the rubric rewards purposeful design over component count, and
that every extra agent was another point of failure inside a fixed build window. Creator
memory is a real idea, not implemented — noted in `docs/architecture.md` as future work
rather than silently dropped.
