/**
 * One shot of the episode. Plays the AI-generated clip if there is one;
 * otherwise shows a placeholder card with the prompt to generate it.
 */
import type React from "react";
import { Video } from "@remotion/media";
import {
  AbsoluteFill,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { anton, inter } from "../../shared/fonts";
import { getSafeArea } from "../../shared/safeArea";
import type { Shot } from "../data/episode";
import { mvTheme } from "../theme";

export const ShotSlot: React.FC<{
  readonly shot: Shot;
  readonly number: number;
}> = ({ shot, number }) => {
  const frame = useCurrentFrame();
  const { fps, width, height, durationInFrames } = useVideoConfig();
  const safe = getSafeArea(width, height);
  const s = safe.scale;
  // Short cross-fade in and out so shots never hard-cut.
  const opacity = interpolate(
    frame,
    [0, 0.25 * fps, durationInFrames - 0.25 * fps, durationInFrames],
    [0, 1, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );

  if (shot.file !== null) {
    return (
      <AbsoluteFill style={{ opacity }}>
        <Video
          src={staticFile(shot.file)}
          objectFit="cover"
          style={{ width: "100%", height: "100%" }}
        />
      </AbsoluteFill>
    );
  }

  const drift = interpolate(frame, [0, durationInFrames], [0, 40]);
  return (
    <AbsoluteFill
      style={{
        opacity,
        background: `radial-gradient(circle at ${30 + drift}% 35%, rgba(139,92,246,0.55), transparent 55%), radial-gradient(circle at ${75 - drift / 2}% 70%, rgba(62,198,255,0.4), transparent 55%), ${mvTheme.black}`,
      }}
    >
      <div
        style={{
          position: "absolute",
          top: safe.top + 120 * s,
          bottom: safe.bottom + 220 * s,
          left: safe.side,
          right: safe.side,
          border: `${3 * s}px dashed rgba(255,255,255,0.35)`,
          borderRadius: 28 * s,
          padding: 44 * s,
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          gap: 26 * s,
        }}
      >
        <div
          style={{
            fontFamily: anton,
            fontSize: 90 * s,
            color: mvTheme.cyan,
            lineHeight: 1,
          }}
        >
          SHOT {number}
        </div>
        <div
          style={{
            fontFamily: inter,
            fontWeight: 800,
            fontSize: 26 * s,
            letterSpacing: 3 * s,
            color: mvTheme.magenta,
          }}
        >
          PLACEHOLDER · GENERATE THIS CLIP ({shot.seconds}s)
        </div>
        <div
          style={{
            fontFamily: inter,
            fontWeight: 400,
            fontSize: 32 * s,
            lineHeight: 1.4,
            color: "rgba(255,255,255,0.88)",
          }}
        >
          {shot.prompt}
        </div>
      </div>
    </AbsoluteFill>
  );
};
