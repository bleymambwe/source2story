import React from "react";
import type { VerificationStatus } from "../schema";

const LABELS: Record<string, string> = {
  unsupported_claim: "UNSUPPORTED CLAIM — BLOCKED",
  value_mismatch: "VALUE MISMATCH — BLOCKED",
  source_conflict: "SOURCE CONFLICT — BLOCKED",
};

/** Wraps a scene's normal visual and visibly marks it as held back by the
 * Verification Agent, instead of silently rendering an unverified claim. */
export const FlaggedOverlay: React.FC<{
  status: VerificationStatus;
  detail?: string;
  children: React.ReactNode;
}> = ({ status, detail, children }) => {
  if (status === "verified") return <>{children}</>;

  return (
    <div style={{ width: "100%", height: "100%", position: "relative" }}>
      <div style={{ filter: "blur(14px) grayscale(1) brightness(0.5)" }}>
        {children}
      </div>
      <div
        style={{
          position: "absolute",
          inset: 0,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          gap: 16,
          padding: 96,
          textAlign: "center",
        }}
      >
        <div
          style={{
            fontFamily: "Inter, Arial, sans-serif",
            fontSize: 32,
            fontWeight: 800,
            color: "#FDA29B",
            letterSpacing: 2,
            border: "3px solid #FDA29B",
            borderRadius: 12,
            padding: "10px 24px",
          }}
        >
          {LABELS[status] ?? "BLOCKED"}
        </div>
        {detail ? (
          <div
            style={{
              fontFamily: "Inter, Arial, sans-serif",
              fontSize: 24,
              color: "white",
              maxWidth: 720,
            }}
          >
            {detail}
          </div>
        ) : null}
      </div>
    </div>
  );
};
