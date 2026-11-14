"""
Text and drawing helpers shared by carousels and reels.

Markup in any headline or caption:
  [c]word[/c]  -> the account's accent colour (cyan for Vice City Corner, lime for Footy)
  [y]word[/y]  -> yellow
  everything else is white, ALL CAPS.
"""
import re
from functools import lru_cache

from PIL import Image, ImageDraw, ImageFont

from .config import FONTS, WHITE, YELLOW


@lru_cache(maxsize=None)
def font(size: float, kind: str = "head") -> ImageFont.FreeTypeFont:
    name = {"head": "Anton-Regular.ttf", "tag": "BebasNeue-Regular.ttf"}[kind]
    return ImageFont.truetype(str(FONTS / name), max(8, int(size)))


def parse(text: str, accent: str, upper: bool = True):
    """'[c]GTA 6[/c] IS [y]HERE[/y]' -> [('GTA', accent), ('6', accent), ('IS', white), ('HERE', yellow)]"""
    text = " ".join(str(text).split())
    words, colour = [], WHITE
    for part in re.split(r"(\[/?[cy]\])", text):
        if part == "[c]":
            colour = accent
        elif part == "[y]":
            colour = YELLOW
        elif part in ("[/c]", "[/y]"):
            colour = WHITE
        else:
            for w in part.split():
                if upper:
                    w = w.upper()
                # the headline font has no emoji: drop anything it cannot draw
                w = "".join(ch for ch in w if ord(ch) < 0x2000 or ch in "‘’“”–—…")
                if not w:
                    continue
                if words and all(ch in ",.!?:;" for ch in w):
                    words[-1] = (words[-1][0] + w, words[-1][1])
                else:
                    words.append((w, colour))
    return words


def plain(text: str) -> str:
    """Markup removed, for captions and alt text."""
    return re.sub(r"\[/?[cy]\]", "", str(text))


def wrap(words, fnt, max_width):
    space = fnt.getlength(" ")
    lines, line, width = [], [], 0
    for word, colour in words:
        w = fnt.getlength(word)
        if line and width + space + w > max_width:
            lines.append(line)
            line, width = [], 0
        width += (space if line else 0) + w
        line.append((word, colour, w))
    if line:
        lines.append(line)
    return lines


def fit(words, start_size, max_width, max_lines, min_size=34, kind="head"):
    """Shrinks the font until the words fit in max_lines lines of max_width."""
    size = start_size
    while True:
        fnt = font(size, kind)
        lines = wrap(words, fnt, max_width)
        widest = max(
            (sum(w for _, _, w in ln) + fnt.getlength(" ") * (len(ln) - 1) for ln in lines),
            default=0,
        )
        if (len(lines) <= max_lines and widest <= max_width) or size <= min_size:
            return fnt, lines
        size -= 2


def cap_height(fnt) -> int:
    box = fnt.getbbox("H")
    return box[3] - box[1]


def draw_block(img, text, accent, *, centre_x, centre_y=None, bottom=None, size=110,
               max_width=960, max_lines=5, min_size=34, shadow=True, alpha=1.0,
               reveal=1.0, line_gap=1.2):
    """Draws centred multi-colour lines. Give either centre_y or bottom (baseline of the last line).
    reveal (0..1) shows the words progressively. Returns (top, bottom) of the block."""
    words = parse(text, accent)
    if not words:
        return (0, 0)
    fnt, lines = fit(words, size, max_width, max_lines, min_size)
    cap = cap_height(fnt)
    step = int(cap * line_gap)
    block = cap + step * (len(lines) - 1)
    if bottom is not None:
        first_baseline = bottom - step * (len(lines) - 1)
    else:
        first_baseline = centre_y - block / 2 + cap
    total_words = sum(len(ln) for ln in lines)
    shown = total_words if reveal >= 1 else int(round(total_words * max(0.0, reveal)))
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    space = fnt.getlength(" ")
    y, k = first_baseline, 0
    for ln in lines:
        total = sum(w for _, _, w in ln) + space * (len(ln) - 1)
        x = centre_x - total / 2
        for word, colour, w in ln:
            if k < shown:
                if shadow:
                    d.text((x + 4, y + 5), word, font=fnt, fill=(0, 0, 0, 170), anchor="ls")
                d.text((x, y), word, font=fnt, fill=colour, anchor="ls")
            x += w + space
            k += 1
        y += step
    if alpha < 1:
        layer.putalpha(layer.getchannel("A").point(lambda a: int(a * max(0.0, alpha))))
    paste(img, layer)
    return (first_baseline - cap, first_baseline - cap + block)


def paste(img, layer):
    if img.mode == "RGBA":
        img.alpha_composite(layer)
    else:
        img.paste(layer, (0, 0), layer)


def pill(img, text, cx, cy, *, bg, fg, size=36, scale=1.0):
    """Rounded tag pill (TR3NDING, TACTICS...) in Bebas Neue, centred on (cx, cy)."""
    if scale <= 0.01:
        return (cx, cy, cx, cy)
    fnt = font(size * scale, "tag")
    spacing = 3 * scale
    widths = [fnt.getlength(ch) for ch in text]
    tw = sum(widths) + spacing * (len(text) - 1)
    pw, ph = tw + 48 * scale, size * 1.45 * scale
    box = (cx - pw / 2, cy - ph / 2, cx + pw / 2, cy + ph / 2)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle(box, radius=ph / 2, fill=bg)
    x = cx - tw / 2
    for ch, cw in zip(text, widths):
        d.text((x, cy + 2 * scale), ch, font=fnt, fill=fg, anchor="lm")
        x += cw + spacing
    return box


@lru_cache(maxsize=None)
def logo(path: str, height: int, opacity: float):
    lg = Image.open(path).convert("RGBA")
    lg = lg.resize((round(lg.width * height / lg.height), height), Image.LANCZOS)
    lg.putalpha(lg.getchannel("A").point(lambda a: int(a * opacity)))
    return lg


def add_logo(img, path, *, height, y, opacity=0.7):
    """Watermark, top centre."""
    lg = logo(str(path), height, opacity)
    x = (img.width - lg.width) // 2
    if img.mode == "RGBA":
        img.alpha_composite(lg, (x, y))
    else:
        img.paste(lg, (x, y), lg)
