/**
 * Where key text may go. Instagram and TikTok cover the top and bottom of a
 * 9:16 video with their own buttons, so we keep important text out of the
 * top 250 px and bottom 400 px. Shorter 4:5 feed posts get smaller margins.
 */
export const getSafeArea = (width: number, height: number) => {
  const isTall = height / width > 1.5;
  const top = isTall ? 250 : 130;
  const bottom = isTall ? 400 : 190;
  return {
    top,
    bottom,
    side: Math.round(width * 0.075),
    /** Height left for content between the safe margins. */
    available: height - top - bottom,
    /** Multiply sizes by this so they scale with the video width. */
    scale: width / 1080,
  };
};
