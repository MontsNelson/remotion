/**
 * The camera. Everything inside it (pitch, players, arrows) is zoomed,
 * panned and gently tilted together. Text overlays sit OUTSIDE the camera
 * so they stay sharp and in the safe zones.
 *
 * How it works: we pick the point the camera should look at (cx, cy in
 * metres), convert it to pixels, then translate the whole layer so that
 * point lands on the pitch centre, and scale by the zoom.
 */
import type React from "react";
import { AbsoluteFill } from "remotion";
import { scene } from "../data/scene";
import { cameraAt } from "../lib/keyframes";
import { toPx } from "../lib/pitch";
import { useLayout, useSeconds } from "../lib/hooks";

export const Camera: React.FC<{ readonly children: React.ReactNode }> = ({
  children,
}) => {
  const layout = useLayout();
  const t = useSeconds();
  const cam = cameraAt(scene.camera, t);
  const focus = toPx({ x: cam.cx, y: cam.cy }, layout);
  const pivot = layout.center;

  return (
    <AbsoluteFill style={{ perspective: 2200 }}>
      <AbsoluteFill
        style={{
          transformOrigin: `${pivot.x}px ${pivot.y}px`,
          translate: `${-(focus.x - pivot.x) * cam.zoom}px ${-(focus.y - pivot.y) * cam.zoom}px`,
          rotate: `x ${cam.tilt}deg`,
          scale: `${cam.zoom}`,
        }}
      >
        {children}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
