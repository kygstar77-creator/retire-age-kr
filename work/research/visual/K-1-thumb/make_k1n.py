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
# 10/27 3차: copywriter 2차 문구(ep/K-1/copy/titles.md '썸네일 문구 2차') — 큰 주황만 '작년보다 올해 74만원 더'(40세 방향 오독 고침), '미국'은 안 넣음(인과 오독 3/3)
BIG[1] = '작년보다 올해 74만원 더'
make('k1n_d.png', 'bank_counter_hands_money_1_18804128.jpg', 0.0, '1년 정기예금 · 세금 뗀 이자|작년 8월 vs 올해 8월', None, top_size=124)
make('k1n_e.png', 'bank_counter_hands_money_1_18804128.jpg', 0.0, T, None, top_size=96)
# 11/3 4차: youtube-loop 08:54 한은 9월분 반영 — 글자 두 곳만(facts F4 1억 세후 2,148,840→3,020,220원, 차 871,380원), 사진·꼴 d 그대로
BIG[1] = '작년보다 올해 87만원 더'
make('k1n_f.png', 'bank_counter_hands_money_1_18804128.jpg', 0.0, '1년 정기예금 · 세금 뗀 이자|작년 9월 vs 올해 9월', None, top_size=124)
# 11/3 레드팀 '달러 지폐가 원화 예금과 무관' → b 사진(장부·펜·지폐)으로 같은 글자 g, f와 짝 비교
make('k1n_g.png', 'savings_account_book_3_36021649.jpg', 0.2, '1년 정기예금 · 세금 뗀 이자|작년 9월 vs 올해 9월', None, top_size=124)
# 11/9 22시 PD(audit 21:05·회의 21:41): f의 주황 줄 끝 '더'가 앱 길이 칸(가로 89.3%부터)에 반쯤 가림 → 글자·사진·꼴 f 그대로,
#   주황 줄만 따로 줄여 폭 85%대(C-35 85~95%)·끝 89% 앞(C-15). 흰 큰 줄은 f와 같은 크기. 큰 두 줄 왼쪽 80→64px(폭 85%와 끝 89%를 함께 지키려고)
def make_h(out, pic, ya, top, top_size=124, band=235, ls=1.14, x0=64, end=0.885):
    im = photo(pic, y_anchor=ya); d0 = ImageDraw.Draw(im)
    bs = min(fit(d0, t, 200, 'black') for t in BIG)                       # f와 같은 흰 줄 크기
    bo = fit(d0, BIG[1], bs, 'black', maxw=int(W * end) - x0 - 6, floor=40)  # 주황 줄만 줄임(테두리 6px 포함 끝 88.5%)
    hb = int(bs * ls) + int(bo * ls); y = HH - 40 - hb
    top_size = min(fit(d0, tl, top_size, '700') for tl in top.split('|'))
    im = shade(im, max(0, y - 160), HH, band); im = shade(im, 0, 420, 215, top=True); d = ImageDraw.Draw(im)
    for i, tl in enumerate(top.split('|')):
        d.text((X0, 36 + i * int(top_size * 1.18)), tl, font=f(top_size, '700'), fill=WHITE, stroke_width=4, stroke_fill=INK)
    for k, (t, s) in enumerate(zip(BIG, (bs, bo))):
        d.text((x0, y - int(s * 0.12)), t, font=f(s, 'black'), fill=WHITE if k == 0 else ORANGE, stroke_width=6, stroke_fill=INK)
        bb = d.textbbox((x0, y - int(s * 0.12)), t, font=f(s, 'black'), stroke_width=6); print(t, f'{s}px 폭 {(bb[2]-bb[0])/W:.1%} 끝 {bb[2]/W:.1%}')
        y += int(s * ls)
    sm = im.resize((1280, 720), Image.LANCZOS); sm.save(os.path.join(O, out))
    for px in (412, 168): sm.resize((px, px * 9 // 16), Image.LANCZOS).save(os.path.join(O, out.replace('.png', f'_{px}.png')))
    print(out, f'큰 글 {bs}/{bo}px·{hb / HH:.0%}')
if __name__ == '__main__' and 'h' in sys.argv[1:]:
    make_h('k1n_h.png', 'bank_counter_hands_money_1_18804128.jpg', 0.0, '1년 정기예금 · 세금 뗀 이자|작년 9월 vs 올해 9월')
