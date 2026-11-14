"""
Settings for both accounts, in one place.

Paths are relative to the project folder, so the same code runs on Windows
and Linux. Machine-specific values (where Google Drive lives) come from
settings.json next to make.py; copy settings.example.json to start.
"""
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
FONTS = ASSETS / "fonts"
LOGOS = ASSETS / "logos"
LIBRARY = ROOT / "library"          # Rockstar screenshots (never committed)
WORK = ROOT / "work"                # temporary render files
CONTENT = ROOT / "content"          # the JSON specs Claude writes

W_POST, H_POST = 1080, 1350         # carousels (4:5)
W_REEL, H_REEL, FPS = 1080, 1920, 30

# Shared colours (the "viral news" text system)
WHITE = "#FFFFFF"
YELLOW = "#FFE14D"
CYAN = "#3FE0C5"
RED = "#E8452C"
LIME = "#B8F34A"
INK = "#0B0F0C"


def _load_settings():
    path = ROOT / "settings.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


SETTINGS = _load_settings()


def drive_root() -> Path:
    """The 'Faceless Accounts' folder inside Google Drive for desktop."""
    if SETTINGS.get("drive_root"):
        return Path(SETTINGS["drive_root"])
    if os.name == "nt":
        return Path(r"G:\My Drive\Faceless Accounts")
    return ROOT / "drive-preview" / "Faceless Accounts"


ACCOUNTS = {
    "vice": {
        "name": "Vice City Corner",
        "handle": "@vicecitycorner6",
        "drive_folder": "GTA 6 - Vice Daily",
        "accent": CYAN,             # [c]...[/c]
        "pill_bg": RED,
        "pill_fg": WHITE,
        "logo": LOGOS / "vicecitycorner_wordmark.png",
        "voice": SETTINGS.get("vice_voice", "am_fenrir"),
        "voice_speed": 1.15,
        "music": "synthwave",
        "follow_line": "Follow @vicecitycorner6 for daily GTA 6 news",
        "image_credit": "Image: Rockstar Games",
        "music_mood": "dark synthwave",
        "base_hashtags": ["#gta6", "#gtavi", "#gta", "#rockstargames"],
        "news_log": "news_log.csv",
    },
    "footy": {
        "name": "Footy Smart",
        "handle": "@footysmart10",
        "drive_folder": "Footy",
        "accent": LIME,
        "pill_bg": LIME,
        "pill_fg": INK,
        "logo": LOGOS / "footysmart_wordmark.png",
        "voice": SETTINGS.get("footy_voice", "bm_george"),
        "voice_speed": 1.1,
        "music": "lofi",
        "follow_line": "Follow @footysmart10 for football tactics explained",
        "image_credit": "",
        "music_mood": "calm lo-fi house",
        "base_hashtags": ["#football", "#tactics", "#premierleague", "#footballtactics"],
        "news_log": "footy_news_log.csv",
    },
}


def account(key: str) -> dict:
    if key not in ACCOUNTS:
        raise SystemExit(f"Unknown account '{key}'. Use one of: {', '.join(ACCOUNTS)}")
    return ACCOUNTS[key]


# Screenshots never to use: they risk Instagram's nudity rules.
BLOCKED_IMAGES = {"Port_Gellhorn_07"}


def library_image(name: str) -> Path:
    """Finds a screenshot by name, with or without .jpg, in library/ or its subfolders."""
    stem = name[:-4] if name.lower().endswith(".jpg") else name
    stem = stem.replace("library/", "")
    if stem in BLOCKED_IMAGES:
        raise SystemExit(f"{stem} is on the blocked list (nudity risk on Instagram). Pick another image.")
    direct = LIBRARY / f"{stem}.jpg"
    if direct.exists():
        return direct
    for found in LIBRARY.rglob(f"{stem}.jpg"):
        return found
    raise SystemExit(
        f"Screenshot '{stem}.jpg' is not in library/. Copy the Rockstar screenshots "
        "from Drive (01 Rockstar Screenshots) into library/."
    )
