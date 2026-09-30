# compare.png(시안 3 + 경쟁 5 + 우리 3) · feed_375.png(어두운 휴대폰 목록 모의) — py -3.12 make_compare.py
# 경쟁: ep/E-1/yt_0930.json 조회 상위 중 메모리·반도체 주제 5편(VNlom76zR6g는 썸네일 없음으로 제외 → 안될공학)
import os
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(os.path.join(H, '..', '..', '..', '..'))
EP = os.path.join(R, 'work/research/longform/ep/E-1'); BN = os.path.join(H, 'bench')
F = lambda n: ImageFont.truetype(os.path.join(R, 'work/video/public/fonts/pd700.ttf'), n)
V = ('e1a', 'e1b', 'e1c')
cells = [(os.path.join(EP, f'thumb_{k}.png'), f'시안 {k}') for k in V] + [
 (os.path.join(BN, 'wu8GBMPD_xk.jpg'), '에디 30.5만'), (os.path.join(BN, '-Yh53SjCAiw.jpg'), '돈워리 11.8만'),
 (os.path.join(BN, 'tVaz2qoAySM.jpg'), 'FutureScope 11.7만'), (os.path.join(BN, 'gJTto7SP8w0.jpg'), '안될공학 11.0만'),
 (os.path.join(BN, 'cBFFyqiKFRs.jpg'), '고덕달팽이 6.2만(3.35배)'), (os.path.join(BN, 'zhTjJwy1mwQ.jpg'), '우리 1위 1,971'),
 (os.path.join(BN, 'JVTYZ208hgw.jpg'), '우리 2위 1,130'), (os.path.join(BN, 'yGuybuoroRI.jpg'), '우리 yGuybuoroRI')]
W, TH, LB, C = 480, 270, 40, 4
im = Image.new('RGB', (W * C + 10 * (C + 1), (TH + LB + 10) * 3 + 10), '#0f0f0f'); d = ImageDraw.Draw(im)
for i, (p, lab) in enumerate(cells):
    x, y = 10 + (i % C) * (W + 10), 10 + (i // C) * (TH + LB + 10)
    im.paste(Image.open(p).convert('RGB').resize((W, TH), Image.LANCZOS), (x, y))
    d.text((x + 4, y + TH + 6), lab, font=F(24), fill='#FFD60A' if lab.startswith('시안') else '#dddddd')
im.save(os.path.join(H, 'compare.png'))
fd = Image.new('RGB', (375 * 3 + 40, 560), '#0f0f0f'); d = ImageDraw.Draw(fd)
for j, k in enumerate(V):
    x0 = 10 + j * 385; t = Image.open(os.path.join(EP, f'thumb_{k}.png')).convert('RGB')
    fd.paste(t.resize((343, 193), Image.LANCZOS), (x0 + 16, 16)); d.text((x0 + 16, 216), '삼성전자 이익 19배, 주가는 3배…', font=F(18), fill='#f1f1f1')
    others = [Image.open(os.path.join(BN, n)).convert('RGB') for n in ('tVaz2qoAySM.jpg', 'cBFFyqiKFRs.jpg')]
    for r, o in enumerate([t] + others):
        yy = 260 + r * 100; fd.paste(o.resize((168, 94), Image.LANCZOS), (x0 + 16, yy))
        d.text((x0 + 194, yy + 4), ['우리 ' + k, 'FutureScope', '고덕달팽이'][r], font=F(16), fill='#aaaaaa')
fd.save(os.path.join(H, 'feed_375.png')); print('ok')
