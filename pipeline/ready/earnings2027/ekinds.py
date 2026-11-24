# Story-specific kinds for the 2027 earnings-test video (Linda & Harold). exec'd from scenes.py after common_kinds.py
TEAL = (30, 120, 86); STEELC = (40, 70, 130); AMBER = (170, 120, 20); GREY = (88, 98, 124); WARN = (214, 120, 40)
PAPER = (250, 247, 240); INKD = (24, 30, 48)

def lay_():
    l = Image.new("RGBA", (W, H), (0, 0, 0, 0)); return l, ImageDraw.Draw(l)

def src(img, s, t=9):
    """source line top-right on every info visual"""
    d = ImageDraw.Draw(img)
    d.text((W - 40, 40), s, font=F(26, "SemiBold"), fill=SOFT, anchor="ra", stroke_width=3, stroke_fill=(0, 0, 0))

def fiction(img):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([40, 30, 470, 82], 26, fill=(0, 0, 0, 160) if False else (20, 26, 44))
    d.text((255, 56), "ILLUSTRATIVE EXAMPLE", font=F(28, "Bold"), fill=SOFT, anchor="mm")

# ---------- 1. phone with a generic bank app: deposits, Social Security missing ----------
def phone(img, cx, cy, s, t, rows, title="CHECKING ••4821", stamp=None):
    p = back(t / 0.45); sc_ = (0.85 + 0.15 * clamp(p)) * s
    w, h = int(640 * sc_), int(1000 * sc_); x0, y0 = int(cx - w / 2), int(cy - h / 2 + 40 * (1 - clamp(p)))
    l, d = lay_(); al = int(255 * clamp(p * 1.3))
    d.rounded_rectangle([x0 + 14, y0 + 20, x0 + w + 14, y0 + h + 20], int(70 * sc_), fill=(0, 0, 0, int(al * .5)))
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], int(70 * sc_), fill=(18, 18, 22, al))
    m = int(18 * sc_)
    d.rounded_rectangle([x0 + m, y0 + m, x0 + w - m, y0 + h - m], int(56 * sc_), fill=(244, 246, 250, al))
    d.rounded_rectangle([cx - 70 * sc_, y0 + m + 14 * sc_, cx + 70 * sc_, y0 + m + 44 * sc_], int(15 * sc_), fill=(18, 18, 22, al))
    d.text((x0 + 60 * sc_, y0 + 120 * sc_), title, font=F(int(30 * sc_), "Bold"), fill=(90, 98, 120, al), anchor="lm")
    d.text((x0 + 60 * sc_, y0 + 175 * sc_), "Recent activity", font=F(int(44 * sc_), "Black"), fill=INKD + (al,), anchor="lm")
    for i, (date, lab, amt, col, dl) in enumerate(rows):
        q = ease((t - dl) / 0.3)
        if q <= 0: continue
        y = y0 + (270 + i * 132) * sc_; a2 = int(al * q)
        d.rounded_rectangle([x0 + 40 * sc_, y - 52 * sc_, x0 + w - 40 * sc_, y + 52 * sc_], int(22 * sc_), fill=(255, 255, 255, a2), outline=(225, 228, 236, a2), width=2)
        d.text((x0 + 70 * sc_, y - 16 * sc_), lab, font=F(int(27 * sc_), "Bold"), fill=INKD + (a2,), anchor="lm")
        d.text((x0 + 70 * sc_, y + 22 * sc_), date, font=F(int(24 * sc_), "SemiBold"), fill=(120, 128, 150, a2), anchor="lm")
        d.text((x0 + w - 70 * sc_, y), amt, font=F(int(30 * sc_), "Black"), fill=col + (a2,), anchor="rm")
    img.alpha_composite(l)
    if stamp and t > stamp[1]:
        q = back((t - stamp[1]) / 0.3); l2, d2 = lay_()
        f = F(int(64 * sc_ * (1.4 - 0.4 * clamp(q))))
        tw = f.getlength(stamp[0]); cy2 = y0 + h * 0.80
        d2.rounded_rectangle([cx - tw / 2 - 30, cy2 - 55, cx + tw / 2 + 30, cy2 + 55], 18, outline=WARN + (int(255 * clamp(q)),), width=10)
        d2.text((cx, cy2), stamp[0], font=f, fill=WARN + (int(255 * clamp(q)),), anchor="mm")
        img.alpha_composite(l2.rotate(-8, center=(cx, cy2)))

def k_bankapp(img, t, dur, a):
    rows = a["rows"]; phone(img, a.get("x", 1420), 470, 0.86, t, rows, stamp=a.get("stamp"))
    for i, ln in enumerate(a.get("lines", [])):
        s_, col = (ln, CREAM) if isinstance(ln, str) else ln
        slide_text(img, (130, 330 + i * 120), s_, fit(s_, a.get("size", 80), 1000), t, 0.3 + i * 0.35, fill=col, anchor="lm")
    if a.get("fic"): fiction(img)

# ---------- 2. the year as 12 check tiles: held vs paid ----------
MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
def k_year(img, t, dur, a):
    held = a.get("held", 4); amt = a.get("amt", "$1,400")
    slide_text(img, (W / 2, 120), a.get("title", "LINDA'S 2027 CHECKS"), 58, t, 0, fill=CREAM)
    for i, m in enumerate(MONTHS):
        r, c = divmod(i, 6); cx = 330 + c * 252; cy = 330 + r * 290
        dl = 0.15 + i * 0.07; p = back((t - dl) / 0.3)
        if p <= 0: continue
        l, d = lay_(); s = 0.75 + 0.25 * clamp(p); al = int(255 * clamp(p * 1.3))
        isheld = i < held and t > a.get("dh", 1.4) + i * 0.25
        col = (120, 54, 30) if isheld else (34, 92, 70)
        d.rounded_rectangle([cx - 110 * s, cy - 120 * s, cx + 110 * s, cy + 120 * s], 22, fill=col + (al,))
        d.text((cx, cy - 82 * s), "CHECK FOR", font=F(int(22 * s), "SemiBold"), fill=SOFT + (al,), anchor="mm")
        d.text((cx, cy - 35 * s), m, font=F(int(54 * s)), fill=CREAM + (al,), anchor="mm")
        d.text((cx, cy + 45 * s), "HELD" if isheld else amt, font=F(int((52 if isheld else 44) * s)), fill=(GOLD if isheld else CREAM) + (al,), anchor="mm")
        img.alpha_composite(l)
    if a.get("foot") and t > a.get("df", 2.6): slide_text(img, (W / 2, 830), a["foot"], 46, t, a.get("df", 2.6), fill=GOLD)
    src(img, "Rules: SSA 2027 fact sheet · SSA Pub. 05-10069")
    if a.get("fic"): fiction(img)

# ---------- 3. earnings bar with the $25,560 line ----------
def k_limitbar(img, t, dur, a):
    d = ImageDraw.Draw(img)
    x0, x1, y, hh = 200, 1720, 470, 130; mx = a.get("max", 40000)
    X = lambda v: x0 + (x1 - x0) * v / mx
    slide_text(img, (W / 2, 140), a.get("title", "LINDA'S 2027 EARNINGS FROM WORK"), 54, t, 0, fill=CREAM)
    d.rounded_rectangle([x0, y, x1, y + hh], 24, fill=(26, 34, 58))
    earn = a["earn"]; lim = 25560
    p = ease((t - 0.3) / 1.4); v = earn * p
    d.rounded_rectangle([x0, y, X(min(v, lim)), y + hh], 24, fill=TEAL)
    if v > lim: d.rounded_rectangle([X(lim), y, X(v), y + hh], 24, fill=WARN)
    text(d, (x0 + 30, y + hh / 2), f"${v:,.0f}", 60, fill=CREAM, anchor="lm", stroke=5)
    # limit line
    q = ease((t - 0.1) / 0.4)
    d.line([(X(lim), y - 90), (X(lim), y + hh + 30)], fill=GOLD + (0,) if q == 0 else GOLD, width=8)
    text(d, (X(lim), y - 130), "2027 LIMIT  $25,560", 46, fill=GOLD)
    if p >= 1:
        slide_text(img, ((X(lim) + X(earn)) / 2, y + hh + 90), f"${earn - lim:,.0f} OVER", 58, t, 1.8, fill=WARN)
        if a.get("half"):
            pop_text(img, (W / 2, 820), f"÷ 2  =  ${(earn - lim) / 2:,.0f} HELD BACK", 90, t, 2.6, fill=GOLD, stroke=6)
    src(img, "SSA 2027 fact sheet: $1 withheld for every $2 above $25,560")
    if a.get("fic"): fiction(img)

# ---------- 4. one dollar splits: 50c you keep, 50c held ----------
def bill(l, d, cx, cy, w, h, lab, col, al):
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], 20, fill=col + (al,), outline=(255, 255, 255, int(al * .6)), width=5)
    d.ellipse([cx - h * .32, cy - h * .32, cx + h * .32, cy + h * .32], outline=(255, 255, 255, int(al * .5)), width=5)
    d.text((cx, cy), lab, font=F(int(h * 0.42)), fill=(255, 255, 255, al), anchor="mm")
def k_dollar(img, t, dur, a):
    """CORRECT picture: the wage dollar is all hers; the 50c comes out of her Social Security benefit"""
    slide_text(img, (W / 2, 140), "EVERY $1 EARNED ABOVE $25,560", 60, t, 0, fill=CREAM)
    l, d = lay_(); p1 = back(t / 0.4); al = int(255 * clamp(p1))
    # left: the paycheck dollar stays whole
    bill(l, d, 560, 440, 420, 220, "$1", (34, 110, 70), al)
    img.alpha_composite(l)
    slide_text(img, (560, 620), "HER WAGE: SHE KEEPS ALL OF IT", 40, t, 0.4, fill=(120, 220, 160))
    # right: the Social Security benefit loses 50c
    p2 = back((t - 1.0) / 0.4)
    if p2 > 0:
        l2, d2 = lay_(); a2 = int(255 * clamp(p2))
        check(l2, d2, 1360, 440, 0.95, a2, amt="$1,400.00", month="SOCIAL SECURITY")
        img.alpha_composite(l2)
    if t > 1.6:
        pop_text(img, (1360, 620), "−50¢", 110, t, 1.6, fill=WARN, stroke=8)
        slide_text(img, (1360, 720), "HELD FROM HER BENEFIT", 40, t, 1.8, fill=GOLD)
    if t > 2.4: slide_text(img, (W / 2, 840), "$1 OF BENEFITS HELD FOR EVERY $2 OVER", 50, t, 2.4, fill=CREAM)
    src(img, "SSA 2027 fact sheet · under full retirement age")

# ---------- 5. four checks into the 'held' folder ----------
def check(l, d, cx, cy, s, al, amt="$1,400.00", month=""):
    w, h = 520 * s, 230 * s
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], 16, fill=PAPER + (al,), outline=(190, 180, 150, al), width=3)
    d.rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy - h / 2 + 34 * s], fill=(86, 120, 170, al))
    d.text((cx - w / 2 + 24 * s, cy - 30 * s), month if " " in month else f"BENEFIT FOR {month}", font=F(int(26 * s), "Bold"), fill=INKD + (al,), anchor="lm")
    d.text((cx + w / 2 - 24 * s, cy + 20 * s), amt, font=F(int(46 * s)), fill=INKD + (al,), anchor="rm")
    d.line([(cx - w / 2 + 24 * s, cy + 70 * s), (cx + 40 * s, cy + 70 * s)], fill=(160, 150, 130, al), width=3)
def k_held(img, t, dur, a):
    d0 = ImageDraw.Draw(img)
    slide_text(img, (W / 2, 120), "$5,000 TO HOLD BACK · THEY STOP WHOLE CHECKS", 46, t, 0, fill=CREAM)
    # folder
    fx, fy = 1450, 520; l, d = lay_()
    d.rounded_rectangle([fx - 300, fy - 210, fx + 300, fy + 230], 30, fill=(120, 54, 30, 255))
    d.rounded_rectangle([fx - 300, fy - 250, fx - 60, fy - 190], 20, fill=(120, 54, 30, 255))
    d.text((fx, fy + 150), "HELD", font=F(90), fill=GOLD + (255,), anchor="mm")
    img.alpha_composite(l)
    total = 0
    for i, m in enumerate(["JAN", "FEB", "MAR", "APR"]):
        dl = a.get("d0", 0.4) + i * 0.6; p = ease((t - dl) / 0.55)
        if t < dl:
            l, d = lay_(); check(l, d, 480, 300 + i * 150, 0.8, 255, month=m); img.alpha_composite(l); continue
        x = 480 + (fx - 480) * p; y = 300 + i * 150 + (fy - 60 - (300 + i * 150)) * p; s = 0.8 - 0.25 * p
        l, d = lay_(); check(l, d, x, y, s, int(255 * (1 - 0.6 * p)), month=m); img.alpha_composite(l)
        if p >= 1: total += 1400
    if total: text(d0, (fx, fy - 40), f"${total:,}", 96, fill=CREAM, stroke=6)
    if t > a.get("d0", 0.4) + 2.8: slide_text(img, (W / 2, 850), "$5,600 HELD  ·  EXTRA $600 PAID BACK THE NEXT YEAR", 44, t, a.get("d0", 0.4) + 2.8, fill=GOLD)
    src(img, "Method: SSA Pub. 05-10069 examples")
    fiction(img)

# ---------- 6. what counts / what doesn't ----------
def k_counts(img, t, dur, a):
    yes = ["Wages", "Bonuses", "Commissions", "Vacation pay", "Self-employment profit"]
    no = ["Pensions", "Annuities", "Investment income", "Interest", "Capital gains", "Veterans / govt. retirement"]
    l0, d0 = lay_()
    for cx, head, col in [(510, "COUNTS", WARN), (1410, "DOESN'T COUNT", TEAL)]:
        d0.rounded_rectangle([cx - 400, 150, cx + 400, 880], 30, fill=(14, 20, 38, 220))
        d0.rounded_rectangle([cx - 400, 150, cx + 400, 250], 30, fill=col + (255,))
        d0.text((cx, 200), head, font=F(56), fill=CREAM + (255,), anchor="mm")
    img.alpha_composite(l0)
    for i, s_ in enumerate(yes):
        slide_text(img, (160, 320 + i * 110), "✓  " + s_, 50, t, 0.3 + i * a.get("gap", 0.25), fill=CREAM, anchor="lm", w="Bold")
    for i, s_ in enumerate(no):
        dl = a.get("dno", 1.6) + i * a.get("gap", 0.25)
        slide_text(img, (1060, 320 + i * 95), "×  " + s_, 46, t, dl, fill=CREAM, anchor="lm", w="Bold")
    src(img, "SSA: Receiving Benefits While Working · Pub. 05-10069")

# ---------- 7. Linda vs Harold ----------
def person(d, cx, cy, s, col, al):
    d.ellipse([cx - 70 * s, cy - 210 * s, cx + 70 * s, cy - 70 * s], fill=col + (al,))
    d.rounded_rectangle([cx - 130 * s, cy - 50 * s, cx + 130 * s, cy + 170 * s], int(70 * s), fill=col + (al,))
def k_vs(img, t, dur, a):
    for i, (nm, age, inc, res, col, rc) in enumerate([
            ("LINDA", "63 · claimed early", "Part-time job $35,560", "4 CHECKS HELD", (70, 110, 170), WARN),
            ("HAROLD", "63 · claimed early", "Pension + investments", "0 CHECKS HELD", (110, 100, 80), (120, 220, 160))]):
        cx = 560 + i * 800; dl = i * a.get("d2", 0.8); p = back((t - dl) / 0.4)
        if p <= 0: continue
        l, d = lay_(); al = int(255 * clamp(p))
        d.rounded_rectangle([cx - 330, 140, cx + 330, 870], 34, fill=(14, 20, 38, int(al * .88)))
        pp = os.path.join(ROOT, "px", ("linda_sq" if i == 0 else "harold_sq") + ".jpg")
        if os.path.exists(pp):
            ph = Image.open(pp).convert("RGB").resize((380, 380), Image.LANCZOS); mk = Image.new("L", (380, 380), 0)
            ImageDraw.Draw(mk).rounded_rectangle([0, 0, 380, 380], 40, fill=al); l.paste(ph, (int(cx - 190), 175), mk)
        else: person(d, cx, 420, 0.9, col, al)
        d.text((cx, 610), nm, font=F(70), fill=CREAM + (al,), anchor="mm")
        d.text((cx, 660), age, font=F(32, "SemiBold"), fill=SOFT + (al,), anchor="mm")
        d.text((cx, 730), inc, font=F(fit(inc, 42, 600, "Bold"), "Bold"), fill=CREAM + (al,), anchor="mm")
        img.alpha_composite(l)
        if t > dl + a.get("dr", 1.2): pop_text(img, (cx, 810), res, 58, t, dl + a.get("dr", 1.2), fill=rc, stroke=5)
    fiction(img)

# ---------- 8. the 14-year payback ----------
def k_payback(img, t, dur, a):
    d = ImageDraw.Draw(img)
    slide_text(img, (W / 2, 120), "SSA'S OWN EXAMPLE: 12 CHECKS HELD", 52, t, 0, fill=CREAM)
    card(img, 520, 330, 560, 200, t, 0.2, STEELC, "$910  →  $975", "a month at full retirement age")
    card(img, 1400, 330, 560, 200, t, 0.6, (120, 54, 30), "$10,920", "12 checks held (12 × $910)")
    x0, x1, y = 200, 1720, 620
    d.rounded_rectangle([x0, y, x1, y + 70], 35, fill=(26, 34, 58))
    p = ease((t - a.get("fs", 1.4)) / max(1.0, a.get("fill", 3.0)))
    d.rounded_rectangle([x0, y, x0 + max(70, (x1 - x0) * p), y + 70], 35, fill=TEAL)
    for k in range(0, 15, 2):
        x = x0 + (x1 - x0) * k / 14; text(d, (x, y + 115), f"{k}", 34, fill=SOFT, w="Bold")
    text(d, (x0 - 10, y + 165), "YEARS", 28, fill=SOFT, w="Bold", anchor="lm")
    yrs = 14 * p
    text(d, (x0 + max(70, (x1 - x0) * p), y - 50), f"+$65/mo · {yrs:4.1f} yrs", 44, fill=CREAM, anchor="rm" if p > 0.4 else "lm")
    if p >= 1: pop_text(img, (W / 2, 850), "≈ 14 YEARS TO EARN IT BACK", 76, t, a.get("fs", 1.4) + a.get("fill", 3.0), fill=GOLD, stroke=6)
    src(img, "SSA Pub. 05-10069 · our math, today's dollars")

# ---------- 9. the age line: two limits, then none ----------
def k_ages(img, t, dur, a):
    d = ImageDraw.Draw(img)
    x0, x1, y = 180, 1740, 560
    segs = [(0.0, 0.50, (120, 54, 30), "BEFORE THE FRA YEAR", "$25,560", "$1 held per $2 over"),
            (0.50, 0.76, AMBER, "YEAR YOU REACH 67", "$67,920", "$1 per $3 · months before"),
            (0.76, 1.0, TEAL, "FROM THAT MONTH", "NO LIMIT", "")]
    for i, (s0, s1, col, lab, big, sub) in enumerate(segs):
        dl = a.get("d", [0.2, 1.2, 2.4])[i]; p = ease((t - dl) / 0.5)
        if p <= 0: continue
        xa = x0 + (x1 - x0) * s0; xb = xa + (x1 - x0) * (s1 - s0) * p
        d.rounded_rectangle([xa + 4, y, xb - 4, y + 90], 22, fill=col)
        cx = (x0 + (x1 - x0) * s0 + x0 + (x1 - x0) * s1) / 2
        if p > 0.6:
            slide_text(img, (cx, y - 230), lab, 30 if i else 38, t, dl + 0.2, fill=SOFT, w="Bold")
            slide_text(img, (cx, y - 150), big, 72 if i < 2 else 60, t, dl + 0.3, fill=GOLD if i < 2 else (120, 220, 160))
            if sub: slide_text(img, (cx, y - 80), sub, 30 if i else 36, t, dl + 0.4, fill=CREAM, w="SemiBold")
    for lab, s0 in [("63", 0.0), ("67", 0.76)]:
        text(d, (x0 + (x1 - x0) * s0 + (30 if s0 == 0 else 0), y + 150), "AGE " + lab, 40, fill=CREAM)
    src(img, "SSA 2027 fact sheet · FRA 67 for almost everyone born 1960+")

# ---------- 10. first-year rule: one month calendar ----------
def k_firstyear(img, t, dur, a):
    d = ImageDraw.Draw(img)
    slide_text(img, (W / 2, 130), "FIRST-YEAR RULE · ANY WHOLE MONTH YOU'RE 'RETIRED'", 46, t, 0, fill=CREAM)
    for i, m in enumerate(MONTHS):
        cx = 180 + i * 142; dl = 0.2 + i * 0.05; p = back((t - dl) / 0.3)
        if p <= 0: continue
        retired = i >= 10
        col = (34, 92, 70) if retired and t > 1.4 else (40, 48, 74)
        d.rounded_rectangle([cx - 62, 330, cx + 62, 500], 16, fill=col)
        text(d, (cx, 380), m, 34, fill=CREAM)
        text(d, (cx, 450), "FULL" if retired and t > 1.4 else "work", 30 if retired else 26, fill=GOLD if retired and t > 1.4 else SOFT, w="Bold")
    slide_text(img, (W / 2, 640), "EARN $2,130 OR LESS THAT MONTH", 72, t, a.get("dt", 1.8), fill=GOLD)
    slide_text(img, (W / 2, 740), "= A FULL CHECK FOR THAT MONTH (2027)", 48, t, a.get("dt", 1.8) + 0.4, fill=CREAM)
    src(img, "SSA Pub. 05-10069 · SSA 2027 fact sheet ($2,130/mo)")

# ---------- link to the COLA video (from partb_wait) ----------
def k_linkvid(img, t, dur, a):
    """real thumbnail of the COLA video, big in the top-right, with a 'watch' pointer (YouTube card links to it)"""
    tp = os.path.join(ROOT, "px", "cola_thumb.jpg")
    th = Image.open(tp).convert("RGB") if os.path.exists(tp) else Image.new("RGB", (1280, 720), (40, 60, 110))
    p = back(t / 0.45); sc_ = 0.85 + 0.15 * clamp(p)
    w = int(1040 * sc_); h = int(w * 9 / 16)
    x1, y0 = 1860, 70; x0 = x1 - w
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay); al = int(255 * clamp(p))
    d.rounded_rectangle([x0 - 12, y0 - 12, x1 + 12, y0 + h + 12], 26, fill=(255, 255, 255, al))
    img.alpha_composite(lay)
    if p > 0.05:
        tm = th.resize((w, h), Image.LANCZOS).convert("RGBA"); tm.putalpha(al)
        mask = Image.new("L", (w, h), 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, w, h], 18, fill=al)
        img.paste(tm, (x0, y0), mask)
        lay2 = Image.new("RGBA", img.size, (0, 0, 0, 0)); d2 = ImageDraw.Draw(lay2)
        cx, cy = x1 - 130, y0 + h - 95
        d2.rounded_rectangle([cx - 85, cy - 60, cx + 85, cy + 60], 30, fill=(255, 0, 0, int(al * 0.92)))
        d2.polygon([(cx - 26, cy - 34), (cx - 26, cy + 34), (cx + 38, cy)], fill=(255, 255, 255, al))
        img.alpha_composite(lay2)
    slide_text(img, (x0 + w / 2, y0 + h + 70), "YOUR 2027 SOCIAL SECURITY RAISE IS 3.6%", 44, t, 0.4, fill=CREAM)
    slide_text(img, (430, 250), "FULL BREAKDOWN", 60, t, 0.5, fill=ACC)
    slide_text(img, (430, 330), "RAISE vs. PREMIUM", 54, t, 0.7, fill=CREAM)
    if t > 0.9:
        q = ease((t - 0.9) / 0.5); d3 = ImageDraw.Draw(img); xe = 600 + (x0 - 70 - 600) * q
        d3.line([(560, 430), (xe, 430)], fill=ACC, width=14)
        if q > 0.95: d3.polygon([(x0 - 70, 400), (x0 - 20, 430), (x0 - 70, 460)], fill=ACC)
    slide_text(img, (430, 540), "▶ WATCH IT NEXT", 50, t, 1.3, fill=(120, 220, 160))
    slide_text(img, (W / 2, 830), a.get("label", "THIS VIDEO: WHAT THAT ONE DIDN'T COVER"), 50, t, 1.6, fill=ACC)


# ---------- comment question (two sides) ----------
def k_choice(img, t, dur, a):
    p = back(t / 0.45); l, d = lay_(); al = int(255 * clamp(p))
    d.rounded_rectangle([300, 200, 1620, 740], 34, fill=CREAM + (al,))
    d.text((W / 2, 300), a["q"], font=F(64), fill=INKD + (al,), anchor="mm")
    for i, (s_, col) in enumerate(zip(a["sides"], [(70, 110, 170), (110, 100, 80)])):
        x = 650 + i * 620
        d.rounded_rectangle([x - 280, 420, x + 280, 640], 24, fill=col + (al,))
        d.text((x, 500), ["LINDA", "HAROLD"][i], font=F(56), fill=(255, 255, 255, al), anchor="mm")
        d.text((x, 575), s_, font=F(fit(s_, 34, 520, "Bold"), "Bold"), fill=(255, 255, 255, al), anchor="mm")
    img.alpha_composite(l)
    slide_text(img, (W / 2, 830), "WHICH WOULD YOU BE? COMMENT ↓", 56, t, 0.6, fill=GOLD)

# ---------- share + subscribe (new wording) ----------
def k_share(img, t, dur, a):
    slide_text(img, (W / 2, 230), "KNOW SOMEONE CLAIMING AND STILL WORKING?", 56, t, 0, fill=CREAM)
    slide_text(img, (W / 2, 330), "SEND THIS BEFORE JANUARY", 64, t, 0.4, fill=GOLD)
    p = back((t - 1.6) / 0.4); clicked = t > 3.2
    if p > 0:
        l, d = lay_(); sz = 0.6 + 0.4 * clamp(p)
        col = (60, 66, 84) if clicked else (30, 110, 80)
        d.rounded_rectangle([W / 2 - 300 * sz, 580 - 80 * sz, W / 2 + 300 * sz, 580 + 80 * sz], 80, fill=col + (255,))
        d.text((W / 2, 580), "SUBSCRIBED ✓" if clicked else "SUBSCRIBE", font=F(int(64 * sz)), fill=(255, 255, 255), anchor="mm")
        img.alpha_composite(l)
    slide_text(img, (W / 2, 760), "THE NEXT RULE, BEFORE IT HITS YOUR BANK ACCOUNT", 44, t, 1.8, fill=SOFT)

# ---------- no double captions: hide a caption chunk when its words are already on screen ----------
import re as _re
try:
    from num2words import num2words as _n2w
except Exception:
    _n2w = None
STOP = set("a an the and or of to in on for is it its it's that this was were be at by with from as so but if you your her she he his they them their there here just not no".split())
KTEXT = {
    "dollar": "every $1 earned above $25,560 your wage you keep all of it 50 cents held from her benefit $1 of benefits held for every $2 over fifty social security",
    "limitbar": "linda's 2027 earnings from work limit $25,560 $35,560 $10,000 over half held back $5,000 ten thousand five thousand",
    "held": "$5,000 to hold back they stop whole checks $5,600 held extra $600 paid back the next year january february march april",
    "year": "linda's 2027 checks january february march april may held $1,400 check for may lands in june full from then on four",
    "counts": "counts doesn't count wages bonuses commissions vacation pay self-employment profit net pensions annuities investment income interest capital gains veterans benefits government military retirement",
    "vs": "linda harold 63 claimed early part-time job $35,560 pension investments 4 checks held 0 checks held",
    "payback": "ssa's own example 12 checks held $910 $975 a month full retirement age $10,920 $65 14 years earn it back",
    "ages": "before the fra year $25,560 $1 held per $2 over year you reach 67 $67,920 $1 per $3 months before from that month no limit age 63 67",
    "firstyear": "first-year rule any whole month retired earn $2,130 or less that month full check",
    "share": "know someone claiming and still working send this before january subscribe next rule before it hits your bank account",
    "choice": "would you have taken the job linda harold works checks held doesn't work",
    "linkvid": "your 2027 social security raise is 3.6% three point six percent full breakdown watch it next",
}
def _num_forms(tok):
    out = set()
    v = tok.replace("$", "").replace(",", "").replace("%", "")
    try:
        x = float(v)
    except ValueError:
        return out
    if _n2w:
        for w in _re.split(r"[\s\-,]+", _n2w(x if x != int(x) else int(x))): out.add(w)
        if int(x) == x and 1100 <= x < 10000 and x % 100 == 0:   # 1,400 -> fourteen hundred
            for w in _re.split(r"[\s\-]+", _n2w(int(x) // 100)): out.add(w)
            out.add("hundred")
    if tok.startswith("$"): out.add("dollars"); out.add("dollar")
    return out
def _toks(s):
    out = set()
    for raw in _re.findall(r"\$?[\d,.]+%?|[a-z']+", s.lower()):
        raw = raw.strip(".,")
        if not raw: continue
        if _re.match(r"\$?\d", raw):
            out |= _num_forms(raw); n = raw.replace(",", ""); out |= {raw, n, n.lstrip("$"), n.rstrip("%")}
        else:
            out.add(raw); out.add(raw.rstrip("s")); out.add(raw.replace("'s", ""))
    return out
def _scene_text(s):
    parts = [KTEXT.get(s["kind"], "")]
    def walk(v):
        if isinstance(v, str): parts.append(v)
        elif isinstance(v, (list, tuple)):
            for x in v: walk(x)
        elif isinstance(v, dict):
            for x in v.values(): walk(x)
    walk(s["a"])
    if "from" in s["a"] or "to" in s["a"]: parts.append(f'${s["a"].get("to", 0):,}')
    return " ".join(p for p in parts if isinstance(p, str))
_cache = {}; _sent = {}
def _sentence_of(ch):
    """captions are judged per SENTENCE, so they never flicker on/off inside one sentence"""
    if not _sent:
        cur = []
        for c in CHUNKS:
            cur.append(c)
            if _re.search(r"[.?!]$", c[-1]["text"]):
                ws = [w for cc in cur for w in cc]
                for cc in cur: _sent[id(cc)] = ws
                cur = []
        ws = [w for cc in cur for w in cc]
        for cc in cur: _sent[id(cc)] = ws
    return _sent.get(id(ch), ch)
def CAP_SKIP(s, ch):
    if "kind0" not in s: s["kind0"] = s["kind"]
    if s["a"].get("nocap") is not None: return bool(s["a"]["nocap"])
    k = id(s)
    if k not in _cache: _cache[k] = _toks(_scene_text(s))
    st = _cache[k]
    words = [w for w in (_re.sub(r"[^a-z0-9'$-]", "", x["text"].lower()) for x in _sentence_of(ch)) if w]
    words = [w2 for w in words for w2 in w.split("-") if w2]
    content = [w for w in words if w not in STOP]
    if not content: return False
    hit = sum(1 for w in content if w in st or w.rstrip("s") in st or w.replace("'s", "") in st)
    return hit / len(content) >= 0.6 and (hit >= 2 or len(content) == 1)

def k_ftitle(img, t, dur, a): k_title(img, t, dur, a); fiction(img)
def k_fphoto(img, t, dur, a): k_photo(img, t, dur, a); fiction(img)
def k_fhero(img, t, dur, a): k_hero(img, t, dur, a); fiction(img)
def label_fiction(S):
    for s_ in S:
        if any(n in s_["bg"] for n in ("linda", "harold")) and s_["kind"] in ("title", "photo", "hero"):
            s_["kind"] = "f" + s_["kind"]
            KTEXT["f" + "title"] = KTEXT.get("title", "")
