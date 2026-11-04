# Scene list — Binance $6.3B hack (Fri 2026-11-06)
ICE = (120, 200, 255)
WHITE = (250, 250, 252)
CIRCLE_LOGO = "circle" if os.path.exists(os.path.join(ROOT, "logos", "circle.png")) else None

# ---------- story-specific kinds ----------
def k_clock(img, t, dur, a):
    """digital clock that ticks up to a timestamp"""
    d = ImageDraw.Draw(img)
    hh, mm = a["time"].split(":")
    m0 = int(mm) - a.get("roll", 5)
    p = ease(t / 0.9)
    cur = int(m0 + (int(mm) - m0) * p)
    s = f"{hh}:{max(cur,0):02d}"
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    ld.rounded_rectangle([W/2-520, 260, W/2+520, 640], 40, fill=(0, 0, 0, 170), outline=RED + (255,), width=6)
    img.alpha_composite(lay)
    text(d, (W/2, 450), s, 260, fill=RED if p >= 1 else INK)
    if int(t * 2) % 2 == 0: d.ellipse([W/2+440, 290, W/2+480, 330], fill=RED)
    slide_text(img, (W/2, 720), a.get("label", "UTC"), 56, t, 0.4, fill=GOLD)
    if a.get("sub"): slide_text(img, (W/2, 800), a["sub"], 40, t, 0.6, fill=MUT, w="Bold")

def k_timer(img, t, dur, a):
    """stopwatch running to 20 minutes"""
    d = ImageDraw.Draw(img)
    cx, cy, r = W/2, 450, 250
    d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=INK, width=14)
    d.rectangle([cx-30, cy-r-60, cx+30, cy-r-10], fill=INK)
    p = ease(t / 1.6)
    d.pieslice([cx-r+25, cy-r+25, cx+r-25, cy+r-25], -90, -90 + 360 * (20/60) * p, fill=RED)
    d.ellipse([cx-150, cy-150, cx+150, cy+150], fill=BG)
    text(d, (cx, cy-10), f"{int(20*p)}", 170, fill=INK)
    text(d, (cx, cy+95), "MINUTES", 40, fill=MUT, w="Bold")
    slide_text(img, (W/2, 790), "MOST OF THE MONEY: GONE", 60, t, 0.6, fill=GOLD)

def wallet_icon(d, cx, cy, s, col, a=255):
    d.rounded_rectangle([cx-110*s, cy-75*s, cx+110*s, cy+75*s], int(20*s), fill=col + (a,))
    d.rounded_rectangle([cx+40*s, cy-28*s, cx+125*s, cy+28*s], int(12*s), fill=mix(col, (0, 0, 0), .35) + (a,))
    d.ellipse([cx+62*s, cy-10*s, cx+82*s, cy+10*s], fill=(255, 255, 255, a))

def k_mixer(img, t, dur, a):
    """coins swirl through a mixer into a fresh wallet"""
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    cx, cy = 700, 470
    for k in range(3):
        r = 200 - k * 55
        d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=MUT + (180,), width=6)
    for i in range(9):
        ang = t * 4 + i * 0.7
        rr = 190 - (i % 3) * 55
        x, y = cx + rr * math.cos(ang), cy + rr * math.sin(ang)
        d.ellipse([x-22, y-22, x+22, y+22], fill=GOLD + (255,))
    p = ease((t - 0.4) / 0.8)
    if p > 0:
        x = cx + 230 + 300 * p
        d.ellipse([x-22, cy-22, x+22, cy+22], fill=GOLD + (255,))
    wallet_icon(d, 1400, cy, 1.3, (60, 70, 100), int(255 * clamp(t / 0.4)))
    img.alpha_composite(lay)
    slide_text(img, (cx, 760), "TORNADO CASH", 60, t, 0.2, fill=INK)
    slide_text(img, (cx, 830), "a crypto mixer", 40, t, 0.4, fill=MUT, w="Bold")
    slide_text(img, (1400, 700), "FRESH WALLET", 54, t, 0.5, fill=GOLD)

def k_rehearsal(img, t, dur, a):
    d = ImageDraw.Draw(img)
    labels = ["TEST 1", "TEST 2", "REHEARSAL"]
    for i, lab in enumerate(labels):
        x = 460 + i * 500
        p = back((t - i * 0.45) / 0.4)
        if p <= 0: continue
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
        wallet_icon(ld, x, 430, 1.1 * (0.6 + 0.4 * clamp(p)), (60, 70, 100), int(255 * clamp(p)))
        img.alpha_composite(lay)
        slide_text(img, (x, 610), lab, 52, t, i * 0.45 + 0.1, fill=GOLD if i == 2 else INK)
        if t > i * 0.45 + 0.4:
            d.line([(x-40, 700), (x-10, 735), (x+50, 665)], fill=GREEN, width=14)
    slide_text(img, (W/2, 230), "PRACTICE WALLETS", 50, t, 0, fill=MUT, w="Bold")

def k_chains(img, t, dur, a):
    names = ["ETHEREUM", "BITCOIN", "TRON", "XRP", "SOLANA", "ARBITRUM", "OPTIMISM", "BASE", "AVALANCHE", "POLYGON"]
    for i, nm in enumerate(names):
        x = 280 + (i % 5) * 340; y = 400 + (i // 5) * 230
        hit = t > 0.25 + i * 0.15
        card(img, x, y, 320, 180, t, i * 0.08, (150, 14, 24) if hit else (40, 50, 80), nm, "HIT" if hit else None)
    pop_text(img, (W/2, 180), "10 BLOCKCHAINS", 110, t, 0, fill=INK)

def k_slip(img, t, dur, a):
    """one signed permission slip"""
    p = back(t / 0.45)
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    al = int(255 * clamp(p)); s = 0.6 + 0.4 * clamp(p)
    ld.rounded_rectangle([W/2-470*s, 450-250*s, W/2+470*s, 450+250*s], 24, fill=(245, 240, 225, al))
    ld.text((W/2, 450-170*s), "PERMISSION SLIP", font=F(int(64*s)), fill=(30, 30, 40, al), anchor="mm")
    ld.text((W/2, 450-40*s), "WALLET  →  CODE", font=F(int(80*s)), fill=BLUE + (al,), anchor="mm")
    ld.line([(W/2-300*s, 450+130*s), (W/2+300*s, 450+130*s)], fill=(30, 30, 40, al), width=4)
    img.alpha_composite(lay)
    q = ease((t - 0.7) / 0.6)
    if q > 0:
        d = ImageDraw.Draw(img)
        pts = [(W/2-260+520*u/20, 450+100 - 30*math.sin(u*1.3)) for u in range(int(20*q)+1)]
        if len(pts) > 1: d.line(pts, fill=(20, 40, 140), width=8)
    slide_text(img, (W/2, 790), "“EIP-7702”", 54, t, 0.5, fill=GOLD)

def k_counter(img, t, dur, a):
    d = ImageDraw.Draw(img)
    n = 18914775 + int(t * 6)
    slide_text(img, (W/2, 290), "WALLET COUNTER (NONCE)", 50, t, 0, fill=MUT, w="Bold")
    text(d, (W/2, 470), f"{n:,}", 190, fill=INK)
    for i in range(3):
        y = 610 + i * 0
    slide_text(img, (W/2, 680), "KEPT MOVING", 80, t, 0.3, fill=GOLD)

def k_slips(img, t, dur, a):
    """fan of 50 permission slips; optional: one matches"""
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    hl = a.get("hl"); win = 31
    n = 50 if hl else int(50 * ease(t / 1.4))
    for i in range(n):
        col_i, row = i % 10, i // 10
        x = 290 + col_i * 150; y = 200 + row * 120
        match = hl and i == win
        fade = 255 if (not hl or match or t < 0.5) else int(255 * (1 - 0.75 * clamp((t - 0.5) / 0.6)))
        fill = (90, 220, 130) if (match and t > 0.5) else (245, 240, 225)
        ld.rounded_rectangle([x-62, y-45, x+62, y+45], 10, fill=fill + (fade,))
        ld.line([(x-40, y+15), (x+40, y+15)], fill=(40, 40, 50, fade), width=3)
        ld.text((x, y-12), f"#{i+1}", font=F(28, "Bold"), fill=(40, 40, 50, fade), anchor="mm")
    img.alpha_composite(lay)
    if hl:
        pop_text(img, (W/2, 860), "ONE MATCHED", 80, t, 0.6, fill=GREEN, stroke=6)
    else:
        slide_text(img, (W/2, 860), f"{n} PRE-SIGNED SLIPS", 70, t, 0, fill=GOLD)

def k_laptop(img, t, dur, a):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    p = back(t / 0.45); s = 0.6 + 0.4 * clamp(p); al = int(255 * clamp(p))
    cx, cy = W/2, 430
    d.rounded_rectangle([cx-330*s, cy-210*s, cx+330*s, cy+190*s], 20, fill=(70, 76, 96, al))
    scr = RED if int(t * 3) % 2 == 0 and t > 0.6 else (20, 26, 44)
    d.rectangle([cx-300*s, cy-185*s, cx+300*s, cy+165*s], fill=scr + (al,))
    d.polygon([(cx-420*s, cy+190*s), (cx+420*s, cy+190*s), (cx+470*s, cy+230*s), (cx-470*s, cy+230*s)], fill=(110, 116, 136, al))
    d.text((cx, cy-10), "⚠", font=F(int(160*s)), fill=(255, 255, 255, al), anchor="mm")
    img.alpha_composite(lay)
    slide_text(img, (W/2, 760), "ONE ENGINEER’S LAPTOP?", 64, t, 0.4, fill=GOLD)
    slide_text(img, (W/2, 840), "Binance’s first explanation", 40, t, 0.6, fill=MUT, w="Bold")

def k_freeze(img, t, dur, a):
    """amount gets iced over with a lock"""
    d = ImageDraw.Draw(img)
    if a.get("logo"): logo(img, a["logo"], W/2, 230, 340, t, 0, plate=WHITE, maxh=110)
    elif a.get("who"): slide_text(img, (W/2, 230), a["who"], 70, t, 0, fill=INK)
    p = ease(t / 1.0)
    v = a["v"] * p
    size = fit(a["fmt"], 200, W - 300)
    col = mix(GOLD, ICE, clamp((t - 1.0) / 0.4))
    text(d, (W/2, 500), money(v) if p < 1 else a["fmt"], size, fill=col)
    q = ease((t - 1.0) / 0.4)
    if q > 0:
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
        ld.rounded_rectangle([280, 370, W-280, 630], 30, fill=ICE + (int(70 * q),), outline=ICE + (int(255 * q),), width=6)
        lx, ly = W - 330, 380
        ld.rounded_rectangle([lx-60, ly-10, lx+60, ly+80], 12, fill=ICE + (int(255 * q),))
        ld.arc([lx-40, ly-70, lx+40, ly+20], 180, 360, fill=ICE + (int(255 * q),), width=14)
        img.alpha_composite(lay)
        pop_text(img, (W/2, 730), "FROZEN", 100, t, 1.0, fill=ICE, stroke=6)
    if a.get("sub"): slide_text(img, (W/2, 840), a["sub"], 42, t, 0.4, fill=MUT, w="Bold")

def k_comment2(img, t, dur, a):
    p = back(t / 0.45)
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    al = int(255 * clamp(p))
    ld.rounded_rectangle([360, 240, 1560, 720], 34, fill=(255, 255, 255, al))
    ld.ellipse([420, 300, 520, 400], fill=GOLD + (al,))
    ld.text((470, 350), "?", font=F(60), fill=(15, 18, 30, al), anchor="mm")
    ld.text((560, 325), "A FREEZE BUTTON IS…", font=F(48), fill=(15, 18, 30, al), anchor="lt")
    ld.rounded_rectangle([440, 460, 940, 630], 24, fill=BLUE + (al,))
    ld.text((690, 545), "PROTECTION", font=F(46), fill=(255, 255, 255, al), anchor="mm")
    ld.rounded_rectangle([980, 460, 1480, 630], 24, fill=RED + (al,))
    ld.text((1230, 545), "A BROKEN PROMISE", font=F(40), fill=(255, 255, 255, al), anchor="mm")
    img.alpha_composite(lay)
    slide_text(img, (W/2, 820), "TELL ME IN THE COMMENTS ↓", 56, t, 0.6, fill=GOLD)

def k_bars(img, t, dur, a):
    """real numbers only: frozen vs. got away"""
    d = ImageDraw.Draw(img)
    items = a["items"]; mx = max(v for _, v, _ in items)
    for i, (lab, v, col) in enumerate(items):
        y = 360 + i * 230
        p = ease((t - 0.2 - i * 0.35) / 0.9)
        slide_text(img, (260, y - 70), lab, 46, t, i * 0.35, fill=col, anchor="lm")
        wmax = 1100 * v / mx
        if p > 0:
            d.rounded_rectangle([260, y - 30, 260 + max(20, wmax * p), y + 50], 16, fill=col)
            text(d, (260 + wmax * p + 40, y + 10), money(v * p) if p < 1 else a["labels"][i], 70, fill=INK, anchor="lm")
    if a.get("foot"): slide_text(img, (W/2, 860), a["foot"], 40, t, 1.0, fill=MUT, w="Bold")

def k_price(img, t, dur, a):
    d = ImageDraw.Draw(img)
    logo(img, "bitcoin", W/2, 230, 480, t, 0, plate=WHITE, maxh=110)
    pop_text(img, (W/2 - 60, 520), "BELOW $77,000", 150, t, 0.3, fill=RED, stroke=6)
    p = ease((t - 0.6) / 0.6)
    if p > 0:
        x = 1720
        d.line([(x, 380), (x, 380 + 220 * p)], fill=RED, width=26)
        if p > 0.9: d.polygon([(x - 50, 600), (x + 50, 600), (x, 680)], fill=RED)
    slide_text(img, (W/2, 760), "in the days after the hack", 46, t, 0.8, fill=MUT, w="Bold")

def k_versus(img, t, dur, a):
    d = ImageDraw.Draw(img)
    logo(img, "binance", W/2, 200, 130, t, 0, plate=WHITE, maxh=110)
    for i, (yr, amt, col) in enumerate([("2019", "$40M", MUT), ("2026", "$6.3B", RED)]):
        x = 560 + i * 800
        slide_text(img, (x, 400), yr, 70, t, i * 0.5, fill=INK)
        pop_text(img, (x, 560), amt, 170 if i else 120, t, 0.2 + i * 0.5, fill=col, stroke=5 if i else 0)
    slide_text(img, (W/2, 480), "→", 120, t, 0.4, fill=GOLD)
    slide_text(img, (W/2, 780), "STOLEN FROM BINANCE", 54, t, 0.9, fill=GOLD)

def k_group(img, t, dur, a):
    """hacker group card (no real faces): hooded silhouette"""
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    p = back(t / 0.4); al = int(255 * clamp(p)); x = W/2
    d.ellipse([x-120, 230, x+120, 470], fill=(30, 34, 48, al), outline=RED + (al,), width=8)
    d.pieslice([x-85, 270, x+85, 440], 180, 360, fill=(8, 10, 18, al))
    d.ellipse([x-55, 300, x+55, 420], fill=(8, 10, 18, al))
    d.pieslice([x-110, 410, x+110, 590], 180, 360, fill=(8, 10, 18, al))
    img.alpha_composite(lay)
    pop_text(img, (W/2, 610), "TRADERTRAITOR", 100, t, 0.2, fill=INK)
    slide_text(img, (W/2, 710), "North Korean state hacking group", 46, t, 0.5, fill=MUT, w="Bold")
    slide_text(img, (W/2, 810), "NAMED BY THE FBI", 56, t, 0.8, fill=GOLD)

# ---------- scenes ----------
sc(None, "date", "pxb:night_0", date="OCT 29, 2026", place="THE BIGGEST CRYPTO HEIST EVER")
sc("took six point", "count", "px:vault_1", v=6.3e9, kicker="STOLEN", label="in a single evening", col=INK)
sc("Binance, the world's", "title", "px:night_3", logo="binance", plate=WHITE, lines=["THE WORLD’S BIGGEST", ("CRYPTO EXCHANGE", GOLD)], size=110)
sc("Most of it", "timer", "px:clock_3")
sc("It's the largest", "title", "px:alarm_1", lines=["LARGEST CRYPTO THEFT", ("EVER RECORDED", GOLD)], size=120)
sc("But the strangest", "title", "dark", kicker="THE STRANGEST PART", lines=["NOT HOW MUCH", "THEY TOOK…"], size=130)
sc("It's how much", "title", "px:lock_3", lines=["…BUT HOW MUCH", ("THEY CAN’T SPEND", GOLD)], size=130)
sc("By the end", "question", "px:chess_3", lines=["WHY WAS ALMOST HALF", "FROZEN WITHIN HOURS?"])
sc("and who still", "title", "px:vault_2", lines=["WHO STILL HOLDS", ("THE REST?", RED)], size=140)
sc("To understand the", "chapter", "gold", num="CHAPTER 1", title="THE SETUP")
sc("The attacker funded", "broll", "dark", clip="code", kicker="36+ HOURS BEFORE", lines=["A FRESH", ("WALLET", GOLD)])
sc("small withdrawals from", "mixer", "px:keyboard_2")
sc("The attack code", "rehearsal", "px:code_2")
sc("then rehearsed one", "photo", "pxb:keyboard_1", lines=["ONE FINAL", ("REHEARSAL", GOLD)], size=150)
sc("At five past", "clock", "px:server_0", time="20:05", label="OCTOBER 29 · UTC")
sc("the real thing", "broll", "dark", clip="servers", kicker="20:05 UTC", lines=["IT", ("BEGINS", GOLD)])
sc("First, five Binance", "title", "px:server_3", logo="binance", plate=WHITE, lines=["5 BINANCE", ("WALLETS", GOLD)], size=150)
sc("two hundred and thirty-three", "count", "px:server_3", v=233e6, fmt=lambda v: f"{v/1e6:,.0f}M XRP", kicker="SENT OUT FIRST", col=GOLD)
sc("Minutes later, a", "clock", "px:night_0", time="20:20", roll=15, label="A BITCOIN WALLET")
sc("eighteen thousand two", "count", "px:coins_0", v=18270, logo="bitcoin", plate=WHITE, fmt=lambda v: f"{v:,.0f} BTC", col=GOLD)
sc("That alone was", "count", "px:cash_1", v=1.47e9, kicker="THAT ALONE", fmt=lambda v: f"${v/1e9:.2f}B", label="value at the time of the theft", col=INK)
sc("In total, ten", "chains", "px:server_0")
sc("So how do", "chapter", "blue", num="CHAPTER 2", title="THE TRICK")
sc("On Ethereum, the", "title", "px:code_0", logo="ethereum", plate=WHITE, lines=[("EIP-7702", GOLD)], size=220, y=560)
sc("It lets a", "slip", "px:signature_3")
sc("But Binance's wallet", "broll", "dark", clip="screen", kicker="THE PROBLEM", lines=["THE WALLET WAS STILL", ("PROCESSING WITHDRAWALS", GOLD)])
sc("so its counter", "counter", "px:code_2")
sc("The attacker's answer?", "title", "red", lines=["THE ANSWER?"], size=200)
sc("Fifty pre-signed permission", "slips", "dark")
sc("Only ONE had", "slips", "dark", hl=True)
sc("One transaction moved", "count", "px:code_0", v=2.5e9, logo="ethereum", plate=WHITE, kicker="IN ONE TRANSACTION", fmt=lambda v: f"~${v/1e9:.1f}B", col=INK)
sc("Binance first said", "laptop", "px:keyboard_2")
sc("Later it found", "title", "px:lock_3", logo="binance", plate=WHITE, lines=["MORE POINTS", ("OF BREACH", RED)], size=150)
sc("And then crypto", "chapter", "red", num="CHAPTER 3", title="THE FREEZE")
sc("It hit the", "broll", "dark", clip="ice", dim=0.5, lines=["CRYPTO", ("HIT THE BRAKES", GOLD)])
sc("At one minute", "clock", "px:clock_3", time="21:01", roll=10, label="UTC", sub="56 minutes after it began")
sc("Tether froze nine", "freeze", "px:ice_1", logo="tether", v=971e6, fmt="$971M", sub="stolen USDT stablecoins")
sc("Three minutes later, Circle", "freeze", "px:ice_3", logo=CIRCLE_LOGO, who="CIRCLE", v=823e6, fmt="$823M", sub="stolen USDC stablecoins · 21:04 UTC")
sc("By half past", "count", "px:ice_2", v=2.7e9, kicker="FROZEN BY 00:30 UTC", fmt=lambda v: f"~${v/1e9:.1f}B", label="about 2.7 billion dollars locked", col=ICE)
sc("The thief rushed", "broll", "dark", clip="city", lines=["THE THIEF", ("RUSHED", RED)])
sc("at a discount", "title", "px:cash_1", kicker="DUMPED COINS AT A DISCOUNT OF", lines=[(">10%", GOLD)], size=260, y=540)
sc("So here's the", "title", "gold", lines=["THE DILEMMA"], size=200)
sc("If a company", "title", "px:lock_3", lines=["IF THEY CAN FREEZE A THIEF’S MONEY…", ("THEY CAN FREEZE YOURS", GOLD)], size=90)
sc("Is that protection", "comment2", "dark")
sc("If you want", "title", "dark", kicker="THE NEXT STORY", lines=["MONEY VANISHING", ("FASTER THAN ANYONE CAN REACT", GOLD)], size=90)
sc("money vanishing faster", "subscribe", "dark")
sc("New stories every", "title", "dark", kicker="NEW STORIES", lines=["MONDAY", "WEDNESDAY", ("FRIDAY", GOLD)], size=110)
sc("But what couldn't", "chapter", "dark", num="CHAPTER 4", title="THE GETAWAY")
sc("Over four hundred", "count", "px:night_3", v=420000, logo="ethereum", plate=WHITE, kicker="STILL WITH THE ATTACKER", fmt=lambda v: f"{v:,.0f}+ ETH", col=INK)
sc("and all eighteen", "count", "px:coins_0", v=18270, logo="bitcoin", plate=WHITE, kicker="+ ALL OF THE BITCOIN", fmt=lambda v: f"{v:,.0f} BTC", col=INK)
sc("About two point", "bars", "dark", items=[("FROZEN", 2.7e9, ICE), ("CAN’T BE FROZEN", 2.4e9, RED)], labels=["~$2.7B", "~$2.4B"], foot="TRM Labs estimates, Oct 30, 2026")
sc("On Saturday, the", "title", "px:night_0", kicker="SATURDAY, OCT 31", lines=["THE FBI", ("NAMES THE CULPRIT", GOLD)], size=130)
sc("TraderTraitor, a", "group", "red")
sc("The same group", "timeline", "px:chess_3", pts=[("FEB 2025", "Bybit: $1.5B"), ("OCT 2026", "Binance: $6.3B")], hl=1)
sc("In the days", "photo", "pxb:alarm_1", lines=["MARKETS", ("SHAKEN", RED)], size=170)
sc("Bitcoin fell below", "price", "px:coins_1")
sc("When Binance reopened", "title", "green", logo="binance", plate=WHITE, lines=["WITHDRAWALS", ("REOPEN", GOLD)], size=150)
sc("customers pulled out", "count", "px:cash_1", v=3.64e9, logo="binance", plate=WHITE, kicker="NET OUTFLOWS · DAY ONE", fmt=lambda v: f"-${v/1e9:.1f}B", col=RED)
sc("Binance says it", "title", "px:vault_1", kicker="BINANCE’S PROMISE", lines=["WE’LL COVER", ("EVERY LOSS", GOLD)], size=140)
sc("from its emergency", "title", "px:vault_2", lines=["SAFU EMERGENCY FUND", ("+ COMPANY MONEY", GOLD)], size=110)
sc("Back in twenty", "chapter", "gold", num="THE LESSON", title="2019 → 2026")
sc("hackers stole forty", "count", "px:coins_0", v=40e6, logo="binance", plate=WHITE, kicker="2019 HACK", label="7,000 bitcoin, worth ~$40M at the time", col=GOLD)
sc("Now, six point", "versus", "px:vault_1")
sc("And this time,", "broll", "dark", clip="vault", dim=0.45, lines=["OPENED WITH", ("ITS OWN SIGNATURE", GOLD)])
sc("Fifty permission slips.", "title", "px:signature_3", lines=[("50", GOLD), "PERMISSION SLIPS"], size=150)
sc("Twenty minutes.", "title", "px:clock_3", lines=[("20", RED), "MINUTES"], size=170)
sc("Six point three billion dollars.", "count", "px:vault_1", v=6.3e9, kicker="GONE", col=INK)

