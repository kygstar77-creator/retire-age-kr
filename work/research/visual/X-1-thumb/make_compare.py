# X-1 비교판 ep/X-1/thumb_compare.png — 우리 최고판 x1f + 예비 x1c(swap 문구 최고) + 경쟁 상위 5(compete_thumb.json, maxres) + 우리 롱폼 조회 상위 3. 위 480px, 아래 168px(같은 순서)
import os, json
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__)); EP = os.path.join(H, '..', '..', 'longform', 'ep')
cj = {r['id']: r for r in json.load(open(os.path.join(H, 'compete_thumb.json'), encoding='utf-8'))['top']}
COMP = '9sprlBRpDn8 jwEwdEUq0_Y L95ue7e0E_0 UcHK1WoTPtY f6MAA2GhsEk'.split()
items = [('우리 X-1 x1f(최고판)', os.path.join(EP, 'X-1', 'thumb_x1f.png')), ('우리 X-1 x1c(예비 문구)', os.path.join(EP, 'X-1', 'thumb_x1c.png'))] + \
    [(f"경쟁 {cj[i]['channel'][:8]} {cj[i]['views'] / 10000:.1f}만", os.path.join(H, 'src', i + '.jpg')) for i in COMP] + \
    [(f'우리 조회 상위 {n}', os.path.join(H, 'src', i + '.jpg')) for n, i in (('N-1', '420buEFKB8k'), ('A-1', 'SCOI0DP-l-s'), ('6월', 'scV67BQvC4Q'))]
F = ImageFont.truetype(r'C:\Windows\Fonts\malgunbd.ttf', 18)


def fit(p, W):
    im = Image.open(p).convert('RGB'); w, h = im.size; t = round(w * 9 / 16)
    if t < h: im = im.crop((0, (h - t) // 2, w, (h - t) // 2 + t))
    return im.resize((W, round(W * 9 / 16)), Image.LANCZOS)


cols, W, pad = 5, 480, 16; HH = 270
rows = (len(items) + cols - 1) // cols
small_h = 94 + 30
bd = Image.new('RGB', (cols * (W + pad) + pad, rows * (HH + 34) + pad + small_h + 40), '#0f0f0f'); d = ImageDraw.Draw(bd)
for n, (lab, p) in enumerate(items):
    x = pad + (n % cols) * (W + pad); y = pad + (n // cols) * (HH + 34)
    bd.paste(fit(p, W), (x, y)); d.text((x, y + HH + 6), lab, fill='white', font=F)
y0 = pad + rows * (HH + 34) + 20
d.text((pad, y0 - 4), '168px(휴대폰 목록 크기) 같은 순서', fill='#aaa', font=F)
for n, (lab, p) in enumerate(items):
    bd.paste(fit(p, 168), (pad + n * (168 + 12), y0 + 24))
out = os.path.join(EP, 'X-1', 'thumb_compare.png'); bd.save(out); print(out, bd.size)
