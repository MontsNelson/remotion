# Faceless Studio: rules for Claude

This project makes posts for two Instagram accounts and saves them to Google Drive.
The daily job is in `tasks/DAILY_TASK.md`. The tools are in `make.py` (run
`python make.py --help`). The plan for the channels is in `PLAN.md`.

## Accounts (completely separate brands: never mix them)

- **Vice City Corner** `@vicecitycorner6`: GTA 6 news. Cyan/yellow text, red
  leetspeak tag pill (TR3NDING, BR3AKING, L3AK, UPDAT3, GAMING, RUMOUR), Rockstar
  screenshots from `library/`, American narrator, synthwave music.
- **Footy Smart** `@footysmart10`: football tactics. Lime/yellow text, lime pill,
  own tactics-board diagrams only, British narrator, lo-fi music. British English.

## Never

- Post, log in to Instagram/Facebook, send messages or pay for anything.
- Invent facts, numbers, dates or quotes. Unconfirmed = RUMOUR/L3AK tag + "not confirmed".
- Use images from Google Images, Pinterest, fan sites or other creators. GTA images
  come only from `library/` (credit "Image: Rockstar Games"); never `Port_Gellhorn_07`.
- Use trailer, match or broadcast footage, club badges, kits or real players' faces.
- Use music other than `factory/music.py` (or none).
- Delete files: move old weeks to `_archive` with `python make.py archive`.

## Always

- Put sources in every caption (`caption.sources` in the plan).
- Check the contact sheets from `python make.py check` before saying you're done.
- Write anything that needs Monty in `NOTE_FOR_MONTY.txt` in that week's folder.
