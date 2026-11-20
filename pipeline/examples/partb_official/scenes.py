# Money Under Fire — "Medicare's 2027 Premium Is Official: $209.40" (Fri 2026-11-20)
exec(open(os.path.join(ROOT, "common_kinds.py")).read())
TEAL = (30, 110, 80); STEELC = (40, 70, 130); AMBER = (150, 112, 20); GREY = (90, 100, 130); RUST = (150, 60, 40)

def k_forecast(img, t, dur, a):
    """real forecast vs actual Part B premium (Trustees forecast vs CMS final)"""
    d = ImageDraw.Draw(img)
    yr, fc, ac = a["yr"], a["fc"], a["ac"]
    slide_text(img, (W / 2, 150), f"{yr} PART B PREMIUM", 56, t, 0, fill=CREAM)
    lo = a.get("lo", 140)
    for i, (lab, v, col, dl) in enumerate([("FORECAST", fc, GREY, 0.2), ("REAL", ac, ACC, a.get("d2", 1.2))]):
        x = 700 + i * 520; p = ease((t - dl) / 0.8); h = 400 * (v - lo) / (215 - lo) * p
        if p <= 0: continue
        d.rounded_rectangle([x - 150, 830 - h, x + 150, 830], 18, fill=col)
        slide_text(img, (x, 875), lab, 50, t, dl, fill=CREAM)
        if p > 0.4: slide_text(img, (x, 830 - h - 55), f"${v:,.2f}", 70, t, dl + 0.3, fill=CREAM)
    if t > a.get("d2", 1.2) + 0.9:
        diff = ac - fc; s_ = ("LOWER" if diff < 0 else "HIGHER")
        pop_text(img, (W / 2, 255), f"${abs(diff):.2f} {s_}", 80, t, a.get("d2", 1.2) + 0.9, fill=ACC if diff > 0 else (120, 220, 160), stroke=6)
    slide_text(img, (W - 60, 60), "2026 Trustees forecast vs. CMS final", 26, t, 0.5, fill=SOFT, w="SemiBold", anchor="rm")

def k_net(img, t, dur, a):
    """average raise minus premium increase = what's left"""
    card(img, 420, 470, 460, 280, t, 0, TEAL, "+$75", "average raise")
    card(img, 960, 470, 460, 280, t, 0.8, RUST, "−$6.50", "Part B increase")
    card(img, 1500, 470, 460, 280, t, 1.6, AMBER, "≈ $68.50", "left for you")
    slide_text(img, (W / 2, 790), "PER MONTH · 2027 · Sources: SSA, CMS", 40, t, 2.0, fill=SOFT, w="Bold")

def k_years(img, t, dur, a):
    """premium % change vs COLA %, 2024-2027 (CMS / SSA)"""
    d = ImageDraw.Draw(img)
    data = [("2024", 5.9, 3.2), ("2025", 5.9, 2.5), ("2026", 9.7, 2.8), ("2027", 3.2, 3.6)]
    slide_text(img, (W / 2, 120), "PART B PREMIUM vs. YOUR RAISE", 58, t, 0, fill=CREAM)
    for i, (yr, pr, cola) in enumerate(data):
        x = 380 + i * 400; dl = 0.2 + i * 0.35; p = ease((t - dl) / 0.7)
        if p <= 0: continue
        for j, (v, col) in enumerate([(pr, AMBER), (cola, TEAL)]):
            xx = x - 75 + j * 150; h = 480 * v / 10 * p
            d.rounded_rectangle([xx - 60, 820 - h, xx + 60, 820], 12, fill=col)
            if p > 0.5: text(d, (xx, 820 - h - 40), f"{v}%", 46, fill=CREAM)
        slide_text(img, (x, 875), yr, 52, t, dl, fill=ACC if yr == "2027" else CREAM)
    d.rounded_rectangle([600, 195, 640, 235], 8, fill=AMBER); text(d, (790, 215), "PREMIUM", 36, fill=CREAM)
    d.rounded_rectangle([1060, 195, 1100, 235], 8, fill=TEAL); text(d, (1230, 215), "YOUR RAISE", 36, fill=CREAM)

def k_three(img, t, dur, a):
    it = [("NEW TO PART B / NOT ON SOCIAL SECURITY YET", "you pay the full $209.40"),
          ("HIGHER INCOME (IRMAA)", "surcharge above $112,000 single"),
          ("PROTECTED BY HOLD HARMLESS IN 2026", "your premium can catch up")]
    slide_text(img, (W / 2, 150), "WHO GETS A DIFFERENT NUMBER", 60, t, 0, fill=ACC)
    for i, (h_, s_) in enumerate(it):
        dl = a["d"][i]; p = back((t - dl) / 0.3)
        if p <= 0: continue
        y = 330 + i * 190; lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay); al = int(255 * clamp(p))
        hl = i == a.get("hl", -1) or a.get("hl", -1) == 9
        d.ellipse([240, y - 55, 350, y + 55], fill=(ACC if hl else GREY) + (al,)); d.text((295, y), str(i + 1), font=F(60), fill=(15, 22, 45, al), anchor="mm")
        d.text((400, y - 25), h_, font=F(fit(h_, 58, 1400)), fill=CREAM + (al,), anchor="lm")
        d.text((400, y + 35), s_, font=F(40, "Bold"), fill=SOFT + (al,), anchor="lm"); img.alpha_composite(lay)

def k_linkwait(img, t, dur, a):
    """real thumbnail of the previous video, big top-right (card + end screen link to it)"""
    th = Image.open(os.path.join(ROOT, "px", "wait_thumb.jpg")).convert("RGB")
    p = back(t / 0.45); sc_ = 0.85 + 0.15 * clamp(p)
    w = int(1040 * sc_); h = int(w * 9 / 16); x1, y0 = 1860, 70; x0 = x1 - w
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay); al = int(255 * clamp(p))
    d.rounded_rectangle([x0 - 12, y0 - 12, x1 + 12, y0 + h + 12], 26, fill=(255, 255, 255, al)); img.alpha_composite(lay)
    if p > 0.05:
        tm = th.resize((w, h), Image.LANCZOS).convert("RGBA")
        mask = Image.new("L", (w, h), 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, w, h], 18, fill=al)
        img.paste(tm, (x0, y0), mask)
        lay2 = Image.new("RGBA", img.size, (0, 0, 0, 0)); d2 = ImageDraw.Draw(lay2); cx, cy = x1 - 130, y0 + h - 95
        d2.rounded_rectangle([cx - 85, cy - 60, cx + 85, cy + 60], 30, fill=(255, 0, 0, int(al * 0.92)))
        d2.polygon([(cx - 26, cy - 34), (cx - 26, cy + 34), (cx + 38, cy)], fill=(255, 255, 255, al)); img.alpha_composite(lay2)
    slide_text(img, (x0 + w / 2, y0 + h + 70), "IRMAA · HOLD HARMLESS · STATE HELP", 44, t, 0.4, fill=CREAM)
    slide_text(img, (430, 250), "ALL 3 EXPLAINED", 60, t, 0.5, fill=ACC)
    slide_text(img, (430, 330), "IN MY LAST VIDEO", 54, t, 0.7, fill=CREAM)
    if t > 0.9:
        q = ease((t - 0.9) / 0.5); d3 = ImageDraw.Draw(img); xe = 600 + (x0 - 70 - 600) * q
        d3.line([(560, 430), (xe, 430)], fill=ACC, width=14)
        if q > 0.95: d3.polygon([(x0 - 70, 400), (x0 - 20, 430), (x0 - 70, 460)], fill=ACC)
    slide_text(img, (430, 540), "▶ WATCH IT NEXT", 50, t, 1.3, fill=(120, 220, 160))

def k_ask(img, t, dur, a):
    p = back(t / 0.45); lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay); al = int(255 * clamp(p))
    ld.rounded_rectangle([300, 230, 1620, 720], 34, fill=CREAM + (al,))
    ld.text((W / 2, 320), "AFTER THE RAISE AND THE PREMIUM:", font=F(52), fill=(15, 22, 45, al), anchor="mm")
    ld.text((W / 2, 390), "BETTER OFF IN JANUARY?", font=F(52), fill=(15, 22, 45, al), anchor="mm")
    ld.rounded_rectangle([420, 470, 940, 640], 24, fill=TEAL + (al,)); ld.text((680, 555), "YES", font=F(70), fill=(255, 255, 255, al), anchor="mm")
    ld.rounded_rectangle([980, 470, 1500, 640], 24, fill=STEELC + (al,)); ld.text((1240, 555), "NOT REALLY", font=F(62), fill=(255, 255, 255, al), anchor="mm")
    img.alpha_composite(lay)
    slide_text(img, (W / 2, 820), "TELL ME IN THE COMMENTS ↓", 56, t, 0.6, fill=ACC)

def k_subscribe3(img, t, dur, a):
    slide_text(img, (W / 2, 280), "ON MEDICARE, OR A FEW YEARS AWAY?", 64, t, 0, fill=CREAM)
    slide_text(img, (W / 2, 380), "ONE RULE EXPLAINED EVERY WEEK", 52, t, 0.3, fill=ACC)
    p = back((t - 0.6) / 0.4); clicked = t > 2.2
    if p > 0:
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay); sz = 0.6 + 0.4 * clamp(p)
        col = (60, 66, 84) if clicked else TEAL
        ld.rounded_rectangle([W / 2 - 300 * sz, 580 - 80 * sz, W / 2 + 300 * sz, 580 + 80 * sz], 80, fill=col + (255,))
        ld.text((W / 2, 580), "SUBSCRIBED ✓" if clicked else "SUBSCRIBE", font=F(int(64 * sz)), fill=(255, 255, 255), anchor="mm")
        img.alpha_composite(lay)
    slide_text(img, (W / 2, 780), "MONEY UNDER FIRE", 48, t, 0.8, fill=SOFT)

def k_tenth(img, t, dur, a):
    d = ImageDraw.Draw(img); p = ease(t / 1.0)
    for i in range(10):
        x = 360 + i * 120
        if p * 10 > i: d.rounded_rectangle([x, 330, x + 100, 560], 14, fill=TEAL)
    q = ease((t - 1.1) / 0.6)
    if q > 0:
        d.rounded_rectangle([360, 330, 360 + 100 * 6.50 / 7.5, 560], 14, fill=AMBER)
        slide_text(img, (420, 620), "$6.50", 46, t, 1.2, fill=ACC)
    slide_text(img, (W / 2, 250), "AVERAGE RAISE ≈ $75 = 10 SLICES OF $7.50", 46, t, 0, fill=SOFT, w="Bold")
    slide_text(img, (W / 2, 760), "2027 PREMIUM INCREASE: LESS THAN ONE SLICE", 52, t, 1.5, fill=CREAM)

# ---------------- scenes ----------------
sc("It's official", "pxcount", "pxb:envelope", v=209.40, fmt=lambda v: f"${v:,.2f}", kicker="IT'S OFFICIAL · 2027 PART B PREMIUM", label="PER MONTH", src="Source: CMS, Nov. 17, 2026", disc=True)
sc("That's $6", "pxcount", "px:calendar", v=6.50, fmt=lambda v: f"+${v:.2f}", kicker="MORE THAN 2026", label="A MONTH")
sc("And for most", "photo", "pxb:mailbox", lines=["IT COMES STRAIGHT OUT OF", ("YOUR SOCIAL SECURITY CHECK", ACC)], y=800, size=86)
sc("So here's your answer", "net", "navy")
sc("And here's something", "title", "navy", kicker="FIRST TIME SINCE 2023", lines=["THE PREMIUM IS GROWING", ("AT A SLOWER RATE THAN YOUR RAISE", ACC)], size=90)
sc("In the next", "title", "px:desk", lines=["THE EXACT NUMBERS", "WHO GETS A DIFFERENT NUMBER", ("THE LINE TO CHECK", ACC)], size=90)

sc("Chapter 1", "chapter", "navy", num="CHAPTER 1", title="THE NUMBERS")
sc("Medicare announced the", "photo", "pxb:calendar", lines=["ANNOUNCED", ("NOVEMBER 17", ACC)], y=800)
sc("The standard Part B premium goes", "pxcount", "px:calc", v=209.40, fmt=lambda v: f"${v:,.2f}", kicker="$202.90 → 2027", label="+3.2%", src="Source: CMS")
sc("Your Social Security raise", "pxcount", "px:piggy", v=3.6, fmt=lambda v: f"{v:.1f}%", kicker="YOUR 2027 RAISE (COLA)", label="PREMIUM: +3.2%", src="Source: SSA")
sc("Now compare that", "years", "navy")
sc("This year $6", "tenth", "navy")
sc("And the forecast", "forecast", "navy", yr=2027, fc=209.50, ac=209.40, d2=1.2, lo=140)
sc("One more number", "pxcount", "px:pills", v=292, fmt=lambda v: f"${v:,.0f}", kicker="PART B DEDUCTIBLE 2027", label="UP FROM $283", src="Source: CMS")
sc("But that $68", "question", "px:desk", lines=["$68.50 ISN'T", "EVERYONE'S NUMBER"])

sc("Chapter 2", "chapter", "navy", num="CHAPTER 2", title="WHO GETS A DIFFERENT NUMBER")
sc("First people who", "three", "navy", d=[0.2, 99, 99], hl=0)
sc("Second people with", "three", "navy", d=[0, 0.2, 99], hl=1)
sc("For 2027 the", "pxcount", "px:calc", v=112000, fmt=lambda v: f"${v:,.0f}", kicker="2027 IRMAA STARTS ABOVE", label="SINGLE FILER · BASED ON YOUR 2025 RETURN", src="Source: CMS / SSA")
sc("Go even $1", "pxcount", "pxb:cliff", v=83.70, fmt=lambda v: f"+${v:.2f}", kicker="$1 OVER THE LINE: PART B", label="+ A DRUG-PLAN SURCHARGE", src="Per month · Source: CMS")
sc("Third people whose", "three", "navy", d=[0, 0, 0.2], hl=2)
sc("I covered all", "linkwait", "navy")
sc("So let me ask", "ask", "px:kitchen")

sc("Chapter 3", "chapter", "navy", num="CHAPTER 3", title="WHAT TO CHECK")
sc("Your 2027 Social", "photo", "pxb:phone", lines=["YOUR NOTICE SHOWS", ("THE NEW PREMIUM", ACC)], y=800)
sc("If you have a my", "when", "navy", gap=3.0)
sc("Skip the big", "notice", "navy", hl=1)
sc("The amount you'll", "notice", "navy", hl=2, anim=False)
sc("And if you have a drug", "pxcount", "px:pharmacy", v=7, fmt=lambda v: f"DEC. {v:.0f}", kicker="COMPARE DRUG / ADVANTAGE PLANS BY", label="OPEN ENROLLMENT ENDS")
sc("If you're on Medicare", "subscribe3", "navy")
sc("This video is", "title", "navy", lines=["GENERAL EDUCATION,", ("NOT ADVICE", ACC)], size=120)
sc("So it's official", "pxcount", "pxb:envelope", v=209.40, fmt=lambda v: f"${v:,.2f}", kicker="IT'S OFFICIAL", label="CHECK THE LAST LINE ON YOUR NOTICE")
