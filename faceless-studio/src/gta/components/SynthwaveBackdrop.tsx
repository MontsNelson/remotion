/**
 * An original synthwave sunset: gradient sky, striped sun, city skyline,
 * shimmering sea and two swaying palm trees. Drawn entirely in SVG, so no
 * game artwork or footage is used.
 */
import type React from "react";
import { interpolate, useVideoConfig } from "remotion";
import { useSeconds } from "../../shared/useSeconds";
import { gtaTheme } from "../theme";

/** A fixed, made-up skyline: [x as share of width, width, height] in px at 1080 wide. */
const SKYLINE: [number, number, number][] = [
  [0.02, 60, 90],
  [0.08, 46, 150],
  [0.13, 70, 110],
  [0.2, 40, 210],
  [0.25, 64, 140],
  [0.31, 52, 260],
  [0.37, 80, 120],
  [0.45, 44, 190],
  [0.5, 66, 300],
  [0.57, 50, 170],
  [0.62, 72, 230],
  [0.69, 40, 130],
  [0.74, 58, 280],
  [0.8, 70, 150],
  [0.87, 48, 200],
  [0.92, 66, 110],
];

/** One palm tree. `flip` mirrors it so the right-hand tree leans the other way. */
const Palm: React.FC<{
  readonly x: number;
  readonly baseY: number;
  readonly height: number;
  readonly flip: boolean;
  readonly sway: number;
}> = ({ x, baseY, height, flip, sway }) => {
  const dir = flip ? -1 : 1;
  const topX = x + dir * height * 0.28;
  const topY = baseY - height;
  const frond = height * 0.42;
  const angles = [-160, -130, -100, -70, -40, -15, 20];
  return (
    <g fill="#0A0312" stroke="#0A0312">
      <path
        d={`M ${x} ${baseY} Q ${x + dir * height * 0.02} ${baseY - height * 0.6} ${topX} ${topY}`}
        fill="none"
        strokeWidth={height * 0.05}
        strokeLinecap="round"
      />
      <g transform={`translate(${topX} ${topY}) rotate(${sway})`}>
        {angles.map((a) => (
          <path
            key={a}
            transform={`rotate(${flip ? 180 - a : a})`}
            d={`M 0 0 Q ${frond * 0.5} ${-frond * 0.22} ${frond} ${frond * 0.18} Q ${frond * 0.5} ${frond * 0.02} 0 0 Z`}
          />
        ))}
      </g>
    </g>
  );
};

export const SynthwaveBackdrop: React.FC = () => {
  const { width: W, height: H, durationInFrames, fps } = useVideoConfig();
  const t = useSeconds();
  const total = durationInFrames / fps;
  const s = W / 1080;
  const horizon = H * 0.6;
  const sunR = 250 * s;
  const sunY = interpolate(
    t,
    [0, total],
    [horizon - 70 * s, horizon - 150 * s],
  );
  const sway = Math.sin(t * 1.3) * 3;

  // Gaps cut into the lower half of the sun, getting taller towards the bottom.
  const gaps = [0, 1, 2, 3, 4, 5].map((i) => ({
    y: sunY + sunR * (0.1 + i * 0.16),
    h: 4 * s + i * 4 * s,
  }));

  return (
    <svg
      width={W}
      height={H}
      viewBox={`0 0 ${W} ${H}`}
      style={{ position: "absolute", inset: 0 }}
    >
      <defs>
        <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor={gtaTheme.skyTop} />
          <stop offset="0.45" stopColor={gtaTheme.skyMid} />
          <stop offset="0.8" stopColor={gtaTheme.pink} />
          <stop offset="1" stopColor={gtaTheme.orange} />
        </linearGradient>
        <linearGradient id="sun" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor={gtaTheme.sunTop} />
          <stop offset="1" stopColor={gtaTheme.pink} />
        </linearGradient>
        <linearGradient id="sea" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#3A0A5C" />
          <stop offset="1" stopColor={gtaTheme.night} />
        </linearGradient>
        <mask id="sunGaps">
          <rect x={0} y={0} width={W} height={H} fill="white" />
          {gaps.map((g, i) => (
            <rect key={i} x={0} y={g.y} width={W} height={g.h} fill="black" />
          ))}
        </mask>
      </defs>

      <rect x={0} y={0} width={W} height={horizon} fill="url(#sky)" />
      <circle
        cx={W / 2}
        cy={sunY}
        r={sunR}
        fill="url(#sun)"
        mask="url(#sunGaps)"
      />

      {/* Skyline */}
      {SKYLINE.map(([x, w, h], i) => (
        <rect
          key={i}
          x={x * W}
          y={horizon - h * s}
          width={w * s}
          height={h * s}
          fill="#1A0530"
        />
      ))}

      {/* Sea with shimmering reflection lines */}
      <rect x={0} y={horizon} width={W} height={H - horizon} fill="url(#sea)" />
      {Array.from({ length: 14 }, (_, i) => {
        const y = horizon + 18 * s + i * i * 3.2 * s;
        const half = (180 - i * 8) * s * (1 + 0.15 * Math.sin(t * 2 + i));
        return (
          <rect
            key={i}
            x={W / 2 - half}
            y={y}
            width={half * 2}
            height={(2 + i * 0.4) * s}
            fill={i % 2 === 0 ? gtaTheme.pink : gtaTheme.orange}
            opacity={0.55 - i * 0.03}
          />
        );
      })}

      <Palm
        x={70 * s}
        baseY={H * 0.95}
        height={700 * s}
        flip={false}
        sway={sway}
      />
      <Palm
        x={W - 60 * s}
        baseY={H * 0.98}
        height={560 * s}
        flip
        sway={-sway}
      />

      {/* Darken the middle so text stays readable */}
      <rect x={0} y={0} width={W} height={H} fill="rgba(5, 0, 15, 0.35)" />
    </svg>
  );
};
