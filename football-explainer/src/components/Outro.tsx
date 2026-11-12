/**
 * The outro: dims the pitch, shows FOLLOW @handle and a question to drive
 * comments. Lives inside a <Sequence>, so frame 0 is its first frame.
 */
import type React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { useLayout } from "../lib/hooks";
import { anton, inter } from "../lib/fonts";
import { theme } from "../lib/theme";

export const Outro: React.FC<{
  readonly follow: string;
  readonly handle: string;
  readonly question: string;
  readonly cta: string;
}> = ({ follow, handle, question, cta }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const layout = useLayout();
  const s = layout.fontScale;

  const pop = (delayFrames: number) =>
    spring({
      frame: frame - delayFrames,
      fps,
      config: { damping: 15, stiffness: 120 },
    });
  const a = pop(4);
  const b = pop(10);
  const c = pop(18);
  const d = pop(26);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "rgba(4, 26, 19, 0.82)",
        opacity: interpolate(frame, [0, 15], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        }),
      }}
    >
      <div
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          top: layout.safeTop,
          bottom: layout.safeBottom,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          textAlign: "center",
          padding: `0 ${90 * s}px`,
        }}
      >
        <div
          style={{
            fontFamily: inter,
            fontWeight: 600,
            fontSize: 34 * s,
            letterSpacing: 8 * s,
            color: theme.text,
            opacity: a * 0.85,
            translate: `0px ${interpolate(a, [0, 1], [30 * s, 0])}px`,
          }}
        >
          {follow}
        </div>
        <div
          style={{
            fontFamily: anton,
            fontSize: 124 * s,
            lineHeight: 1,
            color: theme.cyan,
            marginTop: 10 * s,
            opacity: b,
            scale: `${interpolate(b, [0, 1], [0.85, 1])}`,
          }}
        >
          {handle}
        </div>
        <div
          style={{
            fontFamily: inter,
            fontWeight: 600,
            fontSize: 46 * s,
            lineHeight: 1.25,
            color: theme.text,
            marginTop: 60 * s,
            maxWidth: 860 * s,
            opacity: c,
            translate: `0px ${interpolate(c, [0, 1], [30 * s, 0])}px`,
          }}
        >
          {question}
        </div>
        <div
          style={{
            fontFamily: anton,
            fontSize: 38 * s,
            letterSpacing: 2 * s,
            color: theme.ink,
            backgroundColor: theme.yellow,
            padding: `${14 * s}px ${34 * s}px`,
            borderRadius: 999,
            marginTop: 44 * s,
            opacity: d,
            scale: `${interpolate(d, [0, 1], [0.7, 1])}`,
          }}
        >
          {cta}
        </div>
      </div>
    </AbsoluteFill>
  );
};
