/**
 * A multiverse recast episode: hook card, the AI-generated shots with
 * captions, and a follow card. The AI PARODY badge is always visible.
 * Everything comes from src/multiverse/data/episode.ts.
 */
import type React from "react";
import {
  AbsoluteFill,
  Sequence,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { anton, inter } from "../shared/fonts";
import { fitAntonSize } from "../shared/fitText";
import { getSafeArea } from "../shared/safeArea";
import { Voiceover } from "../shared/Voiceover";
import { ShotSlot } from "./components/ShotSlot";
import { episode, type Word } from "./data/episode";
import voiceover from "./data/episode-voiceover.json";
import { mvTheme } from "./theme";

const colourOf = (c: Word["colour"]) =>
  c === "cyan"
    ? mvTheme.cyan
    : c === "magenta"
      ? mvTheme.magenta
      : mvTheme.white;

const useSafe = () => {
  const { width, height } = useVideoConfig();
  return getSafeArea(width, height);
};

/** Always-on label so viewers know the clip is AI-made. */
const Badge: React.FC = () => {
  const safe = useSafe();
  const s = safe.scale;
  return (
    <div
      style={{
        position: "absolute",
        top: safe.top,
        left: safe.side,
        fontFamily: inter,
        fontWeight: 800,
        fontSize: 24 * s,
        letterSpacing: 4 * s,
        color: mvTheme.white,
        padding: `${10 * s}px ${20 * s}px`,
        borderRadius: 999,
        background: `linear-gradient(90deg, ${mvTheme.violet}, ${mvTheme.magenta})`,
      }}
    >
      {episode.badge}
    </div>
  );
};

const Hook: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const safe = useSafe();
  const s = safe.scale;
  const exit = interpolate(
    frame,
    [durationInFrames - 0.4 * fps, durationInFrames - 1],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );
  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(circle at 50% 45%, rgba(139,92,246,0.45), ${mvTheme.black} 70%)`,
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
        padding: `0 ${safe.side}px`,
        opacity: 1 - exit,
      }}
    >
      <div
        style={{
          fontFamily: inter,
          fontWeight: 800,
          fontSize: 30 * s,
          letterSpacing: 10 * s,
          color: mvTheme.cyan,
          marginBottom: 30 * s,
        }}
      >
        {episode.hook.kicker}
      </div>
      {episode.hook.lines.map((line, i) => {
        const enter = spring({
          frame: frame - 4 - i * 5,
          fps,
          config: { damping: 15, stiffness: 120 },
        });
        return (
          <div
            key={i}
            style={{
              fontFamily: anton,
              fontSize: 104 * s,
              lineHeight: 1.05,
              opacity: enter,
              translate: `0px ${interpolate(enter, [0, 1], [60 * s, 0])}px`,
              textShadow: `0 0 ${40 * s}px rgba(139,92,246,0.6)`,
            }}
          >
            {line.map((w, j) => (
              <span key={j} style={{ color: colourOf(w.colour) }}>
                {w.text}
                {j < line.length - 1 ? " " : ""}
              </span>
            ))}
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

const ShotCaption: React.FC<{ readonly text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { height } = useVideoConfig();
  const safe = useSafe();
  const s = safe.scale;
  const enter = spring({ frame: frame - 6, fps, config: { damping: 18 } });
  return (
    <div
      style={{
        position: "absolute",
        left: safe.side,
        right: safe.side,
        top: height - safe.bottom - 140 * s,
        display: "flex",
        justifyContent: "center",
        opacity: enter,
        translate: `0px ${interpolate(enter, [0, 1], [30 * s, 0])}px`,
      }}
    >
      <div
        style={{
          fontFamily: anton,
          fontSize: 62 * s,
          color: mvTheme.white,
          backgroundColor: "rgba(5,4,11,0.72)",
          padding: `${12 * s}px ${30 * s}px`,
          borderRadius: 18 * s,
          borderBottom: `${5 * s}px solid ${mvTheme.magenta}`,
        }}
      >
        {text}
      </div>
    </div>
  );
};

const Outro: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, width } = useVideoConfig();
  const safe = useSafe();
  const s = safe.scale;
  const pop = (d: number) =>
    spring({ frame: frame - d, fps, config: { damping: 15, stiffness: 120 } });
  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(circle at 50% 45%, rgba(62,198,255,0.35), ${mvTheme.black} 70%)`,
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
        padding: `0 ${safe.side}px`,
        opacity: interpolate(frame, [0, 10], [0, 1], {
          extrapolateRight: "clamp",
        }),
      }}
    >
      <div
        style={{
          fontFamily: inter,
          fontWeight: 600,
          fontSize: 34 * s,
          letterSpacing: 8 * s,
          color: mvTheme.white,
          opacity: pop(2),
        }}
      >
        {episode.outro.follow}
      </div>
      <div
        style={{
          fontFamily: anton,
          fontSize: fitAntonSize(
            episode.handle,
            100 * s,
            width - safe.side * 2,
          ),
          lineHeight: 1.05,
          color: mvTheme.cyan,
          opacity: pop(7),
        }}
      >
        {episode.handle}
      </div>
      <div
        style={{
          fontFamily: inter,
          fontWeight: 600,
          fontSize: 46 * s,
          lineHeight: 1.25,
          color: mvTheme.white,
          marginTop: 46 * s,
          opacity: pop(14),
        }}
      >
        {episode.outro.question}
      </div>
      <div
        style={{
          fontFamily: anton,
          fontSize: 40 * s,
          color: mvTheme.white,
          background: `linear-gradient(90deg, ${mvTheme.violet}, ${mvTheme.magenta})`,
          padding: `${14 * s}px ${34 * s}px`,
          borderRadius: 999,
          marginTop: 40 * s,
          opacity: pop(22),
        }}
      >
        {episode.outro.cta}
      </div>
    </AbsoluteFill>
  );
};

export const RecastReel: React.FC = () => {
  const { fps } = useVideoConfig();
  let cursor = episode.hook.seconds;
  const shotTimes = episode.shots.map((shot) => {
    const from = cursor;
    cursor += shot.seconds;
    return from;
  });
  return (
    <AbsoluteFill style={{ backgroundColor: mvTheme.black }}>
      <Sequence
        name="Hook"
        durationInFrames={Math.round(episode.hook.seconds * fps)}
      >
        <Hook />
      </Sequence>
      {episode.shots.map((shot, i) => (
        <Sequence
          key={i}
          name={`Shot ${i + 1}`}
          from={Math.round(shotTimes[i] * fps)}
          durationInFrames={Math.round(shot.seconds * fps)}
        >
          <ShotSlot shot={shot} number={i + 1} />
          {shot.caption === null ? null : <ShotCaption text={shot.caption} />}
        </Sequence>
      ))}
      <Sequence name="Outro" from={Math.round(cursor * fps)}>
        <Outro />
      </Sequence>
      <Badge />
      {episode.voiceover.enabled ? (
        <Voiceover script={voiceover} volume={episode.voiceover.volume} />
      ) : null}
    </AbsoluteFill>
  );
};
