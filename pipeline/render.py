#!/usr/bin/env python3
"""Billion Dollar Mistakes — scene renderer (PIL -> ffmpeg per scene)."""
import json, math, os, random, re, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1920, 1080, 30
PIPE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.environ.get("VIDEO_DIR", "."))   # per-video work dir: words.json, scenes.py, voice.mp3
OUT = os.path.join(ROOT, "scenes"); os.makedirs(OUT, exist_ok=True)
FD = "/usr/share/fonts/opentype/inter/"
_fc = {}
def F(size, w="Black"):
    k = (size, w)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(FD + f"InterDisplay-{w}.otf", size)
    return _fc[k]

# palette
BG = (10, 13, 24); INK = (240, 242, 248); MUT = (140, 148, 170)
GOLD = (255, 200, 40); RED = (229, 9, 20); BLUE = (22, 64, 190); GREEN = (40, 200, 120)
YEL = (255, 214, 0)

WORDS = [w for w in json.load(open(os.path.join(ROOT, "words.json")))["words"] if w.get("type", "word") == "word"]
AUDIO_END = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",os.path.join(ROOT,"voice.mp3")],capture_output=True,text=True).stdout.strip() or WORDS[-1]["end"])
def norm(s): return re.sub(r"[^a-z0-9$-]", "", s.lower())
_cursor = [0]
def at(phrase):
    """start time of first occurrence of phrase after the cursor"""
    toks = [norm(t) for t in phrase.split()]
    for i in range(_cursor[0], len(WORDS) - len(toks) + 1):
        if all(norm(WORDS[i + j]["text"]) == toks[j] for j in range(len(toks))):
            _cursor[0] = i + 1
            return max(0.0, WORDS[i]["start"] - 0.12)
    raise SystemExit(f"phrase not found: {phrase}")

# ---------- easing / helpers ----------
def clamp(x, a=0, b=1): return max(a, min(b, x))
def ease(x): x = clamp(x); return 1 - (1 - x) ** 3
def back(x):
    x = clamp(x); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2
def mix(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def make_bg(c1, c2, seed):
    rnd = random.Random(seed)
    g = Image.new("RGB", (W + 200, H + 120))
    d = ImageDraw.Draw(g)
    for y in range(g.height):
        d.line([(0, y), (g.width, y)], fill=mix(c1, c2, y / g.height))
    # soft glow blobs
    glow = Image.new("RGB", g.size, (0, 0, 0)); gd = ImageDraw.Draw(glow)
    for _ in range(3):
        x, y, r = rnd.randint(0, g.width), rnd.randint(0, g.height), rnd.randint(300, 600)
        gd.ellipse([x - r, y - r, x + r, y + r], fill=mix(c2, (255, 255, 255), 0.08))
    glow = glow.filter(ImageFilter.GaussianBlur(160))
    g = Image.blend(g, Image.composite(glow, g, Image.new("L", g.size, 90)), 1)
    # grid lines (finance look)
    d = ImageDraw.Draw(g)
    for x in range(0, g.width, 120):
        d.line([(x, 0), (x, g.height)], fill=mix(c2, (255, 255, 255), 0.04))
    for y in range(0, g.height, 120):
        d.line([(0, y), (g.width, y)], fill=mix(c2, (255, 255, 255), 0.04))
    # vignette
    v = Image.new("L", g.size, 0); vd = ImageDraw.Draw(v)
    vd.ellipse([-300, -300, g.width + 300, g.height + 300], fill=255)
    v = v.filter(ImageFilter.GaussianBlur(220))
    return Image.composite(g, Image.new("RGB", g.size, (0, 0, 0)), v)

BGS = {
    "dark": make_bg((8, 10, 20), (18, 24, 44), 1),
    "blue": make_bg((6, 18, 60), (16, 52, 150), 2),
    "red": make_bg((40, 4, 8), (120, 10, 18), 3),
    "gold": make_bg((40, 28, 4), (110, 80, 10), 4),
    "green": make_bg((4, 30, 20), (10, 80, 50), 5),
}
def bg(name, t):
    b = BGS[name]
    ox = int(100 + 60 * math.sin(t * 0.25)); oy = int(60 + 30 * math.cos(t * 0.2))
    return b.crop((ox, oy, ox + W, oy + H)).copy()

def text(d, xy, s, size, fill=INK, w="Black", anchor="mm", stroke=0, sfill=(0, 0, 0)):
    d.text(xy, s, font=F(size, w), fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=sfill)

def fit(s, size, maxw, w="Black"):
    while size > 20 and F(size, w).getlength(s) > maxw: size -= 4
    return size

def pop_text(img, xy, s, size, t, delay=0, fill=INK, w="Black", stroke=0):
    """text that scales in with overshoot"""
    p = back((t - delay) / 0.35)
    if p <= 0: return
    size2 = max(8, int(size * (0.6 + 0.4 * p)))
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    ld.text(xy, s, font=F(size2, w), fill=fill + (int(255 * clamp(p * 1.4)),), anchor="mm",
            stroke_width=stroke, stroke_fill=(0, 0, 0, int(255 * clamp(p))))
    img.alpha_composite(lay)

def slide_text(img, xy, s, size, t, delay=0, fill=INK, w="Black", dx=0, dy=40, anchor="mm"):
    p = ease((t - delay) / 0.4)
    if p <= 0: return
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    x, y = xy
    ld.text((x + dx * (1 - p), y + dy * (1 - p)), s, font=F(size, w), fill=fill + (int(255 * p),), anchor=anchor)
    img.alpha_composite(lay)

def rrect(d, box, r, fill, outline=None, width=0):
    d.rounded_rectangle(box, r, fill=fill, outline=outline, width=width)

def card(img, cx, cy, w, h, t, delay, color, title, sub=None):
    p = back((t - delay) / 0.4)
    if p <= 0: return
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    s = 0.7 + 0.3 * p; ww, hh = w * s, h * s; a = int(255 * clamp(p * 1.3))
    d.rounded_rectangle([cx - ww / 2 + 10, cy - hh / 2 + 16, cx + ww / 2 + 10, cy + hh / 2 + 16], 28, fill=(0, 0, 0, int(a * .45)))
    d.rounded_rectangle([cx - ww / 2, cy - hh / 2, cx + ww / 2, cy + hh / 2], 28, fill=color + (a,))
    ts = fit(title, int(70 * s), ww - 110)
    d.text((cx, cy - (18 if sub else 0) * s), title, font=F(ts), fill=(255, 255, 255, a), anchor="mm")
    if sub:
        d.text((cx, cy + 48 * s), sub, font=F(int(30 * s), "SemiBold"), fill=(255, 255, 255, int(a * .8)), anchor="mm")
    img.alpha_composite(lay)

def money(v):
    if v >= 1e9: return f"${v/1e9:,.1f}B".replace(".0B", "B")
    if v >= 1e6: return f"${v/1e6:,.0f}M"
    return f"${v:,.0f}"

def store_icon(d, cx, cy, s, col, a=255, closed=False):
    # simple storefront
    d.rectangle([cx - 90 * s, cy - 40 * s, cx + 90 * s, cy + 80 * s], fill=col + (a,))
    d.polygon([(cx - 110 * s, cy - 40 * s), (cx + 110 * s, cy - 40 * s), (cx + 90 * s, cy - 80 * s), (cx - 90 * s, cy - 80 * s)], fill=(255, 200, 40, a))
    d.rectangle([cx - 25 * s, cy + 10 * s, cx + 25 * s, cy + 80 * s], fill=(10, 13, 24, a))
    d.rectangle([cx - 75 * s, cy - 20 * s, cx - 40 * s, cy + 20 * s], fill=(200, 220, 255, int(a * .6)))
    d.rectangle([cx + 40 * s, cy - 20 * s, cx + 75 * s, cy + 20 * s], fill=(200, 220, 255, int(a * .6)))

_lc = {}
def logo_img(name, width):
    k = (name, width)
    if k not in _lc:
        lp = os.path.join(ROOT, "logos", name + ".png")
        if not os.path.exists(lp): lp = os.path.join(PIPE, "logos", name + ".png")
        im = Image.open(lp).convert("RGBA")
        bb = im.getbbox(); im = im.crop(bb) if bb else im
        h = int(im.height * width / im.width)
        _lc[k] = im.resize((width, h), Image.LANCZOS)
    return _lc[k]

def logo(img, name, cx, cy, width, t, delay=0, plate=None, maxh=None):
    p = back((t - delay) / 0.4)
    if p <= 0: return
    w = int(width * (0.7 + 0.3 * clamp(p)))
    li = logo_img(name, max(10, w))
    if maxh and li.height > maxh * (0.7 + 0.3 * clamp(p)):
        w = int(w * maxh * (0.7 + 0.3 * clamp(p)) / li.height); li = logo_img(name, max(10, w))
    a = clamp(p * 1.4)
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    if plate:
        d = ImageDraw.Draw(lay); pw, ph = li.width + 120, li.height + 90
        d.rounded_rectangle([cx - pw / 2 + 10, cy - ph / 2 + 16, cx + pw / 2 + 10, cy + ph / 2 + 16], 28, fill=(0, 0, 0, int(110 * a)))
        d.rounded_rectangle([cx - pw / 2, cy - ph / 2, cx + pw / 2, cy + ph / 2], 28, fill=plate + (int(255 * a),))
    if a < 1:
        al = li.getchannel("A").point(lambda v: int(v * a)); li = li.copy(); li.putalpha(al)
    lay.alpha_composite(li, (int(cx - li.width / 2), int(cy - li.height / 2)))
    img.alpha_composite(lay)

# ---------- captions ----------
def caption_chunks():
    chunks, cur = [], []
    for w in WORDS:
        cur.append(w)
        if len(cur) >= 5 or re.search(r"[.?!,:]$", w["text"]):
            chunks.append(cur); cur = []
    if cur: chunks.append(cur)
    return chunks
CHUNKS = caption_chunks()
def draw_caption(img, T):
    ch = None
    for c in CHUNKS:
        if c[0]["start"] - 0.05 <= T <= c[-1]["end"] + 0.25: ch = c
    if not ch: return
    d = ImageDraw.Draw(img)
    f = F(56); sp = f.getlength(" ")
    widths = [f.getlength(w["text"].upper()) for w in ch]
    tot = sum(widths) + sp * (len(ch) - 1)
    x = (W - tot) / 2; y = 975
    for w, ww in zip(ch, widths):
        active = w["start"] - 0.03 <= T <= w["end"] + 0.05
        col = YEL if active else (255, 255, 255)
        d.text((x, y), w["text"].upper(), font=f, fill=col, anchor="lm", stroke_width=7, stroke_fill=(0, 0, 0))
        x += ww + sp

# ---------- scene kinds ----------
def k_title(img, t, dur, a):
    d = ImageDraw.Draw(img)
    lines = a["lines"]; n = len(lines)
    y0 = a.get("y", 500) - (n - 1) * 70
    for i, ln in enumerate(lines):
        s, col = (ln, INK) if isinstance(ln, str) else ln
        size = fit(s, a.get("size", 120), W - 200)
        pop_text(img, (W / 2, y0 + i * 140), s, size, t, delay=i * 0.25, fill=col)
    if a.get("kicker"):
        slide_text(img, (W / 2, y0 - 130), a["kicker"], 40, t, 0, fill=GOLD, w="Bold")
    if a.get("logo"):
        logo(img, a["logo"], W / 2, y0 - 215, 330, t, 0, plate=a.get("plate"), maxh=120)

def k_count(img, t, dur, a):
    d = ImageDraw.Draw(img)
    p = ease(t / min(1.4, dur * 0.6))
    v = a["v"] * p
    s = a["fmt"](v) if "fmt" in a else money(v)
    both = a.get("logo") and a.get("kicker")   # logo + kicker: push the number down so they never overlap
    if a.get("logo"): logo(img, a["logo"], W / 2, 220 if both else 270, 380, t, 0, plate=a.get("plate"), maxh=130 if both else 150)
    elif a.get("kicker"): slide_text(img, (W / 2, 300), a["kicker"], 46, t, 0, fill=MUT, w="Bold")
    if both: slide_text(img, (W / 2, 365), a["kicker"], 40, t, 0.2, fill=MUT, w="Bold")
    size = fit(a["fmt"](a["v"]) if "fmt" in a else money(a["v"]), 210 if both else 230, W - 240)
    shake = (random.Random(int(t * 60)).randint(-8, 8) if 1.35 < t < 1.6 else 0)
    text(d, (W / 2 + shake, 560 if both else 520), s, size, fill=a.get("col", GOLD))
    if a.get("label"): slide_text(img, (W / 2, 740 if both else 700), a["label"], 54, t, 0.5, w="Bold")

def k_date(img, t, dur, a):
    d = ImageDraw.Draw(img)
    s = a["date"]; n = int(clamp(t / 0.9) * len(s))
    text(d, (W / 2, 470), s[:n] + ("|" if int(t * 3) % 2 == 0 and n < len(s) else ""), 170, fill=INK)
    slide_text(img, (W / 2, 640), a["place"], 52, t, 0.9, fill=GOLD, w="Bold")

def k_offer(img, t, dur, a):
    logo(img, "netflix", 520, 450, 380, t, 0, plate=(250, 250, 252))
    logo(img, "blockbuster", 1400, 450, 300, t, 0.25, plate=(250, 250, 252))
    slide_text(img, (520, 640), "the startup", 36, t, 0.3, fill=MUT, w="Bold")
    slide_text(img, (1400, 640), "the giant", 36, t, 0.5, fill=MUT, w="Bold")
    d = ImageDraw.Draw(img)
    p = ease((t - 0.6) / 0.6)
    if p > 0:
        x = 790 + (1130 - 790) * p
        d.line([(790, 450), (x, 450)], fill=GOLD, width=10)
        if p > 0.95: d.polygon([(1130, 425), (1170, 450), (1130, 475)], fill=GOLD)
    q = back((t - 1.3) / 0.4)
    if q > 0:
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
        sz = 0.5 + 0.5 * q
        ld.rounded_rectangle([960 - 170 * sz, 760 - 70 * sz, 960 + 170 * sz, 760 + 70 * sz], 20, fill=GOLD + (255,))
        ld.text((960, 760), "$50M", font=F(int(110 * sz)), fill=(10, 13, 24), anchor="mm")
        img.alpha_composite(lay)

def k_compare(img, t, dur, a):
    d = ImageDraw.Draw(img)
    for i, (name, val, lab, col) in enumerate(a["items"]):
        x = 560 + i * 800
        slide_text(img, (x, 260), name, 60, t, i * 0.3, fill=col)
        p = ease((t - 0.3 - i * 0.3) / 0.9)
        hmax = 480; h = max(6, hmax * val * p)
        d.rounded_rectangle([x - 130, 780 - h, x + 130, 780], 14, fill=col)
        if p > 0.2: slide_text(img, (x, 780 - h - 60), lab, 64, t, 0.5 + i * 0.3, fill=INK)

def k_store(img, t, dur, a):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    p = back(t / 0.5)
    store_icon(d, W / 2, 470, 1.6 * (0.6 + 0.4 * clamp(p)), BLUE, int(255 * clamp(p)))
    img.alpha_composite(lay)
    logo(img, "blockbuster", W / 2, 250, 230, t, 0.25, plate=(250, 250, 252))
    slide_text(img, (W / 2, 760), a.get("label", "ONE STORE LEFT"), 72, t, 0.4, fill=GOLD)
    if a.get("sub"): slide_text(img, (W / 2, 840), a["sub"], 40, t, 0.7, fill=MUT, w="Bold")

def k_stores_grid(img, t, dur, a):
    d = ImageDraw.Draw(img)
    cols, rows = 60, 22; n = cols * rows
    shown = int(n * ease(t / 2.0))
    for i in range(shown):
        cx = 300 + (i % cols) * 22; cy = 230 + (i // cols) * 22
        d.rectangle([cx, cy, cx + 14, cy + 14], fill=GOLD if i % 7 else BLUE)
    lay_count = int(9000 * ease(t / 2.0))
    text(d, (W / 2, 120), f"{lay_count:,} STORES", 90, fill=INK, stroke=6)
    if t > 1.2: slide_text(img, (W / 2, 790), "+ $5.9B YEARLY REVENUE (2004)", 54, t, 1.2, fill=GOLD)

def k_pie(img, t, dur, a):
    d = ImageDraw.Draw(img)
    cx, cy, r = 640, 520, 300
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(40, 52, 90))
    p = ease((t - 0.3) / 1.0)
    if p > 0: d.pieslice([cx - r, cy - r, cx + r, cy + r], -90, -90 + 360 * 0.16 * p, fill=GOLD)
    d.ellipse([cx - 130, cy - 130, cx + 130, cy + 130], fill=BG)
    text(d, (cx, cy), f"{int(16 * p)}%", 90, fill=GOLD)
    slide_text(img, (1300, 430), "OF ALL REVENUE", 60, t, 0.5, fill=INK)
    slide_text(img, (1300, 530), "came from late fees", 48, t, 0.8, fill=MUT, w="Bold")
    slide_text(img, (1300, 640), "(year 2000)", 36, t, 1.0, fill=MUT, w="SemiBold")

def k_envelope(img, t, dur, a):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    p = ease(t / 0.8)
    x = -400 + (W / 2 + 400) * p
    d.rounded_rectangle([x - 300, 330, x + 300, 690], 18, fill=RED + (255,))
    d.polygon([(x - 300, 330), (x, 520), (x + 300, 330)], fill=(180, 6, 14, 255))
    # disc peeking out
    q = ease((t - 0.8) / 0.6)
    dy = -170 * q
    d.ellipse([x - 120, 330 + dy - 120 + 60, x + 120, 330 + dy + 120 + 60], fill=(210, 215, 230, 255) if q > 0 else (0, 0, 0, 0))
    if q > 0: d.ellipse([x - 25, 330 + dy + 35, x + 25, 330 + dy + 85], fill=RED + (255,))
    img.alpha_composite(lay)
    slide_text(img, (W / 2, 820), a.get("label", "DVDs BY MAIL"), 64, t, 1.0, fill=INK)

def k_loss(img, t, dur, a):
    d = ImageDraw.Draw(img)
    p = ease(t / 0.9)
    pts = [(300, 300), (650, 380), (900, 340), (1200, 560), (1600, 760)]
    n = 1 + int(p * (len(pts) - 1) * 10) / 10
    seg = []
    for i in range(len(pts) - 1):
        if n > i + 1: seg.append(pts[i + 1])
        elif n > i:
            f = n - i; seg.append((pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f))
    d.line([pts[0]] + seg, fill=RED, width=14, joint="curve")
    pop_text(img, (W / 2, 210), a.get("big", "-$50M"), 160, t, 0.6, fill=RED, stroke=6)
    if a.get("label"): slide_text(img, (W / 2, 880), a["label"], 50, t, 0.9, fill=INK, w="Bold")

def k_people(img, t, dur, a):
    d = ImageDraw.Draw(img)
    names = a["names"]; n = len(names)
    for i, (nm, role, col) in enumerate(names):
        x = W / 2 + (i - (n - 1) / 2) * 560
        p = back((t - i * 0.25) / 0.4)
        if p <= 0: continue
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
        a_ = int(255 * clamp(p))
        ld.ellipse([x - 110, 260, x + 110, 480], fill=col + (a_,))
        ld.ellipse([x - 55, 300, x + 55, 410], fill=(255, 255, 255, int(a_ * .9)))
        ld.pieslice([x - 95, 400, x + 95, 560], 180, 360, fill=(255, 255, 255, int(a_ * .9)))
        ld.text((x, 560), nm, font=F(fit(nm, 54, 520)), fill=(255, 255, 255, a_), anchor="mm")
        ld.text((x, 625), role, font=F(34, "SemiBold"), fill=MUT + (a_,), anchor="mm")
        img.alpha_composite(lay)
    if a.get("logo"): logo(img, a["logo"], W / 2, 735, 150, t, 0.4, plate=(250, 250, 252), maxh=90)
    if a.get("caption"): slide_text(img, (W / 2, 870 if a.get("logo") else 790), a["caption"], 58 if not a.get("logo") else 46, t, 0.6, fill=GOLD)

def k_quote(img, t, dur, a):
    d = ImageDraw.Draw(img)
    p = ease(t / 0.4)
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    ld.rounded_rectangle([260, 260, 1660, 760], 30, fill=(255, 255, 255, int(235 * p)))
    ld.text((330, 330), "“", font=F(220), fill=GOLD + (int(255 * p),), anchor="lt")
    img.alpha_composite(lay)
    lines = a["lines"]
    for i, ln in enumerate(lines):
        slide_text(img, (W / 2, 470 + i * 90), ln, 64, t, 0.3 + i * 0.25, fill=(15, 18, 30))
    slide_text(img, (W / 2, 700), a["who"], 34, t, 0.8, fill=(90, 96, 120), w="Bold")

def k_chapter(img, t, dur, a):
    d = ImageDraw.Draw(img)
    slide_text(img, (W / 2, 420), a["num"], 44, t, 0, fill=(255, 255, 255), w="Bold")
    p = ease((t - 0.15) / 0.5)
    d.rectangle([W / 2 - 300 * p, 470, W / 2 + 300 * p, 478], fill=(255, 255, 255))
    pop_text(img, (W / 2, 580), a["title"], 150, t, 0.2, fill=(255, 255, 255))

def k_timeline(img, t, dur, a):
    d = ImageDraw.Draw(img)
    pts = a["pts"]; n = len(pts); x0, x1 = 240, 1680
    p = ease(t / 1.0)
    d.line([(x0, 540), (x0 + (x1 - x0) * p, 540)], fill=MUT, width=6)
    for i, (yr, lab) in enumerate(pts):
        x = x0 + (x1 - x0) * i / (n - 1)
        if p * (n - 1) + 0.01 >= i:
            hl = (i == a.get("hl", -1))
            col = GOLD if hl else INK
            d.ellipse([x - 18, 522, x + 18, 558], fill=col)
            slide_text(img, (x, 470), yr, 52, t, i * 0.15, fill=col)
            slide_text(img, (x, 615), lab, 30, t, i * 0.15 + 0.1, fill=col if hl else MUT, w="Bold")

def k_access(img, t, dur, a):
    steps = [("RENT ONLINE", BLUE), ("RETURN IN STORE", (40, 90, 220)), ("SWAP ON THE SPOT", GOLD)]
    d = ImageDraw.Draw(img)
    for i, (s, col) in enumerate(steps):
        card(img, 380 + i * 580, 500, 480, 220, t, i * 0.5, col if col != GOLD else (200, 150, 10), s)
        if i < 2 and t > i * 0.5 + 0.35:
            x = 380 + i * 580 + 250; d.polygon([(x, 470), (x + 50, 500), (x, 530)], fill=INK)
    logo(img, "blockbuster", W / 2 - 230, 230, 200, t, 0, plate=(250, 250, 252))
    slide_text(img, (W / 2 + 120, 230), "TOTAL ACCESS", 64, t, 0.1, fill=GOLD, anchor="lm")

def k_checkmate(img, t, dur, a):
    d = ImageDraw.Draw(img)
    s = 66; x0, y0 = W / 2 - 4 * s, 150
    for r in range(8):
        for c in range(8):
            d.rectangle([x0 + c * s, y0 + r * s, x0 + (c + 1) * s, y0 + (r + 1) * s], fill=(220, 210, 190) if (r + c) % 2 == 0 else (90, 70, 50))
    # kings as discs with letters
    p = ease((t - 0.6) / 0.6)
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    bx, by = x0 + 2.5 * s, y0 + 5.5 * s
    ld.ellipse([bx - 50, by - 50, bx + 50, by + 50], fill=BLUE + (255,)); ld.text((bx, by), "B", font=F(56), fill=(255, 255, 255), anchor="mm")
    rx, ry = x0 + 5.5 * s + 30 * p, y0 + 2.5 * s + 20 * p
    rk = Image.new("RGBA", (120, 120), (0, 0, 0, 0)); rd = ImageDraw.Draw(rk)
    rd.ellipse([10, 10, 110, 110], fill=RED + (255,)); rd.text((60, 60), "N", font=F(56), fill=(255, 255, 255), anchor="mm")
    rk = rk.rotate(-80 * p, resample=Image.BICUBIC)
    lay.alpha_composite(rk, (int(rx - 60), int(ry - 60)))
    img.alpha_composite(lay)
    pop_text(img, (W / 2, 800), "CHECKMATE", 110, t, 0.9, fill=GOLD, stroke=6)

def k_subs(img, t, dur, a):
    d = ImageDraw.Draw(img)
    slide_text(img, (W / 2, 260), "2007", 60, t, 0, fill=GOLD)
    logo(img, "netflix", W / 2, 470, 520, t, 0.15)
    pop_text(img, (W / 2, 640), "LOST SUBSCRIBERS", 110, t, 0.45, fill=INK)
    p = ease((t - 0.9) / 0.6)
    if p > 0:
        d.line([(1560, 300), (1560, 300 + 260 * p)], fill=RED, width=26)
        if p > 0.9: d.polygon([(1510, 560), (1610, 560), (1560, 640)], fill=RED)
    slide_text(img, (W / 2, 790), "one of the only times in its history", 40, t, 1.0, fill=MUT, w="Bold")

def k_question(img, t, dur, a):
    d = ImageDraw.Draw(img)
    pop_text(img, (W / 2, 330), "?", 300, t, 0, fill=GOLD)
    for i, ln in enumerate(a["lines"]):
        slide_text(img, (W / 2, 620 + i * 100), ln, fit(ln, 76, W - 240), t, 0.3 + i * 0.25, fill=INK)

def k_bonus(img, t, dur, a):
    d = ImageDraw.Draw(img)
    p = back(t / 0.5)
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    sz = 0.6 + 0.4 * clamp(p)
    ld.rounded_rectangle([W / 2 - 520 * sz, 300 - 0, W / 2 + 520 * sz, 300 + 330 * sz], 24, fill=(235, 240, 225, int(255 * clamp(p))))
    ld.text((W / 2 - 470 * sz, 340), "PAY TO: CEO", font=F(int(36 * sz), "Bold"), fill=(60, 70, 60), anchor="lt")
    ld.text((W / 2, 300 + 180 * sz), "> $7,600,000", font=F(int(130 * sz)), fill=(20, 90, 50), anchor="mm")
    ld.text((W / 2 + 470 * sz, 300 + 300 * sz), "ANNUAL BONUS", font=F(int(30 * sz), "Bold"), fill=(60, 70, 60), anchor="rm")
    img.alpha_composite(lay)
    q = ease((t - 1.0) / 0.3)
    if q > 0:
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
        ld.text((W / 2 + 330, 640), "DISPUTED", font=F(int(90 * (2 - q))), fill=RED + (int(230 * q),), anchor="mm", stroke_width=6, stroke_fill=(255, 255, 255, int(200 * q)))
        lay = lay.rotate(-10, center=(W / 2 + 330, 640))
        img.alpha_composite(lay)
    slide_text(img, (W / 2, 820), a.get("label", "ICAHN WENT TO WAR"), 66, t, 0.6, fill=GOLD)

def k_comment(img, t, dur, a):
    d = ImageDraw.Draw(img)
    p = back(t / 0.45)
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    al = int(255 * clamp(p))
    ld.rounded_rectangle([360, 260, 1560, 720], 34, fill=(255, 255, 255, al))
    ld.ellipse([420, 320, 520, 420], fill=GOLD + (al,))
    ld.text((470, 370), "?", font=F(60), fill=(15, 18, 30, al), anchor="mm")
    ld.text((560, 340), "YOU’RE ON THE BOARD.", font=F(48), fill=(15, 18, 30, al), anchor="lt")
    ld.rounded_rectangle([440, 470, 940, 640], 24, fill=BLUE + (al,))
    ld.text((690, 555), "PROTECT PROFITS", font=F(40), fill=(255, 255, 255, al), anchor="mm")
    ld.rounded_rectangle([980, 470, 1480, 640], 24, fill=RED + (al,))
    ld.text((1230, 555), "FUND THE FUTURE", font=F(40), fill=(255, 255, 255, al), anchor="mm")
    img.alpha_composite(lay)
    slide_text(img, (W / 2, 820), "TELL ME IN THE COMMENTS ↓", 56, t, 0.6, fill=GOLD)

def k_subscribe(img, t, dur, a):
    d = ImageDraw.Draw(img)
    slide_text(img, (W / 2, 330), "BILLION DOLLAR MISTAKES", 80, t, 0, fill=INK)
    p = back((t - 0.4) / 0.4)
    clicked = t > 1.6
    if p > 0:
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
        sz = 0.6 + 0.4 * clamp(p)
        col = (60, 66, 84) if clicked else RED
        ld.rounded_rectangle([W / 2 - 280 * sz, 520 - 80 * sz, W / 2 + 280 * sz, 520 + 80 * sz], 80, fill=col + (255,))
        ld.text((W / 2, 520), "SUBSCRIBED ✓" if clicked else "SUBSCRIBE", font=F(int(64 * sz)), fill=(255, 255, 255), anchor="mm")
        img.alpha_composite(lay)
    # cursor
    c = ease((t - 0.8) / 0.7)
    if c > 0:
        cx, cy = 1500 - (1500 - 1000) * c, 900 - (900 - 545) * c
        d.polygon([(cx, cy), (cx, cy + 60), (cx + 16, cy + 46), (cx + 28, cy + 72), (cx + 38, cy + 66), (cx + 26, cy + 42), (cx + 46, cy + 42)], fill=(255, 255, 255), outline=(0, 0, 0))
    
def k_debt(img, t, dur, a):
    k_count(img, t, dur, a)

_broll = {}
def k_broll(img, t, dur, a):
    """Pixabay stock clip as full-screen background (pipeline/pixabay.py). args: clip=<name>, ss=start sec,
    optional kicker / lines (bottom-left, stays above the captions), dim=0..1 darkening (default .35)."""
    name = a["clip"]
    if name not in _broll:
        fdir = os.path.join(ROOT, "broll", "frames", name); os.makedirs(fdir, exist_ok=True)
        if not os.listdir(fdir):
            subprocess.run(["ffmpeg", "-v", "error", "-ss", str(a.get("ss", 0)), "-i", os.path.join(ROOT, "broll", name + ".mp4"),
                            "-vf", "fps=30", "-q:v", "3", os.path.join(fdir, "%04d.jpg")], check=True)
        _broll[name] = sorted(os.listdir(fdir))
    fr = _broll[name]; fdir = os.path.join(ROOT, "broll", "frames", name)
    i = min(len(fr) - 1, int(t * FPS)) if a.get("hold", True) else int(t * FPS) % len(fr)
    im = Image.open(os.path.join(fdir, fr[i])).convert("RGBA").resize((W, H))
    img.paste(im, (0, 0))
    img.alpha_composite(Image.new("RGBA", img.size, (0, 0, 0, int(255 * a.get("dim", 0.35)))))
    y = 820 - 110 * (len(a.get("lines", [])) - 1)
    if a.get("kicker"): slide_text(img, (110, y - 95), a["kicker"], 40, t, 0.1, fill=GOLD, w="Bold", anchor="lm")
    for j, ln in enumerate(a.get("lines", [])):
        s_, col = (ln, INK) if isinstance(ln, str) else ln
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
        p = ease((t - 0.2 - j * 0.2) / 0.4)
        if p > 0:
            ld.text((110 + 40 * (1 - p), y + j * 110), s_, font=F(fit(s_, 96, W - 300)), fill=col + (int(255 * p),), anchor="lm",
                    stroke_width=6, stroke_fill=(0, 0, 0, int(255 * p)))
            img.alpha_composite(lay)

KINDS = {k[2:]: v for k, v in globals().items() if k.startswith("k_")}

# ---------- scene list (per video: VIDEO_DIR/scenes.py, uses sc(phrase, kind, bg, **args)) ----------
S = []
def sc(phrase, kind, bgname="dark", **a):
    S.append(dict(t0=at(phrase) if phrase else 0.0, kind=kind, bg=bgname, a=a))
exec(open(os.path.join(ROOT, "scenes.py")).read())
KINDS.update({k[2:]: v for k, v in list(globals().items()) if k.startswith("k_")})

for i, s in enumerate(S):
    s["t1"] = S[i + 1]["t0"] if i + 1 < len(S) else AUDIO_END + 1.2

# snap scene boundaries to frame grid so total length is exact
for s in S:
    s["f0"] = round(s["t0"] * FPS); s["f1"] = round(s["t1"] * FPS)

def render_frame(s, f):
    T = f / FPS; t = T - s["t0"]; dur = s["t1"] - s["t0"]
    img = bg(s["bg"], T).convert("RGBA")
    KINDS[s["kind"]](img, t, dur, s["a"])
    # flash in on chapter cards, small fade-in on others
    if s["kind"] == "chapter" and t < 0.15:
        img.alpha_composite(Image.new("RGBA", img.size, (255, 255, 255, int(255 * (1 - t / 0.15)))))
    img = img.convert("RGB")
    z = 1.0 + 0.07 * (1 - ease(t / 0.28)) + 0.025 * clamp(t / max(dur, 0.1))
    if z > 1.001:
        cw, ch = int(W / z), int(H / z)
        img = img.crop(((W - cw) // 2, (H - ch) // 2, (W - cw) // 2 + cw, (H - ch) // 2 + ch)).resize((W, H), Image.BILINEAR)
    draw_caption(img, T)
    return img

def render_scene(i):
    s = S[i]
    dst = os.path.join(OUT, f"s{i:03d}.mp4")
    if os.path.exists(dst): return dst
    tmp = os.path.join(OUT, f"s{i:03d}.tmp.mp4")
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(FPS), tmp], stdin=subprocess.PIPE)
    for f in range(s["f0"], s["f1"]):
        p.stdin.write(render_frame(s, f).tobytes())
    p.stdin.close()
    if p.wait() == 0: os.rename(tmp, dst)
    return dst

if __name__ == "__main__":
    if sys.argv[1] == "preview":
        for spec in sys.argv[2:]:
            i, tt = spec.split("@"); s = S[int(i)]
            f = int((s["t0"] + float(tt)) * FPS)
            render_frame(s, f).save(os.path.join(ROOT, f"prev_{i}_{tt}.jpg"), quality=85)
    elif sys.argv[1] == "list":
        for i, s in enumerate(S): print(i, s["kind"], round(s["t0"], 2), round(s["t1"] - s["t0"], 2))
    elif sys.argv[1] == "render":
        from multiprocessing import Pool
        with Pool(int(sys.argv[2]) if len(sys.argv) > 2 else 2) as pool:
            for r in pool.imap_unordered(render_scene, range(len(S))): print("done", os.path.basename(r), flush=True)
        with open(os.path.join(ROOT, "concat.txt"), "w") as fh:
            for i in range(len(S)): fh.write(f"file 'scenes/s{i:03d}.mp4'\n")
