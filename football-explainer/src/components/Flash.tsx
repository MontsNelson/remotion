/** A quick white burst at the goal when the ball crosses the line. */
import type React from "react";
import { interpolate } from "remotion";
import { scene } from "../data/scene";
import { metresToPx, toPx } from "../lib/pitch";
import { useLayout, useSeconds } from "../lib/hooks";
import { FrameSvg } from "../lib/FrameSvg";

export const Flash: React.FC = () => {
  const t = useSeconds();
  const layout = useLayout();
  const { t: at, at: where } = scene.goal;

  if (t < at || t > at + 0.8) {
    return null;
  }

  const progress = interpolate(t, [at, at + 0.8], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const center = toPx(where, layout);

  return (
    <FrameSvg>
      <circle
        cx={center.x}
        cy={center.y}
        r={metresToPx(1 + 14 * progress, layout)}
        fill="none"
        stroke="#FFFFFF"
        strokeWidth={6 * layout.fontScale * (1 - progress)}
        opacity={1 - progress}
      />
      <circle
        cx={center.x}
        cy={center.y}
        r={metresToPx(1 + 6 * progress, layout)}
        fill="#FFFFFF"
        opacity={0.6 * (1 - progress)}
      />
    </FrameSvg>
  );
};
