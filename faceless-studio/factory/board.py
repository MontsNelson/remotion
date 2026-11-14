"""
Tactics board drawing (Pillow), used by Footy carousels and the Footy avatar.

Coordinates are in METRES on a 68 x 105 pitch drawn vertically:
  x: 0 = left touchline, 68 = right touchline
  y: 0 = top goal line (the goal the focus team attacks), 105 = bottom goal line
This is the same system as the Remotion tactics reel, so one tactic can feed both.

A board description (JSON) looks like:
{
  "view": [0, 60],                 # which slice of the pitch to show (y from, y to)
  "view_x": [20, 68],              # optional: zoom across too (x from, x to), e.g. for corners
  "team_a": [{"n": 9, "x": 34, "y": 20}, ...],    # focus team (lime)
  "team_b": [{"n": 4, "x": 30, "y": 12}, ...],    # opponents (red)
  "ball": {"x": 40, "y": 18},
  "arrows": [{"kind": "run", "points": [[x,y],[cx,cy],[x2,y2]]},
             {"kind": "pass", "points": [[x,y],[x2,y2]]}],
  "zones": [{"points": [[x,y],...], "label": "TRAP ZONE"}],
  "highlight": {"team": "a", "n": 7},  # pulsing-ring style highlight
  "cuts": [[x, y]]                    # red X where a lane is blocked
}
"""
import math

from PIL import Image, ImageChops, ImageDraw

from .config import LIME, RED, WHITE, YELLOW
from .text import font

PITCH_W, PITCH_L = 68.0, 105.0
GRASS = (11, 61, 46)
GRASS_STRIPE = (15, 72, 54)
LINE = (235, 245, 238)
TEAM_A = LIME
TEAM_B = RED


class Board:
    """Maps metres to pixels inside a box, for the chosen slice of the pitch."""

    def __init__(self, box, view=(0, PITCH_L), margin=1.5, view_x=(0, PITCH_W)):
        self.box = box
        x0, y0, x1, y1 = box
        vy0, vy1 = view
        self.vy0 = vy0 - margin
        self.vy1 = vy1 + margin
        self.vx0, self.vx1 = view_x[0] - margin, view_x[1] + margin
        sx = (x1 - x0) / (self.vx1 - self.vx0)
        sy = (y1 - y0) / (self.vy1 - self.vy0)
        self.s = min(sx, sy)
        used_w = (self.vx1 - self.vx0) * self.s
        used_h = (self.vy1 - self.vy0) * self.s
        self.ox = x0 + ((x1 - x0) - used_w) / 2
        self.oy = y0 + ((y1 - y0) - used_h) / 2

    def p(self, x, y):
        return (self.ox + (x - self.vx0) * self.s, self.oy + (y - self.vy0) * self.s)

    def m(self, metres):
        return metres * self.s


def _rgba(hex_colour, alpha=255):
    h = hex_colour.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), alpha)


def draw_pitch(img, b: Board):
    """Draws the grass and lines, clipped to the visible slice of the pitch."""
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    _draw_pitch(layer, b)
    clip = Image.new("L", img.size, 0)
    ImageDraw.Draw(clip).rectangle([*b.p(b.vx0, b.vy0), *b.p(b.vx1, b.vy1)], fill=255)
    layer.putalpha(ImageChops.multiply(layer.getchannel("A"), clip))
    if img.mode == "RGBA":
        img.alpha_composite(layer)
    else:
        img.paste(layer, (0, 0), layer)


def _draw_pitch(img, b: Board):
    d = ImageDraw.Draw(img)
    x0, y0 = b.p(max(0, b.vx0), max(0, b.vy0))
    x1, y1 = b.p(min(PITCH_W, b.vx1), min(PITCH_L, b.vy1))
    # grass with mowing stripes (every 10.5 m)
    clip_top, clip_bot = b.p(0, b.vy0)[1], b.p(0, b.vy1)[1]
    d.rectangle([b.p(b.vx0, 0)[0], clip_top, b.p(b.vx1, 0)[0], clip_bot], fill=GRASS)
    for k in range(10):
        if k % 2:
            ya, yb = b.p(0, k * 10.5)[1], b.p(0, (k + 1) * 10.5)[1]
            ya, yb = max(ya, clip_top), min(yb, clip_bot)
            if yb > ya:
                d.rectangle([x0, ya, x1, yb], fill=GRASS_STRIPE)
    lw = max(2, int(b.m(0.22)))

    def line(a, c):
        d.line([b.p(*a), b.p(*c)], fill=LINE, width=lw)

    def rect(xa, ya, xb, yb):
        d.rectangle([b.p(xa, ya), b.p(xb, yb)], outline=LINE, width=lw)

    rect(0, 0, PITCH_W, PITCH_L)
    line((0, PITCH_L / 2), (PITCH_W, PITCH_L / 2))
    cx, cy = b.p(34, PITCH_L / 2)
    r = b.m(9.15)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=LINE, width=lw)
    for top in (True, False):
        y_box = 16.5 if top else PITCH_L - 16.5
        y_six = 5.5 if top else PITCH_L - 5.5
        y_goal = 0 if top else PITCH_L
        rect(13.84, 0 if top else y_box, 54.16, y_box if top else PITCH_L)
        rect(24.84, 0 if top else y_six, 43.16, y_six if top else PITCH_L)
        gx0, gy0 = b.p(30.34, y_goal - 2 if top else y_goal)
        gx1, gy1 = b.p(37.66, y_goal if top else y_goal + 2)
        d.rectangle([gx0, gy0, gx1, gy1], outline=LINE, width=lw, fill=(255, 255, 255, 40))
        sx, sy = b.p(34, 11 if top else PITCH_L - 11)
        rs = max(3, b.m(0.3))
        d.ellipse([sx - rs, sy - rs, sx + rs, sy + rs], fill=LINE)
        # the D
        ang = math.degrees(math.acos(5.5 / 9.15))
        start, end = (90 - ang, 90 + ang) if top else (270 - ang, 270 + ang)
        d.arc([sx - r, sy - r, sx + r, sy + r], start, end, fill=LINE, width=lw)


def _bezier(points, n=40):
    if len(points) == 2:
        return points
    (ax, ay), (cx, cy), (bx, by) = points
    out = []
    for k in range(n + 1):
        t = k / n
        out.append(((1 - t) ** 2 * ax + 2 * (1 - t) * t * cx + t * t * bx,
                    (1 - t) ** 2 * ay + 2 * (1 - t) * t * cy + t * t * by))
    return out


def draw_arrow(d, b, points, colour, width, dashed=False):
    pts = [b.p(x, y) for x, y in _bezier(points)]
    if dashed:
        dash, gap = width * 2.6, width * 1.8
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            seg = math.hypot(x2 - x1, y2 - y1)
            k = 0.0
            while k < seg:
                e = min(seg, k + dash)
                d.line([(x1 + (x2 - x1) * k / seg, y1 + (y2 - y1) * k / seg),
                        (x1 + (x2 - x1) * e / seg, y1 + (y2 - y1) * e / seg)], fill=colour, width=width)
                k += dash + gap
    else:
        d.line(pts, fill=colour, width=width, joint="curve")
    (x1, y1), (x2, y2) = pts[-2], pts[-1]
    ang = math.atan2(y2 - y1, x2 - x1)
    L = width * 3.4
    d.polygon([(x2 + math.cos(ang) * 4, y2 + math.sin(ang) * 4),
               (x2 - L * math.cos(ang - 0.45), y2 - L * math.sin(ang - 0.45)),
               (x2 - L * math.cos(ang + 0.45), y2 - L * math.sin(ang + 0.45))], fill=colour)


def draw_board(img, box, spec: dict):
    """Draws a full tactics diagram from a board description into box."""
    b = Board(box, tuple(spec.get("view", (0, PITCH_L))), view_x=tuple(spec.get("view_x", (0, PITCH_W))))
    base = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw_pitch(base, b)
    # keep the drawing inside the box
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(box, radius=28, fill=255)
    over = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(over)
    lw = max(4, int(b.m(0.55)))
    for zone in spec.get("zones", []):
        pts = [b.p(x, y) for x, y in zone["points"]]
        d.polygon(pts, fill=_rgba(YELLOW, 52), outline=_rgba(YELLOW, 230), width=max(3, lw // 2))
        if zone.get("label"):
            lx = min(p[0] for p in pts) + b.m(1.2)
            ly = min(p[1] for p in pts) + b.m(1.2)
            d.text((lx, ly), zone["label"], font=font(b.m(2.6), "tag"), fill=YELLOW, anchor="lt")
    for arrow in spec.get("arrows", []):
        kind = arrow.get("kind", "run")
        colour = {"run": YELLOW, "pass": WHITE, "shot": RED}.get(kind, YELLOW)
        draw_arrow(d, b, [tuple(p) for p in arrow["points"]], colour, lw, dashed=(kind == "pass"))
    for x, y in spec.get("cuts", []):
        cx, cy = b.p(x, y)
        r = b.m(1.3)
        d.line([(cx - r, cy - r), (cx + r, cy + r)], fill=RED, width=lw + 2)
        d.line([(cx - r, cy + r), (cx + r, cy - r)], fill=RED, width=lw + 2)
    radius = b.m(spec.get("dot_size", 2.3))
    hl = spec.get("highlight") or {}
    for team_key, colour, num_colour in (("team_b", TEAM_B, WHITE), ("team_a", TEAM_A, "#0B0F0C")):
        for pl in spec.get(team_key, []):
            px, py = b.p(pl["x"], pl["y"])
            if hl and hl.get("team") == team_key[-1] and hl.get("n") == pl.get("n"):
                for k, a in ((1.9, 120), (1.5, 230)):
                    rr = radius * k
                    d.ellipse([px - rr, py - rr, px + rr, py + rr], outline=_rgba(YELLOW, a), width=max(3, lw // 2))
            d.ellipse([px - radius + 3, py - radius + 6, px + radius + 3, py + radius + 6], fill=(0, 0, 0, 110))
            d.ellipse([px - radius, py - radius, px + radius, py + radius], fill=colour,
                      outline=(255, 255, 255, 235), width=max(2, int(radius * 0.12)))
            if pl.get("n") is not None:
                d.text((px, py + 1), str(pl["n"]), font=font(radius * 1.05, "head"), fill=num_colour, anchor="mm")
    if spec.get("ball"):
        bxm, bym = spec["ball"]["x"], spec["ball"]["y"]
        # a ball on top of a player sits at their feet instead of hiding the number
        for team_key in ("team_a", "team_b"):
            for pl in spec.get(team_key, []):
                if abs(pl["x"] - bxm) < 1.6 and abs(pl["y"] - bym) < 1.6:
                    bxm, bym = pl["x"] + 1.7, pl["y"] + 1.9
        bx, by = b.p(bxm, bym)
        rb = b.m(1.0)
        d.ellipse([bx - rb, by - rb, bx + rb, by + rb], fill=WHITE, outline=(30, 30, 30), width=3)
    base.alpha_composite(over)
    img.paste(base, (0, 0), Image.composite(base.getchannel("A"), Image.new("L", img.size, 0), mask))
    return b
