# FootySmart10 guide: new tactic, re-render, upload

## 1. Swap in a new tactic (edit `src/footysmart10/data/scene.ts`)

Work top to bottom through the file. Keep `npm start` running in another
terminal and Remotion Studio shows every change live.

1. **Headline and tag.** `headline` is a list of lines; each line is a list
   of words with a colour (`white`, `cyan` or `yellow`). Keep lines to about
   14 characters so they fit at the large size.
2. **Phases.** `phases` sets the timeline in seconds and the lower-third
   captions. Keep the first phase (`hook`) and last phase (`outro`); rename
   or retime the ones in between. Change `durationInSeconds` if the total
   changes.
3. **Players.** Each team has 11 players with a `start` position in metres
   and optional `moves`. A move is `{ t, x, y }`: be at (x, y) at second t.
   To make a player wait, repeat the same position with a later `t`.
   Tip: draw the move _after_ its arrow so viewers see the arrow first.
4. **Ball.** `ball` is a list of `{ t, x, y }` keyframes. Repeat a position
   to make the ball sit with a player; a jump to a new position is a pass.
   Set `goal` to the second and spot where the ball crosses the line
   (or move it off-pitch, e.g. `t: 999`, if there is no goal).
5. **Arrows.** `kind: "run"` is a solid curved arrow (3 points: start,
   curve control, end; 2 points for straight). `kind: "lane"` is a dashed
   passing lane; add `cutAt` for the second it gets blocked.
6. **Zones and highlights.** `zones` are shaded polygons with a label.
   `highlights` put pulsing rings on a player (`team` and shirt `number`).
7. **Camera.** `camera` keyframes: `zoom` (1 = whole pitch), `cx`/`cy`
   (the metre point to look at), `tilt` (degrees). Zoom to around 1.5 on
   the area where the action happens.
8. **Outro.** `outro.handle` is your handle (currently `@FOOTYSMART10`);
   `outro.question` drives comments.

Coordinates: x 0 to 68 across, y 0 to 105 down. Top goal = Team B's,
bottom goal = Team A's.

## 2. Re-record the voiceover (edit `src/footysmart10/data/voiceover.json`)

The narration is a separate small file so the voice generator can read it.

1. Write one line per phase. `at` is the second the line starts; keep it
   just after the phase starts (for example 9.3 for a phase starting at 9).
2. Write numbers and names the way they should be _said_: "four-three-three",
   "Footy Smart Ten". Commas add short pauses.
3. Run the generator:

   ```bash
   pip install -r scripts/requirements.txt   # once
   python scripts/voiceover.py src/footysmart10/data/voiceover.json
   ```

   The first run downloads the voice model (about 120 MB) and keeps it in
   `.voice-model/`. Each run prints every clip's length and warns if a line
   runs into the next one. If it warns, shorten the text, raise `speed`
   (1.1 is brisk, 1.2 is fast), or move the next line later.

4. Change the narrator with `voice`. British voices: `bm_george` (default),
   `bm_fable`, `bm_lewis`, `bm_daniel`, `bf_emma`, `bf_isabella`, `bf_alice`,
   `bf_lily` (`bm` = male, `bf` = female).

## 3. Check it

```bash
npx remotion still src/index.ts TacticsReel out/check.png --frame=360
```

Look for: headline fits, captions sit above the bottom 400 px, nothing
important in the top 250 px, no two circles overlapping at key moments.

## 4. Render

```bash
npm run render:football   # out/tactics.mp4 (Reels) and out/tactics-feed.mp4 (feed)
```

Each render takes a few minutes on a laptop. The first render downloads a
headless Chrome once (about 150 MB) unless you already have one.

## 5. Upload

- **Reels:** upload `out/tactics.mp4`. Pick the cover from the hook (first
  second). The caption text and hashtags go in the post, not the video.
- **Feed:** upload `out/tactics-feed.mp4`.
- The voiceover is baked into the MP4. If you add a trending sound inside
  Instagram, turn its volume down so the narration stays clear.
- For baked-in background music instead, put a royalty-free file at
  `public/music.mp3`, set `music.enabled: true` in `scene.ts`, and
  re-render. It dips automatically under the voiceover.

## Troubleshooting

- Text looks wrong or a font is missing: run `npm install` again.
- Video is shorter or longer than expected: check `durationInSeconds` and
  the last phase's `to` value match.
- No sound: check `voiceover.enabled` is `true` in `scene.ts` and that
  `public/voiceover/footysmart10-high-press/` has a `.wav` for every line `id`.
- The voiceover is out of sync after you changed the text: run
  `python scripts/voiceover.py src/footysmart10/data/voiceover.json` again; the clips are not re-made
  automatically.
- A player jumps: two keyframes have the same `t`, or `moves` are not in
  time order. Keep `t` increasing.
