#!/usr/bin/env python3
"""Draw the Friday 20 November 2026 front page (1024x1024, deterministic).

Fresh code written for round 3. Pillow + DejaVu fonts shipped in fonts/.
Every story is real news of 20 November 2026, researched before drawing;
see r3-plan.md in the make.fun working notes for the source of each fact.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
M = 16  # page margin

PAPER = (247, 241, 222)
INK = (26, 26, 26)
NAVY = (20, 38, 74)
NAVY2 = (30, 56, 104)
RED = (179, 39, 30)
RED_DK = (140, 28, 22)
TEAL = (15, 118, 110)
GREEN = (31, 122, 63)
GOLD = (198, 142, 32)
ORANGE = (224, 110, 30)
SKY = (178, 208, 224)
CREAM_DK = (232, 222, 196)
GREY = (90, 90, 88)
RULE = (120, 110, 88)

F_SERIF = os.path.join(HERE, "fonts", "DejaVuSerif.ttf")
F_SERIF_B = os.path.join(HERE, "fonts", "DejaVuSerif-Bold.ttf")
F_SANS = os.path.join(HERE, "fonts", "DejaVuSans.ttf")
F_SANS_B = os.path.join(HERE, "fonts", "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(d, x, y, lines, fnt, fill, leading):
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def text_w(fnt, text):
    return fnt.getlength(text)


def fit_headline(d, x, y, text, fnt, max_w, fill=INK):
    """Draw a headline, shrinking one step if it would overflow."""
    f = fnt
    while f.getlength(text) > max_w and f.size > 10:
        f = font(f.path, f.size - 1)
    d.text((x, y), text, font=f, fill=fill)
    return f.size


def tag(d, x, y, text, fill=GREY):
    """Small source + UTC stamp, e.g. 'REUTERS · 04:54 UTC'."""
    f = font(F_SANS_B, 8)
    d.text((x, y), text, font=f, fill=fill)
    return f


def rule(d, x, y, w, fill=RULE, width=1):
    d.line([(x, y), (x + w, y)], fill=fill, width=width)


def pin(d, cx, cy, n, r=9):
    """Red numbered map pin."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED, outline=(255, 255, 255), width=1)
    f = font(F_SANS_B, 10 if n < 10 else 9)
    t = str(n)
    d.text((cx - f.getlength(t) / 2, cy - 7 if n < 10 else cy - 6), t, font=f, fill=(255, 255, 255))


def burst(d, cx, cy, r, core, mid, edge):
    """Layered explosion burst: outer spikes + circles."""
    for k in range(10):
        a = k * math.pi / 5
        x2 = cx + math.cos(a) * r
        y2 = cy + math.sin(a) * r
        x3 = cx + math.cos(a + 0.22) * r * 0.55
        y3 = cy + math.sin(a + 0.22) * r * 0.55
        d.polygon([(cx, cy), (x2, y2), (x3, y3)], fill=edge)
    d.ellipse([cx - r * 0.62, cy - r * 0.62, cx + r * 0.62, cy + r * 0.62], fill=mid)
    d.ellipse([cx - r * 0.32, cy - r * 0.32, cx + r * 0.32, cy + r * 0.32], fill=core)


# ---------------------------------------------------------------- masthead
def draw_top(d):
    f_kick = font(F_SANS_B, 11)
    d.text((M, 12), "THE WORLD IN ONE DAY", font=f_kick, fill=INK)
    right = "FRIDAY'S NEWS  ·  ONE PAGE  ·  45 STORIES"
    d.text((W - M - f_kick.getlength(right), 12), right, font=f_kick, fill=INK)
    rule(d, M, 30, W - 2 * M, width=2)
    f_date = font(F_SERIF_B, 57)
    title = "Friday 20 November 2026"
    d.text(((W - f_date.getlength(title)) / 2, 36), title, font=f_date, fill=INK)
    f_dek = font(F_SERIF, 15)
    dek = "A cyclone comes ashore in India  ·  Kyiv hit overnight  ·  Climate talks reach their final day"
    d.text(((W - f_dek.getlength(dek)) / 2, 98), dek, font=f_dek, fill=RED)
    rule(d, M, 118, W - 2 * M, width=1)


# ---------------------------------------------------------------- ticker
TICKER = [
    ("300,000", "evacuated as Akvan lands"),
    ("$97.17", "Anthropic first close, +17%"),
    ("118", "Phillips century, Wellington"),
    ("51–48", "Senate rejects Iran curb"),
    ("24.6m", "GTA VI copies on day one"),
    ("$120bn", "COP31 adaptation cash at stake"),
]


def draw_ticker(d):
    y0, y1 = 126, 162
    cw = (W - 2 * M) / 6
    f_num = font(F_SANS_B, 25)
    f_lab = font(F_SANS, 8)
    for i, (num, lab) in enumerate(TICKER):
        x = M + i * cw
        d.text((x + 4, y0), num, font=f_num, fill=NAVY)
        for j, ln in enumerate(wrap(lab, f_lab, cw - 10)):
            d.text((x + 4, y0 + 28 + j * 10), ln, font=f_lab, fill=GREY)
        if i:
            d.line([(x, y0 + 2), (x, y1 - 4)], fill=RULE, width=1)
    rule(d, M, y1, W - 2 * M, width=2)


# ---------------------------------------------------------------- region strip
REGIONS = [
    ("EUROPE", 6, (15, 118, 110)),
    ("THE AMERICAS", 15, (179, 39, 30)),
    ("ASIA-PACIFIC", 8, (31, 122, 63)),
    ("MIDEAST", 6, (198, 142, 32)),
    ("AFRICA", 5, (140, 90, 30)),
    ("OCEANIA", 3, (30, 56, 104)),
    ("WORLD", 2, (90, 90, 88)),
]


def draw_regions(d):
    y = 170
    f = font(F_SANS_B, 10)
    x = M
    for name, n, col in REGIONS:
        label = f"{name} {n}"
        w = f.getlength(label) + 16
        d.rounded_rectangle([x, y, x + w, y + 17], radius=8, fill=col)
        d.text((x + 8, y + 3), label, font=f, fill=(255, 255, 255))
        x += w + 7
    total = "45 STORIES"
    d.text((W - M - f.getlength(total), y + 3), total, font=f, fill=INK)


# ---------------------------------------------------------------- UTC rail
RAIL = [
    ("00:56", "Phillips reaches his century"),
    ("02:00", "Akvan crosses the coast"),
    ("04:54", "Kyiv: three bridges hit"),
    ("05:05", "Cyber chief Cairncross fired"),
    ("05:53", "Asia sell-off deepens"),
]


def draw_rail(d):
    y0, y1 = 194, 214
    d.rectangle([M, y0, W - M, y1], fill=NAVY)
    f_h = font(F_SANS_B, 10)
    d.text((M + 8, y0 + 4), "THE DAY IN UTC", font=f_h, fill=(255, 210, 90))
    f_t = font(F_SANS_B, 9)
    f_x = font(F_SANS, 9)
    x = M + 118
    for t, txt in RAIL:
        d.text((x, y0 + 4), t, font=f_t, fill=(255, 255, 255))
        x += f_t.getlength(t) + 5
        d.text((x, y0 + 4), txt, font=f_x, fill=(200, 210, 225))
        x += f_x.getlength(txt) + 16
        if x > W - M - 60:
            break


# ---------------------------------------------------------------- lead art
def art_cyclone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    # sea bands
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(18, 64, 96))
    d.polygon([(x, y + h - 26), (x + w * 0.35, y + h - 38), (x + w * 0.7, y + h - 22),
               (x + w, y + h - 30), (x + w, y + h), (x, y + h)], fill=(24, 84, 120))
    cx, cy = x + w * 0.42, y + h * 0.46
    for k, (r, col, wd) in enumerate([
            (52, (255, 255, 255), 7), (40, (190, 215, 235), 6),
            (29, (255, 255, 255), 6), (18, (140, 180, 210), 5)]):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=200 + k * 55, end=200 + k * 55 + 250,
              fill=col, width=wd)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(255, 210, 90))
    # rain streaks
    for i in range(9):
        rx = x + 12 + i * 34
        d.line([(rx, y + 8), (rx - 6, y + 26)], fill=(150, 190, 215), width=2)
    # coast label, right-aligned inside the art
    f = font(F_SANS_B, 9)
    lab = "LANDFALL: GOPALPUR"
    d.text((x + w - f.getlength(lab) - 8, y + h - 16), lab, font=f, fill=(255, 255, 255))


def art_kyiv(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(28, 32, 52))
    # night sky band + smoke
    d.rectangle([x, y, x + w, y + 26], fill=(18, 22, 40))
    for i in range(7):
        sx = x + 20 + i * 44
        d.ellipse([sx, y + 6, sx + 34, y + 22], fill=(52, 56, 84))
    # buildings
    for bx, bw, bh in [(0, 46, 44), (52, 34, 60), (92, 52, 38), (150, 30, 52),
                       (186, 44, 40), (236, 36, 58), (278, 40, 34)]:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(12, 14, 26))
        for wy in range(int(y + h - bh + 6), int(y + h - 6), 12):
            for wx in range(int(x + bx + 5), int(x + bx + bw - 5), 12):
                if (wx + wy) % 24 == 0:
                    d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 190, 80))
    # big explosions filling the frame
    burst(d, x + w * 0.30, y + h * 0.42, 26, (255, 240, 180), (255, 150, 40), (224, 70, 20))
    burst(d, x + w * 0.72, y + h * 0.34, 32, (255, 244, 200), (255, 160, 50), (200, 60, 16))
    burst(d, x + w * 0.55, y + h * 0.62, 18, (255, 240, 180), (255, 150, 40), (224, 70, 20))
    # missile streaks
    d.line([(x + 30, y + 4), (x + 88, y + 52)], fill=(255, 220, 120), width=3)
    d.line([(x + w - 40, y + 2), (x + w - 96, y + 44)], fill=(255, 220, 120), width=3)


def art_cop31(d, x, y, w, h):
    # sky bands, sun, layered hills, flags - no empty sky
    bands = [(250, 214, 130), (244, 178, 90), (232, 140, 70), (214, 110, 80)]
    bh = h / 4
    for i, col in enumerate(bands):
        d.rectangle([x, y + i * bh, x + w, y + (i + 1) * bh], fill=col)
    d.ellipse([x + w * 0.60, y + 6, x + w * 0.60 + 44, y + 50], fill=(255, 236, 170))
    d.polygon([(x, y + h * 0.62), (x + w * 0.30, y + h * 0.42), (x + w * 0.62, y + h * 0.62),
               (x + w, y + h * 0.50), (x + w, y + h), (x, y + h)], fill=(46, 110, 74))
    d.polygon([(x, y + h * 0.78), (x + w * 0.25, y + h * 0.60), (x + w * 0.55, y + h * 0.78),
               (x + w, y + h * 0.66), (x + w, y + h), (x, y + h)], fill=(24, 78, 52))
    # flag poles + tiny flags on the ridge
    for fx in [0.18, 0.48, 0.78]:
        px = x + w * fx
        py = y + h * 0.60
        d.line([(px, py), (px, py - 26)], fill=(40, 40, 40), width=2)
        d.polygon([(px, py - 26), (px + 18, py - 21), (px, py - 16)], fill=RED)
    # globe
    d.ellipse([x + 10, y + h - 30, x + 34, y + h - 6], fill=(30, 90, 140))
    d.arc([x + 14, y + h - 28, x + 30, y + h - 8], start=20, end=200, fill=(120, 200, 120), width=2)


# ---------------------------------------------------------------- leads
LEADS = [
    dict(n=1, kick="ODISHA — STORM", art=art_cyclone,
         head="Akvan comes ashore in India",
         tag="IMD · 02:00 UTC",
         body="Severe Cyclone Akvan crosses the Andhra–Odisha coast near Gopalpur, with winds of 70–80 km/h gusting to 90. About 300,000 people were moved to safety."),
    dict(n=2, kick="KYIV — WAR", art=art_kyiv,
         head="Kyiv hit by overnight barrage",
         tag="REUTERS · 04:54 UTC",
         body="Russian ballistic missiles strike Kyiv from 01:25 local time. Three bridges over the Dnipro are damaged, three water workers are killed and about 15 people hurt."),
    dict(n=3, kick="ANTALYA — CLIMATE", art=art_cop31,
         head="COP31 reaches its final day",
         tag="REUTERS · 01:41 UTC",
         body="Negotiators face a Friday deadline as the draft drops fossil-fuel language and the $120bn adaptation target. Talks may run past midnight."),
]


def draw_leads(d):
    y0 = 222
    art_h = 92
    cw = (W - 2 * M - 16) / 3
    f_kick = font(F_SANS_B, 10)
    f_head = font(F_SERIF_B, 17)
    f_body = font(F_SANS, 10)
    for i, L in enumerate(LEADS):
        x = M + i * (cw + 8)
        L["art"](d, x, y0, cw, art_h)
        yy = y0 + art_h + 6
        d.text((x, yy), f"{L['n']} · {L['kick']}", font=f_kick, fill=RED)
        yy += 15
        for ln in wrap(L["head"], f_head, cw):
            d.text((x, yy), ln, font=f_head, fill=INK)
            yy += 20
        tag(d, x, yy + 1, L["tag"])
        yy += 14
        for ln in wrap(L["body"], f_body, cw):
            d.text((x, yy), ln, font=f_body, fill=INK)
            yy += 13
    return y0 + art_h + 6 + 15 + 40 + 14 + 52


# ---------------------------------------------------------------- panel art
def art_shenzhen(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 52, 90))
    fw = w / 3
    # US flag (stripes + blue canton)
    for s in range(5):
        d.rectangle([x, y + s * h / 5, x + fw, y + (s + 1) * h / 5],
                    fill=(178, 34, 34) if s % 2 == 0 else (255, 255, 255))
    d.rectangle([x, y, x + fw * 0.45, y + h * 0.45], fill=(30, 50, 110))
    # China flag
    d.rectangle([x + fw, y, x + 2 * fw, y + h], fill=(222, 40, 30))
    for sx, sy, r in [(0.25, 0.25, 5), (0.45, 0.2, 3), (0.5, 0.4, 3), (0.35, 0.5, 3)]:
        d.ellipse([x + fw + fw * sx - r, y + h * sy - r, x + fw + fw * sx + r, y + h * sy + r],
                  fill=(255, 220, 60))
    # Russia flag
    for i, col in enumerate([(255, 255, 255), (30, 80, 180), (200, 30, 30)]):
        d.rectangle([x + 2 * fw, y + i * h / 3, x + w, y + (i + 1) * h / 3], fill=col)
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(120, 85, 50))


def art_houthi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 20, 38))
    # dark sky band with stars
    for sx, sy in [(12, 8), (40, 14), (70, 6), (110, 12), (150, 7), (178, 14)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(255, 255, 255))
    # thick missile trails
    d.arc([x - 20, y - 30, x + 90, y + 60], start=300, end=30, fill=(255, 150, 40), width=6)
    d.arc([x + 60, y - 40, x + 200, y + 50], start=280, end=20, fill=(255, 190, 80), width=5)
    # PIF tower silhouette
    d.polygon([(x + 128, y + h), (x + 128, y + 22), (x + 142, y + 10), (x + 156, y + 22),
               (x + 156, y + h)], fill=(10, 12, 24))
    for wy in range(y + 26, y + h - 4, 9):
        d.rectangle([x + 134, wy, x + 150, wy + 4], fill=(255, 190, 80))
    burst(d, x + 142, y + 18, 14, (255, 240, 180), (255, 150, 40), (224, 70, 20))
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(8, 10, 20))


def art_senate(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    f_big = font(F_SANS_B, 30)
    d.text((x + 14, y + 10), "51", font=f_big, fill=(230, 70, 60))
    d.text((x + w - 62, y + 10), "48", font=f_big, fill=(120, 170, 230))
    d.rectangle([x + 12, y + h - 16, x + w - 12, y + h - 8], fill=(60, 80, 120))
    d.rectangle([x + 12, y + h - 16, x + 12 + (w - 24) * 51 // 99, y + h - 8], fill=(230, 70, 60))
    f = font(F_SANS_B, 8)
    d.text((x + 12, y + h - 26), "TO REJECT", font=f, fill=(255, 255, 255))


def art_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(36, 120, 58))
    d.rectangle([x + w * 0.42, y, x + w * 0.58, y + h], fill=(214, 186, 130))
    d.ellipse([x + 12, y + 8, x + 30, y + 26], fill=(255, 255, 255))
    d.line([(x + 18, y + 17), (x + 60, y + 44)], fill=(120, 70, 30), width=5)
    f_big = font(F_SANS_B, 26)
    d.text((x + w - 78, y + h - 34), "118", font=f_big, fill=(255, 255, 255))
    f = font(F_SANS_B, 8)
    d.text((x + 8, y + h - 14), "WELLINGTON", font=f, fill=(255, 255, 255))


def art_gta(d, x, y, w, h):
    bands = [(255, 170, 60), (250, 120, 90), (200, 80, 130), (120, 60, 140)]
    bh = h / 4
    for i, col in enumerate(bands):
        d.rectangle([x, y + i * bh, x + w, y + (i + 1) * bh], fill=col)
    d.ellipse([x + w * 0.62, y + 4, x + w * 0.62 + 34, y + 38], fill=(255, 240, 180))
    # palms
    for px in [0.14, 0.86]:
        bx = x + w * px
        d.line([(bx, y + h), (bx + 4, y + h * 0.45)], fill=(30, 20, 40), width=4)
        for a in range(5):
            ang = math.pi * (0.15 + a * 0.18)
            d.line([(bx + 4, y + h * 0.45),
                    (bx + 4 + math.cos(ang) * 22, y + h * 0.45 - math.sin(ang) * 12)],
                   fill=(30, 20, 40), width=3)
    f_big = font(F_SERIF_B, 26)
    d.text((x + w * 0.36, y + h - 32), "VI", font=f_big, fill=(255, 255, 255))


def art_asia(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(96, 16, 20))
    # falling bars
    vals = [0.55, 0.62, 0.48, 0.70, 0.58, 0.85, 0.95]
    bw = w / len(vals)
    for i, v in enumerate(vals):
        bh = h * v
        d.rectangle([x + i * bw + 3, y + h - bh, x + (i + 1) * bw - 3, y + h - 6],
                    fill=(200, 60, 50))
    pts = [(x + i * bw + bw / 2, y + h - h * v - 8) for i, v in enumerate(vals)]
    d.line(pts, fill=(255, 220, 90), width=3)
    f_big = font(F_SANS_B, 20)
    d.text((x + 8, y + 4), "–16%", font=f_big, fill=(255, 255, 255))


def art_eu(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 235, 215))
    # Union Jack (simplified)
    jx, jw = x + 6, w * 0.44
    d.rectangle([jx, y + 6, jx + jw, y + h - 6], fill=(30, 50, 120))
    d.line([(jx, y + 6), (jx + jw, y + h - 6)], fill=(255, 255, 255), width=5)
    d.line([(jx + jw, y + 6), (jx, y + h - 6)], fill=(255, 255, 255), width=5)
    d.line([(jx + jw / 2, y + 6), (jx + jw / 2, y + h - 6)], fill=(255, 255, 255), width=7)
    d.line([(jx, y + h / 2), (jx + jw, y + h / 2)], fill=(255, 255, 255), width=7)
    d.line([(jx + jw / 2, y + 6), (jx + jw / 2, y + h - 6)], fill=(200, 30, 30), width=3)
    d.line([(jx, y + h / 2), (jx + jw, y + h / 2)], fill=(200, 30, 30), width=3)
    # EU flag
    ex = x + w * 0.52
    d.rectangle([ex, y + 6, x + w - 6, y + h - 6], fill=(30, 50, 130))
    for k in range(9):
        a = k * 2 * math.pi / 9 - math.pi / 2
        sx = ex + (w * 0.44) / 2 + math.cos(a) * 14
        sy = y + h / 2 + math.sin(a) * 14
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 220, 60))


def art_cyber(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(22, 26, 34))
    # shield
    cx = x + w * 0.30
    d.polygon([(cx - 20, y + 8), (cx + 20, y + 8), (cx + 20, y + 30),
               (cx, y + h - 8), (cx - 20, y + 30)], outline=(90, 180, 120), width=3)
    d.line([(cx - 10, y + 28), (cx - 2, y + 38), (cx + 12, y + 20)], fill=(90, 220, 140), width=4)
    # FIRED stamp
    f = font(F_SANS_B, 15)
    d.rectangle([x + w * 0.52, y + 14, x + w - 8, y + 38], outline=RED, width=2)
    d.text((x + w * 0.52 + 6, y + 18), "FIRED", font=f, fill=(230, 70, 60))
    f2 = font(F_SANS, 8)
    d.text((x + w * 0.52, y + 42), "after a week of outages", font=f2, fill=(200, 205, 215))


def art_iran(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 60, 110))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(12, 44, 88))
    # tanker
    d.rectangle([x + 20, y + h * 0.52, x + w - 30, y + h * 0.68], fill=(16, 16, 20))
    d.rectangle([x + w - 62, y + h * 0.38, x + w - 44, y + h * 0.52], fill=(16, 16, 20))
    burst(d, x + w - 40, y + h * 0.30, 13, (255, 240, 180), (255, 150, 40), (224, 70, 20))
    f = font(F_SANS_B, 9)
    d.text((x + 8, y + 6), "STRAIT OF HORMUZ", font=f, fill=(255, 255, 255))


def art_anthropic(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 40, 32))
    # candlesticks: open 111.5, high 115, low 92.7, close 97.17
    data = [(0.30, 0.55, True), (0.45, 0.70, True), (0.62, 0.42, False),
            (0.50, 0.66, False), (0.58, 0.40, True)]
    bw = w / 6
    for i, (a, b, up) in enumerate(data):
        lo, hi = min(a, b), max(a, b)
        cx = x + bw * (i + 0.8)
        col = (70, 200, 120) if up else (220, 70, 60)
        d.line([(cx, y + h * (1 - hi)), (cx, y + h * (1 - lo))], fill=col, width=2)
        d.rectangle([cx - 6, y + h * (1 - hi) - 4, cx + 6, y + h * (1 - lo) + 4], fill=col)
    f_big = font(F_SANS_B, 19)
    d.text((x + 8, y + 4), "$97.17", font=f_big, fill=(255, 255, 255))
    f = font(F_SANS_B, 9)
    d.text((x + w - 52, y + h - 16), "+17%", font=f, fill=(90, 230, 140))


# ---------------------------------------------------------------- panels
PANELS = [
    dict(n=4, kick="SHENZHEN — DIPLOMACY", art=art_shenzhen,
         head="Trump, Xi and Putin sign ‘peace declaration’",
         tag="REUTERS · 01:46 UTC",
         body="First three-way summit ends with a four-point text. It says nuclear war must never be fought — and says nothing about Ukraine or Iran."),
    dict(n=5, kick="RIYADH — STRIKE", art=art_houthi,
         head="Houthi missile hits Riyadh’s tallest tower",
         tag="REUTERS · 19:27 UTC",
         body="Windows are blown out across seven floors of the PIF Tower, home of the Saudi wealth fund. No injuries are reported."),
    dict(n=6, kick="WASHINGTON — POLITICS", art=art_senate,
         head="Senate rejects Iran war-powers curb",
         tag="REUTERS · 19:42 UTC",
         body="The vote falls 51–48, largely along party lines. Collins, Murkowski and Paul back the curb; Fetterman is the lone Democrat against."),
    dict(n=7, kick="WELLINGTON — SPORT", art=art_cricket,
         head="Phillips makes history with 118",
         tag="IANS · 00:56 UTC",
         body="First to score centuries in all formats against India in one year. His 216-run stand with Nicholls lifts New Zealand to 317 for 6."),
    dict(n=8, kick="WORLD — GAMES", art=art_gta,
         head="GTA VI’s first full day breaks records",
         tag="SENSOR TOWER · 00:35 UTC",
         body="About 24.6m copies sold on day one, worth $2.36bn. Critics give it 99 on Metacritic — the highest score of the year."),
    dict(n=9, kick="TOKYO — MARKETS", art=art_asia,
         head="Asia’s AI sell-off deepens",
         tag="DOW JONES · 05:53 UTC",
         body="SoftBank plunges 16% intraday as investors doubt AI returns. The Nikkei falls 4.8%, the Kospi 4.6% and Taiwan’s Taiex 6.75%."),
    dict(n=10, kick="BRUSSELS — DIPLOMACY", art=art_eu,
         head="Britain and EU seek a ‘reset’",
         tag="AP · 07:00 UTC",
         body="Burnham meets EU leaders; deals on youth mobility and carbon are on the table."),
    dict(n=11, kick="WASHINGTON — TECH", art=art_cyber,
         head="White House fires cyber chief",
         tag="REUTERS · 05:05 UTC",
         body="Sean Cairncross is out after a week of outages hit air travel, banks and the NSA network. Pentagon CIO Kirsten Davies steps in."),
    dict(n=12, kick="WASHINGTON — IRAN", art=art_iran,
         head="Trump weighs an Iran strike",
         tag="SALALA TIMES · 01:03 UTC",
         body="The president weighs further military action as Hormuz tanker attacks intensify. Envoys report progress on Ukraine guarantees."),
    dict(n=13, kick="NEW YORK — MARKETS", art=art_anthropic,
         head="Anthropic ends first day up 17%",
         tag="NASDAQ · 21:00 UTC",
         body="The Claude maker opens at $111.50 and closes at $97.17, up 17% from its $83 IPO price, as the S&P 500 falls 2.02%."),
]


def draw_panels(d, y0):
    art_h = 56
    cw = (W - 2 * M - 4 * 8) / 5
    f_kick = font(F_SANS_B, 8)
    f_head = font(F_SERIF_B, 12)
    f_body = font(F_SANS, 9)
    row_h = 0
    for row in range(2):
        y = y0 + row * 150
        for col in range(5):
            P = PANELS[row * 5 + col]
            x = M + col * (cw + 8)
            P["art"](d, x, y, cw, art_h)
            yy = y + art_h + 4
            d.text((x, yy), f"{P['n']} · {P['kick']}", font=f_kick, fill=RED)
            yy += 12
            for ln in wrap(P["head"], f_head, cw):
                d.text((x, yy), ln, font=f_head, fill=INK)
                yy += 14
            tag(d, x, yy, P["tag"])
            yy += 11
            for ln in wrap(P["body"], f_body, cw):
                d.text((x, yy), ln, font=f_body, fill=INK)
                yy += 11
            row_h = max(row_h, yy - y)
        rule(d, M, y0 + row * 150 + 146, W - 2 * M)
    return y0 + 300


# ---------------------------------------------------------------- map + briefs
BRIEFS = [
    (14, "CINCINNATI — Dow −1,101 to 49,097; Nasdaq −2.3%."),
    (15, "TAIPEI — Taiex −6.75%; worst week since 1990."),
    (16, "NEW YORK — S&P 7,176; FTSE −0.93%; Brent $90.05."),
    (17, "YENNE — Dozens missing as migrant boat capsizes off Senegal."),
    (18, "SOUTH KORDOFAN — Drone strike kills 10 at Sudan gold mine."),
    (19, "CARACAS — US and Venezuela sign military cooperation deal."),
    (20, "DHAKA — Violence ahead of Hasina's planned return."),
    (21, "JURF AL-NASR — Iraq orders Iran-backed militia out."),
    (22, "COPENHAGEN — Denmark ratifies Greenland security deal."),
    (23, "YONGBYON — IAEA: North Korea expanding uranium enrichment."),
    (24, "MATO GROSSO — Brazil recognises Raoni ancestral land."),
    (25, "NEW YORK — UN secretary-general race stalls after 8 votes."),
    (26, "WASHINGTON — IMF: global debt will near 100% of GDP."),
    (27, "WASHINGTON — Senate passes energy permitting bill, 62–33."),
    (28, "TOKYO — Japan inflation rises; rate hike stays on track."),
    (29, "BRASÍLIA — Central bank sells $1bn to curb the dollar."),
    (30, "NAIROBI — Kenya discharges last Ebola patient, day 37."),
    (31, "MERCURY — BepiColombo reaches Mercury after eight years."),
    (32, "SUVA — Fiji and Tonga declare El Niño drought disasters."),
    (33, "WASHINGTON — Trump pardons late baseball star Pete Rose."),
    (34, "MARTISSANT — Haitian forces kill 34 suspected gang members."),
    (35, "KERCH — Third Ukrainian strike this week hits the bridge."),
    (36, "BERLIN — Allies meet; Europe ready to talk with Russia."),
    (37, "MRIMA HILL — US consortium wins Kenya minerals deal."),
    (38, "NAIROBI — Jepchirchir banned three years for doping."),
    (39, "GAZA — Israeli forces cross Yellow Line, first since truce."),
    (40, "HORMUZ — Tanker catches fire after hitting a mine."),
    (41, "SAN SALVADOR — Bukele registers for a third term."),
    (42, "AL-DAHI — Mosque set on fire in northern Israel."),
    (43, "HUNTSVILLE — Texas executes 70-year-old Reinaldo Dennes."),
    (44, "WELLINGTON — NZ 368 all out; Nicholls carries bat, 175*."),
    (45, "SHENZHEN — Philippines and Chile sign free trade deal."),
]

# pin positions inside the map box (x, y offsets)
PINS = {1: (228, 92), 2: (162, 42), 3: (162, 68), 4: (252, 92), 5: (192, 88),
        6: (48, 62), 7: (282, 162), 8: (56, 84), 9: (270, 66), 10: (146, 40),
        11: (74, 70), 12: (210, 98), 13: (64, 44)}


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    land = (38, 68, 118)
    # rough continents
    d.polygon([(x + 18, y + 28), (x + 70, y + 18), (x + 92, y + 40), (x + 78, y + 78),
               (x + 44, y + 92), (x + 22, y + 66)], fill=land)  # N America
    d.polygon([(x + 74, y + 104), (x + 100, y + 100), (x + 104, y + 138),
               (x + 88, y + 168), (x + 74, y + 140)], fill=land)  # S America
    d.polygon([(x + 138, y + 22), (x + 172, y + 16), (x + 182, y + 44),
               (x + 160, y + 62), (x + 140, y + 48)], fill=land)  # Europe
    d.polygon([(x + 142, y + 72), (x + 178, y + 66), (x + 190, y + 96),
               (x + 172, y + 138), (x + 150, y + 118)], fill=land)  # Africa
    d.polygon([(x + 186, y + 22), (x + 290, y + 18), (x + 292, y + 80),
               (x + 250, y + 108), (x + 210, y + 96), (x + 188, y + 58)], fill=land)  # Asia
    d.polygon([(x + 246, y + 128), (x + 282, y + 124), (x + 288, y + 146),
               (x + 258, y + 154)], fill=land)  # Australia
    # graticule
    for gx in range(x + 40, x + w, 40):
        d.line([(gx, y), (gx, y + h)], fill=(52, 82, 132), width=1)
    for gy in range(y + 30, y + h, 30):
        d.line([(x, gy), (x + w, gy)], fill=(52, 82, 132), width=1)
    for n, (px, py) in PINS.items():
        pin(d, x + px, y + py, n)
    f = font(F_SANS, 8)
    d.text((x + 4, y + h - 12), "Red numbers mark stories 1–13. Positions are approximate.",
           font=f, fill=(200, 210, 225))


def draw_briefs(d, x, y, w, h):
    f_h = font(F_SANS_B, 10)
    d.text((x, y), "ALSO ON FRIDAY 20 NOVEMBER — 32 MORE STORIES", font=f_h, fill=INK)
    rule(d, x, y + 15, w, width=1)
    f_n = font(F_SANS_B, 9)
    f_t = font(F_SANS, 9)
    col_w = (w - 12) / 2
    yy = y + 20
    for i, (n, txt) in enumerate(BRIEFS):
        col = i % 2
        row = i // 2
        bx = x + col * (col_w + 12)
        by = yy + row * 11
        d.text((bx, by), f"{n}.", font=f_n, fill=RED)
        d.text((bx + 18, by), txt, font=f_t, fill=INK)
    return yy + 16 * 11


# ---------------------------------------------------------------- date check + footer
def draw_datecheck(d, y):
    f_h = font(F_SANS_B, 10)
    f_t = font(F_SANS, 9)
    box_h = 38
    d.rectangle([M, y, W - M, y + box_h], outline=RED, width=2)
    d.text((M + 8, y + 4), "DATE CHECK — first reported 19 Nov or earlier, so NOT on this page:",
           font=f_h, fill=RED)
    line1 = ("ICJ Rohingya genocide ruling (19 Nov)  ·  Kyiv drone attack on embassies (19 Nov)  ·  "
             "Anthropic $83 pricing (19 Nov)")
    line2 = ("GTA VI midnight unlock (19 Nov)  ·  COP31 revised draft published (19 Nov)  ·  "
             "Jeffries (18 Nov)")
    d.text((M + 8, y + 18), line1, font=f_t, fill=INK)
    d.text((M + 8, y + 29), line2, font=f_t, fill=INK)
    return y + box_h


def draw_footer(d, y):
    f = font(F_SANS, 9)
    txt = ("Every story here happened, or was first reported, on Friday 20 November 2026.  "
           "Sources: Reuters, AP, AFP, BBC, The Hindu, IMD, IANS, Sensor Tower, Dow Jones, One Turn.")
    d.text(((W - f.getlength(txt)) / 2, y), txt, font=f, fill=GREY)


# ---------------------------------------------------------------- main
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_top(d)
    draw_ticker(d)
    draw_regions(d)
    draw_rail(d)
    leads_end = draw_leads(d)
    panels_end = draw_panels(d, leads_end + 6)
    y = panels_end + 6
    d.text((M, y), "WHERE IT HAPPENED", font=font(F_SANS_B, 10), fill=INK)
    draw_map(d, M, y + 16, 300, 176)
    bx = M + 316
    draw_briefs(d, bx, y, W - M - bx, 200)
    y2 = y + 16 + 176 + 8
    y3 = draw_datecheck(d, y2)
    draw_footer(d, y3 + 6)
    img.save(os.path.join(HERE, "entry.png"))
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
