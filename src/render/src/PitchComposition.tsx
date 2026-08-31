import { Composition, Sequence } from "remotion";
import { TextCard } from "./pitch/TextCard";
import { SplitCompare } from "./pitch/SplitCompare";
import { FPS } from "./schema";

type Slide = { durationS: number; el: React.ReactNode };

const slides: Slide[] = [
  {
    durationS: 5,
    el: (
      <TextCard
        eyebrow="micro1 Agentic Workflows Hackathon"
        title="Source2Story"
        lines={[
          "Turns a source document into an explainer video you can actually vouch for.",
        ]}
      />
    ),
  },
  {
    durationS: 8,
    el: (
      <TextCard
        eyebrow="Who this is for"
        title="People who have to stand behind what they show"
        lines={[
          "Teachers turning a chapter, paper or report into a 90-second lesson explainer.",
          "Students building study aids from their own course readings.",
          "Creators making knowledge-heavy explainers — economics, science, policy.",
        ]}
      />
    ),
  },
  {
    durationS: 9,
    el: (
      <TextCard
        eyebrow="The real bottleneck"
        title="AI video hasn't landed in classrooms because nobody can vouch for it"
        lines={[
          "The videos don't look bad. The problem is accountability.",
          "A teacher can't show a class a number that might be wrong.",
          "A student can't cite it. So the human re-checks every line by hand —",
          "which costs more time than writing the script themselves.",
        ]}
      />
    ),
  },
  {
    durationS: 6,
    el: (
      <TextCard
        eyebrow="Baseline"
        title="One direct prompt: read the source, write the script"
        lines={[
          "No claim tracking. No verification.",
          "Renders whatever the model wrote, with total confidence.",
        ]}
      />
    ),
  },
  { durationS: 8, el: <SplitCompare /> },
  {
    durationS: 9,
    el: (
      <TextCard
        eyebrow="The reframe"
        title="A blocked scene isn't a failure. It's a finding."
        lines={[
          "The source said +24% on page 3 and +17% on page 37, for the same quarter.",
          "The baseline picked one and sounded certain. Source2Story refused, and said why.",
          "For a teacher, that blocked scene IS the lesson: here is where the source",
          "contradicts itself. Verification doubles as source criticism.",
        ]}
      />
    ),
  },
  {
    durationS: 8,
    el: (
      <TextCard
        eyebrow="How it works"
        title="Three agents, one deterministic renderer"
        lines={[
          "Claim Extraction → Script/Storyboard → Verification → Remotion.",
          "Every factual line carries the claim id it rests on, back to a page in the source.",
          "A chart component can only display a number handed to it by a verified claim —",
          "visual truth enforced by construction, not by prompting.",
        ]}
      />
    ),
  },
  {
    durationS: 8,
    el: (
      <TextCard
        eyebrow="Runs on a free local model"
        title="Reproducible by someone with no API budget"
        lines={[
          "micro1 provides no API keys or credits — so a judge reproducing this has none either.",
          "Default backend is Qwen3 7B via local Ollama: no key, no cost.",
          "Anthropic or any OpenAI-compatible endpoint is one env var away.",
          "Same reason it works for a school with no AI budget.",
        ]}
      />
    ),
  },
  {
    durationS: 8,
    el: (
      <TextCard
        eyebrow="Hot take"
        title="Verification mattered more than generation quality"
        lines={[
          "A better-written script still states an unverifiable number with total confidence.",
          "Better prompting cannot fix that — the model has no way to know a figure is contested.",
          "The check that caught it was cheap and needed no model call at all.",
        ]}
      />
    ),
  },
  {
    durationS: 7,
    el: (
      <TextCard
        eyebrow="Honest status"
        title="What's verified, and what isn't"
        lines={[
          "Real: the pipeline, the renderer, and the programmatic verification layer —",
          "unit-tested catching both a source conflict and an unknown claim, with zero LLM calls.",
          "Not verified in this environment: a live LLM run. No key, and the Ollama",
          "install didn't finish before the deadline. Recorded in the changelog, not hidden.",
        ]}
      />
    ),
  },
  {
    durationS: 5,
    el: (
      <TextCard
        eyebrow="Repo"
        title="github.com/bleymambwe/source2story"
        lines={[
          "Code, README, changelog, reproduction guide, eval harness, agent trajectories.",
        ]}
      />
    ),
  },
];

export const PitchCompositionDef = () => {
  const durationInFrames = Math.round(
    slides.reduce((sum, s) => sum + s.durationS, 0) * FPS
  );
  return (
    <Composition
      id="Pitch"
      component={Pitch}
      durationInFrames={durationInFrames}
      fps={FPS}
      width={1280}
      height={720}
    />
  );
};

export const Pitch: React.FC = () => {
  let cursor = 0;
  return (
    <>
      {slides.map((slide, i) => {
        const from = cursor;
        const durationInFrames = Math.round(slide.durationS * FPS);
        cursor += durationInFrames;
        return (
          <Sequence key={i} from={from} durationInFrames={durationInFrames}>
            {slide.el}
          </Sequence>
        );
      })}
    </>
  );
};
