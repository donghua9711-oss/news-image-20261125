#!/usr/bin/env python3
"""Compose the front page for 'The Day in Full', Wednesday 25 Nov 2026.

Layout, top to bottom: navy masthead with the date badge; a rainbow strip
counting the day's thirty stories by region; a UTC strip of timed moments;
three illustrated lead cards; a dot-matrix world map with numbered pins and
a legend; eight story rows in two columns; an 'In Brief' band of nineteen
one-liners; and a navy footer carrying the date check and the source list.

Run once, locally:  python3 compose.py   ->   entry.png (1024 x 1024)
The illustrations under assets/ were drawn for this edition by a small
Pillow script. SOURCES.md names the outlet behind every story.
"""

from PIL import Image, ImageDraw, ImageFont, ImageOps

PAGE = 1024


def hx(code):
    return tuple(int(code[i:i + 2], 16) for i in (0, 2, 4))


PAPER_TONE = hx("F7F3E9")
CREAM_TONE = hx("F7F3E9")
BODY_TEXT = hx("181C26")
MUTED_TEXT = hx("343A44")
FAINT_TEXT = hx("606670")
NAVY_DEEP = hx("0D264C")
NAVY_DEEPER = hx("081832")
BAND_PALE = hx("EEE8D8")
HAIRLINE = hx("B2AC9E")
MAP_LAND = hx("78808E")
MAP_SEA = hx("CEC8B8")
GOLD_TEXT = hx("FFC456")
SKY_TEXT = hx("B2C0D8")

REGION_TONE = {
    "ASIA": hx("C4342C"),
    "EUROPE": hx("265CA8"),
    "AMERICAS": hx("E08A1E"),
    "MIDDLE EAST": hx("7A4AA0"),
    "AFRICA": hx("228B54"),
    "OCEANIA": hx("1E96A0"),
    "GLOBAL": hx("5A606C"),
}
REGION_SEQ = ["ASIA", "EUROPE", "AMERICAS", "MIDDLE EAST", "AFRICA", "OCEANIA", "GLOBAL"]

# Drawn stories as tuples:
# (number, region, city, latitude, longitude, headline, summary, illustration)
DRAWN = [
    (1, "AMERICAS", "Santa Clara", 37.37, -121.97,
     "Nvidia slides 7% as Huang return unravels",
     "Nvidia fell about 7% on Tuesday as the rally from Jensen Huang's "
     "reinstatement faded; lawmakers demand answers on President Trump's "
     "role and Huang is due before a Senate committee.",
     "illo-nvidia.png"),
    (2, "MIDDLE EAST", "Strait of Hormuz", 26.57, 56.27,
     "Iran says two tankers hit mines in Hormuz",
     "Iran's Revolutionary Guard navy said early on Wednesday that two oil "
     "tankers struck naval mines and caught fire on an unauthorised "
     "route; CENTCOM denied the mine claims.",
     "illo-hormuz.png"),
    (3, "AFRICA", "Dakar", 14.72, -17.47,
     "Senegal champions again as court returns title",
     "The Court of Arbitration for Sport upheld Senegal's appeal and set "
     "aside CAF's forfeiture ruling, so January's 1-0 extra-time win over "
     "Morocco stands; Morocco vows a new challenge.",
     "illo-senegal.png"),
    (4, "GLOBAL", "Tokyo", 35.68, 139.69,
     "Asian tech stocks tumble on AI-boom doubts",
     "Japan's Nikkei fell 2.76% and the S&P 500 0.5% as investors doubted "
     "the AI boom again; India's Sensex bucked the slide, up 1.8%, and "
     "Brent crude sat at $87.49."),
    (5, "ASIA", "Jiuquan", 40.97, 100.23,
     "Shenzhou-24 carries Pakistan's first astronaut",
     "China's Shenzhou-24 lifted off at 00:18 UTC with Tang Hongbo, Wu Yi "
     "and Muhammad Zeeshan Ali, the first Pakistani in orbit and "
     "Tiangong's first foreign visitor."),
    (6, "EUROPE", "Madrid", 40.42, -3.70,
     "Spain counts down to Sunday's snap election",
     "Pedro Sánchez and Alberto Núñez Feijóo clash over the housing "
     "crisis that triggered the snap ballot; polls put the PP ahead "
     "before Sunday's vote."),
    (7, "AMERICAS", "Cartagena", 10.39, -75.51,
     "Special forces free Cartagena supermarket hostages",
     "Colombian special forces stormed an Éxito supermarket after a "
     "15-hour standoff, freeing about 20 hostages seized by gunmen after "
     "a failed armoured-truck robbery."),
    (8, "EUROPE", "Kyiv", 50.45, 30.52,
     "Ukraine needs €115 billion in support for 2027",
     "President Zelenskiy said Ukraine will need €115 billion ($125 "
     "billion) in external support in 2027; about €90 billion is "
     "committed and talks continue on the rest."),
    (9, "MIDDLE EAST", "Gaza City", 31.50, 34.47,
     "Israeli strike kills Hamas security chief in Gaza",
     "An Israeli airstrike in western Gaza City killed Naeem Abu Nahel, "
     "head of Hamas's internal security apparatus; six others died in "
     "strikes the same day."),
    (10, "AFRICA", "Minembwe", -3.93, 28.92,
     "Congo army seeks aircraft as rebels claim shoot-down",
     "DR Congo's military lost contact with a Cessna 208 near Minembwe; "
     "FRN rebels say they shot it down, with two aboard reportedly "
     "killed and two captured."),
    (11, "OCEANIA", "Honiara", -9.65, 160.16,
     "Solomon Islands signs Australia security treaty",
     "Honiara made Australia its security partner of choice and "
     "pledged no foreign bases, as its 2022 security pact with China "
     "comes to an end."),
]

# One-liners as tuples: (region, city, latitude, longitude, line, outlet)
BRIEF = [
    ("ASIA", "Dhaka", 23.81, 90.41,
     "Hasina sets Dec 16 for her return, asking Dhaka to fly her home from exile in India", "DW"),
    ("ASIA", "Seoul", 37.57, 126.98,
     "Seoul says Russian jets entered its air defence zone; fighters scrambled", "Reuters"),
    ("ASIA", "Shanghai", 31.23, 121.47,
     "China investigates Shanghai party chief Chen Jining", "Reuters"),
    ("ASIA", "Tai Po", 22.45, 114.17,
     "Hong Kong marks one year since the Tai Po fire", "AP"),
    ("ASIA", "New Delhi", 28.61, 77.21,
     "Sensex rises 1.8%, bucking the global AI sell-off", "Reuters"),
    ("EUROPE", "Warsaw", 52.23, 21.01,
     "Russian drone briefly enters Polish airspace, days after missile incidents", "DW"),
    ("EUROPE", "Moscow", 55.76, 37.62,
     "Leaked data puts Russian war deaths near 500,000", "BBC"),
    ("EUROPE", "London", 51.51, -0.13,
     "England's heat-linked deaths top 5,200, the highest on record", "BBC"),
    ("AMERICAS", "Washington", 38.90, -77.04,
     "Democrats win a House majority of at least 259 seats", "AP"),
    ("AMERICAS", "Ottawa", 45.42, -75.70,
     "Pentagon criticises Canada's military spending", "Reuters"),
    ("MIDDLE EAST", "Riyadh", 24.71, 46.68,
     "Houthi attack on a Riyadh tower injures 11", "Al Jazeera"),
    ("MIDDLE EAST", "Qom", 34.64, 50.88,
     "Iran flogs singer Parastoo Ahmadi 74 times over an unveiled online concert", "AFP"),
    ("AFRICA", "Lusaka", -15.39, 28.32,
     "Zambia indicts an opposition leader on treason charges", "Reuters"),
    ("OCEANIA", "Canberra", -35.28, 149.13,
     "Australia's inflation rises to 4.9%", "ABC News"),
    ("GLOBAL", "Vienna", 48.21, 16.37,
     "Oil falls more than 20% in November; Brent at $87.49", "Reuters"),
    ("GLOBAL", "Geneva", 46.20, 6.14,
     "UN warns HIV gains could unravel as funding falls", "Reuters"),
    ("GLOBAL", "Darmstadt", 49.87, 8.65,
     "BepiColombo slips into Mercury orbit despite a glitch", "ESA"),
    ("GLOBAL", "Sohar", 24.36, 56.75,
     "Microplastics found in most fish sampled off Oman", "Reuters"),
    ("GLOBAL", "Appalachia", 38.50, -80.50,
     "Blight-resistant American chestnuts return to Appalachian forests", "AP"),
]

# Timed moments for the UTC strip: (clock, text)
MOMENTS = [
    ("00:18", "Shenzhou-24 lifts off with Pakistan's first astronaut"),
    ("04:12", "Ukraine hits a Russian weapons ship in the Gulf of Finland"),
    ("05:14", "Nvidia staff applaud Huang as he returns to headquarters"),
    ("06:00", "Tokyo close: the Nikkei ends down 2.76%"),
]

# Dot-matrix landmass on an equirectangular grid: 100 columns of longitude
# (-180..180) by 30 rows of latitude (75..-60). '#' marks land, '.' sea.
# The rows are packed five to a line, separated by '/', to keep the data
# block compact; unpack_grid() restores the row list.
PACKED_GRID = [
    "...#####....##.##.##..##..#...........####....######..##########..########..########../...######..#########.########......#####...........####.....####.####################/...######..##################.......####....#....################.###################/.....####..###################........#...................#######..################..###../............########..################...................#..#################..#....###..",
    "...............#######..################.......................####################........./................######.###########......####.......#######....#####################........../................######.################.......................##.#################...######./...............#################...............................#.#####################........../....................#########.....................................#####################........",
    "...................#######........................................######################..##...../...................####...........................................######################.#....#...../......................###..........................................####################..#..##.....#...../........................##..##........................................#########..##.....##........../.............................####......................................##########..##.......##.#..##....",
    ".............................######......................................#######..####........##################./..............................#######......................................##########..#.....########../..............................########.......................................##########..####......####......../...............................########.......................................######...................#######..##/...............................#########......................................#######..#...............#######..###",
    "...............................########.......................................#######..##..............#######..###/................................######.......................................######..#...............######..##/................................#####.........................................#####.....................#####..#/..................................###..........................................###......................####../..................................###................................................................................##..##",
    "..................................##.......................................................................................##./..................................##......................................................................................##../...................................#......................................................................................../...................................#......................................................................................../....................................................................................................",
]
GRID_W = 100
GRID_H = 30


def unpack_grid():
    rows = []
    for chunk in PACKED_GRID:
        rows.extend(chunk.split("/"))
    return [row.ljust(GRID_W, ".")[:GRID_W] for row in rows]


# ------------------------------------------------------------------ fonts ---
FONT_HOME = "/usr/share/fonts/truetype/dejavu"
_font_cache = {}


def typeface(filename, size):
    key = (filename, size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(f"{FONT_HOME}/{filename}", size)
    return _font_cache[key]


def display(size):
    return typeface("DejaVuSerif-Bold.ttf", size)


def heavy(size):
    return typeface("DejaVuSans-Bold.ttf", size)


def regular(size):
    return typeface("DejaVuSans.ttf", size)


# -------------------------------------------------------------- text flow ---
def break_lines(draw, text, face, limit):
    """Greedy pixel-width word wrap, returned as a list of lines."""
    done, pending = [], ""
    for word in text.split(" "):
        trial = word if not pending else pending + " " + word
        if draw.textlength(trial, font=face) <= limit:
            pending = trial
        else:
            done.append(pending)
            pending = word
    if pending:
        done.append(pending)
    return done


def clamp_lines(draw, text, face, limit, count):
    """Wrap to at most `count` lines, ellipsising the tail of the last."""
    lines = break_lines(draw, text, face, limit)
    if len(lines) <= count:
        return lines
    kept = lines[:count]
    tail = kept[-1]
    while tail and draw.textlength(tail + "…", font=face) > limit:
        tail = tail[:-1]
    kept[-1] = tail + "…"
    return kept


def pin_position(lat, lon, box):
    """Project lat/lon into the map box (same projection as the grid)."""
    x0, y0, wdt, hgt = box
    return (x0 + (lon + 180.0) / 360.0 * wdt,
            y0 + (75.0 - lat) / 135.0 * hgt)

# --------------------------------------------------------------- sections ---
def masthead(d):
    d.rectangle((0, 0, PAGE, 104), fill=NAVY_DEEP)
    d.rectangle((0, 100, PAGE, 104), fill=hx("E08A1E"))
    d.text((26, 14), "THE DAY IN FULL", font=display(47), fill=CREAM_TONE)
    d.text((28, 70), "One page · thirty verified stories · every story reported on the day itself",
           font=regular(14), fill=SKY_TEXT)
    badge = (806, 12, 1000, 92)
    d.rectangle(badge, outline=CREAM_TONE, width=2)
    mid = (badge[0] + badge[2]) / 2
    d.text((mid, 19), "WEDNESDAY", font=heavy(17), fill=GOLD_TEXT, anchor="ma")
    d.text((mid, 42), "25 NOVEMBER", font=heavy(21), fill=CREAM_TONE, anchor="ma")
    d.text((mid, 68), "2026", font=heavy(15), fill=SKY_TEXT, anchor="ma")


def region_strip(d):
    tally = {}
    for story in DRAWN:
        tally[story[1]] = tally.get(story[1], 0) + 1
    for brief in BRIEF:
        tally[brief[0]] = tally.get(brief[0], 0) + 1
    total = sum(tally.values())
    cursor = 0
    for name in REGION_SEQ:
        span = round(PAGE * tally[name] / total)
        d.rectangle((cursor, 104, cursor + span, 134), fill=REGION_TONE[name])
        label = f"{name} {tally[name]}"
        d.text((cursor + span / 2, 112), label, font=heavy(11),
               fill=(255, 255, 255), anchor="ma")
        cursor += span


def utc_strip(d):
    d.rectangle((0, 134, PAGE, 180), fill=BAND_PALE)
    d.text((26, 149), "THE DAY IN UTC", font=heavy(14), fill=NAVY_DEEP)
    cursor = 196
    for clock, text in MOMENTS:
        d.text((cursor, 138), clock, font=heavy(14), fill=REGION_TONE["ASIA"])
        for i, line in enumerate(break_lines(d, text, regular(11), 190)[:2]):
            d.text((cursor, 156 + 12 * i), line, font=regular(11), fill=BODY_TEXT)
        cursor += 206
    d.line((0, 180, PAGE, 180), fill=HAIRLINE, width=1)


def lead_card(d, page_img, x, story):
    num, region, city, _lat, _lon, headline, summary, illo_name = story
    top, bottom, width = 180, 420, 320
    d.rectangle((x, top, x + width, bottom), fill=(255, 255, 255), outline=HAIRLINE)
    d.rectangle((x, top, x + width, top + 5), fill=REGION_TONE[region])
    art = Image.open(f"assets/{illo_name}").convert("RGB")
    page_img.paste(ImageOps.fit(art, (width, 104)), (x, top + 5))
    pen = top + 115
    kicker = f"{num} · {region} — {city.upper()}"
    d.text((x + 10, pen), kicker, font=heavy(11), fill=REGION_TONE[region])
    pen += 17
    for line in clamp_lines(d, headline, heavy(19), width - 20, 2):
        d.text((x + 10, pen), line, font=heavy(19), fill=BODY_TEXT)
        pen += 23
    pen += 2
    for line in clamp_lines(d, summary, regular(12), width - 20, 4):
        d.text((x + 10, pen), line, font=regular(12), fill=MUTED_TEXT)
        pen += 15


def world_map(d):
    box = (16, 428, 636, 174)
    rows = unpack_grid()
    cell_w = box[2] / GRID_W
    cell_h = box[3] / GRID_H
    for r, row in enumerate(rows):
        for c, mark in enumerate(row):
            cx = box[0] + (c + 0.5) * cell_w
            cy = box[1] + (r + 0.5) * cell_h
            if mark == "#":
                d.ellipse((cx - 1.7, cy - 1.7, cx + 1.7, cy + 1.7), fill=MAP_LAND)
            else:
                d.ellipse((cx - 0.7, cy - 0.7, cx + 0.7, cy + 0.7), fill=MAP_SEA)
    for region, _city, lat, lon, _line, _outlet in BRIEF:
        px, py = pin_position(lat, lon, box)
        d.ellipse((px - 3, py - 3, px + 3, py + 3),
                  fill=REGION_TONE[region], outline=(255, 255, 255), width=1)
    for story in DRAWN:
        px, py = pin_position(story[3], story[4], box)
        d.ellipse((px - 10, py - 10, px + 10, py + 10),
                  fill=NAVY_DEEP, outline=(255, 255, 255), width=2)
        d.text((px, py - 7), str(story[0]), font=heavy(12),
               fill=(255, 255, 255), anchor="ma")
    # Legend beside the map.
    lx = 676
    d.text((lx, 422), "WHERE IT HAPPENED", font=heavy(14), fill=NAVY_DEEP)
    d.line((lx, 442, 1008, 442), fill=HAIRLINE, width=1)
    pen = 448
    for story in DRAWN:
        d.text((lx, pen), str(story[0]), font=heavy(12), fill=REGION_TONE[story[1]])
        entry = clamp_lines(d, f"{story[2]} — {story[5]}", regular(11), 306, 1)[0]
        d.text((lx + 26, pen), entry, font=regular(11), fill=BODY_TEXT)
        pen += 15
    d.text((lx, pen + 2), "Coloured dots: the 19 briefs, by region.",
           font=regular(11), fill=FAINT_TEXT)


def story_rows(d):
    rest = DRAWN[3:]
    for i, story in enumerate(rest):
        num, region = story[0], story[1]
        x = 16 + (i % 2) * 512
        y = 610 + (i // 2) * 52
        d.rectangle((x, y, x + 496, y + 48), fill=(255, 255, 255), outline=HAIRLINE)
        d.rectangle((x, y, x + 5, y + 48), fill=REGION_TONE[region])
        d.text((x + 13, y + 5), str(num), font=heavy(17), fill=REGION_TONE[region])
        head = clamp_lines(d, story[5], heavy(14), 438, 1)[0]
        d.text((x + 44, y + 4), head, font=heavy(14), fill=BODY_TEXT)
        for j, line in enumerate(clamp_lines(d, story[6], regular(11), 438, 2)):
            d.text((x + 44, y + 22 + 12 * j), line, font=regular(11), fill=MUTED_TEXT)


def brief_band(d):
    d.rectangle((0, 818, PAGE, 838), fill=NAVY_DEEP)
    d.text((26, 821), "IN BRIEF — 19 MORE STORIES OF THE DAY",
           font=heavy(13), fill=CREAM_TONE)
    middle = (len(BRIEF) + 1) // 2
    for col, group in enumerate((BRIEF[:middle], BRIEF[middle:])):
        x = 26 + col * 500
        pen = 846
        for region, city, _lat, _lon, line, _outlet in group:
            tag = f"{city}: "
            d.text((x, pen), tag, font=heavy(11), fill=REGION_TONE[region])
            tag_w = d.textlength(tag, font=heavy(11))
            text = clamp_lines(d, line, regular(11), 474 - tag_w, 1)[0]
            d.text((x + tag_w, pen), text, font=regular(11), fill=BODY_TEXT)
            pen += 16


def colophon(d):
    d.rectangle((0, 1002, PAGE, PAGE), fill=NAVY_DEEPER)
    d.text((26, 1008),
           "DATE CHECK: every story here was reported on Wednesday 25 November 2026 (UTC).",
           font=heavy(10), fill=GOLD_TEXT)
    d.text((998, 1008), "Sources: Reuters · AP · BBC · Al Jazeera · AFP · DW · ABC · ESA",
           font=regular(9), fill=SKY_TEXT, anchor="ra")


def build():
    page_img = Image.new("RGB", (PAGE, PAGE), PAPER_TONE)
    d = ImageDraw.Draw(page_img)
    masthead(d)
    region_strip(d)
    utc_strip(d)
    for slot, story in enumerate(DRAWN[:3]):
        lead_card(d, page_img, 16 + slot * 336, story)
    world_map(d)
    story_rows(d)
    brief_band(d)
    colophon(d)
    page_img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    build()
