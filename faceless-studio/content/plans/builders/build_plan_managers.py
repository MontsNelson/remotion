"""Five 45-second manager-tactic reels + two carousels for Footy Smart (week of 15-22 Nov 2026)."""
import json
import sys

sys.path.insert(0, "work")
from build_plan_footy import P, arrow, cap, pl, post, pt  # noqa: E402

ARSENAL = "#EF0107"
CITY = "#6CABDD"
LIVERPOOL = "#C8102E"
LEICESTER = "#1D4ED8"
GREY = "#D7DCE0"

SRC = {
    "pl_arteta": {"name": "Premier League", "url": "https://www.premierleague.com/en/news/3662628"},
    "goal_zinchenko": {"name": "Goal", "url": "https://www.goal.com/en-us/news/no-one-laughing-zinchenko-now-arsenal-inverted-left-back-pivotal-role-title-charge/blt9486ab8222250d75"},
    "cv_arsenal": {"name": "Coaches' Voice", "url": "https://learning.coachesvoice.com/cv/arsenal-mikel-artea-tactics-2022-23/"},
    "pl_city": {"name": "Premier League", "url": "https://www.premierleague.com/en/news/4171827"},
    "cv_city": {"name": "Coaches' Voice", "url": "https://learning.coachesvoice.com/cv/manchester-city-pep-guardiola-treble-tactics-haaland/"},
    "pl_gegen": {"name": "Premier League", "url": "https://www.premierleague.com/en/news/4244321"},
    "fft_gegen": {"name": "FourFourTwo", "url": "https://www.fourfourtwo.com/us/features/football-tactics-gegenpressing"},
    "espn_lei": {"name": "ESPN", "url": "https://www.espn.com/soccer/barclays-premier-league/23/blog/post/2874862/premier-league-tactical-trends-of-2015-16"},
    "tfa_lei": {"name": "Total Football Analysis", "url": "https://totalfootballanalysis.com/opinion/counter-attacking-football-the-perfect-strategy-for-underdogs"},
    "afc_city": {"name": "Arsenal.com", "url": "https://www.arsenal.com/news/arsenal-analysed-how-we-beat-manchester-city"},
    "analyst_city": {"name": "The Analyst (Opta)", "url": "https://theanalyst.com/2023/10/arsenal-vs-manchester-city-stats-premier-league-2023-24/"},
    "sky_city": {"name": "Sky Sports", "url": "https://www.skysports.com/football/news/12977670/arsenal-1-0-man-city-gabriel-martinellis-deflected-strike-clinches-important-win-for-gunners-over-premier-league-title-rivals"},
}
TAGS = ["#footballtactics", "#tacticalanalysis", "#footballcoach", "#premierleague"]


def caption(hook, body, question, sources, extra, **kw):
    c = cap(hook, body, question, [], extra, **kw)
    c["sources"] = [SRC[s] for s in sources]
    c["hashtags"] = list(extra) + TAGS
    return c


def base45(headline, question, colours):
    return {
        "durationInSeconds": 45, "pitchFadeInSeconds": 2.5, "playersEnterAt": 3.7, "playerSizeM": 4.4,
        "colours": colours, "tag": "TACTICS, EXPLAINED", "headline": headline,
        "phases": [{"id": "hook", "caption": None, "from": 0, "to": 3.5},
                   {"id": "problem", "caption": "THE PROBLEM", "from": 3.5, "to": 12},
                   {"id": "idea", "caption": "THE IDEA", "from": 12, "to": 21},
                   {"id": "how", "caption": "HOW IT WORKS", "from": 21, "to": 31},
                   {"id": "why", "caption": "WHY IT WORKED", "from": 31, "to": 40},
                   {"id": "outro", "caption": None, "from": 40, "to": 45}],
        "outro": {"follow": "FOLLOW", "handle": "@FOOTYSMART10", "question": question, "cta": "SAVE THIS + FOLLOW"},
        "voiceover": {"enabled": True, "volume": 1},
        "music": {"enabled": False, "file": "music.mp3", "volume": 0.2},
    }


def headline(a, b, c):
    return [[{"text": a, "colour": "white"}], [{"text": b, "colour": "cyan"}], [{"text": c, "colour": "yellow"}]]


def vo(*lines):
    ids = ["hook", "problem", "idea", "how", "why", "outro"]
    ats = [0.25, 3.8, 12.3, 21.3, 31.3, 40.3]
    return {"lines": [{"id": i, "at": a, "text": t} for i, a, t in zip(ids, ats, lines)]}


def cam(*keys):
    return [{"t": t, "zoom": z, "cx": x, "cy": y, "tilt": tilt} for t, z, x, y, tilt in keys]


def ball(*keys):
    return [{"t": t, "x": x, "y": y} for t, x, y in keys]


def zone(f, t, label, *pts):
    return {"from": f, "to": t, "label": label, "points": [pt(x, y) for x, y in pts]}


def run(f, t, *pts):
    return {"kind": "run", "from": f, "to": t, "points": [pt(x, y) for x, y in pts]}


def lane(f, t, a, b, cut=None):
    d = {"kind": "lane", "from": f, "to": t, "points": [pt(*a), pt(*b)]}
    if cut is not None:
        d["cutAt"] = cut
    return d


def named(n, name, x, y, *moves):
    d = pl(n, x, y, *moves)
    d["name"] = name
    return d


def opp_mid_block(press_moves=True):
    """A neutral 4-4-2 mid block defending the top goal."""
    return [pl(1, 34, 4), pl(2, 56, 30), pl(5, 41, 28), pl(4, 27, 28), pl(3, 12, 30),
            pl(7, 56, 46), pl(8, 40, 46, *(((7, 40, 46), (9, 37, 63)) if press_moves else ())),
            pl(6, 28, 46), pl(11, 12, 46),
            pl(9, 40, 62, *(((7, 40, 62), (9, 42, 76)) if press_moves else ())),
            pl(10, 28, 62, *(((7, 28, 62), (9, 26, 76)) if press_moves else ()))]


# ---------------------------------------------------------------- A: Arteta's inverted left-back
def arteta_inverted():
    t = base45(headline("THE TWEAK THAT", "TURNED ARSENAL", "INTO CONTENDERS"),
               "Who's the best inverted full-back you've seen?",
               {"A": ARSENAL, "B": GREY, "numberA": "#FFFFFF", "numberB": "#1B1B1B"})
    t["teams"] = {
        "A": {"name": "Arsenal", "enterFrom": "bottom", "players": [
            pl(1, 34, 100), pl(4, 60, 80, (13, 60, 80), (15, 54, 84)),
            pl(12, 42, 88), pl(6, 26, 88, (13, 26, 88), (15, 22, 86)),
            named(35, "Zinchenko", 8, 80, (12.6, 8, 80), (15.4, 25, 70)),
            named(5, "Partey", 34, 72, (13, 34, 72), (15.4, 41, 70)),
            named(8, "Odegaard", 48, 58, (24, 48, 58), (27, 50, 44)),
            named(34, "Xhaka", 20, 58, (15.6, 20, 58), (18.6, 18, 40), (26.6, 18, 40), (29, 22, 26)),
            pl(7, 61, 42, (16, 61, 42), (18.6, 63, 30)),
            pl(9, 34, 40, (25.5, 34, 40), (28.6, 33, 16)),
            named(11, "Martinelli", 7, 42, (16, 7, 42), (18.6, 5, 30), (26.4, 5, 30), (28, 8, 18))]},
        "B": {"name": "Opponent", "enterFrom": "top", "players": opp_mid_block()},
    }
    t["ball"] = ball((4, 42, 88), (22.0, 42, 88), (22.7, 25, 70), (24.0, 25, 70), (24.8, 18, 40),
                     (26.6, 18, 40), (27.4, 5, 30), (27.6, 5, 30), (28.2, 8, 18), (28.8, 8, 18), (29.6, 33, 16),
                     (30.0, 33, 16), (30.6, 36, 0.6), (45, 36, 0.6))
    t["goal"] = {"t": 30.6, "at": pt(36, 0.6)}
    t["arrows"] = [lane(7.5, 11.8, (26, 88), (34, 72), cut=9.2), lane(8, 11.8, (42, 88), (34, 72), cut=9.6),
                   run(12.4, 16, (8, 80), (14, 72), (24, 70)),
                   run(15.6, 19, (20, 58), (16, 50), (18, 41)),
                   run(16, 19, (7, 42), (4, 36), (5, 31))]
    t["zones"] = [zone(5.5, 11.8, "ONE HOLDER", (26, 64), (42, 64), (42, 78), (26, 78)),
                  zone(15.6, 30.8, "TWO IN MIDFIELD", (18, 64), (48, 64), (48, 76), (18, 76)),
                  zone(31.2, 39.6, "EXTRA MAN", (16, 62), (50, 62), (50, 78), (16, 78))]
    t["highlights"] = [{"from": 5.5, "to": 11.8, "team": "A", "number": 5}, {"from": 12.4, "to": 21, "team": "A", "number": 35},
                       {"from": 23.6, "to": 26.8, "team": "A", "number": 34}]
    t["camera"] = cam((0, 1.06, 34, 52.5, 0), (3.5, 1.0, 34, 52.5, 0), (7, 1.3, 32, 72, 5), (12, 1.3, 30, 72, 5),
                      (16, 1.15, 28, 62, 5), (21, 1.2, 28, 58, 5), (25, 1.15, 26, 46, 5), (29, 1.25, 26, 26, 5),
                      (31.5, 1.15, 30, 50, 4), (39.5, 1.1, 32, 60, 4), (45, 1.06, 34, 52, 3))
    spec = {"tactic": t, "music": "lofi", "feed": True, "voiceover": vo(
        "This tweak turned Arsenal into contenders.",
        "Twenty twenty-two. Teams pressed Arsenal's centre-backs and smothered Partey, the only holding midfielder.",
        "Arteta's answer: the left-back, Zinchenko, steps inside into midfield, right next to Partey.",
        "Now there are two in the middle to pass through, Xhaka is free to push on, and the wingers stay wide.",
        "An extra man in midfield, without losing any width. Arsenal went from fifth to second.",
        "Follow, Footy Smart Ten, for more tactics.")}
    return spec


# ---------------------------------------------------------------- C: Guardiola's Stones
def guardiola_stones():
    t = base45(headline("THE TWEAK BEHIND", "CITY'S TREBLE", "STONES IN MIDFIELD"),
               "Could your centre-back play in midfield?",
               {"A": CITY, "B": GREY, "numberA": "#1C2C5B", "numberB": "#1B1B1B"})
    t["teams"] = {
        "A": {"name": "Man City", "enterFrom": "bottom", "players": [
            pl(31, 34, 100), pl(2, 60, 80, (13, 60, 80), (15, 54, 85)),
            named(5, "Stones", 44, 87, (12.6, 44, 87), (15.4, 42, 70), (33, 42, 70), (35.6, 44, 85)),
            pl(3, 28, 88, (13, 28, 88), (15, 34, 89)), pl(6, 9, 80, (13, 9, 80), (15, 15, 85)),
            named(16, "Rodri", 34, 72, (13, 34, 72), (15.4, 30, 70)),
            named(17, "De Bruyne", 48, 56, (15.6, 48, 56), (18, 43, 50), (24.6, 43, 50), (26, 44, 46)),
            named(8, "Gundogan", 20, 56, (15.6, 20, 56), (18, 25, 50)),
            pl(20, 61, 40, (18, 61, 40), (20, 62, 30)),
            named(9, "Haaland", 34, 36, (24.8, 34, 36), (27, 38, 18)),
            pl(10, 7, 40, (18, 7, 40), (20, 5, 30))]},
        "B": {"name": "Opponent", "enterFrom": "top", "players": opp_mid_block()},
    }
    t["ball"] = ball((4, 28, 88), (13, 28, 88), (15, 34, 89), (22.0, 34, 89), (22.6, 42, 70), (23.6, 42, 70), (24.4, 43, 50), (26.2, 44, 46),
                     (27.0, 38, 19), (27.6, 38, 18), (28.2, 35, 0.6), (45, 35, 0.6))
    t["goal"] = {"t": 28.2, "at": pt(35, 0.6)}
    t["arrows"] = [lane(7.5, 11.8, (28, 88), (34, 72), cut=9.4),
                   run(12.4, 16, (44, 87), (46, 78), (42, 71)),
                   run(16, 19, (20, 56), (21, 52), (25, 50)), run(16, 19, (48, 56), (46, 52), (43, 50)),
                   run(24.6, 27.4, (34, 36), (40, 28), (38, 19)),
                   run(32.8, 36, (42, 70), (46, 78), (44, 84))]
    t["zones"] = [zone(5.5, 11.8, "ONE HOLDER", (26, 64), (42, 64), (42, 78), (26, 78)),
                  zone(17.6, 30.6, "THE BOX", (20, 46), (48, 46), (48, 74), (20, 74))]
    t["highlights"] = [{"from": 5.5, "to": 11.8, "team": "A", "number": 16}, {"from": 12.4, "to": 21, "team": "A", "number": 5},
                       {"from": 32.8, "to": 37, "team": "A", "number": 5}]
    t["camera"] = cam((0, 1.06, 34, 52.5, 0), (3.5, 1.0, 34, 52.5, 0), (7, 1.3, 34, 72, 5), (12, 1.3, 36, 74, 5),
                      (17, 1.15, 34, 64, 5), (21, 1.15, 34, 60, 5), (24.5, 1.15, 36, 48, 5), (28, 1.25, 36, 24, 5),
                      (31.5, 1.15, 36, 66, 4), (39.5, 1.1, 34, 62, 4), (45, 1.06, 34, 52, 3))
    return {"tactic": t, "music": "lofi", "feed": True, "voiceover": vo(
        "This is the tweak behind Man City's treble.",
        "Rodri was the only holding midfielder, and good teams crowded him out of the game.",
        "So Guardiola pushed a centre-back, John Stones, into midfield, right next to Rodri.",
        "That makes a box in the middle, three at the back, and five across the front.",
        "More passing angles going forward, and when they lose it, Stones drops straight back in.",
        "Follow, Footy Smart Ten, for more tactics.")}


# ---------------------------------------------------------------- D: Klopp's gegenpress
def klopp_gegenpress():
    t = base45(headline("THE PRESS THAT", "WON LIVERPOOL", "THE LEAGUE"),
               "Could your team press like this for 90 minutes?",
               {"A": LIVERPOOL, "B": GREY, "numberA": "#FFFFFF", "numberB": "#1B1B1B"})
    t["teams"] = {
        "A": {"name": "Liverpool", "enterFrom": "bottom", "players": [
            pl(1, 34, 96), pl(66, 62, 40, (13, 62, 40), (15.4, 59, 32)),
            pl(4, 40, 62), pl(12, 26, 62), pl(26, 6, 40),
            pl(3, 34, 50, (13, 34, 50), (15.6, 38, 40)),
            named(14, "Henderson", 48, 36, (13, 48, 36), (15.2, 52, 30.5), (21.2, 52, 30.5), (21.8, 54, 28.5)),
            pl(5, 20, 36),
            named(11, "Salah", 56, 20, (13, 56, 20), (15, 57, 24), (22.6, 57, 24), (24.6, 48, 9)),
            named(9, "Firmino", 34, 24, (13, 34, 24), (15.4, 46, 26), (22, 46, 26), (23, 44, 24)),
            named(10, "Mane", 12, 20, (22, 12, 20), (24.6, 22, 10))]},
        "B": {"name": "Opponent", "enterFrom": "top", "players": [
            pl(1, 34, 4, (25.4, 34, 4), (26, 37, 3)), pl(2, 54, 14), pl(5, 40, 12), pl(4, 28, 12), pl(3, 14, 14),
            pl(7, 54, 28, (8.2, 54, 28), (9.2, 54, 26)), pl(8, 40, 30), pl(6, 28, 30), pl(11, 14, 28),
            pl(9, 40, 48), pl(10, 28, 46)]},
    }
    t["ball"] = ball((4, 48, 36), (8.0, 48, 36), (9.0, 54, 26), (21.2, 54, 26), (21.6, 54, 28.5), (22.2, 54, 28.5),
                     (22.9, 44, 24), (23.2, 44, 24), (24.0, 50, 11), (24.6, 48, 9), (25.0, 48, 9), (25.6, 38, 0.6),
                     (45, 38, 0.6))
    t["goal"] = {"t": 25.6, "at": pt(38, 0.6)}
    t["arrows"] = [lane(9.4, 11.8, (54, 26), (40, 48)), lane(9.6, 11.8, (54, 26), (28, 46)),
                   run(12.6, 15.6, (48, 36), (52, 34), (52, 31)), run(12.6, 15.6, (56, 20), (58, 22), (57, 24)),
                   run(12.8, 15.8, (34, 24), (42, 24), (46, 26)), run(12.8, 15.8, (62, 40), (62, 35), (59, 32)),
                   lane(15.8, 20.8, (54, 26), (40, 30), cut=17.2), lane(16.2, 20.8, (54, 26), (54, 14), cut=18.0),
                   lane(16.6, 20.8, (54, 26), (40, 48), cut=18.8),
                   run(22.4, 25, (57, 24), (54, 14), (48, 9))]
    t["zones"] = [zone(9.4, 11.8, "COUNTER DANGER", (24, 40), (60, 40), (60, 70), (24, 70)),
                  zone(13.2, 21.4, "WIN IT IN 6 SECONDS", (44, 18), (64, 18), (64, 36), (44, 36))]
    t["highlights"] = [{"from": 12.6, "to": 21.8, "team": "A", "number": 14}, {"from": 22.6, "to": 25.6, "team": "A", "number": 11}]
    t["camera"] = cam((0, 1.06, 34, 52.5, 0), (3.5, 1.0, 34, 52.5, 0), (7, 1.25, 44, 36, 5), (12, 1.25, 44, 40, 5),
                      (15, 1.55, 52, 28, 6), (21, 1.55, 52, 28, 6), (25, 1.35, 46, 16, 5), (31.5, 1.15, 40, 32, 4),
                      (39.5, 1.1, 36, 44, 4), (45, 1.06, 34, 52, 3))
    return {"tactic": t, "music": "lofi", "feed": True, "voiceover": vo(
        "This is the press that won Liverpool the league.",
        "When you attack and lose the ball, the other team counters into all the space you've left.",
        "Klopp's answer: the moment you lose it, the nearest players hunt it straight back.",
        "Win it in seconds, high up the pitch, and one pass puts you through on goal.",
        "Their defence is still out of shape. That's how Liverpool won the league in twenty twenty.",
        "Follow, Footy Smart Ten, for more tactics.")}


# ---------------------------------------------------------------- G: Ranieri's Leicester
def ranieri_leicester():
    t = base45(headline("HOW LEICESTER", "WON THE LEAGUE", "AT 5000-1"),
               "Will we ever see another Leicester?",
               {"A": LEICESTER, "B": GREY, "numberA": "#FFFFFF", "numberB": "#1B1B1B"})
    t["teams"] = {
        "A": {"name": "Leicester", "enterFrom": "bottom", "players": [
            pl(1, 34, 100), pl(17, 56, 87), pl(5, 40, 90), pl(6, 28, 90), pl(28, 12, 87),
            named(26, "Mahrez", 58, 75, (22, 58, 75), (26, 60, 44)),
            named(14, "Kante", 40, 76, (14, 40, 76), (15.6, 35, 80.5), (16.6, 33, 79)),
            named(4, "Drinkwater", 27, 76, (16, 27, 76), (17.2, 28, 72)),
            pl(11, 10, 74), pl(20, 30, 62, (22, 30, 62), (26, 34, 40)),
            named(9, "Vardy", 42, 58, (21.4, 42, 58), (23, 48, 44), (25.2, 46, 22), (26.4, 42, 14))]},
        "B": {"name": "Big club", "enterFrom": "top", "players": [
            pl(1, 34, 4), pl(2, 54, 48), pl(5, 40, 46), pl(4, 28, 46), pl(3, 14, 48),
            pl(8, 48, 62, (5.5, 48, 62), (7, 46, 64)), pl(6, 34, 64), pl(10, 20, 62),
            pl(7, 58, 72), pl(9, 36, 81, (15.2, 36, 81), (16, 38, 83)), pl(11, 12, 72)]},
    }
    t["ball"] = ball((4, 34, 64), (5.6, 34, 64), (6.4, 46, 64), (8.0, 46, 64), (8.8, 20, 62), (10.4, 20, 62),
                     (11.2, 34, 64), (14.2, 34, 64), (15.2, 35, 79.5), (16.0, 35, 79.5), (16.8, 28, 72.5),
                     (22.6, 28, 72.5), (23.9, 46, 30), (25.2, 46, 22), (26.4, 42, 14), (26.8, 42, 14),
                     (27.4, 35, 0.6), (45, 35, 0.6))
    t["goal"] = {"t": 27.4, "at": pt(35, 0.6)}
    t["arrows"] = [lane(14.2, 15.6, (34, 64), (36, 81), cut=15.2),
                   run(22.2, 25.4, (42, 58), (50, 42), (46, 23)),
                   run(22.4, 26, (58, 75), (62, 60), (60, 45)),
                   lane(22.2, 24.2, (28, 72), (46, 30))]
    t["zones"] = [zone(4.5, 15, "DEEP AND COMPACT", (6, 70), (62, 70), (62, 93), (6, 93)),
                  zone(21.6, 30.6, "SPACE BEHIND", (10, 14), (60, 14), (60, 42), (10, 42))]
    t["highlights"] = [{"from": 12.4, "to": 17, "team": "A", "number": 14}, {"from": 21.4, "to": 27.4, "team": "A", "number": 9}]
    t["camera"] = cam((0, 1.06, 34, 52.5, 0), (3.5, 1.0, 34, 52.5, 0), (6, 1.2, 34, 72, 5), (13, 1.3, 34, 76, 5),
                      (17, 1.3, 32, 72, 5), (21.5, 1.05, 36, 50, 4), (25.5, 1.25, 42, 24, 5), (31.5, 1.1, 36, 48, 4),
                      (39.5, 1.05, 34, 54, 4), (45, 1.06, 34, 52, 3))
    return {"tactic": t, "music": "lofi", "feed": True, "voiceover": vo(
        "How Leicester won the league at five thousand to one.",
        "Less money, less of the ball. So Ranieri didn't try to out-pass anyone.",
        "Two deep banks of four, and Kante hunting every loose ball in front of them.",
        "Win it, and go. One long ball over the top for Vardy's pace.",
        "Big teams pushed up and left space behind for Vardy. Five thousand to one, and champions.",
        "Follow, Footy Smart Ten, for more tactics.")}


# ---------------------------------------------------------------- H: Arteta v City, Oct 2023
def arteta_beats_city():
    t = base45(headline("HOW ARTETA", "FINALLY BEAT", "PEP'S CITY"),
               "What's the best Arsenal win over City?",
               {"A": ARSENAL, "B": CITY, "numberA": "#FFFFFF", "numberB": "#1C2C5B"})
    t["teams"] = {
        "A": {"name": "Arsenal", "enterFrom": "bottom", "players": [
            pl(22, 34, 100), pl(4, 60, 82), pl(2, 42, 88), pl(6, 26, 88), pl(3, 8, 82),
            named(20, "Jorginho", 20, 58, (12.6, 20, 58), (14.8, 28, 72)),
            named(41, "Rice", 34, 72, (12.6, 34, 72), (14.8, 41, 72), (31.4, 41, 72), (33.4, 40, 30)),
            pl(8, 48, 56), named(29, "Havertz", 30, 50, (31.4, 30, 50), (33.4, 33, 22)),
            pl(7, 60, 40),
            named(11, "Martinelli", 8, 40, (31.4, 8, 40), (33.8, 24, 18))]},
        "B": {"name": "Man City", "enterFrom": "top", "players": [
            pl(31, 34, 4), pl(2, 56, 30), pl(3, 42, 28), pl(6, 28, 28), pl(25, 12, 30),
            pl(16, 34, 46), pl(17, 48, 50, (6, 48, 50), (8.5, 44, 66)), pl(20, 22, 50, (6, 22, 50), (8.5, 24, 66)),
            pl(47, 58, 56, (6, 58, 56), (8.5, 56, 76)), pl(9, 34, 62, (6, 34, 62), (8.5, 38, 80)),
            pl(10, 10, 56, (6, 10, 56), (8.5, 14, 76))]},
    }
    t["ball"] = ball((4, 42, 88), (22.0, 42, 88), (22.6, 41, 72), (23.4, 41, 72), (24.0, 28, 72), (25.0, 28, 72),
                     (25.8, 48, 56), (31.4, 48, 56), (33.4, 40, 30), (34.0, 33.5, 22.5), (34.4, 33.5, 22.5),
                     (35.0, 24, 18.5), (35.2, 24, 18.5), (35.8, 36, 0.6), (45, 36, 0.6))
    t["goal"] = {"t": 35.8, "at": pt(36, 0.6)}
    t["arrows"] = [lane(8.8, 11.8, (42, 88), (34, 72), cut=9.6),
                   lane(22.2, 24.4, (41, 72), (28, 72)), lane(24.4, 26.2, (28, 72), (48, 56)),
                   lane(26.6, 30.6, (44, 66), (40, 80), cut=27.6), lane(26.8, 30.6, (24, 66), (30, 82), cut=28.2),
                   run(31.6, 34.2, (8, 40), (14, 26), (24, 19))]
    t["zones"] = [zone(5, 11.8, "CITY'S PRESS", (6, 60), (62, 60), (62, 86), (6, 86)),
                  zone(14.6, 30.6, "DOUBLE PIVOT", (22, 66), (48, 66), (48, 78), (22, 78))]
    t["highlights"] = [{"from": 5, "to": 11.8, "team": "A", "number": 41}, {"from": 12.6, "to": 21, "team": "A", "number": 20},
                       {"from": 31.6, "to": 35.8, "team": "A", "number": 11}]
    t["camera"] = cam((0, 1.06, 34, 52.5, 0), (3.5, 1.0, 34, 52.5, 0), (7, 1.2, 34, 72, 5), (12, 1.3, 34, 74, 5),
                      (21, 1.3, 36, 70, 5), (26, 1.2, 38, 64, 5), (31, 1.1, 34, 50, 4), (34.4, 1.35, 30, 20, 5),
                      (36.5, 1.35, 32, 14, 5), (39.5, 1.1, 34, 40, 4), (45, 1.06, 34, 52, 3))
    return {"tactic": t, "music": "lofi", "feed": True, "voiceover": vo(
        "How Arteta finally beat Pep's City.",
        "Twelve league defeats in a row to City, and their press kept swallowing Arsenal's midfield.",
        "So Arteta started Jorginho next to Declan Rice. Two holding midfielders, side by side.",
        "Two passing options in the middle, and two bodies to block City's central passes.",
        "Late on, Rice heads it down, Havertz lays it off, and Martinelli's shot deflects in. One nil.",
        "Follow, Footy Smart Ten, for more tactics.")}


# ---------------------------------------------------------------- carousels for the top two
ARS_V_GREY = {"a": ARSENAL, "num_a": "#FFFFFF", "b": GREY, "num_b": "#1B1B1B"}
ARS_V_CITY = {"a": ARSENAL, "num_a": "#FFFFFF", "b": CITY, "num_b": "#1C2C5B"}


def N(n, name, x, y):
    return {"n": n, "name": name, "x": x, "y": y}


def with_colours(spec, colours):
    for key in ["cover_board"]:
        spec[key]["colours"] = colours
    for slide in spec["slides"]:
        if slide.get("board"):
            slide["board"]["colours"] = colours
    return spec


def arteta_inverted_carousel():
    before = [P(1, 34, 101), P(4, 60, 80), P(12, 42, 88), P(6, 26, 88), N(35, "Zinchenko", 8, 80), N(5, "Partey", 34, 72),
              P(8, 48, 58), N(34, "Xhaka", 20, 58), P(7, 61, 42), P(9, 34, 40), P(11, 7, 42)]
    after = [P(1, 34, 101), P(4, 54, 84), P(12, 42, 88), P(6, 22, 86), N(35, "Zinchenko", 25, 70), N(5, "Partey", 41, 70),
             P(8, 48, 58), N(34, "Xhaka", 18, 40), P(7, 63, 30), P(9, 34, 40), P(11, 5, 30)]
    opp = [P(9, 40, 76), P(10, 26, 76), P(8, 37, 63), P(6, 28, 50), P(7, 52, 50)]
    return {"kind": "tactics", "tag": "ARTETA", "headline": "THE TWEAK THAT TURNED [c]ARSENAL[/c] INTO [y]CONTENDERS[/y]",
            "cover_board": {"view": [30, 105], "team_a": after, "team_b": opp, "highlight": {"team": "a", "n": 35},
                            "arrows": [arrow("run", (8, 80), (14, 72), (24, 70))]},
            "slides": [
                {"step": "THE PROBLEM", "text": "PRESSED HIGH, [c]PARTEY[/c] WAS THE ONLY HOLDER, AND GOT SMOTHERED",
                 "board": {"view": [30, 105], "team_a": before, "team_b": opp, "highlight": {"team": "a", "n": 5},
                           "arrows": [arrow("pass", (26, 87), (33, 73.5))], "cuts": [[29.5, 80]]}},
                {"step": "THE IDEA", "text": "LEFT-BACK [c]ZINCHENKO[/c] STEPS INSIDE, NEXT TO PARTEY",
                 "board": {"view": [30, 105], "team_a": after, "team_b": opp, "highlight": {"team": "a", "n": 35},
                           "arrows": [arrow("run", (8, 80), (14, 72), (24, 70))],
                           "zones": [{"points": [[18, 64], [48, 64], [48, 76], [18, 76]], "label": "TWO IN MIDFIELD"}]}},
                {"step": "HOW IT WORKS", "text": "[c]XHAKA[/c] PUSHES ON, THE WINGERS STAY WIDE",
                 "board": {"view": [20, 95], "team_a": after, "team_b": opp, "highlight": {"team": "a", "n": 34},
                           "arrows": [arrow("run", (20, 58), (16, 50), (18, 41)), arrow("pass", (25, 69), (18, 41.5))]}},
                {"text": "THE RESULT: ARSENAL WENT FROM [c]FIFTH[/c] TO [y]SECOND[/y]"},
                {"text": "WHO'S THE BEST INVERTED FULL-BACK [y]YOU'VE SEEN?[/y]"}]}


def arteta_city_carousel():
    ars = [P(22, 34, 101), P(4, 60, 82), P(2, 42, 88), P(6, 26, 88), P(3, 8, 82), N(20, "Jorginho", 28, 72), N(41, "Rice", 41, 72),
           P(8, 48, 56), P(29, 30, 50), P(7, 60, 40), P(11, 8, 40)]
    city_press = [P(9, 38, 80), P(10, 14, 76), P(47, 56, 76), P(17, 44, 66), P(20, 24, 66), P(16, 34, 46)]
    return {"kind": "tactics", "tag": "ARTETA", "headline": "HOW [c]ARTETA[/c] FINALLY BEAT [y]PEP'S CITY[/y]",
            "cover_board": {"view": [36, 105], "team_a": ars, "team_b": city_press,
                            "zones": [{"points": [[22, 66], [48, 66], [48, 78], [22, 78]], "label": "DOUBLE PIVOT"}]},
            "slides": [
                {"step": "THE PROBLEM", "text": "[c]12[/c] LEAGUE DEFEATS IN A ROW TO CITY. THEIR PRESS SWALLOWED ARSENAL'S MIDFIELD",
                 "board": {"view": [36, 105], "team_a": ars, "team_b": city_press, "cuts": [[37, 80]],
                           "arrows": [arrow("pass", (42, 87), (34, 73))]}},
                {"step": "THE IDEA", "text": "[c]JORGINHO[/c] STARTS NEXT TO [c]RICE[/c]: TWO HOLDERS SIDE BY SIDE",
                 "board": {"view": [36, 105], "team_a": ars, "team_b": city_press, "highlight": {"team": "a", "n": 20},
                           "zones": [{"points": [[22, 66], [48, 66], [48, 78], [22, 78]], "label": "DOUBLE PIVOT"}]}},
                {"step": "HOW IT WORKS", "text": "TWO PASSING OPTIONS, AND TWO BODIES BLOCKING [c]CITY'S CENTRAL PASSES[/c]",
                 "board": {"view": [36, 105], "team_a": ars, "team_b": city_press,
                           "arrows": [arrow("pass", (41, 71), (29, 72)), arrow("pass", (29, 71), (47, 57))]}},
                {"text": "THEN [c]MARTINELLI[/c], 86 MINUTES, DEFLECTED IN. [y]1-0[/y]. FIRST LEAGUE WIN OVER CITY SINCE 2015"},
                {"text": "BEST ARSENAL WIN [y]OVER CITY?[/y]"}]}


def build():
    posts = []
    posts.append(post("2026-11-15", "21:00", "reel", "arteta-inverted-full-back", "The tweak that turned Arsenal into contenders",
        arteta_inverted(),
        caption("The tweak that turned Arsenal into contenders.",
                ["2022-23: Zinchenko steps in from left-back next to Partey.", "Two in midfield, Xhaka pushes on, the wingers stay wide."],
                "Who's the best inverted full-back you've seen?", ["pl_arteta", "goal_zinchenko", "cv_arsenal"],
                ["#arsenal", "#arteta", "#zinchenko", "#invertedfullback"],
                first_comment="Zinchenko or Timber in this role? 👇",
                alt="Animated tactics board: Arsenal's left-back moves into midfield next to the holding midfielder.",
                story="Poll sticker: 'Inverted full-backs: genius or overrated?'",
                check="Shape details vary between analysts (2-3-5 or 3-2-5). The video keeps it simple on purpose.")))
    posts.append(post("2026-11-16", "21:00", "reel", "guardiola-stones-midfield", "The tweak behind City's treble",
        guardiola_stones(),
        caption("The tweak behind Man City's treble.",
                ["2022-23: Guardiola pushes centre-back John Stones into midfield next to Rodri.",
                 "A box in midfield, three at the back, five across the front."],
                "Could your centre-back play in midfield?", ["pl_city", "cv_city"],
                ["#mancity", "#guardiola", "#johnstones", "#treble"],
                first_comment="Best Guardiola tweak ever? 👇",
                alt="Animated tactics board: a centre-back steps into midfield to form a box with three midfielders.",
                story="Quiz sticker: 'Who stepped into midfield?' Stones / Walker / Dias")))
    posts.append(post("2026-11-18", "21:00", "reel", "klopp-gegenpress", "The press that won Liverpool the league",
        klopp_gegenpress(),
        caption("The press that won Liverpool the league.",
                ["Lose the ball, and the nearest players hunt it straight back.", "Win it high, and their defence is still out of shape."],
                "Could your team press like this for 90 minutes?", ["pl_gegen", "fft_gegen"],
                ["#liverpool", "#klopp", "#gegenpressing", "#counterpress"],
                first_comment="Which team presses best right now? 👇",
                alt="Animated tactics board: Liverpool lose the ball, swarm the carrier, win it back and score.",
                story="Quiz sticker: 'Gegenpress means...' Counter-press / Long ball / Low block")))
    posts.append(post("2026-11-20", "21:00", "reel", "arteta-beats-city", "How Arteta finally beat Pep's City",
        arteta_beats_city(),
        caption("How Arteta finally beat Pep's City.",
                ["October 2023: Jorginho starts next to Rice, two holders against City's press.",
                 "Martinelli wins it late, Arsenal's first league win over City since December 2015."],
                "What's the best Arsenal win over City?", ["afc_city", "analyst_city", "sky_city"],
                ["#arsenal", "#arteta", "#mancity", "#afc"],
                first_comment="Newcastle tomorrow: prediction? 👇",
                alt="Animated tactics board: Arsenal's double pivot beats City's press, then the late winner.",
                story="Poll sticker: 'Arsenal win at Newcastle tomorrow?' Yes / No",
                check="Facts from Arsenal.com's own analysis, The Analyst and Sky Sports. Positions are a simplified illustration.")))
    posts.append(post("2026-11-22", "21:00", "reel", "ranieri-leicester", "How Leicester won the league at 5000-1",
        ranieri_leicester(),
        caption("How Leicester won the league at 5000-1.",
                ["Two deep banks of four, Kante winning everything, then one ball over the top for Vardy."],
                "Will we ever see another Leicester?", ["espn_lei", "tfa_lei"],
                ["#leicester", "#ranieri", "#vardy", "#kante"],
                first_comment="Greatest Premier League story ever? 👇",
                alt="Animated tactics board: Leicester defend deep, Kante wins the ball and a long pass sends Vardy through.",
                story="Slider sticker: 'How shocked were you in 2016?'",
                check="The 5000-1 odds were the pre-season bookmaker price. No other stats are used.")))
    posts.append(post("2026-11-17", "19:00", "carousel", "arteta-inverted-carousel", "The tweak that turned Arsenal into contenders",
        with_colours(arteta_inverted_carousel(), ARS_V_GREY),
        caption("Why did Arsenal's left-back play in midfield?",
                ["Zinchenko stepped in next to Partey: two in midfield, Xhaka free, wingers wide.", "Arsenal went from fifth to second."],
                "Who's the best inverted full-back you've seen?", ["pl_arteta", "goal_zinchenko"],
                ["#arsenal", "#arteta", "#zinchenko"],
                first_comment="Save this for your next team talk 📌",
                alt="Tactics diagrams of Arsenal's 2022-23 inverted left-back.",
                story="Poll sticker: 'Zinchenko: underrated?'")))
    posts.append(post("2026-11-19", "19:00", "carousel", "arteta-city-carousel", "How Arteta finally beat Pep's City",
        with_colours(arteta_city_carousel(), ARS_V_CITY),
        caption("How Arteta finally beat Pep's City.",
                ["Jorginho next to Rice: two holders against City's press, two bodies blocking the middle.",
                 "Then Martinelli, 86 minutes. 1-0."],
                "Best Arsenal win over City?", ["afc_city", "analyst_city"],
                ["#arsenal", "#arteta", "#mancity"],
                first_comment="Where were you when Martinelli scored? 👇",
                alt="Tactics diagrams of Arsenal's double pivot against Manchester City in October 2023.",
                story="Quiz sticker: 'Who scored the winner?' Martinelli / Saka / Havertz")))
    return posts


if __name__ == "__main__":
    plan = {"notes": {"footy": ["Manager tactics week: five 45-second reels (with 4:5 feed versions) at 21:00.",
                                "Arsenal-heavy before Newcastle v Arsenal on Saturday at 17:30."]},
            "swaps": [], "posts": build()}
    json.dump(plan, open("content/plans/2026-11-14_manager-tactics.json", "w"), indent=2, ensure_ascii=False)
    print(len(plan["posts"]), "posts")
