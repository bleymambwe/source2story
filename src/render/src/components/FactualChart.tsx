import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import type { Scene } from "../schema";

/** Draws directly from the scene's own value/unit — this component has no
 * way to show a number that wasn't handed to it by the verified script, by
 * construction. */
export const FactualChart: React.FC<{ scene: Scene }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const numeric = parseFloat(scene.value ?? "0");
  const barWidth = spring({ frame, fps, config: { damping: 200 } });
  const displayValue = interpolate(
    frame,
    [0, fps * 1.2],
    [0, isNaN(numeric) ? 0 : numeric],
    { extrapolateRight: "clamp" }
  );

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        background: "linear-gradient(135deg, #101828, #1D2939)",
        gap: 24,
      }}
    >
      <div
        style={{
          fontFamily: "Inter, Arial, sans-serif",
          fontSize: 96,
          fontWeight: 800,
          color: "#F97066",
        }}
      >
        {displayValue.toFixed(numeric % 1 === 0 ? 0 : 1)}
        <span style={{ fontSize: 48, marginLeft: 8, color: "#98A2B3" }}>
          {scene.unit ?? ""}
        </span>
      </div>
      <div
        style={{
          width: 480,
          height: 24,
          background: "#344054",
          borderRadius: 12,
          overflow: "hidden",
        }}
      >
        <div
          style={{
            width: `${barWidth * 100}%`,
            height: "100%",
            background: "#F97066",
          }}
        />
      </div>
    </div>
  );
};
