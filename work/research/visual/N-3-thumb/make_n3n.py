# N-3 썸네일(visual 10/28 17시) — P-3 make_p3n.py 복사, 사진·문구만 바꾸고 큰 글은 줄마다 크기를 따로(C-35 — 각 줄 화면 폭 85~95%, 남 15/16).
#   문구 ep/N-3/copy/titles.md '10/28 고친 판' 그대로: 흰 줄 '2024년 국세청 직장인 전체 연봉 순위' / 큰 흰 '연봉 5천은 100명 중' / 큰 주황 '위에서 33명 안에' · 알약 없음
#   숫자 낭독 say_v1 31줄 '백 명 중 앞에서 서른세 명 안'과 같음. 사진 Pexels 16456831(횡단보도 위에서 본 사람들)·31863763(정장 두 사람 뒷모습) — 얼굴 없음, photo/sources.json
import os, sys
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
O = os.path.dirname(os.path.abspath(__file__)); H = os.path.join(O, 'photo'); WORK = os.path.abspath(os.path.join(O, '..', '..', '..'))
FONT = os.path.join(WORK, 'fonts'); W, HH = 1920, 1080; X0 = 80; MAXW = 1760
ORANGE, WHITE, INK = (255, 90, 0), (255, 255, 255), (10, 11, 14)
BIG = ['연봉 5천은 100명 중', '위에서 33명 안에']
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
def make(out, pic, ya, top, top_size=96, band=235, ls=1.10, target=0.90, xa=0.5, zoom=1.0):
    im = photo(pic, y_anchor=ya, x_anchor=xa, zoom=zoom); d0 = ImageDraw.Draw(im)
    # C-35: 줄마다 크기 따로 — 폭 target(85~95%)에 맞춤. 둘째 줄 끝은 x 1808(1280판 1205)라 길이 칸(약 1215~)에 안 걸림(C-15)
    sizes = [fit(d0, t, 320, 'black', maxw=int(W * target)) for t in BIG]
    hb = sum(int(s * ls) for s in sizes); y = HH - 30 - hb
    top_size = min(fit(d0, tl, top_size, '700') for tl in top.split('|'))
    im = shade(im, max(0, y - 160), HH, band); im = shade(im, 0, 300, 200, top=True); d = ImageDraw.Draw(im)
    for i, tl in enumerate(top.split('|')):
        d.text((X0, 36 + i * int(top_size * 1.18)), tl, font=f(top_size, '700'), fill=WHITE, stroke_width=4, stroke_fill=INK)
    widths = []
    for k, (t, s) in enumerate(zip(BIG, sizes)):
        bb = d.textbbox((X0, y - int(s * 0.12)), t, font=f(s, 'black'), stroke_width=6); widths.append((bb[2] - bb[0]) / W)
        d.text((X0, y - int(s * 0.12)), t, font=f(s, 'black'), fill=WHITE if k == 0 else ORANGE, stroke_width=6, stroke_fill=INK); y += int(s * ls)
    sm = im.resize((1280, 720), Image.LANCZOS); sm.save(os.path.join(O, out))
    for px in (412, 168): sm.resize((px, px * 9 // 16), Image.LANCZOS).save(os.path.join(O, out.replace('.png', f'_{px}.png')))
    print(out, f'흰 줄 {top_size}px · 큰 글 {sizes}px · 줄별 폭 ' + '·'.join(f'{w:.0%}' for w in widths) + f' · 높이 {hb / HH:.0%}')


T = '2024년 국세청 직장인 전체 연봉 순위'
make('n3n_a.png', 'crowd_crossing_aerial_16456831.jpg', 0.0, T)
make('n3n_b.png', 'two_suits_back_31863763.jpg', 0.35, T)
# c: a 사진을 1.35배 당겨 아래·왼쪽으로 — 건너는 사람들을 위쪽 절반에(C-03), 오른쪽 '東京駅南口' 표지판(외국 장소 단서)은 화면 밖으로
make('n3n_c.png', 'crowd_crossing_aerial_16456831.jpg', 0.9, T, xa=0.35, zoom=1.35)
# d(10/29 visual): c가 제미나이 'AI 사진 티' 4/4·일본 교차로(레드팀) → 한국 거리 실사 Pexels 19271600(비 오는 서울 남대문로 횡단보도, 우산 든 사람들 작게·얼굴 없음, original)
make('n3n_d.png', 'seoul_crosswalk_backs_19271600.jpg', 0.55, T)
