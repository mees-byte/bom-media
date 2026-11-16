# Money Under Fire — "Their Boss Said "Buy More." Then He Locked Their 401(k)." (Mon 2026-11-16)
exec(open(os.path.join(ROOT, "common_kinds.py")).read())
TEAL = (30, 110, 80); STEELC = (40, 70, 130); AMBER = (150, 112, 20); GREY = (90, 100, 130); REDC = (200, 40, 40)

def k_pie62(img, t, dur, a):
    d = ImageDraw.Draw(img)
    cx, cy, r = 620, 520, 290
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(50, 62, 100))
    p = ease((t - 0.3) / 1.0)
    if p > 0: d.pieslice([cx - r, cy - r, cx + r, cy + r], -90, -90 + 360 * 0.62 * p, fill=ACC)
    d.ellipse([cx - 130, cy - 130, cx + 130, cy + 130], fill=(12, 26, 60))
    text(d, (cx, cy), f"{int(62 * p)}%", 100, fill=ACC)
    slide_text(img, (1340, 400), "ENRON'S 401(k) PLAN", 54, t, 0.3, fill=CREAM)
    slide_text(img, (1340, 500), "IN ONE STOCK:", 54, t, 0.5, fill=CREAM)
    slide_text(img, (1340, 610), "ENRON", 110, t, 0.8, fill=ACC)
    slide_text(img, (W / 2, 900), "End of 2000 · Senate testimony, 2002", 28, t, 1.0, fill=SOFT, w="SemiBold")

def k_chat(img, t, dur, a):
    """reconstruction of the Sept 26, 2001 employee online forum, words from the DOJ trial-exhibit transcript"""
    p = back(t / 0.45); al = int(255 * clamp(p))
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    ld.rounded_rectangle([300, 170, 1620, 860], 26, fill=(245, 246, 250, al))
    ld.rounded_rectangle([300, 170, 1620, 260], 26, fill=(40, 70, 130, al)); ld.rectangle([300, 230, 1620, 260], fill=(40, 70, 130, al))
    ld.text((340, 215), "EMPLOYEE ONLINE FORUM · SEPT 26, 2001", font=F(38, "Bold"), fill=(255, 255, 255, al), anchor="lm")
    img.alpha_composite(lay)
    msgs = [("EMPLOYEES ASK.", "The chairman answers:", (90, 96, 120), 0.5),
            ("KEN LAY:", "\"The company is fundamentally sound.\"", (15, 22, 45), 1.3),
            ("KEN LAY:", "\"An incredible bargain.\"", REDC, a.get("d3", 3.5))]
    for i, (who, s_, col, dl) in enumerate(msgs):
        q = ease((t - dl) / 0.35)
        if q <= 0: continue
        y = 360 + i * 150
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay); aa = int(255 * q)
        ld.text((360, y), who, font=F(36, "Bold"), fill=(90, 96, 120, aa), anchor="lm")
        ld.text((360, y + 60), s_, font=F(fit(s_, 64, 1180)), fill=col + (aa,), anchor="lm")
        img.alpha_composite(lay)
    slide_text(img, (W / 2, 820), "Reconstruction · words from the trial-exhibit transcript (U.S. DOJ)", 28, t, 0.8, fill=(90, 96, 120), w="SemiBold")

def k_freeze(img, t, dur, a):
    d = ImageDraw.Draw(img)
    slide_text(img, (W / 2, 160), "ENRON STOCK DURING THE 401(k) FREEZE", 50, t, 0, fill=SOFT, w="Bold")
    p = ease((t - 0.4) / 2.2); v = 13.81 + (9.98 - 13.81) * p
    text(d, (W / 2, 470), f"${v:.2f}", 260, fill=CREAM if p < 1 else ACC, stroke=10)
    # padlock
    lp = back((t - 0.1) / 0.4)
    if lp > 0:
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay); s = clamp(lp); cx, cy = W / 2, 800
        ld.arc([cx - 70 * s, cy - 150 * s, cx + 70 * s, cy - 10 * s], 180, 360, fill=(220, 220, 230, 255), width=int(22 * s) or 1)
        ld.rounded_rectangle([cx - 110 * s, cy - 80 * s, cx + 110 * s, cy + 90 * s], 18, fill=ACC + (255,))
        ld.text((cx, cy + 5), "LOCKED", font=F(int(40 * s) or 1), fill=(15, 22, 45), anchor="mm")
        img.alpha_composite(lay)
    slide_text(img, (W / 2, 230), "Late Oct – mid-Nov 2001, by Enron's account", 30, t, 0.6, fill=SOFT, w="SemiBold")

def k_drop(img, t, dur, a):
    d = ImageDraw.Draw(img)
    slide_text(img, (W / 2, 220), "ONE WORKER'S 401(k)", 56, t, 0, fill=SOFT, w="Bold")
    p = ease((t - 1.6) / 1.6); v = 470 + (40 - 470) * p
    text(d, (W / 2, 500), f"${v:.0f},000", 250, fill=CREAM if p <= 0 else (ACC if p >= 1 else REDC), stroke=10)
    if p >= 1: slide_text(img, (W / 2, 730), "-91%", 90, t, 3.3, fill=REDC)
    slide_text(img, (W / 2, 140), "Source: CNN, 2001", 28, t, 0.6, fill=SOFT, w="SemiBold")

def k_timeline(img, t, dur, a):
    d = ImageDraw.Draw(img)
    ev = a["ev"]; n = len(ev); x0, x1, y = 220, 1700, 560
    p = ease(t / 0.8); d.rectangle([x0, y - 4, x0 + (x1 - x0) * p, y + 4], fill=SOFT)
    for i, (date, lab, dl, col) in enumerate(ev):
        x = x0 + (x1 - x0) * i / (n - 1); q = back((t - dl) / 0.35)
        if q <= 0: continue
        r = 22 * clamp(q); d.ellipse([x - r, y - r, x + r, y + r], fill=col)
        slide_text(img, (x, y - 90), date, 44, t, dl, fill=CREAM)
        slide_text(img, (x, y + 90), lab, fit(lab, 40, 360), t, dl + 0.1, fill=col, w="Bold")

def k_rules(img, t, dur, a):
    slide_text(img, (W / 2, 190), "WHAT CONGRESS CHANGED", 56, t, 0, fill=ACC)
    for i, (h_, s_, dl) in enumerate(a["items"]):
        cx = W / 2 + (i - 0.5) * 760
        card(img, cx, 560, 680, 360, t, dl, (STEELC, TEAL)[i], h_, s_)

def k_ask(img, t, dur, a):
    p = back(t / 0.45); lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay); al = int(255 * clamp(p))
    ld.rounded_rectangle([300, 230, 1620, 720], 34, fill=CREAM + (al,))
    ld.text((W / 2, 320), "YOUR COMPANY MATCH...", font=F(60), fill=(15, 22, 45, al), anchor="mm")
    ld.rounded_rectangle([380, 450, 940, 640], 24, fill=STEELC + (al,)); ld.text((660, 545), "PAID IN COMPANY STOCK", font=F(40), fill=(255, 255, 255, al), anchor="mm")
    ld.rounded_rectangle([980, 450, 1540, 640], 24, fill=TEAL + (al,)); ld.text((1260, 545), "PAID IN CASH / FUNDS", font=F(40), fill=(255, 255, 255, al), anchor="mm")
    img.alpha_composite(lay)
    slide_text(img, (W / 2, 820), "TELL ME IN THE COMMENTS ↓", 56, t, 0.6, fill=ACC)

def k_steps(img, t, dur, a):
    slide_text(img, (W / 2, 170), "CHECK YOUR 401(k)", 60, t, 0, fill=ACC)
    for i, (s_, dl) in enumerate(a["items"]):
        p = back((t - dl) / 0.35)
        if p <= 0: continue
        y = 340 + i * 160; lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay); al = int(255 * clamp(p))
        d.ellipse([330, y - 46, 422, y + 46], fill=TEAL + (al,))
        d.text((376, y), str(i + 1), font=F(56), fill=(255, 255, 255, al), anchor="mm")
        d.text((470, y), s_, font=F(64), fill=CREAM + (al,), anchor="lm")
        img.alpha_composite(lay)
    small(img, "For education only. Not financial advice.")

# ---------------- scenes ----------------
# HOOK: new picture every 1–3 s
sc("Your boss tells", "pxcount", "pxb:ticker", v=25, fmt=lambda v: f"${v:.0f}", kicker="YOUR BOSS SAYS THE STOCK IS", label="A BARGAIN", disc=True)
sc("so you keep", "photo", "pxb:jars", lines=["SO YOU KEEP", ("YOUR RETIREMENT IN IT", ACC)], y=800)
sc("Then your 401k", "photo", "pxb:lock", lines=["THEN YOUR 401(k)", ("GETS LOCKED", ACC)], y=800, size=120)
sc("and within weeks", "broll", "dark", clip="crash", kicker="WITHIN WEEKS", lines=["YOUR LIFE SAVINGS", ("ALMOST GONE", ACC)])
sc("That happened to", "photo", "pxb:tower", lines=["THOUSANDS OF WORKERS.", ("ONE OF AMERICA'S BIGGEST COMPANIES", ACC)], y=800, size=90)
sc("And the trap", "question", "px:worried", lines=["THE TRAP THEY FELL INTO?", "YOU CAN STILL FALL INTO IT TODAY"])
sc("Chapter 1", "chapter", "navy", num="CHAPTER 1", title="THE DREAM COMPANY")
sc("Enron, Houston", "photo", "pxb:houston", lines=["ENRON", ("HOUSTON, TEXAS", ACC)], y=820, size=130)
sc("In 2001, it", "pxcount", "pxb:tower2", v=7, fmt=lambda v: f"#{max(1, round(v))}", kicker="2001 FORTUNE 500", label="SEVENTH-BIGGEST COMPANY IN AMERICA")
sc("Its stock hit", "hero", "navy", **{"from": 0, "to": 90}, kicker="ENRON STOCK, AUGUST 2000", label="ABOUT $90 A SHARE", src="Peak close, Aug 2000")
sc("Working there felt", "broll", "dark", clip="tower", kicker="WORKING AT ENRON", lines=["FELT LIKE", ("WINNING THE LOTTERY", ACC)])
sc("When workers saved", "title", "px:coins", kicker="THE 401(k)", lines=["YOU SAVE.", ("ENRON MATCHES.", ACC)])
sc("But the match", "title", "px:ticker", kicker="THE CATCH", lines=["THE MATCH WAS PAID", ("IN ENRON STOCK", ACC)])
sc("and workers could", "pxcount", "pxb:coins", v=50, fmt=lambda v: f"{v:.0f}", kicker="CAN'T SELL THE MATCH UNTIL AGE", label="BEFORE THAT: STUCK")
sc("Many also bought", "photo", "pxb:money", lines=["MANY BOUGHT MORE", ("WITH THEIR OWN MONEY", ACC)], y=800)
sc("By 2001", "pie62", "navy")
sc("Chapter 2", "chapter", "navy", num="CHAPTER 2", title="THE BARGAIN")
sc("In August 2001", "title", "px:tower", kicker="AUGUST 14, 2001", lines=["THE CEO QUITS", ("AFTER 6 MONTHS", ACC)])
sc("quit after just", "pxcount", "pxb:tower", v=6, fmt=lambda v: f"{v:.0f}", kicker="SKILLING QUITS AFTER", label="MONTHS AS CEO")
sc("The stock kept", "photo", "pxb:chart", lines=["THE STOCK", ("KEEPS SLIDING", ACC)], y=800)
sc("On September 26", "chat", "px:laptop", d3=10.3)
sc("Here's what workers", "question", "px:letter", lines=["WHAT WORKERS", "DIDN'T SEE"])
sc("A vice president", "title", "px:letter", kicker="AUGUST 2001", lines=["A VICE PRESIDENT", ("WARNED LAY IN WRITING", ACC)], size=100)
sc("And according to", "pxcount", "pxb:money", v=1, fmt=lambda v: f"${v:.1f}B" if v < 1 else "$1B", kicker="INSIDERS SOLD ABOUT", label="OF STOCK, OVER A FEW YEARS", src="According to a shareholder lawsuit")
sc("Chapter 3", "chapter", "navy", num="CHAPTER 3", title="THE LOCKDOWN")
sc("On October 16", "pxcount", "pxb:chart", v=618, fmt=lambda v: f"-${v:.0f}M", kicker="OCTOBER 16, 2001", label="REPORTED LOSS")
sc("In the days", "broll", "dark", clip="crash", kicker="DAYS LATER", lines=["THE STOCK", ("FELL HARD", ACC)])
sc("And days later", "photo", "pxb:chain", lines=["THE 401(k) PLAN", ("WAS FROZEN", ACC)], y=800, size=120)
sc("Enron said it", "title", "px:files", kicker="ENRON'S EXPLANATION", lines=["A LONG-PLANNED SWITCH", ("TO A NEW PLAN ADMINISTRATOR", ACC)], size=90)
sc("Workers could not", "photo", "pxb:lock", lines=["CAN'T SELL.", ("NOT A SINGLE SHARE.", ACC)], y=800, size=120)
sc("By Enron's own", "freeze", "navy")
sc("Workers say it", "title", "px:worried", lines=["WORKERS SAY", ("IT STARTED EVEN EARLIER", ACC)])
sc("On December 2", "timeline", "navy", ev=[("AUG 2000", "$90 PEAK", 0.0, CREAM), ("SEPT 26", "\"A BARGAIN\"", 0.0, CREAM), ("OCT", "401(k) FROZEN", 0.0, CREAM), ("DEC 2, 2001", "BANKRUPT", 0.3, REDC)])
sc("By then, the", "photo", "pxb:bankrupt", lines=["STOCK:", ("UNDER $1", ACC)], y=820, size=130)
sc("One worker's 401k", "drop", "navy")
sc("Another retiree says", "pxcount", "pxb:worried", v=1.3, fmt=lambda v: f"${v:.1f}M", kicker="ANOTHER RETIREE SAYS HE LOST", label="")
sc("In total workers", "pxcount", "pxb:money", v=1, fmt=lambda v: "$1B+" if v > 0.95 else f"${v:.1f}B", kicker="WORKERS SAY THEY LOST", label="IN THEIR RETIREMENT PLANS", src="Claim in the workers' lawsuit")
sc("Chapter 4", "chapter", "navy", num="CHAPTER 4", title="WHAT CHANGED")
sc("Workers sued", "photo", "pxb:gavel", lines=["WORKERS SUED.", ("YEARS LATER: PART BACK", ACC)], y=820)
sc("An $85 million", "title", "px:gavel", kicker="SETTLEMENTS", lines=["$85M INSURANCE DEAL", ("$37.5M FROM THE TRUSTEE", ACC)], size=100)
sc("a fraction of", "title", "navy", lines=["A FRACTION", ("OF WHAT WAS LOST", ACC)])
sc("Congress changed the", "title", "px:gavel", lines=["CONGRESS", ("CHANGED THE RULES", ACC)])
sc("Since 2003", "pxcount", "pxb:letter", v=30, fmt=lambda v: f"{v:.0f} DAYS", kicker="SINCE 2003: BLACKOUT WARNING", label="AT LEAST, IN GENERAL")
sc("and since 2007", "rules", "navy", items=[("SINCE 2003", "30-day blackout notice", 0.1), ("SINCE 2007", "right to sell employer stock", 0.6)])
sc("including the company", "title", "px:coins", lines=["INCLUDING THE MATCH", ("AFTER 3 YEARS ON THE JOB", ACC)])
sc("Chapter 5", "chapter", "navy", num="CHAPTER 5", title="YOUR 401(k) TODAY")
sc("But here's the", "title", "px:calc", lines=["THE RULES CAN WARN YOU.", ("THEY CAN'T FORCE YOU TO SELL.", ACC)], size=96)
sc("Some workers, especially", "photo", "pxb:tower2", lines=["SOME WORKERS STILL HOLD", ("THEIR EMPLOYER'S STOCK", ACC)], y=800, size=96)
sc("Same company that", "title", "px:coins", lines=["SAME COMPANY: YOUR PAYCHECK", ("AND YOUR RETIREMENT", ACC)], size=96)
sc("So open your", "steps", "navy", items=[("OPEN YOUR STATEMENT", 0.1), ("HOW MUCH IS IN ONE COMPANY?", 1.6), ("BLACKOUT NOTICE? READ IT.", 3.8)])
sc("This is not", "subscribe2", "navy")
sc("Has your company", "ask", "px:jars")
