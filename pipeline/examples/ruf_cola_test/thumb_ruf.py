import os, sys, importlib.util
from PIL import Image, ImageDraw
spec = importlib.util.spec_from_file_location("R", "/home/claude/bom-media/pipeline/render.py")
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
def make(variant, out):
    if variant == "A":
        img = R.photo_base("mailbox", "bright").crop((0, 0, R.W, R.H)).convert("RGBA")
        img.alpha_composite(Image.new("RGBA", img.size, (6, 14, 34, 120)))
    else:
        img = R.BGS["navy"].crop((100, 60, 100 + R.W, 60 + R.H)).convert("RGBA")
    # notice illustration on the right
    a = dict(hl=2, anim=False); R.KINDS["notice"](img, 5, 5, a) if variant == "B" else None
    d = ImageDraw.Draw(img)
    def T(s, size, y, col=(255, 255, 255), x=90):
        d.text((x, y), s, font=R.F(size), fill=col, anchor="lm", stroke_width=14, stroke_fill=(0, 0, 0))
    if variant == "A":
        T("YOUR RAISE", 150, 250)
        T("$75", 430, 560, R.GOLD)
        T("ISN'T $75", 130, 840 - 10)
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(lay).text((1050, 520), "?", font=R.F(420), fill=R.GOLD + (255,), anchor="mm", stroke_width=14, stroke_fill=(0, 0, 0, 255))
        img.alpha_composite(lay.rotate(10, center=(1050, 520)))
    else:
        T("READ", 150, 260); T("THIS LINE", 150, 420, R.GOLD); T("FIRST", 150, 580)
    img.convert("RGB").resize((1280, 720)).save(out + ".jpg", quality=92)
    img.convert("RGB").save(out + ".png")
make("A", "work/thumb_A"); make("B", "work/thumb_B")
