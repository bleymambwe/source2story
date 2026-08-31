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
        lines={["Turns a source document into a source-grounded explainer video."]}
      />
    ),
  },
  {
    durationS: 7,
    el: (
      <TextCard
        eyebrow="The problem"
        title="Explainer creators end up fact-checking AI output line by line"
        lines={[
          "Who: solo/small-team creators making knowledge-heavy explainer videos.",
          "Generic AI tools produce confident claims and visuals that aren't tied to the source.",
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
        lines={["No claim tracking. No verification. Renders whatever the model wrote."]}
      />
    ),
  },
  { durationS: 7, el: <SplitCompare /> },
  {
    durationS: 7,
    el: (
      <TextCard
        eyebrow="How it works"
        title="Three agents, one deterministic renderer"
        lines={[
          "Claim Extraction → Script/Storyboard → Verification → Remotion.",
          "Verification blocks unsupported, mismatched, or source-conflicted scenes before render.",
        ]}
      />
    ),
  },
  {
    durationS: 7,
    el: (
      <TextCard
        eyebrow="What's real right now"
        title="Changelog"
        lines={[
          "Built: agent pipeline, eval harness, Remotion renderer, trajectory logging.",
          "Verified with a real (non-LLM) test: conflict + unknown-claim detection both caught correctly.",
          "Pending: a live LLM run over the full eval set — no API key was available in the build window.",
        ]}
      />
    ),
  },
  {
    durationS: 6,
    el: (
      <TextCard
        eyebrow="Hot take"
        title="Verification mattered more than generation quality"
        lines={[
          "A better-written script still asserts an unverifiable number with total confidence.",
          "Catching that requires checking claims against the source, not writing a better prompt.",
        ]}
      />
    ),
  },
  {
    durationS: 6,
    el: (
      <TextCard
        eyebrow="Discarded experiment"
        title="Cut a six-agent studio down to three agents"
        lines={[
          "Research/Story/Visual-Director/Composer/Critic looked impressive but added failure points.",
          "Purposeful agents beat more agents — the brief says so directly.",
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
        lines={["Code, README, changelog, reproduction guide, eval harness, agent trajectories."]}
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
