# compare.png(시안 3 + 경쟁 5 + 우리 3) · feed_375.png(어두운 휴대폰 목록 모의) — py -3.12 make_compare.py
import os
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(os.path.join(H, '..', '..', '..', '..'))
EP = os.path.join(R, 'work/research/longform/ep/A-1'); BN = os.path.join(R, 'work/research/design/A-1-thumb/bench')
F = lambda n: ImageFont.truetype(os.path.join(R, 'work/video/public/fonts/pd700.ttf'), n)
cells = [(os.path.join(EP, f'thumb_{k}.png'), f'시안 {k}') for k in ('v5a', 'v5b', 'v5c')] + [
 (os.path.join(BN, 'SCOI0DP-l-s.jpg'), '지금 걸린 v3(재탕·교체 대상)'),
 (os.path.join(BN, 'CB6ibr4KEcc.jpg'), '똑재TV 38.9만'), (os.path.join(BN, 'z6HQrJZUqOk.jpg'), '수페TV 27.9만'),
 (os.path.join(BN, 'rc0OBQNe7LU.jpg'), '수페TV 23.7만'), (os.path.join(BN, 'J0hc2v8DzRo.jpg'), '똑재TV 22.7만'),
 (os.path.join(BN, 'yRDpbgaZahc.jpg'), '은퇴머니 72.4만'), (os.path.join(BN, 'zhTjJwy1mwQ.jpg'), '우리 1위 1,971'),
 (os.path.join(BN, 'JVTYZ208hgw.jpg'), '우리 JVTYZ208hgw'), (os.path.join(BN, 'yGuybuoroRI.jpg'), '우리 yGuybuoroRI')]
W, TH, LB, C = 480, 270, 40, 4
im = Image.new('RGB', (W * C + 10 * (C + 1), (TH + LB + 10) * 3 + 10), '#0f0f0f'); d = ImageDraw.Draw(im)
for i, (p, lab) in enumerate(cells):
    x, y = 10 + (i % C) * (W + 10), 10 + (i // C) * (TH + LB + 10)
    im.paste(Image.open(p).convert('RGB').resize((W, TH), Image.LANCZOS), (x, y))
    d.text((x + 4, y + TH + 6), lab, font=F(24), fill='#FFD60A' if lab.startswith('시안') else '#dddddd')
im.save(os.path.join(H, 'compare.png'))
# 휴대폰 목록: 폭 375 중 썸네일 폭 약 168(검색 결과 옆 배치)과 343(홈 피드) 두 크기
fd = Image.new('RGB', (375 * 3 + 40, 560), '#0f0f0f'); d = ImageDraw.Draw(fd)
for j, k in enumerate(('v5a', 'v5b', 'v5c')):
    x0 = 10 + j * 385; t = Image.open(os.path.join(EP, f'thumb_{k}.png')).convert('RGB')
    fd.paste(t.resize((343, 193), Image.LANCZOS), (x0 + 16, 16)); d.text((x0 + 16, 216), 'JEPQ와 SCHD, 1억 넣고 1년 뒤…', font=F(18), fill='#f1f1f1')
    others = [Image.open(os.path.join(BN, n)).convert('RGB') for n in ('z6HQrJZUqOk.jpg', 'CB6ibr4KEcc.jpg')]
    for r, o in enumerate([t] + others):
        yy = 260 + r * 100; fd.paste(o.resize((168, 94), Image.LANCZOS), (x0 + 16, yy))
        d.text((x0 + 194, yy + 4), ['우리 ' + k, '수페TV', '똑재TV'][r], font=F(16), fill='#aaaaaa')
fd.save(os.path.join(H, 'feed_375.png')); print('ok')
