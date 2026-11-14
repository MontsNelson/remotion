"""Original procedurally generated music (no samples, no copyright issues).

make_track(seconds, style, path, drop_at=None)
  style "synthwave": 100 bpm, A minor, kick/clap/hats, saw bass, detuned pad, arp.
  style "lofi": 86 bpm, softer drums, warm keys, no arp.
"""
import numpy as np
from scipy.signal import butter, sosfilt
from scipy.io import wavfile

SR = 44100
rng = np.random.default_rng(7)


def note_hz(n):  # midi -> hz
    return 440.0 * 2 ** ((n - 69) / 12)


def lowpass(x, cutoff, order=2):
    sos = butter(order, min(cutoff, SR / 2 - 100) / (SR / 2), btype="low", output="sos")
    return sosfilt(sos, x)


def highpass(x, cutoff, order=2):
    sos = butter(order, cutoff / (SR / 2), btype="high", output="sos")
    return sosfilt(sos, x)


def env(n, a=0.005, d=0.2, s=0.0, total=None):
    t = np.arange(n) / SR
    e = np.where(t < a, t / a, np.exp(-(t - a) / max(d, 1e-4)) * (1 - s) + s)
    return e


def saw(freq, n, detune=0.0):
    t = np.arange(n) / SR
    out = np.zeros(n)
    for d in ([-detune, 0, detune] if detune else [0]):
        ph = (t * freq * (1 + d) + rng.random()) % 1.0
        out += 2 * ph - 1
    return out / (3 if detune else 1)


def kick(n):
    t = np.arange(n) / SR
    f = 50 + 110 * np.exp(-t * 35)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 7)


def clap(n):
    noise = rng.standard_normal(n)
    noise = highpass(lowpass(noise, 5000), 900)
    t = np.arange(n) / SR
    e = np.exp(-t * 18)
    for off in (0.0, 0.011, 0.022):  # little flam like a real clap
        k = int(off * SR)
        e[k:] += 0.6 * np.exp(-np.arange(n - k) / SR * 60)
    return noise * e * 0.5


def hat(n, open_=False):
    noise = highpass(rng.standard_normal(n), 7000)
    t = np.arange(n) / SR
    return noise * np.exp(-t * (12 if open_ else 55)) * 0.35


def place(buf, sig, start):
    s = int(start * SR)
    if s >= len(buf):
        return
    e = min(len(buf), s + len(sig))
    buf[s:e] += sig[: e - s]


def make_track(seconds, style, path, drop_at=None):
    bpm = 100 if style == "synthwave" else 86
    beat = 60 / bpm
    n = int(seconds * SR) + SR
    drums = np.zeros(n); bass = np.zeros(n); pad = np.zeros(n); arp = np.zeros(n)
    # A minor: Am - F - C - G (one chord per bar)
    chords = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]
    roots = [45, 41, 48, 43]
    total_beats = int(seconds / beat) + 4
    drop_beat = int(round((drop_at or 0) / beat))
    for b in range(total_beats):
        t0 = b * beat
        bar = b // 4
        chord = chords[bar % 4]
        intro = b < drop_beat
        # drums
        if style == "synthwave":
            if not intro:
                place(drums, kick(int(0.45 * SR)) * 0.9, t0)
                if b % 2 == 1:
                    place(drums, clap(int(0.3 * SR)), t0)
                for k in range(2):
                    place(drums, hat(int(0.08 * SR)), t0 + k * beat / 2 + (beat / 2 if k == 0 else 0) * 0)
                place(drums, hat(int(0.3 * SR), True) * 0.6, t0 + beat / 2)
            else:
                if b % 2 == 0:
                    place(drums, hat(int(0.08 * SR)) * 0.6, t0)
        else:  # lofi
            if b % 4 in (0, 2) or (b % 4 == 3 and b % 8 == 7):
                place(drums, lowpass(kick(int(0.4 * SR)), 900) * 0.8, t0 + (beat * 0.5 if b % 8 == 7 else 0))
            if b % 2 == 1:
                place(drums, lowpass(clap(int(0.3 * SR)), 3000) * 0.8, t0 + 0.012)
            for k in range(2):
                swing = 0.06 if k == 1 else 0
                place(drums, lowpass(hat(int(0.07 * SR)), 9000) * 0.55, t0 + k * beat / 2 + swing)
        # bass: 8ths on the root
        root = roots[bar % 4]
        for k in range(2):
            if intro and style == "synthwave":
                continue
            ln = int(beat / 2 * SR * 0.9)
            sig = saw(note_hz(root), ln) if style == "synthwave" else np.sin(2 * np.pi * note_hz(root) * np.arange(ln) / SR)
            sig = lowpass(sig, 380 if style == "synthwave" else 300) * env(ln, 0.004, 0.18, 0.3)
            place(bass, sig * 0.55, t0 + k * beat / 2)
        # pad: whole bar chord
        if b % 4 == 0:
            ln = int(4 * beat * SR)
            sig = np.zeros(ln)
            for m in chord:
                if style == "synthwave":
                    sig += saw(note_hz(m), ln, detune=0.006)
                else:  # warm electric-piano-ish keys
                    tt = np.arange(ln) / SR
                    f = note_hz(m + 12)
                    sig += (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(4 * np.pi * f * tt)) * np.exp(-tt * 0.9)
            cutoff = 1400 if not intro else 500
            sig = lowpass(sig / 3, cutoff, 2) * env(ln, 0.25 if style == "synthwave" else 0.01, 3.0, 0.7)
            place(pad, sig * (0.35 if style == "synthwave" else 0.45), t0)
        # arp: 16ths through chord tones (synthwave only, after drop)
        if style == "synthwave" and not intro:
            seq = chord + [chord[0] + 12]
            for k in range(4):
                m = seq[(b * 4 + k) % 4] + 12
                ln = int(beat / 4 * SR * 0.8)
                tt = np.arange(ln) / SR
                sq = np.sign(np.sin(2 * np.pi * note_hz(m) * tt))
                place(arp, lowpass(sq, 2600) * env(ln, 0.002, 0.07) * 0.12, t0 + k * beat / 4)
    # riser into the drop
    if style == "synthwave" and drop_at:
        ln = int(min(drop_at, 2.4) * SR)
        noise = highpass(rng.standard_normal(ln), 2000)
        ramp = np.linspace(0, 1, ln) ** 2
        place(drums, noise * ramp * 0.25, drop_at - ln / SR)
    # sidechain-style duck on pad and bass after each kick
    duck = np.ones(n)
    if style == "synthwave":
        for b in range(drop_beat, total_beats):
            s = int(b * beat * SR); ln = int(0.25 * SR)
            if s < n:
                e = min(n, s + ln)
                duck[s:e] = np.minimum(duck[s:e], 0.35 + 0.65 * np.linspace(0, 1, e - s))
    mix = drums * 0.9 + (bass + pad) * duck + arp
    if style == "lofi":
        mix = lowpass(mix, 7000) + rng.standard_normal(n) * 0.004  # tape hiss
    mix = mix[: int(seconds * SR)]
    fade = int(0.6 * SR)
    mix[-fade:] *= np.linspace(1, 0, fade)
    mix = np.tanh(mix * 1.2)  # gentle saturation / limiter
    mix = mix / np.max(np.abs(mix)) * 0.89
    stereo = np.stack([mix, mix], axis=1)
    wavfile.write(path, SR, (stereo * 32767).astype(np.int16))
    return bpm


if __name__ == "__main__":
    import sys
    make_track(float(sys.argv[1]), sys.argv[2], sys.argv[3], float(sys.argv[4]) if len(sys.argv) > 4 else None)
