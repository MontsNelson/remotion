/**
 * Tactical arrows in yellow.
 *  - "run":  a solid curved arrow that draws itself on, with an arrowhead.
 *  - "lane": a dashed passing lane. When `cutAt` passes it dims and gets an X.
 */
import type React from "react";
import { interpolate, spring, useVideoConfig } from "remotion";
import type { ArrowData } from "../data/scene";
import { kick, windowOpacity } from "../lib/keyframes";
import { bezierAngle, bezierPoint, toPath } from "../lib/geometry";
import { toPx } from "../lib/pitch";
import { useLayout, useSeconds } from "../lib/hooks";
import { FrameSvg } from "../../shared/FrameSvg";
import { theme } from "../lib/theme";

export const Arrow: React.FC<{ readonly arrow: ArrowData }> = ({ arrow }) => {
  const t = useSeconds();
  const { fps } = useVideoConfig();
  const layout = useLayout();

  if (t < arrow.from || t > arrow.to) {
    return null;
  }

  const px = arrow.points.map((m) => toPx(m, layout));
  const stroke = 5 * layout.fontScale;
  const opacity = windowOpacity(t, arrow.from, arrow.to, 0.35);

  if (arrow.kind === "lane") {
    const cut = arrow.cutAt !== undefined && t >= arrow.cutAt;
    const mid = {
      x: (px[0].x + px[px.length - 1].x) / 2,
      y: (px[0].y + px[px.length - 1].y) / 2,
    };
    const pop = cut
      ? spring({
          frame: Math.round((t - (arrow.cutAt ?? 0)) * fps),
          fps,
          config: { damping: 12, stiffness: 180 },
        })
      : 0;
    const x = 12 * layout.fontScale;
    return (
      <FrameSvg style={{ opacity }}>
        <path
          d={toPath(px)}
          fill="none"
          stroke={theme.overlay}
          strokeWidth={stroke * 0.8}
          strokeDasharray={`${stroke * 2.5} ${stroke * 1.8}`}
          strokeLinecap="round"
          opacity={cut ? 0.35 : 0.95}
        />
        {cut ? (
          <g
            transform={`translate(${mid.x} ${mid.y}) scale(${pop})`}
            stroke={theme.overlay}
            strokeWidth={stroke * 1.2}
            strokeLinecap="round"
          >
            <line x1={-x} y1={-x} x2={x} y2={x} />
            <line x1={-x} y1={x} x2={x} y2={-x} />
          </g>
        ) : null}
      </FrameSvg>
    );
  }

  // A "run" arrow. Two points become a straight line (control = midpoint).
  const start = px[0];
  const end = px[px.length - 1];
  const control =
    px.length === 3
      ? px[1]
      : { x: (start.x + end.x) / 2, y: (start.y + end.y) / 2 };

  const progress = interpolate(t, [arrow.from, arrow.from + 0.8], [0, 1], {
    easing: kick,
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const head = bezierPoint(start, control, end, progress);
  const angle = bezierAngle(start, control, end, progress);
  const headSize = stroke * 2.6;

  return (
    <FrameSvg style={{ opacity }}>
      <path
        d={toPath(px)}
        fill="none"
        stroke={theme.overlay}
        strokeWidth={stroke}
        strokeLinecap="round"
        pathLength={1}
        strokeDasharray={1}
        strokeDashoffset={1 - progress}
      />
      <polygon
        points={`0,0 ${-headSize},${-headSize * 0.55} ${-headSize},${headSize * 0.55}`}
        fill={theme.overlay}
        transform={`translate(${head.x} ${head.y}) rotate(${angle})`}
      />
    </FrameSvg>
  );
};
