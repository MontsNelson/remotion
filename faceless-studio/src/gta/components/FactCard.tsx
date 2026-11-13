/** One fact card: a small cyan label and a big value, sliding in from the right. */
import type React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { anton, inter } from "../../shared/fonts";
import { gtaTheme } from "../theme";

export const FactCard: React.FC<{
  readonly label: string;
  readonly value: string;
  readonly height: number;
  readonly scale: number;
  /** True for the newest card, which gets a brighter edge. */
  readonly latest: boolean;
}> = ({ label, value, height, scale: s, latest }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const enter = spring({ frame, fps, config: { damping: 16, stiffness: 140 } });
  return (
    <div
      style={{
        height,
        display: "flex",
        alignItems: "center",
        gap: 24 * s,
        padding: `0 ${30 * s}px`,
        borderRadius: 22 * s,
        backgroundColor: gtaTheme.card,
        border: `${3 * s}px solid ${latest ? gtaTheme.pink : "rgba(255,46,154,0.25)"}`,
        boxShadow: latest ? `0 0 ${30 * s}px rgba(255,46,154,0.45)` : "none",
        opacity: enter,
        translate: `${interpolate(enter, [0, 1], [140 * s, 0])}px 0px`,
      }}
    >
      <div
        style={{
          width: 210 * s,
          flexShrink: 0,
          fontFamily: inter,
          fontWeight: 800,
          fontSize: 26 * s,
          letterSpacing: 3 * s,
          color: gtaTheme.cyan,
        }}
      >
        {label}
      </div>
      <div
        style={{
          fontFamily: anton,
          fontSize: Math.min(58 * s, height * 0.48),
          lineHeight: 1,
          color: gtaTheme.white,
        }}
      >
        {value}
      </div>
    </div>
  );
};
