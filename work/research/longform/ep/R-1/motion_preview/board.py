# R-1 첫 장면 비교판: 새(줌아웃) 4장 · 지금 4장 · 경쟁(수페TV·소수몽키 첫 장면) 4장 → board_open.png
import os, sys
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__)); YT = os.path.join(H, '..', '..', '..', '..', 'yt', 'full')
W, HH = 480, 270
F = ImageFont.truetype(r'C:\Windows\Fonts\malgunbd.ttf', 18)
def comp(ch, n):
    d = os.path.join(YT, ch); v = sorted(x for x in os.listdir(d) if os.path.isdir(os.path.join(d, x)))[0]
    fs = sorted(os.listdir(os.path.join(d, v)))[:n]; return [(f'{ch} {f[4:8]}초', Image.open(os.path.join(d, v, f))) for f in fs]
rows = [[(f'새 {fr/30:.1f}초', Image.open(os.path.join(H, f's_{fr}.png'))) for fr in (0, 230, 440, 690)],
        [(f'지금 {fr/30:.1f}초', Image.open(os.path.join(H, f'old_{fr}.png'))) for fr in (0, 230, 440, 690)],
        comp('수페TV', 2) + comp('소수몽키', 2)]
b = Image.new('RGB', (4 * (W + 8) + 8, 3 * (HH + 30) + 8), 'white'); d = ImageDraw.Draw(b)
for r, row in enumerate(rows):
    for c, (lab, im) in enumerate(row):
        x, y = 8 + c * (W + 8), 8 + r * (HH + 30)
        b.paste(im.convert('RGB').resize((W, HH)), (x, y + 24)); d.text((x, y), lab, fill='black', font=F)
b.save(os.path.join(H, 'board_open.png')); print('ok')
