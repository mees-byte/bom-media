# Part D 2027 (+50% unless you switch). exec'd after common_kinds.py and ../cut2032/ckinds.py (doc, news, note, src, lay_, wrap, FS...)
def k_tag(img, t, dur, a):
    """price tag flips $34 -> $51 with +50%"""
    slide_text(img, (W / 2, 130), a.get("kicker", "AVG STAND-ALONE DRUG PLAN PREMIUM · IF YOU KEEP YOUR PLAN"), 40, t, 0, fill=SOFT, w="Bold")
    p = ease((t - a.get("d", 1.0)) / 0.9); v = 34 + 17 * p
    l, d = lay_(); cx, cy = W / 2 - 120, 480
    d.polygon([(cx - 330, cy - 170), (cx + 260, cy - 170), (cx + 380, cy), (cx + 260, cy + 170), (cx - 330, cy + 170)], fill=(250, 247, 238, 255))
    d.ellipse([cx + 230, cy - 26, cx + 282, cy + 26], fill=(14, 20, 38, 255))
    d.text((cx - 40, cy - 90), "PER MONTH", font=F(36, "Bold"), fill=(110, 116, 134, 255), anchor="mm")
    d.text((cx - 40, cy + 30), f"${v:.0f}", font=F(170), fill=(WARN if p > 0.5 else INKD) + (255,), anchor="mm")
    img.alpha_composite(l)
    if p >= 1:
        pop_text(img, (cx + 600, cy - 40), "+50%", 150, t, a.get("d", 1.0) + 1.0, fill=WARN, stroke=8)
        slide_text(img, (cx + 600, cy + 90), "2026 → 2027", 44, t, a.get("d", 1.0) + 1.2, fill=CREAM)
    if a.get("sub") and t > a.get("ds", 2.4): slide_text(img, (W / 2, 800), a["sub"], 46, t, a.get("ds", 2.4), fill=GOLD)
    src(img, a.get("srcl", "KFF, Oct 30, 2026 · stand-alone Part D plans (PDPs)"))

def k_deadline(img, t, dur, a):
    """December calendar page with the 7th circled"""
    l, d = lay_(); p = back(t / 0.45); al = int(255 * clamp(p))
    x0, y0 = 610, 140
    d.rounded_rectangle([x0, y0, x0 + 700, y0 + 680], 30, fill=(250, 247, 238, al))
    d.rounded_rectangle([x0, y0, x0 + 700, y0 + 150], 30, fill=(150, 40, 30, al)); d.rectangle([x0, y0 + 110, x0 + 700, y0 + 150], fill=(150, 40, 30, al))
    d.text((x0 + 350, y0 + 75), "DECEMBER 2026", font=F(56), fill=(255, 255, 255, al), anchor="mm")
    # Dec 1 2026 is a Tuesday
    import calendar as _c
    for day in range(1, 32):
        wd = _c.weekday(2026, 12, day); wk = (day + _c.weekday(2026, 12, 1) - 1) // 7
        x = x0 + 60 + wd * 97; y = y0 + 210 + wk * 92
        d.text((x, y), str(day), font=F(40, "Bold"), fill=((150, 40, 30) if day == 7 else INKD) + (al,), anchor="mm")
        if day == 7 and t > 0.8:
            q = ease((t - 0.8) / 0.5); d.arc([x - 50, y - 44, x + 50, y + 44], 0, int(360 * q), fill=(214, 60, 40, al), width=8)
    img.alpha_composite(l)
    sub_ = a.get("sub", "OPEN ENROLLMENT ENDS DECEMBER 7")
    if t > 1.4: slide_text(img, (W / 2, 900), sub_, fit(sub_, 50, 1600), t, 1.4, fill=GOLD)
    src(img, a.get("srcl", "CMS press release, Sep 28, 2026"))

def k_twonums(img, t, dur, a):
    """KFF +50% vs Medicare < $1"""
    slide_text(img, (W / 2, 130), "TWO REAL ANALYSES · TWO DIFFERENT QUESTIONS", 46, t, 0, fill=CREAM)
    for i, (who, big, sub1, sub2, col) in enumerate([("KFF", "+50%", "$34 → $51", "if people keep their plan", WARN),
                                                     ("MEDICARE (CMS)", "< $1", "$35.09 → $36", "national average", (120, 220, 160))]):
        cx = 560 + i * 800; dl = a.get("d", [0.3, 1.4])[i]; p = back((t - dl) / 0.4)
        if p <= 0: continue
        l, d = lay_(); al = int(255 * clamp(p))
        d.rounded_rectangle([cx - 340, 230, cx + 340, 780], 30, fill=(14, 20, 38, int(al * .92)), outline=col + (al,), width=6)
        d.text((cx, 300), who, font=F(44, "Bold"), fill=SOFT + (al,), anchor="mm")
        d.text((cx, 470), big, font=F(180), fill=col + (al,), anchor="mm")
        d.text((cx, 620), sub1, font=F(60), fill=CREAM + (al,), anchor="mm")
        d.text((cx, 700), sub2, font=F(36, "SemiBold"), fill=SOFT + (al,), anchor="mm")
        img.alpha_composite(l)
    if t > a.get("dv", 2.4): slide_text(img, (W / 2, 860), "VS", 50, t, a.get("dv", 2.4), fill=CREAM)
    src(img, "KFF Oct 30, 2026 · CMS Sep 28, 2026 · stand-alone drug plans")

def k_people(img, t, dur, a):
    """100 person icons: 76 pay more"""
    slide_text(img, (W / 2, 120), a.get("title", "13.6 MILLION PEOPLE IN STAND-ALONE PLANS, NO EXTRA HELP"), 42, t, 0, fill=SOFT, w="Bold")
    d = ImageDraw.Draw(img); n = a.get("n", 76)
    for i in range(100):
        r, c = divmod(i, 20); x = 400 + c * 58; y = 260 + r * 110; dl = 0.2 + i * 0.01
        if t < dl: continue
        on = i < n and t > a.get("dc", 1.6)
        col = WARN if on else (70, 84, 120)
        d.ellipse([x - 14, y - 44, x + 14, y - 16], fill=col); d.rounded_rectangle([x - 20, y - 12, x + 20, y + 40], 14, fill=col)
    if t > a.get("dc", 1.6):
        pop_text(img, (W / 2, 860), a.get("big", "76% PAY MORE IF THEY CHANGE NOTHING"), 64, t, a.get("dc", 1.6) + 0.3, fill=GOLD, stroke=6)
    src(img, "KFF analysis, Oct 30, 2026")

def k_range(img, t, dur, a):
    slide_text(img, (W / 2, 130), "THE 8 NATIONAL STAND-ALONE PLANS · AVERAGE MONTHLY PREMIUM, 2027", 42, t, 0, fill=SOFT, w="Bold")
    d = ImageDraw.Draw(img); x0, x1, y = 260, 1660, 470
    p = ease((t - 0.3) / 1.2)
    if p > 0.05: card(img, x0 + 120, y + 180, 340, 170, t, 0.4, TEAL, "$6.50", "cheapest (avg)")
    if p >= 1: card(img, x1 - 120, y + 180, 340, 170, t, 1.5, (150, 40, 30), "$204.50", "priciest (avg)")
    if t > 2.4: slide_text(img, (W / 2, 330), "CHEAPEST PREMIUM ≠ CHEAPEST PLAN FOR YOUR DRUGS", 50, t, 2.4, fill=GOLD)
    src(img, "KFF, Oct 30, 2026")

def k_fork(img, t, dur, a):
    slide_text(img, (W / 2, 140), "BY DECEMBER 7", 70, t, 0, fill=GOLD)
    for i, (lab, sub, col) in enumerate([("COMPARE PLANS", "Medicare Plan Finder · SHIP counselors", TEAL), ("KEEP YOUR PLAN", "in most cases at its 2027 price · know the cost", STEELC)]):
        cx = 560 + i * 800; dl = 0.4 + i * 0.6; p = back((t - dl) / 0.4)
        if p <= 0: continue
        l, d = lay_(); al = int(255 * clamp(p))
        d.rounded_rectangle([cx - 340, 300, cx + 340, 640], 30, fill=col + (al,))
        d.text((cx, 430), lab, font=F(fit(lab, 72, 620)), fill=(255, 255, 255, al), anchor="mm")
        d.text((cx, 530), sub, font=F(fit(sub, 36, 620, "SemiBold"), "SemiBold"), fill=(255, 255, 255, int(al * .9)), anchor="mm")
        img.alpha_composite(l)
    if t > 1.0: text(ImageDraw.Draw(img), (W / 2, 470), "OR", 50, fill=CREAM)
    src(img, "CMS, Sep 28, 2026")
