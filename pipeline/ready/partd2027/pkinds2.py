# "Editorial" look (2026-11-27, v2 after Mees: navy cards = same as videos nobody watched).
# Full-bleed real photos / b-roll + white paper cards, black type, red rules, yellow marker bands.
# exec'd AFTER common_kinds / ckinds / pkinds: overrides title, photo, note, options, tag, deadline, twonums, people, range, fork.
PW = (251, 249, 244); INK2 = (18, 20, 26); GRY = (112, 114, 122); RED2 = (204, 38, 30); GRN2 = (22, 128, 74); MARK = (255, 216, 0)

def _col(c):
    """map the old palette onto the paper palette"""
    if c in (WARN, (120, 54, 30), (150, 40, 30), RED): return RED2
    if c in (TEAL, (120, 220, 160), GREEN): return GRN2
    if c in (STEELC,): return (30, 60, 120)
    return INK2

def pcard(d, box, al, top=RED2, shadow=True):
    x0, y0, x1, y1 = box
    if shadow: d.rectangle([x0 + 14, y0 + 18, x1 + 14, y1 + 18], fill=(0, 0, 0, int(al * .42)))
    d.rectangle(box, fill=PW + (al,))
    if top: d.rectangle([x0, y0, x1, y0 + 12], fill=top + (al,))

def label(img, xy, s, t, delay=0, bgc=RED2, fg=(255, 255, 255), size=34, anchor="m"):
    """small solid label (kicker), slides in"""
    p = ease((t - delay) / 0.35)
    if p <= 0: return
    l, d = lay_(); f = F(size, "Black"); w = f.getlength(s); x, y = xy
    x0 = x - w / 2 - 22 if anchor == "m" else x
    al = int(255 * p); dx = -30 * (1 - p)
    d.rectangle([x0 + dx, y - size * 0.85, x0 + w + 44 + dx, y + size * 0.85], fill=bgc + (al,))
    d.text((x0 + 22 + dx, y), s, font=f, fill=fg + (al,), anchor="lm")
    img.alpha_composite(l)

def band(img, xy, s, size, t, delay=0, bgc=MARK, fg=INK2, anchor="m"):
    """marker band sweeps left->right, then the words appear on it"""
    q = clamp((t - delay) / 0.35)
    if q <= 0: return
    l, d = lay_(); f = F(size, "Black"); w = f.getlength(s); x, y = xy
    x0 = x - w / 2 - 26 if anchor == "m" else x
    d.rectangle([x0 + 10, y - size * 0.62 + 10, x0 + (w + 52) * ease(q) + 10, y + size * 0.62 + 10], fill=(0, 0, 0, 90))
    d.rectangle([x0, y - size * 0.62, x0 + (w + 52) * ease(q), y + size * 0.62], fill=bgc + (255,))
    if q > 0.45: d.text((x0 + 26, y + size * 0.04), s, font=f, fill=fg + (int(255 * clamp((q - 0.45) * 3)),), anchor="lm")
    img.alpha_composite(l)

def shadow_text(img, xy, s, size, t, delay=0, fill=(255, 255, 255), w="Black", anchor="mm"):
    p = ease((t - delay) / 0.4)
    if p <= 0: return
    l, d = lay_(); x, y = xy; y += 36 * (1 - p); al = int(255 * p)
    d.text((x + 5, y + 7), s, font=F(size, w), fill=(0, 0, 0, int(al * .75)), anchor=anchor)
    l = l.filter(ImageFilter.GaussianBlur(5)); d = ImageDraw.Draw(l)
    d.text((x, y), s, font=F(size, w), fill=fill + (al,), anchor=anchor, stroke_width=2, stroke_fill=(0, 0, 0, int(al * .6)))
    img.alpha_composite(l)

def _lines_block(img, t, a, cy):
    lines = a["lines"]; n = len(lines); gap = int(a.get("size", 120) * 1.25)
    y0 = cy - (n - 1) * gap / 2
    if a.get("kicker"): label(img, (W / 2, y0 - gap * 0.55 - 40), a["kicker"], t, 0, size=fit(a["kicker"], 36, 1500))
    for i, ln in enumerate(lines):
        s_, col = (ln, INK) if isinstance(ln, str) else ln
        size = fit(s_, a.get("size", 120), W - 260)
        if col in (GOLD, YEL): band(img, (W / 2, y0 + i * gap), s_, size, t, 0.15 + i * 0.25)
        elif col in (WARN, RED): band(img, (W / 2, y0 + i * gap), s_, size, t, 0.15 + i * 0.25, bgc=RED2, fg=(255, 255, 255))
        elif col == SOFT: shadow_text(img, (W / 2, y0 + i * gap), s_, size, t, 0.15 + i * 0.25, fill=(225, 228, 236))
        else: shadow_text(img, (W / 2, y0 + i * gap), s_, size, t, 0.1 + i * 0.25)

def k_title(img, t, dur, a): _lines_block(img, t, a, a.get("y", 470))
def k_photo(img, t, dur, a): _lines_block(img, t, a, a.get("y", 760))

def k_note(img, t, dur, a):
    p = back(t / 0.4); l, d = lay_(); al = int(255 * clamp(p)); oy = 40 * (1 - clamp(p))
    nl = len(a.get("lines", [])); y1 = 640 + nl * 58
    pcard(d, [380, 230 + oy, 1540, y1 + oy], al, top=_col(a.get("bcol", INK2)) if _col(a.get("bcol", INK2)) != INK2 else RED2)
    d.text((W / 2, 310 + oy), a["kicker"], font=F(fit(a["kicker"], 36, 1060, "Black"), "Black"), fill=GRY + (al,), anchor="mm")
    d.line([(480, 352 + oy), (1440, 352 + oy)], fill=(222, 218, 208, al), width=3)
    d.text((W / 2, 470 + oy), a["big"], font=F(fit(a["big"], 140, 1040)), fill=_col(a.get("bcol", INK2)) + (al,), anchor="mm")
    for i, ln in enumerate(a.get("lines", [])):
        d.text((W / 2, 600 + i * 58 + oy), ln, font=F(fit(ln, 40, 1040, "Bold"), "Bold"), fill=(60, 62, 70, al), anchor="mm")
    img.alpha_composite(l)
    src(img, a.get("src", ""))

def k_options(img, t, dur, a):
    label(img, (W / 2, 150), a.get("title", ""), t, 0, size=36)
    for i, (big, lab, sub, col) in enumerate(a["opts"]):
        cx = 600 + i * 720; dl = a.get("d", [0.3, 1.3])[i]; p = back((t - dl) / 0.4)
        if p <= 0: continue
        l, d = lay_(); al = int(255 * clamp(p)); oy = 40 * (1 - clamp(p)); c = _col(col) if _col(col) != INK2 else RED2
        pcard(d, [cx - 310, 270 + oy, cx + 310, 760 + oy], al, top=c)
        d.text((cx, 360 + oy), lab, font=F(fit(lab, 44, 540)), fill=GRY + (al,), anchor="mm")
        d.text((cx, 520 + oy), big, font=F(fit(big, 150, 540)), fill=INK2 + (al,), anchor="mm")
        d.text((cx, 670 + oy), sub, font=F(fit(sub, 40, 560, "Bold"), "Bold"), fill=c + (al,), anchor="mm")
        img.alpha_composite(l)
    src(img, a.get("srcl", ""))

def k_tag(img, t, dur, a):
    label(img, (W / 2, 140), a.get("kicker", "AVG STAND-ALONE DRUG PLAN PREMIUM · IF YOU KEEP YOUR PLAN"), t, 0, size=32)
    p = ease((t - a.get("d", 1.0)) / 0.9); v = 34 + 17 * p
    l, d = lay_(); cx, cy = W / 2 - 230, 500
    d.polygon([(cx - 330 + 14, cy - 170 + 18), (cx + 260 + 14, cy - 170 + 18), (cx + 380 + 14, cy + 18), (cx + 260 + 14, cy + 170 + 18), (cx - 330 + 14, cy + 170 + 18)], fill=(0, 0, 0, 100))
    d.polygon([(cx - 330, cy - 170), (cx + 260, cy - 170), (cx + 380, cy), (cx + 260, cy + 170), (cx - 330, cy + 170)], fill=PW + (255,))
    d.ellipse([cx + 230, cy - 26, cx + 282, cy + 26], fill=(40, 40, 46, 255))
    d.text((cx - 40, cy - 100), "PER MONTH", font=F(36, "Black"), fill=GRY + (255,), anchor="mm")
    d.text((cx - 40, cy + 25), f"${v:.0f}", font=F(180), fill=(RED2 if p > 0.5 else INK2) + (255,), anchor="mm")
    img.alpha_composite(l)
    if p >= 1:
        band(img, (cx + 760, cy - 40), "+50%", 140, t, a.get("d", 1.0) + 0.95, bgc=RED2, fg=(255, 255, 255))
        shadow_text(img, (cx + 760, cy + 90), "2026 → 2027", 46, t, a.get("d", 1.0) + 1.2)
    if a.get("sub") and t > a.get("ds", 2.4): band(img, (W / 2, 820), a["sub"], 46, t, a.get("ds", 2.4))
    src(img, a.get("srcl", "KFF, Oct 30, 2026 · stand-alone Part D plans (PDPs)"))

def k_deadline(img, t, dur, a):
    l, d = lay_(); p = back(t / 0.45); al = int(255 * clamp(p)); oy = 40 * (1 - clamp(p))
    x0, y0 = 610, 120 + oy
    pcard(d, [x0, y0, x0 + 700, y0 + 680], al, top=None)
    d.rectangle([x0, y0, x0 + 700, y0 + 140], fill=RED2 + (al,))
    d.text((x0 + 350, y0 + 72), "DECEMBER 2026", font=F(56), fill=(255, 255, 255, al), anchor="mm")
    import calendar as _c
    for i, nm in enumerate("MTWTFSS"):
        d.text((x0 + 60 + i * 97, y0 + 175), nm, font=F(26, "Black"), fill=GRY + (al,), anchor="mm")
    for day in range(1, 32):
        wd = _c.weekday(2026, 12, day); wk = (day + _c.weekday(2026, 12, 1) - 1) // 7
        x = x0 + 60 + wd * 97; y = y0 + 240 + wk * 88
        if day == 7 and t > 0.8:
            q = ease((t - 0.8) / 0.4); d.ellipse([x - 44 * q, y - 44 * q, x + 44 * q, y + 44 * q], fill=RED2 + (al,))
        d.text((x, y), str(day), font=F(40, "Bold"), fill=(((255, 255, 255) if t > 1.0 else RED2) if day == 7 else INK2) + (al,), anchor="mm")
    img.alpha_composite(l)
    sub_ = a.get("sub", "OPEN ENROLLMENT ENDS DECEMBER 7")
    if t > 1.4: band(img, (W / 2, 885), sub_, fit(sub_, 50, 1600), t, 1.4)
    src(img, a.get("srcl", "CMS press release, Sep 28, 2026"))

def k_twonums(img, t, dur, a):
    label(img, (W / 2, 140), "TWO REAL ANALYSES · TWO DIFFERENT QUESTIONS", t, 0, bgc=INK2, size=34)
    for i, (who, big, sub1, sub2, col) in enumerate([("KFF", "+50%", "$34 → $51", "if people keep their plan", RED2),
                                                     ("MEDICARE (CMS)", "< $1", "$35.09 → $36", "national average", GRN2)]):
        cx = 560 + i * 800; dl = a.get("d", [0.3, 1.4])[i]; p = back((t - dl) / 0.4)
        if p <= 0: continue
        l, d = lay_(); al = int(255 * clamp(p)); oy = 40 * (1 - clamp(p))
        pcard(d, [cx - 330, 240 + oy, cx + 330, 790 + oy], al, top=col)
        d.text((cx, 315 + oy), who, font=F(44, "Black"), fill=GRY + (al,), anchor="mm")
        d.text((cx, 480 + oy), big, font=F(180), fill=col + (al,), anchor="mm")
        d.text((cx, 630 + oy), sub1, font=F(62), fill=INK2 + (al,), anchor="mm")
        d.text((cx, 712 + oy), sub2, font=F(36, "Bold"), fill=GRY + (al,), anchor="mm")
        img.alpha_composite(l)
    if t > a.get("dv", 2.4):
        q = back((t - a.get("dv", 2.4)) / 0.35); l, d = lay_(); r = 70 * clamp(q)
        d.ellipse([W / 2 - r, 515 - r, W / 2 + r, 515 + r], fill=INK2 + (255,))
        if q > 0.5: d.text((W / 2, 515), "VS", font=F(54), fill=(255, 255, 255, 255), anchor="mm")
        img.alpha_composite(l)
    src(img, "KFF Oct 30, 2026 · CMS Sep 28, 2026 · stand-alone drug plans")

def k_people(img, t, dur, a):
    l, d = lay_(); p = back(t / 0.4); al = int(255 * clamp(p))
    pcard(d, [330, 170, 1590, 900], al, top=RED2)
    d.text((W / 2, 235), a.get("title", "13.6 MILLION PEOPLE IN STAND-ALONE PLANS, NO EXTRA HELP"), font=F(38, "Black"), fill=GRY + (al,), anchor="mm")
    img.alpha_composite(l); d = ImageDraw.Draw(img); n = a.get("n", 76)
    for i in range(100):
        r, c = divmod(i, 20); x = 418 + c * 57; y = 340 + r * 100; dl = 0.2 + i * 0.01
        if t < dl: continue
        on = i < n and t > a.get("dc", 1.6) + i * 0.012
        col = RED2 if on else (196, 192, 184)
        d.ellipse([x - 13, y - 42, x + 13, y - 16], fill=col); d.rounded_rectangle([x - 19, y - 11, x + 19, y + 36], 13, fill=col)
    if t > a.get("dc", 1.6):
        band(img, (W / 2, 832), a.get("big", "76% PAY MORE IF THEY CHANGE NOTHING"), 56, t, a.get("dc", 1.6) + 0.9, bgc=RED2, fg=(255, 255, 255))
    src(img, "KFF analysis, Oct 30, 2026")

def k_range(img, t, dur, a):
    label(img, (W / 2, 140), "THE 8 NATIONAL STAND-ALONE PLANS · AVG MONTHLY PREMIUM, 2027", t, 0, bgc=INK2, size=32)
    for i, (big, lab, col, dl) in enumerate([("$6.50", "CHEAPEST (AVG)", GRN2, 0.4), ("$204.50", "PRICIEST (AVG)", RED2, 1.5)]):
        cx = 600 + i * 720; p = back((t - dl) / 0.4)
        if p <= 0: continue
        l, d = lay_(); al = int(255 * clamp(p)); oy = 40 * (1 - clamp(p))
        pcard(d, [cx - 300, 280 + oy, cx + 300, 680 + oy], al, top=col)
        d.text((cx, 370 + oy), lab, font=F(40, "Black"), fill=GRY + (al,), anchor="mm")
        d.text((cx, 520 + oy), big, font=F(fit(big, 160, 540)), fill=col + (al,), anchor="mm")
        d.text((cx, 630 + oy), "per month", font=F(36, "Bold"), fill=GRY + (al,), anchor="mm")
        img.alpha_composite(l)
    if t > 2.4: band(img, (W / 2, 830), "CHEAPEST PREMIUM ≠ CHEAPEST PLAN FOR YOUR DRUGS", 50, t, 2.4)
    src(img, "KFF, Oct 30, 2026")

def k_fork(img, t, dur, a):
    band(img, (W / 2, 160), "BY DECEMBER 7", 70, t, 0, bgc=RED2, fg=(255, 255, 255))
    for i, (lab, sub, col) in enumerate([("COMPARE PLANS", "Medicare Plan Finder · SHIP counselors", GRN2), ("KEEP YOUR PLAN", "in most cases at its 2027 price · know the cost", (30, 60, 120))]):
        cx = 560 + i * 800; dl = 0.4 + i * 0.6; p = back((t - dl) / 0.4)
        if p <= 0: continue
        l, d = lay_(); al = int(255 * clamp(p)); oy = 40 * (1 - clamp(p))
        pcard(d, [cx - 340, 300 + oy, cx + 340, 660 + oy], al, top=col)
        d.text((cx, 440 + oy), lab, font=F(fit(lab, 72, 600)), fill=col + (al,), anchor="mm")
        d.text((cx, 550 + oy), sub, font=F(fit(sub, 34, 600, "Bold"), "Bold"), fill=GRY + (al,), anchor="mm")
        img.alpha_composite(l)
    if t > 1.0:
        l, d = lay_(); d.ellipse([W / 2 - 56, 480 - 56, W / 2 + 56, 480 + 56], fill=INK2 + (255,))
        d.text((W / 2, 480), "OR", font=F(44), fill=(255, 255, 255, 255), anchor="mm"); img.alpha_composite(l)
    src(img, "CMS, Sep 28, 2026")

def k_outro(img, t, dur, a):
    """end card: subscribe + room on the right for YouTube's end-screen video element (keep >= 5 s)"""
    shadow_text(img, (560, 250), "MONEY UNDER FIRE", 78, t, 0.0)
    shadow_text(img, (560, 330), "Social Security & Medicare, explained before the deadline", 32, t, 0.2, fill=(230, 232, 240), w="Bold")
    # subscribe button + cursor click
    p = back((t - 0.5) / 0.4)
    if p > 0:
        clicked = t > 1.9; l, d = lay_(); s = 1.0 - 0.06 * clamp(1 - abs(t - 1.9) / 0.12)
        bw, bh = 520 * s, 130 * s; cx, cy = 560, 520
        d.rounded_rectangle([cx - bw / 2 + 10, cy - bh / 2 + 14, cx + bw / 2 + 10, cy + bh / 2 + 14], 20, fill=(0, 0, 0, 110))
        d.rounded_rectangle([cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2], 20, fill=((90, 92, 100) if clicked else RED2) + (int(255 * clamp(p)),))
        d.text((cx, cy), "SUBSCRIBED ✓" if clicked else "SUBSCRIBE", font=F(fit("SUBSCRIBED ✓", 64, 460)), fill=(255, 255, 255, int(255 * clamp(p))), anchor="mm")
        # cursor glides to the button
        q = ease((t - 1.0) / 0.85); mx, my = 980 - 330 * q, 760 - 200 * q
        if t > 1.0:
            d.polygon([(mx, my), (mx, my + 62), (mx + 17, my + 47), (mx + 30, my + 74), (mx + 41, my + 69), (mx + 28, my + 43), (mx + 50, my + 43)], fill=(255, 255, 255, 255), outline=(0, 0, 0, 255))
        img.alpha_composite(l)
    if t > 2.3: band(img, (560, 700), "NEW VIDEOS MON · WED · FRI", 44, t, 2.3)
    if t > 2.7: shadow_text(img, (560, 790), "so the next deadline doesn't sneak up on you", 32, t, 2.7, fill=(230, 232, 240), w="Bold")
    # right: frame for the end-screen video
    q = back((t - 0.8) / 0.45)
    if q > 0:
        l, d = lay_(); al = int(255 * clamp(q)); x0, y0, x1, y1 = 1060, 300, 1800, 716
        d.rectangle([x0, y0, x1, y1], outline=(255, 255, 255, al), width=6)
        d.rectangle([x0 + 6, y0 + 6, x1 - 6, y1 - 6], fill=(0, 0, 0, int(al * .35)))
        img.alpha_composite(l)
        label(img, (1430, 260), "WATCH NEXT", t, 0.9, bgc=RED2, size=34)

_k_news_old = k_news
def k_news(img, t, dur, a):
    a2 = dict(a); ttl = a2.pop("title", "HOW THE NEWS REPORTED IT"); a2["title"] = ""
    _k_news_old(img, t, dur, a2); label(img, (W / 2, 140), ttl, t, 0, bgc=INK2, size=34)
