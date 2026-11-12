# One-page guide: new tactic, re-render, upload

## 1. Swap in a new tactic (edit `src/data/scene.ts`)

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
8. **Outro.** `outro.handle` is your handle; `outro.question` drives comments.

Coordinates: x 0 to 68 across, y 0 to 105 down. Top goal = Team B's,
bottom goal = Team A's.

## 2. Check it

```bash
npm run stills      # writes out/still-1s.png ... still-25s.png
```

Look for: headline fits, captions sit above the bottom 400 px, nothing
important in the top 250 px, no two circles overlapping at key moments.

## 3. Render

```bash
npm run render        # out/tactics.mp4       1080x1920 for Reels
npm run render:feed   # out/tactics-feed.mp4  1080x1350 for the feed
```

Each render takes a few minutes on a laptop. The first render downloads a
headless Chrome once (about 150 MB) unless you already have one.

## 4. Upload

- **Reels:** upload `out/tactics.mp4`. Pick the cover from the hook (first
  second). The caption text and hashtags go in the post, not the video.
- **Feed:** upload `out/tactics-feed.mp4`.
- Add music inside Instagram if you want a trending sound. If you prefer
  baked-in audio, put a royalty-free file at `public/music.mp3`, set
  `music.enabled: true` in `scene.ts`, and re-render.

## Troubleshooting

- Text looks wrong or a font is missing: run `npm install` again.
- Video is shorter or longer than expected: check `durationInSeconds` and
  the last phase's `to` value match.
- A player jumps: two keyframes have the same `t`, or `moves` are not in
  time order. Keep `t` increasing.
