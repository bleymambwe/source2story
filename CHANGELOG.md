# Improvement Changelog

Each entry: what was tried and why, the evidence from `eval/results/`, and the decision it
led to. Entries are added as the project is actually built — this is the live document, not
a plan written in advance.

| Stage | What was tried and why | Evidence | Decision / learning |
|---|---|---|---|
| Scaffold | Built the baseline prompt, the 3-agent pipeline (claim extraction → script → verification), and an independent eval auditor that scores both the same way. | Unit-level check (no LLM, no API key needed): fed the Verification Agent a claim ledger with a known conflict (two different revenue-growth figures for the same quarter, `eval/cases/revenue_conflict.txt`) and a script citing both an unknown claim id and a conflicted one. It correctly blocked both scenes (`SOURCE_CONFLICT`, `UNSUPPORTED_CLAIM`) and let the transition scene through — with an `ExplodingLLM` stub proving no model call was needed to catch either failure. | Confirms the programmatic layer of verification (existence + conflict checks) works before spending any API budget on the semantic layer. Full baseline-vs-agent runs with real LLM calls are pending an `ANTHROPIC_API_KEY`. |
| Baseline | Single direct prompt: read the source, write a ~90s script + one-line visual per scene. Rendered through the same Remotion pipeline as the agent solution. | _pending eval run_ | Establishes the starting point. |
| Iteration 1 | _tbd_ | _tbd_ | _tbd_ |
| Iteration 2 | _tbd_ | _tbd_ | _tbd_ |
| Final | _tbd_ | _tbd_ | _tbd_ |

## Hot take

_Filled in once the adversarial (conflicting-numbers) eval case has actually been run against
both baseline and agent — this should be a real observed failure mode, not a predicted one._
