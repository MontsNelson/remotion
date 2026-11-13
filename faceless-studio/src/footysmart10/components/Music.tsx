/**
 * Optional background music. Only plays when scene.music.enabled is true
 * AND you have put the file in the public/ folder.
 *
 * Volume: fades in over 1.5 s and out over the last 2 s, and dips
 * ("ducks") to a quarter while the voiceover is speaking so the
 * narration is always easy to hear.
 */
import type React from "react";
import { Audio } from "@remotion/media";
import { interpolate, staticFile, useVideoConfig } from "remotion";
import { scene } from "../data/scene";
import voiceover from "../data/voiceover.json";
import timings from "../data/voiceover-timings.json";

const DUCKED = 0.25;
const RAMP_SECONDS = 0.25;

export const Music: React.FC = () => {
  const { fps, durationInFrames } = useVideoConfig();
  if (!scene.music.enabled) {
    return null;
  }

  const speaking = scene.voiceover.enabled
    ? voiceover.lines.map((line) => ({
        from: line.at,
        to: line.at + (timings[line.id as keyof typeof timings] ?? 0),
      }))
    : [];

  return (
    <Audio
      name="Music"
      src={staticFile(scene.music.file)}
      volume={(frame) => {
        const t = frame / fps;
        const fade = interpolate(
          frame,
          [0, 1.5 * fps, durationInFrames - 2 * fps, durationInFrames - 1],
          [0, 1, 1, 0],
          { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
        );
        // 1 when nobody is talking, DUCKED while a line plays, smooth ramps.
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
        return scene.music.volume * fade * duck;
      }}
    />
  );
};
