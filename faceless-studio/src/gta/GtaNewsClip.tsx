/**
 * A GTA news clip: big countdown hook, then fact cards one by one,
 * then a follow card with the disclaimer. Everything it shows comes
 * from src/gta/data/countdown.ts.
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
import { useSeconds } from "../shared/useSeconds";
import { Voiceover } from "../shared/Voiceover";
import { SynthwaveBackdrop } from "./components/SynthwaveBackdrop";
import { FactCard } from "./components/FactCard";
import { countdown, daysBetween } from "./data/countdown";
import voiceover from "./data/countdown-voiceover.json";
import { gtaTheme } from "./theme";

const fade = (t: number, from: number, to: number) =>
  interpolate(t, [from, to], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

/** The pill row at the top: kicker and tag. Always visible. */
const TopBar: React.FC = () => {
  const { width, height } = useVideoConfig();
  const safe = getSafeArea(width, height);
  const s = safe.scale;
  const t = useSeconds();
  const pill: React.CSSProperties = {
    fontFamily: inter,
    fontWeight: 800,
    fontSize: 26 * s,
    letterSpacing: 4 * s,
    padding: `${12 * s}px ${24 * s}px`,
    borderRadius: 999,
  };
  return (
    <div
      style={{
        position: "absolute",
        top: safe.top,
        left: 0,
        right: 0,
        display: "flex",
        justifyContent: "center",
        gap: 14 * s,
        opacity:
          fade(t, 0, 0.4) *
          (1 - fade(t, countdown.outro.from, countdown.outro.from + 0.4)),
      }}
    >
      <div
        style={{
          ...pill,
          backgroundColor: gtaTheme.pink,
          color: gtaTheme.white,
        }}
      >
        {countdown.kicker}
      </div>
      <div
        style={{
          ...pill,
          color: gtaTheme.cyan,
          border: `${3 * s}px solid ${gtaTheme.cyan}`,
        }}
      >
        {countdown.tag}
      </div>
    </div>
  );
};

/** The hook: "GTA 6 IS / 6 / DAYS AWAY", centred and huge. */
const Hook: React.FC<{ readonly days: number }> = ({ days }) => {
  const frame = useCurrentFrame();
  const { fps, width, height, durationInFrames } = useVideoConfig();
  const s = getSafeArea(width, height).scale;
  const pop = (delay: number) =>
    spring({
      frame: frame - delay,
      fps,
      config: { damping: 13, stiffness: 120 },
    });
  const exit = interpolate(
    frame,
    [durationInFrames - 0.4 * fps, durationInFrames - 1],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );
  const line: React.CSSProperties = {
    fontFamily: anton,
    lineHeight: 1,
    textShadow: "0 10px 40px rgba(0,0,0,0.6)",
  };
  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        opacity: 1 - exit,
        scale: `${1 - 0.15 * exit}`,
      }}
    >
      <div
        style={{
          ...line,
          fontSize: 110 * s,
          color: gtaTheme.white,
          opacity: pop(3),
        }}
      >
        {countdown.hookLines.before}
      </div>
      <div
        style={{
          ...line,
          fontSize: 460 * s,
          color: gtaTheme.pink,
          WebkitTextStroke: `${6 * s}px ${gtaTheme.white}`,
          scale: `${interpolate(pop(8), [0, 1], [0.3, 1])}`,
          opacity: pop(8),
        }}
      >
        {days}
      </div>
      <div
        style={{
          ...line,
          fontSize: 110 * s,
          color: gtaTheme.cyan,
          opacity: pop(14),
        }}
      >
        {countdown.hookLines.after}
      </div>
    </AbsoluteFill>
  );
};

/** After the hook: a compact countdown and the fact cards stacking up. */
const Facts: React.FC<{ readonly days: number | null }> = ({ days }) => {
  const { width, height, fps } = useVideoConfig();
  const safe = getSafeArea(width, height);
  const s = safe.scale;
  const t = useSeconds();
  const headerHeight = 190 * s;
  const gap = 16 * s;
  const n = countdown.facts.length;
  const cardHeight = Math.min(
    126 * s,
    (safe.available - headerHeight - 90 * s - gap * (n - 1)) / n,
  );
  const shown = countdown.facts.filter((f) => t >= f.at);
  return (
    <div
      style={{
        position: "absolute",
        top: safe.top + 90 * s,
        left: safe.side,
        right: safe.side,
        opacity: 1 - fade(t, countdown.outro.from, countdown.outro.from + 0.4),
      }}
    >
      <div
        style={{
          height: headerHeight,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          gap: 24 * s,
          opacity: fade(t, countdown.hookEndsAt, countdown.hookEndsAt + 0.4),
        }}
      >
        {days === null ? null : (
          <>
            <div
              style={{
                fontFamily: anton,
                fontSize: 170 * s,
                lineHeight: 1,
                color: gtaTheme.pink,
                WebkitTextStroke: `${4 * s}px ${gtaTheme.white}`,
              }}
            >
              {days}
            </div>
            <div
              style={{
                fontFamily: anton,
                fontSize: 74 * s,
                lineHeight: 1,
                color: gtaTheme.white,
              }}
            >
              {countdown.compactLabel}
            </div>
          </>
        )}
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap }}>
        {countdown.facts.map((fact, i) => (
          <Sequence
            key={fact.label}
            name={`Fact: ${fact.label}`}
            from={Math.round(fact.at * fps)}
            layout="none"
          >
            <FactCard
              label={fact.label}
              value={fact.value}
              height={cardHeight}
              scale={s}
              latest={i === shown.length - 1}
            />
          </Sequence>
        ))}
      </div>
    </div>
  );
};

/** The end card: follow, question, call to action, disclaimer. */
const Outro: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const safe = getSafeArea(width, height);
  const s = safe.scale;
  const pop = (delay: number) =>
    spring({
      frame: frame - delay,
      fps,
      config: { damping: 15, stiffness: 120 },
    });
  return (
    <AbsoluteFill
      style={{
        backgroundColor: "rgba(8, 2, 18, 0.95)",
        opacity: interpolate(frame, [0, 12], [0, 1], {
          extrapolateRight: "clamp",
        }),
      }}
    >
      <div
        style={{
          position: "absolute",
          top: safe.top,
          bottom: safe.bottom,
          left: safe.side,
          right: safe.side,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          textAlign: "center",
        }}
      >
        <div
          style={{
            fontFamily: inter,
            fontWeight: 600,
            fontSize: 34 * s,
            letterSpacing: 8 * s,
            color: gtaTheme.white,
            opacity: pop(3),
          }}
        >
          {countdown.outro.follow}
        </div>
        <div
          style={{
            fontFamily: anton,
            fontSize: fitAntonSize(
              countdown.handle,
              112 * s,
              width - safe.side * 2,
            ),
            lineHeight: 1.05,
            color: gtaTheme.pink,
            opacity: pop(8),
            scale: `${interpolate(pop(8), [0, 1], [0.85, 1])}`,
          }}
        >
          {countdown.handle}
        </div>
        <div
          style={{
            fontFamily: inter,
            fontWeight: 600,
            fontSize: 48 * s,
            lineHeight: 1.25,
            color: gtaTheme.white,
            marginTop: 50 * s,
            opacity: pop(16),
          }}
        >
          {countdown.outro.question}
        </div>
        <div
          style={{
            fontFamily: anton,
            fontSize: 40 * s,
            letterSpacing: 2 * s,
            color: gtaTheme.night,
            backgroundColor: gtaTheme.cyan,
            padding: `${14 * s}px ${34 * s}px`,
            borderRadius: 999,
            marginTop: 40 * s,
            opacity: pop(24),
          }}
        >
          {countdown.outro.cta}
        </div>
        <div
          style={{
            fontFamily: inter,
            fontWeight: 400,
            fontSize: 24 * s,
            lineHeight: 1.35,
            color: "rgba(255,255,255,0.7)",
            marginTop: 60 * s,
            maxWidth: 760 * s,
            opacity: pop(30),
          }}
        >
          {countdown.disclaimer}
        </div>
      </div>
    </AbsoluteFill>
  );
};

export const GtaNewsClip: React.FC = () => {
  const { fps } = useVideoConfig();
  const days = countdown.showCountdown
    ? daysBetween(countdown.postDate, countdown.releaseDate)
    : null;
  return (
    <AbsoluteFill style={{ backgroundColor: gtaTheme.night }}>
      <SynthwaveBackdrop />
      <TopBar />
      {days === null ? null : (
        <Sequence
          name="Hook"
          durationInFrames={Math.round((countdown.hookEndsAt + 0.2) * fps)}
        >
          <Hook days={days} />
        </Sequence>
      )}
      <Facts days={days} />
      <Sequence name="Outro" from={Math.round(countdown.outro.from * fps)}>
        <Outro />
      </Sequence>
      {countdown.voiceover.enabled ? (
        <Voiceover script={voiceover} volume={countdown.voiceover.volume} />
      ) : null}
    </AbsoluteFill>
  );
};
