# C-39 경쟁 옆 홈 6장 판 (copywriter 11/27) — 판 PNG는 경쟁 썸네일 포함이라 git add 금지
import sys
from PIL import Image, ImageDraw, ImageFont
D='C:/Users/강영준/Documents/GitHub/retire-age-kr/work/research/visual/NDG-1-thumb/'
comp=['comp/e-dceDD09Us.jpg','comp/QIW7Den1dVM.jpg','comp/BHX-OBkk-3o.jpg','comp/_Qxy66N-yHc.jpg','comp/ihpmQU33A_g.jpg']
ours=sys.argv[1]; tag=sys.argv[2]
font=ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf',26)
W,H=412,232
for bi,pos in enumerate([1,4,5]):  # 0-based 자리: 2번·5번·6번
    rot=comp[bi:]+comp[:bi]
    items=rot[:pos]+[ours]+rot[pos:]
    B=Image.new('RGB',(3*W+40,2*(H+40)+10),'white'); d=ImageDraw.Draw(B)
    for i,p in enumerate(items):
        im=Image.open(D+p).convert('RGB').resize((W,H))
        x=10+(i%3)*(W+10); y=10+(i//3)*(H+40)
        B.paste(im,(x,y)); d.text((x,y+H+4),f'{i+1}번',fill='black',font=font)
    out=D+f'ut3/board_{tag}_{bi+1}.png'; B.save(out); print(out,'ours at',pos+1)
