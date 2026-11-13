# GTA channel guide: a new clip every day

Each clip is driven by `src/gta/data/countdown.ts` (what is shown) and
`src/gta/data/countdown-voiceover.json` (what is said).

## Daily countdown (until launch)

1. In `countdown.ts`, set `postDate` to the day you will post
   (`YYYY-MM-DD`). The big number updates itself.
2. In `countdown-voiceover.json`, change the `hook` line to match, for
   example "G T A 6 is just five days away." Write "G T A" with spaces
   so the voice says the letters.
3. Record and render:

   ```bash
   python scripts/voiceover.py src/gta/data/countdown-voiceover.json
   npm run render:gta
   ```

On launch day set `showCountdown` to `false` and change the `kicker` (for
example "OUT NOW") and the facts.

## News clips (after launch)

Keep the same template and swap the six fact cards for the story: a
`label` (short, upper case) and a `value` (one line). Time each card's `at`
to the moment the narration mentions it.

## Before you post: check the facts

Prices, dates and editions change. Check every number against Rockstar's
Newswire or a major outlet on the day. If something is a rumour, say so on
screen ("RUMOUR") or leave it out.

## Keep it a fan channel

- Leave the disclaimer on the end card.
- Don't re-upload Rockstar trailers or artwork; use the synthwave
  background, or your own gameplay captures after launch.
- See PLAN.md for the logo and name advice.
