import importlib.util
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
spec = importlib.util.spec_from_file_location("R", "/home/claude/bom-media/pipeline/render.py")
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
W,H=1920,1080; GOLD=R.GOLD
im=Image.open("/home/claude/med90/frank2.png").convert("RGB")
s=max(W/im.width,H/im.height); im=im.resize((int(im.width*s)+1,int(im.height*s)+1),Image.LANCZOS).crop((0,0,W,H))
im=ImageEnhance.Contrast(im).enhance(1.1)
img=im.convert("RGBA")
g=Image.new("RGBA",(W,H),(0,0,0,0)); gd=ImageDraw.Draw(g)
for x in range(W):
    a=int(200*max(0,min(1,(x-1000)/500))); gd.line([(x,0),(x,H)],fill=(6,14,34,a))
img.alpha_composite(g); d=ImageDraw.Draw(img)
X=1880
def T(y,s,size,col=(255,255,255)): d.text((X,y),s,font=R.F(size),fill=col,anchor="rm",stroke_width=14,stroke_fill=(0,0,0))
T(220,"WHERE'S",150); T(400,"MY $90?",190,GOLD)
pill="-$214 A YEAR"; f=R.F(86); pw=f.getlength(pill)+70
d.rounded_rectangle([X-pw,540,X,680],30,fill=(250,247,238),outline=(0,0,0),width=6)
d.text((X-pw/2,610),pill,font=f,fill=(15,22,45),anchor="mm")
img.convert("RGB").save("/home/claude/med90/thumb.png"); img.convert("RGB").resize((1280,720),Image.LANCZOS).save("/home/claude/med90/thumb.jpg",quality=92)
