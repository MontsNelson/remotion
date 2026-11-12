/**
 * A lower-third caption, e.g. "THE SHAPE". Lives inside a <Sequence>, so
 * frame 0 is the moment the caption starts. It fades and slides in, then
 * fades and slides out just before the sequence ends.
 */
import type React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { useLayout } from "../lib/hooks";
import { anton, inter } from "../lib/fonts";
import { theme } from "../lib/theme";

export const Caption: React.FC<{
  readonly text: string;
  readonly step: number;
  readonly totalSteps: number;
}> = ({ text, step, totalSteps }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const layout = useLayout();
  const s = layout.fontScale;

  const enter = spring({ frame, fps, config: { damping: 18, stiffness: 120 } });
  const exitStart = durationInFrames - Math.round(0.4 * fps);

  return (
    <div
      style={{
        position: "absolute",
        left: 70 * s,
        top: layout.height - layout.safeBottom - 175 * s,
        display: "flex",
        alignItems: "stretch",
        gap: 22 * s,
        padding: `${16 * s}px ${34 * s}px ${16 * s}px ${26 * s}px`,
        borderRadius: 18 * s,
        background:
          "linear-gradient(90deg, rgba(0,0,0,0.6) 0%, rgba(0,0,0,0.35) 70%, rgba(0,0,0,0) 100%)",
        opacity:
          interpolate(frame, [0, 10], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          }) *
          interpolate(frame, [exitStart, durationInFrames - 1], [1, 0], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          }),
        translate: `0px ${
          interpolate(enter, [0, 1], [50 * s, 0]) +
          interpolate(frame, [exitStart, durationInFrames - 1], [0, -30 * s], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          })
        }px`,
      }}
    >
      {/* Yellow accent bar */}
      <div
        style={{
          width: 10 * s,
          borderRadius: 6 * s,
          backgroundColor: theme.yellow,
        }}
      />
      <div style={{ display: "flex", flexDirection: "column" }}>
        <div
          style={{
            fontFamily: inter,
            fontWeight: 800,
            fontSize: 24 * s,
            letterSpacing: 4 * s,
            color: theme.yellow,
            marginBottom: 6 * s,
          }}
        >
          STEP {step} OF {totalSteps}
        </div>
        <div
          style={{
            fontFamily: anton,
            fontSize: 78 * s,
            lineHeight: 1,
            color: theme.text,
            textTransform: "uppercase",
            letterSpacing: 1 * s,
          }}
        >
          {text}
        </div>
      </div>
    </div>
  );
};
