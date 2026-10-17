# H-2 비교판 ep/H-2/thumb_compare.png — 우리 최종 h2y(13차) + 경쟁 상위 5(compete.md 표 1~5, mqdefault) + 우리 롱폼 조회 상위 3(H-1 compare.json과 같은 3편) + 지난 편 H-1 h1k. 위 줄 480px, 아래 줄 168px(같은 순서)
import os
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__)); EP = os.path.join(H, '..', '..', 'longform', 'ep')
items = [('우리 H-2 h2y(최종)', os.path.join(EP, 'H-2', 'thumb_h2y.png'))] + \
    [(f'경쟁 {c}', os.path.join(H, 'src', i + '.jpg')) for c, i in (('강투연 1.6만', 'bSrhZncUGD4'), ('강투연 1.3만', 'WzQebWiEi14'), ('강투연 4천', 'Us6f2rPmpr8'), ('돈불리GO 4천', 'pqVRJi2YfIA'), ('Turbo832 12만', 'ATut9O9qpoU'))] + \
    [(f'우리 조회 상위 {n}', os.path.join(H, 'src', i + '.jpg')) for n, i in (('A-1', 'SCOI0DP-l-s'), ('6월', 'scV67BQvC4Q'), ('N-1', '420buEFKB8k'))] + \
    [('우리 지난 편 H-1 h1k', os.path.join(EP, 'H-1', 'thumb_h1k.png'))]
F = ImageFont.truetype(r'C:\Windows\Fonts\malgunbd.ttf', 18)
def fit(p, W):
    im = Image.open(p).convert('RGB'); w, h = im.size; t = round(w * 9 / 16)
    if t < h: im = im.crop((0, (h - t) // 2, w, (h - t) // 2 + t))
    return im.resize((W, round(W * 9 / 16)), Image.LANCZOS)
cols, W, pad = 5, 480, 16; HH = 270
rows = (len(items) + cols - 1) // cols
small_h = 94 + 30
bd = Image.new('RGB', (cols * (W + pad) + pad, rows * (HH + 34) + pad + 2 * small_h + 40), '#0f0f0f'); d = ImageDraw.Draw(bd)
for n, (lab, p) in enumerate(items):
    x = pad + (n % cols) * (W + pad); y = pad + (n // cols) * (HH + 34)
    bd.paste(fit(p, W), (x, y)); d.text((x, y + HH + 6), lab, fill='white', font=F)
y0 = pad + rows * (HH + 34) + 20
d.text((pad, y0 - 4), '168px(휴대폰 목록 크기) 같은 순서', fill='#aaa', font=F)
for n, (lab, p) in enumerate(items):
    x = pad + n * (168 + 12); y = y0 + 24
    bd.paste(fit(p, 168), (x, y))
out = os.path.join(EP, 'H-2', 'thumb_compare.png'); bd.save(out); print(out, bd.size)
