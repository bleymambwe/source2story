import { CalculateMetadataFunction, Composition, Sequence } from "remotion";
import { SceneRenderer } from "./components/SceneRenderer";
import { explainerSchema, ExplainerProps, FPS } from "./schema";
import sampleAgent from "../sample-data/agent_verified_script.json";

const calculateMetadata: CalculateMetadataFunction<ExplainerProps> = ({
  props,
}) => {
  const durationInFrames = Math.max(
    1,
    Math.round(
      props.scenes.reduce((sum, s) => sum + s.duration_s, 0) * FPS
    )
  );
  return { durationInFrames };
};

export const ExplainerComposition = () => {
  return (
    <Composition
      id="Explainer"
      component={Explainer}
      durationInFrames={300}
      fps={FPS}
      width={1280}
      height={720}
      schema={explainerSchema}
      defaultProps={sampleAgent as ExplainerProps}
      calculateMetadata={calculateMetadata}
    />
  );
};

export const Explainer: React.FC<ExplainerProps> = ({ scenes }) => {
  let frameCursor = 0;
  return (
    <>
      {scenes.map((scene) => {
        const from = frameCursor;
        const durationInFrames = Math.round(scene.duration_s * FPS);
        frameCursor += durationInFrames;
        return (
          <Sequence
            key={scene.scene_id}
            from={from}
            durationInFrames={durationInFrames}
          >
            <SceneRenderer scene={scene} />
          </Sequence>
        );
      })}
    </>
  );
};
