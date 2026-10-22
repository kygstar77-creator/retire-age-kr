# J-1 썸네일 새 꼴(visual 10/21 17시) — H-3 make_h3v.py 복사, 사진·문구만 바꿈. 문구는 ep/J-1/copy/titles.md 1위 그대로(copywriter):
#   흰 줄 '종부세 정부안 · 국회 심사 중' / 큰 흰 '공시 20억 한 채 보유세' / 큰 주황 '안 살면 140만원 넘게 늘어' / 알약 '2028년 기준'
#   숫자 facts C1·C2: 거주 0 618.9→759.8만(+140.9 → '140만원 넘게'). 사진 Pexels 31414676(Hyeok Jang, 한강 다리·아파트 저녁) · 38249703(Jueon Kim, 아파트 외벽) — 얼굴 없음
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
sys.stdout.reconfigure(encoding='utf-8')
O = os.path.dirname(os.path.abspath(__file__)); H = os.path.join(O, 'photo'); WORK = os.path.abspath(os.path.join(O, '..', '..', '..'))
FONT = os.path.join(WORK, 'fonts'); W, HH = 1920, 1080; X0 = 80; MAXW = 1760
ORANGE, WHITE, INK = (255, 90, 0), (255, 255, 255), (10, 11, 14)
BIG = ['공시 20억 한 채 보유세', '안 살면 140만원 넘게 늘어']
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
    while size > floor and d.textlength(t, font=f(size, w)) > maxw: size -= 4
    return size
def make(out, pic, ya, top, pill, top_size=88, pill_size=100, band=235, ls=1.14):
    im = photo(pic, y_anchor=ya); d0 = ImageDraw.Draw(im)
    bs = min(fit(d0, t, 200, 'black') for t in BIG); hb = len(BIG) * int(bs * ls); y = HH - 40 - hb
    top_size = fit(d0, top, top_size, '700')
    im = shade(im, max(0, y - 160), HH, band); im = shade(im, 0, 420, 215, top=True); d = ImageDraw.Draw(im)
    d.text((X0, 36), top, font=f(top_size, '700'), fill=WHITE, stroke_width=4, stroke_fill=INK)
    if pill:
        pill_size = fit(d0, pill, pill_size, '700', MAXW - 64)
        yy = 36 + top_size + 28; ft = f(pill_size, '700'); tw = d.textlength(pill, font=ft); ph = int(pill_size * 1.36)
        d.rounded_rectangle((X0, yy, X0 + tw + 64, yy + ph), 24, fill=ORANGE); d.text((X0 + 32, yy + ph // 2), pill, font=ft, fill=WHITE, anchor='lm')
    for k, t in enumerate(BIG):
        d.text((X0, y - int(bs * 0.12)), t, font=f(bs, 'black'), fill=WHITE if k == 0 else ORANGE, stroke_width=6, stroke_fill=INK); y += int(bs * ls)
    sm = im.resize((1280, 720), Image.LANCZOS); sm.save(os.path.join(O, out))
    for px in (412, 168): sm.resize((px, px * 9 // 16), Image.LANCZOS).save(os.path.join(O, out.replace('.png', f'_{px}.png')))
    print(out, top_size, pill_size if pill else '-')



T, P = '종부세 정부안 · 국회 심사 중', '2028년 기준'
if len(sys.argv) == 1: make('j1n_a.png', 'apartment_building_evening_seoul_1_31414676.jpg', 0.0, T, P, top_size=120, pill_size=120)
if len(sys.argv) == 1: make('j1n_b.png', 'korean_apartment_complex_3_38249703.jpg', 0.3, T, P, top_size=120, pill_size=120)

# 2차(visual 10/22 17시) — copywriter 10/21 18:54 문구 2차 1위 그대로, 사진은 1차 추천 b와 같은 것
if len(sys.argv) > 1 and sys.argv[1] == 'c':
    BIG[:] = ['공시가격 20억 보유세', '거주 안 하면 140만원 늘어']
    make('j1n_c.png', 'korean_apartment_complex_3_38249703.jpg', 0.3, '종부세 정부안 · 국회 심사 중 · 집 한 채', '2028년 한 해', top_size=120, pill_size=120)
