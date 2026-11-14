import json, sys
sys.path.insert(0, "work")
import build_plan_vice
posts = build_plan_vice.build()
try:
    import build_plan_footy
    posts += build_plan_footy.build()
except ImportError:
    pass
import build_plan_managers
posts += build_plan_managers.build()
plan = {
  "notes": {
    "vice": ["Launch week: daily carousels plus reels on Sat, Mon, Wed, Thu and Fri.",
             "19 Nov is launch day: five posts from 00:05. Post the 00:05 one only once the game unlocks.",
             "Facts were checked on 14 Nov. Re-read each CHECK BEFORE POSTING note."],
    "footy": ["Hard launch: a reel or carousel every day this week.",
              "International break until 17 Nov, so it's evergreen tactics first.",
              "Newcastle v Arsenal is Sat 21 Nov at 17:30: the Arsenal corners reel goes out that morning.",
              "Manager tactics: five 45-second reels at 21:00 (with 4:5 feed versions) plus two Arteta carousels."]},
  "swaps": [{"account": "footy", "text": "Sunday 22 Nov 18:00: the Sunday run may replace the systems poll with a Newcastle v Arsenal breakdown."}],
  "posts": posts,
}
json.dump(plan, open("content/plans/2026-11-14_launch-fortnight.json", "w"), indent=2, ensure_ascii=False)
print(len(posts), "posts")
