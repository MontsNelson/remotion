/**
 * Word-by-word captions: shows the current phrase (up to four words) with
 * the word being spoken in yellow. Sits just above Instagram's bottom
 * button area. Timings come from the voiceover generator.
 */
import type React from "react";
import { useVideoConfig } from "remotion";
import { anton } from "./fonts";
import { getSafeArea } from "./safeArea";
import { useSeconds } from "./useSeconds";

export type CaptionWord = { word: string; start: number; end: number };

export const WordCaptions: React.FC<{
  readonly words: CaptionWord[];
  /** Pixels from the top of the frame to the middle of the caption line. */
  readonly centreY: number;
}> = ({ words, centreY }) => {
  const t = useSeconds();
  const { width, height } = useVideoConfig();
  const safe = getSafeArea(width, height);
  const s = safe.scale;
  if (words.length === 0) {
    return null;
  }
  let current = -1;
  for (let i = 0; i < words.length; i++) {
    if (words[i].start <= t) {
      current = i;
    }
  }
  if (current === -1 || t > words[current].end + 0.35) {
    return null;
  }
  const groupStart = Math.floor(current / 4) * 4;
  const group = words.slice(groupStart, groupStart + 4);
  return (
    <div
      style={{
        position: "absolute",
        left: safe.side,
        right: safe.side + 60 * s,
        top: centreY - 40 * s,
        display: "flex",
        justifyContent: "center",
        gap: 18 * s,
        fontFamily: anton,
        fontSize: 64 * s,
        lineHeight: 1.2,
        textTransform: "uppercase",
        WebkitTextStroke: `${3 * s}px #000`,
        paintOrder: "stroke fill",
        textShadow: "0 4px 18px rgba(0,0,0,0.8)",
        whiteSpace: "nowrap",
      }}
    >
      {group.map((w, i) => (
        <span
          key={groupStart + i}
          style={{ color: groupStart + i === current ? "#FFE14D" : "#FFFFFF" }}
        >
          {w.word}
        </span>
      ))}
    </div>
  );
};
