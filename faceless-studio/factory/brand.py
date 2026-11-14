"""
Makes the logos and profile pictures for both accounts, in code (no downloads).

    python make.py brand

Writes assets/logos/:
  vicecitycorner_wordmark.png   transparent watermark used on posts and reels
  vicecitycorner_avatar.png     1080x1080 profile picture (original design)
  footysmart_wordmark.png
  footysmart_avatar.png
"""
import math

from PIL import Image, ImageDraw

from .board import Board, draw_arrow, draw_pitch
from .config import INK, LIME, LOGOS, RED, WHITE, YELLOW
from .text import cap_height, font

PINK = "#FF3EA5"
NIGHT = (14, 6, 30)


def wordmark(words, path, height=150):
    """Two-colour Anton wordmark on a transparent background."""
    fnt = font(height)
    gap = height * 0.18
    widths = [fnt.getlength(w) for w, _ in words]
    cap = cap_height(fnt)
    img = Image.new("RGBA", (int(sum(widths) + gap * (len(words) - 1) + 40), cap + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x = 20
    for (w, colour), wd in zip(words, widths):
        d.text((x + 3, 20 + cap + 4), w, font=fnt, fill=(0, 0, 0, 150), anchor="ls")
        d.text((x, 20 + cap), w, font=fnt, fill=colour, anchor="ls")
        x += wd + gap
    img.save(path)


def vice_avatar(path):
    S = 1080
    img = Image.new("RGB", (S, S), NIGHT)
    d = ImageDraw.Draw(img)
    # sky gradient
    top, mid, low = (18, 0, 43), (120, 20, 120), (255, 120, 80)
    for y in range(S):
        t = y / S
        if t < 0.55:
            k = t / 0.55
            c = tuple(int(top[i] + (mid[i] - top[i]) * k) for i in range(3))
        else:
            k = (t - 0.55) / 0.45
            c = tuple(int(mid[i] + (low[i] - mid[i]) * k) for i in range(3))
        d.line([(0, y), (S, y)], fill=c)
    # striped sun
    sun = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sun)
    r = 300
    cx, cy = S // 2, 610
    for y in range(cy - r, cy + r):
        t = (y - (cy - r)) / (2 * r)
        c = (255, int(212 - 120 * t), int(92 + 40 * t), 255)
        half = (r * r - (y - cy) ** 2) ** 0.5
        sd.line([(cx - half, y), (cx + half, y)], fill=c)
    for i in range(6):
        y = cy + 20 + i * 42
        sd.rectangle([0, y, S, y + 6 + i * 4], fill=(0, 0, 0, 0))
    img.paste(sun, (0, 0), sun)
    # water
    d.rectangle([0, 840, S, S], fill=(30, 8, 60))
    for i in range(9):
        y = 860 + i * i * 3
        w = 260 - i * 18
        d.rectangle([S / 2 - w, y, S / 2 + w, y + 4], fill=PINK if i % 2 == 0 else "#FF9F43")
    # palm silhouette (left): curved trunk and tapered fronds
    pd = ImageDraw.Draw(img)
    pd.line([(120, 1080), (150, 820), (215, 560)], fill=(10, 3, 18), width=36, joint="curve")
    top = (215, 560)
    for ang, length in ((-170, 300), (-140, 330), (-110, 280), (-60, 300), (-25, 330), (5, 290), (35, 240)):
        a = math.radians(ang)
        tip = (top[0] + math.cos(a) * length, top[1] + math.sin(a) * length + 60)
        mid = (top[0] + math.cos(a) * length * 0.5, top[1] + math.sin(a) * length * 0.5 - 40)
        n = math.radians(ang + 90)
        pts = []
        for k in range(21):
            t = k / 20
            x = (1 - t) ** 2 * top[0] + 2 * (1 - t) * t * mid[0] + t * t * tip[0]
            y = (1 - t) ** 2 * top[1] + 2 * (1 - t) * t * mid[1] + t * t * tip[1]
            w = 34 * (1 - t) * (0.4 + t)
            pts.append((x + math.cos(n) * w, y + math.sin(n) * w))
        for k in range(20, -1, -1):
            t = k / 20
            x = (1 - t) ** 2 * top[0] + 2 * (1 - t) * t * mid[0] + t * t * tip[0]
            y = (1 - t) ** 2 * top[1] + 2 * (1 - t) * t * mid[1] + t * t * tip[1]
            w = 34 * (1 - t) * (0.4 + t)
            pts.append((x - math.cos(n) * w, y - math.sin(n) * w))
        pd.polygon(pts, fill=(10, 3, 18))
    # VCC monogram
    fnt = font(330)
    d = ImageDraw.Draw(img)
    d.text((S / 2 + 8, 380 + 10), "VCC", font=fnt, fill=(0, 0, 0), anchor="mm")
    d.text((S / 2, 380), "VCC", font=fnt, fill=WHITE, anchor="mm", stroke_width=10, stroke_fill=PINK)
    # ring
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, S, S], fill=255)
    out = Image.new("RGB", (S, S), NIGHT)
    out.paste(img, (0, 0), mask)
    ImageDraw.Draw(out).ellipse([12, 12, S - 12, S - 12], outline="#19F0FF", width=22)
    out.save(path)


def footy_avatar(path):
    S = 1080
    img = Image.new("RGBA", (S, S), (8, 14, 11, 255))
    b = Board((200, 150, 880, 640), view=(0, 34))
    draw_pitch(img, b)
    d = ImageDraw.Draw(img)
    draw_arrow(d, b, [(14, 28), (16, 14), (28, 9)], YELLOW, 20)
    draw_arrow(d, b, [(54, 26), (44, 24)], WHITE, 13, dashed=True)
    for (x, y), colour in (((14, 28), LIME), ((54, 26), LIME), ((30, 18), RED), ((42, 12), RED)):
        px, py = b.p(x, y)
        r = 46
        d.ellipse([px - r, py - r, px + r, py + r], fill=colour, outline=WHITE, width=9)
    d.text((S / 2, 765), "FOOTY", font=font(205), fill=WHITE, anchor="mm")
    d.text((S / 2, 915), "SMART", font=font(140), fill=LIME, anchor="mm")
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, S, S], fill=255)
    out = Image.new("RGB", (S, S), (8, 14, 11))
    out.paste(img.convert("RGB"), (0, 0), mask)
    ImageDraw.Draw(out).ellipse([12, 12, S - 12, S - 12], outline=LIME, width=24)
    out.save(path)


def make_all():
    LOGOS.mkdir(parents=True, exist_ok=True)
    wordmark([("VICE CITY", WHITE), ("CORNER", PINK)], LOGOS / "vicecitycorner_wordmark.png")
    wordmark([("FOOTY", WHITE), ("SMART", LIME)], LOGOS / "footysmart_wordmark.png")
    vice_avatar(LOGOS / "vicecitycorner_avatar.png")
    footy_avatar(LOGOS / "footysmart_avatar.png")
    return sorted(p.name for p in LOGOS.glob("*.png"))
