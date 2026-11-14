"""
Where finished posts go, and the text files that go with them.

Google Drive layout (per account):
  <drive>/<account folder>/02 Ready Posts/
     2026-W47 (16-22 Nov)/
        WEEK_SCHEDULE.txt + WEEK_SCHEDULE.csv
        Mon 16 Nov/
           1800_carousel_<slug>/   1.jpg 2.jpg ... caption.txt
           2000_reel_<slug>/       reel.mp4 cover.jpg caption.txt
     BREAKING/2026-11-18_<slug>/   post these straight away
     _archive/                     weeks older than 3 weeks
     POSTING_GUIDE.txt  stats.csv  news_log.csv
  <drive>/THIS_WEEK_BOTH_ACCOUNTS.txt   one checklist for both accounts
"""
import csv
import datetime as dt
import re
import shutil
from pathlib import Path

from . import config
from .text import plain

MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
DAYS = "Mon Tue Wed Thu Fri Sat Sun".split()
STATS_HEADER = ["date", "post_folder", "reach", "likes", "comments", "saves", "shares", "follows"]
NEWS_HEADER = ["date", "headline", "source_urls", "used"]


def ready_root(account_key: str) -> Path:
    acct = config.account(account_key)
    return config.drive_root() / acct["drive_folder"] / "02 Ready Posts"


def parse_date(s: str) -> dt.date:
    return dt.date.fromisoformat(s)


def week_folder_name(day: dt.date) -> str:
    monday = day - dt.timedelta(days=day.weekday())
    sunday = monday + dt.timedelta(days=6)
    year, week, _ = monday.isocalendar()
    if monday.month == sunday.month:
        span = f"{monday.day}-{sunday.day} {MONTHS[sunday.month - 1]}"
    else:
        span = f"{monday.day} {MONTHS[monday.month - 1]}-{sunday.day} {MONTHS[sunday.month - 1]}"
    return f"{year}-W{week:02d} ({span})"


def day_folder_name(day: dt.date) -> str:
    return f"{DAYS[day.weekday()]} {day.day} {MONTHS[day.month - 1]}"


def slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", plain(text).lower()).strip("-")
    return s[:48].rstrip("-") or "post"


def post_folder(post: dict) -> Path:
    day = parse_date(post["date"])
    hhmm = post["time"].replace(":", "")
    name = f"{hhmm}_{post['type']}_{post['slug']}"
    if post.get("breaking"):
        return ready_root(post["account"]) / "BREAKING" / f"{post['date']}_{post['slug']}"
    return ready_root(post["account"]) / week_folder_name(day) / day_folder_name(day) / name


def nice_when(post: dict) -> str:
    day = parse_date(post["date"])
    return f"{DAYS[day.weekday()]} {day.day} {MONTHS[day.month - 1]} {day.year} {post['time']}"


def write_caption(post: dict, folder: Path):
    """caption.txt in the order Monty pastes things into Meta Business Suite."""
    acct = config.account(post["account"])
    c = post.get("caption", {})
    lines = [f"POST AT: {nice_when(post)}   TYPE: {post['type']}",
             f"ACCOUNT: {acct['name']} ({acct['handle']})", "", "CAPTION:"]
    body = [c.get("hook", "")] + list(c.get("body", [])) + [c.get("question", "")]
    lines += [ln for ln in body if ln]
    sources = c.get("sources", [])
    if sources:
        lines.append("Source: " + ", ".join(s["name"] if isinstance(s, dict) else s for s in sources))
    if c.get("uses_rockstar_images", post["account"] == "vice") and acct["image_credit"]:
        lines.append(acct["image_credit"])
    lines.append(acct["follow_line"])
    tags = list(dict.fromkeys(acct["base_hashtags"] + c.get("hashtags", [])))[:12]
    lines += ["", "HASHTAGS:", " ".join(tags), "",
              "FIRST COMMENT:", c.get("first_comment", ""), "",
              "ALT TEXT:", c.get("alt_text", ""), "",
              "STORY IDEA:", c.get("story_idea", "")]
    if post["type"] == "carousel":
        lines += ["", "MUSIC (carousels only):", c.get("music_mood", acct["music_mood"])]
    check = c.get("check", "")
    lines += ["", "CHECK BEFORE POSTING:", check or "Nothing special: facts checked against the sources above."]
    urls = [s["url"] for s in sources if isinstance(s, dict) and s.get("url")]
    if urls:
        lines += ["", "SOURCE LINKS (for you, not for the caption):"] + urls
    (folder / "caption.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def ensure_account_files(account_key: str):
    root = ready_root(account_key)
    root.mkdir(parents=True, exist_ok=True)
    (root / "BREAKING").mkdir(exist_ok=True)
    (root / "_archive").mkdir(exist_ok=True)
    stats = root / "stats.csv"
    if not stats.exists():
        with open(stats, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(STATS_HEADER)
    log = root / config.account(account_key)["news_log"]
    if not log.exists():
        with open(log, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(NEWS_HEADER)
    guide_src = config.ROOT / "docs" / "POSTING_GUIDE.txt"
    if guide_src.exists():
        shutil.copyfile(guide_src, root / "POSTING_GUIDE.txt")


def log_news(account_key: str, date: str, headline: str, urls, used: bool):
    log = ready_root(account_key) / config.account(account_key)["news_log"]
    ensure_account_files(account_key)
    with open(log, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([date, headline, " ".join(urls), "yes" if used else "no"])


def write_week_schedule(account_key: str, plan: dict, monday: dt.date):
    """WEEK_SCHEDULE.txt/.csv for one account and one Monday-Sunday week."""
    sunday = monday + dt.timedelta(days=6)
    posts = [p for p in plan["posts"] if p["account"] == account_key and not p.get("breaking")
             and monday <= parse_date(p["date"]) <= sunday]
    if not posts:
        return None
    posts.sort(key=lambda p: (p["date"], p["time"]))
    folder = ready_root(account_key) / week_folder_name(monday)
    folder.mkdir(parents=True, exist_ok=True)
    acct = config.account(account_key)
    notes = plan.get("notes", {}).get(account_key, [])
    swaps = [s for s in plan.get("swaps", []) if s.get("account") == account_key]
    out = [f"{acct['name'].upper()} ({acct['handle']}) - WEEK SCHEDULE {week_folder_name(monday)}", ""]
    for s in swaps:
        out.append(f"SWAP: {s['text']}")
    if swaps:
        out.append("")
    if notes:
        out.append("THIS WEEK:")
        out += [f"- {n}" for n in notes]
        out.append("")
    rows = [("Day", "Time", "Type", "Folder", "Headline", "Status")]
    for p in posts:
        day = parse_date(p["date"])
        rows.append((day_folder_name(day), p["time"], p["type"],
                     f"{day_folder_name(day)}/{p['time'].replace(':', '')}_{p['type']}_{p['slug']}",
                     plain(p.get("headline", "")), "[ ]"))
    widths = [max(len(str(r[i])) for r in rows) for i in range(len(rows[0]))]
    widths[4] = min(widths[4], 70)
    for r in rows:
        out.append(" | ".join(str(v)[: widths[i]].ljust(widths[i]) for i, v in enumerate(r)))
    out += ["", "Times are UK time. Tick Status when scheduled. See POSTING_GUIDE.txt for the steps."]
    (folder / "WEEK_SCHEDULE.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
    with open(folder / "WEEK_SCHEDULE.csv", "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)
    return folder / "WEEK_SCHEDULE.txt"


def write_both_accounts(plan: dict):
    """One list for Sunday scheduling: both accounts' posts in this plan, sorted by day and time."""
    posts = [p for p in plan["posts"] if not p.get("breaking")]
    posts.sort(key=lambda p: (p["date"], p["time"], p["account"]))
    if not posts:
        return None
    first, last = parse_date(posts[0]["date"]), parse_date(posts[-1]["date"])
    rows = [("Account", "Day", "Time", "Type", "Folder path", "Headline", "Status")]
    for p in posts:
        acct = config.account(p["account"])
        rel = post_folder(p).relative_to(config.drive_root())
        rows.append((acct["name"], day_folder_name(parse_date(p["date"])), p["time"], p["type"], str(rel),
                     plain(p.get("headline", ""))[:70], "[ ]"))
    widths = [max(len(str(r[i])) for r in rows) for i in range(len(rows[0]))]
    title = f"BOTH ACCOUNTS - {day_folder_name(first)} to {day_folder_name(last)} {last.year}"
    lines = [title, "", "Schedule these in Meta Business Suite (see POSTING_GUIDE.txt). Times are UK time.", ""]
    lines += [" | ".join(str(v).ljust(widths[i]) for i, v in enumerate(r)) for r in rows]
    path = config.drive_root() / "THIS_WEEK_BOTH_ACCOUNTS.txt"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def archive_old_weeks(account_key: str, today: dt.date, keep_weeks=3):
    """Moves week folders older than keep_weeks into _archive (never deletes)."""
    root = ready_root(account_key)
    moved = []
    cutoff = today - dt.timedelta(weeks=keep_weeks)
    for folder in root.glob("20??-W??*"):
        m = re.match(r"(\d{4})-W(\d{2})", folder.name)
        if not m:
            continue
        monday = dt.date.fromisocalendar(int(m.group(1)), int(m.group(2)), 1)
        if monday + dt.timedelta(days=6) < cutoff:
            (root / "_archive").mkdir(exist_ok=True)
            shutil.move(str(folder), str(root / "_archive" / folder.name))
            moved.append(folder.name)
    return moved
