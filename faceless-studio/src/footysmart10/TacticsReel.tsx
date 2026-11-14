/**
 * The whole video. Layers, from back to front:
 *   1. Camera (zooms, pans, tilts) containing the pitch, zones, arrows,
 *      players, pulsing rings, the ball and the goal flash.
 *   2. A soft vignette.
 *   3. Text overlays on their own Sequences: the hook headline, one caption
 *      per phase, and the outro. These stay OUTSIDE the camera so they are
 *      always sharp and inside the Reels safe zones.
 *   4. The voiceover and optional music.
 *
 * Timing comes from scene.ts (seconds) and is converted to frames here.
 */
import type React from "react";
import {
  AbsoluteFill,
  Sequence,
  Track,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { scene as defaultScene, type SceneData } from "./data/scene";
import { SceneContext, useScene } from "./data/sceneContext";
import { theme } from "./lib/theme";
import { inter } from "../shared/fonts";
import { Camera } from "./components/Camera";
import { Pitch } from "./components/Pitch";
import { Player } from "./components/Player";
import { Ball } from "./components/Ball";
import { Arrow } from "./components/Arrow";
import { Zone } from "./components/Zone";
import { PulseRing } from "./components/PulseRing";
import { Flash } from "./components/Flash";
import { Caption } from "./components/Caption";
import { Headline } from "./components/Headline";
import { Outro } from "./components/Outro";
import { Music } from "./components/Music";
import { Voiceover, type VoiceoverScript } from "../shared/Voiceover";
import { WordCaptions, type CaptionWord } from "../shared/WordCaptions";
import { getLayout } from "./lib/pitch";
import defaultVoiceover from "./data/voiceover.json";
import defaultTimings from "./data/voiceover-timings.json";

/** The pitch fades in behind the hook headline. */
const PitchFadeIn: React.FC<{ readonly children: React.ReactNode }> = ({
  children,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const scene = useScene();
  return (
    <AbsoluteFill
      style={{
        opacity: interpolate(
          frame,
          [0, scene.pitchFadeInSeconds * fps],
          [0, 1],
          {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          },
        ),
      }}
    >
      {children}
    </AbsoluteFill>
  );
};

export type TacticsReelProps = {
  /** A tactic in the same shape as scene.ts, or null for the built-in one. */
  tactic: SceneData | null;
  /** Narration script (clips in public/<outputFolder>/) with each clip's
   *  length in seconds, or null for the default high press narration. */
  voiceover: (VoiceoverScript & { durations: Record<string, number> }) | null;
  /** Word-by-word caption timings, or null for none. */
  captions: CaptionWord[] | null;
  /** Music file inside public/ (made by factory/music.py), or null for none. */
  musicFile: string | null;
};

export const TacticsReel: React.FC<TacticsReelProps> = (props) => {
  const scene = props.tactic ?? defaultScene;
  return (
    <SceneContext.Provider value={scene}>
      <TacticsReelInner {...props} scene={scene} />
    </SceneContext.Provider>
  );
};

const TacticsReelInner: React.FC<TacticsReelProps & { scene: SceneData }> = ({
  scene,
  voiceover,
  captions,
  musicFile,
}) => {
  const { fps, width, height } = useVideoConfig();
  const layout = getLayout(width, height);
  const script = voiceover ?? defaultVoiceover;
  const timings: Record<string, number> = voiceover
    ? voiceover.durations
    : defaultTimings;
  const speaking = scene.voiceover.enabled
    ? script.lines.map((line) => ({
        from: line.at,
        to: line.at + (timings[line.id] ?? 0),
      }))
    : [];

  const hook = scene.phases[0];
  const outro = scene.phases[scene.phases.length - 1];
  const captioned = scene.phases.filter((p) => p.caption !== null);

  return (
    <AbsoluteFill
      style={{ backgroundColor: theme.background, fontFamily: inter }}
    >
      <Camera>
        <PitchFadeIn>
          <Pitch />
        </PitchFadeIn>

        {scene.zones.map((zone, i) => (
          <Zone key={i} zone={zone} />
        ))}

        {scene.arrows.map((arrow, i) => (
          <Arrow key={i} arrow={arrow} />
        ))}

        {/* Team B (building up) and Team A (pressing). Each player slides in
            slightly after the previous one. */}
        {scene.teams.B.players.map((player, i) => (
          <Player
            key={`B${player.number}`}
            team="B"
            player={player}
            enterAt={scene.playersEnterAt + i * 0.12}
            enterFrom={scene.teams.B.enterFrom}
          />
        ))}
        {scene.teams.A.players.map((player, i) => (
          <Player
            key={`A${player.number}`}
            team="A"
            player={player}
            enterAt={scene.playersEnterAt + i * 0.12}
            enterFrom={scene.teams.A.enterFrom}
          />
        ))}

        {scene.highlights.map((highlight, i) => (
          <PulseRing key={i} highlight={highlight} />
        ))}

        <Ball />
        <Flash />
      </Camera>

      {/* Soft vignette over the whole frame */}
      <AbsoluteFill
        style={{
          background:
            "radial-gradient(ellipse at center, rgba(0,0,0,0) 45%, rgba(0,0,0,0.55) 100%)",
          pointerEvents: "none",
        }}
      />

      {/* Hook headline. It stays a little past its phase so it can lift away
          smoothly while the first caption is already arriving. */}
      <Sequence
        name="Hook headline"
        from={hook.from * fps}
        durationInFrames={(hook.to - hook.from + 0.5) * fps}
        layout="none"
      >
        <Headline tag={scene.tag} lines={scene.headline} />
      </Sequence>

      {/* One lower-third caption per phase */}
      <Track name="Captions">
        {captioned.map((phase, i) => (
          <Sequence
            key={phase.id}
            name={`Caption: ${phase.caption}`}
            from={phase.from * fps}
            durationInFrames={(phase.to - phase.from) * fps}
            layout="none"
          >
            <Caption
              text={phase.caption ?? ""}
              step={i + 1}
              totalSteps={captioned.length}
            />
          </Sequence>
        ))}
      </Track>

      <Sequence
        name="Outro"
        from={outro.from * fps}
        durationInFrames={(outro.to - outro.from) * fps}
        layout="none"
      >
        <Outro
          follow={scene.outro.follow}
          handle={scene.outro.handle}
          question={scene.outro.question}
          cta={scene.outro.cta}
        />
      </Sequence>

      {captions ? (
        <WordCaptions
          words={captions}
          centreY={layout.height - layout.safeBottom + 60 * layout.fontScale}
        />
      ) : null}

      {scene.voiceover.enabled ? (
        <Voiceover script={script} volume={scene.voiceover.volume} />
      ) : null}
      <Music
        file={musicFile ?? (scene.music.enabled ? scene.music.file : null)}
        volume={scene.music.volume}
        speaking={speaking}
      />
    </AbsoluteFill>
  );
};
