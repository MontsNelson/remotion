/**
 * The ball: a small white circle with a short motion trail.
 * The trail is just the ball's position a few frames ago, drawn fainter.
 */
import type React from "react";
import { interpolate } from "remotion";
import { scene } from "../data/scene";
import { isMovingAt, kick, pointAt } from "../lib/keyframes";
import { metresToPx, toPx } from "../lib/pitch";
import { useLayout, useSeconds } from "../lib/hooks";
import { FrameSvg } from "../lib/FrameSvg";
import { theme } from "../lib/theme";

const TRAIL_LENGTH = 6;
const TRAIL_GAP_SECONDS = 0.045;

export const Ball: React.FC = () => {
  const t = useSeconds();
  const layout = useLayout();
  const appearsAt = scene.ball[0].t;

  if (t < appearsAt) {
    return null;
  }

  const radius = metresToPx(1.1, layout);
  const now = toPx(pointAt(scene.ball, t, kick), layout);
  const moving = isMovingAt(scene.ball, t);

  const trail = Array.from({ length: TRAIL_LENGTH }, (_, i) => i + 1);

  return (
    <FrameSvg
      style={{
        opacity: interpolate(t, [appearsAt, appearsAt + 0.3], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        }),
      }}
    >
      {moving
        ? trail.map((i) => {
            const ghost = toPx(
              pointAt(scene.ball, t - i * TRAIL_GAP_SECONDS, kick),
              layout,
            );
            return (
              <circle
                key={i}
                cx={ghost.x}
                cy={ghost.y}
                r={radius * (1 - i / (TRAIL_LENGTH + 2))}
                fill={theme.ball}
                opacity={0.45 * (1 - i / TRAIL_LENGTH)}
              />
            );
          })
        : null}
      <circle
        cx={now.x}
        cy={now.y}
        r={radius}
        fill={theme.ball}
        stroke="rgba(0,0,0,0.45)"
        strokeWidth={Math.max(1.5, radius * 0.18)}
      />
    </FrameSvg>
  );
};
