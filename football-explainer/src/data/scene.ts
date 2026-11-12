/**
 * scene.ts — THE ONE FILE YOU EDIT TO CHANGE THE TACTIC.
 *
 * Everything that describes the tactic lives here: the headline, the phases,
 * where every player starts and moves, where the ball goes, which arrows,
 * zones and highlights appear, and how the camera moves.
 *
 * Nothing in here is animation code. The components in src/components read
 * this data and animate it for you.
 *
 * Units:
 *   - Positions are in METRES on a 105 x 68 pitch.
 *       x runs across the pitch:  0 = left touchline, 68 = right touchline
 *       y runs down the pitch:    0 = TOP goal line, 105 = BOTTOM goal line
 *     The top goal belongs to Team B, the bottom goal belongs to Team A.
 *   - Times (`t`, `from`, `to`) are in SECONDS from the start of the video.
 */

// ---------------------------------------------------------------------------
// Types (you normally don't need to touch these)
// ---------------------------------------------------------------------------

/** A point on the pitch, in metres. */
export type Metres = { x: number; y: number };

/** A point on the pitch at a moment in time. */
export type Keyframe = Metres & { t: number };

export type PlayerData = {
  /** Shirt number shown inside the circle. */
  number: number;
  /** Where the player stands when the shape forms. */
  start: Metres;
  /**
   * Optional moves. Between two keyframes the player glides smoothly.
   * Repeat a position with a later `t` to make the player wait there.
   */
  moves?: Keyframe[];
};

export type TeamData = {
  name: string;
  players: PlayerData[];
  /** Which side of the frame the players slide in from during THE SHAPE. */
  enterFrom: "top" | "bottom";
};

export type PhaseData = {
  id: string;
  /** Lower-third caption. Use null for phases without a caption. */
  caption: string | null;
  from: number;
  to: number;
};

export type ArrowData = {
  /** "run" = solid curved arrow that draws on. "lane" = dashed passing lane. */
  kind: "run" | "lane";
  from: number;
  to: number;
  /** 2 points = straight line. 3 points = start, curve control, end. */
  points: Metres[];
  /** Lanes only: the second the lane gets cut off (shows a slash, dims it). */
  cutAt?: number;
};

export type ZoneData = {
  from: number;
  to: number;
  /** Corners of the shaded area, in metres. */
  points: Metres[];
  label?: string;
};

export type HighlightData = {
  from: number;
  to: number;
  team: "A" | "B";
  number: number;
};

export type CameraKeyframe = {
  t: number;
  /** 1 = whole pitch. 1.5 = zoomed in 50%. */
  zoom: number;
  /** The point (in metres) the camera looks at. */
  cx: number;
  cy: number;
  /** Tilt in degrees for the pseudo-3D feel. 0 = flat. */
  tilt: number;
};

export type HeadlineWord = {
  text: string;
  colour: "white" | "cyan" | "yellow";
};

// ---------------------------------------------------------------------------
// THE TACTIC: a 4-3-3 high press trap
// ---------------------------------------------------------------------------

export const scene = {
  /** Total length of the video in seconds. */
  durationInSeconds: 30,

  /** Seconds the pitch takes to fade in behind the hook headline. */
  pitchFadeInSeconds: 2.5,

  /** The second the 22 players start sliding into position. */
  playersEnterAt: 3.3,

  /** Small rounded pill shown above the headline. */
  tag: "TACTICS, EXPLAINED",

  /** The hook headline. One array per line. Colour key words cyan or yellow. */
  headline: [
    [{ text: "THE PRESS THAT", colour: "white" }],
    [{ text: "WINS THE BALL", colour: "cyan" }],
    [{ text: "IN 5 SECONDS", colour: "yellow" }],
  ] as HeadlineWord[][],

  /** The six phases of the video. Captions are shown as lower-thirds. */
  phases: [
    { id: "hook", caption: null, from: 0, to: 3 },
    { id: "setup", caption: "THE SHAPE", from: 3, to: 9 },
    { id: "trigger", caption: "THE TRIGGER", from: 9, to: 15 },
    { id: "squeeze", caption: "THE SQUEEZE", from: 15, to: 21 },
    { id: "payoff", caption: "THE PAYOFF", from: 21, to: 27 },
    { id: "outro", caption: null, from: 27, to: 30 },
  ] as PhaseData[],

  /** Outro screen. */
  outro: {
    follow: "FOLLOW",
    handle: "@FOOTYSMART10",
    question: "Which side would you spring the trap on, left or right?",
    cta: "TELL ME IN THE COMMENTS",
  },

  /**
   * Voiceover. The narration TEXT lives in src/data/voiceover.json, so the
   * voice generator (scripts/voiceover.py) can read it. After editing that
   * file, run `python scripts/voiceover.py` to re-record the clips.
   * Set `enabled` to false for a silent video.
   */
  voiceover: {
    enabled: true,
    /** 1 = full volume. */
    volume: 1,
  },

  /**
   * Optional background music. Put a royalty-free file in public/music.mp3
   * and flip `enabled` to true. Volume is kept low, fades in and out, and
   * dips further whenever the voiceover is speaking.
   */
  music: {
    enabled: false,
    file: "music.mp3",
    volume: 0.3,
  },

  teams: {
    /** Team A: the pressing side (cyan). Defends the BOTTOM goal. */
    A: {
      name: "Team A",
      enterFrom: "bottom",
      players: [
        { number: 1, start: { x: 34, y: 100 } },
        // Back four
        {
          number: 2,
          start: { x: 58, y: 72 },
          moves: [
            { t: 10, x: 58, y: 72 },
            { t: 14, x: 60, y: 48 },
            { t: 17.5, x: 60, y: 48 },
            { t: 19.5, x: 61, y: 42 },
            { t: 23, x: 61, y: 42 },
            { t: 26, x: 55, y: 38 },
          ],
        },
        {
          number: 5,
          start: { x: 42, y: 76 },
          moves: [
            { t: 10, x: 42, y: 76 },
            { t: 14, x: 44, y: 60 },
          ],
        },
        {
          number: 4,
          start: { x: 26, y: 76 },
          moves: [
            { t: 10, x: 26, y: 76 },
            { t: 14, x: 32, y: 62 },
          ],
        },
        {
          number: 3,
          start: { x: 10, y: 72 },
          moves: [
            { t: 10, x: 10, y: 72 },
            { t: 14, x: 18, y: 58 },
          ],
        },
        // Midfield three
        {
          number: 6,
          start: { x: 34, y: 60 },
          moves: [
            { t: 10, x: 34, y: 60 },
            { t: 14, x: 40, y: 46 },
            { t: 22, x: 40, y: 46 },
            { t: 25, x: 36, y: 30 },
          ],
        },
        {
          number: 8,
          start: { x: 46, y: 50 },
          moves: [
            { t: 10, x: 46, y: 50 },
            { t: 13, x: 48, y: 34 },
            { t: 17.5, x: 48, y: 34 },
            { t: 19.5, x: 51, y: 30 },
            { t: 23.3, x: 50, y: 30 },
            { t: 25.5, x: 50, y: 21 },
          ],
        },
        {
          number: 10,
          start: { x: 22, y: 50 },
          moves: [
            { t: 10, x: 22, y: 50 },
            { t: 14, x: 30, y: 42 },
          ],
        },
        // Front three
        {
          number: 7,
          start: { x: 54, y: 36 },
          moves: [
            { t: 10.5, x: 54, y: 36 },
            { t: 13.5, x: 57, y: 26 },
            { t: 17.5, x: 57, y: 26 },
            { t: 19.5, x: 60, y: 24 },
            { t: 20.5, x: 60, y: 24 },
            { t: 21.6, x: 62, y: 23 },
            { t: 22.8, x: 62, y: 23 },
            { t: 26, x: 56, y: 15 },
          ],
        },
        {
          number: 9,
          start: { x: 34, y: 30 },
          moves: [
            { t: 10.5, x: 34, y: 30 },
            { t: 13.5, x: 41, y: 22 },
            { t: 17, x: 41, y: 22 },
            { t: 19, x: 45, y: 19 },
            { t: 22.5, x: 45, y: 19 },
            { t: 24.2, x: 40, y: 14 },
            { t: 24.8, x: 40, y: 14 },
            { t: 26.5, x: 38, y: 5 },
          ],
        },
        {
          number: 11,
          start: { x: 14, y: 36 },
          moves: [
            { t: 10.5, x: 14, y: 36 },
            { t: 14, x: 24, y: 30 },
            { t: 22.5, x: 24, y: 30 },
            { t: 26, x: 21, y: 18 },
          ],
        },
      ],
    } as TeamData,

    /** Team B: building up from the back (orange-red). Defends the TOP goal. */
    B: {
      name: "Team B",
      enterFrom: "top",
      players: [
        {
          number: 1,
          start: { x: 34, y: 4 },
          moves: [
            { t: 24.5, x: 34, y: 4 },
            { t: 25.3, x: 31, y: 2.5 },
          ],
        },
        // Back four
        {
          number: 2,
          start: { x: 62, y: 18 },
          moves: [
            { t: 15, x: 62, y: 18 },
            { t: 17, x: 64, y: 22 },
            { t: 21.6, x: 64, y: 22 },
            { t: 24, x: 60, y: 27 },
          ],
        },
        {
          number: 5,
          start: { x: 44, y: 14 },
          moves: [
            { t: 11, x: 44, y: 14 },
            { t: 13, x: 40, y: 16 },
            { t: 22, x: 40, y: 16 },
            { t: 25, x: 36, y: 9 },
          ],
        },
        {
          number: 4,
          start: { x: 24, y: 14 },
          moves: [
            { t: 22, x: 24, y: 14 },
            { t: 25, x: 28, y: 8 },
          ],
        },
        {
          number: 3,
          start: { x: 6, y: 18 },
          moves: [
            { t: 22, x: 6, y: 18 },
            { t: 25, x: 14, y: 12 },
          ],
        },
        // Two holding midfielders
        {
          number: 6,
          start: { x: 28, y: 26 },
          moves: [
            { t: 22, x: 28, y: 26 },
            { t: 25, x: 30, y: 17 },
          ],
        },
        {
          number: 8,
          start: { x: 42, y: 26 },
          moves: [
            { t: 11, x: 42, y: 26 },
            { t: 13, x: 46, y: 28 },
            { t: 22, x: 46, y: 28 },
            { t: 25, x: 44, y: 24 },
          ],
        },
        // Attackers
        {
          number: 7,
          start: { x: 60, y: 40 },
          moves: [
            { t: 12, x: 60, y: 40 },
            { t: 14, x: 62, y: 36 },
          ],
        },
        { number: 10, start: { x: 34, y: 36 } },
        { number: 11, start: { x: 8, y: 40 } },
        { number: 9, start: { x: 34, y: 50 } },
      ],
    } as TeamData,
  },

  /**
   * The ball's path. It glides from one keyframe to the next.
   * Repeat a position with a later `t` to make the ball wait (a player has it).
   */
  ball: [
    { t: 3.5, x: 34, y: 4 }, // Team B goalkeeper has it
    { t: 7.4, x: 34, y: 4 },
    { t: 8.2, x: 44, y: 14 }, // to centre-back 5
    { t: 10.0, x: 44, y: 14 },
    { t: 10.8, x: 62, y: 18 }, // THE TRIGGER: out to the right-back
    { t: 15.0, x: 62, y: 18 },
    { t: 17.0, x: 64, y: 22 }, // right-back dribbles into the trap
    { t: 21.0, x: 64, y: 22 },
    { t: 21.6, x: 62, y: 23 }, // Team A 7 wins it
    { t: 22.2, x: 62, y: 23 },
    { t: 22.9, x: 50, y: 30 }, // quick pass to 8
    { t: 23.4, x: 50, y: 30 },
    { t: 24.2, x: 40, y: 14 }, // through ball to 9
    { t: 24.8, x: 40, y: 14 },
    { t: 25.3, x: 36.5, y: 0.6 }, // GOAL
    { t: 30, x: 36.5, y: 0.6 },
  ] as Keyframe[],

  /** The second the ball crosses the line. Triggers the goal flash. */
  goal: { t: 25.3, at: { x: 36.5, y: 0.6 } },

  /** Curved run arrows and dashed passing lanes. */
  arrows: [
    // THE TRIGGER: the front two angle their runs to show the ball outside
    {
      kind: "run",
      from: 10.5,
      to: 15,
      points: [
        { x: 54, y: 36 },
        { x: 60, y: 32 },
        { x: 57.5, y: 27 },
      ],
    },
    {
      kind: "run",
      from: 11,
      to: 15,
      points: [
        { x: 34, y: 30 },
        { x: 40, y: 28 },
        { x: 41, y: 23 },
      ],
    },
    // THE SQUEEZE: every passing lane out of the trap gets cut
    {
      kind: "lane",
      from: 15.2,
      to: 21.3,
      cutAt: 18.6,
      points: [
        { x: 64, y: 22 },
        { x: 40, y: 16 },
      ],
    },
    {
      kind: "lane",
      from: 15.6,
      to: 21.3,
      cutAt: 19.2,
      points: [
        { x: 64, y: 22 },
        { x: 46, y: 28 },
      ],
    },
    {
      kind: "lane",
      from: 16,
      to: 21.3,
      cutAt: 19.6,
      points: [
        { x: 64, y: 22 },
        { x: 62, y: 36 },
      ],
    },
    {
      kind: "run",
      from: 16,
      to: 21,
      points: [
        { x: 41, y: 22 },
        { x: 44, y: 22 },
        { x: 45, y: 19 },
      ],
    },
    {
      kind: "run",
      from: 16.3,
      to: 21,
      points: [
        { x: 48, y: 34 },
        { x: 51, y: 33 },
        { x: 51, y: 30 },
      ],
    },
    {
      kind: "run",
      from: 16.6,
      to: 21,
      points: [
        { x: 60, y: 48 },
        { x: 62, y: 45 },
        { x: 61, y: 42 },
      ],
    },
    {
      kind: "run",
      from: 16.9,
      to: 21,
      points: [
        { x: 57, y: 26 },
        { x: 61, y: 27 },
        { x: 61, y: 24 },
      ],
    },
    // THE PAYOFF: the striker's run in behind
    {
      kind: "run",
      from: 22.4,
      to: 24.6,
      points: [
        { x: 45, y: 19 },
        { x: 40, y: 18 },
        { x: 40, y: 14 },
      ],
    },
  ] as ArrowData[],

  /** Translucent yellow areas. */
  zones: [
    {
      from: 9.6,
      to: 21.4,
      label: "TRAP ZONE",
      points: [
        { x: 47, y: 7 },
        { x: 68, y: 7 },
        { x: 68, y: 34 },
        { x: 50, y: 34 },
      ],
    },
  ] as ZoneData[],

  /** Pulsing rings around a key player. */
  highlights: [
    { from: 10.8, to: 15, team: "B", number: 2 },
    { from: 15, to: 21.6, team: "A", number: 7 },
    { from: 24.2, to: 25.6, team: "A", number: 9 },
  ] as HighlightData[],

  /** Camera moves. The camera glides between these keyframes. */
  camera: [
    { t: 0, zoom: 1.06, cx: 34, cy: 52.5, tilt: 0 },
    { t: 3, zoom: 1.0, cx: 34, cy: 52.5, tilt: 0 },
    { t: 7, zoom: 1.0, cx: 34, cy: 52.5, tilt: 5 },
    { t: 9.5, zoom: 1.0, cx: 34, cy: 52.5, tilt: 5 },
    { t: 12.5, zoom: 1.45, cx: 50, cy: 25, tilt: 5 },
    { t: 15, zoom: 1.45, cx: 50, cy: 25, tilt: 5 },
    { t: 18, zoom: 1.65, cx: 54, cy: 26, tilt: 6 },
    { t: 21, zoom: 1.65, cx: 54, cy: 26, tilt: 6 },
    { t: 23, zoom: 1.35, cx: 48, cy: 22, tilt: 5 },
    { t: 25.3, zoom: 1.45, cx: 40, cy: 13, tilt: 5 },
    { t: 27, zoom: 1.15, cx: 36, cy: 30, tilt: 4 },
    { t: 30, zoom: 1.08, cx: 34, cy: 45, tilt: 3 },
  ] as CameraKeyframe[],
};

export type SceneData = typeof scene;
