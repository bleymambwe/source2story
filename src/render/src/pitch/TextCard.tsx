import React from "react";
import { interpolate, useCurrentFrame, useVideoConfig } from "remotion";

export const TextCard: React.FC<{
  eyebrow?: string;
  title: string;
  lines?: string[];
  bg?: string;
}> = ({ eyebrow, title, lines = [], bg = "#0B1220" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const opacity = interpolate(frame, [0, fps * 0.3], [0, 1], {
    extrapolateRight: "clamp",
  });
  const rise = interpolate(frame, [0, fps * 0.4], [24, 0], {
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        background: bg,
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        padding: "0 110px",
        gap: 20,
        opacity,
        transform: `translateY(${rise}px)`,
      }}
    >
      {eyebrow ? (
        <div
          style={{
            fontFamily: "Inter, Arial, sans-serif",
            fontSize: 24,
            fontWeight: 700,
            letterSpacing: 3,
            color: "#F97066",
            textTransform: "uppercase",
          }}
        >
          {eyebrow}
        </div>
      ) : null}
      <div
        style={{
          fontFamily: "Inter, Arial, sans-serif",
          fontSize: 56,
          fontWeight: 800,
          color: "white",
          lineHeight: 1.2,
          maxWidth: 1000,
        }}
      >
        {title}
      </div>
      {lines.length ? (
        <div style={{ display: "flex", flexDirection: "column", gap: 10, marginTop: 8 }}>
          {lines.map((line, i) => (
            <div
              key={i}
              style={{
                fontFamily: "Inter, Arial, sans-serif",
                fontSize: 28,
                color: "#D0D5DD",
                maxWidth: 980,
              }}
            >
              {line}
            </div>
          ))}
        </div>
      ) : null}
    </div>
  );
};
