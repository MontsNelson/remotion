/**
 * One player: a coloured circle with a shirt number.
 * It slides into position with a spring when the shape forms, then glides
 * between the `moves` keyframes from scene.ts.
 */
import type React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import type { PlayerData } from "../data/scene";
import { pointAt } from "../lib/keyframes";
import { metresToPx, toPx } from "../lib/pitch";
import { useLayout } from "../lib/hooks";
import { inter } from "../lib/fonts";
import { theme } from "../lib/theme";

/** Diameter of a player circle, in metres (so it scales with the pitch). */
export const PLAYER_SIZE_M = 4.6;

export const Player: React.FC<{
  readonly team: "A" | "B";
  readonly player: PlayerData;
  /** The second this player slides in. */
  readonly enterAt: number;
  readonly enterFrom: "top" | "bottom";
}> = ({ team, player, enterAt, enterFrom }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const layout = useLayout();

  const enterFrame = Math.round(enterAt * fps);
  if (frame < enterFrame) {
    return null;
  }

  // Where is the player right now? First keyframe is the start position.
  const keyframes = [{ t: 0, ...player.start }, ...(player.moves ?? [])];
  const pos = toPx(pointAt(keyframes, frame / fps), layout);
  const size = metresToPx(PLAYER_SIZE_M, layout);

  // Entrance: springs from off its spot into place.
  const entrance = spring({
    frame: frame - enterFrame,
    fps,
    config: { damping: 16, stiffness: 110, mass: 0.9 },
  });
  const slide = (enterFrom === "top" ? -1 : 1) * layout.height * 0.18;

  const color = team === "A" ? theme.teamA : theme.teamB;
  const numberColor = team === "A" ? theme.ink : theme.text;

  return (
    <div
      style={{
        position: "absolute",
        left: pos.x - size / 2,
        top: pos.y - size / 2,
        width: size,
        height: size,
        borderRadius: "50%",
        backgroundColor: color,
        border: `${Math.max(2, size * 0.06)}px solid rgba(255,255,255,0.9)`,
        boxShadow: "0 6px 14px rgba(0,0,0,0.45)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontFamily: inter,
        fontWeight: 800,
        fontSize: size * 0.46,
        color: numberColor,
        opacity: interpolate(frame - enterFrame, [0, 8], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        }),
        translate: `0px ${interpolate(entrance, [0, 1], [slide, 0])}px`,
        scale: `${interpolate(entrance, [0, 1], [0.4, 1])}`,
      }}
    >
      {player.number}
    </div>
  );
};
