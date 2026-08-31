import React from "react";
import { interpolate, useCurrentFrame } from "remotion";

/** Stylised, deliberately non-photorealistic placeholder for illustrative-only
 * scenes, labelled so it never reads as archival/factual footage. */
export const Illustrative: React.FC<{ prompt: string }> = ({ prompt }) => {
  const frame = useCurrentFrame();
  const drift = interpolate(frame, [0, 150], [0, 20]);

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        position: "relative",
        background:
          "radial-gradient(circle at 30% 30%, #5B7FFF 0%, #2A2E70 55%, #0B0E2A 100%)",
        overflow: "hidden",
      }}
    >
      <div
        style={{
          position: "absolute",
          inset: -40,
          transform: `translate(${drift}px, ${drift * 0.5}px)`,
          background:
            "repeating-linear-gradient(45deg, rgba(255,255,255,0.05) 0 2px, transparent 2px 40px)",
        }}
      />
      <div
        style={{
          position: "absolute",
          top: 32,
          left: 32,
          fontFamily: "Inter, Arial, sans-serif",
          fontSize: 20,
          fontWeight: 700,
          color: "rgba(255,255,255,0.85)",
          background: "rgba(0,0,0,0.35)",
          padding: "6px 14px",
          borderRadius: 999,
          letterSpacing: 1,
        }}
      >
        ILLUSTRATIVE
      </div>
      <div
        style={{
          position: "absolute",
          inset: 0,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          padding: 96,
        }}
      >
        <div
          style={{
            fontFamily: "Inter, Arial, sans-serif",
            fontSize: 28,
            color: "rgba(255,255,255,0.7)",
            textAlign: "center",
          }}
        >
          {prompt}
        </div>
      </div>
    </div>
  );
};
