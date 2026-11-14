# The plan: running three faceless channels with AI

> **Update 14 Nov:** the daily autopilot (`tasks/DAILY_TASK.md`, `SETUP_PC.md`) now runs
> Vice City Corner and Footy Smart from Monty's PC; the multiverse channel is **AI Studio**
> (@ms_ai_studio26) and is made by hand with Higgsfield.

Written 13 November 2026. GTA 6 launches on Thursday 19 November, so the
GTA channel comes first this week.

## 1. The three channels at a glance

|                  | FootySmart10                                | GTA 6 news                             | Multiverse                            |
| ---------------- | ------------------------------------------- | -------------------------------------- | ------------------------------------- |
| **Promise**      | "Understand football tactics in 30 seconds" | "Everything GTA 6, fast and accurate"  | "Famous scenes, wrong characters"     |
| **Format**       | Animated pitch explainer, 25–30 s           | Countdown and fact-card clips, 15–25 s | AI-generated parody shots, 15–25 s    |
| **Template**     | `TacticsReel` (done)                        | `GtaCountdown` (done)                  | `RecastReel` (done, needs your clips) |
| **Voice**        | British male, George                        | American male, Fenrir                  | American female, Heart                |
| **Posts**        | 3 a week                                    | Daily to launch, then 4 a week         | 2–3 a week                            |
| **Hardest part** | Picking good tactics                        | Staying accurate                       | Generating good clips                 |
| **Risk level**   | Low                                         | Medium (trademark)                     | High (likeness and copyright)         |

Post the same video to Instagram Reels, TikTok and YouTube Shorts. The
feed version (1080x1350) is for the Instagram grid.

## 2. How every video gets made

The same six steps for all three channels. Claude can do steps 1 and 2;
the studio does 3 to 5.

1. **Idea.** Pick from the idea bank below or ask Claude for 10 new ones.
2. **Script.** Fill in the channel's data file and voiceover script.
3. **Voice.** `python scripts/voiceover.py <script>` records the narration
   and warns if any line is too long.
4. **Preview.** `npm start` opens Remotion Studio; scrub through it.
5. **Render.** `npm run render:football`, `render:gta` or `render:recast`.
6. **Post and log.** Upload, write the caption, then record the numbers in
   your tracking sheet 48 hours later (section 8).

Budget about 30–45 minutes per football or GTA video once you are used to
it. Multiverse episodes take longer because of clip generation.

## 3. FootySmart10: tactics explainers

**Already built:** the high press trap video, with British narration.

**Content pillars**

1. **Tactic explainers.** One idea per video: the press trap, inverted
   full-backs, the false nine, a low block, overloads to isolate.
2. **"Why it worked."** After a big weekend, recreate one goal's build-up
   with generic Team A and Team B. Name the real match in the caption, not
   on screen with badges.
3. **Set pieces.** Corner routines, free-kick decoys, long throws.
4. **Formations compared.** 4-3-3 against 3-5-2: where each one is weak.

**Idea bank (next ten)**

1. The 3-5-2 counter from a deep block.
2. Inverted full-back: building with a box midfield.
3. The false nine pulling centre-backs out.
4. How a low block protects the box.
5. Third-man runs to break a press.
6. Overload one side, switch to the other.
7. The near-post corner flick-on.
8. Rest defence: stopping the counter before it starts.
9. Pressing traps in the middle of the pitch.
10. Why teams play out from the back.

**Rules:** no club badges, real player faces or broadcast footage.
Generic numbers and colours keep it safe.

## 4. GTA 6 news: launch first

**Already built:** a countdown clip with six checked facts, an American
narrator and a fan disclaimer. Changing the day takes two edits
(see `docs/gta-guide.md`).

**Facts checked today**

| Fact                                                       | Status                                                                                              |
| ---------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| Release Thursday 19 November 2026                          | Confirmed by Rockstar; reconfirmed by the October launch trailer                                    |
| PS5 and Xbox Series X\|S                                   | Confirmed                                                                                           |
| PC                                                         | No date announced                                                                                   |
| Vice City, state of Leonida; Jason Duval and Lucia Caminos | Confirmed                                                                                           |
| Price, US: about $80 standard, $99.99 Ultimate             | Reported from Rockstar's pre-order details; one outlet says $79.99. Check the store before posting. |
| Trailer 3                                                  | Unverified; treat claims as fake until Rockstar posts it                                            |
| Preload start date                                         | Sources disagree (10 or 12 November)                                                                |

**Launch calendar**

| Date                | Post                                                                                                                                       |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Fri 13 Nov          | "6 days" countdown (rendered)                                                                                                              |
| Sat 14 – Wed 18 Nov | Countdown each day: 5, 4, 3, 2, 1 days. Swap one fact card per day for something new (editions, preload, map size claims marked as rumour) |
| Thu 19 Nov          | "OUT NOW": launch times, what to do first                                                                                                  |
| Week after          | Two a day: tips, hidden details, best early cars and missions, news recaps                                                                 |
| Then                | Four a week: news, guides, "10 things you missed"                                                                                          |

**The logo and name.** The account is @vicecitycorner6, which avoids
"GTA" in the name. The avatar still copies the official GTA VI logo style,
which Rockstar can report as brand impersonation. Use your own mark
instead (for example a palm-and-sunset monogram in the same colours), with
"Unofficial GTA 6 news" in the bio. Keep the end-card disclaimer.

**Footage.** Don't re-upload trailers or press artwork. Before launch, use
the synthwave template. After launch, use your own gameplay captures and
check Rockstar's current policy on gameplay videos before monetising.

## 5. Multiverse: AI parody recasts

**Already built:** the episode template with a hook card, captioned shot
slots, an always-on "AI PARODY" badge and a follow card. Each empty slot
shows the prompt for that shot, so you can plan the timing before
generating anything.

**What changes from your original idea, and why.** Swapping real actors'
or footballers' faces into real film scenes runs into four problems:

1. **Real faces.** YouTube now lets any adult find and report AI copies of
   their likeness, and says labelling a video as AI is not a defence.
   TikTok bans using private people's likeness without consent and
   requires labels on realistic AI people.
2. **Film and TV footage.** Clips from films get matched automatically by
   copyright systems and claimed or muted, and the account can be struck.
3. **Footballers' image rights.** Players and clubs actively enforce them.
4. **Reach.** Platforms say they reduce reach for undisclosed AI content.

So the template is built for a version that can grow:

- **Stylised, not photorealistic.** Animated, claymation, anime or comic
  styles. Parody of _types_ ("the world's best boss", "a moody
  goalkeeper") instead of copies of real faces.
- **Newly generated scenes.** Recreate the _feel_ of a famous scene with an
  AI video tool. No ripped footage.
- **Labelled every time.** Badge on screen plus the platform's AI label.
- **A recurring original character.** The strongest version of this
  channel: one mascot character you own who keeps landing in famous film
  situations. You own it, so nobody can take it down.

**About Deep-Live-Cam.** I didn't use your Deep-Live-Cam fork. Its README
requires consent from the person whose face is used and a clear "deepfake"
label when posting. It is fine with your own face or someone who agrees,
but not with actors or footballers.

**Tools.** Any AI video generator that does 9:16 clips works: Kling,
Runway, Google Veo, OpenAI Sora, Pika, or Higgsfield (already connected
to your Claude account, though the connector can't generate clips from
here). Most refuse real celebrities anyway. Compare current prices; they
change often.

**Idea bank**

1. What if the world's best boss ran a Premier League dressing room
   (prompts already written in `episode.ts`).
2. A Victorian butler commentates a Sunday league match.
3. A space-movie crew tries to assemble flat-pack furniture.
4. A noir detective investigates who ate the last biscuit.
5. A medieval knight's first day at a call centre.
6. A pirate captain does a property tour.
7. The mascot character goes to a wedding speech, a heist planning
   meeting, and a penalty shoot-out.

## 6. Running it with AI each week

| Day       | Task                                                                | Who                 |
| --------- | ------------------------------------------------------------------- | ------------------- |
| Monday    | Ask Claude for next week's ideas and scripts for all three channels | Claude              |
| Tuesday   | Record voices, render football and GTA videos                       | Studio              |
| Wednesday | Generate multiverse clips, render episodes                          | You + AI video tool |
| Thursday  | Schedule everything for the week                                    | You                 |
| Daily     | Reply to comments for 15 minutes; note video ideas from them        | You                 |
| Sunday    | Fill in the tracking sheet; drop what didn't work                   | You                 |

**Scheduling:** Meta Business Suite schedules Instagram Reels for free.
TikTok and YouTube Studio both have built-in scheduling on desktop.

**Prompts to reuse with Claude**

- _Football:_ "Write a new scene.ts and voiceover.json for the FootySmart10
  tactics reel about [tactic]. British English, 30 seconds, six phases,
  same structure as the high press trap."
- _GTA:_ "Make today's GTA countdown: [n] days to go. Check the latest
  news first and only use facts confirmed by Rockstar or two major outlets;
  label anything else as a rumour."
- _Multiverse:_ "Give me 10 multiverse parody premises that use stylised
  original characters, no real people, then write the hook and 3 shot
  prompts for the best one."

## 7. Account set-up checklist

- [ ] One account per channel on Instagram, TikTok and YouTube.
- [ ] Switch each to a professional or creator account for stats.
- [ ] Bio: what the channel is, how often you post, "Unofficial" for GTA,
      "AI parody" for multiverse.
- [ ] Your own logo for the GTA channel (see section 4).
- [ ] Turn on the AI label when posting multiverse videos.
- [ ] Two-factor login on every account.
- [x] Handles in the data files: @FOOTYSMART10 and @VICECITYCORNER6.
- [x] AI Studio handle: @ms_ai_studio26 (first three episodes in `docs/ai-studio-episodes.md`).

## 8. What to measure

Track each post in a spreadsheet 48 hours after posting:

| Number                         | Why it matters                            |
| ------------------------------ | ----------------------------------------- |
| Views                          | Reach                                     |
| Average watch time / % watched | Whether the hook and pacing work          |
| Shares and saves               | The strongest signal for tactics and news |
| Comments                       | Ideas for the next video                  |
| Follows from the post          | Whether the channel promise lands         |

Every two weeks, keep the top three formats and drop the bottom three.

## 9. Making money (later)

Build an audience first. Options, roughly in order:

1. **Platform payouts** (YouTube Shorts revenue share, TikTok's creator
   programme, Instagram bonuses where offered). Each has its own
   eligibility rules, and TikTok's programme favours longer videos; check
   the current rules when you get close.
2. **Brand deals and affiliate links:** football coaching apps and kit for
   FootySmart10; gaming gear for GTA.
3. **Selling the templates:** the tactics template itself is a product for
   coaches and other creators.

Original templates matter here: reposted or "reused" content is often
refused for monetisation.

## 10. The next 30 days

| Week           | FootySmart10                       | GTA                         | Multiverse                             |
| -------------- | ---------------------------------- | --------------------------- | -------------------------------------- |
| 13–19 Nov      | Post the high press video + 2 more | Daily countdown, launch day | Set up accounts, test 2 video tools    |
| 20–26 Nov      | 3 posts                            | 2 a day for launch week     | Episode 1 (world's best boss)          |
| 27 Nov – 3 Dec | 3 posts                            | 4 posts                     | Design the mascot character, episode 2 |
| 4–10 Dec       | 3 posts, review numbers            | 4 posts, review numbers     | Episode 3, review numbers              |

## 11. Where the code lives

Everything is in `faceless-studio/` on the `claude/practical-bell-96tql0`
branch of your `remotion` fork. To give it its own repository, create an
empty repository on GitHub (for example `faceless-studio`), add it to a
Claude session, and ask Claude to move the folder there. Or do it yourself
from a clone of the fork:

```bash
git subtree split --prefix=faceless-studio -b faceless-studio
git push https://github.com/<you>/faceless-studio.git faceless-studio:main
```

## Sources

- Release date: [Rockstar Newswire](https://www.rockstargames.com/newswire/article/ak3ak31a49a221/grand-theft-auto-vi-is-now-set-to-launch-november-19-2026),
  [Rockstar on X](https://x.com/RockstarGames/status/1986540361011880167),
  [Vice](https://www.vice.com/en/article/gta-6-release-date-launch-times-new-zealand-method/)
- Launch trailer and characters: [The Escapist](https://www.escapistmagazine.com/gta-6-launch-trailer/),
  [G2A News](https://www.g2a.com/news/gta-6-news/gta-vi-launch-trailer-is-here-and-rockstar-puts-jason-and-lucia-front-and-center/)
- Price and preload: [Mac Observer](https://www.macobserver.com/news/gta-6-launch-day-release-date-platforms-price/),
  [The Gamer Scene](https://www.thegamerscene.news/gta-6),
  [Screen Rant](https://screenrant.com/gta-6-release-date-preorders-price-trailers-editions/)
- AI labels and likeness rules: [Uppbeat](https://uppbeat.io/blog/creator-news/new-ai-labels-on-instagram-and-youtube-tell-your-viewers-whats-real-and-tell-you-whats-been-flagged),
  [Storrito on TikTok's 2026 rules](https://storrito.com/resources/tiktoks-2026-ai-labeling-rules-and-what-they-signal-for-platform-governance/),
  [Lindsey Gamble on Instagram](https://www.lindseygamble.com/blog/instagram-updates-its-ai-generated-profile-label-and-limits-recommendations-for-undisclosed-profiles),
  [OpenArt creator guide](https://openart.ai/blog/creators-guide-ai-disclosure-2026/)

The AI-rules sources are secondary; check each platform's own policy page
before relying on a detail.
