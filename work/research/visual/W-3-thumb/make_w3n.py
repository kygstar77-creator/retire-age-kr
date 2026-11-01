# W-3 썸네일(visual 11/1 17시 회차, 18:56 늦게 돎) — P-3 make_p3n.py 복사, 사진·문구만 바꿈. 문구는 ep/W-3/copy/titles.md 1위 짝(copywriter 10/20·10/23) 그대로:
#   흰 줄 '삼성전자 배당금 · 배당소득 분리과세' / 큰 흰 '배당 500만원 받는데' / 큰 주황 '세금은 그대로였다' / 알약 없음(C-10)
#   숫자 facts [C1] 배당 500만원: 지금 15.4% 77만원 = 분리과세 첫 칸 14%+1.4% 77만원. 사진 Pexels 8296977·33175646·7680748 — 얼굴 없음, photo/sources.json
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
sys.stdout.reconfigure(encoding='utf-8')
O = os.path.dirname(os.path.abspath(__file__)); H = os.path.join(O, 'photo'); WORK = os.path.abspath(os.path.join(O, '..', '..', '..'))
FONT = os.path.join(WORK, 'fonts'); W, HH = 1920, 1080; X0 = 80; MAXW = 1760
ORANGE, WHITE, INK = (255, 90, 0), (255, 255, 255), (10, 11, 14)
BIG = ['배당 500만원 받는데', '세금은 그대로였다']
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
def make(out, pic, ya, top, pill, top_size=88, pill_size=100, band=235, ls=1.14, big=None):
    BIG = big or globals()['BIG']
    im = photo(pic, y_anchor=ya); d0 = ImageDraw.Draw(im)
    # 큰 글은 x 1680(1280판 1120)에서 끝냄 — 오른쪽 아래 길이 칸에 '요'·숫자가 안 걸리게(C-15, 10/27 감사 H-3 '억' 가림)
    bs = min(fit(d0, t, 200, 'black', maxw=1600) for t in BIG); hb = len(BIG) * int(bs * ls); y = HH - 40 - hb
    top_size = min(fit(d0, tl, top_size, '700') for tl in top.split('|'))
    im = shade(im, max(0, y - 160), HH, band); im = shade(im, 0, 420, 215, top=True); d = ImageDraw.Draw(im)
    for i, tl in enumerate(top.split('|')):
        d.text((X0, 36 + i * int(top_size * 1.18)), tl, font=f(top_size, '700'), fill=WHITE, stroke_width=4, stroke_fill=INK)
    if pill:
        pill_size = fit(d0, pill, pill_size, '700', MAXW - 64)
        yy = 36 + len(top.split('|')) * int(top_size * 1.18) + 10; ft = f(pill_size, '700'); tw = d.textlength(pill, font=ft); ph = int(pill_size * 1.36)
        d.rounded_rectangle((X0, yy, X0 + tw + 64, yy + ph), 24, fill=ORANGE); d.text((X0 + 32, yy + ph // 2), pill, font=ft, fill=WHITE, anchor='lm')
    for k, t in enumerate(BIG):
        d.text((X0, y - int(bs * 0.12)), t, font=f(bs, 'black'), fill=WHITE if k == 0 else ORANGE, stroke_width=6, stroke_fill=INK); y += int(bs * ls)
    sm = im.resize((1280, 720), Image.LANCZOS); sm.save(os.path.join(O, out))
    for px in (412, 168): sm.resize((px, px * 9 // 16), Image.LANCZOS).save(os.path.join(O, out.replace('.png', f'_{px}.png')))
    print(out, top_size, f'큰 글 {bs}px·{hb / HH:.0%}')



T = '삼성전자 배당금 · 배당소득 분리과세'
make('w3n_a.png', 'calc_signing_8296977.jpg', 0.2, T, None, top_size=96)
make('w3n_b.png', 'wallet_cash_33175646.jpg', 0.3, T, None, top_size=96)
make('w3n_c.png', 'red_calc_receipts_7680748.jpg', 0.2, T, None, top_size=96)
# 11/1 1차 이해(40·50·60): 주제 3/3, 걸림 '그대로였다'가 좋은 뜻(안 올랐다)·나쁜 뜻(안 줄었다)인지 3/3 · '500만원' 1년치인지 2/3
#   → d: 큰 글 '1년에 배당 500만원' / '세금은 안 줄었다'(facts [C1] 77만원=77만원, 제목 '줄어드는 사람'과 같은 낱말) — 합 16자
make('w3n_d.png', 'red_calc_receipts_7680748.jpg', 0.2, T, None, top_size=96, big=['1년에 배당 500만원', '세금은 안 줄었다'])
# 11/1 19:1x copywriter '11/1 고친 판'(titles.md 41행, 40·50·60 6차 통과) 나옴 → a~d(옛 문구) 버리고 새 문구로 e·f
T2 = '올해 생긴 배당소득 분리과세'
B2 = ['배당·이자 2천만까지 그대로', '넘는 사람만 세금 달라져요']
make('w3n_e.png', 'red_calc_receipts_7680748.jpg', 0.2, T2, None, top_size=96, big=B2)
make('w3n_f.png', 'calc_signing_8296977.jpg', 0.2, T2, None, top_size=96, big=B2)
