"""
Vice City Corner reels (1080x1920, 30 fps), built from Rockstar stills,
motion, text, AI voiceover and original music. No trailer footage.

A reel script is JSON:
{
  "account": "vice",
  "music": "synthwave",            # or "lofi", or null for none
  "scenes": [
    {"type": "hook",   "image": "Vice_City_27", "pill": "TR3NDING",
     "text": "GTA 6 IS OUT IN", "say": "GTA 6 is out in..."},
    {"type": "number", "image": "Vice_City_27", "number": "5", "label": "DAYS",
     "say": "five days."},
    {"type": "image",  "image": "Vice_City_15", "focus_x": 0.55,
     "text": "[c]VICE CITY[/c]", "say": "Vice City, in the state of Leonida."},
    {"type": "versus", "top": {"image": "GTAV_Los_Santos_01", "label": "GTA V"},
     "bottom": {"image": "Vice_City_15", "label": "GTA 6"},
     "text": "LOS SANTOS VS [c]VICE CITY[/c]", "say": "Los Santos versus Vice City."},
    {"type": "end", "image": "Vice_City_15", "pill": "SAVE THE DATE",
     "lines": ["[y]NOVEMBER 19[/y]", "ARE YOU [c]READY?[/c]"],
     "say": "November nineteenth. Are you ready? Follow Vice City Corner."}
  ]
}

Each scene lasts as long as its voice line plus a beat (or "min" seconds).
Word-by-word captions show on "image" and "versus" scenes (turn off with
"captions": false). Everything stays out of Instagram's button zones.
"""
import json
import math
import subprocess
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw

from . import audio, config, voice
from .config import FPS, H_REEL as H, W_REEL as W, WHITE, YELLOW
from .text import add_logo, cap_height, draw_block, font, parse, pill

MIN_SECONDS = {"hook": 2.2, "number": 1.6, "image": 1.8, "versus": 2.6, "end": 3.0}
CAPTION_Y = 1330          # centre of the word-caption band (well above the bottom 300 px)
SAFE_RIGHT = W - 130      # Instagram's buttons sit on the right


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def prog(t, start, dur):
    return clamp((t - start) / dur) if dur > 0 else 1.0


def ease_in_out(p):
    return 3 * p * p - 2 * p * p * p


def back_out(p, s=1.7):
    p -= 1
    return p * p * ((s + 1) * p + s) + 1


@lru_cache(maxsize=None)
def load(name):
    return Image.open(config.library_image(name)).convert("RGB")


def kenburns(name, p, z0=1.05, z1=1.18, fx=0.5, fy=0.5, w=W, h=H):
    img = load(name)
    base = max(w / img.width, h / img.height)
    z = z0 + (z1 - z0) * ease_in_out(clamp(p))
    cw, ch = w / (base * z), h / (base * z)
    cx = (img.width - cw) * clamp(fx) + cw / 2
    cy = (img.height - ch) * clamp(fy) + ch / 2
    return img.resize((w, h), Image.BILINEAR, box=(cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2))


@lru_cache(maxsize=None)
def vertical_fade(h, top_alpha, bottom_alpha, start, end):
    mask = Image.new("L", (1, h))
    for y in range(h):
        t = clamp((y / h - start) / max(end - start, 1e-6))
        t = t * t * (3 - 2 * t)
        mask.putpixel((0, y), int(top_alpha + (bottom_alpha - top_alpha) * t))
    black = Image.new("RGBA", (W, h), (0, 0, 0, 255))
    black.putalpha(mask.resize((W, h)))
    return black


def darken(img, a):
    return Image.blend(img, Image.new("RGB", img.size, "black"), a)


def flash(img, amount):
    if amount <= 0.01:
        return img
    return Image.blend(img.convert("RGB"), Image.new("RGB", img.size, "white"), clamp(amount)).convert("RGBA")


def shake(t, start, strength=18, dur=0.25):
    p = prog(t, start, dur)
    if p <= 0 or p >= 1:
        return 0, 0
    a = strength * (1 - p)
    return int(a * math.sin(t * 90)), int(a * math.cos(t * 77))


class Reel:
    def __init__(self, spec, work_dir: Path):
        self.spec = spec
        self.acct = config.account(spec["account"])
        self.accent = self.acct["accent"]
        self.work = work_dir
        self.work.mkdir(parents=True, exist_ok=True)
        self.timeline = []   # (start, end, scene, words)

    # ---------- audio + timing ----------
    def plan(self):
        t = 0.0
        clips = []
        for i, scene in enumerate(self.spec["scenes"]):
            say = scene.get("say", "")
            words, vlen = [], 0.0
            if say:
                wav = self.work / f"line_{i:02d}.wav"
                vlen = voice.speak(say, scene.get("voice", self.acct["voice"]),
                                   scene.get("speed", self.acct["voice_speed"]), wav)
                lead = 0.12
                clips.append((wav, t + lead))
                words = [{**w, "start": w["start"] + t + lead, "end": w["end"] + t + lead}
                         for w in voice.word_timings(say, vlen)]
            dur = max(scene.get("min", MIN_SECONDS.get(scene["type"], 2.0)), vlen + 0.4)
            self.timeline.append((t, t + dur, scene, words))
            t += dur
        self.total = round(t * FPS) / FPS
        music_style = self.spec.get("music", self.acct["music"])
        drop = self.timeline[1][0] if len(self.timeline) > 1 else None
        self.mix = audio.build(clips, self.total, music_style, self.work / "mix.wav", drop_at=drop)
        return self.total

    # ---------- drawing ----------
    def captions(self, img, t, words):
        """Shows the current phrase (up to 4 words), current word in yellow."""
        if not words or t < words[0]["start"] or t > words[-1]["end"] + 0.3:
            return
        idx = max(i for i, w in enumerate(words) if w["start"] <= t) if t >= words[0]["start"] else 0
        group_start = (idx // 4) * 4
        group = words[group_start: group_start + 4]
        fnt = font(84)
        tokens = [(w["word"].upper().strip(), w is words[idx]) for w in group]
        space = fnt.getlength(" ")
        total = sum(fnt.getlength(tk) for tk, _ in tokens) + space * (len(tokens) - 1)
        while total > SAFE_RIGHT - 70 and fnt.size > 50:
            fnt = font(fnt.size - 4)
            space = fnt.getlength(" ")
            total = sum(fnt.getlength(tk) for tk, _ in tokens) + space * (len(tokens) - 1)
        x = (70 + SAFE_RIGHT) / 2 - total / 2
        y = CAPTION_Y + cap_height(fnt) / 2
        d = ImageDraw.Draw(img)
        for tk, current in tokens:
            d.text((x, y), tk, font=fnt, fill=YELLOW if current else WHITE, anchor="ls",
                   stroke_width=7, stroke_fill=(0, 0, 0))
            x += fnt.getlength(tk) + space

    def scene_frame(self, scene, start, end, t, words):
        local = t - start
        p = local / max(end - start, 1e-6)
        kind = scene["type"]
        if kind in ("hook", "number", "end"):
            img = darken(kenburns(scene.get("image", "Vice_City_27"), p, 1.2, 1.08, scene.get("focus_x", 0.5)),
                         0.55 if kind != "hook" else 0.68).convert("RGBA")
        elif kind == "versus":
            img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
            half = H // 2
            for key, y0 in (("top", 0), ("bottom", half)):
                part = scene[key]
                ph = kenburns(part["image"], p, 1.05, 1.15, part.get("focus_x", 0.5), w=W, h=half)
                img.paste(darken(ph, 0.25), (0, y0))
            d = ImageDraw.Draw(img)
            d.rectangle([0, half - 4, W, half + 4], fill=WHITE)
            pill(img, scene["top"].get("label", "").upper(), W / 2, 330, bg=(0, 0, 0), fg=WHITE, size=56)
            pill(img, scene["bottom"].get("label", "").upper(), W / 2, half + 110, bg=(0, 0, 0),
                 fg=self.accent, size=56)
        else:
            img = kenburns(scene["image"], p, 1.06, 1.2, scene.get("focus_x", 0.5)).convert("RGBA")
            img.alpha_composite(vertical_fade(H, 0, 215, 0.42, 0.82))
            img.alpha_composite(vertical_fade(H, 130, 0, 0.0, 0.22))

        if kind == "hook":
            top, _ = draw_block(img, scene.get("text", ""), self.accent, centre_x=W / 2, centre_y=960, size=150,
                                max_width=900, max_lines=4, reveal=prog(local, 0.2, 1.1) * 1.0001)
            if scene.get("pill"):
                # sits just above the headline, however many lines it has
                pill(img, scene["pill"].upper(), W / 2, top - 70, bg=self.acct["pill_bg"], fg=self.acct["pill_fg"],
                     size=44, scale=back_out(prog(local, 0.05, 0.35)))
        elif kind == "number":
            s = back_out(prog(local, 0, 0.35))
            dx, dy = shake(local, 0, 22)
            layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            d = ImageDraw.Draw(layer)
            f = font(int(760 * max(s, 0.02)))
            d.text((W / 2 + 10 + dx, 960 + 14 + dy), str(scene["number"]), font=f, fill=(0, 0, 0, 160), anchor="mm")
            d.text((W / 2 + dx, 960 + dy), str(scene["number"]), font=f, fill=YELLOW, anchor="mm")
            img.alpha_composite(layer)
            if scene.get("above"):
                draw_block(img, scene["above"], self.accent, centre_x=W / 2, centre_y=470, size=110, max_width=900)
            draw_block(img, f"[c]{scene.get('label', '')}[/c]", self.accent, centre_x=W / 2, centre_y=1420,
                       size=160, max_width=900, alpha=prog(local, 0.25, 0.25))
        elif kind == "image":
            if scene.get("pill"):
                pill(img, scene["pill"].upper(), W / 2, 330, bg=self.acct["pill_bg"], fg=self.acct["pill_fg"], size=42)
            if scene.get("text"):
                draw_block(img, scene["text"], self.accent, centre_x=W / 2, centre_y=1080, size=130,
                           max_width=900, max_lines=3, alpha=prog(local, 0.0, 0.2))
        elif kind == "versus":
            if scene.get("text"):
                draw_block(img, scene["text"], self.accent, centre_x=W / 2, centre_y=H // 2 - 150, size=86,
                           max_width=900, max_lines=2)
        elif kind == "end":
            img.alpha_composite(vertical_fade(H, 0, 200, 0.35, 0.8))
            if scene.get("pill"):
                pill(img, scene["pill"].upper(), W / 2, 560, bg=self.acct["pill_bg"], fg=self.acct["pill_fg"],
                     size=44, scale=back_out(prog(local, 0.0, 0.3)))
            y = 760
            for k, line in enumerate(scene.get("lines", [])):
                size = 170 if k == 0 else 100
                _, bottom = draw_block(img, line, self.accent, centre_x=W / 2, centre_y=y, size=size,
                                       max_width=900, max_lines=2, alpha=prog(local, 0.1 + 0.35 * k, 0.3))
                y = bottom + 110
            draw_block(img, f"FOLLOW [y]{self.acct['handle'].upper()}[/y]", self.accent, centre_x=W / 2,
                       centre_y=max(y + 40, 1250), size=76, max_width=900,
                       alpha=prog(local, 0.2 + 0.35 * len(scene.get("lines", [])), 0.3))

        if kind in ("image", "versus") and scene.get("captions", True):
            self.captions(img, t, words)
        add_logo(img, self.acct["logo"], height=46, y=150, opacity=0.72)
        # flash on each cut (not on the very first frame of the hook)
        if start > 0 and kind != "end":
            img = flash(img, 0.5 * (1 - prog(local, 0, 0.18)))
        return img

    def frame(self, t):
        for start, end, scene, words in self.timeline:
            if start <= t < end:
                return self.scene_frame(scene, start, end, t, words)
        start, end, scene, words = self.timeline[-1]
        return self.scene_frame(scene, start, end, min(t, end - 1e-3), words)

    # ---------- output ----------
    def render(self, out_mp4: Path, cover_jpg: Path):
        self.plan()
        silent = self.work / "video.mp4"
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
               "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
               "-pix_fmt", "yuv420p", str(silent)]
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        frames = int(round(self.total * FPS))
        for k in range(frames):
            proc.stdin.write(self.frame(k / FPS).convert("RGB").tobytes())
        proc.stdin.close()
        if proc.wait() != 0:
            raise SystemExit("ffmpeg failed while encoding the video")
        mux(silent, self.mix, out_mp4)
        # cover: the hook with its full headline
        first = self.timeline[0]
        self.scene_frame(first[2], first[0], first[1], first[1] - 0.05, first[3]).convert("RGB").save(
            cover_jpg, quality=92)
        return {"seconds": self.total, "voice_lines": [s.get("say", "") for s in self.spec["scenes"]]}


def mux(video, audio_wav, out_mp4):
    """Joins picture and sound, normalising loudness to about -14 LUFS."""
    out_mp4.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(video), "-i", str(audio_wav),
                        "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                        "-ar", "48000", "-shortest", "-movflags", "+faststart", str(out_mp4)])
    if r.returncode != 0:
        raise SystemExit("ffmpeg failed while adding the soundtrack")


def render(spec: dict, out_dir: Path, work_dir: Path):
    reel = Reel(spec, work_dir)
    info = reel.render(out_dir / "reel.mp4", out_dir / "cover.jpg")
    (out_dir / "script.json").write_text(json.dumps(spec, indent=2), encoding="utf-8")
    return info
