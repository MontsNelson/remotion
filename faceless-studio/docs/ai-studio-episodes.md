# AI Studio (@ms_ai_studio26): first three episodes

Each episode is a hook card, three AI clips and a follow card, about 19 seconds.
The clips come from **Higgsfield** (Seedance 2.0 works well; on the Starter plan
use mode **fast**, 720p). The studio adds the hook, captions, narration, the
**AI PARODY** badge and the end card (`src/multiverse/`, see `docs/recast-guide.md`).

**How to make a clip in Higgsfield**
1. Open Higgsfield > Video > Seedance 2.0.
2. Aspect ratio **9:16**, duration **5 s**, mode **fast**, audio **off** (the studio adds narration).
3. Paste the prompt, generate, download the MP4.
4. Save it as `public/clips/epXX-shotY.mp4` and set that shot's `file` in
   `src/multiverse/data/episode.ts`. Then `npm run render:recast`.

**Rules that keep the account safe:** stylised characters only (animation,
claymation, comic). No real actors', players' or celebrities' faces, names or
voices. No footage from films or TV. Keep the AI PARODY badge on and switch on
Instagram's AI label when posting.

Credits: you have 13.88 credits on the Starter plan. Generate one test clip
first to see how many credits a 5-second clip costs before doing a full episode.

---

## Episode 1: The world's best boss in a dressing room

**Hook:** WHAT IF THE / WORLD'S BEST BOSS / RAN A DRESSING ROOM?
**Narration (hook):** "What if the world's best boss ran a Premier League dressing room?"

| Shot | Caption | Prompt |
| --- | --- | --- |
| 1 | Half-time team talk | 3D animated cartoon, vertical 9:16. An overconfident office manager in a cheap grey suit, holding a mug that says WORLD'S BEST BOSS, bursts into a football dressing room at half-time and gives a cringe pep talk. Players in plain unbranded kits stare blankly. Warm lighting, comedic timing, handheld documentary-style camera with a quick zoom on a player's face. |
| 2 | The tactics board | 3D animated cartoon, vertical 9:16. The same manager draws on a tactics whiteboard, but the drawing is a stick-figure heart and the word TEAMWORK spelled wrong. A player raises a hand to object. Documentary-style camera, awkward pause, the manager looks straight at the camera. |
| 3 | Man of the match... trophy? | 3D animated cartoon, vertical 9:16. After the match the manager hands out homemade paper trophies to every player, including the kit man. The players slowly start smiling. Confetti falls. Documentary-style camera, warm comedic ending. |

**Outro narration:** "Follow for more. Who should we drop in next?"
**Caption:** What if the world's best boss ran a Premier League dressing room? 😂 AI parody, all characters are made up. Who should we drop in next? #aiparody #aivideo #football #dressingroom #funnyvideos

---

## Episode 2: A medieval knight on VAR duty

**Hook:** WHAT IF A / MEDIEVAL KNIGHT / WAS ON VAR?
**Narration (hook):** "What if a medieval knight was in charge of VAR?"

| Shot | Caption | Prompt |
| --- | --- | --- |
| 1 | Checking the offside | Claymation stop-motion style, vertical 9:16. A knight in full shiny armour sits in a cramped VAR booth full of TV screens, squinting at a frozen football replay through his visor and measuring the screen with a long wooden ruler. Candles on the desk next to the monitors. Comedic, slightly jerky stop-motion movement. |
| 2 | Consulting the scroll | Claymation stop-motion style, vertical 9:16. The knight unrolls an enormous parchment scroll of rules that spills across the floor of the VAR booth, while a small clay referee on a monitor waits impatiently, tapping his foot. Warm candlelight mixed with blue screen light. |
| 3 | Decision: by the sword | Claymation stop-motion style, vertical 9:16. The knight stands, raises his sword dramatically, and a trumpet player in the corner blows a fanfare. On the screen the clay referee points to the penalty spot. Confetti made of tiny paper flags. Big comedic ending. |

**Outro narration:** "Follow for more. Who should we drop in next?"
**Caption:** Honestly might be faster than the real thing 🗡️ AI parody, all characters are made up. Who should run VAR next? #aiparody #var #football #claymation #aivideo

---

## Episode 3: The nature documentary, Sunday league edition

**Hook:** SUNDAY LEAGUE / LIKE A / NATURE DOCUMENTARY
**Narration:** this one is narrated all the way through, in a calm British voice
(`bm_george`, speed 1.0). Write it as a hushed wildlife documentary.

| Shot | Caption | Narration | Prompt |
| --- | --- | --- | --- |
| 1 | The keeper awakens | "Dawn. The Sunday league goalkeeper emerges, slowly, from his car." | 3D animated cartoon, vertical 9:16, misty early morning at a muddy local football pitch. A sleepy amateur goalkeeper in an oversized unbranded jersey climbs out of a small hatchback, stretching, holding a bacon sandwich. Shot like a wildlife documentary: slow telephoto zoom, soft morning light, dew on the grass. |
| 2 | The warm-up ritual | "He performs the ancient warm-up ritual. Two stretches. Mostly, he talks." | 3D animated cartoon, vertical 9:16. The same goalkeeper does one half-hearted stretch, then leans on the goalpost chatting, gesturing wildly, while teammates jog past. Wildlife documentary framing from behind long grass, slow push-in. |
| 3 | The save | "And then, against all the odds... the save of his life." | 3D animated cartoon, vertical 9:16. In slow motion the goalkeeper launches into a spectacular full-stretch dive and tips a shot over the bar, mud spraying everywhere, teammates frozen in disbelief. Golden backlight, wildlife documentary slow-motion style. |

**Outro narration:** "Follow for more. Which Sunday league legend should we film next?"
**Caption:** Every Sunday league keeper ever 🧤 AI parody, all characters are made up. Tag your keeper. #sundayleague #grassroots #aiparody #football #goalkeeper

---

### Turning an episode on in the studio

Episode 1 is already in `src/multiverse/data/episode.ts`. For episodes 2 and 3,
copy that file's `hook`, `shots` and `outro` values from the tables above, then
update `src/multiverse/data/episode-voiceover.json` with the narration lines and
run `python scripts/voiceover.py src/multiverse/data/episode-voiceover.json`.
