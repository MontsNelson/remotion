/**
 * The voiceover. Each narration line is its own audio clip on the timeline,
 * starting at the second given in src/data/voiceover.json.
 * The clips themselves are made by scripts/voiceover.py.
 */
import type React from "react";
import { Audio } from "@remotion/media";
import { Track, staticFile, useVideoConfig } from "remotion";
import { scene } from "../data/scene";
import voiceover from "../data/voiceover.json";

export const Voiceover: React.FC = () => {
  const { fps } = useVideoConfig();
  if (!scene.voiceover.enabled) {
    return null;
  }
  return (
    <Track name="Voiceover">
      {voiceover.lines.map((line) => (
        <Audio
          key={line.id}
          name={`Voiceover: ${line.id}`}
          src={staticFile(`voiceover/${line.id}.wav`)}
          from={Math.round(line.at * fps)}
          volume={scene.voiceover.volume}
        />
      ))}
    </Track>
  );
};
