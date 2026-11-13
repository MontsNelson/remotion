/**
 * Plays a voiceover script: one audio clip per line, each starting at the
 * second given in its voiceover.json. The clips are recorded by
 * scripts/voiceover.py into public/<outputFolder>/<line id>.wav.
 * Works for every channel.
 */
import type React from "react";
import { Audio } from "@remotion/media";
import { Track, staticFile, useVideoConfig } from "remotion";

export type VoiceoverScript = {
  voice: string;
  speed: number;
  outputFolder: string;
  videoLengthSeconds: number;
  lines: { id: string; at: number; text: string }[];
};

export const Voiceover: React.FC<{
  readonly script: VoiceoverScript;
  readonly volume: number;
}> = ({ script, volume }) => {
  const { fps } = useVideoConfig();
  return (
    <Track name="Voiceover">
      {script.lines.map((line) => (
        <Audio
          key={line.id}
          name={`Voiceover: ${line.id}`}
          src={staticFile(`${script.outputFolder}/${line.id}.wav`)}
          from={Math.round(line.at * fps)}
          volume={volume}
        />
      ))}
    </Track>
  );
};
