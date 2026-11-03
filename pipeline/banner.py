import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
src, logo_src, out = sys.argv[1], sys.argv[2], sys.argv[3]
W, H = 2560, 1440
FD = "/usr/share/fonts/opentype/inter/InterDisplay-"
bg = Image.open(src).convert("RGB")
s = max(W / bg.width, H / bg.height)
bg = bg.resize((int(bg.width * s) + 1, int(bg.height * s) + 1), Image.LANCZOS)
bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width - W) // 2 + W, (bg.height - H) // 2 + H))
# darken central safe band (1546x423 centered) for legibility
band = Image.new("L", (W, H), 0); bd = ImageDraw.Draw(band)
bd.rectangle([0, H / 2 - 260, W, H / 2 + 260], fill=170)
band = band.filter(ImageFilter.GaussianBlur(90))
bg = Image.composite(Image.new("RGB", (W, H), (6, 8, 16)), bg, band)
d = ImageDraw.Draw(bg)
cx, cy = W / 2, H / 2
logo = Image.open(logo_src).convert("RGBA").resize((240, 240), Image.LANCZOS)
m = Image.new("L", (240, 240), 0); ImageDraw.Draw(m).ellipse([0, 0, 239, 239], fill=255)
title = ImageFont.truetype(FD + "Black.otf", 84)
sub = ImageFont.truetype(FD + "Bold.otf", 40)
tw = title.getlength("BILLION DOLLAR MISTAKES")
total = 240 + 44 + tw
x0 = cx - total / 2
bg.paste(logo, (int(x0), int(cy - 120)), m)
tx = x0 + 284
d.text((tx, cy - 40), "BILLION DOLLAR MISTAKES", font=title, fill=(255, 255, 255), anchor="lm")
d.text((tx + 4, cy + 50), "The stories behind money, power and panic", font=sub, fill=(255, 200, 40), anchor="lm")
d.text((tx + 4, cy + 104), "NEW VIDEOS  MON · WED · FRI", font=ImageFont.truetype(FD + "SemiBold.otf", 34), fill=(200, 205, 220), anchor="lm")
bg.save(out, quality=92)
print("safe area check: content width", total, "<= 1546:", total <= 1546)
