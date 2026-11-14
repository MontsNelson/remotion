"""
Carousels (1080x1350), one JPG per slide.

Two kinds, chosen by "kind" in the spec:

"news" (Vice City Corner): Rockstar screenshot, dark fade, red tag pill, headline.
{
  "account": "vice", "kind": "news",
  "tag": "TR3NDING",
  "headline": "[c]GTA 6[/c] IS FIVE DAYS AWAY AND [y]THE PRELOAD IS LIVE[/y]",
  "image": "Vice_City_27", "focus_x": 0.5,
  "slides": [
     "PLAIN TEXT SLIDE OVER THE SAME IMAGE",
     {"text": "...", "image": "Jason_Duval_11", "focus_x": 0.6},
     {"text": "...", "compare": {"left": "GTAV_Los_Santos_01", "left_label": "GTA V",
                                  "right": "Vice_City_15", "right_label": "GTA 6"}},
     "LAST SLIDE IS A QUESTION [y]FOR THE COMMENTS?[/y]"
  ]
}

"tactics" (Footy Smart): drawn tactics boards (see board.py).
{
  "account": "footy", "kind": "tactics",
  "tag": "TACTICS",
  "headline": "HOW [c]ARSENAL[/c] WIN [y]CORNERS[/y]",
  "cover_board": { ...board... },
  "slides": [{"text": "...", "board": { ...board... }}, ..., {"text": "QUESTION?"}]
}
"""
from pathlib import Path

from PIL import Image, ImageDraw

from . import config
from .board import draw_board
from .config import H_POST as H, W_POST as W, WHITE, YELLOW
from .text import add_logo, draw_block, font, pill

JPG_QUALITY = 93


# ---------- backgrounds ----------
def cover_crop(path: Path, w: int, h: int, focus_x: float = 0.5, focus_y: float = 0.5):
    img = Image.open(path).convert("RGB")
    scale = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * scale), round(img.height * scale)), Image.LANCZOS)
    left = round((img.width - w) * min(1, max(0, focus_x)))
    top = round((img.height - h) * min(1, max(0, focus_y)))
    return img.crop((left, top, left + w, top + h))


def bottom_fade(img, start=0.45, end=0.70):
    mask = Image.new("L", (1, img.height))
    for y in range(img.height):
        t = min(1, max(0, (y / img.height - start) / (end - start)))
        mask.putpixel((0, y), round(255 * t * t * (3 - 2 * t)))
    return Image.composite(Image.new("RGB", img.size, "black"), img, mask.resize(img.size))


def darken(img, amount):
    return Image.blend(img, Image.new("RGB", img.size, "black"), amount)


# ---------- shared bits ----------
def carousel_icon(d):
    x, y, s = W - 96, 40, 40
    d.rounded_rectangle([x + 11, y + 11, x + 11 + s, y + 11 + s], radius=11, outline="white", width=5)
    d.rounded_rectangle([x, y, x + s, y + s], radius=11, fill="white")


def swipe_dots(d, total, active=0):
    r, gap = 6, 22
    x0 = W / 2 - gap * (total - 1) / 2
    for i in range(total):
        cx = x0 + i * gap
        d.ellipse([cx - r, H - 36 - r, cx + r, H - 36 + r], fill="#FFFFFF" if i == active else "#6B6B6B")


def counter(d, number, total):
    d.text((W - 48, 76), f"{number}/{total}", font=font(44, "tag"), fill="white", anchor="rs")


def follow_line(img, acct, y):
    d = ImageDraw.Draw(img)
    d.text((W / 2, y), f"FOLLOW {acct['handle'].upper()}", font=font(62), fill=YELLOW, anchor="ms")


def watermark(img, acct):
    add_logo(img, acct["logo"], height=44, y=34, opacity=0.7)


# ---------- news (Vice City Corner) ----------
def news_slide_background(slide, spec):
    if isinstance(slide, dict) and slide.get("compare"):
        c = slide["compare"]
        half = W // 2
        left = cover_crop(config.library_image(c["left"]), half, H, c.get("left_focus_x", 0.5))
        right = cover_crop(config.library_image(c["right"]), W - half, H, c.get("right_focus_x", 0.5))
        bg = Image.new("RGB", (W, H))
        bg.paste(left, (0, 0))
        bg.paste(right, (half, 0))
        return darken(bg, 0.35), c
    image = slide.get("image") if isinstance(slide, dict) else None
    fx = slide.get("focus_x", 0.5) if isinstance(slide, dict) and image else spec.get("focus_x", 0.5)
    bg = cover_crop(config.library_image(image or spec["image"]), W, H, fx)
    return darken(bg, 0.6), None


def render_news(spec, out_dir: Path):
    acct = config.account(spec["account"])
    slides = spec.get("slides", [])
    total = len(slides) + 1
    files = []
    # cover
    bg = cover_crop(config.library_image(spec["image"]), W, H, spec.get("focus_x", 0.5))
    img = bottom_fade(bg)
    top, _ = draw_block(img, spec["headline"], acct["accent"], centre_x=W / 2, bottom=H - 92,
                        size=112, max_width=960, max_lines=5, shadow=False)
    pill(img, spec.get("tag", "TR3NDING").upper(), W / 2, top - 52, bg=acct["pill_bg"], fg=acct["pill_fg"], size=36)
    d = ImageDraw.Draw(img)
    swipe_dots(d, min(total, 6))
    carousel_icon(d)
    watermark(img, acct)
    files.append(save(img, out_dir / "1.jpg"))
    # slides
    for i, slide in enumerate(slides, start=2):
        text = slide["text"] if isinstance(slide, dict) else slide
        bg, compare = news_slide_background(slide, spec)
        img = bg.copy()
        d = ImageDraw.Draw(img)
        last = i == total
        if compare:
            # labels on each half, text in the lower third
            for label, cx, colour in ((compare.get("left_label", ""), W / 4, WHITE),
                                      (compare.get("right_label", ""), 3 * W / 4, acct["accent"])):
                if label:
                    pill(img, label.upper(), cx, 190, bg=(0, 0, 0), fg=colour, size=44)
            d.line([(W / 2, 120), (W / 2, H * 0.56)], fill=(255, 255, 255), width=4)
            draw_block(img, text, acct["accent"], centre_x=W / 2, centre_y=H * 0.72, size=74,
                       max_width=900, max_lines=5)
        else:
            centre = H / 2 - (70 if last else 0)
            _, bottom = draw_block(img, text, acct["accent"], centre_x=W / 2, centre_y=centre, size=80,
                                   max_width=900, max_lines=7)
            if last:
                follow_line(img, acct, bottom + 150)
        counter(d, i, total)
        watermark(img, acct)
        files.append(save(img, out_dir / f"{i}.jpg"))
    return files


# ---------- tactics (Footy Smart) ----------
def footy_background():
    img = Image.new("RGB", (W, H), (8, 14, 11))
    d = ImageDraw.Draw(img)
    for y in range(H):  # very subtle vertical gradient
        t = y / H
        d.line([(0, y), (W, y)], fill=(int(8 + 6 * t), int(14 + 10 * t), int(11 + 6 * t)))
    return img


def render_tactics(spec, out_dir: Path):
    acct = config.account(spec["account"])
    slides = spec.get("slides", [])
    total = len(slides) + 1
    files = []
    # cover: big board, dark fade, headline
    img = footy_background()
    draw_board(img, (40, 110, W - 40, 830), spec.get("cover_board", {"view": [0, 60]}))
    img = bottom_fade(img, 0.58, 0.72)
    top, _ = draw_block(img, spec["headline"], acct["accent"], centre_x=W / 2, bottom=H - 92,
                        size=118, max_width=960, max_lines=4, shadow=False)
    pill(img, spec.get("tag", "TACTICS").upper(), W / 2, top - 52, bg=acct["pill_bg"], fg=acct["pill_fg"], size=36)
    d = ImageDraw.Draw(img)
    swipe_dots(d, min(total, 6))
    carousel_icon(d)
    watermark(img, acct)
    files.append(save(img, out_dir / "1.jpg"))
    for i, slide in enumerate(slides, start=2):
        last = i == total
        img = footy_background()
        d = ImageDraw.Draw(img)
        if slide.get("board") and not last:
            draw_board(img, (50, 120, W - 50, 900), slide["board"])
            if slide.get("step"):
                pill(img, slide["step"].upper(), W / 2, 965, bg=acct["pill_bg"], fg=acct["pill_fg"], size=34)
            draw_block(img, slide["text"], acct["accent"], centre_x=W / 2, centre_y=1145, size=70,
                       max_width=940, max_lines=4)
        else:
            if slide.get("board"):
                draw_board(img, (50, 120, W - 50, 700), slide["board"])
                _, bottom = draw_block(img, slide["text"], acct["accent"], centre_x=W / 2, centre_y=900,
                                       size=78, max_width=920, max_lines=4)
            else:
                _, bottom = draw_block(img, slide["text"], acct["accent"], centre_x=W / 2, centre_y=H / 2 - 70,
                                       size=86, max_width=920, max_lines=6)
            if last:
                follow_line(img, acct, bottom + 140)
        counter(d, i, total)
        watermark(img, acct)
        files.append(save(img, out_dir / f"{i}.jpg"))
    return files


def save(img, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(path, quality=JPG_QUALITY)
    return path


def render(spec: dict, out_dir: Path):
    kind = spec.get("kind", "news")
    if kind == "news":
        return render_news(spec, out_dir)
    if kind == "tactics":
        return render_tactics(spec, out_dir)
    raise SystemExit(f"Unknown carousel kind '{kind}'. Use 'news' or 'tactics'.")
