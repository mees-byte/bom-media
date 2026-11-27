import sys, importlib.util
from PIL import Image, ImageDraw, ImageEnhance
spec = importlib.util.spec_from_file_location("R", "/home/claude/bom-media/pipeline/render.py")
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
W, H = 1920, 1080; GOLD = R.GOLD
im = Image.open(sys.argv[1]).convert("RGB"); var = sys.argv[2]
s = max(W / im.width, H / im.height) * 1.12; im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS).crop((40, 0, 40 + W, H))
im = ImageEnhance.Contrast(im).enhance(1.15); im = ImageEnhance.Sharpness(im).enhance(1.3); img = im.convert("RGBA")
g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
for x in range(W):
    a = int(235 * max(0, min(1, (x - 900) / 320))); gd.line([(x, 0), (x, H)], fill=(6, 12, 30, a))
img.alpha_composite(g); d = ImageDraw.Draw(img); X = 1880
def T(y, s_, size, col=(255, 255, 255), sw=16): d.text((X, y), s_, font=R.F(size), fill=col, anchor="rm", stroke_width=sw, stroke_fill=(0, 0, 0))
if var == "A":
    T(300, "+50%", 290, GOLD, 18); T(560, "DRUG PLAN", 120); T(690, "IN 2027?", 120); T(820, "AVG STAND-ALONE PLAN · IF YOU KEEP IT", 50, (225, 230, 242), 10)
else:
    T(280, "$34→$51", 210, GOLD, 18); T(500, "UNLESS YOU", 110); T(630, "SWITCH?", 110); T(770, "AVG STAND-ALONE DRUG PLAN · 2027", 50, (225, 230, 242), 8)
img.convert("RGB").save(sys.argv[3] + ".png"); img.convert("RGB").resize((1280, 720), Image.LANCZOS).save(sys.argv[3] + ".jpg", quality=92)
