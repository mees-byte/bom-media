#!/usr/bin/env python3
"""Join rendered scenes + 1s thumbnail intro, mix voice/music/sfx, write VIDEO_DIR/VIDEO.mp4.
Usage: VIDEO_DIR=work python3 pipeline/render.py render 2 && VIDEO_DIR=work python3 pipeline/mix.py <thumbnail.png> [music.mp3]"""
import os, subprocess, sys
PIPE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.environ.get("VIDEO_DIR", "."))
thumb = sys.argv[1]
music = sys.argv[2] if len(sys.argv) > 2 else os.path.join(PIPE, "assets", "music.mp3")
os.chdir(ROOT)
run = lambda c: subprocess.run(c, check=True)
lst = subprocess.run(["python3", os.path.join(PIPE, "render.py"), "list"], capture_output=True, text=True, env=dict(os.environ, VIDEO_DIR=ROOT), check=True).stdout
S = [l.split() for l in lst.strip().splitlines()]
run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-framerate", "30", "-i", thumb, "-vf",
     "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,format=yuv420p,trim=duration=1.0",
     "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-r", "30", "scenes/intro.mp4"])
with open("concat_full.txt", "w") as f:
    f.write("file 'scenes/intro.mp4'\n")
    for i in range(len(S)): f.write(f"file 'scenes/s{i:03d}.mp4'\n")
run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", "concat_full.txt", "-c", "copy", "video_noaudio.mp4"])
D = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", "video_noaudio.mp4"], capture_output=True, text=True).stdout)
off = 1.0
ch = [float(s[2]) + off for s in S if s[1] == "chapter"]
cuts = [float(s[2]) + off for s in S if s[1] != "chapter"][1:]
im = []
for s in S:
    t = float(s[2]) + off
    if s[1] == "count": im.append(t + 1.35)
    if s[1] == "offer": im.append(t + 1.3)
    if s[1] == "bonus": im.append(t + 1.0)
    if s[1] == "checkmate": im.append(t + 0.9)
twist = ch[len(ch) // 2] if ch else D / 2
A = os.path.join(PIPE, "assets")
inputs = ["-i", "video_noaudio.mp4", "-i", "voice.mp3", "-stream_loop", "2", "-i", music]
fc = [f"[1:a]adelay=1000|1000,apad=whole_dur={D},asplit=2[v][vsc]",
      f"[2:a]atrim=0:{D},volume=0.24,volume='if(between(t,{twist-0.2},{twist+2.2}),0.15,1)':eval=frame,afade=t=in:d=0.5,afade=t=out:st={D-3}:d=3[m0]",
      "[m0][vsc]sidechaincompress=threshold=0.04:ratio=6:attack=20:release=400[m]"]
mix = []; k = 3
# no whoosh on cuts/chapters (owner request 2026-11-04); only impacts on big numbers
for t, vol, f in [(x, 0.45, "impact") for x in im]:
    inputs += ["-i", os.path.join(A, f + ".mp3")]
    ms = max(0, int(t * 1000 - (200 if f == "whoosh" else 0)))
    fc.append(f"[{k}:a]volume={vol},adelay={ms}|{ms}[x{k}]"); mix.append(f"[x{k}]"); k += 1
fc.append("[v][m]" + "".join(mix) + f"amix=inputs={2+len(mix)}:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11,volume=2dB,alimiter=limit=0.89[a]")
run(["ffmpeg", "-y", "-v", "error"] + inputs + ["-filter_complex", ";".join(fc), "-map", "0:v", "-map", "[a]", "-c:v", "copy",
     "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart", "VIDEO.mp4"])
print("VIDEO.mp4", D, "s; chapters at", [round(c) for c in ch])
