#!/usr/bin/env python3
"""Light attention sound effects, synthesised locally (numpy) — no credits, no whooshes/sweeps.
Builds VIDEO_DIR/sfx.wav (48 kHz mono, same timeline as VIDEO.mp4 incl. the 1 s thumbnail intro) from the scene list.
mix.py mixes it in automatically when sfx.wav exists.
Usage: VIDEO_DIR=work python3 pipeline/sfx.py
Sounds are short and quiet (−24…−30 dBFS peaks before the mix): soft pops on text reveals, clock ticks, paper/key clicks,
an ice crackle on freezes, a soft low thump on chapter cards, a two-note chime on questions/matches, a digital glitch on
the laptop/breach scene, a cash-drawer 'ding' on the subscribe click. Never on every cut: titles get a pop on ~every 2nd one."""
import os, subprocess, numpy as np
PIPE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.environ.get("VIDEO_DIR", "."))
SR = 48000; OFF = 1.0
rng = np.random.default_rng(7)
def t_(d): return np.arange(int(SR * d)) / SR
def env(x, a=0.003, dec=20.0):
    t = t_(len(x) / SR); return x * np.minimum(1, t / a) * np.exp(-dec * t)
def pop():      t = t_(.12); return env(np.sin(2*np.pi*(380 + 900*t)*t), dec=38) * .5
def tick():     t = t_(.03); return env(np.sin(2*np.pi*2600*t) + .5*rng.standard_normal(len(t)), a=.0005, dec=180) * .35
def click():    t = t_(.025); return env(rng.standard_normal(len(t)), a=.0003, dec=260) * .30
def thump():    t = t_(.6); return env(np.sin(2*np.pi*(70 - 25*t)*t), a=.004, dec=7) * .9
def chime():
    t = t_(.9); return env(np.sin(2*np.pi*880*t) + .7*np.sin(2*np.pi*1320*t)*(t > .09), a=.002, dec=5) * .28
def crackle():
    t = t_(.7); n = rng.standard_normal(len(t)) * (rng.random(len(t)) > .985)
    n = np.convolve(n, np.exp(-np.arange(60) / 8), "same"); return env(n, a=.002, dec=5) * .35
def glitch():
    t = t_(.35); g = np.sign(np.sin(2*np.pi*180*t)) * ((np.floor(t*40) % 3) != 0)
    return env(g + .4*rng.standard_normal(len(t)), a=.001, dec=6) * .16
def ding():     t = t_(.7); return env(np.sin(2*np.pi*1568*t) + .4*np.sin(2*np.pi*2349*t), a=.001, dec=6) * .25

lst = subprocess.run(["python3", os.path.join(PIPE, "render.py"), "list"], capture_output=True, text=True,
                     env=dict(os.environ, VIDEO_DIR=ROOT), check=True).stdout.split("\n")
S = [l.split() for l in lst if l.strip()]
end = float(S[-1][2]) + float(S[-1][3]) + OFF + 2
out = np.zeros(int(SR * end))
def put(sound, at, gain=1.0):
    i = int(SR * at); out[i:i + len(sound)] += sound[:max(0, len(out) - i)] * gain
nt = 0
for _, kind, t0, dur in S:
    t, d = float(t0) + OFF, float(dur)
    if kind == "chapter": put(thump(), t + .02)
    elif kind in ("title", "photo"):
        nt += 1
        if nt % 2: put(pop(), t + .08)
    elif kind in ("clock", "timer", "counter"):
        for k in range(int(min(d, 3.5) / .5)): put(tick(), t + .1 + k * .5, .9 if k % 2 else 1)
    elif kind in ("slips", "rehearsal", "chains", "stores_grid"):
        for k in range(10 if kind == "chains" else 6): put(click(), t + .25 + k * (.15 if kind == "chains" else .22), .8)
    elif kind == "slip": put(click(), t + .7); put(click(), t + 1.1)
    elif kind == "freeze": put(crackle(), t + 1.0)
    elif kind in ("question", "comment", "comment2"): put(chime(), t + .1)
    elif kind == "laptop": put(glitch(), t + .65)
    elif kind == "subscribe": put(click(), t + 1.6); put(ding(), t + 1.65)
    elif kind == "broll": put(pop(), t + .25, .6)
    elif kind == "date": put(tick(), t + .1); put(tick(), t + .4); put(tick(), t + .7)
# 'ONE MATCHED' on the second slips scene
sl = [s for s in S if s[1] == "slips"]
if len(sl) > 1: put(chime(), float(sl[1][2]) + OFF + .55)
out = out / max(1e-9, np.abs(out).max()) * 0.5
pcm = (out * 32767).astype(np.int16)
p = os.path.join(ROOT, "sfx.wav")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-", p], input=pcm.tobytes(), check=True)
print("sfx.wav", round(end, 1), "s")
