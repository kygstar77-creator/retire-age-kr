# P-3 썸네일(visual 10/27 17시) — K-1 make_k1n.py 복사, 사진·문구만 바꿈. 문구는 ep/P-3/copy/titles.md '2차 고친 판'(copywriter 10/27 00:38) 그대로:
#   흰 줄 '건강보험 피부양자 · 국민연금만 받을 때' / 큰 흰 '국민연금 월 166만원' / 큰 주황 '넘으면 피부양자 빠져요' / 알약 '재산 없으면 건보료 월 6만 8천원'
#   숫자 calc_out 167만원 행 67,926원(약 6만 8천원)·연 2천만원 문턱(월 1,666,666원). 사진 Pexels 618158(노인 손 서명)·29765568(서류 쓰는 손) — 얼굴 없음, photo/sources.json
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
sys.stdout.reconfigure(encoding='utf-8')
O = os.path.dirname(os.path.abspath(__file__)); H = os.path.join(O, 'photo'); WORK = os.path.abspath(os.path.join(O, '..', '..', '..'))
FONT = os.path.join(WORK, 'fonts'); W, HH = 1920, 1080; X0 = 80; MAXW = 1760
ORANGE, WHITE, INK = (255, 90, 0), (255, 255, 255), (10, 11, 14)
BIG = ['국민연금 월 166만원', '넘으면 피부양자 빠져요']
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


T = '건강보험 피부양자 · 국민연금만 받을 때'
P = '재산 없으면 건보료 월 6만 8천원'
make('p3n_a.png', 'senior_hands_signing_618158.jpg', 0.15, T, P, top_size=96)
make('p3n_b.png', 'hands_official_form_29765568.jpg', 0.25, T, P, top_size=96)
# c: a 사진에 흰 줄을 두 줄로 나눠 키움(K-1 1차 '168px 흰 줄 안 읽힘' 교훈, 새 말 없음)
make('p3n_c.png', 'senior_hands_signing_618158.jpg', 0.15, '건강보험 피부양자|국민연금만 받을 때', P, top_size=124)
# 10/27 2차: 이해 1차(40·50·60) '6만 8천원이 누구 돈인지' 3/3·168px 알약 안 읽힘 3/3·50세 '제목 "얼마 낼까" 답을 썸네일이 먼저 줌' → 알약 뺌(C-10, 새 말 없음)
make('p3n_d.png', 'senior_hands_signing_618158.jpg', 0.15, T, None, top_size=96)
