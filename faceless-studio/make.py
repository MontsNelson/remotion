"""
Faceless Studio: one command for everything.

  python make.py brand                      make logos and profile pictures
  python make.py carousel <spec.json>       one carousel  -> work/out/<name>/
  python make.py reel <spec.json>           one Vice City Corner reel
  python make.py footy-reel <spec.json>     one Footy Smart tactics reel (Remotion)
  python make.py plan <plan.json> [--force] [--only vice|footy]
                                            render every post in a plan into Google Drive,
                                            with captions, WEEK_SCHEDULE and the combined list
  python make.py check <folder>             quality check + contact sheets in work/check/
  python make.py archive                    move weeks older than 3 weeks into _archive
  python make.py log-news <vice|footy> <date> <headline> <url...> [--used]
  python make.py notify "<message>"         Windows notification (prints elsewhere)

A plan is JSON (see content/plans/ for real ones):
{
  "notes":  {"vice": ["..."], "footy": ["..."]},       # bullet points for WEEK_SCHEDULE
  "swaps":  [{"account": "vice", "text": "replace Thursday's 18:00 post with ..."}],
  "posts": [
    {"account": "vice", "date": "2026-11-16", "time": "18:00", "type": "carousel",
     "slug": "preload-is-live", "headline": "...", "spec": { ...carousel spec... },
     "caption": {"hook": "...", "body": ["..."], "question": "...",
                 "sources": [{"name": "IGN", "url": "https://..."}],
                 "hashtags": ["#gta6news"], "first_comment": "...", "alt_text": "...",
                 "story_idea": "...", "check": "..."},
     "breaking": false}
  ]
}
"""
import argparse
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

from factory import config, output

LOGS = config.ROOT / "logs"


def log(msg: str):
    LOGS.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%H:%M:%S")
    with open(LOGS / f"{dt.date.today().isoformat()}.txt", "a", encoding="utf-8") as f:
        f.write(f"{stamp} {msg}\n")
    print(msg, flush=True)


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def render_post(post: dict, folder: Path):
    from factory import carousel, footy_reel, reel
    spec = dict(post["spec"])
    spec.setdefault("account", post["account"])
    work = config.WORK / f"{post['account']}_{post['date']}_{post['slug']}"
    if post["type"] == "carousel":
        files = carousel.render(spec, folder)
        return f"{len(files)} slides"
    if post["type"] == "reel":
        if post["account"] == "footy":
            info = footy_reel.render(spec, folder, work, post["slug"])
        else:
            info = reel.render(spec, folder, work)
        return f"{info['seconds']:.1f}s reel"
    raise SystemExit(f"Unknown post type {post['type']}")


def cmd_plan(args):
    plan = load(args.plan)
    done, failed = [], []
    for post in sorted(plan["posts"], key=lambda p: (p["date"], p["time"])):
        if args.only and post["account"] != args.only:
            continue
        output.ensure_account_files(post["account"])
        folder = output.post_folder(post)
        marker = folder / ("reel.mp4" if post["type"] == "reel" else "1.jpg")
        if marker.exists() and not args.force:
            output.write_caption(post, folder)
            log(f"skip (already made): {folder.relative_to(config.drive_root())}")
            continue
        try:
            folder.mkdir(parents=True, exist_ok=True)
            started = time.time()
            what = render_post(post, folder)
            output.write_caption(post, folder)
            done.append(post)
            log(f"made {what} in {time.time() - started:.0f}s: {folder.relative_to(config.drive_root())}")
        except SystemExit as e:  # keep going with the other posts
            failed.append((post, str(e)))
            log(f"FAILED {post['account']} {post['date']} {post['slug']}: {e}")
    weeks = sorted({output.parse_date(p["date"]) - dt.timedelta(days=output.parse_date(p["date"]).weekday())
                    for p in plan["posts"]})
    for account_key in config.ACCOUNTS:
        for monday in weeks:
            path = output.write_week_schedule(account_key, plan, monday)
            if path:
                log(f"schedule: {path.relative_to(config.drive_root())}")
    both = output.write_both_accounts(plan)
    if both:
        log(f"combined list: {both}")
    log(f"plan done: {len(done)} made, {len(failed)} failed")
    if failed:
        sys.exit(1)


def contact_sheet(images, out, thumb_w=270):
    from PIL import Image
    thumbs = []
    for im in images:
        img = Image.open(im) if not isinstance(im, Image.Image) else im
        thumbs.append(img.convert("RGB").resize((thumb_w, round(img.height * thumb_w / img.width))))
    h = max(t.height for t in thumbs)
    sheet = Image.new("RGB", (len(thumbs) * (thumb_w + 8), h), "white")
    for i, t in enumerate(thumbs):
        sheet.paste(t, (i * (thumb_w + 8), 0))
    sheet.save(out, quality=85)
    return out


def check_post(folder: Path, report: list):
    """Checks one post folder and writes a contact sheet to look at."""
    from PIL import Image
    from factory import audio
    sheet_dir = config.WORK / "check"
    sheet_dir.mkdir(parents=True, exist_ok=True)
    name = folder.name
    cap = folder / "caption.txt"
    problems = []
    if not cap.exists():
        problems.append("no caption.txt")
    elif "Source:" not in cap.read_text(encoding="utf-8"):
        problems.append("caption has no Source: line")
    if (folder / "reel.mp4").exists():
        mp4 = folder / "reel.mp4"
        probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=width,height",
                                "-of", "json", str(mp4)], capture_output=True, text=True)
        info = json.loads(probe.stdout or "{}")
        dur = float(info.get("format", {}).get("duration", 0))
        dims = [(s.get("width"), s.get("height")) for s in info.get("streams", []) if s.get("width")]
        if dims and dims[0] != (1080, 1920):
            problems.append(f"reel is {dims[0]}, not 1080x1920")
        if not 5 <= dur <= 90:
            problems.append(f"reel length {dur:.1f}s")
        lufs = audio.loudness(mp4)
        if lufs is None or not -16.5 <= lufs <= -12.5:
            problems.append(f"loudness {lufs} LUFS (want about -14)")
        size_mb = mp4.stat().st_size / 1e6
        if size_mb > 250:
            problems.append(f"reel is {size_mb:.0f} MB")
        frames = []
        for frac in (0.1, 0.5, 0.92):
            out = sheet_dir / f"_frame_{frac}.jpg"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{dur * frac:.2f}", "-i", str(mp4),
                            "-frames:v", "1", str(out)], check=False)
            if out.exists():
                frames.append(out)
        if (folder / "cover.jpg").exists():
            frames.insert(0, folder / "cover.jpg")
        sheet = contact_sheet(frames, sheet_dir / f"{name}.jpg") if frames else None
        summary = f"{dur:.1f}s, {lufs} LUFS, {size_mb:.1f} MB"
    else:
        slides = sorted(folder.glob("[0-9]*.jpg"), key=lambda p: int(p.stem))
        if not slides:
            problems.append("no slides")
        for s in slides:
            w, h = Image.open(s).size
            if (w, h) != (1080, 1350):
                problems.append(f"{s.name} is {w}x{h}")
            if s.stat().st_size > 8e6:
                problems.append(f"{s.name} over 8 MB")
        sheet = contact_sheet(slides, sheet_dir / f"{name}.jpg") if slides else None
        summary = f"{len(slides)} slides"
    report.append((folder, summary, problems, sheet))


def cmd_check(args):
    root = Path(args.folder)
    folders = [p.parent for p in root.rglob("caption.txt")] or [root]
    report = []
    for folder in sorted(set(folders)):
        check_post(folder, report)
    bad = 0
    for folder, summary, problems, sheet in report:
        status = "OK " if not problems else "FIX"
        bad += bool(problems)
        print(f"{status} {folder.name}: {summary}" + (f" | {'; '.join(problems)}" if problems else "")
              + (f" | sheet: {sheet}" if sheet else ""))
    print(f"\n{len(report)} posts checked, {bad} need fixing. Look at the contact sheets before posting.")


def cmd_notify(args):
    message = args.message
    if os.name == "nt":
        script = config.ROOT / "windows" / "notify.ps1"
        subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script),
                        "-Title", "Faceless Studio", "-Message", message])
    print(f"NOTIFY: {message}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("brand")
    for name in ("carousel", "reel", "footy-reel"):
        p = sub.add_parser(name)
        p.add_argument("spec")
        p.add_argument("--out")
    p = sub.add_parser("plan")
    p.add_argument("plan")
    p.add_argument("--force", action="store_true")
    p.add_argument("--only", choices=list(config.ACCOUNTS))
    p = sub.add_parser("check")
    p.add_argument("folder")
    sub.add_parser("archive")
    p = sub.add_parser("log-news")
    p.add_argument("account", choices=list(config.ACCOUNTS))
    p.add_argument("date")
    p.add_argument("headline")
    p.add_argument("urls", nargs="*")
    p.add_argument("--used", action="store_true")
    p = sub.add_parser("notify")
    p.add_argument("message")
    args = ap.parse_args()

    if args.cmd == "brand":
        from factory import brand
        print("\n".join(brand.make_all()))
    elif args.cmd in ("carousel", "reel", "footy-reel"):
        spec = load(args.spec)
        name = Path(args.spec).stem
        out = Path(args.out) if args.out else config.WORK / "out" / name
        if args.cmd == "carousel":
            from factory import carousel
            print(carousel.render(spec, out))
        elif args.cmd == "reel":
            from factory import reel
            print(reel.render(spec, out, config.WORK / f"tmp_{name}"))
        else:
            from factory import footy_reel
            print(footy_reel.render(spec, out, config.WORK / f"tmp_{name}", name))
        print(f"-> {out}")
    elif args.cmd == "plan":
        cmd_plan(args)
    elif args.cmd == "check":
        cmd_check(args)
    elif args.cmd == "archive":
        for key in config.ACCOUNTS:
            moved = output.archive_old_weeks(key, dt.date.today())
            print(f"{key}: archived {moved or 'nothing'}")
    elif args.cmd == "log-news":
        output.log_news(args.account, args.date, args.headline, args.urls, args.used)
    elif args.cmd == "notify":
        cmd_notify(args)


if __name__ == "__main__":
    main()
