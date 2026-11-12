# JT-1 썸네일(visual 2026-11-12 17시) — RT-1 make_rt1n.py 복사, 사진·문구만 바꿈(N-2 thumb_A 꼴, C-35 줄별 폭, 큰 글 아래 C-02).
#   문구 ep/JT-1/copy/titles.md '쓸 것' 썸네일 1위(B5 4차판) 그대로: 흰 줄 '주택연금 5억 집 · 65세 vs 70세 받은 돈 합' / 큰 흰 '93세 전엔 일찍 든 쪽이 더' / 큰 주황 '넘으면 기다린 쪽이 더' · 알약 없음(C-10)
#   사실 S1(5억·65세·70세)·calc §1(93.0세). 사진 Pexels(photo/sources.json) — 얼굴 없음(손·뒷모습)
import os, sys
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
O = os.path.dirname(os.path.abspath(__file__)); H = os.path.join(O, 'photo'); WORK = os.path.abspath(os.path.join(O, '..', '..', '..'))
FONT = os.path.join(WORK, 'fonts'); W, HH = 1920, 1080; X0 = 80; MAXW = 1760
ORANGE, WHITE, INK = (255, 90, 0), (255, 255, 255), (10, 11, 14)
BIG = ['93세 전엔 일찍 든 쪽이 더', '넘으면 기다린 쪽이 더']
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


def make(out, pic, ya, top, big=None, top_size=96, band=235, ls=1.10, target=0.90, xa=0.5, zoom=1.0, top_sizes=None, hmax=0.45, tshade=(300, 200), targets=None):
    BIG = big or globals()['BIG']
    im = photo(pic, y_anchor=ya, x_anchor=xa, zoom=zoom); d0 = ImageDraw.Draw(im)
    # C-35: 줄마다 크기 따로 — 폭 target에 맞춤. 짧은 첫 줄('서울 25개 구 중')이 커져 두 줄이 화면 45%(C-02)를 넘으면 둘을 같은 비율로 줄임
    sizes = [fit(d0, t, 320, 'black', maxw=int(W * tg)) for t, tg in zip(BIG, targets or [target] * len(BIG))]
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



T = '주택연금 5억 집 · 65세 vs 70세|받은 돈 합'
make('jt1_a.png', 'couple_autumn_back_14347362.jpg', 0.35, T, top_sizes=[120, 120], tshade=(440, 240))
make('jt1_b.png', 'hands_notebook_5756577.jpg', 0.3, T, top_sizes=[120, 120], tshade=(440, 240))
make('jt1_c.png', 'key_hand_8292791.jpg', 0.3, T, top_sizes=[120, 120], tshade=(440, 240))
make('jt1_d.png', 'hand_writing_8123908.jpg', 0.6, T, top_sizes=[120, 120], tshade=(440, 240))
# 2차(같은 회차): 흰 줄을 '무엇의 이야기'|'무엇을 비교' 두 줄로 끊음(1차는 '받은 돈 합'만 둘째 줄로 떨어짐) · c(빨간 손톱·열쇠 작음)·d(흐림) 뺌
T2 = '주택연금 5억 집|65세 vs 70세 받은 돈 합'
make('jt1_a2.png', 'couple_autumn_back_14347362.jpg', 0.30, T2, top_sizes=[120, 104], tshade=(440, 240))
make('jt1_b2.png', 'hands_notebook_5756577.jpg', 0.3, T2, top_sizes=[120, 104], tshade=(440, 240))
# 3차(같은 회차): a2·b2 짝 비교 1:1(순서 따라 이김) · 둘 다 경쟁 5장보다 어둡고 '집'이 안 보임 → 한국 동네·아파트가 보이는 밝은 벤치 뒷모습(Pexels 14618066)
make('jt1_e.png', 'couple_bench_korea_14618066.jpg', 0.25, T2, top_sizes=[120, 104], tshade=(400, 200), band=220)
# e는 터키 콘야 사진(머릿수건)이라 '우리 이야기'로 안 읽힘 → 안 씀. 4차: 아파트 앞면(집 = 담보, 경쟁 2·4번도 아파트) 밝은 사진
make('jt1_f.png', 'apt_facade_3736898.jpg', 0.3, T2, top_sizes=[120, 104], tshade=(400, 220), band=235)
# 5차(같은 회차): thumblen — 셋 다 둘째 줄 끝 '더'가 길이 칸에 걸림(1,298픽셀) → H-4 g5처럼 둘째 줄만 줄임(폭 90→80%)
for k, pic, ya, kw in (('a3', 'couple_autumn_back_14347362.jpg', 0.30, {}), ('b3', 'hands_notebook_5756577.jpg', 0.3, {}), ('f2', 'apt_facade_3736898.jpg', 0.3, {'tshade': (400, 220)})):
    make(f'jt1_{k}.png', pic, ya, T2, top_sizes=[120, 104], targets=[0.90, 0.80], **({'tshade': (440, 240)} | kw))
