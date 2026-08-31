import React from "react";
import { interpolate, useCurrentFrame, useVideoConfig } from "remotion";

export const Caption: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const opacity = interpolate(frame, [0, fps * 0.3], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        position: "absolute",
        bottom: 64,
        left: 80,
        right: 80,
        textAlign: "center",
        opacity,
      }}
    >
      <span
        style={{
          fontFamily: "Inter, Arial, sans-serif",
          fontSize: 40,
          fontWeight: 600,
          color: "white",
          background: "rgba(0,0,0,0.55)",
          padding: "14px 28px",
          borderRadius: 12,
          boxDecorationBreak: "clone",
          WebkitBoxDecorationBreak: "clone",
          lineHeight: 1.4,
        }}
      >
        {text}
      </span>
    </div>
  );
};
