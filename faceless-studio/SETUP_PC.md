# Set up the autopilot on Monty's Windows PC

**How to use:** open Claude Code on the PC in an empty folder (for example
`C:\Users\monty\content-factory`), paste everything below the line, and answer
its questions. It installs everything, regenerates the first fortnight of posts
into Google Drive, and schedules the daily run.

---

You are setting up "Faceless Studio" on this Windows PC: an automatic content
factory for two Instagram accounts. The code is already written and tested; your
job is to install it, connect it to Google Drive, test it, and schedule it.
Explain each step in one plain-English line. Install only what's missing.

Decisions already made (don't ask again):
- Accounts: **Vice City Corner** `@vicecitycorner6` (GTA 6 news) and **Footy Smart**
  `@footysmart10` (football tactics, Premier League first, Arsenal when there's a
  real angle). Two separate brands.
- Runs on this PC, daily at 07:00 UK. The PC stays on.
- Voices: GTA `am_fenrir`, Footy `bm_george` (unless Monty says otherwise below).
- No trailer or match footage; stills, diagrams, AI voice and original music only.
- Monty doesn't own GTA V or GTA 6 (no Photo Mode posts).

## Step 0: ask Monty (one message, then wait)
1. Path of the Google Drive for desktop folder (usually `G:\My Drive`). If Google
   Drive for desktop isn't installed, walk him through installing it and signing in
   to his montynelson2609 Gmail, then continue.
2. Did he pick different voices from the samples? (GTA: Fenrir, Michael or Puck;
   Footy: George, Fable or Lewis.)

## Step 1: tools
Check, and install with winget only if missing:
- Git (`winget install Git.Git`), Python 3.11+ (`winget install Python.Python.3.12`,
  with "Add to PATH"), Node.js LTS 22+ (`winget install OpenJS.NodeJS.LTS`),
  ffmpeg (`winget install Gyan.FFmpeg`). Open a new terminal after installing and
  confirm `git --version`, `python --version`, `node -v`, `ffmpeg -version`.

## Step 2: get the code (only the project folder, not the whole repository)
```
git clone --filter=blob:none --no-checkout --depth 1 -b claude/practical-bell-96tql0 https://github.com/MontsNelson/remotion.git faceless-src
cd faceless-src
git sparse-checkout set faceless-studio
git checkout
cd faceless-studio
```
Everything below runs inside `faceless-src\faceless-studio`.

## Step 3: install
```
npm install
python -m pip install -r requirements.txt
```
Then copy `settings.example.json` to `settings.json` and set `drive_root` to
`<Drive path>\Faceless Accounts` (double the backslashes in JSON) and the voices.

## Step 4: screenshots and voice model
1. Copy every `.jpg` from `<Drive>\Faceless Accounts\GTA 6 - Vice Daily\01 Rockstar Screenshots`
   and its `GTA V (for comparisons)` subfolder into `library\`. Expect 39 + 18 files.
2. `python -c "from factory import voice; voice.prepare_model()"` (downloads the free
   Kokoro voice model, about 120 MB, from npm and checks its checksum).

## Step 5: test, and make the first fortnight
1. `python make.py plan content/plans/2026-11-14_launch-fortnight.json`
   This rebuilds all posts for 14-22 November straight into Google Drive (17 Vice
   City Corner posts, 9 Footy Smart posts) with captions and schedules. Reels use
   Remotion; the first one downloads a headless browser (about 100 MB).
2. `python make.py check "<Drive>\Faceless Accounts\GTA 6 - Vice Daily\02 Ready Posts"`
   and the same for `Footy\02 Ready Posts`. Open a few contact sheets from
   `work\check\` and confirm they look right. Fix anything that's off.
3. Posts dated before today are fine to leave; Monty skips them.

## Step 6: the daily run
1. Run `claude --help` and check the non-interactive flags on this version. Edit the
   `claude -p ...` line in `windows\run_daily.bat` if the flags differ (the run must
   not stop for permission prompts; `.claude\settings.json` holds the allow-list).
2. Run `windows\run_daily.bat` once by hand and read `logs\<today>.txt`. It should
   research, make today's post(s) and show a notification.
3. Schedule it:
   `powershell -ExecutionPolicy Bypass -File windows\install_schedule.ps1 -Time 07:00`
4. Power: Settings > System > Power > set sleep to "Never" when plugged in, and in
   Control Panel > Power Options > Change plan settings > Advanced > Sleep > Allow
   wake timers: Enable. Show Monty how to check (`schtasks /query /tn "Faceless Studio daily run"`),
   run it now (`schtasks /run /tn ...`) and turn it off (`schtasks /change /tn ... /disable`).

## Step 7: finish
Give Monty a short summary: what's in Drive, the next automatic run time, and
remind him that `POSTING_GUIDE.txt` in each `02 Ready Posts` folder has the
Sunday scheduling steps. The rules for every run are in `CLAUDE.md`.
