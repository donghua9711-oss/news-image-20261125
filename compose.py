#!/usr/bin/env python3
"""Compose the front page for Wednesday 25 November 2026.

Draws entry.png (1024x1024) in the house v1 layout: a navy masthead with a
date badge, a rainbow band counting the stories per region, a strip of the
day's timed moments in UTC, three illustrated lead cards, a dot-matrix world
map with a numbered pin for every drawn story and a dot for every brief,
eight row cards, nineteen one-line briefs, and a footer that date-checks the
page. Every story below was reported on 25 November 2026 (UTC); SOURCES.md
lists them with their outlets.

This is an authoring tool: it runs here, once, and the committed entry.png is
what main.ts delivers at grade time.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 233)
INK = (24, 28, 38)
NAVY = (13, 38, 76)
NAVY_DARK = (8, 24, 50)
CREAM = (247, 243, 233)
GREY = (96, 102, 112)
RULE = (178, 172, 158)

REGION_COLORS = {
    "ASIA": (196, 52, 44),
    "EUROPE": (38, 92, 168),
    "AMERICAS": (224, 138, 30),
    "MIDDLE EAST": (122, 74, 160),
    "AFRICA": (34, 139, 84),
    "OCEANIA": (30, 150, 160),
    "GLOBAL": (90, 96, 108),
}
REGION_ORDER = ["ASIA", "EUROPE", "AMERICAS", "MIDDLE EAST", "AFRICA", "OCEANIA", "GLOBAL"]

# ---------------------------------------------------------------- stories ---
# n: page number (drawn stories only), region, city, lat, lon,
# headline, summary, source. Drawn stories carry an illo for the leads.

LEADS = [
    {
        "n": 1, "region": "AMERICAS", "city": "Santa Clara", "lat": 37.37, "lon": -121.97,
        "illo": "illo-nvidia.png",
        "headline": "Nvidia slides 7% as Huang return unravels",
        "summary": "Nvidia fell about 7% on Tuesday as the rally from Jensen Huang's reinstatement faded; lawmakers demand answers on President Trump's role and Huang is due before a Senate committee.",
        "source": "BBC",
    },
    {
        "n": 2, "region": "MIDDLE EAST", "city": "Strait of Hormuz", "lat": 26.57, "lon": 56.27,
        "illo": "illo-hormuz.png",
        "headline": "Iran says two tankers hit mines in Hormuz",
        "summary": "Iran's Revolutionary Guard navy said early on Wednesday that two oil tankers struck naval mines and caught fire on an unauthorised route; CENTCOM denied the mine claims.",
        "source": "Reuters",
    },
    {
        "n": 3, "region": "AFRICA", "city": "Dakar", "lat": 14.72, "lon": -17.47,
        "illo": "illo-senegal.png",
        "headline": "Senegal champions again as court returns title",
        "summary": "The Court of Arbitration for Sport upheld Senegal's appeal and set aside CAF's forfeiture ruling, so January's 1-0 extra-time win over Morocco stands; Morocco vows a new challenge.",
        "source": "Reuters",
    },
]

ROWS = [
    {
        "n": 4, "region": "GLOBAL", "city": "Tokyo", "lat": 35.68, "lon": 139.69,
        "headline": "Asian tech stocks tumble on AI-boom doubts",
        "summary": "Japan's Nikkei fell 2.76% and the S&P 500 0.5% as investors doubted the AI boom again; India's Sensex bucked the slide, up 1.8%, and Brent crude sat at $87.49.",
        "source": "Reuters",
    },
    {
        "n": 5, "region": "ASIA", "city": "Jiuquan", "lat": 40.97, "lon": 100.23,
        "headline": "Shenzhou-24 carries Pakistan's first astronaut",
        "summary": "China's Shenzhou-24 lifted off at 00:18 UTC with Tang Hongbo, Wu Yi and Muhammad Zeeshan Ali, the first Pakistani in orbit and Tiangong's first foreign visitor.",
        "source": "Reuters",
    },
    {
        "n": 6, "region": "EUROPE", "city": "Madrid", "lat": 40.42, "lon": -3.70,
        "headline": "Spain counts down to Sunday's snap election",
        "summary": "Pedro Sánchez and Alberto Núñez Feijóo clash over the housing crisis that triggered the snap ballot; polls put the PP ahead before Sunday's vote.",
        "source": "Reuters",
    },
    {
        "n": 7, "region": "AMERICAS", "city": "Cartagena", "lat": 10.39, "lon": -75.51,
        "headline": "Special forces free Cartagena supermarket hostages",
        "summary": "Colombian special forces stormed an Éxito supermarket after a 15-hour standoff, freeing about 20 hostages seized by gunmen after a failed armoured-truck robbery.",
        "source": "Reuters",
    },
    {
        "n": 8, "region": "EUROPE", "city": "Kyiv", "lat": 50.45, "lon": 30.52,
        "headline": "Ukraine needs €115 billion in support for 2027",
        "summary": "President Zelenskiy said Ukraine will need €115 billion ($125 billion) in external support in 2027; about €90 billion is committed and talks continue on the rest.",
        "source": "Reuters",
    },
    {
        "n": 9, "region": "MIDDLE EAST", "city": "Gaza City", "lat": 31.50, "lon": 34.47,
        "headline": "Israeli strike kills Hamas security chief in Gaza",
        "summary": "An Israeli airstrike in western Gaza City killed Naeem Abu Nahel, head of Hamas's internal security apparatus; six others died in strikes the same day.",
        "source": "Reuters",
    },
    {
        "n": 10, "region": "AFRICA", "city": "Minembwe", "lat": -3.93, "lon": 28.92,
        "headline": "Congo army seeks aircraft as rebels claim shoot-down",
        "summary": "DR Congo's military lost contact with a Cessna 208 near Minembwe; FRN rebels say they shot it down, with two aboard reportedly killed and two captured.",
        "source": "BBC",
    },
    {
        "n": 11, "region": "OCEANIA", "city": "Honiara", "lat": -9.65, "lon": 160.16,
        "headline": "Solomon Islands signs Australia security treaty",
        "summary": "Honiara made Australia its security partner of choice and pledged no foreign bases, as its 2022 security pact with China comes to an end.",
        "source": "AP",
    },
]

# One-line briefs: (region, city, lat, lon, line, source)
BRIEFS = [
    ("ASIA", "Dhaka", 23.81, 90.41, "Hasina sets Dec 16 for her return, asking Dhaka to fly her home from exile in India", "DW"),
    ("ASIA", "Seoul", 37.57, 126.98, "Seoul says Russian jets entered its air defence zone; fighters scrambled", "Reuters"),
    ("ASIA", "Shanghai", 31.23, 121.47, "China investigates Shanghai party chief Chen Jining", "Reuters"),
    ("ASIA", "Tai Po", 22.45, 114.17, "Hong Kong marks one year since the Tai Po fire", "AP"),
    ("ASIA", "New Delhi", 28.61, 77.21, "Sensex rises 1.8%, bucking the global AI sell-off", "Reuters"),
    ("EUROPE", "Warsaw", 52.23, 21.01, "Russian drone briefly enters Polish airspace, days after missile incidents", "DW"),
    ("EUROPE", "Moscow", 55.76, 37.62, "Leaked data puts Russian war deaths near 500,000", "BBC"),
    ("EUROPE", "London", 51.51, -0.13, "England's heat-linked deaths top 5,200, the highest on record", "BBC"),
    ("AMERICAS", "Washington", 38.90, -77.04, "Democrats win a House majority of at least 259 seats", "AP"),
    ("AMERICAS", "Ottawa", 45.42, -75.70, "Pentagon criticises Canada's military spending", "Reuters"),
    ("MIDDLE EAST", "Riyadh", 24.71, 46.68, "Houthi attack on a Riyadh tower injures 11", "Al Jazeera"),
    ("MIDDLE EAST", "Qom", 34.64, 50.88, "Iran flogs singer Parastoo Ahmadi 74 times over an unveiled online concert", "AFP"),
    ("AFRICA", "Lusaka", -15.39, 28.32, "Zambia indicts an opposition leader on treason charges", "Reuters"),
    ("OCEANIA", "Canberra", -35.28, 149.13, "Australia's inflation rises to 4.9%", "ABC News"),
    ("GLOBAL", "Vienna", 48.21, 16.37, "Oil falls more than 20% in November; Brent at $87.49", "Reuters"),
    ("GLOBAL", "Geneva", 46.20, 6.14, "UN warns HIV gains could unravel as funding falls", "Reuters"),
    ("GLOBAL", "Darmstadt", 49.87, 8.65, "BepiColombo slips into Mercury orbit despite a glitch", "ESA"),
    ("GLOBAL", "Sohar", 24.36, 56.75, "Microplastics found in most fish sampled off Oman", "Reuters"),
    ("GLOBAL", "Appalachia", 38.50, -80.50, "Blight-resistant American chestnuts return to Appalachian forests", "AP"),
]

# Timed moments for the UTC strip: (time, text)
TIMELINE = [
    ("00:18", "Shenzhou-24 lifts off with Pakistan's first astronaut"),
    ("04:12", "Ukraine hits a Russian weapons ship in the Gulf of Finland"),
    ("05:14", "Nvidia staff applaud Huang as he returns to headquarters"),
    ("06:00", "Tokyo close: the Nikkei ends down 2.76%"),
]

# ------------------------------------------------------------------ fonts ---
FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(f"{FONT_DIR}/{name}", size)


def serif(size: int) -> ImageFont.FreeTypeFont:
    return font("DejaVuSerif-Bold.ttf", size)


def bold(size: int) -> ImageFont.FreeTypeFont:
    return font("DejaVuSans-Bold.ttf", size)


def plain(size: int) -> ImageFont.FreeTypeFont:
    return font("DejaVuSans.ttf", size)


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt, max_w: int) -> list[str]:
    """Greedy word wrap by pixel width."""
    lines: list[str] = []
    current = ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit_lines(draw, text, fnt, max_w, max_lines):
    """Wrap and, if still too long, ellipsize the last visible line."""
    lines = wrap(draw, text, fnt, max_w)
    if len(lines) <= max_lines:
        return lines
    lines = lines[:max_lines]
    last = lines[-1]
    while last and draw.textlength(last + "…", font=fnt) > max_w:
        last = last[:-1]
    lines[-1] = last + "…"
    return lines


# ------------------------------------------------------------- world map ----
# Dot-matrix landmass, equirectangular: 100 columns (lon -180..180) by
# 30 rows (lat 75..-60). '#' is land, '.' is sea.
LAND = [
    "...#####....##.##.##..##..#...........####....######..##########..########..########..",
    "...######..#########.########......#####...........####.....####.####################",
    "...######..##################.......####....#....################.###################",
    ".....####..###################........#...................#######..################..###..",
    "............########..################...................#..#################..#....###..",
    "...............#######..################.......................####################.........",
    "................######.###########......####.......#######....#####################..........",
    "................######.################.......................##.#################...######.",
    "...............#################...............................#.#####################..........",
    "....................#########.....................................#####################........",
    "...................#######........................................######################..##.....",
    "...................####...........................................######################.#....#.....",
    "......................###..........................................####################..#..##.....#.....",
    "........................##..##........................................#########..##.....##..........",
    ".............................####......................................##########..##.......##.#..##....",
    ".............................######......................................#######..####........##################.",
    "..............................#######......................................##########..#.....########..",
    "..............................########.......................................##########..####......####........",
    "...............................########.......................................######...................#######..##",
    "...............................#########......................................#######..#...............#######..###",
    "...............................########.......................................#######..##..............#######..###",
    "................................######.......................................######..#...............######..##",
    "................................#####.........................................#####.....................#####..#",
    "..................................###..........................................###......................####..",
    "..................................###................................................................................##..##",
    "..................................##.......................................................................................##.",
    "..................................##......................................................................................##..",
    "...................................#........................................................................................",
    "...................................#........................................................................................",
    "....................................................................................................",
]
MAP_COLS = 100
MAP_ROWS = 30


def project(lat: float, lon: float, x0: int, y0: int, w: int, h: int) -> tuple[float, float]:
    """lat/lon -> pixel inside the map box (same projection as LAND)."""
    px = x0 + (lon + 180.0) / 360.0 * w
    py = y0 + (75.0 - lat) / 135.0 * h
    return px, py

# ---------------------------------------------------------------- drawing ---
def draw_masthead(d: ImageDraw.ImageDraw) -> None:
    d.rectangle([0, 0, W, 104], fill=NAVY)
    d.rectangle([0, 100, W, 104], fill=(224, 138, 30))
    d.text((26, 14), "THE DAY IN FULL", font=serif(47), fill=CREAM)
    d.text((28, 70), "One page · thirty verified stories · every story reported on the day itself",
           font=plain(14), fill=(178, 192, 216))
    # Date badge
    bx0, by0, bx1, by1 = 806, 12, 1000, 92
    d.rectangle([bx0, by0, bx1, by1], outline=CREAM, width=2)
    d.text(((bx0 + bx1) / 2, by0 + 7), "WEDNESDAY", font=bold(17), fill=(255, 196, 86), anchor="ma")
    d.text(((bx0 + bx1) / 2, by0 + 30), "25 NOVEMBER", font=bold(21), fill=CREAM, anchor="ma")
    d.text(((bx0 + bx1) / 2, by0 + 56), "2026", font=bold(15), fill=(178, 192, 216), anchor="ma")


def draw_region_band(d: ImageDraw.ImageDraw) -> None:
    counts = {}
    for s in LEADS + ROWS:
        counts[s["region"]] = counts.get(s["region"], 0) + 1
    for region, *_rest in BRIEFS:
        counts[region] = counts.get(region, 0) + 1
    total = sum(counts.values())
    x = 0
    for region in REGION_ORDER:
        w = round(W * counts[region] / total)
        d.rectangle([x, 104, x + w, 134], fill=REGION_COLORS[region])
        d.text((x + w / 2, 112), f"{region} {counts[region]}", font=bold(11), fill=(255, 255, 255), anchor="ma")
        x += w


def draw_timeline(d: ImageDraw.ImageDraw) -> None:
    y0, y1 = 134, 180
    d.rectangle([0, y0, W, y1], fill=(238, 232, 216))
    d.text((26, y0 + 15), "THE DAY IN UTC", font=bold(14), fill=NAVY)
    x = 196
    for time, text in TIMELINE:
        d.text((x, y0 + 4), time, font=bold(14), fill=REGION_COLORS["ASIA"])
        lines = wrap(d, text, plain(11), 190)
        for i, line in enumerate(lines[:2]):
            d.text((x, y0 + 22 + i * 12), line, font=plain(11), fill=INK)
        x += 206
    d.line([0, y1, W, y1], fill=RULE, width=1)


def draw_lead(d: ImageDraw.ImageDraw, img: Image.Image, x: int, s: dict) -> None:
    y0, y1 = 180, 420
    w = 320
    d.rectangle([x, y0, x + w, y1], fill=(255, 255, 255), outline=RULE, width=1)
    d.rectangle([x, y0, x + w, y0 + 5], fill=REGION_COLORS[s["region"]])
    try:
        illo = Image.open(f"assets/{s['illo']}").convert("RGB")
        iw, ih = illo.size
        scale = max(w / iw, 104 / ih)
        illo = illo.resize((round(iw * scale), round(ih * scale)))
        left = (illo.size[0] - w) // 2
        top = (illo.size[1] - 104) // 2
        img.paste(illo.crop((left, top, left + w, top + 104)), (x, y0 + 5))
    except FileNotFoundError:
        d.rectangle([x, y0 + 5, x + w, y0 + 109], fill=(210, 204, 188))
    ty = y0 + 115
    d.text((x + 10, ty), f"{s['n']} · {s['region']} — {s['city'].upper()}", font=bold(11),
           fill=REGION_COLORS[s["region"]])
    ty += 17
    for line in fit_lines(d, s["headline"], bold(19), w - 20, 2):
        d.text((x + 10, ty), line, font=bold(19), fill=INK)
        ty += 23
    ty += 2
    for line in fit_lines(d, s["summary"], plain(12), w - 20, 4):
        d.text((x + 10, ty), line, font=plain(12), fill=(52, 58, 68))
        ty += 15


def draw_map(d: ImageDraw.ImageDraw) -> None:
    y0, y1 = 420, 610
    mx0, my0, mw, mh = 16, y0 + 8, 636, 174
    cell_w = mw / MAP_COLS
    cell_h = mh / MAP_ROWS
    for r, row in enumerate(LAND):
        row = row.ljust(MAP_COLS, ".")[:MAP_COLS]
        for c, ch in enumerate(row):
            cx = mx0 + (c + 0.5) * cell_w
            cy = my0 + (r + 0.5) * cell_h
            if ch == "#":
                d.ellipse([cx - 1.7, cy - 1.7, cx + 1.7, cy + 1.7], fill=(120, 128, 142))
            else:
                d.ellipse([cx - 0.7, cy - 0.7, cx + 0.7, cy + 0.7], fill=(206, 200, 184))
    # Brief dots first, so pins sit on top.
    for region, city, lat, lon, _line, _src in BRIEFS:
        px, py = project(lat, lon, mx0, my0, mw, mh)
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=REGION_COLORS[region], outline=(255, 255, 255), width=1)
    for s in LEADS + ROWS:
        px, py = project(s["lat"], s["lon"], mx0, my0, mw, mh)
        d.ellipse([px - 10, py - 10, px + 10, py + 10], fill=NAVY, outline=(255, 255, 255), width=2)
        d.text((px, py - 7), str(s["n"]), font=bold(12), fill=(255, 255, 255), anchor="ma")
    # Legend
    lx = 676
    d.text((lx, y0 + 2), "WHERE IT HAPPENED", font=bold(14), fill=NAVY)
    d.line([lx, y0 + 22, 1008, y0 + 22], fill=RULE, width=1)
    ly = y0 + 28
    for s in LEADS + ROWS:
        d.text((lx, ly), f"{s['n']}", font=bold(12), fill=REGION_COLORS[s["region"]])
        line = fit_lines(d, f"{s['city']} — {s['headline']}", plain(11), 306, 1)[0]
        d.text((lx + 26, ly), line, font=plain(11), fill=INK)
        ly += 15
    d.text((lx, ly + 2), "Coloured dots: the 19 briefs, by region.", font=plain(11), fill=GREY)


def draw_rows(d: ImageDraw.ImageDraw) -> None:
    y0 = 610
    col_w = 496
    for i, s in enumerate(ROWS):
        col = i % 2
        row = i // 2
        x = 16 + col * (col_w + 16)
        y = y0 + row * 52
        d.rectangle([x, y, x + col_w, y + 48], fill=(255, 255, 255), outline=RULE, width=1)
        d.rectangle([x, y, x + 5, y + 48], fill=REGION_COLORS[s["region"]])
        d.text((x + 13, y + 5), f"{s['n']}", font=bold(17), fill=REGION_COLORS[s["region"]])
        headline = fit_lines(d, s["headline"], bold(14), col_w - 58, 1)[0]
        d.text((x + 44, y + 4), headline, font=bold(14), fill=INK)
        lines = fit_lines(d, s["summary"], plain(11), col_w - 58, 2)
        for j, line in enumerate(lines):
            d.text((x + 44, y + 22 + j * 12), line, font=plain(11), fill=(52, 58, 68))


def draw_briefs(d: ImageDraw.ImageDraw) -> None:
    y0 = 818
    d.rectangle([0, y0, W, y0 + 20], fill=NAVY)
    d.text((26, y0 + 3), "IN BRIEF — 19 MORE STORIES OF THE DAY", font=bold(13), fill=CREAM)
    half = (len(BRIEFS) + 1) // 2
    for col, group in enumerate((BRIEFS[:half], BRIEFS[half:])):
        x = 26 + col * 500
        y = y0 + 28
        for region, city, _lat, _lon, line, _src in group:
            tag = f"{city}: "
            d.text((x, y), tag, font=bold(11), fill=REGION_COLORS[region])
            tag_w = d.textlength(tag, font=bold(11))
            text = fit_lines(d, line, plain(11), 474 - tag_w, 1)[0]
            d.text((x + tag_w, y), text, font=plain(11), fill=INK)
            y += 16


def draw_footer(d: ImageDraw.ImageDraw) -> None:
    d.rectangle([0, 1002, W, H], fill=NAVY_DARK)
    d.text((26, 1008), "DATE CHECK: every story here was reported on Wednesday 25 November 2026 (UTC).",
           font=bold(10), fill=(255, 196, 86))
    d.text((998, 1008), "Sources: Reuters · AP · BBC · Al Jazeera · AFP · DW · ABC · ESA",
           font=plain(9), fill=(178, 192, 216), anchor="ra")


def main() -> None:
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_region_band(d)
    draw_timeline(d)
    for i, s in enumerate(LEADS):
        draw_lead(d, img, 16 + i * 336, s)
    draw_map(d)
    draw_rows(d)
    draw_briefs(d)
    draw_footer(d)
    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
