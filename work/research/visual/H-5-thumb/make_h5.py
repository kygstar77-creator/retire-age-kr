# H-5 썸네일(visual 2026-11-13 17시) — JT-1 make_jt1.py 복사, 사진·문구만 바꿈 + 알약 하나(N-2 thumb_A 꼴, 큰 글 아래 C-02, 줄별 폭 C-35).
#   문구 ep/H-5/copy/titles.md v2 '썸네일 문구' 그대로: 흰 줄 '송도 84㎡ 전체 거래 중간 가격' / 큰 흰 '고점 때 9억이던 값' / 큰 주황 '지금 7억 3,500만원' · 알약 '2021년 고점 기준'
#   사실 calc2_out §1(고점 1년 중앙 9.00억 → 최근 2026.07~10 중앙 7.35억 = 82%), script 19·87행 자막. 사진 Pexels(photo/sources.json) — 얼굴 없음, 설명에 Incheon/Songdo 적힌 것만
import os, sys
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
O = os.path.dirname(os.path.abspath(__file__)); H = os.path.join(O, 'photo'); WORK = os.path.abspath(os.path.join(O, '..', '..', '..'))
FONT = os.path.join(WORK, 'fonts'); W, HH = 1920, 1080; X0 = 80
ORANGE, WHITE, INK = (255, 90, 0), (255, 255, 255), (10, 11, 14)
BIG = ['고점 때 9억이던 값', '지금 7억 3,500만원']
TOP = '송도 84㎡ 전체 거래 중간 가격'
PILL = '2021년 고점 기준'


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


def fit(d, t, size, w, maxw, floor=40):
    while size > floor and d.textlength(t, font=f(size, w)) > maxw: size -= 2
    return size


def make(out, pic, ya, xa=0.5, zoom=1.0, band=235, tshade=(380, 210), targets=(0.86, 0.80), ls=1.10, hmax=0.45, top_size=104):
    im = photo(pic, y_anchor=ya, x_anchor=xa, zoom=zoom); d0 = ImageDraw.Draw(im)
    sizes = [fit(d0, t, 320, 'black', maxw=int(W * tg)) for t, tg in zip(BIG, targets)]
    hb = sum(int(s * ls) for s in sizes)
    if hb > HH * hmax: k = HH * hmax / hb; sizes = [int(s * k) for s in sizes]; hb = sum(int(s * ls) for s in sizes)
    y = HH - 30 - hb
    ts = fit(d0, TOP, top_size, '700', maxw=int(W * 0.88))
    im = shade(im, max(0, y - 160), HH, band); im = shade(im, 0, tshade[0], tshade[1], top=True); d = ImageDraw.Draw(im)
    ty = 36
    d.text((X0, ty), TOP, font=f(ts, '700'), fill=WHITE, stroke_width=5, stroke_fill=INK); ty += int(ts * 1.30)
    # 알약: 주황 바탕 흰 글(답 숫자 아님 — 기준 시점 한 줄, copy v2)
    ps = int(ts * 0.80); pf = f(ps, '700'); tw = d.textlength(PILL, font=pf); px, py = 28, 12
    d.rounded_rectangle((X0, ty, X0 + tw + 2 * px, ty + ps + 2 * py + 6), radius=(ps + 2 * py) // 2, fill=ORANGE)
    d.text((X0 + px, ty + py - int(ps * 0.08)), PILL, font=pf, fill=WHITE)
    widths = []
    for k, (t, s) in enumerate(zip(BIG, sizes)):
        bb = d.textbbox((X0, y - int(s * 0.12)), t, font=f(s, 'black'), stroke_width=6); widths.append((bb[2] - bb[0]) / W)
        d.text((X0, y - int(s * 0.12)), t, font=f(s, 'black'), fill=WHITE if k == 0 else ORANGE, stroke_width=6, stroke_fill=INK); y += int(s * ls)
    sm = im.resize((1280, 720), Image.LANCZOS); sm.save(os.path.join(O, out))
    for p in (412, 168): sm.resize((p, p * 9 // 16), Image.LANCZOS).save(os.path.join(O, out.replace('.png', f'_{p}.png')))
    print(out, f'흰 줄 {ts}px · 알약 {ps}px · 큰 글 {sizes}px · 줄별 폭 ' + '·'.join(f'{w:.0%}' for w in widths) + f' · 높이 {hb / HH:.0%}')


if __name__ == '__main__':
    make('h5_a.png', 'songdo_park_canal_18495181.jpg', 0.25)
    make('h5_b.png', 'songdo_canal_dusk_37736994.jpg', 0.35)
    make('h5_c.png', 'songdo_towers_918291.jpg', 0.3)
