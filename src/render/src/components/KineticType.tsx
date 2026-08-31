import React from "react";
import { interpolate, useCurrentFrame, useVideoConfig } from "remotion";

export const KineticType: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const scale = interpolate(frame, [0, fps * 0.4], [0.85, 1], {
    extrapolateRight: "clamp",
  });
  const opacity = interpolate(frame, [0, fps * 0.4], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background: "#0B1220",
        padding: 96,
      }}
    >
      <div
        style={{
          fontFamily: "Inter, Arial, sans-serif",
          fontSize: 64,
          fontWeight: 700,
          color: "white",
          textAlign: "center",
          transform: `scale(${scale})`,
          opacity,
        }}
      >
        {text}
      </div>
    </div>
  );
};
