import sys, importlib.util
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
spec = importlib.util.spec_from_file_location("R", "/home/claude/bom-media/pipeline/render.py")
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
W,H=1920,1080; GOLD=R.GOLD
src=sys.argv[1]; out=sys.argv[2]; person=len(sys.argv)>3
im=Image.open(src).convert("RGB")
s=max(W/im.width,H/im.height); im=im.resize((int(im.width*s)+1,int(im.height*s)+1),Image.LANCZOS)
im=im.crop(((im.width-W)//2,(im.height-H)//2,(im.width-W)//2+W,(im.height-H)//2+H))
im=ImageEnhance.Contrast(im).enhance(1.1); img=im.convert("RGBA")
g=Image.new("RGBA",(W,H),(0,0,0,0)); gd=ImageDraw.Draw(g)
for x in range(W):
    a=int(215*max(0,min(1,(x-700)/500))); gd.line([(x,0),(x,H)],fill=(6,14,34,a))
img.alpha_composite(g); d=ImageDraw.Draw(img); X=1870
def T(y,s_,size,col=(255,255,255)): d.text((X,y),s_,font=R.F(size),fill=col,anchor="rm",stroke_width=14,stroke_fill=(0,0,0))
T(200,"2027 PREMIUM",120); T(420,"$209.50?",230,GOLD)
pill="YOUR 2025 TAXES MATTER"; f=R.F(76); pw=f.getlength(pill)+70
d.rounded_rectangle([X-pw,590,X,720],30,fill=(250,247,238),outline=(0,0,0),width=6)
d.text((X-pw/2,655),pill,font=f,fill=(15,22,45),anchor="mm")
img.convert("RGB").save(out+".png"); img.convert("RGB").resize((1280,720),Image.LANCZOS).save(out+".jpg",quality=92)
