"""
AI voiceover with Kokoro (free, Apache-2.0, runs offline).

The first call downloads the model (about 120 MB) from the npm registry into
.voice-model/ and checks its checksum. Voices: bm_/bf_ = British,
am_/af_ = American (m = male, f = female).
"""
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from functools import lru_cache

import numpy as np
import soundfile as sf

from .config import ROOT

MODEL_DIR = ROOT / ".voice-model"
MODEL_PATH = MODEL_DIR / "model_quantized.onnx"
VOICES_PATH = MODEL_DIR / "voices-en.npz"
WEIGHTS_PACKAGE = "kokoro-q8-shards@1.0.0"
VOICES_PACKAGE = "kokoro-js@1.2.1"
MODEL_SHA256 = "fbae9257e1e05ffc727e951ef9b9c98418e6d79f1c9b6b13bd59f5c9028a1478"
ENGLISH = ("af_", "am_", "bf_", "bm_")


def _npm_pack(package, dest):
    npm = shutil.which("npm")
    if npm is None:
        sys.exit("npm was not found. Install Node.js from https://nodejs.org/")
    result = subprocess.run([npm, "pack", package, "--pack-destination", dest, "--silent"],
                            capture_output=True, text=True, shell=os.name == "nt")
    if result.returncode != 0:
        sys.exit(f"Could not download {package}:\n{result.stderr}")
    return os.path.join(dest, result.stdout.strip().splitlines()[-1])


def _extract(tgz, dest):
    with tarfile.open(tgz) as tar:
        if sys.version_info >= (3, 12):
            tar.extractall(dest, filter="data")
        else:
            tar.extractall(dest)
    return os.path.join(dest, "package")


def prepare_model():
    """Downloads and assembles the voice model the first time only."""
    if MODEL_PATH.exists() and VOICES_PATH.exists():
        return
    MODEL_DIR.mkdir(exist_ok=True)
    print("First run: downloading the Kokoro voice model (about 120 MB)...")
    with tempfile.TemporaryDirectory() as tmp:
        if not MODEL_PATH.exists():
            weights = _extract(_npm_pack(WEIGHTS_PACKAGE, tmp), os.path.join(tmp, "w"))
            digest = hashlib.sha256()
            part_path = str(MODEL_PATH) + ".part"
            with open(part_path, "wb") as out:
                for i in range(6):
                    with open(os.path.join(weights, f"kokoro-q8.part{i}.bin"), "rb") as f:
                        chunk = f.read()
                        digest.update(chunk)
                        out.write(chunk)
            if digest.hexdigest() != MODEL_SHA256:
                os.remove(part_path)
                sys.exit("The downloaded model did not match the expected checksum.")
            os.replace(part_path, MODEL_PATH)
        voices_dir = os.path.join(_extract(_npm_pack(VOICES_PACKAGE, tmp), os.path.join(tmp, "v")), "voices")
        voices = {}
        for name in sorted(os.listdir(voices_dir)):
            if name.startswith(ENGLISH) and name.endswith(".bin"):
                data = np.fromfile(os.path.join(voices_dir, name), dtype=np.float32)
                voices[name[:-4]] = data.reshape(-1, 1, 256)
        np.savez(VOICES_PATH, **voices)
    print("Voice model ready.")


@lru_cache(maxsize=1)
def _kokoro():
    prepare_model()
    from kokoro_onnx import Kokoro
    return Kokoro(str(MODEL_PATH), str(VOICES_PATH))


def voices():
    return _kokoro().get_voices()


def speak(text: str, voice: str, speed: float, out_wav) -> float:
    """Speaks text into out_wav (24 kHz mono). Returns the length in seconds."""
    kokoro = _kokoro()
    if voice not in kokoro.get_voices():
        sys.exit(f"Unknown voice {voice}. Choose one of: {', '.join(kokoro.get_voices())}")
    audio, rate = kokoro.create(spoken(text), voice=voice, speed=speed,
                                lang="en-gb" if voice.startswith("b") else "en-us")
    sf.write(str(out_wav), audio, rate)
    return len(audio) / rate


def spoken(text: str) -> str:
    """Text as it should be said: markup removed, GTA spelled out so it is read as letters."""
    t = re.sub(r"\[/?[cy]\]", "", text)
    t = re.sub(r"\bGTA\b", "G T A", t, flags=re.IGNORECASE)
    return t


def word_timings(text: str, duration: float):
    """Estimated start/end of each word, spread over the clip by word length.
    Pauses after commas and full stops get a little extra time."""
    words = re.sub(r"\[/?[cy]\]", "", text).split()
    if not words:
        return []
    weights = []
    for w in words:
        weight = len(re.sub(r"[^\w']", "", w)) + 2
        if w[-1] in ",;:":
            weight += 3
        elif w[-1] in ".!?":
            weight += 5
        weights.append(weight)
    total = sum(weights)
    usable = max(0.1, duration - 0.15)
    out, t = [], 0.05
    for w, weight in zip(words, weights):
        span = usable * weight / total
        out.append({"word": w, "start": round(t, 3), "end": round(t + span, 3)})
        t += span
    return out
