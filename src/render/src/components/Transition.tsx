import React from "react";
import { interpolate, useCurrentFrame } from "remotion";

export const Transition: React.FC<{ label: string }> = ({ label }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 10, 20, 30], [0, 1, 1, 0], {
    extrapolateLeft: "clamp",
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
        background: "black",
      }}
    >
      <div
        style={{
          fontFamily: "Inter, Arial, sans-serif",
          fontSize: 40,
          color: "white",
          opacity,
        }}
      >
        {label}
      </div>
    </div>
  );
};
