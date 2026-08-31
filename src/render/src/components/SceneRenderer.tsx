import React from "react";
import type { Scene } from "../schema";
import { Caption } from "./Caption";
import { FactualChart } from "./FactualChart";
import { FlaggedOverlay } from "./FlaggedOverlay";
import { Illustrative } from "./Illustrative";
import { KineticType } from "./KineticType";
import { Transition } from "./Transition";

export const SceneRenderer: React.FC<{ scene: Scene }> = ({ scene }) => {
  const visual = (() => {
    switch (scene.visual_type) {
      case "factual_chart":
        return <FactualChart scene={scene} />;
      case "illustrative":
        return <Illustrative prompt={scene.visual_prompt} />;
      case "transition":
        return <Transition label={scene.visual_prompt} />;
      case "kinetic_type":
      default:
        return <KineticType text={scene.visual_prompt} />;
    }
  })();

  return (
    <div style={{ width: "100%", height: "100%", position: "relative" }}>
      <FlaggedOverlay status={scene.status} detail={scene.detail}>
        {visual}
      </FlaggedOverlay>
      {scene.status === "verified" && scene.visual_type !== "transition" ? (
        <Caption text={scene.narration} />
      ) : null}
    </div>
  );
};
