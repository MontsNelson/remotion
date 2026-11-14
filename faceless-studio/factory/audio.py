"""
Builds a reel's soundtrack: voice lines on top of original music.

- Music comes from music.py (generated in code, so no copyright claims).
- While someone speaks, the music drops to about 25% and comes back in the gaps.
- The final mix is normalised to about -14 LUFS (Instagram's loudness) when
  it is muxed with the video (see reel.mux).
"""
import subprocess

import numpy as np
import soundfile as sf
from scipy.signal import resample_poly

from . import music

SR = 44100


def _load_mono(path):
    data, rate = sf.read(str(path), dtype="float32")
    if data.ndim > 1:
        data = data.mean(axis=1)
    if rate != SR:
        data = resample_poly(data, SR, rate).astype(np.float32)
    return data


def build(voice_clips, total_seconds, music_style, out_wav, duck_to=0.25, music_level=0.5, drop_at=None):
    """voice_clips: [(wav_path, start_seconds)]. Writes a stereo 44.1 kHz WAV."""
    n = int(total_seconds * SR)
    voice = np.zeros(n, dtype=np.float32)
    for path, start in voice_clips:
        clip = _load_mono(path)
        s = int(start * SR)
        e = min(n, s + len(clip))
        if e > s:
            voice[s:e] += clip[: e - s]
    tmp_music = str(out_wav) + ".music.wav"
    if music_style:
        music.make_track(total_seconds + 0.5, music_style, tmp_music, drop_at)
        bed = _load_mono(tmp_music)[:n]
        bed = np.pad(bed, (0, max(0, n - len(bed))))
    else:
        bed = np.zeros(n, dtype=np.float32)
    # ducking envelope: 1 in gaps, duck_to while the voice is active, smooth 120 ms ramps
    active = np.abs(voice) > 0.01
    win = int(0.25 * SR)
    if active.any():
        held = np.convolve(active.astype(np.float32), np.ones(win, dtype=np.float32), mode="same") > 0
    else:
        held = active
    target = np.where(held, duck_to, 1.0).astype(np.float32)
    ramp = int(0.12 * SR)
    kernel = np.ones(ramp, dtype=np.float32) / ramp
    env = np.convolve(target, kernel, mode="same")
    mix = voice * 1.0 + bed * music_level * env
    # gentle fade in/out and a safety limiter
    fade = int(0.4 * SR)
    mix[:fade] *= np.linspace(0, 1, fade)
    mix[-fade:] *= np.linspace(1, 0, fade)
    peak = float(np.max(np.abs(mix))) or 1.0
    if peak > 0.98:
        mix = mix / peak * 0.98
    stereo = np.stack([mix, mix], axis=1)
    sf.write(str(out_wav), stereo, SR)
    return out_wav


def loudness(path):
    """Integrated loudness (LUFS) of a media file, measured by ffmpeg."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af",
                        "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=summary", "-f", "null", "-"],
                       capture_output=True, text=True)
    for line in r.stderr.splitlines():
        if "Input Integrated" in line:
            return float(line.split(":")[1].split()[0])
    return None
