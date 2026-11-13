/**
 * A translucent yellow area with a dashed edge and an optional label.
 * It breathes slightly so it feels alive.
 */
import type React from "react";
import type { ZoneData } from "../data/scene";
import { windowOpacity } from "../lib/keyframes";
import { toPx } from "../lib/pitch";
import { useLayout, useSeconds } from "../lib/hooks";
import { FrameSvg } from "../../shared/FrameSvg";
import { inter } from "../../shared/fonts";
import { theme } from "../lib/theme";

export const Zone: React.FC<{ readonly zone: ZoneData }> = ({ zone }) => {
  const t = useSeconds();
  const layout = useLayout();

  if (t < zone.from || t > zone.to) {
    return null;
  }

  const px = zone.points.map((m) => toPx(m, layout));
  const points = px.map((p) => `${p.x},${p.y}`).join(" ");
  const minX = Math.min(...px.map((p) => p.x));
  const minY = Math.min(...px.map((p) => p.y));
  const breathe = 0.85 + 0.15 * Math.sin(t * Math.PI * 1.2);

  return (
    <FrameSvg style={{ opacity: windowOpacity(t, zone.from, zone.to, 0.5) }}>
      <polygon
        points={points}
        fill={theme.overlay}
        fillOpacity={0.16 * breathe}
        stroke={theme.overlay}
        strokeOpacity={0.85}
        strokeWidth={2.5 * layout.fontScale}
        strokeDasharray={`${10 * layout.fontScale} ${8 * layout.fontScale}`}
        strokeLinejoin="round"
      />
      {zone.label ? (
        <text
          x={minX + 14 * layout.fontScale}
          y={minY + 34 * layout.fontScale}
          fill={theme.overlay}
          fontFamily={inter}
          fontWeight={800}
          fontSize={22 * layout.fontScale}
          letterSpacing={2 * layout.fontScale}
        >
          {zone.label}
        </text>
      ) : null}
    </FrameSvg>
  );
};
