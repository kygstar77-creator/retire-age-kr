# H-4 썸네일(visual 11/2 09시) — S-1 make_s1n.py 복사, 사진·문구만 바꿈(C-35 줄별 폭 85~95%, 큰 글 높이 45% 넘으면 줄임 C-02).
#   문구 ep/H-4/copy/titles.md '10/29 고친 판' 그대로: 흰 줄 '광명 아파트 15억이라던데, 실거래 전부 세어 보니' / 큰 흰 '서울 25개 구 중' / 큰 주황 '17곳이 광명보다 비쌌다' · 알약 없음
#   사실 facts [2] 광명 9.70억 26곳 중 18번째 → 위 17곳 모두 서울 구 · [5] 2019년 뒤 단지 14.71억(15억). 사진 Pexels 19848427·18705526·27976252 — 아파트 단지 원경, 사람 없음, photo/sources.json
import os, sys
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
O = os.path.dirname(os.path.abspath(__file__)); H = os.path.join(O, 'photo'); WORK = os.path.abspath(os.path.join(O, '..', '..', '..', '..'))
FONT = os.path.join(WORK, 'fonts'); W, HH = 1920, 1080; X0 = 80; MAXW = 1760
ORANGE, WHITE, INK = (255, 90, 0), (255, 255, 255), (10, 11, 14)
BIG = ['서울 25개 구 중', '17곳이 광명보다 비쌌다']
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
T2 = '광명 아파트 15억이라던데,|실거래 전부 세어 보니'   # S-1 d 교훈: 168px에서 주제 낱말('광명 아파트')이 읽히게 앞 조각을 크게
make('h4n_a.png', 'haze_aerial_19848427.jpg', 0.15, T)
make('h4n_b.png', 'night_reflect_18705526.jpg', 0.3, T)
make('h4n_c.png', 'river_towers_27976252.jpg', 0.2, T)
make('h4n_d.png', 'night_reflect_18705526.jpg', 0.3, T2, top_sizes=[130, 84])
make('h4n_e.png', 'river_towers_27976252.jpg', 0.2, T2, top_sizes=[130, 84])
# 11/2 레드팀 '고쳐서': 김포 사진(b) 위 '광명 아파트' = 광명으로 오해 → 광명 실물(Wikimedia Commons Apartmentgwangmyeong.jpg, Kimhs5400, CC BY 4.0 — 설명란 출처 표기)
make('h4n_f.png', 'gm_complex_wm.jpg', 0.45, T)
make('h4n_g.png', 'gm_complex_wm.jpg', 0.45, T2, top_sizes=[130, 84])
# h: g와 같은 꼴, 사진만 dusk.py(어둡게·푸르게) — 짝 비교 b>g 이유 '야간이라 대비·주목도'
make('h4n_h.png', 'gm_complex_wm_dusk.jpg', 0.45, T2, top_sizes=[130, 84])
# g2: 1초 시험(새 Agent·제미나이) '실거래 전부 세어 보니'가 회색 하늘 위에서 안 읽힘 → 위 그라데이션만 진하게(300px·200 → 420px·240)
make('h4n_g2.png', 'gm_complex_wm.jpg', 0.45, T2, top_sizes=[130, 84], tshade=(420, 240))
# 11/2 17시 copywriter '11/2 레드팀 지적 반영'(titles.md): 흰 줄 '전부' 뺌 → g와 같은 사진·꼴·큰 글, 흰 줄만 → g3
make('h4n_g3.png', 'gm_complex_wm.jpg', 0.45, '광명 아파트 15억이라던데,|실거래 세어 보니', top_sizes=[130, 84])
# g4: 흰 둘째 줄이 짧아졌으니(13→9자) 84→112px — g 1초 시험 약점 '168px 위 두 줄 안 읽힘'
make('h4n_g4.png', 'gm_complex_wm.jpg', 0.45, '광명 아파트 15억이라던데,|실거래 세어 보니', top_sizes=[130, 112])
