# CC-1 커버드콜 썸네일 시안(visual 2026-11-23 09시) — H-6 make_h6.py 복사(N-2 thumb_A 꼴, 큰 글 아래 40~45% C-02), 사진·문구만 바꿈. 트랙:A
#   문구 research/copy/cc1/titles.md 07:53 그대로: 흰 줄 '배당 ETF 1억씩, 1년 뒤 남은 돈' / 큰 흰 '커버드콜 9,654만원' / 큰 주황 '일반형 1억 1,793만원' · 알약 없음
#   사실 ep/CC-1/facts_1122.md 19행(최근 1년 2025-11-20→2026-11-20, 분배금 15.4% 뗌): 커버드콜 9,654만 · 일반형 1억 1,793만
#   사진 Pexels(photo/sources.json) — 손·달러만, 얼굴 없음, 하락 몸짓 사람 없음(KOSPI-1 교훈)
import os, sys, json
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
O = os.path.dirname(os.path.abspath(__file__)); H = os.path.join(O, 'photo'); WORK = os.path.abspath(os.path.join(O, '..', '..', '..'))
FONT = os.path.join(WORK, 'fonts'); W, HH = 1920, 1080; X0 = 80
ORANGE, WHITE, INK = (255, 90, 0), (255, 255, 255), (10, 11, 14)
BIG = ['커버드콜 9,654만원', '일반형 1억 1,793만원']
TOP = '배당 ETF 1억씩, 1년 뒤 남은 돈'
PILL = None
assert sum(len(t.replace(' ', '')) for t in BIG) <= 24 and all(len(t.replace(' ', '')) <= 12 for t in BIG)
fx = open(os.path.join(WORK, 'research', 'longform', 'ep', 'CC-1', 'facts_1122.md'), encoding='utf-8').read()
assert '**9,654만**' in fx and '**1억 1,793만**' in fx


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
    if PILL:
        ps = int(ts * pk); pf = f(ps, '700'); tw = d.textlength(PILL, font=pf); px, py = 28, 12
        d.rounded_rectangle((X0, ty, X0 + tw + 2 * px, ty + ps + 2 * py + 6), radius=(ps + 2 * py) // 2, fill=ORANGE)
        d.text((X0 + px, ty + py - int(ps * 0.08)), PILL, font=pf, fill=WHITE)
    else: ps = 0
    widths = []
    for k, (t, s) in enumerate(zip(BIG, sizes)):
        bb = d.textbbox((X0, y - int(s * 0.12)), t, font=f(s, 'black'), stroke_width=sw); widths.append((bb[2] - bb[0]) / W)
        d.text((X0, y - int(s * 0.12)), t, font=f(s, 'black'), fill=WHITE if k == 0 else ORANGE, stroke_width=sw, stroke_fill=INK); y += int(s * ls)
    sm = im.resize((1280, 720), Image.LANCZOS); sm.save(os.path.join(O, out))
    for p in (412, 168): sm.resize((p, p * 9 // 16), Image.LANCZOS).save(os.path.join(O, out.replace('.png', f'_{p}.png')))
    print(out, f'흰 줄 {ts}px · 알약 {ps}px · 큰 글 {sizes}px · 줄별 폭 ' + '·'.join(f'{w:.0%}' for w in widths) + f' · 높이 {hb / HH:.0%}')




if __name__ == '__main__':
    kw = dict(band=190, tshade=(330, 160), sw=13, tsw=8)
    make('cc1_a.png', 'p_4475469.jpg', 0.25, **kw)   # 어두운 탁자 위 달러 세는 손
    make('cc1_b.png', 'p_6693632.jpg', 0.3, **kw)    # 서류 위 달러 세는 손
    make('cc1_c.png', 'p_6328948.jpg', 0.3, **kw)    # 나무 탁자 위 달러 세기
