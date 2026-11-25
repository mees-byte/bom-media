# final thumbnail variants: photo left (zoomed), short text right. usage: VIDEO_DIR=work python3 thumb_final.py photo.png A|B out_noext
import sys, importlib.util
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
spec = importlib.util.spec_from_file_location("R", "/home/claude/bom-media/pipeline/render.py")
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
W, H = 1920, 1080; GOLD = R.GOLD
im = Image.open(sys.argv[1]).convert("RGB"); var = sys.argv[2]
z = 1.18; s = max(W / im.width, H / im.height) * z
im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
im = im.crop((60, 0, 60 + W, H))
im = ImageEnhance.Contrast(im).enhance(1.15); im = ImageEnhance.Color(im).enhance(1.08); im = ImageEnhance.Sharpness(im).enhance(1.3)
img = im.convert("RGBA")
g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
for x in range(W):
    a = int(235 * max(0, min(1, (x - 860) / 340))); gd.line([(x, 0), (x, H)], fill=(6, 12, 30, a))
img.alpha_composite(g); d = ImageDraw.Draw(img); X = 1880
def T(y, s_, size, col=(255, 255, 255), sw=16): d.text((X, y), s_, font=R.F(size), fill=col, anchor="rm", stroke_width=sw, stroke_fill=(0, 0, 0))
if var == "A":
    T(330, "−22%", 290, GOLD, 18)
    T(590, "IN 2032", 150)
    T(760, "IF CONGRESS WAITS", 64, (225, 230, 242), 10)
else:
    T(250, "$477", 280, GOLD, 18)
    T(480, "LESS A MONTH?", 104)
    T(640, "AVG CHECK · 2032 PROJECTION", 52, (225, 230, 242), 8)
img.convert("RGB").save(sys.argv[3] + ".png"); img.convert("RGB").resize((1280, 720), Image.LANCZOS).save(sys.argv[3] + ".jpg", quality=92)
