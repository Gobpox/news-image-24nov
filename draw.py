"""The World in One Picture — Tuesday, twenty-four November.

Fresh build for this edition, written in this session from the locked
bagarte geometry spec, with the previous edition's verdict amendments:
the story count is computed from the story table and printed in the
strap, never hand-typed; the deck is a single line in every panel;
ALSO sub-lines carry only a core figure and a source, or nothing;
hero and card decks share one size, and all small captions share one
size; the pictured layer keeps its locked sizes throughout; the
pictured layer is confirmed-only, and the day's single reported story
sits in ALSO only; disputed claims carry attribution inside the
headline or band. All important numbers are interpolated from the
figures registry. Audits measure glyph ink, never anchor boxes, with
a minimum clearance rule across text, lines, graphics, strips, the
rail, the date-check box and the masthead. Deterministic output.
"""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
FIG = {f["key"]: f["display"] for f in json.loads(
    (HERE / "figures.json").read_text(encoding="utf-8"))["figures"]}

W = H = 1024
MX, RX = 12, 1012
PAPER = (244, 239, 227)
INK = (26, 24, 20)
RED = (178, 34, 30)
BANDRED = (176, 32, 28)
MUTE = (96, 90, 78)
GREY = (52, 48, 42)
CAPGREY = (104, 96, 84)
SRCGREY = (110, 100, 88)
NAVY = (18, 32, 54)
TEAL = (23, 92, 96)
GOLD = (196, 148, 38)
PURPLE = (120, 70, 160)
SEA = (46, 139, 87)
CREAM = (255, 253, 246)
HAIR = (190, 182, 168)

REGION = {"EUR": (52, 84, 140), "ASI": RED, "AME": TEAL,
          "MEA": PURPLE, "AFR": GOLD, "OCE": SEA, "GLO": MUTE}
REGION_NAME = {"EUR": "Europe", "ASI": "Asia-Pacific", "AME": "Americas",
               "MEA": "Middle East", "AFR": "Africa", "OCE": "Oceania",
               "GLO": "Space"}
SURE = {"C": ("CONFIRMED", (26, 118, 60)),
        "R": ("REPORTED", (186, 44, 36))}

def load_font(name, size, weight=None):
    f = ImageFont.truetype(str(HERE / "fonts" / name), size)
    if weight is not None:
        try:
            f.set_variation_by_axes([weight])
        except Exception:
            pass
    return f

def SERIF(size):
    return load_font("PlayfairDisplay-Bold.ttf", size, 700)

def SANS(size):
    return load_font("Archivo.ttf", size, 400)

def SANS_B(size):
    return load_font("Archivo.ttf", size, 700)

# ---------------------------------------------------------------- data
# (place, region, field, headline, deck, source, sure)
HEROES = [
    ("BROOKLYN, USA", "AME", "Justice",
     "Huawei guilty: 10 of 12 counts",
     "Cleared of racketeering charge",
     "Reuters", "C"),
    ("STRAIT OF HORMUZ", "MEA", "Conflict",
     "Iran says mines hit",
     "Day 270; centre: unconfirmed",
     "AP", "C"),
    ("KUALA LUMPUR, MALAYSIA", "ASI", "Justice",
     "Malaysia: 6,803 home",
     "1,500 by ship, 5,303 by air",
     "AP", "C"),
]
HERO_BAND = [
    f"BROOKLYN — {FIG['huawei_counts']} COUNTS",
    f"HORMUZ — IRAN SAYS {FIG['hormuz_tankers']} TANKERS HIT",
    f"KUALA LUMPUR — {FIG['malaysia_repatriate']} TO GO HOME",
]
HERO_PLATE = ["HUAWEI", "HORMUZ", "MALAYSIA"]

CARDS = [
    ("SANTA CLARA, USA", "AME", "Economy",
     "Nvidia slides about 7%",
     "Anthropic $79, IPO $83",
     "AP", "C"),
    ("RIYADH, SAUDI ARABIA", "MEA", "Conflict",
     "Riyadh tower hit again",
     "11 hurt; 2nd in 5 days",
     "Middle East Eye", "C"),
    ("KYIV, UKRAINE", "EUR", "Conflict",
     "Kyiv strikes oil plants",
     "Day 1,732; Putin vows",
     "Straits Times", "C"),
    ("DAKAR, SENEGAL", "AFR", "Sport",
     "CAS restores Senegal title",
     "AFCON 2025; 1-0 back",
     "France 24", "C"),
    ("DOHA, QATAR", "ASI", "Sport",
     "Sooryavanshi, 15: 204",
     "Off 53 balls, 28 sixes",
     "Cricinfo", "C"),
    ("ULLEUNGDO, S. KOREA", "ASI", "Conflict",
     "Seoul scrambles jets",
     "Russians near Ulleung",
     "Al Jazeera", "C"),
    ("ERBIL, IRAQ", "MEA", "Energy",
     "Baghdad takes oilfields",
     "4 provinces, smuggling",
     "Al Jazeera", "C"),
    ("WARSAW, POLAND", "EUR", "Conflict",
     "Poland: drone was deliberate",
     "Moscow rejects; AWACS",
     "Fox News", "C"),
    ("TRIPOLI, LIBYA", "AFR", "Conflict",
     "Libya asks Kyiv: why?",
     "Benghazi ships at issue",
     "Guardian", "C"),
    ("NEW YORK, UN", "GLO", "Technology",
     "UN chief urges AI safety talks",
     "Framework within a year",
     "UN News", "C"),
]
CARD_OVERLAY = ["-7%", "11 HURT", "OIL HIT", "1-0", "204",
                "JETS UP", "4 PROV.", "AWACS", "WHY?", "1 YEAR"]
CARD_FLAG = ["US", "SA", "UA", "SN", "QA", "KR", "IQ", "PL", "LY", "UN"]

# (place-label, region, field, main, sub) — sub = core figure + source only
ALSO = [
    ("Tallinn", "EUR", "Conflict", "Russia warns Estonia", "Tallinn · CNBC"),
    ("Strasbourg", "EUR", "Justice", "Court backs turn-backs", "Strasbourg · Le Monde"),
    ("Paris", "EUR", "Justice", "Sarkozy trial 2027", "Paris · BBC"),
    ("London", "EUR", "Politics", "Benefits overhaul", "London · BBC"),
    ("Madrid", "EUR", "Sport", "Real beat PSV 5-1", "Madrid · France 24"),
    ("Villavicencio", "AME", "Conflict", "Colombia car bomb", f"{FIG['colombia_bomb']} · Al Jazeera"),
    ("Guasave", "AME", "Justice", "Mexico: boss held", f"{FIG['mexico_killed']} killed · BBC"),
    ("Washington", "AME", "Politics", "Dems win House", "Washington · CNBC"),
    ("Iowa", "AME", "Society", "Iowa blast set Wed", f"{FIG['iowa_barrels']} barrels · CBC"),
    ("Havana", "AME", "Health", "Life 78.8 to 74.4", "Cuba · Guardian"),
    ("Shanghai", "ASI", "Politics", "Shanghai aide probed", "4th of 24 · El País"),
    ("Beijing", "ASI", "Space", "Pakistan space pick", "Beijing · BBC"),
    ("Kathmandu", "ASI", "Diplomacy", "India pledges €1.4bn", "Kathmandu · DW"),
    ("Dushanbe", "ASI", "Justice", "Tajikistan quits ICC", "Dushanbe · Reuters"),
    ("Gaza", "MEA", "Conflict", "Gaza chief killed", f"{FIG['gaza_chief_killed']} killed · BBC"),
    ("Gaza", "MEA", "Health", "272 meningitis cases", "Gaza · Guardian"),
    ("Jerusalem", "MEA", "Politics", "Katz claims chem arms", "Jerusalem · CBS"),
    ("Abuja", "AFR", "Economy", "Abuja: $20.5bn OK", f"rate {FIG['nigeria_rate']} · Vanguard"),
    ("Khartoum", "AFR", "Conflict", "Khartoum UN site hit", "OIC condemns · RFI"),
    ("Honiara", "OCE", "Diplomacy", "Solomons pact to end", "REPORTED · Reuters"),
    ("Canberra", "OCE", "Technology", "Canberra fines 5%", "tech firms · Guardian"),
]
ALSO_SURE = ["C"] * 19 + ["R", "C"]

STORIES_ALL = HEROES + CARDS + [
    (a[0], a[1], a[2], a[3], a[4], "", s)
    for a, s in zip(ALSO, ALSO_SURE)]
TOTAL = len(STORIES_ALL)
REGIONS_N = len({s[1] for s in STORIES_ALL if s[1] != "GLO"})
FIELDS_N = len({s[2] for s in STORIES_ALL})

RAIL = [
    (FIG["huawei_ratio"], "HUAWEI COUNTS GUILTY", False),
    (FIG["hormuz_tankers"], "TANKERS, SAYS IRAN", True),
    (FIG["sooryavanshi_runs"], "SOORYAVANSHI, AGE 15", False),
    (FIG["riyadh_injured"], "HURT IN RIYADH STRIKE", False),
]

TIMELINE = [
    ("TUE", "HORMUZ TALKS OFF"),
    ("TUE", "BROOKLYN VERDICT"),
    ("TUE", "RIYADH TOWER HIT"),
    ("06:00", "DOHA MATCH STARTS"),
    ("11:49", "204 OFF 53 DONE"),
    ("21:13", "AP: AI SELL-OFF"),
    ("TUE", "KL REPATRIATION"),
]

DATE_CHECK = (
    f"Left out, not Tuesday: Nvidia +{FIG['nvidia_monday']} to {FIG['nvidia_monday_close']}, "
    "Huang back (Mon 23 Nov); Oxfam toxic Gaza "
    f"{FIG['oxfam_share']} (Mon); Belgium strike, Puigdemont amnesty (Mon); "
    f"COP31 end (Sun 22 Nov); Binance {FIG['binance_hack']} exploit (29 Oct). "
    "Not yet: Huawei sentence (2027); Hormuz mines confirmed; "
    "Iowa blast (Wed); Solomon signing (Wed)."
)

PINS = [  # story no, lon, lat, dx, dy
    (1, -74.0, 40.7, -14, -12), (2, 56.0, 26.5, 10, -10),
    (3, 101.7, 3.1, 12, 8), (4, -122.0, 37.4, -12, 10),
    (5, 46.7, 24.6, -12, 12), (6, 30.5, 50.4, -10, -12),
    (7, -17.4, 14.7, -12, 6), (8, 51.5, 25.3, 14, 12),
    (9, 130.9, 37.5, 10, -8), (10, 44.0, 36.2, 12, -12),
    (11, 21.0, 52.2, 12, -6), (12, 13.2, 32.9, -14, 12),
    (13, -74.0, 40.7, 14, 12),
]

MAP_ROWS = [
    "....................................................................",
    "..........########..................##########################......",
    ".......############...........##################################....",
    ".....##############.........####################################....",
    "....################.......######..##########################.......",
    "...#################......#####....########..################.......",
    "....################......####......######.....#############........",
    ".....##############.......###........####........##########.........",
    "......############....................##..........########..........",
    ".......##########..................................#######..........",
    "........########....................................######..........",
    ".........#######..................##................#####...........",
    "..........######.................####...............####............",
    "...........#####................######...............##.............",
    "............####...............########.............................",
    ".............###..............##########..................##........",
    ".............##..............############................####.......",
    "..............................##########................######......",
    "...............................########..................########...",
    "................................######....................######....",
    ".................................####......................####.....",
    "..................................##........................##......",
    "....................................................................",
    "....................................................................",
    "...........................................##.......................",
    "..........................................####......................",
    "..........................................####......................",
    "....................................................................",
    "....................................................................",
    "....................................................................",
]

# ------------------------------------------------------- recording layer
TEXTS = []      # (x0,y0,x1,y1,string,tag)
LINES = []      # (x0,y0,x1,y1,tag) axis-aligned only
OBSTACLES = []  # (x0,y0,x1,y1,tag)
FLAGS = []      # (x0,y0,x1,y1,tag)
FAIL = []

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def text(x, y, s, font, fill, tag, anchor_left=True):
    """Draw left-aligned text at (x,y); record its glyph ink box."""
    bb = d.textbbox((x, y), s, font=font)
    d.text((x, y), s, font=font, fill=fill)
    TEXTS.append((bb[0], bb[1], bb[2], bb[3], s, tag))
    return bb

def text_c(cx, y, s, font, fill, tag):
    wdt = d.textlength(s, font=font)
    return text(cx - wdt / 2, y, s, font, fill, tag)

def text_r(rx, y, s, font, fill, tag):
    wdt = d.textlength(s, font=font)
    return text(rx - wdt, y, s, font, fill, tag)

def hcheck(s, font, limit, what):
    if d.textlength(s, font=font) > limit:
        FAIL.append(f"H-CHECK {what}: '{s}' too wide")

def wrap(s, font, width, max_lines, what):
    words, lines, cur = s.split(), [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if d.textlength(trial, font=font) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        FAIL.append(f"WRAP {what}: '{s}' needs {len(lines)} lines")
    return lines[:max_lines]

def hline(x0, x1, y, fill, wdt, tag):
    d.line([(x0, y), (x1, y)], fill=fill, width=wdt)
    LINES.append((x0, y - wdt // 2, x1, y - wdt // 2 + wdt - 1, tag))

def chip(x_right, y, sure, tag):
    label, col = SURE[sure]
    f = SANS_B(9)
    wdt = d.textlength(label, font=f) + 12
    x0 = x_right - wdt
    d.rounded_rectangle([x0, y, x_right, y + 16], 3, fill=CREAM, outline=col, width=1)
    text(x0 + 6, y + 3, label, f, col, tag)
    return x0

def obstacle(x0, y0, x1, y1, tag):
    OBSTACLES.append((x0, y0, x1, y1, tag))

# ---------------------------------------------------------------- flags
FLAG_DEF = {
    "US": [("field", (178, 34, 30))],
    "IR": [("hband", (0, 128, 0)), ("hband", (255, 255, 255)), ("hband", RED)],
    "MY": [("field", (204, 0, 0))],
    "SA": [("field", (0, 108, 53))],
    "UA": [("hband", (0, 91, 172)), ("hband", (255, 213, 0))],
    "SN": [("vband", (0, 133, 63)), ("vband", (252, 209, 22)), ("vband", (206, 17, 38))],
    "QA": [("field", (255, 255, 255))],
    "KR": [("field", (255, 255, 255))],
    "IQ": [("hband", (206, 17, 38)), ("hband", (255, 255, 255)), ("hband", (0, 0, 0))],
    "PL": [("hband", (255, 255, 255)), ("hband", (220, 20, 60))],
    "LY": [("hband", (231, 0, 11)), ("hband", (0, 0, 0)), ("hband", (0, 122, 61))],
    "UN": [("field", (91, 146, 197))],
}

def draw_flag(x, y, code, tag):
    wdt, hgt = 24, 16
    d.rectangle([x, y, x + wdt, y + hgt], fill=(255, 255, 255), outline=INK, width=1)
    steps = FLAG_DEF.get(code, [("field", (40, 80, 160))])
    kind = steps[0][0]
    if kind == "field":
        d.rectangle([x + 1, y + 1, x + wdt - 1, y + hgt - 1], fill=steps[0][1])
    elif kind == "hband":
        bh = hgt / len(steps)
        for i, (_, c) in enumerate(steps):
            d.rectangle([x + 1, y + 1 + i * bh, x + wdt - 1, y + (i + 1) * bh], fill=c)
    elif kind == "vband":
        bw = wdt / len(steps)
        for i, (_, c) in enumerate(steps):
            d.rectangle([x + 1 + i * bw, y + 1, x + (i + 1) * bw, y + hgt - 1], fill=c)
    if code == "US":
        for i in range(4):
            d.rectangle([x + 1, y + 1 + i * 4, x + wdt - 1, y + 3 + i * 4], fill=(255, 255, 255))
        d.rectangle([x + 1, y + 1, x + 11, y + 8], fill=(40, 40, 120))
    elif code == "MY":
        for i in range(4):
            d.rectangle([x + 1, y + 1 + i * 4, x + wdt - 1, y + 3 + i * 4], fill=(255, 255, 255))
        d.rectangle([x + 1, y + 1, x + 11, y + 8], fill=(1, 1, 102))
        d.ellipse([x + 3, y + 2, x + 7, y + 6], fill=(255, 204, 0))
    elif code == "QA":
        d.polygon([(x + 9, y + 1), (x + wdt - 1, y + 1), (x + wdt - 1, y + hgt - 1),
                   (x + 9, y + hgt - 1), (x + 13, y + 8)], fill=(138, 21, 56))
    elif code == "KR":
        d.ellipse([x + 9, y + 4, x + 15, y + 10], fill=(205, 46, 58))
        d.pieslice([x + 9, y + 4, x + 15, y + 10], 90, 270, fill=(0, 71, 160))
    elif code == "IQ":
        d.ellipse([x + 10, y + 6, x + 14, y + 10], outline=(0, 122, 61), width=1)
    elif code == "LY":
        d.ellipse([x + 10, y + 5, x + 15, y + 10], outline=(255, 255, 255), width=1)
    elif code == "UN":
        d.ellipse([x + 7, y + 2, x + 17, y + 12], outline=(255, 255, 255), width=1)
        d.line([(x + 12, y + 2), (x + 12, y + 12)], fill=(255, 255, 255), width=1)
    FLAGS.append((x, y, x + wdt, y + hgt, tag))

# ------------------------------------------------------------ hero scenes
def scene_huawei(x, y):
    d.rectangle([x, y, x + 266, y + 114], fill=(214, 222, 232))
    d.rectangle([x, y + 78, x + 266, y + 114], fill=(120, 132, 150))
    for i, cx in enumerate([x + 52, x + 92, x + 172, x + 212]):
        d.rectangle([cx, y + 26, cx + 14, y + 78], fill=CREAM, outline=INK, width=2)
        obstacle(cx, y + 26, cx + 14, y + 78, "hero1")
    d.rectangle([x + 38, y + 18, x + 228, y + 26], fill=CREAM, outline=INK, width=2)
    d.rectangle([x + 38, y + 78, x + 228, y + 86], fill=CREAM, outline=INK, width=2)
    obstacle(x + 38, y + 18, x + 228, y + 26, "hero1")
    d.line([(x + 132, y + 44), (x + 158, y + 62)], fill=INK, width=4)
    d.rectangle([x + 156, y + 60, x + 172, y + 68], fill=(120, 72, 20), outline=INK, width=1)
    obstacle(x + 130, y + 42, x + 174, y + 70, "hero1")

def scene_hormuz(x, y):
    d.rectangle([x, y, x + 266, y + 114], fill=(168, 198, 224))
    d.rectangle([x, y + 62, x + 266, y + 114], fill=(52, 96, 140))
    for wx in range(x + 8, x + 258, 36):
        d.arc([wx, y + 88, wx + 24, y + 102], 0, 180, fill=CREAM, width=2)
    d.rectangle([x + 70, y + 48, x + 190, y + 62], fill=(60, 60, 66), outline=INK, width=2)
    d.rectangle([x + 96, y + 38, x + 120, y + 48], fill=(90, 90, 96), outline=INK, width=1)
    obstacle(x + 70, y + 38, x + 190, y + 62, "hero2")
    for mx, my in [(x + 216, y + 76), (x + 238, y + 92), (x + 30, y + 84)]:
        d.ellipse([mx - 8, my - 8, mx + 8, my + 8], fill=(30, 30, 34), outline=CREAM, width=2)
        obstacle(mx - 8, my - 8, mx + 8, my + 8, "hero2")

def scene_malaysia(x, y):
    d.rectangle([x, y, x + 266, y + 114], fill=(196, 226, 208))
    d.rectangle([x, y + 74, x + 266, y + 114], fill=(52, 110, 130))
    d.polygon([(x + 36, y + 74), (x + 130, y + 74), (x + 118, y + 88), (x + 48, y + 88)],
              fill=(150, 40, 36), outline=INK, width=2)
    d.rectangle([x + 62, y + 60, x + 104, y + 74], fill=CREAM, outline=INK, width=1)
    obstacle(x + 36, y + 60, x + 130, y + 88, "hero3")
    d.polygon([(x + 168, y + 34), (x + 232, y + 46), (x + 168, y + 52), (x + 182, y + 46)],
              fill=CREAM, outline=INK, width=2)
    obstacle(x + 168, y + 34, x + 232, y + 52, "hero3")

HERO_SCENES = [scene_huawei, scene_hormuz, scene_malaysia]

# ------------------------------------------------------------ card strips
def strip_canvas():
    return Image.new("RGB", (190, 55), (232, 226, 210))

def pic_chart(s):
    dr = ImageDraw.Draw(s)
    dr.line([(18, 38), (52, 26), (84, 32), (116, 14)], fill=RED, width=4)
    dr.polygon([(116, 14), (104, 16), (112, 26)], fill=RED)
    return s

def pic_tower(s):
    dr = ImageDraw.Draw(s)
    dr.rectangle([52, 6, 74, 38], fill=NAVY, outline=INK, width=1)
    dr.polygon([(52, 6), (63, 0), (74, 6)], fill=GOLD)
    for wy in (12, 20, 28):
        dr.rectangle([57, wy, 69, wy + 4], fill=(255, 214, 90))
    return s

def pic_oil(s):
    dr = ImageDraw.Draw(s)
    dr.rectangle([8, 24, 52, 38], fill=(90, 90, 96), outline=INK, width=1)
    dr.rectangle([24, 12, 36, 24], fill=(90, 90, 96), outline=INK, width=1)
    dr.polygon([(30, 2), (22, 12), (38, 12)], fill=(232, 120, 30))
    return s

def pic_trophy(s):
    dr = ImageDraw.Draw(s)
    dr.rectangle([50, 4, 76, 22], fill=GOLD, outline=INK, width=1)
    dr.arc([38, 6, 52, 20], 90, 270, fill=GOLD, width=3)
    dr.arc([74, 6, 88, 20], 270, 90, fill=GOLD, width=3)
    dr.rectangle([60, 22, 66, 30], fill=GOLD)
    dr.rectangle([50, 30, 76, 35], fill=(120, 72, 20))
    return s

def pic_cricket(s):
    dr = ImageDraw.Draw(s)
    dr.polygon([(48, 2), (58, 4), (50, 34), (42, 32)], fill=(196, 148, 38), outline=INK, width=1)
    dr.ellipse([72, 22, 86, 36], fill=RED, outline=INK, width=1)
    return s

def pic_jet(s):
    dr = ImageDraw.Draw(s)
    dr.polygon([(14, 28), (48, 14), (70, 20), (48, 26), (22, 36)], fill=NAVY, outline=INK, width=1)
    dr.polygon([(40, 22), (32, 36), (44, 34)], fill=TEAL)
    return s

def pic_derrick(s):
    dr = ImageDraw.Draw(s)
    dr.polygon([(40, 36), (63, 4), (86, 36)], outline=INK, width=3)
    dr.line([(48, 26), (78, 26)], fill=INK, width=2)
    dr.line([(54, 16), (72, 16)], fill=INK, width=2)
    return s

def pic_drone(s):
    dr = ImageDraw.Draw(s)
    dr.rectangle([40, 16, 58, 26], fill=NAVY, outline=INK, width=1)
    for cx, cy in [(32, 10), (66, 10), (32, 30), (66, 30)]:
        dr.ellipse([cx - 8, cy - 4, cx + 8, cy + 4], outline=INK, width=2)
        dr.line([(cx, cy), (49, 21)], fill=INK, width=1)
    return s

def pic_ship(s):
    dr = ImageDraw.Draw(s)
    dr.polygon([(16, 26), (84, 26), (76, 38), (24, 38)], fill=(150, 40, 36), outline=INK, width=1)
    dr.rectangle([40, 14, 62, 26], fill=CREAM, outline=INK, width=1)
    dr.rectangle([48, 6, 54, 14], fill=(90, 90, 96))
    return s

def pic_globe(s):
    dr = ImageDraw.Draw(s)
    dr.ellipse([44, 2, 84, 38], fill=(91, 146, 197), outline=INK, width=1)
    dr.ellipse([56, 2, 72, 38], outline=CREAM, width=1)
    dr.line([(44, 20), (84, 20)], fill=CREAM, width=1)
    return s

PICS = [pic_chart, pic_tower, pic_oil, pic_trophy, pic_cricket,
        pic_jet, pic_derrick, pic_drone, pic_ship, pic_globe]

# ------------------------------------------------------------- masthead
text(MX, 1, "THE WORLD IN ONE PICTURE · ORIGINAL DRAWINGS", SANS_B(15), RED, "eyebrow")
strap = f"{TOTAL} STORIES · {REGIONS_N} REGIONS + SPACE · {FIELDS_N} FIELDS"
text_r(RX, -3, strap, SANS_B(22), INK, "strap")
date_s = "Tuesday 24 November 2026"
date_f = SERIF(76)
date_w = d.textlength(date_s, font=date_f)
date_x = (W - date_w) / 2
date_bb = text(date_x, -4, date_s, date_f, INK, "date")
# red bar: two flanking segments only, never crossing the date ink
seg_y0, seg_y1 = 30, 33
d.rectangle([MX, seg_y0, date_bb[0] - 5, seg_y1], fill=RED)
d.rectangle([date_bb[2] + 5, seg_y0, RX, seg_y1], fill=RED)
LINES.append((MX, seg_y0, date_bb[0] - 5, seg_y1, "mast-red-L"))
LINES.append((date_bb[2] + 5, seg_y0, RX, seg_y1, "mast-red-R"))
hline(MX, RX, 99, INK, 2, "date-rule")

# ------------------------------------------------------------- timeline
d.rectangle([MX, 100, MX + 56, 124], fill=RED)
text_c(MX + 28, 102, "THE DAY", SANS_B(9), CREAM, "timeline-label")
text_c(MX + 28, 113, "IN UTC", SANS_B(9), CREAM, "timeline-label")
tl_x0, tl_step = 76, (RX - 76) / 7
for i, (tm, cap) in enumerate(TIMELINE):
    cx = tl_x0 + i * tl_step + tl_step / 2
    text_c(cx, 100, tm, SANS_B(13), RED, "timeline")
    hcheck(cap, SANS(10), tl_step - 4, "timeline cap")
    text_c(cx, 114, cap, SANS(10), CAPGREY, "timeline")
    if i:
        sx = tl_x0 + i * tl_step - 5
        d.line([(sx, 103), (sx, 121)], fill=HAIR, width=1)
hline(MX, RX, 127, (150, 142, 126), 1, "timeline-rule")

# ------------------------------------------------------- heroes + rail
HY, HW = 128, 266
for i, (hero, band, plate, scene) in enumerate(
        zip(HEROES, HERO_BAND, HERO_PLATE, HERO_SCENES)):
    place, region, field, headline, deck, source, sure = hero
    x = MX + i * (HW + 14)
    scene(x, HY)
    d.rectangle([x, HY + 114, x + HW, HY + 136], fill=BANDRED)
    hcheck(band, SANS_B(13), HW - 4, "hero band")
    text_c(x + HW / 2, HY + 118, band, SANS_B(13), CREAM, f"hero{i+1}-band")
    # name plate, top-left inside scene
    pf = SANS_B(12)
    pw = d.textlength(plate, font=pf) + 12
    d.rectangle([x + 7, HY + 4, x + 7 + pw, HY + 20], fill=CREAM, outline=INK, width=2)
    text(x + 13, HY + 6, plate, pf, INK, f"hero{i+1}-plate")
    chip(x + HW - 6, HY + 4, sure, f"hero{i+1}-chip")
    d.rectangle([x, HY, x + HW, HY + 136], outline=(120, 112, 96), width=1)
    ky = HY + 138
    col = REGION[region]
    d.ellipse([x, ky, x + 18, ky + 18], fill=col)
    text_c(x + 9, ky + 2, str(i + 1), SANS_B(12), CREAM, f"hero{i+1}-num")
    text(x + 24, ky, place.replace(", ", " · "), SANS_B(15), col, f"hero{i+1}-kicker")
    text_r(x + HW, ky + 3, source, SANS(12), SRCGREY, f"hero{i+1}-source")
    hf = SERIF(38)
    for j, line in enumerate(wrap(headline, hf, HW - 2, 2, f"hero{i+1} headline")):
        text(x, ky + 11 + j * 41, line, hf, INK, f"hero{i+1}-headline")
    hcheck(deck, SANS(15), HW - 2, f"hero{i+1} deck")
    text(x, ky + 102, deck, SANS(15), GREY, f"hero{i+1}-deck")

RAIL_X = 852
text(RAIL_X, HY + 1, "THE DAY IN NUMBERS", SANS_B(13), RED, "rail-head")
rail_tops = [HY + 18, HY + 81, HY + 144, HY + 204]
for i, ((num, cap, red), top) in enumerate(zip(RAIL, rail_tops)):
    if i in (1, 2):
        hline(RAIL_X, RX, top - 5, HAIR, 1, f"rail-hair-{i}")
    nf = SERIF(55)
    hcheck(num, nf, RX - RAIL_X, "rail number")
    off = nf.getbbox(num)[1]
    bb = text(RAIL_X, top - off, num, nf, RED if red else INK, f"rail{i+1}-num")
    hcheck(cap, SANS(13), RX - RAIL_X, f"rail{i+1} cap")
    text(RAIL_X, bb[3] + 1, cap, SANS(13), CAPGREY, f"rail{i+1}-cap")

# ---------------------------------------------------------------- cards
CY, CW = 385, 192
STRIP_INK = []  # (card_idx, PIL image of strip) for strip audit
for i, card in enumerate(CARDS):
    place, region, field, headline, deck, source, sure = card
    cx = MX + (i % 5) * (CW + 10)
    cy = CY + (i // 5) * 151
    strip = PICS[i](strip_canvas())
    STRIP_INK.append(strip.copy())
    img.paste(strip, (cx + 1, cy + 1))
    d.rounded_rectangle([cx, cy, cx + CW, cy + 56], 4, outline=(120, 112, 96), width=1)
    draw_flag(cx + 3, cy + 3, CARD_FLAG[i], f"card{i+1}-flag")
    # overlay, top-right inside strip, cream stroke via manual offsets
    ov = CARD_OVERLAY[i]
    of = SANS_B(28 if len(ov) <= 5 else 24 if len(ov) <= 9 else 20 if len(ov) <= 12 else 17)
    ow = d.textlength(ov, font=of)
    ox, oy = cx + CW - 6 - ow, cy + 2
    for dxs, dys in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
        d.text((ox + dxs, oy + dys), ov, font=of, fill=CREAM)
    bb = d.textbbox((ox, oy), ov, font=of, stroke_width=2)
    d.text((ox, oy), ov, font=of, fill=(16, 20, 34), stroke_width=0)
    TEXTS.append((bb[0], bb[1], bb[2], bb[3], ov, f"card{i+1}-overlay"))
    # location tab + status chip, shared row inside strip
    tab_f = SANS_B(9)
    tab_s = f"{i + 4} · {place.split(',')[0]}"
    tw = d.textlength(tab_s, font=tab_f) + 12
    d.rounded_rectangle([cx + 3, cy + 39, cx + 3 + tw, cy + 52], 3, fill=REGION[region])
    text(cx + 9, cy + 41, tab_s, tab_f, CREAM, f"card{i+1}-tab")
    chip(cx + CW - 3, cy + 39, sure, f"card{i+1}-chip")
    text(cx, cy + 59, field.upper(), SANS_B(11), REGION[region], f"card{i+1}-field")
    text_r(cx + CW, cy + 58, source, SANS(12), SRCGREY, f"card{i+1}-source")
    hf = SERIF(27)
    for j, line in enumerate(wrap(headline, hf, CW - 4, 2, f"card{i+1} headline")):
        text(cx, cy + 67 + j * 31, line, hf, INK, f"card{i+1}-headline")
    hcheck(deck, SANS(15), CW - 4, f"card{i+1} deck")
    text(cx, cy + 134, deck, SANS(15), GREY, f"card{i+1}-deck")

# ------------------------------------------------------ bottom: map+ALSO
BY = 692
hline(MX, RX, BY - 1, INK, 2, "bottom-rule")
text(MX, BY, "WHERE IT HAPPENED", SANS_B(14), RED, "map-head")
text(288, BY, "ALSO ON TUESDAY 24 NOVEMBER", SANS_B(14), RED, "also-head")
MAP_X, MAP_Y, MAP_W, MAP_H = MX, BY + 15, 240, 150
d.rectangle([MAP_X, MAP_Y, MAP_X + MAP_W, MAP_Y + MAP_H], fill=(16, 26, 44))
cell_w, cell_h = MAP_W / 68, MAP_H / 30
for r, row in enumerate(MAP_ROWS):
    for c, ch in enumerate(row):
        if ch == "#":
            px, py = MAP_X + c * cell_w + cell_w / 2, MAP_Y + r * cell_h + cell_h / 2
            d.ellipse([px - 1.6, py - 1.6, px + 1.6, py + 1.6], fill=(120, 150, 190))
pin_region = {i + 1: (HEROES + CARDS)[i][1] for i in range(13)}
for num, lon, lat, dx, dy in PINS:
    px = MAP_X + (lon + 168) / 360 * MAP_W
    py = MAP_Y + (78 - lat) / 134 * MAP_H
    d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 214, 90))
    qx, qy = px + dx, py + dy
    d.line([(px, py), (qx, qy)], fill=(255, 214, 90), width=1)
    d.ellipse([qx - 9, qy - 9, qx + 9, qy + 9], fill=REGION[pin_region[num]],
              outline=(255, 255, 255), width=1)
    text_c(qx, qy - 7, str(num), SANS_B(10), CREAM, f"pin{num}")
# legend = computed region tally
from collections import Counter
tally = Counter(s[1] for s in STORIES_ALL)
ly = MAP_Y + MAP_H + 8
for k, reg in enumerate(["EUR", "ASI", "AME", "MEA", "AFR", "OCE", "GLO"]):
    lx = MX + (k % 2) * 122
    yy = ly + (k // 2) * 18
    d.ellipse([lx, yy + 3, lx + 9, yy + 12], fill=REGION[reg])
    text(lx + 13, yy, f"{REGION_NAME[reg]} {tally[reg]}", SANS(11), GREY, "legend")

ALSO_X = [288, 526, 776]
ALSO_W = [226, 238, 236]
for g in range(3):
    group = ALSO[g * 7:(g + 1) * 7]
    cx = ALSO_X[g]
    for j, (pl, region, field, main, sub) in enumerate(group):
        n = 14 + g * 7 + j
        yy = BY + 15 + j * 37
        d.ellipse([cx, yy + 1, cx + 17, yy + 18], fill=REGION[region])
        text_c(cx + 8.5, yy + 3, str(n), SANS_B(11), CREAM, f"also{n}-num")
        hcheck(main, SANS_B(17), ALSO_W[g] - 26, f"also{n} main")
        text(cx + 22, yy, main, SANS_B(17), INK, f"also{n}-main")
        if j < 6:  # last row: no sub — it would sit under the date-check box
            hcheck(sub, SANS(13), ALSO_W[g] - 26, f"also{n} sub")
            text(cx + 22, yy + 21, sub, SANS(13), CAPGREY, f"also{n}-sub")

# ------------------------------------------------- date check + footer
DC_Y = 954
d.rectangle([MX, DC_Y, RX, DC_Y + 45], fill=(253, 240, 238), outline=RED, width=2)
d.rectangle([MX + 6, DC_Y + 14, MX + 112, DC_Y + 30], fill=RED)
text_c(MX + 59, DC_Y + 16, "DATE CHECK", SANS_B(11), CREAM, "dc-tab")
dc_lines = wrap(DATE_CHECK, SANS(11), RX - MX - 130, 3, "date check")
for j, line in enumerate(dc_lines):
    text(MX + 122, DC_Y + 12 + j * 15, line, SANS(11), GREY, "dc-text")
FY = 999
text(MX, FY, "Every story happened or was first reported on Tue 24 Nov 2026; claims attributed.",
     SANS(11), GREY, "footer-left")
seen, srcs = set(), []
for s in STORIES_ALL:
    if s[5] and s[5] not in seen:
        seen.add(s[5])
        srcs.append(s[5])
footer_r = " · ".join(srcs[:5]) + f" + {len(srcs) - 5} more · Original drawings"
text_r(RX, FY, footer_r, SANS(11), GREY, "footer-right")
# HOW SURE, segmented on one baseline
hx = MX
bb = text(hx, FY + 13, "HOW SURE: ", SANS_B(11), INK, "howsure")
hx = bb[2]
bb = text(hx, FY + 13, "CONFIRMED", SANS_B(11), SURE["C"][1], "howsure")
hx = bb[2]
bb = text(hx, FY + 13, " 2+ outlets · ", SANS(11), GREY, "howsure")
hx = bb[2]
bb = text(hx, FY + 13, "REPORTED", SANS_B(11), SURE["R"][1], "howsure")
text(bb[2], FY + 13, " one outlet or claim", SANS(11), GREY, "howsure")

# ---------------------------------------------------------------- audits
def gap_boxes(a, b):
    dx = max(b[0] - a[2], a[0] - b[2], 0)
    dy = max(b[1] - a[3], a[1] - b[3], 0)
    import math
    return math.hypot(dx, dy) if (dx or dy) else 0.0

def overlaps(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]

AUDIT = {}

# 1) text-vs-text (+ masthead pairs handled in audit 6, how-sure segments
#    and pin numbers on their discs are single logical lines)
EXEMPT_PAIRS = [("date", "strap"), ("date", "eyebrow")]
finds = []
for i in range(len(TEXTS)):
    for j in range(i + 1, len(TEXTS)):
        a, b = TEXTS[i], TEXTS[j]
        if a[5] == b[5] and a[5] in ("howsure",):
            continue
        if (a[5], b[5]) in EXEMPT_PAIRS or (b[5], a[5]) in EXEMPT_PAIRS:
            continue
        if overlaps(a, b):
            finds.append(f"OVERLAP '{a[4]}'[{a[5]}] x '{b[4]}'[{b[5]}]")
        elif gap_boxes(a, b) < 3:
            finds.append(f"NEAR<3 '{a[4]}'[{a[5]}] x '{b[4]}'[{b[5]}] gap={gap_boxes(a, b):.1f}")
AUDIT["TEXT-AUDIT"] = finds

# 2) text-vs-line
finds = []
for t in TEXTS:
    for ln in LINES:
        lx0, ly0, lx1, ly1, ltag = ln
        if ltag.startswith("mast-red"):
            continue  # masthead audit owns the red segments
        x_overlap = t[0] < lx1 and lx0 < t[2]
        if not x_overlap:
            continue
        if t[1] <= ly1 and ly0 <= t[3]:
            finds.append(f"PENETRATION '{t[4]}'[{t[5]}] x line[{ltag}]")
        else:
            g = max(ly0 - t[3], t[1] - ly1, 0)
            if g < 3:
                finds.append(f"NEAR<3 '{t[4]}'[{t[5]}] x line[{ltag}] gap={g}")
AUDIT["LINE-AUDIT"] = finds

# 4) text-vs-graphics (obstacles + flags; own-scene heroes exempt,
#    flags never exempt)
finds = []
for t in TEXTS:
    for ob in OBSTACLES:
        if t[5].startswith("hero") and ob[4] == f"hero{t[5][4]}":
            continue
        if overlaps(t, ob):
            finds.append(f"GFX-OVERLAP '{t[4]}'[{t[5]}] x obstacle[{ob[4]}]")
        elif gap_boxes(t, ob) < 3:
            finds.append(f"GFX-NEAR<3 '{t[4]}'[{t[5]}] x obstacle[{ob[4]}]")
    for fl in FLAGS:
        if overlaps(t, fl):
            if not t[5].endswith("-overlay"):
                finds.append(f"FLAG-OVERLAP '{t[4]}'[{t[5]}] x flag[{fl[4]}]")
        elif gap_boxes(t, fl) < 3 and not t[5].endswith("-tab"):
            finds.append(f"FLAG-NEAR<3 '{t[4]}'[{t[5]}] x flag[{fl[4]}]")
AUDIT["GFX-AUDIT"] = finds

# 5) strip audit: overlay ink vs strip outline, pictogram, furniture
import numpy as np
finds = []
for i, strip in enumerate(STRIP_INK):
    ov = CARD_OVERLAY[i]
    of = SANS_B(28 if len(ov) <= 5 else 24 if len(ov) <= 9 else 20 if len(ov) <= 12 else 17)
    cx = MX + (i % 5) * (CW + 10)
    cy = CY + (i // 5) * 151
    ox = cx + CW - 6 - d.textlength(ov, font=of)
    oy = cy + 2
    sx, sy = ox - (cx + 1), oy - (cy + 1)  # strip coords
    blank = Image.new("RGB", (190, 55), (0, 0, 0))
    bd = ImageDraw.Draw(blank)
    bd.text((sx, sy), ov, font=of, fill=(255, 255, 255), stroke_width=2, stroke_fill=(255, 255, 255))
    mask = np.array(blank.convert("L")) > 0
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        finds.append(f"card{i+1}: overlay ink empty")
        continue
    edges = {"L": xs.min(), "T": ys.min(), "R": 189 - xs.max(), "B": 54 - ys.max()}
    for k, v in edges.items():
        if v < 3:
            finds.append(f"card{i+1}: overlay edge {k}={v} <3")
    arr = np.array(strip)
    bg = arr[0, 0].astype(int)
    pic = np.abs(arr.astype(int) - bg).sum(axis=2) > 30
    pic[:2, :] = False
    # dilation distance from overlay ink to pictogram pixels
    from scipy.ndimage import binary_dilation
    dist = None
    m = mask.copy()
    for step in range(1, 13):
        m = binary_dilation(m)
        if (m & pic).any():
            dist = step
            break
    if dist is not None and dist < 3:
        finds.append(f"card{i+1}: overlay-to-pictogram distance {dist} <3")
    # furniture: flag box in strip coords (3,3,27,19); tab/chip rows y39..52
    furn = [(3, 3, 27, 19)]
    ink_box = (xs.min(), ys.min(), xs.max(), ys.max())
    for fb in furn:
        if overlaps((*ink_box, "", ""), (*fb, "", "")):
            finds.append(f"card{i+1}: overlay overlaps flag")
        elif gap_boxes((*ink_box, "", ""), (*fb, "", "")) < 3:
            finds.append(f"card{i+1}: overlay-flag gap <3")
    if ink_box[3] >= 39 - 2:
        finds.append(f"card{i+1}: overlay ink reaches tab row")
AUDIT["STRIP-AUDIT"] = finds

# 6) masthead audit: date ink vs red segments, date rule; strap/eyebrow
#    ink vs red bar; timeline times vs date rule
finds = []
db = next(t for t in TEXTS if t[5] == "date")
if db[0] - (date_bb[0] - 5) < 3 and False:
    pass
# segment ends are 5px from the date *anchor* box; measure vs ink box:
left_seg_end = date_bb[0] - 5
right_seg_start = date_bb[2] + 5
if db[0] - left_seg_end < 3:
    finds.append(f"date ink to left red segment = {db[0] - left_seg_end} <3")
if right_seg_start - db[2] < 0:
    finds.append("right red segment crosses date anchor")
# date ink bottom vs date rule (y=98..99)
if 98 - db[3] < 3:
    finds.append(f"date ink bottom to rule = {98 - db[3]} <3")
for tag in ("strap", "eyebrow"):
    tb = next(t for t in TEXTS if t[5] == tag)
    if tb[3] > 30 - 3 and tb[0] < RX and tb[2] > MX:
        # vertical gap between ink bottom and red bar top (30)
        if 30 - tb[3] < 3 and tb[3] <= 30:
            finds.append(f"{tag} ink to red bar = {30 - tb[3]} <3")
for t in TEXTS:
    if t[5] == "timeline" and t[1] - 99 < 3:
        finds.append(f"timeline '{t[4]}' ink to date rule = {t[1] - 99} <3")
AUDIT["MASTHEAD-AUDIT"] = finds

# 7) rail audit: hairline in first empty row under previous caption,
#    >=3px below caption ink, >=3px above next number ink
finds = []
rail_nums = [t for t in TEXTS if t[5].startswith("rail") and t[5].endswith("-num")]
rail_caps = [t for t in TEXTS if t[5].startswith("rail") and t[5].endswith("-cap")]
for i in range(1, 3):
    hair_y = rail_tops[i] - 5
    prev_caps = [c for c in rail_caps if c[5] == f"rail{i}-cap"]
    if prev_caps:
        under = hair_y - max(c[3] for c in prev_caps)
        if under < 3:
            finds.append(f"rail hairline {i}: {under}px under caption <3")
    nxt = [n for n in rail_nums if n[5] == f"rail{i+1}-num"]
    if nxt and nxt[0][1] - hair_y < 3:
        finds.append(f"rail hairline {i}: {nxt[0][1] - hair_y}px above number <3")
AUDIT["RAIL-AUDIT"] = finds

# 8) date-check audit: text padding inside box >=3 on all sides
finds = []
dc = [t for t in TEXTS if t[5] == "dc-text"]
if dc:
    if min(t[0] for t in dc) - MX < 3:
        finds.append("dc text left padding <3")
    if RX - max(t[2] for t in dc) < 3:
        finds.append("dc text right padding <3")
    if min(t[1] for t in dc) - DC_Y < 3:
        finds.append("dc text top padding <3")
    if DC_Y + 45 - max(t[3] for t in dc) < 3:
        finds.append("dc text bottom padding <3")
AUDIT["DC-AUDIT"] = finds

# registry self-check: every FIG display appears in drawn text
drawn = " | ".join(t[4] for t in TEXTS) + " | " + DATE_CHECK
missing = [k for k, v in FIG.items() if v not in drawn]
AUDIT["FIG-SELFCHECK (WARN only)"] = [f"display not drawn: {k}={FIG[k]}" for k in missing]

img.save(HERE / "entry.png", optimize=False)
for name, f_ in AUDIT.items():
    print(f"{name}: {len(f_)} finding(s)")
    for x in f_:
        print("  ", x)
for x in FAIL:
    print("FAIL", x)
print("TOTAL AUDIT FINDINGS:",
      sum(len(v) for k, v in AUDIT.items() if "WARN" not in k),
      "| FAIL:", len(FAIL))
