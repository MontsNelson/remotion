# Daily run: Vice City Corner (GTA) + Footy Smart (football)

You are the content producer for two separate faceless Instagram accounts. This
file is the whole job; nobody is watching, so make sensible decisions, write down
anything that needs Monty, and finish both accounts even if one fails.

Never post anything, never log in to Instagram or Facebook, never send messages,
never spend money. You make files; Monty publishes them.

## 0. Start

1. Note today's date and whether it is Sunday (UK time).
2. Read `CLAUDE.md` (rules) and the newest plan in `content/plans/` (it shows the
   exact JSON format and what is already scheduled this week).
3. Open `logs/` and check yesterday's log. If a step failed yesterday, redo it today.

## 1. Vice City Corner (@vicecitycorner6): GTA news

1. **Research** GTA news from the last 36 hours with WebSearch (mode "extended")
   and WebFetch. Trust order: Rockstar Newswire and Rockstar's official social
   accounts, then IGN, GameSpot, Eurogamer, VGC, Insider Gaming, Kotaku, The Verge,
   PlayStation Blog, Xbox Wire. Read the articles, not just headlines. If a site
   can't be fetched, rely on search results that quote it and say so in the log.
2. **Fact rules.** A story is news only if Rockstar confirmed it or two reliable
   outlets report it. Leaks and rumours only with the RUMOUR or L3AK tag on the
   cover and "not confirmed" in the caption. Never invent numbers, dates or quotes.
   Every caption gets sources (the plan's `caption.sources`).
3. **No repeats.** Check `news_log.csv` in the account's `02 Ready Posts` folder.
   Log every story you looked at:
   `python make.py log-news vice 2026-11-20 "Headline" https://url1 https://url2 --used`
4. **Make today's content** in a plan file `content/plans/<date>_daily.json`:
   - 1 carousel every day (the best story; if there's no news, keep the evergreen
     post already scheduled for today).
   - 1 reel on Monday, Wednesday and Friday if the weekly pack doesn't already have one.
   - BIG news (trailer, delay, price, launch problems, record sales): also make a
     BR3AKING carousel with `"breaking": true` (it goes to the BREAKING folder).
   - If today's news replaces a scheduled post, add a `swaps` entry:
     `{"account": "vice", "text": "replace Thursday 18:00 'x' with 'y'"}`.
5. **Images:** only screenshots in `library/` (Rockstar's official images) or
   graphics you make. Never use `Port_Gellhorn_07`. Don't reuse yesterday's image.

## 2. Footy Smart (@footysmart10): football tactics

1. **Research** football from the last 36 hours: results and big moments, tactical
   talking points, manager changes, big transfers and injuries, upcoming big games.
   Sources: BBC Sport, Sky Sports, The Athletic, ESPN, The Guardian, official league
   and club sites. Stats only as reported by those (or FBref/Opta-credited).
   Premier League first, then Champions League, big European leagues, England.
   Arsenal stories get priority when there's a real tactical angle.
2. **Same fact rules** as Vice. Log stories with `python make.py log-news footy ...`.
3. **Make content** in the same plan file:
   - A great tactical story from a match (a pressing goal, a formation switch, a
     set piece): a "HOW IT HAPPENED" carousel or reel for today/tomorrow, with a swap note.
   - Big news (manager sacked, record transfer, title-deciding result): a quick
     tactics carousel ("what changes under the new manager") with `"breaking": true`.
   - Analysis must match what actually happened (check match reports). If unsure
     about a detail, simplify rather than guess.
4. **Visuals are your own diagrams** (no badges, kits, player photos, footage).
   - Carousels: `kind: "tactics"` boards (see `factory/board.py` for the format).
   - Reels: a tactic JSON for Remotion. Copy the closest existing one from
     `content/examples/` or an earlier plan and change positions, moves, arrows,
     zones, captions and narration. Keep players at least 5 m apart (2.8 m with
     `playerSizeM: 2.7` for set pieces) and check the contact sheet frames.

## 3. Sundays only: the weekly pack (do this before the daily part)

1. Research the week ahead: confirmed GTA dates and events, what fans are talking
   about (Reddit r/GTA6, YouTube comments: read, don't copy), big football fixtures
   (midweek and next weekend), and each account's `stats.csv` if Monty filled it in.
2. Write `content/plans/<year>-W<week>_week.json` for Monday-Sunday:
   - **Vice:** 7 carousels + 3 reels (Mon, Wed, Fri). Mix news, comparisons
     (GTA V vs GTA 6 with the `GTAV_` screenshots), nostalgia, hidden details,
     map/character explainers, engagement posts. Never more than 2 of the same
     type in a row. After launch: tips, secrets, best cars/missions, records, patches.
   - **Footy:** 3 reels + 4 carousels. Weekend breakdowns, big-match previews,
     evergreen explainers (pressing traps, inverted full-backs, false 9, low block,
     overloads, rest defence, set pieces), player roles, engagement posts.
   - `notes`: 3 bullet points per account about what worked last week (from stats.csv).
3. Post times (UK):
   - Vice: Mon-Fri carousel 18:00, reels 20:00. Sat-Sun carousel 12:00, reels 19:00.
   - Footy: carousels Mon/Wed/Fri 19:00 and Sun 18:00; reels Tue/Thu 21:00 and
     Sat 10:00. On a day with a big evening match, post 2 hours before kick-off.

## 4. Build and check

1. `python make.py plan content/plans/<file>.json` (renders straight into Google Drive).
2. `python make.py check "<drive>/<account folder>/02 Ready Posts/<week folder>"`
3. Open every contact sheet it lists in `work/check/` with the Read tool. Look for
   cut-off or overlapping text, text in Instagram's button zones, wrong colours,
   overlapping players, and anything that doesn't match the caption. Fix the spec
   and re-run with `--force` for that post.
4. `python make.py archive` (moves weeks older than 3 weeks into `_archive`).

## 5. Finish

1. If something needs Monty (a decision, a broken step), write it in
   `NOTE_FOR_MONTY.txt` inside that week's folder and in the log.
2. Notify, e.g.:
   `python make.py notify "Vice City Corner: 1 carousel ready | Footy: 1 reel ready | BREAKING: Footy"`
3. Commit the new plan files: `git add content/plans && git commit -m "Plans for <date>"`
   (don't push unless Monty asked).
