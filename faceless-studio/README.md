# Faceless Studio

Makes the posts for three faceless channels and saves them, ready to schedule,
into Google Drive. Two engines work together:

- **Python factory** (`make.py`, `factory/`): carousels for both accounts, Vice
  City Corner reels from Rockstar stills, AI voiceover (Kokoro), word-by-word
  captions, original music, Drive folders, captions, schedules and logs.
- **Remotion** (`src/`): the animated Footy Smart tactics reels.

| Account | What it posts | Voice |
| --- | --- | --- |
| **Vice City Corner** @vicecitycorner6 | GTA 6 news carousels + reels | American male (`am_fenrir`) |
| **Footy Smart** @footysmart10 | Tactics-board carousels + animated reels | British male (`bm_george`) |
| **AI Studio** @ms_ai_studio26 | AI parody "multiverse" recasts (made by hand) | American female (`af_heart`) |

- **Set up on the PC:** paste `SETUP_PC.md` into Claude Code.
- **Daily autopilot:** `tasks/DAILY_TASK.md` (runs at 07:00 via Task Scheduler).
- **Rules for every run:** `CLAUDE.md`. **Your Sunday steps:** `docs/POSTING_GUIDE.txt`.
- **The bigger plan:** `PLAN.md`.

## The factory by hand

```bash
python make.py --help
python make.py plan content/plans/2026-11-14_launch-fortnight.json   # render a whole plan into Drive
python make.py check "<Drive>/Faceless Accounts/Footy/02 Ready Posts"  # QA + contact sheets
python make.py carousel my-carousel.json      # one-off renders into work/out/
python make.py reel my-gta-reel.json
python make.py footy-reel content/examples/footy-reel-high-press.json
```

## Run it

```bash
npm install
npm start                        # Remotion Studio: preview every video live
pip install -r requirements.txt   # once, for the voiceover
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
