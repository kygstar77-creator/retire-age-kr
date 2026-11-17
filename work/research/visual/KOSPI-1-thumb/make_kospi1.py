# KOSPI-1 썸네일(visual 2026-11-17 17시) — SQ-1 make_sq1.py 복사, 사진·문구만 바꿈(N-2 thumb_A 꼴, 큰 글 아래 C-02).
#   문구 research/copy/kospi1/titles.md 1위 TH2' 그대로: 흰 줄 '1995년부터 매일 마감 가격으로 셈' / 큰 흰 '코스피 하루 5% 하락' / 큰 주황 '올해만 23번 나왔다' · 알약 'IMF 외환위기 때 한 해 9번'(copywriter: 알약 크게)
#   사실 ep/KOSPI-1/calc2_out.txt: 2026 하루 종가 -5% 이하 23일(11/13까지) · 1997 9·1998 9. 사진 Pexels(photo/sources.json) — 얼굴 정면 없음
import os, sys
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
O = os.path.dirname(os.path.abspath(__file__)); H = os.path.join(O, 'photo'); WORK = os.path.abspath(os.path.join(O, '..', '..', '..'))
FONT = os.path.join(WORK, 'fonts'); W, HH = 1920, 1080; X0 = 80
ORANGE, WHITE, INK = (255, 90, 0), (255, 255, 255), (10, 11, 14)
BIG = ['코스피 하루 5% 하락', '올해만 23번 나왔다']
TOP = '1995년부터 매일 마감 가격으로 셈'
PILL = 'IMF 외환위기 때 한 해 9번'


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


def make(out, pic, ya, xa=0.5, zoom=1.0, band=235, tshade=(380, 210), targets=(0.86, 0.80), ls=1.10, hmax=0.45, top_size=104, sw=6, tsw=5, pk=1.15):
    im = photo(pic, y_anchor=ya, x_anchor=xa, zoom=zoom); d0 = ImageDraw.Draw(im)
    sizes = [fit(d0, t, 320, 'black', maxw=int(W * tg)) for t, tg in zip(BIG, targets)]
    hb = sum(int(s * ls) for s in sizes)
    if hb > HH * hmax: k = HH * hmax / hb; sizes = [int(s * k) for s in sizes]; hb = sum(int(s * ls) for s in sizes)
    y = HH - 30 - hb
    ts = fit(d0, TOP, top_size, '700', maxw=int(W * 0.88))
    im = shade(im, max(0, y - 160), HH, band); im = shade(im, 0, tshade[0], tshade[1], top=True); d = ImageDraw.Draw(im)
    ty = 36
    d.text((X0, ty), TOP, font=f(ts, '700'), fill=WHITE, stroke_width=tsw, stroke_fill=INK); ty += int(ts * 1.30)
    # 알약: 주황 바탕 흰 글 — 비교 숫자 'IMF 때 9번', copywriter 요청으로 흰 줄보다 크게
    ps = int(ts * pk); pf = f(ps, '700'); tw = d.textlength(PILL, font=pf); px, py = 28, 12
    d.rounded_rectangle((X0, ty, X0 + tw + 2 * px, ty + ps + 2 * py + 6), radius=(ps + 2 * py) // 2, fill=ORANGE)
    d.text((X0 + px, ty + py - int(ps * 0.08)), PILL, font=pf, fill=WHITE)
    widths = []
    for k, (t, s) in enumerate(zip(BIG, sizes)):
        bb = d.textbbox((X0, y - int(s * 0.12)), t, font=f(s, 'black'), stroke_width=sw); widths.append((bb[2] - bb[0]) / W)
        d.text((X0, y - int(s * 0.12)), t, font=f(s, 'black'), fill=WHITE if k == 0 else ORANGE, stroke_width=sw, stroke_fill=INK); y += int(s * ls)
    sm = im.resize((1280, 720), Image.LANCZOS); sm.save(os.path.join(O, out))
    for p in (412, 168): sm.resize((p, p * 9 // 16), Image.LANCZOS).save(os.path.join(O, out.replace('.png', f'_{p}.png')))
    print(out, f'흰 줄 {ts}px · 알약 {ps}px · 큰 글 {sizes}px · 줄별 폭 ' + '·'.join(f'{w:.0%}' for w in widths) + f' · 높이 {hb / HH:.0%}')


if __name__ == '__main__':
    make('k1_a.png', 'candle_down_35118208.jpg', 0.15, band=150, tshade=(400, 150), sw=13, tsw=8)
    make('k1_b.png', 'arrows_tablet_36633901.jpg', 0.0, band=170, tshade=(400, 150), sw=13, tsw=8)
    make('k1_c.png', 'hands_phone_32219704.jpg', 0.2, band=190, tshade=(400, 160), sw=13, tsw=8)
