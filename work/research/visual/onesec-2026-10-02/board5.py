# F5: 우리 d1k·d1l·d1m + 경쟁 5, 168px 한 판(GPT 웹 1회 업로드용)
import os, json
from PIL import Image, ImageDraw, ImageFont
H=os.path.dirname(os.path.abspath(__file__)); V=os.path.dirname(H); EP=os.path.join(V,'..','longform','ep')
W,HH=168,95; F=ImageFont.truetype(r'C:\Windows\Fonts\malgunbd.ttf',13)
D1C=[c['id'] for c in json.load(open(os.path.join(V,'D-1-thumb','compare.json'),encoding='utf-8')) if c['who']=='경쟁'][:5]
def small(p):
    im=Image.open(p).convert('RGB'); w,h=im.size; t=round(w*9/16)
    if t<h: im=im.crop((0,(h-t)//2,w,(h-t)//2+t))
    return im.resize((W,HH),Image.LANCZOS)
items=[(f'우리 {t.upper()}',os.path.join(EP,'D-1',f'thumb_{t}.png')) for t in ('d1k','d1l','d1m')]+[(f'경쟁 {i+1}',os.path.join(V,'D-1-thumb','src',k+'.jpg')) for i,k in enumerate(D1C)]
cols,pad=4,12; rows=2
bd=Image.new('RGB',(cols*(W+pad)+pad,rows*(HH+30)+pad),'white'); d=ImageDraw.Draw(bd)
for n,(lab,p) in enumerate(items):
    x=pad+(n%cols)*(W+pad); y=pad+(n//cols)*(HH+30); bd.paste(small(p),(x,y)); d.text((x,y+HH+4),lab,fill='black',font=F)
bd.save(os.path.join(H,'board5_d1klm.png')); print(bd.size, D1C)
