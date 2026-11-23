# thumbnail: graded AI photo of Linda (left) + overlay right. usage: VIDEO_DIR=work python3 thumb_e27.py <photo> <out_noext>
import sys, importlib.util, os
from PIL import Image, ImageDraw, ImageEnhance
spec = importlib.util.spec_from_file_location("R", "/home/claude/bom-media/pipeline/render.py")
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
W, H = 1920, 1080; GOLD = R.GOLD
im = Image.open(sys.argv[1]).convert("RGB")
s = max(W / im.width, H / im.height) * 1.05; im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
ox = int(os.environ.get("OX", "60")); im = im.crop((ox, 0, ox + W, H))
im = ImageEnhance.Contrast(im).enhance(1.12); im = ImageEnhance.Brightness(im).enhance(1.05); img = im.convert("RGBA")
g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
for x in range(W):
    a = int(225 * max(0, min(1, (x - 820) / 380))); gd.line([(x, 0), (x, H)], fill=(6, 14, 34, a))
img.alpha_composite(g); d = ImageDraw.Draw(img); X = 1870
def T(y, s_, size, col=(255, 255, 255)): d.text((X, y), s_, font=R.F(size), fill=col, anchor="rm", stroke_width=14, stroke_fill=(0, 0, 0))
T(170, "CHECKS STOPPED?", 104)
T(380, "$25,560", 230, GOLD)
pill = "EARN $1 OVER = 50¢ HELD"; f = R.F(64); pw = f.getlength(pill) + 70
d.rounded_rectangle([X - pw, 560, X, 690], 30, fill=(250, 247, 238), outline=(0, 0, 0), width=6)
d.text((X - pw / 2, 625), pill, font=f, fill=(15, 22, 45), anchor="mm")
img.convert("RGB").save(sys.argv[2] + ".png"); img.convert("RGB").resize((1280, 720), Image.LANCZOS).save(sys.argv[2] + ".jpg", quality=92)
