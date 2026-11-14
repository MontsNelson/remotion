/**
 * Background music: original tracks made by factory/music.py (no copyright).
 * Fades in over 1.5 s and out over the last 2 s, and dips ("ducks") to a
 * quarter whenever the voiceover is speaking so the narration stays clear.
 */
import type React from "react";
import { Audio } from "@remotion/media";
import { interpolate, staticFile, useVideoConfig } from "remotion";

const DUCKED = 0.25;
const RAMP_SECONDS = 0.25;

export const Music: React.FC<{
  /** File inside public/, or null for no music. */
  readonly file: string | null;
  readonly volume: number;
  /** When the narrator is speaking, in seconds. */
  readonly speaking: { from: number; to: number }[];
}> = ({ file, volume, speaking }) => {
  const { fps, durationInFrames } = useVideoConfig();
  if (file === null) {
    return null;
  }
  return (
    <Audio
      name="Music"
      src={staticFile(file)}
      volume={(frame) => {
        const t = frame / fps;
        const fade = interpolate(
          frame,
          [0, 1.5 * fps, durationInFrames - 2 * fps, durationInFrames - 1],
          [0, 1, 1, 0],
          { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
        );
        const duck = Math.min(
          1,
          ...speaking.map((s) =>
            interpolate(
              t,
              [s.from - RAMP_SECONDS, s.from, s.to, s.to + RAMP_SECONDS],
              [1, DUCKED, DUCKED, 1],
              { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
            ),
          ),
        );
        return volume * fade * duck;
      }}
    />
  );
};
