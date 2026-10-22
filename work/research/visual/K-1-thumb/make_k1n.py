# K-1 썸네일(visual 10/22 09시) — J-1 make_j1n.py 복사, 사진·문구만 바꿈. 문구는 ep/K-1/copy/titles.md 1위 그대로(copywriter 10/21 18:56):
#   흰 줄 '1년 정기예금 · 작년 8월 vs 올해 8월 · 세금 뗀 이자' / 큰 흰 '정기예금 1억 이자' / 큰 주황 '작년 금리보다 74만원 더' / 알약 없음(C-10)
#   숫자 facts F3 2.51%→3.39% · F4 세후 2,123,460→2,867,940원 차 744,480원. 사진 Pexels 18804128(은행 창구 손·달러 — 제목 '미국'과 이어짐, 50세 지적)·36021649(장부·펜·지폐) — 얼굴 없음
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
sys.stdout.reconfigure(encoding='utf-8')
O = os.path.dirname(os.path.abspath(__file__)); H = os.path.join(O, 'photo'); WORK = os.path.abspath(os.path.join(O, '..', '..', '..'))
FONT = os.path.join(WORK, 'fonts'); W, HH = 1920, 1080; X0 = 80; MAXW = 1760
ORANGE, WHITE, INK = (255, 90, 0), (255, 255, 255), (10, 11, 14)
BIG = ['정기예금 1억 이자', '작년 금리보다 74만원 더']
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
    top_size = min(fit(d0, tl, top_size, '700') for tl in top.split('|'))
    im = shade(im, max(0, y - 160), HH, band); im = shade(im, 0, 420, 215, top=True); d = ImageDraw.Draw(im)
    for i, tl in enumerate(top.split('|')):
        d.text((X0, 36 + i * int(top_size * 1.18)), tl, font=f(top_size, '700'), fill=WHITE, stroke_width=4, stroke_fill=INK)
    if pill:
        pill_size = fit(d0, pill, pill_size, '700', MAXW - 64)
        yy = 36 + top_size + 28; ft = f(pill_size, '700'); tw = d.textlength(pill, font=ft); ph = int(pill_size * 1.36)
        d.rounded_rectangle((X0, yy, X0 + tw + 64, yy + ph), 24, fill=ORANGE); d.text((X0 + 32, yy + ph // 2), pill, font=ft, fill=WHITE, anchor='lm')
    for k, t in enumerate(BIG):
        d.text((X0, y - int(bs * 0.12)), t, font=f(bs, 'black'), fill=WHITE if k == 0 else ORANGE, stroke_width=6, stroke_fill=INK); y += int(bs * ls)
    sm = im.resize((1280, 720), Image.LANCZOS); sm.save(os.path.join(O, out))
    for px in (412, 168): sm.resize((px, px * 9 // 16), Image.LANCZOS).save(os.path.join(O, out.replace('.png', f'_{px}.png')))
    print(out, top_size, f'큰 글 {bs}px·{hb / HH:.0%}')


T = '1년 정기예금 · 작년 8월 vs 올해 8월 · 세금 뗀 이자'
make('k1n_a.png', 'bank_counter_hands_money_1_18804128.jpg', 0.0, T, None, top_size=96)
make('k1n_b.png', 'savings_account_book_3_36021649.jpg', 0.2, T, None, top_size=96)
# 10/22 2차: 1차 40·50·60세 3/3 '168px에서 흰 줄 안 읽힘' → 같은 낱말을 두 줄로 나눠 키움(새 말 없음)
make('k1n_c.png', 'bank_counter_hands_money_1_18804128.jpg', 0.0, '1년 정기예금 · 세금 뗀 이자|작년 8월 vs 올해 8월', None, top_size=124)
