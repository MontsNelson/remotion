/**
 * episode.ts — THE FILE YOU EDIT FOR EACH MULTIVERSE RECAST.
 *
 * How an episode is made:
 *   1. Paste each shot's `prompt` into your AI video tool and generate a
 *      vertical (9:16) clip about `seconds` long.
 *   2. Save the clips in public/clips/ and put their names in `file`,
 *      for example "clips/ep01-shot1.mp4". While `file` is null the video
 *      shows a placeholder with the prompt, so you can preview the timing.
 *   3. Edit episode-voiceover.json to match, run the voice generator, render.
 *
 * Ground rules this template is built around (see PLAN.md):
 *   - Stylised (animated, claymation, comic) characters, not photorealistic
 *     copies of real people's faces.
 *   - No footage ripped from films or TV: every shot is newly generated.
 *   - The AI PARODY badge stays on screen the whole time.
 */

export type Word = { text: string; colour: "white" | "cyan" | "magenta" };

export type Shot = {
  /** Path inside public/, or null to show the placeholder. */
  file: string | null;
  seconds: number;
  /** Short lower-third caption. Use null for none. */
  caption: string | null;
  /** The prompt you give your AI video tool for this shot. */
  prompt: string;
};

export const episode = {
  handle: "@MS_AI_STUDIO26",
  badge: "AI PARODY",

  hook: {
    seconds: 3.5,
    kicker: "MULTIVERSE",
    lines: [
      [{ text: "WHAT IF THE", colour: "white" }],
      [{ text: "WORLD'S BEST BOSS", colour: "cyan" }],
      [{ text: "RAN A DRESSING ROOM?", colour: "magenta" }],
    ] as Word[][],
  },

  shots: [
    {
      file: null,
      seconds: 4,
      caption: "Half-time team talk",
      prompt:
        "3D animated cartoon, vertical 9:16. An overconfident office manager in a cheap grey suit, holding a mug that says WORLD'S BEST BOSS, bursts into a football dressing room at half-time and gives a cringe pep talk. Players in plain unbranded kits stare blankly. Warm lighting, comedic timing, handheld documentary-style camera with a quick zoom on a player's face.",
    },
    {
      file: null,
      seconds: 4,
      caption: "The tactics board",
      prompt:
        "3D animated cartoon, vertical 9:16. The same manager draws on a tactics whiteboard, but the drawing is a stick-figure heart and the word TEAMWORK spelled wrong. A player raises a hand to object. Documentary-style camera, awkward pause, the manager looks straight at the camera.",
    },
    {
      file: null,
      seconds: 4,
      caption: "Man of the match... trophy?",
      prompt:
        "3D animated cartoon, vertical 9:16. After the match the manager hands out homemade paper trophies to every player, including the kit man. The players slowly start smiling. Confetti falls. Documentary-style camera, warm comedic ending.",
    },
  ] as Shot[],

  outro: {
    seconds: 3.5,
    follow: "FOLLOW",
    question: "Who should we drop into a film next?",
    cta: "COMMENT A NAME",
  },

  voiceover: { enabled: true, volume: 1 },
};

/** Total episode length in seconds: hook + every shot + outro. */
export const episodeSeconds = () =>
  episode.hook.seconds +
  episode.shots.reduce((sum, shot) => sum + shot.seconds, 0) +
  episode.outro.seconds;
