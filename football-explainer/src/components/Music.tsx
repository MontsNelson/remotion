/**
 * Optional background music. Only plays when scene.music.enabled is true
 * AND you have put the file in the public/ folder. Volume stays low
 * ("ducked") and fades in over 1.5 s and out over the last 2 s.
 */
import type React from "react";
import { Audio, interpolate, staticFile, useVideoConfig } from "remotion";
import { scene } from "../data/scene";

export const Music: React.FC = () => {
  const { fps, durationInFrames } = useVideoConfig();
  if (!scene.music.enabled) {
    return null;
  }
  const level = scene.music.volume;
  return (
    <Audio
      src={staticFile(scene.music.file)}
      volume={(frame) =>
        interpolate(
          frame,
          [0, 1.5 * fps, durationInFrames - 2 * fps, durationInFrames - 1],
          [0, level, level, 0],
          { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
        )
      }
    />
  );
};
