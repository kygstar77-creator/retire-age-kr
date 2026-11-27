# C-39 경쟁 옆 홈 6장 판 (copywriter 11/27) — 판 PNG는 경쟁 썸네일 포함이라 git add 금지
import sys,glob
from PIL import Image, ImageDraw, ImageFont
ours,compdir,outpre=sys.argv[1],sys.argv[2],sys.argv[3]
comp=sorted(glob.glob(compdir+'/*.jpg'))[:5]
font=ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf',26)
W,H=412,232
for bi,pos in enumerate([1,4,5]):
    rot=comp[bi:]+comp[:bi]; items=rot[:pos]+[ours]+rot[pos:]
    B=Image.new('RGB',(3*W+40,2*(H+40)+10),'white'); d=ImageDraw.Draw(B)
    for i,p in enumerate(items):
        x=10+(i%3)*(W+10); y=10+(i//3)*(H+40)
        B.paste(Image.open(p).convert('RGB').resize((W,H)),(x,y)); d.text((x,y+H+4),f'{i+1}번',fill='black',font=font)
    B.save(f'{outpre}_{bi+1}.png'); print(bi+1,'ours at',pos+1)
