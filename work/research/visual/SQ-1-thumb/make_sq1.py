# SQ-1 썸네일(visual 2026-11-17) — H-5 make_h5.py 복사, 사진·문구만 바꿈(N-2 thumb_A 꼴, 큰 글 아래 C-02, 테두리판 o1 꼴 — 11/14 benchmark 지시).
#   문구 research/copy/sq1/final.txt 그대로(copywriter 11/16 18:55 요청): 흰 줄 '15년 전 1억 넣었다면' / 큰 흰 '나스닥100 13.6억' / 큰 주황 'SCHD 6.8억' · 알약 '달러 기준 · 2011년 10월~2026년 10월'
#   사실 ep/SQ-1/calc_krw_out_1116.txt 15년: 달러 1억 → SCHD 0% 13.56억 · SCHD 100% 6.77억(ECOS 20111031~20261030). 사진 Pexels(photo/sources.json) — 얼굴 없음(손만)
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.stdout.reconfigure(encoding='utf-8')
O = os.path.dirname(os.path.abspath(__file__)); H = os.path.join(O, 'photo'); WORK = os.path.abspath(os.path.join(O, '..', '..', '..'))
FONT = os.path.join(WORK, 'fonts'); W, HH = 1920, 1080; X0 = 80
ORANGE, WHITE, INK = (255, 90, 0), (255, 255, 255), (10, 11, 14)
BIG = ['나스닥100 13.6억', 'SCHD 6.8억']
TOP = '15년 전 1억원 넣었다면'   # 11/18 copywriter 1초 시험 반려: '달러 기준'을 '13.6억 달러'로 오해 → 알약 바꿈, '1억원'
PILL = '가장 크게 빠진 폭은 나스닥100이 더 컸다'   # 사실 ep/SQ-1/calc_mix_out_1112.txt 최대낙폭 SCHD 0% -32.6% vs 100% -21.5% · 권유 한 방향(3/3) 막기
# 기간·'달러로 넣고 배당 재투자·원화 환산'은 설명 첫 줄로(youtube-loop)


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


def make(out, pic, ya, xa=0.5, zoom=1.0, band=235, tshade=(380, 210), targets=(0.86, 0.80), ls=1.10, hmax=0.45, top_size=104, sw=6, tsw=5, blur=0, pk=0.80):
    im = photo(pic, y_anchor=ya, x_anchor=xa, zoom=zoom)
    if blur: im = im.filter(ImageFilter.GaussianBlur(blur))   # 11/18: 배경 모니터 숫자가 답 숫자와 섞여 읽힘 → 흐리게
    d0 = ImageDraw.Draw(im)
    sizes = [fit(d0, t, 320, 'black', maxw=int(W * tg)) for t, tg in zip(BIG, targets)]
    hb = sum(int(s * ls) for s in sizes)
    if hb > HH * hmax: k = HH * hmax / hb; sizes = [int(s * k) for s in sizes]; hb = sum(int(s * ls) for s in sizes)
    y = HH - 30 - hb
    ts = fit(d0, TOP, top_size, '700', maxw=int(W * 0.88))
    im = shade(im, max(0, y - 160), HH, band); im = shade(im, 0, tshade[0], tshade[1], top=True); d = ImageDraw.Draw(im)
    ty = 36
    d.text((X0, ty), TOP, font=f(ts, '700'), fill=WHITE, stroke_width=tsw, stroke_fill=INK); ty += int(ts * 1.30)
    # 알약: 주황 바탕 흰 글(답 숫자 아님 — 기준 시점 한 줄, copy v2)
    ps = fit(d0, PILL, int(ts * pk), '700', maxw=int(W * 0.84)); pf = f(ps, '700'); tw = d.textlength(PILL, font=pf); px, py = 28, 12
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
    # 11/17 시안 a·b·c(옛 알약 '달러 기준 · …') — 1안 sq1_c는 비교 기준으로 그대로 둠
    # make('sq1_a.png', 'chart_point_5833757.jpg', 0.2, band=0, tshade=(380, 120), sw=15, tsw=9)
    # make('sq1_b.png', 'laptop_chart_6172578.jpg', 0.3, band=0, tshade=(380, 120), sw=15, tsw=9)
    # make('sq1_c.png', 'chart_point_5833757.jpg', 0.2, band=150, tshade=(380, 120), sw=13, tsw=8)
    # 11/18 고친 판(copywriter 14:26): 새 알약·흰 줄 '1억원'·배경 흐리게 — d는 흐림 8, e는 흐림 14+알약 조금 크게
    make('sq1_d.png', 'chart_point_5833757.jpg', 0.2, band=150, tshade=(380, 120), sw=13, tsw=8, blur=8)
    make('sq1_e.png', 'chart_point_5833757.jpg', 0.2, band=170, tshade=(380, 140), sw=13, tsw=8, blur=14, pk=0.92)
