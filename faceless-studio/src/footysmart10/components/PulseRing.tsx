/**
 * Two pulsing rings that expand around a key player to say "look here".
 * The rings follow the player, so they use the same keyframes as Player.
 */
import type React from "react";
import { scene, type HighlightData } from "../data/scene";
import { pointAt, windowOpacity } from "../lib/keyframes";
import { metresToPx, toPx } from "../lib/pitch";
import { useLayout, useSeconds } from "../lib/hooks";
import { FrameSvg } from "../../shared/FrameSvg";
import { theme } from "../lib/theme";
import { PLAYER_SIZE_M } from "./Player";

export const PulseRing: React.FC<{ readonly highlight: HighlightData }> = ({
  highlight,
}) => {
  const t = useSeconds();
  const layout = useLayout();

  if (t < highlight.from || t > highlight.to) {
    return null;
  }

  const player = scene.teams[highlight.team].players.find(
    (p) => p.number === highlight.number,
  );
  if (!player) {
    return null;
  }

  const keyframes = [{ t: 0, ...player.start }, ...(player.moves ?? [])];
  const pos = toPx(pointAt(keyframes, t), layout);
  const base = metresToPx(PLAYER_SIZE_M, layout) / 2;

  // Two rings, half a cycle apart. Each grows from the circle edge outward
  // and fades as it grows. One cycle takes a second.
  const rings = [0, 0.5].map((offset) => {
    const phase = (t + offset) % 1;
    return { r: base * (1.15 + 0.9 * phase), opacity: 1 - phase };
  });

  return (
    <FrameSvg
      style={{ opacity: windowOpacity(t, highlight.from, highlight.to, 0.3) }}
    >
      {rings.map((ring, i) => (
        <circle
          key={i}
          cx={pos.x}
          cy={pos.y}
          r={ring.r}
          fill="none"
          stroke={theme.overlay}
          strokeWidth={3 * layout.fontScale}
          opacity={ring.opacity}
        />
      ))}
    </FrameSvg>
  );
};
