#!/usr/bin/env python3
"""Compose the front page for THE WORLD TODAY - Saturday 21 November 2026.

Renders a 1024x1024 PNG newspaper front page with PIL and real fonts.
Lead story: Russian missiles land in Poland. Secondary stories: the Wall
Street AI sell-off, Trump's data-centre tax threat, Cyclone Akvan.
Everything is drawn in code - no generated imagery, no network.
"""
import math
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1024, 1024
MARGIN = 38
CONTENT_W = W - 2 * MARGIN

PAPER = (247, 242, 231)
INK = (18, 18, 18)
RED = (178, 34, 28)
NAVY = (24, 38, 64)
GREY = (96, 92, 84)

SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SERIF_I = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centered(draw, y, text, fnt, fill, x0=0, x1=W):
    w = draw.textlength(text, font=fnt)
    draw.text(((x0 + x1 - w) / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size


def rule(draw, y, weight=2, fill=INK, x0=MARGIN, x1=W - MARGIN):
    draw.line([(x0, y), (x1, y)], fill=fill, width=weight)


def vgrad(size, top, bottom):
    """Vertical RGB gradient as an image."""
    w, h = size
    base = Image.new("RGB", (1, h))
    px = base.load()
    for yy in range(h):
        t = yy / max(1, h - 1)
        px[0, yy] = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
    return base.resize((w, h))


def draw_lead_scene():
    """Dusk over Polish farmland: a missile impact, smoke, NATO jets above.

    Layered: gradient sky -> horizon glow -> stars -> treeline -> fields
    -> road and crater -> smoke plume (many soft blurred blobs, not discs)
    -> jets and contrails. Built on separate layers and blurred so no hard
    vector edges survive at full size.
    """
    img_w, img_h = CONTENT_W, 320
    scene = Image.new("RGB", (img_w, img_h))
    horizon = int(img_h * 0.62)

    # --- sky: deep indigo at top warming to burnt orange at the horizon
    sky = vgrad((img_w, horizon + 2), (26, 34, 66), (214, 116, 52))
    scene.paste(sky, (0, 0))

    # low sun glow sitting on the horizon, left of centre: drawn on a
    # full-scene layer so no hard layer edge can ever show
    glow = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gx, gy = int(img_w * 0.36), horizon
    for i in range(30, 0, -1):
        t = i / 30
        r = int(430 * math.sqrt(t))
        alpha = int(150 * (1 - t) ** 1.8)
        gd.ellipse([gx - r, gy - int(r * 0.62), gx + r, gy + int(r * 0.62)],
                   fill=(255, 186, 108, alpha))
    glow = glow.filter(ImageFilter.GaussianBlur(22))
    scene.paste(glow, (0, 0), glow)

    # a few faint early stars in the upper sky
    rng = random.Random(21112026)
    stars = ImageDraw.Draw(scene)
    for _ in range(46):
        x = rng.randint(4, img_w - 4)
        y = rng.randint(4, int(horizon * 0.42))
        r = rng.choice([1, 1, 2])
        a = rng.randint(90, 210)
        stars.ellipse([x - r, y - r, x + r, y + r], fill=(a + 40, a + 40, a + 60))

    # --- distant treeline, dark and uneven
    tree = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
    td = ImageDraw.Draw(tree)
    x = -10
    while x < img_w + 10:
        tw = rng.randint(26, 60)
        th = rng.randint(8, 22)
        td.ellipse([x, horizon - th, x + tw, horizon + 4], fill=(30, 26, 40, 255))
        x += tw - rng.randint(8, 20)
    tree = tree.filter(ImageFilter.GaussianBlur(2.5))
    scene.paste(tree, (0, 0), tree)

    # --- fields: receding bands, darker toward the viewer
    bands = [
        (0.62, 0.70, (96, 74, 44)),
        (0.70, 0.79, (74, 62, 40)),
        (0.79, 0.89, (56, 50, 36)),
        (0.89, 1.00, (40, 38, 30)),
    ]
    fd = ImageDraw.Draw(scene)
    for (t0, t1, col) in bands:
        fd.rectangle([0, int(img_h * t0), img_w, int(img_h * t1)], fill=col)
    # faint furrow lines converging on the horizon for depth - kept very
    # subtle so they read as field texture, not rays
    for i in range(-4, 10):
        x0 = img_w * 0.5 + i * 110
        fd.line([(x0, horizon), (img_w * 0.5 + i * 40, img_h)],
                fill=(48, 44, 36), width=1)

    # --- dirt road sweeping from the lower left toward the impact site
    impact_x, impact_y = int(img_w * 0.68), int(img_h * 0.86)
    road = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
    rd = ImageDraw.Draw(road)
    rd.polygon(
        [(0, img_h), (120, img_h), (impact_x - 26, impact_y + 6),
         (impact_x + 10, impact_y - 4)],
        fill=(104, 86, 62, 255),
    )
    rd.line([(0, img_h), (impact_x - 26, impact_y + 6)], fill=(128, 108, 80, 255), width=2)
    rd.line([(120, img_h), (impact_x + 10, impact_y - 4)], fill=(128, 108, 80, 255), width=2)
    road = road.filter(ImageFilter.GaussianBlur(1.5))
    scene.paste(road, (0, 0), road)

    # --- impact crater: scorched ellipse with a hot orange heart
    crater = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
    cd = ImageDraw.Draw(crater)
    cd.ellipse([impact_x - 104, impact_y - 30, impact_x + 104, impact_y + 30],
               fill=(16, 12, 10, 235))
    cd.ellipse([impact_x - 70, impact_y - 19, impact_x + 70, impact_y + 19],
               fill=(34, 20, 12, 235))
    cd.ellipse([impact_x - 38, impact_y - 10, impact_x + 38, impact_y + 10],
               fill=(214, 96, 30, 220))
    cd.ellipse([impact_x - 17, impact_y - 5, impact_x + 17, impact_y + 5],
               fill=(255, 196, 90, 235))
    crater = crater.filter(ImageFilter.GaussianBlur(3))
    scene.paste(crater, (0, 0), crater)

    # scattered debris shards catching the firelight
    dd = ImageDraw.Draw(scene)
    for _ in range(14):
        dx = impact_x + rng.randint(-130, 130)
        dy = impact_y + rng.randint(-12, 24)
        s = rng.randint(2, 4)
        dd.polygon([(dx, dy), (dx + s, dy + 1), (dx + 1, dy + s)],
                   fill=(200, 160, 110))

    # --- smoke plume: many overlapping soft blobs, heavy blur, no discs.
    # Broad and dark at the base, widening and thinning as it rises and
    # drifts left, so the column reads as one continuous mass.
    smoke = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
    sd = ImageDraw.Draw(smoke)
    px, py = impact_x, impact_y - 10
    for step in range(60):
        t = step / 60
        drift = -70 * t * t + rng.randint(-10, 10)
        rise = 250 * t
        r = 16 + 58 * t + rng.randint(-5, 9)
        cx, cy = px + drift + rng.randint(-12, 12), py - rise
        shade = int(88 - 52 * t)
        warm = int(36 * (1 - t))
        sd.ellipse([cx - r, cy - r * 0.7, cx + r, cy + r * 0.7],
                   fill=(shade + warm, shade, shade - 6, rng.randint(120, 175)))
    smoke = smoke.filter(ImageFilter.GaussianBlur(20))
    scene.paste(smoke, (0, 0), smoke)
    # darker heart low in the plume so the column reads as one mass
    core = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
    cd2 = ImageDraw.Draw(core)
    cd2.ellipse([impact_x - 44, impact_y - 140, impact_x + 36, impact_y - 8],
                fill=(48, 40, 36, 170))
    core = core.filter(ImageFilter.GaussianBlur(16))
    scene.paste(core, (0, 0), core)

    # --- NATO jets high in the sky with thin contrails
    jets = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
    jd = ImageDraw.Draw(jets)
    for (jx, jy, s, flip) in [(int(img_w * 0.20), 52, 19, 1),
                              (int(img_w * 0.30), 86, 14, 1),
                              (int(img_w * 0.86), 46, 15, -1)]:
        jd.polygon([(jx - s, jy), (jx + s, jy - 3), (jx + s * 2, jy),
                    (jx + s, jy + 3)], fill=(12, 12, 16, 255))
        jd.polygon([(jx - s * 0.4, jy - 2), (jx + s * 0.2, jy - s * 0.75),
                    (jx + s * 0.5, jy - 2)], fill=(12, 12, 16, 255))
        jd.line([(jx - s * 2, jy + 1), (jx - s * 11, jy + 7)],
                fill=(235, 235, 235, 190), width=2)
    jets = jets.filter(ImageFilter.GaussianBlur(0.8))
    scene.paste(jets, (0, 0), jets)

    # gentle vignette so the panel sits inside the page
    vig = Image.new("L", (img_w, img_h), 0)
    vd = ImageDraw.Draw(vig)
    vd.rectangle([0, 0, img_w, img_h], fill=28)
    vd.rectangle([6, 6, img_w - 6, img_h - 6], fill=0)
    vig = vig.filter(ImageFilter.GaussianBlur(10))
    scene.paste(Image.new("RGB", (img_w, img_h), (10, 10, 14)), (0, 0), vig)
    return scene


def main():
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)

    # ---------- masthead ----------
    mast = font(SERIF_B, 92)
    bbox = d.textbbox((0, 0), "THE WORLD TODAY", font=mast)
    mw = bbox[2] - bbox[0]
    d.text(((W - mw) / 2, 26), "THE WORLD TODAY", font=mast, fill=INK)
    y = 26 + bbox[3] + 8
    rule(d, y, 3)
    rule(d, y + 6, 1)
    date_f = font(SANS_B, 29)
    y = centered(d, y + 16, "SATURDAY, 21 NOVEMBER 2026", date_f, RED) + 2
    rule(d, y + 8, 1)

    # ---------- lead kicker + headline ----------
    kick = font(SANS_B, 24)
    y = centered(d, y + 20, "NATO ON ALERT  •  WAR IN EUROPE", kick, RED) + 4
    head = font(SERIF_B, 66)
    y = centered(d, y + 2, "MISSILES FALL ON POLAND", head, INK)
    sub = font(SERIF_I, 25)
    sub_lines = wrap(
        d,
        "Russian cruise missiles land on NATO soil in a mass strike on Ukraine "
        "— Warsaw calls it a deliberate provocation.",
        sub, CONTENT_W - 40)
    for line in sub_lines:
        y = centered(d, y + 2, line, sub, (48, 48, 48))

    # ---------- lead illustration ----------
    scene = draw_lead_scene()
    img_y = y + 12
    page.paste(scene, (MARGIN, img_y))
    d.rectangle([MARGIN, img_y, MARGIN + CONTENT_W - 1, img_y + 319],
                outline=INK, width=2)
    cap = font(SERIF_I, 19)
    cap_lines = wrap(
        d,
        "Smoke rises over south-eastern Poland after Russian missiles came down "
        "near the Ukrainian border. NATO jets scrambled; no one was hurt.",
        cap, CONTENT_W)
    cy = img_y + 320 + 8
    for line in cap_lines:
        cy = centered(d, cy, line, cap, GREY)
    rule(d, cy + 10, 1)

    # ---------- three secondary stories ----------
    col_w = (CONTENT_W - 2 * 26) // 3
    stories = [
        ("MARKETS",
         "WALL STREET SLUMPS",
         "The S&P 500 slides into correction as Nvidia plunges 13% "
         "on an SEC probe."),
        ("WASHINGTON",
         "TRUMP: TAX ON AI CENTRES ABROAD",
         "US firms building data centres overseas face a ban or a "
         "“tremendous tax”."),
        ("INDIA",
         "CYCLONE AKVAN SPARES ODISHA",
         "372,000 evacuated as the storm hits the coast — "
         "no deaths, little damage."),
    ]
    top = cy + 20
    kick_f = font(SANS_B, 20)
    head_f = font(SERIF_B, 29)
    deck_f = font(SANS_R, 20)
    for i, (kicker, headline, deck) in enumerate(stories):
        x0 = MARGIN + i * (col_w + 26)
        d.text((x0, top), kicker, font=kick_f, fill=RED)
        hy = top + 30
        for line in wrap(d, headline, head_f, col_w):
            d.text((x0, hy), line, font=head_f, fill=INK)
            hy += 34
        dy = hy + 6
        for line in wrap(d, deck, deck_f, col_w):
            d.text((x0, dy), line, font=deck_f, fill=(52, 52, 52))
            dy += 25
        if i < 2:
            d.line([(x0 + col_w + 13, top), (x0 + col_w + 13, top + 178)],
                   fill=(190, 184, 172), width=1)

    # ---------- bottom ticker ----------
    band_y = H - 74
    d.rectangle([0, band_y, W, H], fill=NAVY)
    tick_text = ("ALSO TODAY:  MYANMAR CALLS ICJ GENOCIDE RULING “UNFAIR”   •   "
                 "UK AND EU SIGN FOOD AND CARBON DEALS")
    tick_size = 21
    while tick_size > 12:
        tick = font(SANS_B, tick_size)
        if d.textlength(tick_text, font=tick) <= W - 48:
            break
        tick_size -= 1
    tw = d.textlength(tick_text, font=tick)
    d.text(((W - tw) / 2, band_y + 12), tick_text, font=tick, fill=(240, 238, 230))
    foot = font(SANS_R, 15)
    foot_text = "THE WORLD TODAY — A SUMMARY OF SATURDAY 21 NOVEMBER 2026"
    fw = d.textlength(foot_text, font=foot)
    d.text(((W - fw) / 2, band_y + 44), foot_text, font=foot, fill=(170, 178, 198))

    # ---------- fine grain so flat areas do not band ----------
    noise = Image.effect_noise((W, H), 7).convert("L")
    page = Image.composite(
        Image.new("RGB", (W, H), (255, 255, 255)),
        page, noise.point(lambda v: int(v * 0.05)))

    page.save("entry.png", optimize=True)
    print("saved entry.png", page.size)


if __name__ == "__main__":
    main()
