# calm palette: navy backgrounds, cream text, gold accent, no red
NAVY1, NAVY2 = (6, 14, 34), (20, 44, 92)
BGS["navy"] = make_bg(NAVY1, NAVY2, 7)
CREAM = (246, 238, 220); SOFT = (170, 182, 205); ACC = GOLD
SHADOW = (0, 0, 0)
pct = lambda v: f"{v:.1f}%"
usd2 = lambda v: f"${v:,.2f}"
usd0 = lambda v: f"${v:,.0f}"

def small(img, s, y=1040, t=9, fill=SOFT):
    d = ImageDraw.Draw(img); d.text((W - 40, 40), s, font=F(28, "SemiBold"), fill=fill, anchor="ra", stroke_width=3, stroke_fill=(0, 0, 0))

def k_open(img, t, dur, a):
    k_photo(img, t, dur, a)
    small(img, "For education only. Not financial advice.")

def k_hero(img, t, dur, a):
    """THE key number of the video, with its source in small print"""
    d = ImageDraw.Draw(img)
    slide_text(img, (W / 2, 250), a["kicker"], 48, t, 0, fill=SOFT, w="Bold")
    p = ease((t - 0.2) / 1.2)
    v = a["from"] + (a["to"] - a["from"]) * p
    size = 300
    text(d, (W / 2, 500), usd0(v), size, fill=CREAM if p < 1 else ACC, stroke=8)
    if p >= 1: slide_text(img, (W / 2, 700), a["label"], 56, t, 1.4, fill=CREAM)
    slide_text(img, (W / 2, 800), a["src"], 30, t, 1.6, fill=SOFT, w="SemiBold")

def k_quarter(img, t, dur, a):
    d = ImageDraw.Draw(img)
    for row, (yr, col) in enumerate([("LAST YEAR", SOFT), ("THIS YEAR", ACC)]):
        y = 330 + row * 260
        slide_text(img, (330, y), yr, 44, t, row * 0.6, fill=col, anchor="lm")
        for i, m in enumerate(["JUL", "AUG", "SEP"]):
            card(img, 800 + i * 320, y, 270, 150, t, row * 0.6 + 0.15 + i * 0.15, (40, 70, 130) if row == 0 else (150, 112, 20), m)
    if t > 1.8: slide_text(img, (W / 2, 820), "AVERAGE vs AVERAGE  =  THE COLA", 54, t, 1.8, fill=CREAM)

def k_flow(img, t, dur, a):
    d = ImageDraw.Draw(img)
    card(img, 380, 470, 480, 220, t, 0, (40, 70, 130), "YOUR BENEFIT", "incl. the raise")
    card(img, 960, 470, 420, 220, t, 0.5, (110, 84, 20), "PART B", "taken out first")
    card(img, 1540, 470, 480, 220, t, 1.0, (30, 110, 80), "YOUR DEPOSIT", "what reaches the bank")
    for i in range(2):
        if t > 0.35 + i * 0.5:
            x = 640 + i * 560; d.polygon([(x, 440), (x + 50, 470), (x, 500)], fill=CREAM)
    slide_text(img, (W / 2, 760), "MOST MEDICARE ENROLLEES: DEDUCTED AUTOMATICALLY", 44, t, 1.4, fill=SOFT, w="Bold")

def k_split(img, t, dur, a):
    """$75 raise -> $6.60 peels off -> about $68 left (THE key number)"""
    d = ImageDraw.Draw(img)
    x0, x1, y = 260, 1660, 330
    full = x1 - x0; cut = full * 6.60 / 75
    p = ease((t - 0.8) / 0.8)
    d.rounded_rectangle([x0, y, x1 - cut, y + 110], 18, fill=(30, 110, 80))
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    ld.rounded_rectangle([x1 - cut, y + 140 * p, x1, y + 110 + 140 * p], 18, fill=(150, 112, 20, 255))
    img.alpha_composite(lay)
    text(d, (x0 + 30, y + 55), "$75 RAISE (AVERAGE)", 46, fill=CREAM, anchor="lm")
    if p > 0.5: slide_text(img, (x1 - cut / 2 - 40, y + 250), "-$6.60 PART B", 40, t, 1.3, fill=ACC)
    q = back((t - 2.0) / 0.5)
    if q > 0:
        pop_text(img, (W / 2 - 150, 730), "≈ $68", 220, t, 2.0, fill=ACC, stroke=8)
        slide_text(img, (W / 2 + 420, 730), "IN THE BANK", 60, t, 2.2, fill=CREAM)
    slide_text(img, (W / 2, 880), "Sources: SSA 2027 COLA; 2026 Medicare Trustees Report (projection)", 28, t, 2.4, fill=SOFT, w="SemiBold")

def k_comment2(img, t, dur, a):
    p = back(t / 0.45)
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    al = int(255 * clamp(p))
    ld.rounded_rectangle([340, 230, 1580, 720], 34, fill=CREAM + (al,))
    ld.text((W / 2, 320), "LAST YEAR'S RAISE...", font=F(56), fill=(15, 22, 45, al), anchor="mm")
    ld.rounded_rectangle([420, 450, 940, 640], 24, fill=(30, 110, 80, al))
    ld.text((680, 545), "IT REACHED ME", font=F(44), fill=(255, 255, 255, al), anchor="mm")
    ld.rounded_rectangle([980, 450, 1500, 640], 24, fill=(40, 70, 130, al))
    ld.text((1240, 545), "BILLS GOT THERE FIRST", font=F(38), fill=(255, 255, 255, al), anchor="mm")
    img.alpha_composite(lay)
    slide_text(img, (W / 2, 820), "TELL ME IN THE COMMENTS ↓", 56, t, 0.6, fill=ACC)

def shield(ld, cx, cy, s, col, al):
    pts = [(cx, cy - 200 * s), (cx + 170 * s, cy - 130 * s), (cx + 150 * s, cy + 80 * s), (cx, cy + 210 * s), (cx - 150 * s, cy + 80 * s), (cx - 170 * s, cy - 130 * s)]
    ld.polygon(pts, fill=col + (al,))

def k_shield(img, t, dur, a):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    p = back(t / 0.5)
    shield(ld, 520, 470, 1.2 * (0.6 + 0.4 * clamp(p)), (30, 110, 80), int(255 * clamp(p)))
    ld.line([(450, 470), (510, 540), (620, 390)], fill=(255, 255, 255, int(255 * clamp(p))), width=22)
    img.alpha_composite(lay)
    slide_text(img, (1250, 330), a.get("kicker", "THE RULE"), 44, t, 0.2, fill=SOFT, w="Bold")
    for i, ln in enumerate(a["lines"]):
        s_, col = (ln, CREAM) if isinstance(ln, str) else ln
        slide_text(img, (1250, 450 + i * 110), s_, fit(s_, 84, 950), t, 0.35 + i * 0.25, fill=col)

def k_tenth(img, t, dur, a):
    d = ImageDraw.Draw(img)
    cols = 10
    p = ease(t / 1.0)
    for i in range(cols):
        x = 360 + i * 120
        if p * cols > i:
            d.rounded_rectangle([x, 330, x + 100, 560], 14, fill=(30, 110, 80))
    q = ease((t - 1.1) / 0.6)
    if q > 0:
        w_ = 100 * 6.60 / 7.5   # $6.60 out of a $7.50 slice (one tenth of $75)
        d.rounded_rectangle([360, 330, 360 + w_, 560], 14, fill=(150, 112, 20))
        slide_text(img, (420, 620), "$6.60", 46, t, 1.2, fill=ACC)
    slide_text(img, (W / 2, 250), "AVERAGE RAISE ≈ $75 = 10 SLICES OF $7.50", 46, t, 0, fill=SOFT, w="Bold")
    slide_text(img, (W / 2, 760), "PROJECTED PREMIUM INCREASE: LESS THAN ONE SLICE", 52, t, 1.5, fill=CREAM)

def k_subscribe2(img, t, dur, a):
    d = ImageDraw.Draw(img)
    slide_text(img, (W / 2, 280), "WITHIN 10 YEARS OF RETIREMENT?", 64, t, 0, fill=CREAM)
    slide_text(img, (W / 2, 380), "MON · WED · FRI", 52, t, 0.3, fill=ACC)
    p = back((t - 0.6) / 0.4); clicked = t > 2.2
    if p > 0:
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay); sz = 0.6 + 0.4 * clamp(p)
        col = (60, 66, 84) if clicked else (30, 110, 80)
        ld.rounded_rectangle([W / 2 - 300 * sz, 580 - 80 * sz, W / 2 + 300 * sz, 580 + 80 * sz], 80, fill=col + (255,))
        ld.text((W / 2, 580), "SUBSCRIBED ✓" if clicked else "SUBSCRIBE", font=F(int(64 * sz)), fill=(255, 255, 255), anchor="mm")
        img.alpha_composite(lay)
    slide_text(img, (W / 2, 780), "MONEY UNDER FIRE", 48, t, 0.8, fill=SOFT)

def k_limits(img, t, dur, a):
    items = [("NEW TO PART B", "first year"), ("MEDICARE, NO SS YET", "premium paid directly"), ("HIGHER INCOMES", "pay IRMAA")]
    slide_text(img, (W / 2, 260), "NOT COVERED BY THE RULE", 56, t, 0, fill=ACC)
    for i, (h, s_) in enumerate(items):
        card(img, 400 + i * 560, 520, 500, 240, t, 0.3 + i * a.get("gap", 3.0), (40, 70, 130), h, s_)

def k_basket(img, t, dur, a):
    d = ImageDraw.Draw(img)
    for i, (h, items, col) in enumerate([("CPI-W TRACKS", ["prices paid by", "urban wage earners", "& clerical workers"], (40, 70, 130)),
                                          ("MANY RETIREES SPEND MORE ON", ["healthcare", "housing", "pharmacy"], (110, 84, 20))]):
        x = 560 + i * 800
        slide_text(img, (x, 280), h, 50, t, i * 1.2, fill=CREAM)
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
        p = ease((t - i * 1.2) / 0.5)
        if p > 0:
            ld.polygon([(x - 220, 400), (x + 220, 400), (x + 170, 700), (x - 170, 700)], fill=col + (int(230 * p),))
            ld.line([(x - 150, 400), (x - 60, 320), (x + 60, 320), (x + 150, 400)], fill=col + (int(255 * p),), width=14)
            img.alpha_composite(lay)
            for j, it in enumerate(items):
                slide_text(img, (x, 470 + j * 75), it, 40, t, i * 1.2 + 0.3 + j * 0.2, fill=(255, 255, 255), w="Bold")
    slide_text(img, (W / 2, 820), "NOT THE SAME SHOPPING BASKET", 54, t, 2.6, fill=ACC)

def k_notice(img, t, dur, a):
    """a generic one-page COLA notice (illustration, no real data) with one line highlighted"""
    hl = a.get("hl", -1)
    p = ease(t / 0.5) if a.get("anim", True) else 1
    x0, y0 = W / 2 - 430, 130 + 60 * (1 - p)
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    al = int(255 * p)
    ld.rounded_rectangle([x0 + 14, y0 + 18, x0 + 874, y0 + 760], 16, fill=(0, 0, 0, int(al * .4)))
    ld.rounded_rectangle([x0, y0, x0 + 860, y0 + 742], 16, fill=(250, 247, 238, al))
    ld.text((x0 + 60, y0 + 60), "YOUR NEW BENEFIT AMOUNT", font=F(40), fill=(20, 30, 60, al), anchor="lm")
    for k in range(3): ld.rounded_rectangle([x0 + 60, y0 + 120 + k * 34, x0 + 800 - k * 120, y0 + 136 + k * 34], 6, fill=(205, 205, 210, al))
    rows = [("Benefit before deductions", "$ ----"), ("Medicare deductions / taxes withheld", "- $ ---"), ("Amount you will receive", "$ ----")]
    for i, (lab, val) in enumerate(rows):
        y = y0 + 330 + i * 120
        if i == hl:
            ld.rounded_rectangle([x0 + 40, y - 48, x0 + 820, y + 48], 14, fill=(255, 214, 0, int(al * 0.85)))
        ld.text((x0 + 70, y), lab, font=F(34, "Bold"), fill=(20, 30, 60, al), anchor="lm")
        ld.text((x0 + 790, y), val, font=F(36), fill=(20, 30, 60, al), anchor="rm")
        if i == 1: ld.line([(x0 + 60, y + 60), (x0 + 800, y + 60)], fill=(20, 30, 60, al), width=3)
    ld.text((x0 + 430, y0 + 700), "ILLUSTRATION — NOT A REAL NOTICE", font=F(22, "SemiBold"), fill=(140, 140, 150, al), anchor="mm")
    img.alpha_composite(lay)
    if a.get("label"): slide_text(img, (W / 2, 950 - 70), a["label"], 1, t, 9)

def k_when(img, t, dur, a):
    card(img, 600, 450, 620, 260, t, 0, (30, 110, 80), "ONLINE", "late November · my Social Security")
    card(img, 1320, 450, 620, 260, t, a.get("gap", 4.5), (40, 70, 130), "BY MAIL", "December · unless paperless")


def k_pxcount(img, t, dur, a):
    """big number straight on a bright Pixabay photo (hook pattern)"""
    d = ImageDraw.Draw(img)
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).rectangle([0, 0, W, H], fill=(4, 10, 28, 95)); img.alpha_composite(lay)
    slide_text(img, (W / 2, 250), a["kicker"], 54, t, 0, fill=CREAM)
    p = ease(t / 0.9); s_ = a["fmt"](a["v"] * p)
    d = ImageDraw.Draw(img)
    text(d, (W / 2, 510), s_, 300, fill=ACC, stroke=12)
    if a.get("label"): slide_text(img, (W / 2, 720), a["label"], 60, t, 0.7, fill=CREAM)
    if a.get("src"): slide_text(img, (W / 2, 820), a["src"], 32, t, 0.9, fill=CREAM, w="SemiBold")
    if a.get("disc"): small(img, "For education only. Not financial advice.")

def k_compare2(img, t, dur, a):
    d = ImageDraw.Draw(img)
    for i, (name, val, lab, col) in enumerate([("YOUR RAISE", 2.8, "2.8%", (30, 110, 80)), ("PART B PREMIUM", 9.7, "+9.7%", (150, 112, 20))]):
        x = 640 + i * 640
        slide_text(img, (x, 830), name, 50, t, i * 0.3, fill=CREAM)
        p = ease((t - 0.3 - i * 0.3) / 0.9); h = max(6, 440 * val / 9.7 * p)
        d.rounded_rectangle([x - 130, 770 - h, x + 130, 770], 14, fill=col)
        if p > 0.2: slide_text(img, (x, 770 - h - 55), lab, 70, t, 0.5 + i * 0.3, fill=CREAM)
    pop_text(img, (W / 2, 520), "3X+", 150, t, 1.3, fill=ACC, stroke=8)
    slide_text(img, (W / 2, 120), "2026 · Sources: SSA, CMS", 28, t, 1.5, fill=SOFT, w="SemiBold")

