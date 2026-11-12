/**
 * The ONE place where metres become pixels.
 *
 * The pitch is 105 m long and 68 m wide. We draw it vertically (the long side
 * runs top to bottom) because the video is vertical. `getLayout()` works out
 * how big the pitch can be for a given video size while keeping key text out
 * of the Reels safe zones, and `toPx()` converts any metre point to pixels.
 */
import type { Metres } from "../data/scene";

export const PITCH = { length: 105, width: 68 };

export type Layout = {
  width: number;
  height: number;
  /** Pixels at the top and bottom where Instagram overlays its own UI. */
  safeTop: number;
  safeBottom: number;
  /** Pixels per metre. */
  scale: number;
  /** Where the pitch rectangle sits inside the frame, in pixels. */
  pitch: { left: number; top: number; width: number; height: number };
  /** Centre of the pitch rectangle, in pixels. Used as the camera pivot. */
  center: { x: number; y: number };
  /** Multiply font sizes by this so text scales with the video width. */
  fontScale: number;
};

export const getLayout = (width: number, height: number): Layout => {
  // Tall 9:16 videos (Reels) get the official safe zones. Shorter formats
  // (4:5 feed posts) get smaller margins so the pitch stays big.
  const isTall = height / width > 1.5;
  const safeTop = isTall ? 250 : 130;
  const safeBottom = isTall ? 400 : 190;
  const sideMargin = Math.round(width * 0.065);

  const availableWidth = width - sideMargin * 2;
  const availableHeight = height - safeTop - safeBottom;

  const scale = Math.min(
    availableWidth / PITCH.width,
    availableHeight / PITCH.length,
  );

  const pitchWidth = PITCH.width * scale;
  const pitchHeight = PITCH.length * scale;
  const left = (width - pitchWidth) / 2;
  const top = safeTop + (availableHeight - pitchHeight) / 2;

  return {
    width,
    height,
    safeTop,
    safeBottom,
    scale,
    pitch: { left, top, width: pitchWidth, height: pitchHeight },
    center: { x: left + pitchWidth / 2, y: top + pitchHeight / 2 },
    fontScale: width / 1080,
  };
};

/** Convert a point in metres to a pixel position inside the frame. */
export const toPx = (m: Metres, layout: Layout) => ({
  x: layout.pitch.left + m.x * layout.scale,
  y: layout.pitch.top + m.y * layout.scale,
});

/** Convert a distance in metres to pixels. */
export const metresToPx = (metres: number, layout: Layout) =>
  metres * layout.scale;
