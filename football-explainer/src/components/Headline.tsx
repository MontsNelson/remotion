/**
 * The hook: a news-style cover headline in Anton with a small tag pill.
 * Each line springs up one after another. The whole thing lifts away at the
 * end of its sequence so the next scene never cuts in abruptly.
 */
import type React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import type { HeadlineWord } from "../data/scene";
import { useLayout } from "../lib/hooks";
import { anton, inter } from "../lib/fonts";
import { theme } from "../lib/theme";

const wordColour = (colour: HeadlineWord["colour"]) =>
  colour === "cyan"
    ? theme.cyan
    : colour === "yellow"
      ? theme.yellow
      : theme.text;

export const Headline: React.FC<{
  readonly tag: string;
  readonly lines: HeadlineWord[][];
}> = ({ tag, lines }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const layout = useLayout();
  const s = layout.fontScale;

  const exitStart = durationInFrames - Math.round(0.45 * fps);
  const exit = interpolate(frame, [exitStart, durationInFrames - 1], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const pill = spring({ frame, fps, config: { damping: 14, stiffness: 140 } });

  return (
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
        padding: `0 ${80 * s}px`,
        textAlign: "center",
        opacity: 1 - exit,
        translate: `0px ${-60 * s * exit}px`,
      }}
    >
      {/* Tag pill */}
      <div
        style={{
          fontFamily: inter,
          fontWeight: 800,
          fontSize: 26 * s,
          letterSpacing: 5 * s,
          color: theme.ink,
          backgroundColor: theme.yellow,
          padding: `${12 * s}px ${28 * s}px`,
          borderRadius: 999,
          marginBottom: 40 * s,
          opacity: pill,
          scale: `${interpolate(pill, [0, 1], [0.6, 1])}`,
        }}
      >
        {tag}
      </div>

      {lines.map((line, i) => {
        const enter = spring({
          frame: frame - 6 - i * 5,
          fps,
          config: { damping: 15, stiffness: 120 },
        });
        return (
          <div
            key={i}
            style={{
              fontFamily: anton,
              fontSize: 118 * s,
              lineHeight: 1.02,
              textTransform: "uppercase",
              textShadow: "0 10px 30px rgba(0,0,0,0.5)",
              opacity: enter,
              translate: `0px ${interpolate(enter, [0, 1], [70 * s, 0])}px`,
              scale: `${interpolate(enter, [0, 1], [0.92, 1])}`,
            }}
          >
            {line.map((word, j) => (
              <span key={j} style={{ color: wordColour(word.colour) }}>
                {word.text}
                {j < line.length - 1 ? " " : ""}
              </span>
            ))}
          </div>
        );
      })}
    </div>
  );
};
