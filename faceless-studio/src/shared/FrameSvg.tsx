/** A full-frame SVG layer. Overlays (arrows, zones, rings) draw into one. */
import type React from "react";
import { useVideoConfig } from "remotion";

export const FrameSvg: React.FC<{
  readonly children: React.ReactNode;
  readonly style?: React.CSSProperties;
}> = ({ children, style }) => {
  const { width, height } = useVideoConfig();
  return (
    <svg
      width={width}
      height={height}
      viewBox={`0 0 ${width} ${height}`}
      style={{ position: "absolute", top: 0, left: 0, ...style }}
    >
      {children}
    </svg>
  );
};
