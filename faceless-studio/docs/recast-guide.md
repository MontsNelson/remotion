# Multiverse guide: making an episode

An episode is a hook card, three to five AI-generated shots, and a follow
card. Everything is set in `src/multiverse/data/episode.ts`.

1. **Pick a premise** that follows the ground rules in PLAN.md, for example
   "What if the world's best boss ran a Premier League dressing room?".
2. **Write the hook** (`hook.lines`, two or three short lines) and one
   `prompt` per shot. Start each prompt with the style ("3D animated
   cartoon", "claymation", "comic-book") and "vertical 9:16".
3. **Preview the timing** in Studio. While a shot's `file` is `null` the
   video shows a placeholder card with its prompt.
4. **Generate the clips** in your AI video tool, about `seconds` long each.
   Save them as `public/clips/ep02-shot1.mp4` and so on, and set each
   shot's `file` to `"clips/ep02-shot1.mp4"`.
5. **Narration**: edit `src/multiverse/data/episode-voiceover.json`. Set
   `videoLengthSeconds` to the hook + shots + outro total, and start the
   outro line just after the last shot ends. Record it:

   ```bash
   python scripts/voiceover.py src/multiverse/data/episode-voiceover.json
   ```

6. **Render**: `npm run render:recast`.
7. **Post** with the platform's AI label switched on (see PLAN.md).

The AI PARODY badge stays on screen for the whole video. Keep it.
