import sys,os
sys.path.insert(0,r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
from PIL import Image,ImageDraw,ImageFilter,ImageEnhance
import cardshort as C
H=os.path.dirname(os.path.abspath(__file__))
W,HH=1080,1920
bg=Image.open(os.path.join(H,'gold_photo.jpg')).convert('RGB').resize((W,HH),Image.LANCZOS).filter(ImageFilter.GaussianBlur(3))
bg=ImageEnhance.Brightness(ImageEnhance.Contrast(bg).enhance(1.2)).enhance(1.35)
d=ImageDraw.Draw(bg)
def txt(x,y,s,f,fill,sw=14):
    d.text((x,y),s,font=f,fill=fill,stroke_width=sw,stroke_fill=(0,0,0))
f1=C.BHS(190); f2=C.BHS(330); f3=C.BHS(110)
txt(50,200,'금 -34%, 왜',f1,(255,255,255))
txt(30,470,'+51%?',f2,(255,214,0),20)
txt(64,1560,'1/29 고점 → 10/6',f3,(255,255,255),10)
bg.save(os.path.join(H,'ff_v8b.png'))
