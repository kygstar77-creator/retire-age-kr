# RT-1 썸네일(visual 11/3 09시) — H-4 make_h4n.py 복사, 사진·문구만 바꿈(C-35 줄별 폭 85~95%, 큰 글 높이 45% 넘으면 줄임 C-02).
#   문구 ep/RT-1/copy/titles.md '11/3 고친 판' 1위 B 그대로: 흰 줄 '퇴직금·근속 24가지로 IRP 세금 셈해 보니' / 큰 흰 '1천만원 넘게 아끼는 건' / 큰 주황 '24가지 중 3가지뿐' · 알약 없음(C-10)
#   사실 facts [F3] 24경우 중 IRP로 아끼는 세금 1천만원 넘는 칸 3. 사진 Pexels 9301822·4498123·4226206 — 퇴직 날 짐 상자, 얼굴 없음, photo/sources.json
import os, sys
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
O = os.path.dirname(os.path.abspath(__file__)); H = os.path.join(O, 'photo'); WORK = os.path.abspath(os.path.join(O, '..', '..', '..'))
FONT = os.path.join(WORK, 'fonts'); W, HH = 1920, 1080; X0 = 80; MAXW = 1760
ORANGE, WHITE, INK = (255, 90, 0), (255, 255, 255), (10, 11, 14)
BIG = ['1천만원 넘게 아끼는 건', '24가지 중 3가지뿐']
def f(size, w='700'):
    if w == 'black':
        ft = ImageFont.truetype(os.path.join(FONT, 'NotoSansKR-Black.ttf'), size); ft.set_variation_by_name('Black'); return ft
    return ImageFont.truetype(os.path.join(FONT, f'pd{w}.ttf'), size)
def photo(name, y_anchor=0.0, x_anchor=0.5, zoom=1.0):
    im = Image.open(os.path.join(H, name)).convert('RGB'); r = max(W / im.width, HH / im.height) * zoom
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x = int((im.width - W) * x_anchor); y = int((im.height - HH) * y_anchor); return im.crop((x, y, x + W, y + HH))
def shade(im, y0, y1, alpha, top=False):
    m = Image.new('L', im.size, 0); d = ImageDraw.Draw(m)
    for y in range(y0, y1):
        t = (y - y0) / max(1, (y1 - y0) * 0.45) if not top else (y1 - y) / max(1, (y1 - y0) * 0.45)
        d.line([(0, y), (W, y)], fill=int(alpha * min(1, t)))
    return Image.composite(Image.new('RGB', im.size, INK), im, m)
def fit(d, t, size, w, maxw=MAXW, floor=40):
    while size > floor and d.textlength(t, font=f(size, w)) > maxw: size -= 2
    return size


def make(out, pic, ya, top, top_size=96, band=235, ls=1.10, target=0.90, xa=0.5, zoom=1.0, top_sizes=None, hmax=0.45, tshade=(300, 200)):
    im = photo(pic, y_anchor=ya, x_anchor=xa, zoom=zoom); d0 = ImageDraw.Draw(im)
    # C-35: 줄마다 크기 따로 — 폭 target에 맞춤. 짧은 첫 줄('서울 25개 구 중')이 커져 두 줄이 화면 45%(C-02)를 넘으면 둘을 같은 비율로 줄임
    sizes = [fit(d0, t, 320, 'black', maxw=int(W * target)) for t in BIG]
    hb = sum(int(s * ls) for s in sizes)
    if hb > HH * hmax: k = HH * hmax / hb; sizes = [int(s * k) for s in sizes]; hb = sum(int(s * ls) for s in sizes)
    y = HH - 30 - hb
    top_size = min(fit(d0, tl, top_size, '700') for tl in top.split('|'))
    tsz = top_sizes or [top_size] * len(top.split('|'))
    im = shade(im, max(0, y - 160), HH, band); im = shade(im, 0, tshade[0], tshade[1], top=True); d = ImageDraw.Draw(im)
    ty = 36
    for tl, ts in zip(top.split('|'), tsz):
        d.text((X0, ty), tl, font=f(ts, '700'), fill=WHITE, stroke_width=4 if ts < 120 else 6, stroke_fill=INK); ty += int(ts * 1.18)
    widths = []
    for k, (t, s) in enumerate(zip(BIG, sizes)):
        bb = d.textbbox((X0, y - int(s * 0.12)), t, font=f(s, 'black'), stroke_width=6); widths.append((bb[2] - bb[0]) / W)
        d.text((X0, y - int(s * 0.12)), t, font=f(s, 'black'), fill=WHITE if k == 0 else ORANGE, stroke_width=6, stroke_fill=INK); y += int(s * ls)
    sm = im.resize((1280, 720), Image.LANCZOS); sm.save(os.path.join(O, out))
    for px in (412, 168): sm.resize((px, px * 9 // 16), Image.LANCZOS).save(os.path.join(O, out.replace('.png', f'_{px}.png')))
    print(out, f'흰 줄 {tsz}px · 큰 글 {sizes}px · 줄별 폭 ' + '·'.join(f'{w:.0%}' for w in widths) + f' · 높이 {hb / HH:.0%}')


T = '광명 아파트 15억이라던데, 실거래 전부 세어 보니'


T = '퇴직금·근속 24가지로 IRP 세금 셈해 보니'
T2 = '퇴직금·근속 24가지로|IRP 세금 셈해 보니'   # S-1·H-4 교훈: 168px에서 주제 낱말이 읽히게 두 줄로 키움
make('rt1n_b.png', 'office_box_plant_9301822.jpg', 0.5, T2, top_sizes=[120, 120])
make('rt1n_c.png', 'box_hands_top_4498123.jpg', 0.4, T2, top_sizes=[120, 120])
# 11/3 2차: b·c 상자가 큰 글 그라데이션에 묻힘(C-03 주인공 위쪽 55~60%) → 당겨 찍기(zoom)로 상자 윗면·손을 위로
make('rt1n_b2.png', 'office_box_plant_9301822.jpg', 0.62, T2, top_sizes=[120, 120], zoom=1.45, xa=0.42)
make('rt1n_c2.png', 'box_hands_top_4498123.jpg', 0.15, T2, top_sizes=[120, 120], zoom=1.25, xa=0.6)
# 11/3 3차: 상자가 화면 가운데 위에 오는 사진(Pexels 4226206 사무용품 상자 든 몸통, 얼굴 없음) — 위로 당겨 자름
make('rt1n_d.png', 'office_box_carry_4226206.jpg', 0.55, T2, top_sizes=[120, 120])
make('rt1n_d2.png', 'office_box_carry_4226206.jpg', 0.75, T2, top_sizes=[120, 120], zoom=1.2)
# 11/3 4차: 1초 시험(제미나이 2번·레드팀) 셋 다 '168px 위 흰 두 줄 안 읽힘' → 흰 줄만 120→150px, 위 그라데이션 진하게(H-4 g2 교훈)
make('rt1n_d3.png', 'office_box_carry_4226206.jpg', 0.55, T2, top_sizes=[150, 150], tshade=(440, 240))
