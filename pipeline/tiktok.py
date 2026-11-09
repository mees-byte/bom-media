#!/usr/bin/env python3
"""Cut a 9:16 TikTok from the long video (0 credits). Same look as shorts.py, but laid out for TikTok's UI:
hook text top (frame 0), channel name directly under the video (TikTok's caption/buttons cover the bottom ~25%).
Usage: python3 tiktok.py VIDEO.mp4 START_SEC DURATION_SEC "HOOK TEXT (max ~6 words)" out.mp4 [NAME]
Default NAME = "BILLION DOLLAR MISTAKES". Use 60–90 s for the daily main TikTok (TikTok only pays for videos > 1 min)."""
import subprocess, sys, textwrap
src, start, dur, hook, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4], sys.argv[5]
name = sys.argv[6] if len(sys.argv) > 6 else ""  # owner 2026-11-09: no channel name on TikToks
FONT = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
lines = textwrap.wrap(hook.upper(), 16)[:3]
draw = []
y0 = 300 if len(lines) < 3 else 250
for i, ln in enumerate(lines):
    ln = ln.replace("'", "’").replace(":", "\\:")
    draw.append(f"drawtext=fontfile={FONT}:text='{ln}':fontsize=92:fontcolor=white:borderw=8:bordercolor=black:x=(w-text_w)/2:y={y0 + i*110}")
if name: draw.append(f"drawtext=fontfile={FONT}:text='{name}':fontsize=44:fontcolor=0xFFD600:borderw=4:bordercolor=black:x=(w-text_w)/2:y=1390")
fc = ("[0:v]split=2[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:2,eq=brightness=-0.25[bg];"
      "[b]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2+80," + ",".join(draw) + ",format=yuv420p[v]")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(start), "-t", str(dur), "-i", src, "-filter_complex", fc,
                "-map", "[v]", "-map", "0:a", "-af", f"afade=t=out:st={max(dur-0.4, 0)}:d=0.4",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-c:a", "aac", "-b:a", "160k",
                "-r", "30", "-movflags", "+faststart", out], check=True)
print(out)
