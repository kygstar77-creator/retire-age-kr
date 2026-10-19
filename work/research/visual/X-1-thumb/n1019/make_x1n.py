# X-1 새 썸네일(10/19 썸네일 꼴 규칙: N-2 thumb_A 꼴 + 큰 글 두 줄 아래 40~45%, textpos-1019).
#   부품·글꼴·색은 visual/textpos-1019/make_h2tp.py와 같다(작은 흰 줄·주황 알약 왼쪽 위, 큰 두 줄 아래 — 첫 줄 흰, 둘째 줄 주황).
#   문구는 ep/X-1/meta.json thumb_text·thumb_text_small(copywriter 10/19) 그대로 나눠 담음. 새 말 없음.
#   숫자: calc_out.txt 12행 2025-10-13 SPY 원화 +9.69%(→+10%) · 16행 2026-07-02 SPY 원화 −10.76%(→−11%).
#   사진: Pexels 영상 4275306(Saif Abdulraheem, 손에 든 100달러 다발, 얼굴 없음) 6초 프레임 · 5466779(olia danilevich, 위에서 본 달러 세기) 2초 프레임.
#   py -3.12 make_x1n.py → ep/X-1/thumb_x1n_a.png, _b.png, _c.png (1280×720). meta.json·유튜브는 건드리지 않는다.
import os, sys, json
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(os.path.join(H, '..', '..', '..', '..'))
FONT = os.path.join(WORK, 'fonts'); FR = os.path.join(H, 'frames')
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'X-1')
W, HH = 1920, 1080; X0 = 80; MAXW = 1760; LS = 1.14
ORANGE, WHITE, INK = (255, 90, 0), (255, 255, 255), (10, 11, 14)


def f(size, w='700'):
    if w == 'black':
        ft = ImageFont.truetype(os.path.join(FONT, 'NotoSansKR-Black.ttf'), size); ft.set_variation_by_name('Black'); return ft
    return ImageFont.truetype(os.path.join(FONT, f'pd{w}.ttf'), size)


def photo(name, y_anchor=0.5, x_anchor=0.5, zoom=1.0, dark=1.0):
    im = Image.open(os.path.join(FR, name)).convert('RGB')
    r = max(W / im.width, HH / im.height) * zoom
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x = int((im.width - W) * x_anchor); y = int((im.height - HH) * y_anchor)
    im = im.crop((x, y, x + W, y + HH))
    return ImageEnhance.Brightness(im).enhance(dark) if dark != 1.0 else im


def shade(im, y0, y1, alpha, top=False):
    m = Image.new('L', im.size, 0); d = ImageDraw.Draw(m)
    for y in range(y0, y1):
        t = (y - y0) / max(1, (y1 - y0) * 0.45) if not top else (y1 - y) / max(1, (y1 - y0) * 0.45)
        d.line([(0, y), (W, y)], fill=int(alpha * min(1, t)))
    return Image.composite(Image.new('RGB', im.size, INK), im, m)


def fit(d, t, size, w, maxw=MAXW, floor=40):
    while size > floor and d.textlength(t, font=f(size, w)) > maxw: size -= 4
    return size


def make(name, pic, top, big, pill, band=110, top_alpha=200, bigmax=210, **ph):
    im = photo(pic, **ph); d0 = ImageDraw.Draw(im)
    ws = fit(d0, top, 76, '700'); bs = min(fit(d0, t, bigmax, 'black') for t in big); ps = 62
    hb = len(big) * int(bs * LS); y = HH - 40 - hb
    im = shade(im, max(0, y - 140), HH, band)
    im = shade(im, 0, 330, top_alpha, top=True)
    d = ImageDraw.Draw(im)
    d.text((X0, 40), top, font=f(ws, '700'), fill=WHITE, stroke_width=3, stroke_fill=INK)
    py = 40 + ws + 20; ft = f(ps, '700'); tw = d.textlength(pill, font=ft); phh = int(ps * 1.4)
    d.rounded_rectangle((X0, py, X0 + tw + 52, py + phh), 18, fill=ORANGE)
    d.text((X0 + 26, py + phh // 2), pill, font=ft, fill=WHITE, anchor='lm')
    for k, t in enumerate(big):
        d.text((X0, y - int(bs * 0.12)), t, font=f(bs, 'black'), fill=WHITE if k == 0 else ORANGE, stroke_width=6, stroke_fill=INK)
        y += int(bs * LS)
    out = os.path.join(EP, name); im.resize((1280, 720), Image.LANCZOS).save(out)
    print(out, f'큰 글 {bs}px · 덩어리 {hb / HH:.0%}')


# a: 큰 글 = 물음(thumb_A처럼), 알약 = 답
make('thumb_x1n_a.png', '4275306_6.jpg', '원화로 본 1억, 넣은 때에 따라', ['S&P500에 1억', '산 날만 다르면?'],
     '작년 10월 +10% · 올 7월 −11%', y_anchor=0.0, zoom=1.1)
# b: 큰 글 = 답 두 줄(흰 +10%, 주황 −11%), 작은 줄 = 물음
make('thumb_x1n_b.png', '4275306_6.jpg', 'S&P500에 1억, 산 날만 다르면?', ['작년 10월 +10%', '올 7월 −11%'],
     '원화 기준', y_anchor=0.0, zoom=1.1)
# c: b와 문구 같고 사진만 위에서 본 달러 세기
make('thumb_x1n_c.png', '5466779_2.jpg', 'S&P500에 1억, 산 날만 다르면?', ['작년 10월 +10%', '올 7월 −11%'],
     '원화 기준', y_anchor=0.2, zoom=1.15, dark=0.95)

json.dump({
    '4275306': {'site': 'Pexels(영상 프레임)', 'by': 'Saif Abdulraheem', 'url': 'https://www.pexels.com/video/person-counting-money-4275306/', 'license': 'https://www.pexels.com/license/', 'face': '없음(손만)', 'frame': '6초'},
    '5466779': {'site': 'Pexels(영상 프레임)', 'by': 'olia danilevich', 'url': 'https://www.pexels.com/video/a-person-counting-money-5466779/', 'license': 'https://www.pexels.com/license/', 'face': '없음(손만)', 'frame': '2초'},
}, open(os.path.join(H, 'sources.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
