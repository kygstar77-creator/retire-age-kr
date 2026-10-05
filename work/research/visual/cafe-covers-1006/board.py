import os, json, sys
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
H=os.path.dirname(os.path.abspath(__file__)); R=os.path.join(H,'..','..')
meta=json.load(open(os.path.join(H,'comp','comp.json'),encoding='utf-8'))
ours={'hfguar1006_B5':('hfguar1006','hfguar1006/covers_try/00_B5.png'),
      'retmid1005_v4':('retmid1005','retmid1005/covers_try/00_v4_396more.png'),
      'retmid1005_v5':('retmid1005','retmid1005/covers_try/00_v5_plus396.png'),
      'retmid1005_cur':('retmid1005','retmid1005/pkg/img/00.png')}
S=110; F=ImageFont.truetype(r'C:\Windows\Fonts\malgunbd.ttf',12)
for key,(k,p) in ours.items():
    items=[('우리 새 표지',os.path.join(R,p))]
    for c in meta[k][:5]: items.append((f'경쟁 {len(items)}',os.path.join(H,'comp',c['file'])))
    pad=12; bd=Image.new('RGB',(len(items)*(S+pad)+pad,S+2*pad+20),'white'); d=ImageDraw.Draw(bd)
    for i,(lab,pp) in enumerate(items):
        im=Image.open(pp).convert('RGB'); w,h=im.size; m=min(w,h)
        im=im.crop(((w-m)//2,(h-m)//2,(w-m)//2+m,(h-m)//2+m)).resize((S,S),Image.LANCZOS)
        x=pad+i*(S+pad); bd.paste(im,(x,pad)); d.text((x,pad+S+4),lab,fill='black',font=F)
    bd.save(os.path.join(H,f'board_{key}.png')); print(key,bd.size)
