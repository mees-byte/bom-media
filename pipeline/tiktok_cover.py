#!/usr/bin/env python3
"""Give a TikTok its own cover (0 credits). Takes one frame of the LONG video, builds a 9:16 cover
(blurred background, the frame's graphic in the middle, big hook text on top), and prepends it for 0.5 s
so TikTok uses it as the thumbnail. Every TikTok must get a DIFFERENT frame + text (owner request 2026-11-06).
Usage: python3 tiktok_cover.py LONG.mp4 FRAME_SEC TIKTOK_IN.mp4 TIKTOK_OUT.mp4 "LINE 1|*LINE 2*|LINE 3" [x0,y0,x1,y1]
Lines split by |; a line wrapped in *stars* is gold. Optional crop box on the 1920x1080 frame (default 240,0,1680,850:
everything above the burned-in captions). Also writes TIKTOK_OUT with .jpg extension (the cover itself)."""
import subprocess, sys, tempfile, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
long_v, t, tin, tout, text = sys.argv[1], float(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5]
box = tuple(int(v) for v in sys.argv[6].split(",")) if len(sys.argv) > 6 else (240, 0, 1680, 850)
FONT = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
GOLD = (255, 214, 0)
tmp = tempfile.mkdtemp()
frame = os.path.join(tmp, "f.png")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", long_v, "-frames:v", "1", frame], check=True)
src = Image.open(frame).convert("RGB")
bg = src.crop((0, 0, 1920, 850)).resize((int(1920 * 1920 / 850), 1920))
x = (bg.width - 1080) // 2
bg = bg.crop((x, 0, x + 1080, 1920)).filter(ImageFilter.GaussianBlur(30))
bg = ImageEnhance.Brightness(bg).enhance(0.45)
fg = src.crop(box)
fh = int(fg.height * 1080 / fg.width)
fg = fg.resize((1080, fh), Image.LANCZOS)
y_fg = max(660, (1920 - fh) // 2 + 120)
bg.paste(fg, (0, y_fg))
d = ImageDraw.Draw(bg)
lines = [l for l in text.split("|") if l]
size = 112 if max(len(l.strip("*")) for l in lines) <= 13 else 92
f = ImageFont.truetype(FONT, size)
for i, l in enumerate(lines):
    gold = l.startswith("*") and l.endswith("*")
    d.text((540, 170 + i * int(size * 1.16)), l.strip("*"), font=f, fill=GOLD if gold else "white",
           anchor="mt", stroke_width=10, stroke_fill="black")
d.text((540, 1730), "BILLION DOLLAR MISTAKES", font=ImageFont.truetype(FONT, 48), fill=GOLD,
       anchor="mt", stroke_width=5, stroke_fill="black")
cover = os.path.splitext(tout)[0] + ".jpg"
bg.save(cover, quality=92)
fc = ("[0:v]scale=1080:1920,format=yuv420p,setsar=1[c];[2:v]setsar=1[m];"
      "[2:a]aresample=44100,aformat=channel_layouts=stereo[ma];[c][1:a][m][ma]concat=n=2:v=1:a=1[v][a]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-t", "0.5", "-framerate", "30", "-i", cover,
                "-f", "lavfi", "-t", "0.5", "-i", "anullsrc=r=44100:cl=stereo", "-i", tin, "-filter_complex", fc,
                "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-r", "30",
                "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", tout], check=True)
print(tout, cover)
