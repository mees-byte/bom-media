# "22% cut, Q4 2032" — serious, document/newsroom-style kinds. exec'd from scenes.py after common_kinds.py
PAPER = (247, 245, 239); INKD = (24, 30, 48); TEAL = (30, 120, 86); WARN = (214, 120, 40); STEELC = (40, 70, 130); AMBER = (170, 120, 20)
HL = (255, 214, 0)
def lay_():
    l = Image.new("RGBA", (W, H), (0, 0, 0, 0)); return l, ImageDraw.Draw(l)
def src(img, s):
    d = ImageDraw.Draw(img)
    d.text((W - 40, 40), s, font=F(26, "SemiBold"), fill=SOFT, anchor="ra", stroke_width=3, stroke_fill=(0, 0, 0))
def wrap(text_, font, maxw):
    out, cur = [], ""
    for w in text_.split():
        t2 = (cur + " " + w).strip()
        if font.getlength(t2) > maxw and cur: out.append(cur); cur = w
        else: cur = t2
    if cur: out.append(cur)
    return out

# ---------- 1. document excerpt with a highlighter sweep (exact quote, attributed) ----------
def k_doc(img, t, dur, a):
    p = back(t / 0.45); l, d = lay_(); al = int(255 * clamp(p))
    x0, y0, x1 = 300, 230 + 30 * (1 - clamp(p)), 1620
    f = F(46, "SemiBold"); lines = wrap(a["quote"], f, x1 - x0 - 140)
    y1 = y0 + 190 + len(lines) * 70 + 40
    d.rounded_rectangle([x0 + 14, y0 + 18, x1 + 14, y1 + 18], 10, fill=(0, 0, 0, int(al * .45)))
    d.rounded_rectangle([x0, y0, x1, y1], 10, fill=PAPER + (al,))
    d.text((x0 + 70, y0 + 60), a["head"], font=F(30, "Bold"), fill=(110, 116, 134, al), anchor="lm")
    d.line([(x0 + 70, y0 + 100), (x1 - 70, y0 + 100)], fill=(200, 196, 186, al), width=3)
    # highlighter: sweeps over the key phrase(s), line by line
    hl = a.get("hl", [])
    q = clamp((t - a.get("dh", 0.9)) / max(0.4, a.get("hs", 1.6)))
    for i, ln in enumerate(lines):
        y = y0 + 170 + i * 70
        for ph in hl:
            if ph in ln:
                xs = x0 + 70 + f.getlength(ln[:ln.index(ph)]); xe = xs + f.getlength(ph)
                xe2 = xs + (xe - xs) * clamp(q * 1.2)
                if xe2 > xs: d.rectangle([xs - 6, y - 30, xe2 + 6, y + 32], fill=HL + (int(al * .75),))
        d.text((x0 + 70, y), ln, font=f, fill=INKD + (al,), anchor="lm")
    d.text((x0 + 70, y1 - 40), a["cite"], font=F(26, "SemiBold"), fill=(110, 116, 134, al), anchor="lm")
    img.alpha_composite(l)

# ---------- 2. countdown: years ticking to Q4 2032 ----------
def k_countdown(img, t, dur, a):
    d = ImageDraw.Draw(img)
    slide_text(img, (W / 2, 150), a.get("kicker", "RETIREMENT (OASI) TRUST FUND RESERVES"), 46, t, 0, fill=SOFT, w="Bold")
    yrs = list(range(2026, 2033)); p = clamp((t - 0.3) / a.get("run", 2.4)); k = min(len(yrs) - 1, int(p * (len(yrs) - 1) + 0.0001))
    for i, y_ in enumerate(yrs):
        x = 260 + i * 233; on = i <= k
        col = (120, 54, 30) if i == len(yrs) - 1 and on else ((40, 70, 130) if on else (28, 36, 60))
        d.rounded_rectangle([x - 100, 330, x + 100, 470], 18, fill=col)
        text(d, (x, 400), str(y_), 52, fill=CREAM if on else (90, 100, 130))
    if p >= 1:
        q = back((t - 0.3 - a.get("run", 2.4)) / 0.4)
        if q > 0:
            l, ld = lay_(); al = int(255 * clamp(q))
            for j, m in enumerate(["OCT", "NOV", "DEC"]):
                x = 1580 + (j - 1) * 120
                ld.rounded_rectangle([x - 52, 520, x + 52, 600], 12, fill=WARN + (al,)); ld.text((x, 560), m, font=F(34), fill=(255, 255, 255, al), anchor="mm")
            img.alpha_composite(l)
        pop_text(img, (W / 2, 720), a.get("big", "RESERVES RUN OUT: Q4 2032"), 84, t, 0.6 + a.get("run", 2.4), fill=GOLD, stroke=6)
        if a.get("sub"): slide_text(img, (W / 2, 830), a["sub"], 44, t, 1.0 + a.get("run", 2.4), fill=CREAM)
    src(img, "2026 Social Security Trustees Report (June 9, 2026)")

# ---------- 3. the check shrinks 22% ----------
def check(l, d, cx, cy, w, h, al, amt, sub):
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], 16, fill=PAPER + (al,), outline=(190, 180, 150, al), width=3)
    d.rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy - h / 2 + 40], fill=(86, 120, 170, al))
    d.text((cx - w / 2 + 30, cy - 40), sub, font=F(28, "Bold"), fill=INKD + (al,), anchor="lm")
    d.text((cx + w / 2 - 30, cy + 30), amt, font=F(72), fill=INKD + (al,), anchor="rm")
def k_shrink(img, t, dur, a):
    slide_text(img, (W / 2, 140), "AVG RETIREMENT CHECK: $2,170 (JAN 2027)", 46, t, 0, fill=SOFT, w="Bold")
    if t > a.get("d", 1.0) - 0.6: slide_text(img, (W / 2, 210), "IF THE CUT HIT IN Q4 2032 (TODAY'S DOLLARS, ILLUSTRATION)", 38, t, a.get("d", 1.0) - 0.6, fill=GOLD, w="Bold")
    p = ease((t - a.get("d", 1.0)) / 1.4); full = 1100; w = full - (full * 0.22) * p
    v = 2170 - 477 * p
    l, d = lay_(); check(l, d, W / 2, 470, w, 330, 255, f"${v:,.0f}", "SOCIAL SECURITY · RETIREMENT" if p < 0.5 else "IF CUT HIT · Q4 2032"); img.alpha_composite(l)
    if p > 0:
        d0 = ImageDraw.Draw(img); xr = W / 2 + full / 2
        d0.rounded_rectangle([xr - full * 0.22 * p, 305, xr, 635], 16, outline=WARN, width=5)
    if p >= 1:
        pop_text(img, (W / 2, 720), "−$477 A MONTH  ·  ≈ −$5,700 A YEAR", 66, t, a.get("d", 1.0) + 1.5, fill=WARN, stroke=6)
        slide_text(img, (W / 2, 820), "78% OF $2,170 = $1,693 · TODAY'S DOLLARS · ILLUSTRATION", 40, t, a.get("d", 1.0) + 1.8, fill=CREAM)
    src(img, "SSA 2027 COLA fact sheet · 2026 Trustees Report · our math")

# ---------- 4. the trust fund tank ----------
def k_tank(img, t, dur, a):
    d = ImageDraw.Draw(img)
    cx, top, bot, wd = W / 2, 230, 760, 460
    d.rounded_rectangle([cx - wd / 2, top, cx + wd / 2, bot], 30, outline=CREAM, width=8)
    ph = a.get("phase", 0)
    lvl = 0.85 if ph == 0 else (0.85 - 0.40 * ease(t / 2.5) if ph == 1 else max(0.0, 0.45 - 0.45 * ease(t / max(1.0, a.get("drain", 3.0)))))
    if lvl > 0.01: d.rounded_rectangle([cx - wd / 2 + 12, bot - 12 - (bot - top - 24) * lvl, cx + wd / 2 - 12, bot - 12], 22, fill=TEAL)
    text(d, (cx, top - 50), "RETIREMENT TRUST FUND RESERVES", 40, fill=CREAM)
    # inflow / outflow arrows
    for side, lab, col, big in [(-1, "PAYROLL TAX IN", (120, 220, 160), ph == 0), (1, "BENEFITS OUT", WARN, ph >= 1)]:
        x = cx + side * (wd / 2 + 260); y = 480
        w_ = 26 if big or ph == 0 else 18
        if side < 0: d.line([(x - 140, y), (cx - wd / 2 - 30, y)], fill=col, width=w_); d.polygon([(cx - wd / 2 - 30, y - 40), (cx - wd / 2 + 10, y), (cx - wd / 2 - 30, y + 40)], fill=col)
        else: d.line([(cx + wd / 2 + 30, y), (x + 140, y)], fill=col, width=w_ + (14 if ph >= 1 else 0)); d.polygon([(x + 140, y - 40), (x + 180, y), (x + 140, y + 40)], fill=col)
        text(d, (x, y - 80), lab, 38, fill=col)
    if ph == 0: slide_text(img, (W / 2, 850), "FOR YEARS: MORE IN THAN OUT → SURPLUS SAVED", 46, t, 0.6, fill=CREAM)
    elif ph == 1: slide_text(img, (W / 2, 850), "NOW: MORE OUT THAN IN → RESERVES SHRINKING (EMPTY BY Q4 2032)", 46, t, 0.4, fill=GOLD)
    else:
        if lvl <= 0.01: pop_text(img, (cx, 520), "Q4 2032", 90, t, a.get("drain", 3.0), fill=WARN, stroke=6)
        slide_text(img, (W / 2, 850), "RESERVES EMPTY ≠ SOCIAL SECURITY STOPS", 48, t, a.get("drain", 3.0) + 0.3, fill=CREAM)
    src(img, "2026 Social Security Trustees Report")

# ---------- 5. 78 of 100 squares ----------
def k_grid78(img, t, dur, a):
    d = ImageDraw.Draw(img)
    slide_text(img, (W / 2, 120), "EVERY $100 OF SCHEDULED BENEFITS, AFTER Q4 2032", 46, t, 0, fill=SOFT, w="Bold")
    s, g = 54, 10; x0 = W / 2 - (10 * s + 9 * g) / 2; y0 = 200
    for i in range(100):
        r, c = divmod(i, 10); dl = 0.2 + i * 0.012
        if t < dl: continue
        paid = i < 78
        col = TEAL if paid else ((120, 54, 30) if t > a.get("dc", 1.8) else (40, 70, 130))
        d.rounded_rectangle([x0 + c * (s + g), y0 + r * (s + g), x0 + c * (s + g) + s, y0 + r * (s + g) + s], 8, fill=col)
    if t > a.get("dc", 1.8):
        slide_text(img, (360, 420), "$78", 120, t, a.get("dc", 1.8), fill=(120, 220, 160))
        slide_text(img, (360, 520), "STILL PAID", 44, t, a.get("dc", 1.8), fill=CREAM)
        slide_text(img, (1560, 420), "−$22", 120, t, a.get("dc", 1.8) + 0.3, fill=WARN)
        slide_text(img, (1560, 520), "THE CUT", 44, t, a.get("dc", 1.8) + 0.3, fill=CREAM)
    src(img, "Trustees: income covers 78% of OASI benefits at depletion")

# ---------- 6. two cards (merged funds / couple estimate) ----------
def k_note(img, t, dur, a):
    p = back(t / 0.4); l, d = lay_(); al = int(255 * clamp(p))
    d.rounded_rectangle([360, 220, 1560, 760], 34, fill=(14, 20, 38, int(al * .92)), outline=a.get("col", STEELC) + (al,), width=6)
    d.text((W / 2, 300), a["kicker"], font=F(40, "Bold"), fill=SOFT + (al,), anchor="mm")
    d.text((W / 2, 450), a["big"], font=F(fit(a["big"], 140, 1100)), fill=a.get("bcol", GOLD) + (al,), anchor="mm")
    for i, ln in enumerate(a.get("lines", [])):
        d.text((W / 2, 580 + i * 60), ln, font=F(40, "Bold"), fill=CREAM + (al,), anchor="mm")
    img.alpha_composite(l)
    src(img, a.get("src", ""))

# ---------- 7. ages today -> Q4 2032 ----------
def k_ages32(img, t, dur, a):
    d = ImageDraw.Draw(img)
    slide_text(img, (W / 2, 150), "WHO IT WOULD HIT: EVERYONE ON RETIREMENT BENEFITS THEN", 44, t, 0, fill=CREAM)
    for i, (a0, a1) in enumerate([(60, 66), (70, 76)]):
        y = 380 + i * 240; dl = 0.3 + i * 0.7; p = ease((t - dl) / 0.8)
        if p <= 0: continue
        card(img, 520, y, 360, 170, t, dl, (40, 70, 130), f"{a0}", "age today")
        if p > 0.3:
            xe = 760 + 400 * p; d.line([(760, y), (xe, y)], fill=GOLD, width=12)
            if p >= 1: d.polygon([(1160, y - 30), (1200, y), (1160, y + 30)], fill=GOLD)
        if p >= 1: card(img, 1420, y, 360, 170, t, dl + 0.8, (120, 54, 30), f"{a1}", "in Q4 2032")
    src(img, "Our math · 2026 Trustees Report")

# ---------- 8. the date moved (OASI only) ----------
def k_shift(img, t, dur, a):
    d = ImageDraw.Draw(img)
    slide_text(img, (W / 2, 140), "RETIREMENT (OASI) FUND · RESERVE DEPLETION YEAR", 46, t, 0, fill=SOFT, w="Bold")
    card(img, 600, 400, 520, 260, t, 0.3, (40, 48, 74), "2033", "2025 report")
    if t > 1.0:
        q = ease((t - 1.0) / 0.3); d.line([(380, 400), (380 + 440 * q, 400)], fill=WARN, width=12)
    card(img, 1320, 400, 520, 260, t, 1.3, (120, 54, 30), "2032", "2026 report")
    slide_text(img, (W / 2, 690), "ONE YEAR CLOSER", 70, t, 1.8, fill=GOLD)
    slide_text(img, (W / 2, 790), "Combined OASI + DI: 2034 — same as last year", 36, t, 2.2, fill=SOFT, w="SemiBold")
    src(img, "CRFB analysis · SSA press release, June 9, 2026")

# ---------- 9. why the long-term shortfall grew (per CRFB) ----------
def k_reasons(img, t, dur, a):
    slide_text(img, (W / 2, 140), "WHY THE LONG-TERM SHORTFALL GREW (PER CRFB)", 50, t, 0, fill=CREAM)
    rows = [("MORE THAN HALF", "Lower expected birth rates", "1.9 → 1.75 children per woman"),
            ("ABOUT A THIRD", "Lower expected immigration", "assumed in the projections"),
            ("ABOUT A QUARTER", "2025 tax law", "less income tax collected on benefits")]
    for i, (sh, lab, sub) in enumerate(rows):
        dl = a.get("d", [0.4, 1.4, 2.4])[i]; p = back((t - dl) / 0.4)
        if p <= 0: continue
        y = 330 + i * 180; l, d = lay_(); al = int(255 * clamp(p))
        d.rounded_rectangle([260, y - 70, 1660, y + 70], 24, fill=(14, 20, 38, int(al * .9)))
        d.rounded_rectangle([260, y - 70, 720, y + 70], 24, fill=AMBER + (al,))
        d.text((490, y), sh, font=F(44), fill=(255, 255, 255, al), anchor="mm")
        d.text((770, y - 20), lab, font=F(48), fill=CREAM + (al,), anchor="lm")
        d.text((770, y + 34), sub, font=F(30, "SemiBold"), fill=SOFT + (al,), anchor="lm")
        img.alpha_composite(l)
    slide_text(img, (W / 2, 880), "Shares overlap because other changes offset part of the worsening", 30, t, 3.0, fill=SOFT, w="SemiBold")
    src(img, "CRFB, Analysis of the 2026 Trustees' Report")

# ---------- 10. the three ways to fix it ----------
def k_options(img, t, dur, a):
    slide_text(img, (W / 2, 130), a.get("title", "TO CLOSE THE 75-YEAR GAP, IF CONGRESS ACTED TODAY"), 46, t, 0, fill=CREAM)
    opts = a.get("opts", [("+34%", "PAYROLL TAX", "+4.25 points", STEELC), ("−25%", "ALL BENEFITS", "everyone", (120, 54, 30)), ("−30%", "NEW BENEFICIARIES", "only", AMBER)])
    for i, (big, lab, sub, col) in enumerate(opts):
        cx = 400 + i * 560 if len(opts) == 3 else 640 + i * 640; dl = a.get("d", [0.3, 1.3, 2.3])[i]; p = back((t - dl) / 0.4)
        if p <= 0: continue
        l, d = lay_(); al = int(255 * clamp(p)); s = 0.8 + 0.2 * clamp(p)
        d.rounded_rectangle([cx - 240 * s, 280, cx + 240 * s, 760], 30, fill=col + (al,))
        d.text((cx, 430), big, font=F(int(140 * s)), fill=(255, 255, 255, al), anchor="mm")
        d.text((cx, 580), lab, font=F(fit(lab, 48, 440)), fill=(255, 255, 255, al), anchor="mm")
        d.text((cx, 650), sub, font=F(34, "SemiBold"), fill=(255, 255, 255, int(al * .85)), anchor="mm")
        if i < len(opts) - 1 and p >= 1: text(ImageDraw.Draw(img), (cx + 280, 520), "OR", 40, fill=SOFT)
        img.alpha_composite(l)
    src(img, "CRFB calculations · combined funds, 75-year fix")

def k_vote(img, t, dur, a):
    p = back(t / 0.45); l, d = lay_(); al = int(255 * clamp(p))
    d.rounded_rectangle([240, 210, 1680, 760], 34, fill=CREAM + (al,))
    d.text((W / 2, 300), "IF IT WERE YOUR VOTE…", font=F(64), fill=INKD + (al,), anchor="mm")
    for i, (lab, col) in enumerate([("RAISE TAXES", STEELC), ("CUT BENEFITS", (120, 54, 30)), ("A MIX", AMBER)]):
        x = 520 + i * 440
        d.rounded_rectangle([x - 190, 430, x + 190, 640], 26, fill=col + (al,))
        d.text((x, 535), lab, font=F(fit(lab, 54, 340)), fill=(255, 255, 255, al), anchor="mm")
    img.alpha_composite(l)
    slide_text(img, (W / 2, 840), "COMMENT YOUR ANSWER ↓  NO POLITICS, JUST YOUR CHOICE", 46, t, 0.6, fill=GOLD)

# ---------- 11. 1983 timeline ----------
def k_y1983(img, t, dur, a):
    d = ImageDraw.Draw(img)
    slide_text(img, (W / 2, 130), "IT HAPPENED BEFORE: 1983", 60, t, 0, fill=GOLD)
    pts = [(0.0, "EARLY 1983", "Fund months away\nfrom exhaustion"), (0.5, "MARCH 1983", "Congress passes\na fix"), (1.0, "APRIL 1983", "President Reagan\nsigns it")]
    x0, x1, y = 300, 1620, 470
    p = ease((t - 0.3) / a.get("run", 2.5)); d.line([(x0, y), (x0 + (x1 - x0) * p, y)], fill=CREAM, width=8)
    for f_, lab, sub in pts:
        if p + 0.001 < f_: continue
        x = x0 + (x1 - x0) * f_; d.ellipse([x - 22, y - 22, x + 22, y + 22], fill=GOLD)
        text(d, (x, y - 80), lab, 44, fill=CREAM)
        for j, ln in enumerate(sub.split("\n")): text(d, (x, y + 70 + j * 46), ln, 34, fill=SOFT, w="Bold")
    if a.get("show_paid"):
        items = ["Yearly raise delayed 6 months", "Up to half of benefits taxed (some people)", "Full retirement age 65 → 67, phased in"]
        for i, s_ in enumerate(items):
            slide_text(img, (W / 2, 690 + i * 62), "•  " + s_, 44, t, a.get("dp", 0.3) + i * a.get("gap", 1.4), fill=CREAM, w="Bold")
    src(img, "CRS R47040 · SSA legislative history, 1983 amendments")

def k_share(img, t, dur, a):
    slide_text(img, (W / 2, 230), "KNOW SOMEONE COUNTING ON EVERY DOLLAR?", 56, t, 0, fill=CREAM)
    slide_text(img, (W / 2, 330), "SEND THEM THIS", 64, t, 0.4, fill=GOLD)
    p = back((t - 1.4) / 0.4); clicked = t > 3.0
    if p > 0:
        l, d = lay_(); sz = 0.6 + 0.4 * clamp(p); col = (60, 66, 84) if clicked else (30, 110, 80)
        d.rounded_rectangle([W / 2 - 300 * sz, 580 - 80 * sz, W / 2 + 300 * sz, 580 + 80 * sz], 80, fill=col + (255,))
        d.text((W / 2, 580), "SUBSCRIBED ✓" if clicked else "SUBSCRIBE", font=F(int(64 * sz)), fill=(255, 255, 255), anchor="mm")
        img.alpha_composite(l)
    slide_text(img, (W / 2, 760), "NEXT TRUSTEES REPORT: WHAT CHANGED, IN DOLLARS", 44, t, 1.8, fill=SOFT)

def k_bigcut(img, t, dur, a):
    slide_text(img, (W / 2, 200), a.get("kicker", ""), 44, t, 0, fill=SOFT, w="Bold")
    pop_text(img, (W / 2, 470), "−22%", 300, t, 0.1, fill=WARN, stroke=10)
    slide_text(img, (W / 2, 760), a.get("sub", "PROJECTED · Q4 2032 · IF CONGRESS DOES NOTHING"), 44, t, 0.5, fill=CREAM, w="Bold")
