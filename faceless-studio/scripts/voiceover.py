"""
Records voiceovers: one WAV file per line of a voiceover.json script.

    python scripts/voiceover.py                    # every script in src/
    python scripts/voiceover.py src/gta/data/countdown-voiceover.json

A script file looks like this:

    {
      "voice": "bm_george",           # bm_/bf_ = British, am_/af_ = American
      "speed": 1.1,                   # 1 = normal, 1.1 = brisk, 1.2 = fast
      "outputFolder": "voiceover/my-video",   # inside public/
      "videoLengthSeconds": 30,
      "lines": [ { "id": "hook", "at": 0.25, "text": "..." }, ... ]
    }

What it does, in plain English:
  1. The first time, it fetches the free Kokoro voice model (Apache-2.0)
     from the npm registry (about 120 MB) into a hidden .voice-model folder,
     checks the file is exactly the expected one, and keeps it for next time.
  2. It speaks each line and saves it to public/<outputFolder>/<id>.wav.
  3. It writes each clip's length to <script name>-timings.json next to the
     script, and warns you if a line runs into the next one or past the end.

Setup (once):  pip install -r requirements.txt
"""

import glob
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile

import numpy as np
import soundfile as sf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(ROOT, ".voice-model")
MODEL_PATH = os.path.join(MODEL_DIR, "model_quantized.onnx")
VOICES_PATH = os.path.join(MODEL_DIR, "voices-en.npz")

# Kokoro-82M (Apache-2.0). The weights and voices are published on npm.
WEIGHTS_PACKAGE = "kokoro-q8-shards@1.0.0"
VOICES_PACKAGE = "kokoro-js@1.2.1"
MODEL_SHA256 = "fbae9257e1e05ffc727e951ef9b9c98418e6d79f1c9b6b13bd59f5c9028a1478"
ENGLISH_VOICE_PREFIXES = ("af_", "am_", "bf_", "bm_")

# Leave this much silence between one line ending and the next starting.
MIN_GAP_SECONDS = 0.1


def npm_pack(package: str, dest: str) -> str:
    """Downloads an npm package as a .tgz into `dest` and returns its path."""
    npm = shutil.which("npm")
    if npm is None:
        sys.exit("npm was not found. Install Node.js from https://nodejs.org/")
    result = subprocess.run(
        [npm, "pack", package, "--pack-destination", dest, "--silent"],
        capture_output=True,
        text=True,
        shell=os.name == "nt",
    )
    if result.returncode != 0:
        sys.exit(f"Could not download {package}:\n{result.stderr}")
    return os.path.join(dest, result.stdout.strip().splitlines()[-1])


def extract(tgz: str, dest: str) -> str:
    with tarfile.open(tgz) as tar:
        if sys.version_info >= (3, 12):
            tar.extractall(dest, filter="data")
        else:
            tar.extractall(dest)
    return os.path.join(dest, "package")


def prepare_model() -> None:
    """Downloads and assembles the voice model the first time only."""
    if os.path.exists(MODEL_PATH) and os.path.exists(VOICES_PATH):
        return
    os.makedirs(MODEL_DIR, exist_ok=True)
    print("First run: downloading the Kokoro voice model (about 120 MB)...")
    with tempfile.TemporaryDirectory() as tmp:
        if not os.path.exists(MODEL_PATH):
            weights = extract(npm_pack(WEIGHTS_PACKAGE, tmp), os.path.join(tmp, "w"))
            digest = hashlib.sha256()
            with open(MODEL_PATH + ".part", "wb") as out:
                for i in range(6):
                    part = os.path.join(weights, f"kokoro-q8.part{i}.bin")
                    with open(part, "rb") as f:
                        chunk = f.read()
                        digest.update(chunk)
                        out.write(chunk)
            if digest.hexdigest() != MODEL_SHA256:
                os.remove(MODEL_PATH + ".part")
                sys.exit("The downloaded model did not match the expected checksum.")
            os.replace(MODEL_PATH + ".part", MODEL_PATH)

        voices_dir = os.path.join(
            extract(npm_pack(VOICES_PACKAGE, tmp), os.path.join(tmp, "v")), "voices"
        )
        voices = {}
        for name in sorted(os.listdir(voices_dir)):
            if name.startswith(ENGLISH_VOICE_PREFIXES) and name.endswith(".bin"):
                data = np.fromfile(os.path.join(voices_dir, name), dtype=np.float32)
                voices[name[:-4]] = data.reshape(-1, 1, 256)
        np.savez(VOICES_PATH, **voices)
    print("Voice model ready.")


def record(kokoro, script_path: str) -> bool:
    """Records every line of one script. Returns False if a line overruns."""
    with open(script_path, encoding="utf-8") as f:
        config = json.load(f)
    print(f"\n{os.path.relpath(script_path, ROOT)}")

    out_dir = os.path.join(ROOT, "public", config["outputFolder"])
    os.makedirs(out_dir, exist_ok=True)
    lines = sorted(config["lines"], key=lambda line: line["at"])
    timings = {}
    for line in lines:
        voice = line.get("voice", config["voice"])
        if voice not in kokoro.get_voices():
            sys.exit(f"Unknown voice {voice}. Choose one of: {', '.join(kokoro.get_voices())}")
        audio, rate = kokoro.create(
            line["text"],
            voice=voice,
            speed=line.get("speed", config["speed"]),
            # British voices (b...) get British pronunciation.
            lang="en-gb" if voice.startswith("b") else "en-us",
        )
        sf.write(os.path.join(out_dir, f"{line['id']}.wav"), audio, rate)
        timings[line["id"]] = round(len(audio) / rate, 3)
        print(f"  {line['id']:<10} {timings[line['id']]:5.2f}s  {line['text']}")

    timings_path = script_path[: -len(".json")] + "-timings.json"
    with open(timings_path, "w", encoding="utf-8") as f:
        json.dump(timings, f, indent=2)
        f.write("\n")

    ok = True
    for current, following in zip(lines, lines[1:] + [None]):
        end = current["at"] + timings[current["id"]]
        limit = (
            following["at"] - MIN_GAP_SECONDS
            if following
            else config["videoLengthSeconds"]
        )
        if end > limit:
            ok = False
            print(
                f"  WARNING: '{current['id']}' ends at {end:.2f}s but must end by "
                f"{limit:.2f}s. Shorten the text, raise the speed, or move the "
                "next line later."
            )
    return ok


def main() -> None:
    scripts = sys.argv[1:] or sorted(
        glob.glob(os.path.join(ROOT, "src", "**", "*voiceover.json"), recursive=True)
    )
    if not scripts:
        sys.exit("No voiceover.json files found.")
    prepare_model()
    from kokoro_onnx import Kokoro

    kokoro = Kokoro(MODEL_PATH, VOICES_PATH)
    results = [record(kokoro, os.path.abspath(path)) for path in scripts]
    print("\nAll lines fit." if all(results) else "\nSome lines need fixing (see warnings).")


if __name__ == "__main__":
    main()
