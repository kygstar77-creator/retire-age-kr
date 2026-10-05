# 우리 1위 시안 vs 경쟁 1등(조회 최다 단희TV gosYz3ho038 139만) 나란한 비교판 + 어두운 유튜브 목록 위 168px — py -3.12 top1_board.py r2e
import sys, os
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__)); EP = os.path.join(H, '..', '..', 'longform', 'ep', 'R-1')
k = sys.argv[1]; F = ImageFont.truetype(r'C:\Windows\Fonts\malgunbd.ttf', 15)
def fit(p, W):
    im = Image.open(p).convert('RGB'); w, h = im.size; t = round(w * 9 / 16)
    if t < h: im = im.crop((0, (h - t) // 2, w, (h - t) // 2 + t))
    return im.resize((W, round(W * 9 / 16)), Image.LANCZOS)
items = [(os.path.join(EP, f'thumb_{k}.png'), f'우리 {k}'), (os.path.join(H, 'src', 'gosYz3ho038.jpg'), '경쟁 1등 단희TV 139만회')]
for W in (168, 480):
    HH = round(W * 9 / 16); bd = Image.new('RGB', (2 * W + 36, HH + 40), '#0F0F0F'); d = ImageDraw.Draw(bd)
    for i, (p, lab) in enumerate(items):
        bd.paste(fit(p, W), (12 + i * (W + 12), 12)); d.text((12 + i * (W + 12), HH + 16), lab, fill='#F1F1F1', font=F)
    bd.save(os.path.join(H, f'{k}_top1_{W}.png')); print(f'{k}_top1_{W}.png', bd.size)
