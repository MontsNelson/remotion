"""
Footy Smart tactics reels, rendered with Remotion (smooth animated board).

A spec is JSON:
{
  "account": "footy",
  "tactic": { ...same shape as src/footysmart10/data/scene.ts... },
  "voiceover": {
    "voice": "bm_george", "speed": 1.1,         # optional, defaults from config
    "lines": [{"id": "hook", "at": 0.25, "text": "..."}, ...]
  },
  "music": "lofi"                              # or null
}
See content/examples/footy-reel-high-press.json for a full tactic.

What it does: records each narration line (Kokoro), works out word-by-word
caption timings, makes an original music bed, renders the Remotion
composition with those as props, then normalises loudness to -14 LUFS.
"""
import json
import os
import shutil
import subprocess
from pathlib import Path

from . import config, music, voice
from .config import ROOT
from .reel import mux

MIN_GAP = 0.1


def _npx():
    npx = shutil.which("npx")
    if npx is None:
        raise SystemExit("npx was not found. Install Node.js from https://nodejs.org/")
    return npx


def _browser_args():
    exe = config.SETTINGS.get("browser_executable") or os.environ.get("REMOTION_BROWSER")
    return [f"--browser-executable={exe}"] if exe else []


def render(spec: dict, out_dir: Path, work_dir: Path, slug: str, composition="TacticsReel"):
    acct = config.account(spec.get("account", "footy"))
    tactic = spec["tactic"]
    length = float(tactic["durationInSeconds"])
    vo = spec.get("voiceover") or {"lines": []}
    voice_name = vo.get("voice", acct["voice"])
    speed = vo.get("speed", acct["voice_speed"])
    folder = f"voiceover/footy-{slug}"
    (ROOT / "public" / folder).mkdir(parents=True, exist_ok=True)

    lines = sorted(vo["lines"], key=lambda ln: ln["at"])
    durations, captions, warnings = {}, [], []
    for line in lines:
        wav = ROOT / "public" / folder / f"{line['id']}.wav"
        secs = voice.speak(line["text"], line.get("voice", voice_name), line.get("speed", speed), wav)
        durations[line["id"]] = round(secs, 3)
        captions += [{**w, "start": round(w["start"] + line["at"], 3), "end": round(w["end"] + line["at"], 3)}
                     for w in voice.word_timings(line["text"], secs)]
    for cur, nxt in zip(lines, lines[1:] + [None]):
        end = cur["at"] + durations[cur["id"]]
        limit = nxt["at"] - MIN_GAP if nxt else length
        if end > limit:
            warnings.append(f"line '{cur['id']}' ends at {end:.2f}s but must end by {limit:.2f}s")
    if warnings:
        raise SystemExit("Narration does not fit:\n  " + "\n  ".join(warnings)
                         + "\nShorten the text, raise the speed, or move the next line later.")

    music_file = None
    style = spec.get("music", acct["music"])
    if style:
        music_file = f"music/footy-{slug}.wav"
        (ROOT / "public" / "music").mkdir(parents=True, exist_ok=True)
        music.make_track(length + 0.5, style, str(ROOT / "public" / music_file))

    props = {
        "tactic": tactic,
        "voiceover": {"voice": voice_name, "speed": speed, "outputFolder": folder,
                      "videoLengthSeconds": length, "lines": lines, "durations": durations},
        "captions": captions,
        "musicFile": music_file,
    }
    work_dir.mkdir(parents=True, exist_ok=True)
    props_path = work_dir / "props.json"
    props_path.write_text(json.dumps(props), encoding="utf-8")
    raw = work_dir / "raw.mp4"
    shell = os.name == "nt"
    r = subprocess.run([_npx(), "remotion", "render", "src/index.ts", composition, str(raw),
                        f"--props={props_path}", "--log=error", *_browser_args()], cwd=ROOT, shell=shell)
    if r.returncode != 0:
        raise SystemExit("Remotion render failed")
    # re-encode the audio with loudness normalisation, keep the picture as is
    out_dir.mkdir(parents=True, exist_ok=True)
    tmp_audio = work_dir / "audio.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw), "-vn", str(tmp_audio)], check=True)
    mux(raw, tmp_audio, out_dir / "reel.mp4")
    cover_frame = int(min(2.6, length / 2) * 30)
    subprocess.run([_npx(), "remotion", "still", "src/index.ts", composition, str(out_dir / "cover.jpg"),
                    f"--props={props_path}", f"--frame={cover_frame}", "--image-format=jpeg",
                    "--log=error", *_browser_args()], cwd=ROOT, shell=shell, check=True)
    (out_dir / "script.json").write_text(json.dumps(spec, indent=2), encoding="utf-8")
    return {"seconds": length, "voice_lines": [ln["text"] for ln in lines], "durations": durations}
