# Retirement Under Fire — Scam Files #1 TEST Short (content kept inside the centre 1080 px: cropped to a square for 9:16)
BGS["navy"] = make_bg((6, 14, 34), (20, 44, 92), 7)
CREAM = (246, 238, 220); SOFT = (170, 182, 205); ACC = GOLD
CX = W / 2; MW = 980
def lines_(img, t, ls, y, size=110, gap=None, d0=0.0, stroke=8):
    gap = gap or int(size * 1.15)
    for i, ln in enumerate(ls):
        s_, col = (ln, CREAM) if isinstance(ln, str) else ln
        sz = fit(s_, size, MW)
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
        p = back((t - d0 - i * 0.2) / 0.35)
        if p <= 0: continue
        ld.text((CX, y + i * gap), s_, font=F(max(8, int(sz * (0.7 + 0.3 * p)))), fill=col + (int(255 * clamp(p * 1.4)),), anchor="mm",
                stroke_width=stroke, stroke_fill=(0, 0, 0, int(255 * clamp(p))))
        img.alpha_composite(lay)
def k_big(img, t, dur, a):
    if a.get("dim"): img.alpha_composite(Image.new("RGBA", img.size, (4, 10, 28, a["dim"])))
    if a.get("kicker"): slide_text(img, (CX, a.get("y", 420) - 150), a["kicker"], 48, t, 0, fill=SOFT, w="Bold")
    lines_(img, t, a["lines"], a.get("y", 420), a.get("size", 120))
def k_call(img, t, dur, a):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    p = back(t / 0.4); s = 0.7 + 0.3 * clamp(p); al = int(255 * clamp(p))
    sh = 6 * math.sin(t * 40) if t < 1.6 else 0
    x0, y0 = CX - 260 * s + sh, 90
    d.rounded_rectangle([x0, y0, x0 + 520 * s, y0 + 780 * s], 60, fill=(20, 24, 36, al), outline=(200, 205, 220, al), width=8)
    d.text((CX + sh, y0 + 140 * s), "INCOMING CALL", font=F(int(36 * s), "Bold"), fill=SOFT + (al,), anchor="mm")
    d.text((CX + sh, y0 + 260 * s), "SOCIAL", font=F(int(70 * s)), fill=(255, 255, 255, al), anchor="mm")
    d.text((CX + sh, y0 + 340 * s), "SECURITY", font=F(int(70 * s)), fill=(255, 255, 255, al), anchor="mm")
    d.ellipse([CX - 190 * s + sh, y0 + 560 * s, CX - 70 * s + sh, y0 + 680 * s], fill=(200, 60, 50, al))
    d.ellipse([CX + 70 * s + sh, y0 + 560 * s, CX + 190 * s + sh, y0 + 680 * s], fill=(40, 170, 90, al))
    img.alpha_composite(lay)
    if t > 2.0: slide_text(img, (CX, 930 - 40), "", 10, t, 9)
def k_threat(img, t, dur, a):
    img.alpha_composite(Image.new("RGBA", img.size, (4, 10, 28, 120)))
    p = back(t / 0.4); lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay); al = int(255 * clamp(p))
    d.rounded_rectangle([CX - 480, 200, CX + 480, 640], 30, fill=CREAM + (al,))
    d.text((CX, 290), "“YOUR SOCIAL SECURITY", font=F(54), fill=(20, 30, 60, al), anchor="mm")
    d.text((CX, 370), "NUMBER HAS BEEN", font=F(54), fill=(20, 30, 60, al), anchor="mm")
    d.text((CX, 480), "SUSPENDED.”", font=F(96), fill=(150, 30, 30, al), anchor="mm")
    d.text((CX, 590), "— the scammer", font=F(34, "SemiBold"), fill=(90, 96, 120, al), anchor="mm")
    img.alpha_composite(lay)
def giftcard(d, x, y, col, al, rot=0):
    d.rounded_rectangle([x - 150, y - 95, x + 150, y + 95], 18, fill=col + (al,))
    d.rectangle([x - 150, y - 20, x + 150, y + 10], fill=(255, 255, 255, int(al * .5)))
    d.text((x, y + 55), "GIFT CARD", font=F(30), fill=(255, 255, 255, al), anchor="mm")
def k_gift(img, t, dur, a):
    for i, (col, x, y, r) in enumerate([((40, 110, 180), CX - 230, 330, 10), ((150, 112, 20), CX, 300, -6), ((30, 120, 80), CX + 230, 340, 8)]):
        p = back((t - i * 0.25) / 0.4)
        if p <= 0: continue
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); giftcard(ImageDraw.Draw(lay), x, y - 40 * (1 - clamp(p)), col, int(255 * clamp(p)))
        img.alpha_composite(lay.rotate(r, center=(x, y)))
    lines_(img, t, ["PAY TODAY", ("OR BE ARRESTED", ACC)], 620, 100, d0=1.0)
def k_never(img, t, dur, a):
    slide_text(img, (CX, 140), "SOCIAL SECURITY WILL NEVER:", 52, t, 0, fill=ACC)
    items = [("SUSPEND YOUR SSN", 0.2), ("THREATEN ARREST", 3.9), ("ASK FOR GIFT CARDS,", 6.1), ("WIRES, CRYPTO OR CASH", 6.4)]
    for i, (s_, dl) in enumerate(items):
        p = back((t - dl) / 0.35)
        if p <= 0: continue
        y = 300 + i * 150
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay); al = int(255 * clamp(p))
        if i != 3:
            d.ellipse([CX - 470, y - 45, CX - 380, y + 45], fill=(150, 112, 20, al))
            d.line([(CX - 450, y - 25), (CX - 400, y + 25)], fill=(255, 255, 255, al), width=12)
            d.line([(CX - 450, y + 25), (CX - 400, y - 25)], fill=(255, 255, 255, al), width=12)
        d.text((CX - 340, y), s_, font=F(fit(s_, 76, 800)), fill=CREAM + (al,), anchor="lm")
        img.alpha_composite(lay)
    small_src = "Source: Social Security Administration"
    slide_text(img, (CX, 880), small_src, 30, t, 1.0, fill=SOFT, w="SemiBold")

sc("Can you spot", "big", "pxb:hands", lines=["CAN YOU SPOT", ("THE SCAM?", ACC)], y=380, size=130, dim=60)
sc("Your phone rings", "call", "navy")
sc("A voice says", "threat", "px:oldphone")
sc("Pay a fee", "gift", "navy")
sc("Here's the rule", "big", "navy", lines=["HERE'S", ("THE RULE", ACC)], size=150)
sc("Social Security says", "never", "navy")
sc("And that caller", "big", "px:phone", kicker="AND THAT CALLER ID?", lines=["SCAMMERS", ("CAN FAKE IT", ACC)], size=130)
sc("If a call asks", "big", "pxb:lock", lines=["ANY OF THOSE?", ("IT'S A SCAM.", ACC), "EVERY TIME."], size=120, y=300, dim=110)
sc("Hang up and", "big", "navy", lines=["HANG UP.", ("CALL SOCIAL SECURITY", ACC), ("YOURSELF.", ACC)], size=110, y=330)
sc("You can report", "big", "navy", kicker="REPORT IT", lines=[("oig.ssa.gov", ACC)], size=130)
sc("Who in your", "big", "pxb:family", lines=["WHO IN YOUR FAMILY", ("NEEDS THIS RULE?", ACC)], y=380, size=110, dim=90)
