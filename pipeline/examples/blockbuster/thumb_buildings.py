import os, sys
os.chdir("/root/bdm"); sys.path.insert(0, "/root/bdm")
sys.argv = ["render.py"]
import render as R
from PIL import Image, ImageDraw, ImageFilter

W, H = 1920, 1080
img = R.BGS["dark"].crop((100, 60, 100 + W, 60 + H)).convert("RGBA")

def glow(cx, cy, r, col, a=90):
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col + (a,))
    img.alpha_composite(g.filter(ImageFilter.GaussianBlur(r // 2)))

GROUND = 1000
glow(520, 640, 460, (229, 9, 20), 150)      # Netflix: bright red glow
glow(1240, 820, 330, (22, 64, 190), 55)     # Blockbuster: weak, fading glow

# ---- Netflix HQ: tall, lit tower (winner)
lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
x0, x1, top = 290, 750, 360
ld.rectangle([x0 + 18, top + 18, x1 + 18, GROUND], fill=(0, 0, 0, 120))
ld.rectangle([x0, top, x1, GROUND], fill=(40, 12, 18, 255))
ld.rectangle([x0, top, x0 + 22, GROUND], fill=(229, 9, 20, 255))
ld.rectangle([x1 - 22, top, x1, GROUND], fill=(229, 9, 20, 255))
for r in range(11):
    for c in range(6):
        wx = x0 + 50 + c * 70; wy = top + 160 + r * 42
        lit = (r * 7 + c * 3) % 6 != 0
        ld.rectangle([wx, wy, wx + 46, wy + 25], fill=(255, 225, 215, 245) if lit else (90, 30, 40, 255))
ld.rectangle([x0 - 20, GROUND - 80, x1 + 20, GROUND], fill=(25, 8, 12, 255))
ld.rectangle([(x0 + x1) / 2 - 60, GROUND - 80, (x0 + x1) / 2 + 60, GROUND], fill=(255, 210, 200, 230))
img.alpha_composite(lay)

# ---- Blockbuster store: low, dark, closed (loser) — kept left of the bottom-right duration badge
lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
bx0, bx1, btop = 950, 1480, 640
ld.rectangle([bx0 + 18, btop + 18, bx1 + 18, GROUND], fill=(0, 0, 0, 120))
ld.rectangle([bx0, btop, bx1, GROUND], fill=(16, 42, 120, 255))
ld.polygon([(bx0 - 35, btop), (bx1 + 35, btop), (bx1 + 10, btop - 60), (bx0 - 10, btop - 60)], fill=(190, 150, 30, 255))
for c in range(3):
    wx = bx0 + 45 + c * 165
    if c == 1: continue
    ld.rectangle([wx, btop + 175, wx + 120, btop + 300], fill=(40, 50, 80, 255))           # dark, empty windows
    ld.line([(wx + 15, btop + 185), (wx + 70, btop + 250), (wx + 55, btop + 295)], fill=(150, 160, 190, 255), width=4)  # crack
dx = (bx0 + bx1) / 2
ld.rectangle([dx - 60, btop + 200, dx + 60, GROUND], fill=(8, 10, 18, 255))
img.alpha_composite(lay)
# CLOSED sign on the door
sign = Image.new("RGBA", (300, 110), (0, 0, 0, 0)); sd = ImageDraw.Draw(sign)
sd.rounded_rectangle([0, 0, 299, 109], 14, fill=(229, 9, 20, 255), outline=(255, 255, 255, 255), width=6)
sd.text((150, 56), "CLOSED", font=R.F(66), fill=(255, 255, 255), anchor="mm")
sign = sign.rotate(-8, expand=True, resample=Image.BICUBIC)
img.alpha_composite(sign, (int(dx - sign.width / 2), btop + 205))

d = ImageDraw.Draw(img)
d.rectangle([0, GROUND, W, H], fill=(6, 8, 16))
d.line([(0, GROUND), (W, GROUND)], fill=(60, 70, 100), width=4)

# ---- real logos on white plates
R.logo(img, "netflix", (x0 + x1) / 2, top + 80, 330, 5, plate=(250, 250, 252))
R.logo(img, "blockbuster", dx, btop + 70, 230, 5, plate=(235, 235, 240), maxh=100)

# ---- headline: $50,000,000 in WHITE + gold question mark
d = ImageDraw.Draw(img)
num, q = "$50,000,000", "?"
size = R.fit(num + q, 250, W - 160)
f = R.F(size)
wn, wq = f.getlength(num), f.getlength(q)
x = (W - wn - wq) / 2; y = 205
for dxs, col in ((10, (0, 0, 0)),):
    d.text((x + dxs, y + 10), num, font=f, fill=col, anchor="lm", stroke_width=22, stroke_fill=(0, 0, 0))
    d.text((x + wn + dxs, y + 10), q, font=f, fill=col, anchor="lm", stroke_width=22, stroke_fill=(0, 0, 0))
d.text((x, y), num, font=f, fill=(255, 255, 255), anchor="lm", stroke_width=16, stroke_fill=(0, 0, 0))
d.text((x + wn, y), q, font=f, fill=R.GOLD, anchor="lm", stroke_width=16, stroke_fill=(0, 0, 0))

full = img.convert("RGB")
full.save("/root/bdm/out/THUMBNAIL_v3.png")
full.resize((1280, 720), Image.LANCZOS).save("/root/bdm/out/THUMBNAIL_v3.jpg", quality=92)
print("ok")
