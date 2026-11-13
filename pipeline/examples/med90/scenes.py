# Money Under Fire — "Is the Government Keeping Your Medicare Money? The $90 Check, Explained" (Fri 2026-11-13)
exec(open(os.path.join(ROOT, "common_kinds.py")).read())
TEAL = (30, 110, 80); STEELC = (40, 70, 130); AMBER = (150, 112, 20); GREY = (90, 100, 130)

def k_people(img, t, dur, a):
    """dot grid: each dot = 1 million Part B enrollees; 21 gold (got $90), rest grey"""
    d = ImageDraw.Draw(img)
    total, got = a.get("total", 63), a.get("got", 21)
    cols = 9; r = 30; gap = 82; x0 = W / 2 - (cols - 1) * gap / 2; y0 = 230
    shown = int(total * ease(t / 1.4))
    for i in range(shown):
        x = x0 + (i % cols) * gap; y = y0 + (i // cols) * gap
        col = ACC if (a.get("hl") and i < got) else (GREY if a.get("hl") else CREAM)
        d.ellipse([x - r, y - r, x + r, y + r], fill=col)
    slide_text(img, (W / 2, 150), a.get("kicker", ""), 46, t, 0, fill=SOFT, w="Bold")
    if a.get("label"): slide_text(img, (W / 2, 900 - 30), a["label"], 52, t, 1.2, fill=a.get("lcol", CREAM))

def k_checklist(img, t, dur, a):
    slide_text(img, (W / 2, 170), "TO GET THE $90, YOU HAD TO:", 54, t, 0, fill=ACC)
    for i, (s_, dl) in enumerate(a["items"]):
        p = back((t - dl) / 0.35)
        if p <= 0: continue
        y = 320 + i * 140; lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay); al = int(255 * clamp(p))
        d.ellipse([360, y - 42, 444, y + 42], fill=TEAL + (al,))
        d.line([(380, y), (397, y + 20), (426, y - 18)], fill=(255, 255, 255, al), width=12)
        d.text((490, y), s_, font=F(64), fill=CREAM + (al,), anchor="lm")
        img.alpha_composite(lay)

def k_nothing(img, t, dur, a):
    slide_text(img, (W / 2, 180), a.get("kicker", "GOT NOTHING"), 54, t, 0, fill=ACC)
    for i, (h_, s_, dl) in enumerate(a["items"]):
        cx = W / 2 + (i - (len(a["items"]) - 1) / 2) * 600
        card(img, cx, 500, 520, 260, t, dl, (STEELC, AMBER, GREY)[i], h_, s_)
        if t > dl + 0.5:
            pop_text(img, (cx, 740), "$0", 100, t, dl + 0.5, fill=ACC, stroke=6)

def k_premium(img, t, dur, a):
    d = ImageDraw.Draw(img)
    slide_text(img, (W / 2, 160), "STANDARD PART B PREMIUM · PER MONTH", 46, t, 0, fill=SOFT, w="Bold")
    for i, (yr, v, col) in enumerate([("2025", 185.0, GREY), ("2026", 202.90, ACC)]):
        x = 680 + i * 560; p = ease((t - 0.2 - i * 0.5) / 0.8); h = 470 * v / 210 * p
        d.rounded_rectangle([x - 150, 800 - h, x + 150, 800], 18, fill=col)
        slide_text(img, (x, 850), yr, 56, t, i * 0.5, fill=CREAM)
        if p > 0.3: slide_text(img, (x, 800 - h - 55), f"${v:,.2f}", 66, t, 0.4 + i * 0.5, fill=CREAM)
    if t > 1.8: pop_text(img, (960, 420), "+$17.90", 110, t, 1.8, fill=ACC, stroke=6)
    slide_text(img, (W / 2, 950 - 40), "Source: CMS", 28, t, 1.0, fill=SOFT, w="SemiBold")

def k_months(img, t, dur, a):
    d = ImageDraw.Draw(img)
    slide_text(img, (W / 2, 200), "THIS YEAR'S INCREASE: $17.90 × 12 MONTHS", 48, t, 0, fill=SOFT, w="Bold")
    for i in range(12):
        x = 330 + i * 110; p = ease((t - i * 0.06) / 0.4)
        if p <= 0: continue
        covered = t > 1.2 and i < 5
        d.rounded_rectangle([x, 380, x + 90, 560], 14, fill=TEAL if covered else (60, 70, 100))
        d.text((x + 45, 600), ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"][i], font=F(36, "Bold"), fill=SOFT, anchor="mm")
    if t > 1.2: slide_text(img, (W / 2, 720), "THE $90 COVERS ABOUT 5 MONTHS. ONCE.", 62, t, 1.2, fill=ACC)

def k_quarter25(img, t, dur, a):
    d = ImageDraw.Draw(img)
    cx, cy, r = 620, 520, 280
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(50, 62, 100))
    p = ease((t - 0.3) / 0.9)
    if p > 0: d.pieslice([cx - r, cy - r, cx + r, cy + r], -90, -90 + 90 * p, fill=ACC)
    d.ellipse([cx - 120, cy - 120, cx + 120, cy + 120], fill=(12, 26, 60))
    text(d, (cx, cy), f"{int(25 * p)}%", 90, fill=ACC)
    slide_text(img, (1300, 420), "PREMIUM = ABOUT", 56, t, 0.4, fill=CREAM)
    slide_text(img, (1300, 510), "1/4 OF PART B COSTS", 64, t, 0.6, fill=ACC)
    slide_text(img, (1300, 610), "set by law", 40, t, 0.8, fill=SOFT, w="Bold")

def k_ask(img, t, dur, a):
    p = back(t / 0.45); lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay); al = int(255 * clamp(p))
    ld.rounded_rectangle([340, 230, 1580, 720], 34, fill=CREAM + (al,))
    ld.text((W / 2, 320), "DID THE $90 SHOW UP?", font=F(60), fill=(15, 22, 45, al), anchor="mm")
    ld.rounded_rectangle([420, 450, 940, 640], 24, fill=TEAL + (al,)); ld.text((680, 545), "YES, I GOT IT", font=F(44), fill=(255, 255, 255, al), anchor="mm")
    ld.rounded_rectangle([980, 450, 1500, 640], 24, fill=STEELC + (al,)); ld.text((1240, 545), "I GOT NOTHING", font=F(44), fill=(255, 255, 255, al), anchor="mm")
    img.alpha_composite(lay)
    slide_text(img, (W / 2, 820), "TELL ME IN THE COMMENTS ↓", 56, t, 0.6, fill=ACC)

# ---------------- scenes ----------------
sc("Last month nearly", "pxcount", "pxb:checkpen", v=90, fmt=lambda v: f"${v:.0f}", kicker="NEARLY 21 MILLION GOT", disc=True)
sc("More than 40", "pxcount", "pxb:frank", v=40, fmt=lambda v: f"{v:.0f}M+", kicker="ON PART B, GOT", label="NOTHING")
sc("And the ones who", "pxcount", "pxb:bills", v=215, fmt=lambda v: f"+${v:.0f}", kicker="THEIR PREMIUM THIS YEAR", label="≈ A YEAR MORE")
sc("So is the government", "photo", "pxb:whitehouse", lines=["MONEY IN YOUR POCKET?", ("OR PAYING MORE?", ACC)], y=800)
sc("No politics", "title", "navy", lines=["NO POLITICS.", ("JUST YOUR CHECK.", ACC)])
sc("Chapter 1", "chapter", "navy", num="CHAPTER 1", title="THE $90")
sc("In early October", "title", "px:whitehouse", kicker="OCTOBER 2, 2026", lines=["ONE-TIME", ("$90 MEDICARE PAYMENT", ACC)])
sc("The next day", "photo", "pxb:envelope", lines=["NEXT DAY:", ("MEDICARE PUBLISHED THE DETAILS", ACC)], y=800, size=90)
sc("Most people who", "broll", "dark", clip="cash", kicker="AROUND OCTOBER 8", lines=["DIRECT DEPOSIT", ("FROM SOCIAL SECURITY", ACC)])
sc("Others got a", "photo", "pxb:check", lines=["OTHERS:", ("A PAPER CHECK", ACC)], y=800)
sc("But here's the part", "people", "navy", total=63, kicker="EACH DOT ≈ 1 MILLION PEOPLE WITH PART B", label="MORE THAN 60 MILLION")
sc("Medicare says only", "people", "navy", total=63, got=21, hl=True, kicker="GOLD = QUALIFIED FOR THE $90", label="ONLY ABOUT 21 MILLION", lcol=ACC)
sc("So who got", "question", "px:desk", lines=["SO WHO GOT", "LEFT OUT?"])
sc("Chapter 2", "chapter", "navy", num="CHAPTER 2", title="WHO GOT NOTHING")
sc("To get the", "checklist", "px:stetho", items=[("ORIGINAL MEDICARE + PART B", 2.3), ("LIVE IN THE U.S.", 4.2), ("NO MEDICAID PREMIUM HELP", 5.7), ("NO IRMAA SURCHARGE", 8.6)])
sc("That means if", "pxcount", "pxb:frank", v=0, fmt=lambda v: "$0", kicker="MEDICARE ADVANTAGE?", label="IN MEDICARE ADVANTAGE")
sc("even though Medicare", "title", "px:stetho", kicker="EVEN THOUGH", lines=["THEY GENERALLY STILL PAY", ("THE PART B PREMIUM", ACC)], size=90)
sc("If Medicaid helps", "nothing", "px:hospital", kicker="ALSO LEFT OUT", items=[("MEDICAID HELP", "premium already covered", 0.2), ("IRMAA", "≈ 8% of Part B", 4.0)])
sc("So let me ask", "ask", "px:kitchen")
sc("But the bigger", "broll", "dark", clip="calc", kicker="THE BIGGER STORY", lines=["IT'S", ("THE MATH", ACC)])
sc("Chapter 3", "chapter", "navy", num="CHAPTER 3", title="THE MATH")
sc("$90 sounds like", "photo", "pxb:piggy", lines=["$90 SOUNDS LIKE", ("MONEY BACK", ACC)], y=800)
sc("But this year", "premium", "navy")
sc("That's $17.90 more", "pxcount", "navy", v=17.90, fmt=lambda v: f"+${v:.2f}", kicker="MORE", label="EVERY MONTH")
sc("$214.80 a year", "pxcount", "pxb:bills", v=214.80, fmt=lambda v: f"+${v:,.2f}", kicker="EVERY YEAR", label="STANDARD PREMIUM INCREASE", src="Source: CMS · $17.90 × 12")
sc("The $90 covers", "months", "navy")
sc("And it didn't", "photo", "pxb:jar", lines=["NOT FROM YOUR PREMIUMS:", ("MEDICARE IMPROVEMENT FUND", ACC)], y=800, size=90)
sc("If you're within", "subscribe2", "navy")
sc("Now why does", "broll", "dark", clip="pills", kicker="WHY DOES IT KEEP RISING?", lines=["MEDICARE COSTS", ("GO UP", ACC)])
sc("By law the", "quarter25", "navy")
sc("And the 2027", "title", "px:calendar", kicker="NEXT UP", lines=["THE 2027 PREMIUM", ("NOT ANNOUNCED YET", ACC)])
sc("The trustees projected", "pxcount", "pxb:calendar", v=209.50, fmt=lambda v: f"${v:,.2f}", kicker="2027 PREMIUM · PROJECTED", label="PROJECTED, NOT OFFICIAL", src="2026 Medicare Trustees Report (projection)")
sc("That would be", "pxcount", "navy", v=6.60, fmt=lambda v: f"+${v:.2f}", kicker="PROJECTED INCREASE", label="PER MONTH")
sc("Which leaves the", "question", "px:desk", lines=["SHOULD YOU", "CHASE THE $90?"])
sc("Chapter 4", "chapter", "navy", num="CHAPTER 4", title="CHASE THE $90?")
sc("If you're in Medicare", "photo", "pxb:stetho", lines=["SWITCH PLANS", ("FOR $90?", ACC)], y=800)
sc("But as one", "title", "px:pills", kicker="WHAT MATTERS MORE", lines=["YOUR DOCTORS", "YOUR DRUGS", ("YOUR TOTAL COSTS", ACC)], size=96)
sc("And since the", "title", "navy", lines=["ALREADY SENT.", ("ONE TIME ONLY.", ACC)])
sc("This is education", "title", "navy", lines=["EDUCATION, NOT ADVICE.", ("EVERY PLAN IS DIFFERENT", ACC)], size=96)
sc("So back to", "broll", "dark", clip="flag", kicker="BACK TO THE QUESTION", lines=["KEEPING YOUR", ("MEDICARE MONEY?", ACC)])
sc("For nearly 21", "pxcount", "pxb:checkpen", v=90, fmt=lambda v: f"${v:.0f}", kicker="NEARLY 21 MILLION GOT", label="ONCE")
sc("And this year under", "pxcount", "pxb:bills", v=17.90, fmt=lambda v: f"+${v:.2f}", kicker="STANDARD PREMIUM, BY LAW", label="EVERY MONTH")
sc("And here's something", "photo", "pxb:frank", lines=["THIS WEEK:", ("CHECK YOUR OCTOBER STATEMENT", ACC)], y=800, size=90)
sc("Then ask yourself", "question", "px:kitchen", lines=["DID I KNOW WHICH", "GROUP I WAS IN?"])
