# W-3 큰 글 자간 시험(visual 11/2 23시, today.md 47행 벤치마크 지시) — e3(make_w3n.py 끝 줄)과 사진·꼴·문구 그대로, 큰 글 자간만 -4%(글자 크기의 4%씩 좁힘).
#   좁힌 만큼 같은 폭 한계(1600px, C-15 길이 칸)에서 글자가 커진다. 지면 판(ep/W-3/thumb_w3n_e3.png)은 바꾸지 않음 — 결과는 judges.md 기록만.
import os, sys
from PIL import Image, ImageDraw
sys.stdout.reconfigure(encoding='utf-8')
sys.argv = sys.argv[:1]
import importlib.util
O = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(O, 'make_w3n.py'), encoding='utf-8').read().split("\n\n\n\nT = ")[0]   # 함수만 가져옴(끝의 make() 호출은 안 돌림)
g = {'__file__': os.path.join(O, 'make_w3n.py')}; exec(src, g)
f, photo, shade, W, HH, X0, MAXW = g['f'], g['photo'], g['shade'], g['W'], g['HH'], g['X0'], g['MAXW']
ORANGE, WHITE, INK = g['ORANGE'], g['WHITE'], g['INK']
TOP = '2026년부터 배당소득 분리과세'; BIG = ['1년 배당·이자 2천만까지', '넘는 사람만 세금 달라져요']

def tw(d, t, ft, tr):  # 자간 tr(글자 크기 비율) 넣은 줄 폭
    return sum(d.textlength(c, font=ft) for c in t) + tr * ft.size * (len(t) - 1)

def draw_tr(d, x, y, t, ft, tr, fill):
    for c in t:
        d.text((x, y), c, font=ft, fill=fill, stroke_width=6, stroke_fill=INK); x += d.textlength(c, font=ft) + tr * ft.size

def make(out, tr, ls=1.14, band=235, top_size=96, sx=1.0):
    im = photo('red_calc_receipts_7680748.jpg', y_anchor=0.2); d0 = ImageDraw.Draw(im)
    def fitw(t):
        s = 260
        while s > 40 and tw(d0, t, f(s, 'black'), tr) * sx > 1600: s -= 2
        return s
    bs = min(fitw(t) for t in BIG); hb = len(BIG) * int(bs * ls); y = HH - 40 - hb
    top_size = g['fit'](d0, TOP, top_size, '700')
    im = shade(im, max(0, y - 160), HH, band); im = shade(im, 0, 420, 215, top=True); d = ImageDraw.Draw(im)
    d.text((X0, 36), TOP, font=f(top_size, '700'), fill=WHITE, stroke_width=4, stroke_fill=INK)
    rows = []
    for k, t in enumerate(BIG):
        ft = f(bs, 'black'); yy = y - int(bs * 0.12)
        if sx == 1.0: draw_tr(d, X0, yy, t, ft, tr, WHITE if k == 0 else ORANGE)
        else:  # 가로 sx배: 글자 판을 따로 그려 가로만 줄여 붙임
            lw = int(tw(d0, t, ft, tr)) + 40; ly = Image.new('RGBA', (lw, int(bs * 1.6)), (0, 0, 0, 0)); dl = ImageDraw.Draw(ly)
            draw_tr(dl, 20 - 6, 0, t, ft, tr, (WHITE if k == 0 else ORANGE) + (255,))
            ly = ly.resize((round(lw * sx), ly.height), Image.LANCZOS); im.paste(ly, (X0 - round(14 * sx), yy), ly); d = ImageDraw.Draw(im)
        # 잉크 크기(1280×720 판 기준, 테두리 뺌): 폭 = 첫 글자 왼쪽~끝 글자 오른쪽, 높이 = 한글 글자 높이(bbox)
        l = ft.getbbox(t[0])[0]; r = tw(d0, t[:-1], ft, tr) + ft.getbbox(t[-1])[2]
        hs = sorted(ft.getbbox(c)[3] - ft.getbbox(c)[1] for c in t if '가' <= c <= '힣'); h = hs[len(hs) // 2]   # 한글 한 자 잉크 높이 가운데값
        rows.append((t, (r - l) * sx / W, h * 720 / HH)); y += int(bs * ls)
    sm = im.resize((1280, 720), Image.LANCZOS); sm.save(os.path.join(O, out))
    for px in (412, 168): sm.resize((px, px * 9 // 16), Image.LANCZOS).save(os.path.join(O, out.replace('.png', f'_{px}.png')))
    print(out, f'자간 {tr:+.0%} 가로 {sx:.0%} 큰 글 {bs}px(1080판)·두 줄 {hb / HH:.0%}')
    for t, wp, hp in rows: print(f'  {t}: 폭 {wp:.0%} · 글자 높이 {hp:.0f}px({hp / 720:.1%})')

make('w3n_e3_tr0.png', 0.0)    # e3 재현(측정용 — 자간 0이면 e3와 같은 크기여야 함)
make('w3n_e3t.png', -0.04)     # 자간 -4%
make('w3n_e3h.png', 0.0, sx=0.9)  # 가로 90%
