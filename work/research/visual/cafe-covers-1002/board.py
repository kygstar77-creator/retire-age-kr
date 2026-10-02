# 비교판: 우리 새 표지 + 네이버 카페 탭 상위 글 썸네일(모바일 검색 2026-10-02 15:3x, search.pstatic f192_192 정사각형)을
# 휴대폰 목록 크기(110px)로 한 판에. 같은 글의 두 번째 사진은 뺀다.
#   py -3.12 board.py
import os, json, sys
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, '..', '..')
meta = json.load(open(os.path.join(H, 'comp', 'comp.json'), encoding='utf-8'))
S = 110; F = ImageFont.truetype(r'C:\Windows\Fonts\malgunbd.ttf', 12)
for name, comps in meta.items():
    seen, items = set(), [('우리 새 표지', os.path.join(R, name, 'pkg', 'img', '00.png'))]
    for c in comps:
        if c['link'] in seen: continue
        seen.add(c['link']); items.append((f'경쟁 {len(items)}', os.path.join(H, 'comp', c['file'])))
    items = items[:6]
    pad = 12; bd = Image.new('RGB', (len(items) * (S + pad) + pad, S + 2 * pad + 20), 'white'); d = ImageDraw.Draw(bd)
    for i, (lab, p) in enumerate(items):
        im = Image.open(p).convert('RGB'); w, h = im.size; m = min(w, h)
        im = im.crop(((w - m) // 2, (h - m) // 2, (w - m) // 2 + m, (h - m) // 2 + m)).resize((S, S), Image.LANCZOS)
        x = pad + i * (S + pad); bd.paste(im, (x, pad)); d.text((x, pad + S + 4), lab, fill='black', font=F)
    bd.save(os.path.join(H, f'board_{name}.png')); print(name, bd.size, [l for l, _ in items])
