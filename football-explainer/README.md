# Football tactics explainer (Remotion)

A vertical, animated football tactics explainer, made entirely in code with
[Remotion](https://www.remotion.dev). The default topic is a 4-3-3 high press
trap. Change the topic by editing **one file**: `src/data/scene.ts`.

Two outputs, same animation:

| Composition       | Size        | Use                             |
| ----------------- | ----------- | ------------------------------- |
| `TacticsReel`     | 1080 x 1920 | Instagram Reels, TikTok, Shorts |
| `TacticsReelFeed` | 1080 x 1350 | Instagram feed (4:5)            |

Both are 30 fps and 30 seconds long, with a British English voiceover
explaining each step.

## Run it

```bash
npm install
npm start          # opens Remotion Studio in your browser for live preview
```

## Render it

```bash
npx remotion render src/index.ts TacticsReel out/tactics.mp4        # Reel
npx remotion render src/index.ts TacticsReelFeed out/tactics-feed.mp4 # Feed
```

Or the shortcuts: `npm run render` and `npm run render:feed`.
Check still frames at 1, 6, 12, 18 and 25 seconds with `npm run stills`.

## Change the topic

Open `src/data/scene.ts`. Everything about the tactic lives there:
headline, phases and captions, player positions and moves, ball path,
arrows, zones, highlighted players, camera moves and the outro.
See [GUIDE.md](./GUIDE.md) for the one-page walkthrough.

## How the code is organised

```
scripts/
  voiceover.py        Records the narration clips (British English voice)
  requirements.txt    Python packages for the generator
public/voiceover/     The recorded narration clips
src/
  index.ts            Registers the root (Remotion boilerplate)
  Root.tsx            Registers the two compositions (Reel and Feed)
  TacticsReel.tsx     Stacks the layers and times the text overlays
  data/scene.ts       ALL the tactic data. Edit this to change the topic.
  data/voiceover.json The narration text and when each line starts
  data/voiceover-timings.json  Clip lengths (written by the generator)
  lib/
    pitch.ts          The one helper that turns metres into pixels
    keyframes.ts      Smooth interpolation between keyframes
    geometry.ts       Curve maths for arrows
    fonts.ts          Anton (headlines) and Inter (small text)
    theme.ts          Colours
    hooks.ts          useLayout() and useSeconds()
    FrameSvg.tsx      A full-frame SVG layer for overlays
  components/
    Pitch.tsx         Grass, stripes, lines
    Player.tsx        A numbered circle that slides in and glides around
    Ball.tsx          White ball with a motion trail
    Arrow.tsx         Curved run arrows and dashed passing lanes
    Zone.tsx          Translucent pressing area
    PulseRing.tsx     Pulsing rings on a key player
    Flash.tsx         Goal burst
    Camera.tsx        Zoom, pan and tilt for everything on the pitch
    Headline.tsx      The hook headline and tag pill
    Caption.tsx       Lower-third captions
    Outro.tsx         Follow + question screen
    Voiceover.tsx     Plays the narration clips at the right moments
    Music.tsx         Optional background music
```

Pitch coordinates are in metres on a 105 x 68 pitch. `x` runs across
(0 = left touchline, 68 = right), `y` runs down (0 = top goal line,
105 = bottom goal line). Times are in seconds.

## Voiceover

The narration text is in `src/data/voiceover.json`. The audio clips in
`public/voiceover/` are generated from it, offline, with the free
[Kokoro](https://github.com/hexgrad/kokoro) text-to-speech model (Apache-2.0)
in a British English voice:

```bash
pip install -r scripts/requirements.txt   # once (needs Python 3.10+)
python scripts/voiceover.py               # re-records every line
```

The first run downloads the voice model (about 120 MB) from the npm
registry into `.voice-model/` and checks its checksum. The clips for the
current tactic are already included, so you only need this when you change
the narration.

## Optional music

Put a royalty-free track at `public/music.mp3` and set
`music.enabled: true` in `src/data/scene.ts`. It plays quietly, fades
in and out, and dips under the voiceover. No music is bundled.

## Packages used

- `remotion` and `@remotion/cli` (the scaffold)
- `@remotion/google-fonts` for Anton and Inter
- `@remotion/media` to play the voiceover clips

Nothing else. Arrows, zones and the pitch are plain SVG.

Team names are "Team A" and "Team B" and players are numbers only, so there
are no club badges, player names or likenesses to worry about.
