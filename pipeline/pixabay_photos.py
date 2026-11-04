#!/usr/bin/env python3
"""Download candidate Pixabay PHOTOS (free, no credits) for photo backgrounds, plus a contact sheet to pick from.
Needs env PIXABAY_KEY (never commit the key: this repo is public).
Usage: VIDEO_DIR=work python3 pipeline/pixabay_photos.py '[["cash","cash money dollars"],["chess","chess king"]]'
 -> work/px_dl/<name>_<i>.jpg (4 per query) + work/px_dl/_sheet.jpg + _meta.json
Then LOOK at _sheet.jpg, copy the best ones to work/px/<name>.jpg and use them in scenes.py as background
"px:<name>" (darkened + slightly blurred, behind animations) or "pxb:<name>" (bright, with the "photo" kind as pattern break).
Rules: no identifiable people/faces, no fake logos, no glitches/watermarks, nothing pretending to be footage of the real event."""
import json, os, sys, time, urllib.parse, urllib.request
from PIL import Image, ImageDraw
KEY = os.environ.get("PIXABAY_KEY") or sys.exit("PIXABAY_KEY not set")
ROOT = os.path.abspath(os.environ.get("VIDEO_DIR", ".")); OUT = os.path.join(ROOT, "px_dl"); os.makedirs(OUT, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (bom-media pipeline)"}   # without a UA Pixabay answers 403
def get(u): return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30)
res = {}
for name, q in json.loads(sys.argv[1]):
    url = "https://pixabay.com/api/?" + urllib.parse.urlencode(dict(key=KEY, q=q, image_type="photo", orientation="horizontal",
                                                                      min_width=1920, safesearch="true", per_page=8, order="popular"))
    hits = json.load(get(url))["hits"]
    res[name] = []
    for i, h in enumerate(hits[:4]):
        fn = f"{name}_{i}.jpg"; open(os.path.join(OUT, fn), "wb").write(get(h["largeImageURL"]).read())
        res[name].append(dict(file=fn, id=h["id"], page=h["pageURL"], user=h["user"], tags=h["tags"]))
    time.sleep(0.4)
json.dump(res, open(os.path.join(OUT, "_meta.json"), "w"), indent=1)
names = list(res); g = Image.new("RGB", (1600, 225 * len(names)))
for r, n in enumerate(names):
    for c, it in enumerate(res[n]):
        im = Image.open(os.path.join(OUT, it["file"])).convert("RGB"); im = im.resize((400, int(400 * im.height / im.width))).crop((0, 0, 400, 225))
        ImageDraw.Draw(im).text((6, 6), f"{n}_{c}", fill=(255, 0, 255)); g.paste(im, (c * 400, r * 225))
g.save(os.path.join(OUT, "_sheet.jpg"), quality=75)
print({k: len(v) for k, v in res.items()}, "->", os.path.join(OUT, "_sheet.jpg"))
