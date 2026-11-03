#!/usr/bin/env python3
"""Cut a 9:16 YouTube Short from the long video.
Usage: python3 shorts.py VIDEO.mp4 START_SEC DURATION_SEC "HOOK TEXT (max ~6 words)" out.mp4
Layout: blurred full-frame background, the 16:9 video centered, hook text on top (frame 0), channel tag at bottom."""
import subprocess, sys, textwrap
src, start, dur, hook, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4], sys.argv[5]
FONT = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
lines = textwrap.wrap(hook.upper(), 16)[:3]
draw = []
for i, ln in enumerate(lines):
    ln = ln.replace("'", "’").replace(":", "\\:")
    draw.append(f"drawtext=fontfile={FONT}:text='{ln}':fontsize=92:fontcolor=white:borderw=8:bordercolor=black:x=(w-text_w)/2:y={300 + i*110}")
draw.append(f"drawtext=fontfile={FONT}:text='@billiondollarmistakes':fontsize=44:fontcolor=0xFFD600:borderw=4:bordercolor=black:x=(w-text_w)/2:y=1600")
fc = ("[0:v]split=2[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:2,eq=brightness=-0.25[bg];"
      "[b]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2+80," + ",".join(draw) + ",format=yuv420p[v]")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(start), "-t", str(dur), "-i", src, "-filter_complex", fc,
                "-map", "[v]", "-map", "0:a", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-c:a", "aac", "-b:a", "160k",
                "-r", "30", "-movflags", "+faststart", out], check=True)
print(out)
