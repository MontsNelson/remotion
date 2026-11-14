"""Footy Smart posts for 14-22 Nov 2026 (hard launch). Checked 14 Nov 2026."""
import copy
import json

SRC = {
    "sky_setpieces": {"name": "Sky Sports", "url": "https://www.skysports.com/football/news/13601338/arsenal-were-set-piece-kings-last-season-so-why-have-they-stopped-scoring-from-set-pieces-between-the-lines-explains"},
    "analyst_corners": {"name": "The Analyst (Opta)", "url": "https://theanalyst.com/articles/arsenal-corner-struggles-no-goals-premier-league-title"},
    "breaks": {"name": "Premier League calendar via TwentyClubs", "url": "https://twentyclubs.com/international-breaks"},
    "fixture": {"name": "OddSonar", "url": "https://oddsonar.com/en/magazine/international-breaks-2026-27-when-leagues-resume"},
    "explainer": {"name": "Footy Smart tactics explainer (no match stats used)", "url": ""},
}
TAGS = ["#footballtactics", "#tacticalanalysis", "#footballcoach", "#soccertactics", "#coaching", "#premierleague"]
OUTRO_HANDLE = "@FOOTYSMART10"


def post(date, time, type_, slug, headline, spec, caption):
    return {"account": "footy", "date": date, "time": time, "type": type_, "slug": slug,
            "headline": headline, "spec": spec, "caption": caption}


def cap(hook, body, question, sources, extra=(), first_comment="", alt="", story="", check="", mood="calm lo-fi house"):
    return {"hook": hook, "body": body, "question": question, "sources": [SRC[s] for s in sources],
            "hashtags": list(extra) + TAGS, "first_comment": first_comment, "alt_text": alt,
            "story_idea": story, "check": check, "music_mood": mood, "uses_rockstar_images": False}


def P(n, x, y):
    return {"n": n, "x": x, "y": y}


def arrow(kind, *pts):
    return {"kind": kind, "points": [list(p) for p in pts]}


# ---------------------------------------------------------------- carousels
def low_block():
    lime_442 = [P(2, 56, 92), P(5, 42, 94), P(4, 26, 94), P(3, 12, 92),
                P(7, 58, 82), P(8, 42, 83), P(6, 26, 83), P(11, 10, 82), P(9, 30, 70), P(10, 40, 70)]
    red_att = [P(6, 34, 62), P(8, 50, 68), P(10, 18, 68), P(7, 63, 76), P(11, 5, 76), P(9, 34, 88)]
    cover = {"view": [50, 105], "team_a": lime_442 + [P(1, 34, 102)], "team_b": red_att,
             "ball": {"x": 34, "y": 62},
             "zones": [{"points": [[4, 79], [64, 79], [64, 96], [4, 96]], "label": "NO SPACE"}]}
    s1 = copy.deepcopy(cover)
    s1["arrows"] = [arrow("pass", (34, 63), (34, 86))]
    s1["cuts"] = [[34, 76]]
    s1["zones"] = [{"points": [[4, 79], [64, 79], [64, 96], [4, 96]], "label": "COMPACT"}]
    s2 = {"view": [58, 105], "team_a": [P(2, 57, 88), P(5, 42, 96), P(4, 30, 96), P(3, 14, 94), P(6, 36, 89), P(8, 46, 86), P(1, 34, 102)],
          "team_b": [P(7, 63, 84), P(9, 36, 94), P(11, 24, 95)], "ball": {"x": 63, "y": 84},
          "arrows": [arrow("run", (57, 88), (60, 88), (61, 85.5)), arrow("pass", (63, 84), (52, 92), (34, 97))],
          "highlight": {"team": "b", "n": 7}}
    s3 = {"view": [36, 105], "team_a": [P(5, 40, 93), P(4, 26, 94), P(8, 46, 84), P(10, 24, 76), P(9, 34, 70), P(7, 58, 80), P(1, 34, 102)],
          "team_b": [P(9, 36, 90), P(6, 34, 66), P(8, 50, 70)], "ball": {"x": 40, "y": 93},
          "arrows": [arrow("pass", (40, 92), (24, 77)), arrow("run", (34, 69), (42, 58), (42, 46)),
                     arrow("run", (58, 79), (62, 64), (58, 50))],
          "highlight": {"team": "a", "n": 5}}
    return {"kind": "tactics", "tag": "TACTICS", "headline": "THE [c]LOW BLOCK[/c]: HOW UNDERDOGS [y]SHUT OUT BIG TEAMS[/y]",
            "cover_board": cover,
            "slides": [
                {"step": "STEP 1", "text": "TWO BANKS SIT DEEP: [c]NO SPACE[/c] BETWEEN THE LINES", "board": s1},
                {"step": "STEP 2", "text": "SHOW THEM WIDE: A CROSS INTO A [c]CROWDED BOX[/c] IS EASY TO DEFEND", "board": s2},
                {"step": "STEP 3", "text": "WIN IT AND [y]BREAK FAST[/y]: THE COUNTER IS THE PAYOFF", "board": s3},
                {"text": "WHICH TEAM PARKS THE BUS [y]BEST?[/y]"}]}


def inverted_fullback():
    base = [P(1, 34, 101), P(3, 8, 78), P(4, 25, 86), P(5, 43, 86), P(2, 60, 78), P(6, 34, 72),
            P(8, 47, 60), P(10, 21, 60), P(7, 61, 46), P(9, 34, 42), P(11, 7, 46)]
    red_press = [P(9, 28, 76), P(10, 42, 76), P(6, 24, 58), P(8, 36, 56), P(7, 50, 58)]
    cover = {"view": [38, 105], "team_a": base, "team_b": red_press, "ball": {"x": 43, "y": 86},
             "arrows": [arrow("run", (60, 78), (58, 70), (46, 68))], "highlight": {"team": "a", "n": 2}}
    shape32 = [P(1, 34, 101), P(3, 12, 82), P(4, 28, 88), P(5, 45, 86), P(6, 30, 72), P(2, 44, 69),
               P(8, 50, 56), P(10, 20, 58), P(7, 63, 46), P(9, 34, 42), P(11, 6, 46)]
    s1 = copy.deepcopy(cover)
    s2 = {"view": [38, 105], "team_a": shape32, "team_b": red_press, "ball": {"x": 45, "y": 86},
          "zones": [{"points": [[8, 66], [52, 66], [52, 92], [8, 92]], "label": "3-2 BASE"}],
          "arrows": [arrow("pass", (45, 85), (44, 70.5)), arrow("pass", (28, 87), (30, 73.5))]}
    s3 = {"view": [38, 105], "team_a": shape32, "team_b": [P(9, 30, 82), P(10, 42, 80), P(6, 24, 60), P(8, 36, 58), P(7, 52, 60)],
          "ball": {"x": 45, "y": 86}, "arrows": [arrow("pass", (45, 85), (44, 70.5)), arrow("pass", (44, 68), (50, 57.5))],
          "cuts": [[37, 86]], "highlight": {"team": "a", "n": 2}}
    s4 = {"view": [20, 95], "team_a": shape32, "team_b": [P(3, 56, 36), P(5, 44, 32), P(8, 36, 50)],
          "ball": {"x": 44, "y": 69}, "arrows": [arrow("run", (63, 46), (65, 38), (64, 28)), arrow("pass", (44, 68), (60, 52), (63, 44))],
          "highlight": {"team": "a", "n": 7}}
    return {"kind": "tactics", "tag": "TACTICS", "headline": "THE [c]INVERTED FULL-BACK[/c], EXPLAINED [y]IN 4 SLIDES[/y]",
            "cover_board": cover,
            "slides": [
                {"step": "STEP 1", "text": "ON THE BALL, THE RIGHT-BACK [c]STEPS INTO MIDFIELD[/c]", "board": s1},
                {"step": "STEP 2", "text": "THAT MAKES A [c]3-2 BASE[/c]: THREE AT THE BACK, TWO IN FRONT", "board": s2},
                {"step": "STEP 3", "text": "MORE [c]PASSING ANGLES[/c] AGAINST THE PRESS, AND COVER IF YOU LOSE IT", "board": s3},
                {"step": "STEP 4", "text": "THE WINGER STAYS [c]WIDE[/c] TO KEEP THE PITCH BIG", "board": s4},
                {"text": "WOULD YOU PLAY [y]AN INVERTED FULL-BACK?[/y]"}]}


def corners_setup(with_arrows=False, screens=False, runs=False):
    lime = [P(7, 66, 1.6), P(6, 37, 2.6), P(4, 31, 3.2), P(5, 42.5, 15.5), P(2, 31, 15.5),
            P(9, 44.5, 12) if screens else P(9, 47, 14), P(8, 30.8, 12) if screens else P(8, 25, 12), P(10, 34, 22), P(11, 52, 18)]
    red = [P(1, 34, 1.8), P(4, 30, 6.2), P(5, 34, 6.4), P(6, 38, 6.2), P(3, 42, 6.6), P(2, 40.5, 12.5), P(8, 28, 13),
           P(7, 47.5, 10), P(10, 34, 18.5), P(11, 22, 16)]
    b = {"view": [0, 24], "view_x": [20, 68], "dot_size": 1.25, "team_a": lime, "team_b": red, "ball": {"x": 67, "y": 0.9}}
    arrows = []
    if with_arrows:
        arrows.append(arrow("pass", (66.5, 1.2), (52, 11), (39.5, 8.5)))
    if runs:
        arrows += [arrow("run", (42.5, 15.5), (41, 11), (39.5, 9)), arrow("run", (31, 15.5), (33, 12.5), (34.5, 10.2))]
    if screens:
        arrows += [arrow("run", (25, 12), (28, 11.5), (30.2, 12)), arrow("run", (47, 14), (46, 12.5), (44.8, 12.1))]
    b["arrows"] = arrows
    return b


def arsenal_corners():
    cover = corners_setup(with_arrows=True, runs=True)
    s_gk = corners_setup()
    s_gk["zones"] = [{"points": [[29, 0.4], [40, 0.4], [40, 4.8], [29, 4.8]], "label": "KEEPER CROWDED"}]
    s_gk["highlight"] = {"team": "a", "n": 6}
    s_screen = corners_setup(screens=True)
    s_screen["highlight"] = {"team": "a", "n": 9}
    s_ball = corners_setup(with_arrows=True, screens=True, runs=True)
    s_ball["zones"] = [{"points": [[34, 7.2], [44, 7.2], [44, 11], [34, 11]], "label": "FRONT ZONE"}]
    return {"kind": "tactics", "tag": "TACTICS", "headline": "HOW [c]ARSENAL'S CORNERS[/c] WORK, AND WHY THEY'VE [y]GONE QUIET[/y]",
            "cover_board": cover,
            "slides": [
                {"text": "LAST SEASON ARSENAL WERE THE PREMIER LEAGUE'S [c]SET-PIECE KINGS[/c]", "board": corners_setup()},
                {"step": "STEP 1", "text": "CROWD THE [c]GOALKEEPER[/c] SO HE CAN'T COME AND CLAIM IT", "board": s_gk},
                {"step": "STEP 2", "text": "[c]SCREENS[/c]: TEAMMATES STEP ACROSS THE MARKERS", "board": s_screen},
                {"step": "STEP 3", "text": "AN [c]INSWINGER[/c] INTO THE FRONT ZONE, AND RUNNERS ATTACK IT", "board": s_ball},
                {"text": "THIS SEASON THE CORNER GOALS HAVE [y]DRIED UP[/y]"},
                {"text": "HAVE TEAMS FIGURED IT OUT, [y]OR IS IT A BLIP?[/y]"}]}


def rest_defence():
    attack = [P(9, 34, 14), P(11, 12, 20), P(7, 58, 18), P(10, 24, 28), P(8, 44, 26), P(2, 62, 34), P(3, 6, 34),
              P(6, 34, 46), P(4, 27, 56), P(5, 41, 56), P(1, 34, 100)]
    red = [P(9, 30, 61), P(10, 39, 62), P(5, 40, 14), P(4, 28, 14), P(8, 34, 24)]
    zone = {"points": [[22, 42], [46, 42], [46, 62], [22, 62]], "label": "REST DEFENCE"}
    cover = {"view": [6, 72], "team_a": attack, "team_b": red, "ball": {"x": 24, "y": 28}, "zones": [zone]}
    s1 = copy.deepcopy(cover)
    s1["highlight"] = {"team": "a", "n": 6}
    s2 = copy.deepcopy(cover)
    s2["zones"] = []
    s2["highlight"] = {"team": "a", "n": 4}
    s2["arrows"] = [arrow("run", (27, 56), (28, 59), (29.5, 60)), arrow("run", (41, 56), (40, 59), (39.5, 60))]
    s3 = copy.deepcopy(cover)
    s3["zones"] = []
    s3["ball"] = {"x": 34, "y": 24}
    s3["arrows"] = [arrow("pass", (34, 25), (35, 60))]
    s3["cuts"] = [[34.5, 50]]
    return {"kind": "tactics", "tag": "TACTICS", "headline": "[c]REST DEFENCE[/c]: WHY THE BEST TEAMS [y]NEVER GET COUNTERED[/y]",
            "cover_board": cover,
            "slides": [
                {"step": "STEP 1", "text": "WHEN YOU ATTACK, A FEW PLAYERS [c]STAY BEHIND THE BALL[/c]", "board": s1},
                {"step": "STEP 2", "text": "THEY MARK THE STRIKERS [c]BEFORE[/c] YOU EVEN LOSE IT", "board": s2},
                {"step": "STEP 3", "text": "LOSE THE BALL AND THE COUNTER IS [y]DEAD ON ARRIVAL[/y]", "board": s3},
                {"text": "HOW MANY WOULD YOU [y]LEAVE BEHIND?[/y]"}]}


def systems_poll():
    f433 = [P(1, 34, 100), P(2, 60, 80), P(5, 43, 86), P(4, 25, 86), P(3, 8, 80), P(6, 34, 72), P(8, 47, 60),
            P(10, 21, 60), P(7, 60, 42), P(9, 34, 38), P(11, 8, 42)]
    f352 = [P(1, 34, 100), P(5, 34, 87), P(4, 20, 85), P(6, 48, 85), P(2, 63, 62), P(3, 5, 62), P(8, 46, 66),
            P(14, 34, 72), P(10, 22, 66), P(9, 28, 42), P(11, 41, 42)]
    b433 = {"view": [30, 105], "team_a": f433}
    b352 = {"view": [30, 105], "team_a": f352}
    return {"kind": "tactics", "tag": "YOUR PICK", "headline": "[c]4-3-3[/c] OR [y]3-5-2[/y]? WHICH SYSTEM WOULD YOU PLAY?",
            "cover_board": {"view": [30, 105], "team_a": f433},
            "slides": [
                {"step": "4-3-3", "text": "[c]WIDTH[/c] FROM THE WINGERS, [c]THREE[/c] IN MIDFIELD, ONE STRIKER", "board": b433},
                {"step": "3-5-2", "text": "[c]WING-BACKS[/c] GIVE THE WIDTH, [c]TWO[/c] UP TOP", "board": b352},
                {"text": "4-3-3 OR 3-5-2? [y]COMMENT YOUR PICK[/y]"}]}


# ---------------------------------------------------------------- reels (Remotion tactics)
def mv(*keys):
    return [{"t": t, "x": x, "y": y} for t, x, y in keys]


def pl(n, x, y, *moves):
    d = {"number": n, "start": {"x": x, "y": y}}
    if moves:
        d["moves"] = mv(*moves)
    return d


def pt(x, y):
    return {"x": x, "y": y}


def tactic_base(headline, captions, question, durations=30):
    return {
        "durationInSeconds": durations, "pitchFadeInSeconds": 2.5, "playersEnterAt": 3.3, "playerSizeM": 4.6,
        "tag": "TACTICS, EXPLAINED", "headline": headline,
        "phases": [{"id": "hook", "caption": None, "from": 0, "to": 3},
                   {"id": "p1", "caption": captions[0], "from": 3, "to": 9},
                   {"id": "p2", "caption": captions[1], "from": 9, "to": 15},
                   {"id": "p3", "caption": captions[2], "from": 15, "to": 21},
                   {"id": "p4", "caption": captions[3], "from": 21, "to": 27},
                   {"id": "outro", "caption": None, "from": 27, "to": 30}],
        "outro": {"follow": "FOLLOW", "handle": OUTRO_HANDLE, "question": question, "cta": "SAVE THIS + FOLLOW"},
        "voiceover": {"enabled": True, "volume": 1},
        "music": {"enabled": False, "file": "music.mp3", "volume": 0.3},
    }


def third_man_reel():
    t = tactic_base([[{"text": "THE PASS THAT", "colour": "white"}], [{"text": "BREAKS ANY PRESS", "colour": "cyan"}],
                     [{"text": "THE THIRD MAN", "colour": "yellow"}]],
                    ["THE PRESS", "THE BOUNCE", "THE THIRD MAN", "THE PAYOFF"],
                    "Who's the best third-man runner in the league?")
    t["teams"] = {
        "A": {"name": "Team A", "enterFrom": "bottom", "players": [
            pl(1, 34, 100), pl(2, 60, 80), pl(5, 44, 86), pl(4, 24, 86), pl(3, 8, 80),
            pl(6, 34, 74, (9, 34, 74), (11.5, 32, 72)),
            pl(8, 50, 64, (13, 50, 64), (15, 43, 67), (16.6, 43, 67), (18.6, 45, 60), (21.4, 45, 60), (23, 44, 52)),
            pl(10, 20, 64), pl(11, 8, 52, (19, 8, 52), (22, 12, 38)),
            pl(9, 34, 50, (9.5, 34, 50), (11.6, 36, 61)),
            pl(7, 60, 52, (18.6, 60, 52), (22.4, 55, 31), (24.2, 47, 17), (26, 46, 16))]},
        "B": {"name": "Team B", "enterFrom": "top", "players": [
            pl(1, 34, 4, (24.6, 34, 4), (25.2, 32, 3)),
            pl(2, 58, 44, (21.8, 58, 44), (24, 53, 26)), pl(5, 42, 42), pl(4, 26, 42), pl(3, 10, 44),
            pl(7, 58, 62), pl(8, 42, 60, (6.5, 42, 60), (8.5, 36, 67)), pl(6, 26, 60), pl(11, 10, 62),
            pl(9, 40, 76, (6, 40, 76), (8, 45, 81)), pl(10, 28, 76, (6, 28, 76), (8, 25, 81))]},
    }
    t["ball"] = [{"t": 3.5, **pt(44, 86)}, {"t": 12.0, **pt(44, 86)}, {"t": 12.8, **pt(36, 61)},
                 {"t": 15.6, **pt(36, 61)}, {"t": 16.4, **pt(43, 67)}, {"t": 16.8, **pt(43, 67)},
                 {"t": 18.6, **pt(45, 60)}, {"t": 21.4, **pt(45, 60)}, {"t": 22.4, **pt(55, 31)},
                 {"t": 24.2, **pt(47, 17)}, {"t": 24.5, **pt(47, 17)}, {"t": 25.1, **pt(37, 0.6)}, {"t": 30, **pt(37, 0.6)}]
    t["goal"] = {"t": 25.1, "at": pt(37, 0.6)}
    t["arrows"] = [
        {"kind": "lane", "from": 7, "to": 9.6, "cutAt": 8.4, "points": [pt(44, 86), pt(34, 74)]},
        {"kind": "run", "from": 9.4, "to": 13, "points": [pt(34, 50), pt(32, 56), pt(36, 61)]},
        {"kind": "run", "from": 13, "to": 16.4, "points": [pt(50, 64), pt(48, 68), pt(43, 67)]},
        {"kind": "run", "from": 18.4, "to": 22.4, "points": [pt(60, 52), pt(62, 40), pt(55, 31)]},
    ]
    t["zones"] = [{"from": 15.2, "to": 21, "label": "FACING FORWARD", "points": [pt(37, 62), pt(54, 62), pt(54, 72), pt(37, 72)]}]
    t["highlights"] = [{"from": 11, "to": 15.6, "team": "A", "number": 9}, {"from": 15.6, "to": 21.4, "team": "A", "number": 8},
                       {"from": 22.4, "to": 25.2, "team": "A", "number": 7}]
    t["camera"] = [{"t": 0, "zoom": 1.06, "cx": 34, "cy": 52.5, "tilt": 0}, {"t": 3, "zoom": 1.0, "cx": 34, "cy": 52.5, "tilt": 0},
                   {"t": 6, "zoom": 1.0, "cx": 34, "cy": 52.5, "tilt": 5}, {"t": 8.5, "zoom": 1.4, "cx": 38, "cy": 72, "tilt": 5},
                   {"t": 14.5, "zoom": 1.45, "cx": 40, "cy": 66, "tilt": 5}, {"t": 19, "zoom": 1.3, "cx": 44, "cy": 52, "tilt": 5},
                   {"t": 22.5, "zoom": 1.35, "cx": 46, "cy": 30, "tilt": 5}, {"t": 25.2, "zoom": 1.45, "cx": 42, "cy": 16, "tilt": 5},
                   {"t": 27, "zoom": 1.15, "cx": 36, "cy": 34, "tilt": 4}, {"t": 30, "zoom": 1.08, "cx": 34, "cy": 45, "tilt": 3}]
    vo = {"lines": [
        {"id": "hook", "at": 0.25, "text": "This one pass breaks any press."},
        {"id": "p1", "at": 3.6, "text": "They press high. Two strikers on your centre-backs, and the pass into midfield is covered."},
        {"id": "p2", "at": 9.3, "text": "So the striker drops short, and the centre-back fires it into his feet."},
        {"id": "p3", "at": 15.3, "text": "One touch, laid off to the third man, arriving facing forward."},
        {"id": "p4", "at": 21.3, "text": "The press is beaten. One ball in behind, and you're through."},
        {"id": "outro", "at": 27.05, "text": "Follow, Footy Smart Ten, for more tactics."}]}
    return {"tactic": t, "voiceover": vo, "music": "lofi"}


def overload_reel():
    t = tactic_base([[{"text": "WHY TEAMS CROWD", "colour": "white"}], [{"text": "ONE SIDE", "colour": "cyan"}],
                     [{"text": "ON PURPOSE", "colour": "yellow"}]],
                    ["THE OVERLOAD", "THE SHIFT", "THE SWITCH", "THE PAYOFF"],
                    "Which winger would you want in that one-v-one?")
    t["teams"] = {
        "A": {"name": "Team A", "enterFrom": "bottom", "players": [
            pl(1, 34, 100), pl(4, 26, 64), pl(5, 42, 64), pl(2, 60, 52),
            pl(3, 12, 48, (8.5, 12, 48), (11, 6, 31)),
            pl(6, 34, 52, (5, 34, 52), (8, 30, 48)),
            pl(10, 22, 40, (5, 22, 40), (7, 18, 38)),
            pl(8, 46, 40, (6, 46, 40), (9, 33, 36), (16.5, 33, 36), (19, 40, 32)),
            pl(11, 8, 28, (9, 8, 28), (11, 10, 24)),
            pl(9, 34, 24, (5.5, 34, 24), (8, 24, 22)),
            pl(7, 64, 26, (14.6, 64, 26), (15.6, 64, 24), (21.2, 64, 24), (22.8, 56, 14), (26, 54, 12))]},
        "B": {"name": "Team B", "enterFrom": "top", "players": [
            pl(1, 34, 4, (23, 34, 4), (23.8, 36, 3)),
            pl(3, 12, 18, (6, 12, 18), (9, 8, 20)), pl(4, 26, 16, (6, 26, 16), (9, 18, 17)),
            pl(5, 42, 16, (6, 42, 16), (9, 30, 17)), pl(2, 56, 18, (6.5, 56, 18), (9.5, 46, 19), (16.4, 46, 19), (18.6, 58, 22), (21.6, 58, 22), (22.8, 61, 18)),
            pl(11, 14, 30, (6, 14, 30), (9, 9, 33)), pl(6, 28, 30, (6, 28, 30), (9, 21, 31)),
            pl(8, 40, 30, (6, 40, 30), (9, 30, 30)), pl(7, 54, 30, (6.5, 54, 30), (9.5, 43, 31)),
            pl(9, 28, 44), pl(10, 40, 44)]},
    }
    t["ball"] = [{"t": 3.5, **pt(34, 52)}, {"t": 5.0, **pt(34, 52)}, {"t": 5.6, **pt(22, 40)}, {"t": 7.0, **pt(18, 38)},
                 {"t": 7.6, **pt(8, 28)}, {"t": 10.4, **pt(8, 28)}, {"t": 11.0, **pt(6, 31)}, {"t": 12.0, **pt(6, 31)},
                 {"t": 12.7, **pt(18, 38)}, {"t": 13.4, **pt(18, 38)}, {"t": 14.0, **pt(33, 36)}, {"t": 15.6, **pt(33, 36)},
                 {"t": 16.6, **pt(64, 24)}, {"t": 21.2, **pt(64, 24)}, {"t": 22.8, **pt(56, 14)}, {"t": 23.2, **pt(56, 14)},
                 {"t": 23.8, **pt(37, 0.6)}, {"t": 30, **pt(37, 0.6)}]
    t["goal"] = {"t": 23.8, "at": pt(37, 0.6)}
    t["arrows"] = [
        {"kind": "run", "from": 5.4, "to": 9, "points": [pt(34, 24), pt(28, 25), pt(24, 22)]},
        {"kind": "run", "from": 8.6, "to": 12, "points": [pt(12, 48), pt(6, 42), pt(6, 31)]},
        {"kind": "lane", "from": 14.4, "to": 17, "points": [pt(33, 36), pt(64, 24)]},
        {"kind": "run", "from": 21, "to": 23.4, "points": [pt(64, 24), pt(62, 17), pt(56, 14)]},
    ]
    t["zones"] = [{"from": 6, "to": 14.5, "label": "OVERLOAD", "points": [pt(0, 16), pt(30, 16), pt(30, 42), pt(0, 42)]},
                  {"from": 11.5, "to": 21, "label": "1V1 SPACE", "points": [pt(50, 10), pt(68, 10), pt(68, 34), pt(50, 34)]}]
    t["highlights"] = [{"from": 11.5, "to": 21.2, "team": "A", "number": 7}]
    t["camera"] = [{"t": 0, "zoom": 1.06, "cx": 34, "cy": 52.5, "tilt": 0}, {"t": 3, "zoom": 1.0, "cx": 34, "cy": 52.5, "tilt": 0},
                   {"t": 5.5, "zoom": 1.3, "cx": 28, "cy": 34, "tilt": 5}, {"t": 11, "zoom": 1.3, "cx": 28, "cy": 32, "tilt": 5},
                   {"t": 14, "zoom": 1.2, "cx": 38, "cy": 30, "tilt": 5}, {"t": 17, "zoom": 1.4, "cx": 52, "cy": 24, "tilt": 5},
                   {"t": 21, "zoom": 1.55, "cx": 54, "cy": 18, "tilt": 6}, {"t": 24, "zoom": 1.45, "cx": 46, "cy": 12, "tilt": 5},
                   {"t": 27, "zoom": 1.15, "cx": 36, "cy": 30, "tilt": 4}, {"t": 30, "zoom": 1.08, "cx": 34, "cy": 45, "tilt": 3}]
    vo = {"lines": [
        {"id": "hook", "at": 0.25, "text": "Why top teams crowd one side on purpose."},
        {"id": "p1", "at": 3.6, "text": "Flood the left. Full-back, winger, midfielders, even the striker drifts across."},
        {"id": "p2", "at": 9.3, "text": "The defence has to slide with them, and one man is left alone on the far side."},
        {"id": "p3", "at": 15.3, "text": "Then switch it. One long diagonal to the isolated winger."},
        {"id": "p4", "at": 21.3, "text": "One against one, with space to attack. Cut inside, and finish."},
        {"id": "outro", "at": 27.05, "text": "Follow, Footy Smart Ten, for more tactics."}]}
    return {"tactic": t, "voiceover": vo, "music": "lofi"}


def corners_reel():
    t = tactic_base([[{"text": "HOW ARSENAL", "colour": "white"}], [{"text": "TURNED CORNERS", "colour": "cyan"}],
                     [{"text": "INTO A WEAPON", "colour": "yellow"}]],
                    ["THE SETUP", "THE SCREENS", "THE DELIVERY", "WHY IT WORKS"],
                    "Will Arsenal score from a corner at Newcastle?")
    t["playerSizeM"] = 2.7
    t["teams"] = {
        "A": {"name": "Team A", "enterFrom": "bottom", "players": [
            pl(1, 34, 100), pl(3, 28, 45),
            pl(7, 66, 1.8),
            pl(6, 37.2, 3.0, (9.5, 37.2, 3.0), (11, 36.8, 2.6)),
            pl(4, 31, 3.4, (9.5, 31, 3.4), (11, 31.4, 3.0)),
            pl(5, 42.5, 15.5, (17, 42.5, 15.5), (18.8, 39.6, 9.0)),
            pl(2, 31, 15.5, (17, 31, 15.5), (18.8, 34.4, 10.6)),
            pl(9, 47, 14, (11, 47, 14), (12.6, 44.6, 12.1)),
            pl(8, 25, 12, (11, 25, 12), (12.6, 30.7, 12.4)),
            pl(10, 34, 22), pl(11, 52, 18)]},
        "B": {"name": "Team B", "enterFrom": "top", "players": [
            pl(1, 34, 1.8, (19.6, 34, 1.8), (20.1, 36, 1.4)),
            pl(4, 30, 6.4), pl(5, 34, 6.6), pl(6, 38, 6.4, (18.6, 38, 6.4), (19.4, 38.6, 7.2)), pl(3, 42.2, 6.8),
            pl(2, 40.5, 12.6), pl(8, 28, 13.2), pl(7, 47.6, 10.2),
            pl(10, 34, 18.6), pl(11, 22, 16.5), pl(9, 34, 40)]},
    }
    t["ball"] = [{"t": 3.5, **pt(67, 0.9)}, {"t": 18.4, **pt(67, 0.9)}, {"t": 18.9, **pt(52, 7.5)},
                 {"t": 19.4, **pt(40.2, 8.8)}, {"t": 19.7, **pt(40.2, 8.8)}, {"t": 20.1, **pt(36.4, 0.6)}, {"t": 30, **pt(36.4, 0.6)}]
    t["goal"] = {"t": 20.1, "at": pt(36.4, 0.6)}
    t["arrows"] = [
        {"kind": "run", "from": 10.6, "to": 13.2, "points": [pt(25, 12), pt(28, 11.4), pt(30.4, 12.2)]},
        {"kind": "run", "from": 10.6, "to": 13.2, "points": [pt(47, 14), pt(46, 12.4), pt(44.9, 12.1)]},
        {"kind": "run", "from": 16.4, "to": 19.6, "points": [pt(42.5, 15.5), pt(41.4, 11.6), pt(39.8, 9.2)]},
        {"kind": "run", "from": 16.4, "to": 19.6, "points": [pt(31, 15.5), pt(33, 12.6), pt(34.3, 10.8)]},
        {"kind": "lane", "from": 21.2, "to": 26.6, "points": [pt(66.5, 1.4), pt(52, 11), pt(40, 8.8)]},
    ]
    t["zones"] = [{"from": 9.4, "to": 15, "label": "KEEPER", "points": [pt(29, 0.3), pt(40, 0.3), pt(40, 4.9), pt(29, 4.9)]},
                  {"from": 15.2, "to": 26.6, "label": "FRONT ZONE", "points": [pt(34, 7.6), pt(45, 7.6), pt(45, 11.2), pt(34, 11.2)]}]
    t["highlights"] = [{"from": 9.6, "to": 12.6, "team": "A", "number": 6}, {"from": 12.6, "to": 15.2, "team": "A", "number": 9},
                       {"from": 16.6, "to": 20.2, "team": "A", "number": 5}]
    t["camera"] = [{"t": 0, "zoom": 1.06, "cx": 34, "cy": 52.5, "tilt": 0}, {"t": 3, "zoom": 1.0, "cx": 34, "cy": 52.5, "tilt": 0},
                   {"t": 6.5, "zoom": 2.45, "cx": 46, "cy": 9, "tilt": 5}, {"t": 15, "zoom": 2.45, "cx": 45, "cy": 9, "tilt": 5},
                   {"t": 18.4, "zoom": 2.6, "cx": 44, "cy": 8, "tilt": 5}, {"t": 21, "zoom": 2.55, "cx": 42, "cy": 7.5, "tilt": 5},
                   {"t": 26.6, "zoom": 2.4, "cx": 45, "cy": 8.5, "tilt": 5}, {"t": 28, "zoom": 1.2, "cx": 38, "cy": 30, "tilt": 3},
                   {"t": 30, "zoom": 1.08, "cx": 34, "cy": 45, "tilt": 3}]
    vo = {"lines": [
        {"id": "hook", "at": 0.25, "text": "This is how Arsenal turned corners into a weapon."},
        {"id": "p1", "at": 3.6, "text": "Bodies on the goalkeeper, and runners waiting just outside the six-yard box."},
        {"id": "p2", "at": 9.3, "text": "Then the screens. Teammates step across the markers to free the runners."},
        {"id": "p3", "at": 15.3, "text": "The inswinger comes towards goal, and the runner attacks the front zone."},
        {"id": "p4", "at": 21.3, "text": "The keeper can't come, the markers are stuck, and it's a header from close range."},
        {"id": "outro", "at": 27.05, "text": "Follow, Footy Smart Ten, for more tactics."}]}
    return {"tactic": t, "voiceover": vo, "music": "lofi"}


def build():
    high_press = json.load(open("content/examples/footy-reel-high-press.json"))
    out = []
    out.append(post("2026-11-14", "10:00", "reel", "high-press-trap", "The press that wins the ball in 5 seconds",
        high_press,
        cap("The press that wins the ball in five seconds.",
            ["Show them wide, spring the trap, win it high and score.", "A 4-3-3 pressing trap explained in 30 seconds."],
            "Which side would you spring the trap on, left or right?", ["explainer"], ["#highpress", "#pressing"],
            first_comment="Which team presses like this best? 👇",
            alt="Animated tactics board: a 4-3-3 forces the opponent wide, traps them by the touchline, wins the ball and scores.",
            story="Quiz sticker: 'What triggers the press?' Pass wide / Back pass / Long ball")))
    out.append(post("2026-11-15", "18:00", "carousel", "the-low-block", "The low block: how underdogs shut out big teams",
        low_block(),
        cap("How do underdogs stop the big teams? The low block.",
            ["Two compact banks close to the box, show them wide, then break fast when you win it."],
            "Which team parks the bus best?", ["explainer"], ["#lowblock", "#defending"],
            first_comment="Best low block you've ever seen? 🚌",
            alt="Tactics diagrams showing a deep 4-4-2 low block, defending a cross and breaking on the counter.",
            story="Poll sticker: 'Parking the bus is...' Smart / Boring")))
    out.append(post("2026-11-16", "19:00", "carousel", "inverted-full-back", "The inverted full-back, explained",
        inverted_fullback(),
        cap("Why do full-backs keep ending up in midfield?",
            ["On the ball, the right-back steps inside to make a 3-2 base.",
             "More passing angles against the press, more cover if you lose it, and the winger keeps the width."],
            "Would you play an inverted full-back?", ["explainer"], ["#invertedfullback", "#buildup"],
            first_comment="Name a full-back who does this brilliantly 👇",
            alt="Tactics diagrams showing a right-back moving into midfield to form a 3-2 build-up shape.",
            story="Quiz sticker: 'Inverted full-back moves...' Inside / Outside")))
    out.append(post("2026-11-17", "21:00", "reel", "third-man-run", "The pass that breaks any press: the third man",
        third_man_reel(),
        cap("The pass that breaks any press.",
            ["Striker drops, centre-back plays into his feet, one touch to the third man facing forward, then in behind."],
            "Who's the best third-man runner in the league?", ["explainer"], ["#thirdmanrun", "#playingoutfromtheback"],
            first_comment="Save this for your next training session 📌",
            alt="Animated tactics board showing a third-man combination that breaks a high press and leads to a goal.",
            story="Question sticker: 'Who does this best?'")))
    out.append(post("2026-11-18", "19:00", "carousel", "arsenal-corners", "How Arsenal's corners work, and why they've gone quiet",
        arsenal_corners(),
        cap("Arsenal's corners were feared last season. This season they've gone quiet.",
            ["The routine: crowd the keeper, screen the markers, swing an inswinger into the front zone.",
             "Sky Sports and The Analyst have both looked at why the goals have dried up."],
            "Have teams figured it out, or is it a blip?", ["sky_setpieces", "analyst_corners"], ["#arsenal", "#afc", "#setpieces", "#corners"],
            first_comment="Arsenal fans: worried or not? 👇",
            alt="Tactics diagrams of a corner routine: players crowding the goalkeeper, screens on markers and runners attacking the near post.",
            story="Poll sticker: 'Arsenal score from a corner at Newcastle?' Yes / No",
            check="Open The Analyst link and make sure it is about this season (2026-27). Don't add goal counts: sources disagree on last season's total. The new 'anti-blocking' rule is only reported by fan sites, so don't say it caused this.")))
    out.append(post("2026-11-19", "21:00", "reel", "overload-to-isolate", "Why teams crowd one side on purpose",
        overload_reel(),
        cap("Why do top teams crowd one side on purpose?",
            ["Overload one flank, drag the defence across, then switch it to the winger left one-v-one."],
            "Which winger would you want in that one-v-one?", ["explainer"], ["#overload", "#wingplay"],
            first_comment="Drop the best 1v1 winger in the world right now 👇",
            alt="Animated tactics board: a team overloads the left, the defence shifts, and a long switch finds the isolated right winger.",
            story="Poll sticker: 'Best 1v1 winger?' with two names")))
    out.append(post("2026-11-20", "19:00", "carousel", "rest-defence", "Rest defence: why the best teams never get countered",
        rest_defence(),
        cap("Why do the best teams almost never get countered?",
            ["Rest defence: a few players stay behind the ball and mark the strikers before you lose it."],
            "How many would you leave behind?", ["explainer"], ["#restdefence", "#counterattack"],
            first_comment="2 or 3 at the back when you attack? 👇",
            alt="Tactics diagrams showing a team attacking while three players stay behind the ball to stop counter-attacks.",
            story="Slider sticker: 'How many stay back?'")))
    out.append(post("2026-11-21", "10:00", "reel", "arsenal-corner-routine", "How Arsenal turned corners into a weapon",
        corners_reel(),
        cap("How Arsenal turned corners into a weapon.",
            ["Crowd the keeper, screen the markers, inswinger into the front zone, header from close range.",
             "Newcastle v Arsenal kicks off at 17:30 today."],
            "Will Arsenal score from a corner at Newcastle?", ["sky_setpieces", "fixture"], ["#arsenal", "#afc", "#nufc", "#setpieces"],
            first_comment="Prediction for today? 👇",
            alt="Animated tactics board of a corner routine with screens and a near-post header.",
            story="Poll sticker: 'Corner goal today?' Yes / No",
            check="Kick-off was reported as 17:30 GMT. Check the time before posting.")))
    out.append(post("2026-11-22", "18:00", "carousel", "433-or-352", "4-3-3 or 3-5-2? Which system would you play?",
        systems_poll(),
        cap("Two systems. One choice.",
            ["4-3-3: width from the wingers and three in midfield.", "3-5-2: wing-backs give the width and two strikers up top."],
            "Comment your pick 👇", ["explainer"], ["#formation", "#433", "#352"],
            first_comment="And why? Best answer gets pinned 📌",
            alt="Two tactics boards comparing a 4-3-3 and a 3-5-2 formation.",
            story="Poll sticker: 4-3-3 / 3-5-2")))
    return out
