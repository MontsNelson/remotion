/**
 * countdown.ts — THE FILE YOU EDIT FOR EACH GTA NEWS CLIP.
 *
 * Facts below were checked on 13 Nov 2026 against news coverage of
 * Rockstar's announcements. Re-check anything that may have changed
 * before you post (prices, dates, trailers).
 *
 * Times are in seconds from the start of the clip.
 * The narration lives in countdown-voiceover.json; keep the two in sync.
 */

export type Fact = { at: number; label: string; value: string };

export const countdown = {
  durationInSeconds: 23,

  /** Your handle, shown on the end card. */
  handle: "@YOURGTAHANDLE",

  /** Small pill at the top, and a tag beside it. */
  kicker: "GTA 6 COUNTDOWN",
  tag: "FAN NEWS",

  /**
   * The countdown. Days left = releaseDate minus postDate, so set
   * postDate to the day you will post the clip. Use YYYY-MM-DD.
   * Set showCountdown to false for a plain news clip.
   */
  showCountdown: true,
  postDate: "2026-11-13",
  releaseDate: "2026-11-19",
  hookLines: { before: "GTA 6 IS", after: "DAYS AWAY" },
  compactLabel: "DAYS TO GO",

  /** The hook (big countdown) runs until this second. */
  hookEndsAt: 3,

  /** Fact cards. Each slides in at `at`; time them to the narration. */
  facts: [
    { at: 3.2, label: "RELEASE", value: "THU 19 NOV 2026" },
    { at: 6.0, label: "CONSOLES", value: "PS5 · XBOX SERIES X|S" },
    { at: 8.0, label: "PC", value: "NO DATE YET" },
    { at: 9.6, label: "MAP", value: "VICE CITY, LEONIDA" },
    { at: 11.9, label: "PLAY AS", value: "JASON & LUCIA" },
    { at: 14.1, label: "PRICE (US)", value: "$79.99 · ULTIMATE $99.99" },
  ] as Fact[],

  outro: {
    from: 18.6,
    follow: "FOLLOW",
    question: "Day one, or waiting for reviews?",
    cta: "COMMENT BELOW",
  },

  /** Always shown on the end card. Keep it. */
  disclaimer:
    "Unofficial fan channel. Not affiliated with Rockstar Games or Take-Two Interactive.",

  voiceover: { enabled: true, volume: 1 },
};

/** Whole days between two YYYY-MM-DD dates (never negative). */
export const daysBetween = (from: string, to: string) =>
  Math.max(0, Math.round((Date.parse(to) - Date.parse(from)) / 86_400_000));
