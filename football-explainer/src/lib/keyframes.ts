/**
 * Keyframe helpers. A keyframe is "be at this value at this second".
 * These helpers find the two keyframes around the current time and glide
 * between them with smooth easing, so nothing ever jumps.
 */
import { Easing, interpolate } from "remotion";
import type { CameraKeyframe, Keyframe, Metres } from "../data/scene";

type Timed = { t: number };

/** Smooth start and end, used for player and camera movement. */
export const smooth = Easing.inOut(Easing.cubic);

/** Fast start, slow end, used for passes and shots. */
export const kick = Easing.out(Easing.cubic);

/**
 * Returns which keyframe segment `t` is in and how far through it we are
 * (0 = at keyframe `index`, 1 = at keyframe `index + 1`).
 */
const segmentAt = <T extends Timed>(
  keyframes: T[],
  t: number,
  easing: (n: number) => number,
) => {
  if (t <= keyframes[0].t) {
    return { index: 0, progress: 0 };
  }
  const last = keyframes.length - 1;
  if (t >= keyframes[last].t) {
    return { index: last, progress: 0 };
  }
  for (let i = 0; i < last; i++) {
    const a = keyframes[i];
    const b = keyframes[i + 1];
    if (t >= a.t && t < b.t) {
      const progress =
        b.t === a.t
          ? 1
          : interpolate(t, [a.t, b.t], [0, 1], {
              easing,
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
            });
      return { index: i, progress };
    }
  }
  return { index: last, progress: 0 };
};

const lerp = (a: number, b: number, p: number) => a + (b - a) * p;

/** Position (in metres) along a list of keyframes at time `t` (seconds). */
export const pointAt = (
  keyframes: Keyframe[],
  t: number,
  easing: (n: number) => number = smooth,
): Metres => {
  const { index, progress } = segmentAt(keyframes, t, easing);
  const a = keyframes[index];
  const b = keyframes[Math.min(index + 1, keyframes.length - 1)];
  return { x: lerp(a.x, b.x, progress), y: lerp(a.y, b.y, progress) };
};

/** True while the keyframes describe movement at time `t`. */
export const isMovingAt = (keyframes: Keyframe[], t: number) => {
  const { index, progress } = segmentAt(keyframes, t, smooth);
  if (progress === 0 && index === keyframes.length - 1) {
    return false;
  }
  const a = keyframes[index];
  const b = keyframes[Math.min(index + 1, keyframes.length - 1)];
  return a.x !== b.x || a.y !== b.y;
};

/** Camera settings at time `t` (seconds). */
export const cameraAt = (keyframes: CameraKeyframe[], t: number) => {
  const { index, progress } = segmentAt(keyframes, t, smooth);
  const a = keyframes[index];
  const b = keyframes[Math.min(index + 1, keyframes.length - 1)];
  return {
    zoom: lerp(a.zoom, b.zoom, progress),
    cx: lerp(a.cx, b.cx, progress),
    cy: lerp(a.cy, b.cy, progress),
    tilt: lerp(a.tilt, b.tilt, progress),
  };
};

/**
 * Opacity that fades in at the start of a time window and out at the end.
 * `t` is seconds, `from`/`to` are the window, `fade` is the fade length.
 */
export const windowOpacity = (
  t: number,
  from: number,
  to: number,
  fade = 0.4,
) =>
  interpolate(t, [from, from + fade, to - fade, to], [0, 1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
