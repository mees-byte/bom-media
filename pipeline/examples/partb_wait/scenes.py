# Money Under Fire — "Medicare's 2027 Premium Drops Any Day. 4 Things That Matter More" (Wed 2026-11-18)
exec(open(os.path.join(ROOT, "common_kinds.py")).read())
TEAL = (30, 110, 80); STEELC = (40, 70, 130); AMBER = (150, 112, 20); GREY = (90, 100, 130); RUST = (150, 60, 40)

def k_four(img, t, dur, a):
    items = [("1", "A FORECAST THAT'S BEEN WRONG"), ("2", "A TAX-RETURN TRAP"), ("3", "A CATCH FOR SMALLER CHECKS"), ("4", "A STATE PROGRAM THAT PAYS IT")]
    slide_text(img, (W / 2, 150), "4 THINGS THAT MATTER MORE", 60, t, 0, fill=ACC)
    for i, (n, s_) in enumerate(items):
        dl = a["d"][i]; p = back((t - dl) / 0.35)
        if p <= 0: continue
        y = 300 + i * 150; lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay); al = int(255 * clamp(p))
        d.ellipse([330, y - 50, 430, y + 50], fill=ACC + (al,)); d.text((380, y), n, font=F(60), fill=(15, 22, 45, al), anchor="mm")
        d.text((480, y), s_, font=F(64), fill=CREAM + (al,), anchor="lm"); img.alpha_composite(lay)

def k_linkvid(img, t, dur, a):
    p = back(t / 0.4); lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay); al = int(255 * clamp(p))
    d.rounded_rectangle([460, 260, 1460, 700], 30, fill=(250, 247, 238, al))
    d.rounded_rectangle([500, 300, 900, 525], 18, fill=(12, 26, 60, al)); d.text((700, 412), "$75?", font=F(110), fill=ACC + (al,), anchor="mm")
    d.text((940, 340), "FULL BREAKDOWN:", font=F(40, "Bold"), fill=(90, 100, 130, al), anchor="lm")
    d.text((940, 410), "YOUR 2027 RAISE", font=F(56), fill=(15, 22, 45, al), anchor="lm")
    d.text((940, 475), "vs. THE PREMIUM", font=F(56), fill=(15, 22, 45, al), anchor="lm")
    d.text((960, 620), "▶  LINKED ON SCREEN  ↗", font=F(48), fill=TEAL + (al,), anchor="mm")
    img.alpha_composite(lay)
    slide_text(img, (W / 2, 820), a.get("label", "THIS VIDEO: WHAT THAT ONE DIDN'T COVER"), 50, t, 0.8, fill=ACC)

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
    slide_text(img, (W - 60, 60), "Medicare Trustees forecast vs. CMS", 26, t, 0.5, fill=SOFT, w="SemiBold", anchor="rm")

def k_lookback(img, t, dur, a):
    d = ImageDraw.Draw(img)
    card(img, 520, 470, 560, 280, t, 0, STEELC, "2025 TAX RETURN", "income: MAGI")
    p = ease((t - 0.8) / 0.8)
    if p > 0:
        x1 = 820 + 280 * p; d.line([(820, 470), (x1, 470)], fill=ACC, width=16)
        if p > 0.95: d.polygon([(1100, 435), (1150, 470), (1100, 505)], fill=ACC)
    card(img, 1420, 470, 560, 280, t, 1.6, AMBER, "2027 PREMIUM", "Part B + drug plan")
    slide_text(img, (W / 2, 760), "TWO YEARS LATER", 70, t, 2.2, fill=ACC)

def k_cliff(img, t, dur, a):
    d = ImageDraw.Draw(img)
    slide_text(img, (W / 2, 140), "2026 · SINGLE FILER · MAGI", 46, t, 0, fill=SOFT, w="Bold")
    x0, x1, y = 260, 1660, 760; edge = 960
    d.line([(x0, y), (x1, y)], fill=CREAM, width=6)
    text(d, (edge, y + 60), "$109,000", 50, fill=CREAM)
    p = ease((t - 0.3) / 0.8)
    d.rounded_rectangle([x0, y - 330 * p, edge - 10, y], 14, fill=TEAL)
    if p > 0.5: text(d, ((x0 + edge) / 2, y - 330 - 50), "$202.90", 76, fill=CREAM)
    q = ease((t - a.get("d2", 1.4)) / 0.6)
    if q > 0:
        d.rounded_rectangle([edge + 10, y - 460 * q, x1, y], 14, fill=AMBER)
        if q > 0.6: text(d, ((edge + x1) / 2, y - 460 - 50), "$284.10", 76, fill=ACC)
    if t > a.get("d2", 1.4) + 0.8: pop_text(img, (edge - 330, 230), "$1 OVER THE LINE", 70, t, a.get("d2", 1.4) + 0.8, fill=ACC, stroke=6)
    slide_text(img, (W - 60, 60), "Part B per month · Source: CMS", 26, t, 0.5, fill=SOFT, w="SemiBold", anchor="rm")

def k_couple(img, t, dur, a):
    for i in range(2):
        card(img, 680 + i * 560, 470, 480, 300, t, i * 0.5, AMBER, "+$81.20", "per month, each")
    slide_text(img, (W / 2, 780), "BOTH ON MEDICARE? YOU EACH PAY IT", 60, t, 1.0, fill=ACC)

def k_events(img, t, dur, a):
    ev = ["MARRIAGE", "DIVORCE / ANNULMENT", "DEATH OF A SPOUSE", "STOPPED WORKING", "WORK REDUCED", "LOST INCOME PROPERTY", "LOST EMPLOYER PENSION", "EMPLOYER SETTLEMENT"]
    slide_text(img, (W / 2, 150), "FORM SSA-44 · THE 8 LIFE-CHANGING EVENTS", 52, t, 0, fill=ACC)
    for i, e in enumerate(ev):
        c, r = i % 2, i // 2; x = 560 + c * 800; y = 300 + r * 140
        p = back((t - 0.2 - i * 0.18) / 0.3)
        if p <= 0: continue
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay); al = int(255 * clamp(p))
        hl = e in a.get("hl", [])
        d.rounded_rectangle([x - 360, y - 52, x + 360, y + 52], 26, fill=(TEAL if hl else STEELC) + (al,))
        d.text((x, y), e, font=F(44), fill=(255, 255, 255, al), anchor="mm"); img.alpha_composite(lay)

def k_nocount(img, t, dur, a):
    it = ["SELLING A HOUSE", "SELLING STOCK", "BIG IRA WITHDRAWAL", "ROTH CONVERSION"]
    slide_text(img, (W / 2, 160), "A SPIKE YOU CHOSE DOESN'T COUNT", 60, t, 0, fill=ACC)
    for i, s_ in enumerate(it):
        dl = a["d"][i]; p = back((t - dl) / 0.3)
        if p <= 0: continue
        y = 320 + i * 140; lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay); al = int(255 * clamp(p))
        d.ellipse([500, y - 45, 590, y + 45], fill=RUST + (al,))
        d.line([(525, y - 20), (565, y + 20)], fill=(255, 255, 255, al), width=12); d.line([(565, y - 20), (525, y + 20)], fill=(255, 255, 255, al), width=12)
        d.text((640, y), s_, font=F(64), fill=CREAM + (al,), anchor="lm"); img.alpha_composite(lay)

def k_ask3(img, t, dur, a):
    p = back(t / 0.45); lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay); al = int(255 * clamp(p))
    ld.rounded_rectangle([300, 230, 1620, 720], 34, fill=CREAM + (al,))
    ld.text((W / 2, 320), "YOUR MEDICARE BILL LOOKS BACK 2 YEARS.", font=F(52), fill=(15, 22, 45, al), anchor="mm")
    ld.text((W / 2, 390), "DID YOU KNOW?", font=F(52), fill=(15, 22, 45, al), anchor="mm")
    ld.rounded_rectangle([420, 470, 940, 640], 24, fill=TEAL + (al,)); ld.text((680, 555), "YES", font=F(70), fill=(255, 255, 255, al), anchor="mm")
    ld.rounded_rectangle([980, 470, 1500, 640], 24, fill=STEELC + (al,)); ld.text((1240, 555), "NO", font=F(70), fill=(255, 255, 255, al), anchor="mm")
    img.alpha_composite(lay)
    slide_text(img, (W / 2, 820), "TELL ME IN THE COMMENTS ↓", 56, t, 0.6, fill=ACC)

def k_catchup(img, t, dur, a):
    """illustration only: standard premium vs a protected (held-harmless) premium catching up"""
    d = ImageDraw.Draw(img)
    slide_text(img, (W / 2, 150), "ILLUSTRATION", 34, t, 0, fill=SOFT, w="Bold")
    base, y = 830, 0
    for i, (lab, hgt, col, dl) in enumerate([("STANDARD PREMIUM", 470, GREY, 0.1), ("PROTECTED: YOU PAID LESS", 330, TEAL, 0.5)]):
        x = 680 + i * 560; p = ease((t - dl) / 0.7)
        d.rounded_rectangle([x - 170, base - hgt * p, x + 170, base], 18, fill=col)
        slide_text(img, (x, 880), lab, 40, t, dl, fill=CREAM)
    if a.get("up"):
        q = ease((t - 1.2) / 0.9); x = 1240
        if q > 0:
            d.rounded_rectangle([x - 170, base - 330 - 140 * q, x + 170, base - 330], 18, fill=AMBER)
            pop_text(img, (x + 330, base - 400), "CATCH-UP", 64, t, 1.6, fill=ACC, stroke=6)

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
    slide_text(img, (W / 2, 780), a.get("sub", "MONEY UNDER FIRE"), 48, t, 0.8, fill=SOFT)

def k_msp(img, t, dur, a):
    d = ImageDraw.Draw(img)
    card(img, 380, 450, 480, 240, t, 0, STEELC, "YOUR STATE", "Medicare Savings Program")
    card(img, 960, 450, 440, 240, t, 0.6, AMBER, "PAYS PART B", "instead of you")
    card(img, 1540, 450, 480, 240, t, 1.2, TEAL, "YOUR CHECK", "premium no longer taken out")
    for i in range(2):
        if t > 0.4 + i * 0.6:
            x = 640 + i * 560; d.polygon([(x, 420), (x + 50, 450), (x, 480)], fill=CREAM)
    slide_text(img, (W / 2, 720), a.get("label", "LIMITED INCOME & SAVINGS · APPLY VIA YOUR STATE MEDICAID OFFICE"), 40, t, 1.6, fill=SOFT, w="Bold")

def k_todo(img, t, dur, a):
    it = [("TURN ON ALERTS", "my Social Security · notice late Nov."), ("2025 INCOME UNUSUAL?", "check SSA-44 life-changing events"),
          ("MONEY TIGHT?", "ask about a Medicare Savings Program"), ("DRUG PLAN / ADVANTAGE?", "compare plans by December 7")]
    slide_text(img, (W / 2, 130), "WHILE YOU WAIT", 60, t, 0, fill=ACC)
    for i, (h_, s_) in enumerate(it):
        dl = a["d"][i]; p = back((t - dl) / 0.3)
        if p <= 0: continue
        y = 280 + i * 160; lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay); al = int(255 * clamp(p))
        done = i < a.get("done", 0) or t > dl + 1.0
        d.rounded_rectangle([300, y - 55, 410, y + 55], 20, fill=(TEAL if done else GREY) + (al,))
        if done: d.line([(325, y), (348, y + 25), (388, y - 25)], fill=(255, 255, 255, al), width=14)
        d.text((450, y - 20), h_, font=F(56), fill=CREAM + (al,), anchor="lm")
        d.text((450, y + 30), s_, font=F(36, "Bold"), fill=SOFT + (al,), anchor="lm"); img.alpha_composite(lay)

# ---------------- scenes ----------------
# HOOK (new image every 1–3 s)
sc("Any day now", "pxcount", "pxb:calendar", v=209.50, fmt=lambda v: f"${v:,.2f}?", kicker="2027 PART B PREMIUM", label="ANNOUNCEMENT: ANY DAY NOW", disc=True)
sc("and most retirees", "photo", "pxb:clock", lines=["MOST RETIREES", ("JUST WAIT FOR ONE NUMBER", ACC)], y=800, size=90)
sc("But the number", "title", "navy", lines=["THE NUMBER ISN'T", ("THE WHOLE BILL", ACC)])
sc("For some people", "photo", "pxb:taxform", lines=["FOR SOME, IT WAS DECIDED BY", ("A TAX RETURN", ACC)], y=800, size=90)
sc("So while we", "four", "navy", d=[3.3, 6.1, 7.6, 9.7])
sc("If you want", "linkvid", "navy")
sc("This one covers", "title", "navy", lines=["THIS VIDEO:", ("WHAT THAT ONE DIDN'T COVER", ACC)], size=100)
# CHAPTER 1
sc("Chapter 1", "chapter", "navy", num="CHAPTER 1", title="THE FORECAST ISN'T THE ANSWER")
sc("Every year Medicare's", "photo", "pxb:forecast", lines=["EVERY YEAR:", ("THE TRUSTEES' FORECAST", ACC)], y=800)
sc("This year's forecast", "pxcount", "px:calendar", v=209.50, fmt=lambda v: f"${v:,.2f}", kicker="2027 FORECAST", label="A FORECAST, NOT A BILL", src="2026 Medicare Trustees Report")
sc("But a forecast", "title", "px:envelope", lines=["A FORECAST", ("IS NOT A BILL", ACC)])
sc("And it has", "title", "navy", lines=["IT HAS MISSED BEFORE.", ("IN BOTH DIRECTIONS.", ACC)], size=100)
sc("For 2026 the", "forecast", "navy", yr=2026, fc=206.50, ac=202.90, d2=3.2)
sc("For 2022 it", "forecast", "navy", yr=2022, fc=158.50, ac=170.10, d2=5.0)
sc("Partly because Medicare", "photo", "pxb:pharmacy", lines=["MONEY SET ASIDE FOR", ("A NEW ALZHEIMER'S DRUG", ACC)], y=800, size=90)
sc("Then the drug's", "title", "px:pills", lines=["PRICE CUT.", ("COVERAGE LIMITED.", ACC)])
sc("Medicare didn't change", "title", "navy", kicker="2022", lines=["NO MID-YEAR CHANGE", ("TO THE PREMIUM", ACC)], size=100)
sc("Instead the next", "pxcount", "pxb:piggy", v=164.90, fmt=lambda v: f"${v:,.2f}", kicker="2023 PREMIUM WENT DOWN", label="FIRST DROP IN MORE THAN A DECADE", src="Source: CMS")
sc("So when the", "pxcount", "navy", v=209.50, fmt=lambda v: f"${v:,.2f}?", kicker="THE REAL 2027 NUMBER", label="MAY NOT BE EXACTLY THIS")
sc("And the day", "subscribe3", "navy", sub="THE DAY IT LANDS, I'LL BREAK IT DOWN")
sc("But for some", "question", "px:desk", lines=["THE STANDARD PREMIUM", "WON'T BE YOURS?"])
# CHAPTER 2
sc("Chapter 2", "chapter", "navy", num="CHAPTER 2", title="THE TAX RETURN THAT SETS YOUR BILL")
sc("If your income", "title", "px:calc", kicker="HIGHER INCOME?", lines=["A SURCHARGE ON PART B", ("AND YOUR DRUG PLAN", ACC)], size=96)
sc("It's called IRMAA", "title", "navy", lines=[("IRMAA", ACC)], size=220)
sc("Here's the part", "photo", "pxb:taxes", lines=["HERE'S THE PART", ("MOST PEOPLE MISS", ACC)], y=800)
sc("Your 2027 premium", "lookback", "navy")
sc("A return most", "photo", "pxb:taxform", lines=["A RETURN MOST PEOPLE", ("HAVE ALREADY FILED", ACC)], y=800, size=90)
sc("For 2026 the surcharge", "pxcount", "px:calc", v=109000, fmt=lambda v: f"${v:,.0f}", kicker="2026 · SURCHARGE STARTS ABOVE", label="SINGLE FILER · MAGI", src="Source: CMS / SSA")
sc("Or $218,000 for", "pxcount", "px:calc", v=218000, fmt=lambda v: f"${v:,.0f}", kicker="2026 · SURCHARGE STARTS ABOVE", label="MARRIED, FILING JOINTLY", src="Source: CMS / SSA")
sc("And it's a cliff", "photo", "pxb:cliff", lines=["AND IT'S", ("A CLIFF", ACC)], y=800)
sc("$1 over the", "cliff", "navy", d2=3.5)
sc("That's $81.20 more", "pxcount", "navy", v=81.20, fmt=lambda v: f"+${v:.2f}", kicker="MORE PER MONTH", label="EVERY MONTH. ALL YEAR.")
sc("And if you're married", "couple", "navy")
sc("So think about", "title", "px:calendar", kicker="THINK ABOUT", lines=[("2025", ACC)], size=220)
sc("Did you sell", "photo", "pxb:house", lines=["SOLD A HOUSE?"], y=800)
sc("Take a big", "photo", "pxb:jar", lines=["BIG RETIREMENT", ("WITHDRAWAL?", ACC)], y=800)
sc("Work a full", "photo", "pxb:clock", lines=["A FULL YEAR OF SALARY", ("BEFORE RETIRING?", ACC)], y=800, size=90)
sc("That one year", "title", "navy", lines=["ONE YEAR CAN SHOW UP", ("ON YOUR MEDICARE BILL", ACC)], size=100)
sc("There's a way", "title", "px:envelope", kicker="A WAY BACK", lines=["ASK SOCIAL SECURITY TO USE", ("YOUR NEWER, LOWER INCOME", ACC)], size=90)
sc("The form is", "title", "navy", kicker="THE FORM", lines=[("SSA-44", ACC)], size=220)
sc("It lists eight", "events", "navy", hl=["STOPPED WORKING", "WORK REDUCED", "DEATH OF A SPOUSE", "DIVORCE / ANNULMENT", "LOST EMPLOYER PENSION"])
sc("But a one-time", "nocount", "navy", d=[2.2, 3.4, 4.6, 6.0])
sc("So let me", "ask3", "px:kitchen")
# CHAPTER 3
sc("Chapter 3", "chapter", "navy", num="CHAPTER 3", title="THE CATCH FOR SMALLER CHECKS")
sc("This one surprises", "photo", "pxb:mailbox", lines=["IT SURPRISES PEOPLE", ("WHO THOUGHT THEY WERE PROTECTED", ACC)], y=800, size=80)
sc("There's a rule", "title", "navy", kicker="THE RULE", lines=[("HOLD HARMLESS", ACC)], size=160)
sc("For most people", "shield", "navy", kicker="IF PART B COMES OUT OF YOUR CHECK", lines=["A PREMIUM INCREASE CAN'T", ("SHRINK YOUR CHECK", ACC), "BELOW LAST YEAR'S"])
sc("This year in", "catchup", "navy")
sc("But that protection", "title", "navy", lines=["IT DOESN'T ERASE IT.", ("IT POSTPONES IT.", ACC)], size=100)
sc("When the next", "catchup", "navy", up=True)
sc("So if you", "title", "px:calendar", kicker="PROTECTED IN 2026?", lines=["YOUR 2027 INCREASE CAN BE", ("BIGGER THAN THE HEADLINE", ACC)], size=90)
sc("If your check", "notice", "navy", hl=1)
sc("If you're on", "subscribe3", "navy")
sc("And if a", "question", "px:piggy", lines=["SMALLER CHECK?", "THIS MATTERS MOST"])
# CHAPTER 4
sc("Chapter 4", "chapter", "navy", num="CHAPTER 4", title="THE PROGRAM THAT PAYS YOUR PREMIUM")
sc("It's called a", "title", "navy", lines=["MEDICARE", ("SAVINGS PROGRAM", ACC)], size=140)
sc("Every state runs", "msp", "navy")
sc("When that happens", "photo", "pxb:piggy2", lines=["THE PREMIUM STOPS COMING", ("OUT OF YOUR CHECK", ACC)], y=800, size=90)
sc("For most people that's", "pxcount", "navy", v=200, fmt=lambda v: f"≈ ${v:.0f}", kicker="STAYS IN YOUR CHECK", label="PER MONTH, FOR MOST PEOPLE")
sc("And it automatically", "photo", "pxb:pills", lines=["+ EXTRA HELP WITH", ("PRESCRIPTION DRUG COSTS", ACC)], y=800, size=90)
sc("Depending on the", "pxcount", "px:jar", v=3, fmt=lambda v: f"{v:.0f} MONTHS", kicker="DEPENDING ON THE PROGRAM, UP TO", label="OF PREMIUMS PAID BACK")
sc("The rules vary", "title", "navy", lines=["RULES VARY BY STATE", ("SOME HAVE NO SAVINGS LIMIT", ACC)], size=100)
sc("Medicare's own website", "quote", "navy", lines=["Even if you don't think you qualify,", "you should still apply."], who="— Medicare.gov")
sc("So what can", "question", "px:desk", lines=["WHAT CAN YOU DO", "WHILE WE WAIT?"])
# CHAPTER 5
sc("Chapter 5", "chapter", "navy", num="CHAPTER 5", title="WHAT TO DO THIS WEEK")
sc("If you have a My", "photo", "pxb:phone", lines=["TURN ON", ("TEXT OR EMAIL ALERTS", ACC)], y=800)
sc("Social Security says", "when", "navy", gap=5.5)
sc("If your 2025", "todo", "navy", d=[0, 0.3, 99, 99], done=1)
sc("If money is", "todo", "navy", d=[0, 0, 0.3, 99], done=2)
sc("If you have a drug", "todo", "navy", d=[0, 0, 0, 0.3], done=3)
sc("This video is", "title", "navy", lines=["GENERAL EDUCATION,", ("NOT ADVICE", ACC)], size=120)
sc("So back to", "pxcount", "pxb:calendar", v=209.50, fmt=lambda v: f"${v:,.2f}?", kicker="THE NUMBER EVERYONE IS WAITING FOR", label="IT MATTERS. BUT...")
sc("But for a lot", "title", "navy", lines=["THE TAX RETURN", "THE CATCH-UP", ("A PROGRAM YOU NEVER APPLIED FOR", ACC)], size=90)
sc("And when the", "subscribe3", "navy", sub="THE DAY THE NUMBER LANDS: FULL BREAKDOWN")
