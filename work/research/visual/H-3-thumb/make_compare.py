# H-3 비교판 ep/H-3/thumb_compare.png — 우리 시안(최고판 먼저) + 경쟁 상위 5(ep/H-3/compete.md 표 1~5, maxresdefault) + 우리 롱폼 조회 상위 3(H-2 비교판과 같은 3편).
#   위: 480px, 아래 줄: 168px(같은 순서). py -3.12 make_compare.py h3c,h3a,h3b
import os, sys
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__)); EP = os.path.join(H, '..', '..', 'longform', 'ep')
ours = sys.argv[1].split(',')
items = [(f'우리 H-3 {k}' + ('(최고판)' if n == 0 else ''), os.path.join(EP, 'H-3', f'thumb_{k}.png')) for n, k in enumerate(ours)] + \
    [(f'경쟁 {c}', os.path.join(H, 'src', i + '.jpg')) for c, i in (('부동산오감스 4.2만', 'QO-6aWpqVm4'), ('고부자 1.6만', '4O6trzyjalI'), ('서울아파트 찍어주는 오빠 1.3만', 'TPD-zw4TvG4'), ('돈불리GO 3.4천', 'BAO0xDdBGVI'), ('돈불리GO 2.4천', 'y76t2BQ4O6s'))] + \
    [(f'우리 조회 상위 {n}', os.path.join(H, 'src', i + '.jpg')) for n, i in (('A-1', 'SCOI0DP-l-s'), ('6월', 'scV67BQvC4Q'), ('N-1', '420buEFKB8k'))]
F = ImageFont.truetype(r'C:\Windows\Fonts\malgunbd.ttf', 18)
def fit(p, W):
    im = Image.open(p).convert('RGB'); w, h = im.size; t = round(w * 9 / 16)
    if t < h: im = im.crop((0, (h - t) // 2, w, (h - t) // 2 + t))
    return im.resize((W, round(W * 9 / 16)), Image.LANCZOS)
cols, W, pad = 4, 480, 16; HH = 270
rows = (len(items) + cols - 1) // cols
small_cols = 6; srows = (len(items) + small_cols - 1) // small_cols
bd = Image.new('RGB', (cols * (W + pad) + pad, rows * (HH + 34) + pad + srows * 124 + 40), '#0f0f0f'); d = ImageDraw.Draw(bd)
for n, (lab, p) in enumerate(items):
    x = pad + (n % cols) * (W + pad); y = pad + (n // cols) * (HH + 34)
    bd.paste(fit(p, W), (x, y)); d.text((x, y + HH + 6), lab, fill='white', font=F)
y0 = pad + rows * (HH + 34) + 20
d.text((pad, y0 - 4), '168px(휴대폰 목록 크기) 같은 순서', fill='#aaa', font=F)
for n, (lab, p) in enumerate(items):
    x = pad + (n % small_cols) * (168 + 12); y = y0 + 24 + (n // small_cols) * 124
    bd.paste(fit(p, 168), (x, y))
out = os.path.join(EP, 'H-3', 'thumb_compare.png'); bd.save(out); print(out, bd.size)
