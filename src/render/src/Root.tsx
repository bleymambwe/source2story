import "./index.css";
import { ExplainerComposition } from "./Composition";
import { PitchCompositionDef } from "./PitchComposition";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <ExplainerComposition />
      <PitchCompositionDef />
    </>
  );
};
