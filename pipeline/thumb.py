#!/usr/bin/env python3
"""Thumbnail in the same design as the video (owner request 2026-11-04): video background,
real company logo(s) on white plates, WHITE text with black outline, gold question marks. No AI image, no credits.
Usage: VIDEO_DIR=work python3 pipeline/thumb.py work/thumb_spec.json   -> work/thumb.png + work/thumb.jpg
spec example (the 2026-11-06 Binance thumbnail):
{"bg": "dark",
 "lines": [["WHO STOLE", 150, 260], ["$6.3", 260, 450], ["BILLION?", 190, 640], ["IN 20 MINUTES", 110, 820]],
 "logos": [["binance", 1480, 400, 420]],
 "qmarks": [[1150, 250, 260, 12]]}
lines = [text, size, y] (left-aligned at x=90); logos = [name, cx, cy, width]; qmarks = [x, y, size, rotation].
Keep the bottom-right corner (x>1500, y>880) empty: YouTube puts the duration there."""
import os, sys, json, importlib.util
from PIL import Image, ImageDraw
spec = importlib.util.spec_from_file_location("R", os.path.join(os.path.dirname(os.path.abspath(__file__)), "render.py"))
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)   # needs VIDEO_DIR with words.json/voice.mp3/scenes.py
S = json.load(open(sys.argv[1]))
img = R.bg(S.get("bg", "dark"), 0).convert("RGBA")
for name, cx, cy, width in S.get("logos", []):
    li = R.logo_img(name, width)
    if li.height > width: li = R.logo_img(name, int(width * width / li.height))
    d = ImageDraw.Draw(img); pw, ph = li.width + 110, li.height + 90
    d.rounded_rectangle([cx-pw/2+14, cy-ph/2+20, cx+pw/2+14, cy+ph/2+20], 36, fill=(0, 0, 0, 120))
    d.rounded_rectangle([cx-pw/2, cy-ph/2, cx+pw/2, cy+ph/2], 36, fill=(250, 250, 252, 255))
    img.alpha_composite(li, (int(cx-li.width/2), int(cy-li.height/2)))
for x, y, size, rot in S.get("qmarks", []):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((x, y), "?", font=R.F(size), fill=R.GOLD + (255,), anchor="mm", stroke_width=12, stroke_fill=(0, 0, 0, 255))
    img.alpha_composite(lay.rotate(rot, center=(x, y), resample=Image.BICUBIC))
d = ImageDraw.Draw(img)
for text, size, y in S["lines"]:
    d.text((90, y), text, font=R.F(size), fill=(255, 255, 255), anchor="lm", stroke_width=10, stroke_fill=(0, 0, 0))
out = img.convert("RGB")
out.save(os.path.join(R.ROOT, "thumb.png")); out.save(os.path.join(R.ROOT, "thumb.jpg"), quality=92)
print("thumb.png / thumb.jpg written")
