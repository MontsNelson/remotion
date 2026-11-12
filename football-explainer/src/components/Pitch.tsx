/**
 * The pitch: deep green grass with mowing stripes and white lines.
 * Drawn as SVG. Every coordinate goes through toPx() so the pitch is
 * always 105 x 68 metres no matter the video size.
 */
import type React from "react";
import { PITCH, metresToPx, toPx } from "../lib/pitch";
import { useLayout } from "../lib/hooks";
import { theme } from "../lib/theme";
import { FrameSvg } from "../lib/FrameSvg";

export const Pitch: React.FC = () => {
  const layout = useLayout();
  const { pitch } = layout;
  const line = Math.max(2, metresToPx(0.2, layout));

  // Pixel positions of the standard pitch markings.
  const W = PITCH.width;
  const L = PITCH.length;
  const boxLeft = (W - 40.32) / 2;
  const sixLeft = (W - 18.32) / 2;
  const goalLeft = (W - 7.32) / 2;
  const arcHalf = Math.sqrt(9.15 * 9.15 - 5.5 * 5.5); // where the D meets the box

  const p = (x: number, y: number) => toPx({ x, y }, layout);
  const r = (m: number) => metresToPx(m, layout);

  const stripeCount = 10;
  const stripes = Array.from({ length: stripeCount }, (_, i) => i);

  return (
    <FrameSvg>
      {/* Grass */}
      <rect
        x={pitch.left}
        y={pitch.top}
        width={pitch.width}
        height={pitch.height}
        fill={theme.pitch}
      />
      {/* Mowing stripes: every second band is a touch lighter */}
      {stripes.map((i) =>
        i % 2 === 0 ? null : (
          <rect
            key={i}
            x={pitch.left}
            y={pitch.top + (pitch.height / stripeCount) * i}
            width={pitch.width}
            height={pitch.height / stripeCount}
            fill={theme.pitchStripe}
          />
        ),
      )}

      <g
        fill="none"
        stroke={theme.lines}
        strokeWidth={line}
        strokeOpacity={0.85}
      >
        {/* Outline and halfway line */}
        <rect
          x={pitch.left}
          y={pitch.top}
          width={pitch.width}
          height={pitch.height}
        />
        <line
          x1={p(0, L / 2).x}
          y1={p(0, L / 2).y}
          x2={p(W, L / 2).x}
          y2={p(W, L / 2).y}
        />
        {/* Centre circle and spot */}
        <circle cx={p(W / 2, L / 2).x} cy={p(W / 2, L / 2).y} r={r(9.15)} />
        <circle
          cx={p(W / 2, L / 2).x}
          cy={p(W / 2, L / 2).y}
          r={line}
          fill={theme.lines}
        />

        {/* Top penalty area, six-yard box, spot and D */}
        <rect
          x={p(boxLeft, 0).x}
          y={p(boxLeft, 0).y}
          width={r(40.32)}
          height={r(16.5)}
        />
        <rect
          x={p(sixLeft, 0).x}
          y={p(sixLeft, 0).y}
          width={r(18.32)}
          height={r(5.5)}
        />
        <circle
          cx={p(W / 2, 11).x}
          cy={p(W / 2, 11).y}
          r={line}
          fill={theme.lines}
        />
        <path
          d={`M ${p(W / 2 - arcHalf, 16.5).x} ${p(W / 2 - arcHalf, 16.5).y} A ${r(9.15)} ${r(9.15)} 0 0 0 ${p(W / 2 + arcHalf, 16.5).x} ${p(W / 2 + arcHalf, 16.5).y}`}
        />

        {/* Bottom penalty area, six-yard box, spot and D */}
        <rect
          x={p(boxLeft, L - 16.5).x}
          y={p(boxLeft, L - 16.5).y}
          width={r(40.32)}
          height={r(16.5)}
        />
        <rect
          x={p(sixLeft, L - 5.5).x}
          y={p(sixLeft, L - 5.5).y}
          width={r(18.32)}
          height={r(5.5)}
        />
        <circle
          cx={p(W / 2, L - 11).x}
          cy={p(W / 2, L - 11).y}
          r={line}
          fill={theme.lines}
        />
        <path
          d={`M ${p(W / 2 - arcHalf, L - 16.5).x} ${p(W / 2 - arcHalf, L - 16.5).y} A ${r(9.15)} ${r(9.15)} 0 0 1 ${p(W / 2 + arcHalf, L - 16.5).x} ${p(W / 2 + arcHalf, L - 16.5).y}`}
        />

        {/* Corner arcs */}
        <path
          d={`M ${p(0, 1).x} ${p(0, 1).y} A ${r(1)} ${r(1)} 0 0 0 ${p(1, 0).x} ${p(1, 0).y}`}
        />
        <path
          d={`M ${p(W - 1, 0).x} ${p(W - 1, 0).y} A ${r(1)} ${r(1)} 0 0 0 ${p(W, 1).x} ${p(W, 1).y}`}
        />
        <path
          d={`M ${p(W, L - 1).x} ${p(W, L - 1).y} A ${r(1)} ${r(1)} 0 0 0 ${p(W - 1, L).x} ${p(W - 1, L).y}`}
        />
        <path
          d={`M ${p(1, L).x} ${p(1, L).y} A ${r(1)} ${r(1)} 0 0 0 ${p(0, L - 1).x} ${p(0, L - 1).y}`}
        />

        {/* Goals (drawn just outside the goal lines) */}
        <rect
          x={p(goalLeft, -2).x}
          y={p(goalLeft, -2).y}
          width={r(7.32)}
          height={r(2)}
          fill="rgba(255,255,255,0.18)"
        />
        <rect
          x={p(goalLeft, L).x}
          y={p(goalLeft, L).y}
          width={r(7.32)}
          height={r(2)}
          fill="rgba(255,255,255,0.18)"
        />
      </g>
    </FrameSvg>
  );
};
