# Faceless Studio

One [Remotion](https://www.remotion.dev) project that makes the videos for
three faceless channels, each with its own template, colours and AI voice:

| Channel           | What it posts                        | Template       | Voice                        |
| ----------------- | ------------------------------------ | -------------- | ---------------------------- |
| **@FOOTYSMART10** | Animated football tactics explainers | `TacticsReel`  | British male (`bm_george`)   |
| **GTA 6 news**    | Countdown and news clips             | `GtaCountdown` | American male (`am_fenrir`)  |
| **Multiverse**    | AI parody "what if" recasts          | `RecastReel`   | American female (`af_heart`) |

Every template renders as a Reel (1080x1920) and as a feed post (1080x1350).
The plan for running all three is in **[PLAN.md](./PLAN.md)**.

## Run it

```bash
npm install
npm start                        # Remotion Studio: preview every video live
pip install -r scripts/requirements.txt   # once, for the voiceover
```

## Make a video

1. Edit the channel's data file (text, timings, facts, shots).
2. Edit the matching `*voiceover.json` and record it:
   `python scripts/voiceover.py <path to the voiceover.json>`
3. Preview in Studio, then render:

```bash
npm run render:football   # out/tactics.mp4 + out/tactics-feed.mp4
npm run render:gta        # out/gta.mp4 + out/gta-feed.mp4
npm run render:recast     # out/recast.mp4 + out/recast-feed.mp4
```

Step-by-step guides per channel:
[football](./docs/football-guide.md), [GTA](./docs/gta-guide.md),
[multiverse](./docs/recast-guide.md).

## How the code is organised

```
PLAN.md                 The plan for running the three channels
docs/                   One guide per channel
scripts/voiceover.py    Records narration with the free Kokoro voice model
src/
  Root.tsx              Registers every video, grouped by channel
  shared/               Fonts, safe areas, text fitting, voiceover player
  footysmart10/         Tactics reel: data/scene.ts holds the whole tactic
  gta/                  GTA clips: data/countdown.ts holds the facts
  multiverse/           Recasts: data/episode.ts holds the shots and prompts
public/
  voiceover/            Recorded narration, one folder per video
  clips/                Your AI-generated clips for the multiverse channel
```

## Voiceover

`scripts/voiceover.py` speaks each line of a voiceover script with
[Kokoro](https://github.com/hexgrad/kokoro), a free text-to-speech model
(Apache-2.0) that runs offline. British voices start with `b`, American
voices with `a`; `m` is male and `f` is female. The first run downloads the
model (about 120 MB) from the npm registry into `.voice-model/` and checks
its checksum. The script warns you if a line overlaps the next one.

## Packages used

- `remotion`, `@remotion/cli` (the scaffold)
- `@remotion/google-fonts` for Anton and Inter
- `@remotion/media` to play voiceover and video clips

Backgrounds, pitches, sunsets and overlays are drawn in code, so no game
artwork, club badges or film footage is bundled.
