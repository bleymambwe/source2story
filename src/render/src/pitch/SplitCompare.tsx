import React from "react";
import { FactualChart } from "../components/FactualChart";
import { FlaggedOverlay } from "../components/FlaggedOverlay";
import type { Scene } from "../schema";

const baselineScene: Scene = {
  scene_id: "cmp-baseline",
  narration: "Revenue increased 24% year-over-year.",
  visual_type: "factual_chart",
  visual_prompt: "Revenue growth",
  value: "24",
  unit: "%",
  status: "verified",
  duration_s: 6,
};

const agentScene: Scene = {
  ...baselineScene,
  scene_id: "cmp-agent",
  status: "source_conflict",
  detail:
    "p.3 says +24%; p.37 restates the same quarter to +17%. Not rendering an unverified number.",
};

export const SplitCompare: React.FC = () => {
  return (
    <div style={{ width: "100%", height: "100%", display: "flex" }}>
      <div style={{ width: "50%", height: "100%", position: "relative" }}>
        <FactualChart scene={baselineScene} />
        <Label text="BASELINE" color="#98A2B3" />
      </div>
      <div style={{ width: 4, background: "black" }} />
      <div style={{ width: "50%", height: "100%", position: "relative" }}>
        <FlaggedOverlay status={agentScene.status} detail={agentScene.detail}>
          <FactualChart scene={agentScene} />
        </FlaggedOverlay>
        <Label text="SOURCE2STORY" color="#F97066" />
      </div>
    </div>
  );
};

const Label: React.FC<{ text: string; color: string }> = ({ text, color }) => (
  <div
    style={{
      position: "absolute",
      top: 24,
      left: 24,
      fontFamily: "Inter, Arial, sans-serif",
      fontSize: 22,
      fontWeight: 800,
      letterSpacing: 2,
      color,
    }}
  >
    {text}
  </div>
);
