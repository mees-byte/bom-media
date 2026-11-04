#!/usr/bin/env python3
"""Download a free Pixabay stock VIDEO clip as b-roll (no credits, no attribution needed).
Needs env PIXABAY_KEY (never commit the key: this repo is public).
Usage: VIDEO_DIR=work python3 pipeline/pixabay.py "<search terms>" <name> [min_seconds]
 -> work/broll/<name>.mp4 (1920x1080, 30 fps, no audio, max 8 s) + a line in work/broll/credits.txt
Rules: mood/b-roll only (servers, code, vaults, city, charts-free abstract). Skip clips with identifiable people
(tags filtered below, and LOOK at a frame with Read before using it). Never use a clip as fake 'evidence'."""
import json, os, subprocess, sys, urllib.parse
def curl(u, out=None):  # curl, not urllib: urllib gets 403 through the proxy
    r = subprocess.run(["curl", "-sSfL", "-A", "bom-media-pipeline/1.0"] + (["-o", out] if out else []) + [u], capture_output=True, check=True)
    return r.stdout
KEY = os.environ.get("PIXABAY_KEY") or sys.exit("PIXABAY_KEY not set")
ROOT = os.path.abspath(os.environ.get("VIDEO_DIR", ".")); OUT = os.path.join(ROOT, "broll"); os.makedirs(OUT, exist_ok=True)
q, name = sys.argv[1], sys.argv[2]; mins = float(sys.argv[3]) if len(sys.argv) > 3 else 5
BAD = {"man", "woman", "person", "people", "face", "girl", "boy", "businessman", "portrait", "child", "crowd", "hacker", "anonymous"}
url = "https://pixabay.com/api/videos/?" + urllib.parse.urlencode({"key": KEY, "q": q, "safesearch": "true", "per_page": 30, "order": "popular"})
hits = json.loads(curl(url))["hits"]
def ok(h):
    tags = {t.strip() for t in h["tags"].lower().split(",")}
    words = {w for t in tags for w in t.split()}
    v = h["videos"]["large"] if h["videos"]["large"]["width"] >= 1920 else h["videos"]["medium"]
    return h["duration"] >= mins and v["width"] >= 1280 and not (words & BAD) and "ai generated" not in tags
cand = [h for h in hits if ok(h)]
if not cand: sys.exit(f"no usable clip for '{q}' ({len(hits)} hits)")
h = cand[0]; v = h["videos"]["large"] if h["videos"]["large"]["width"] >= 1920 else h["videos"]["medium"]
raw = os.path.join(OUT, name + ".raw.mp4"); dst = os.path.join(OUT, name + ".mp4")
curl(v["url"], raw)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", raw, "-t", "8", "-an", "-vf",
                "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30,format=yuv420p",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", dst], check=True)
os.remove(raw)
with open(os.path.join(OUT, "credits.txt"), "a") as f: f.write(f"{name}: Pixabay video {h['id']} by {h['user']} — {h['pageURL']}\n")
print(dst, h["id"], h["duration"], "s |", h["tags"])
