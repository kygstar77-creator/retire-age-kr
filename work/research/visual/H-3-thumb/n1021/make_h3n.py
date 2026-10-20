# H-3 새 꼴(10/21 visual, PD 요청) — N-2 thumb_A 꼴 + 큰 글 아래 40~45%(T-1 make_n1020 틀 그대로).
#   문구: ep/H-3/copy/titles.md B3'(앞줄·큰 글·작은 줄) 그대로, 동네만 18:10 요청대로 '송파 신천동'. 새 말 없음.
#   사진: Pexels(번호·작가·주소 sources.json), 얼굴 없음.  py -3.12 make_h3n.py → h3n_a.png, h3n_b.png (1280x720)
import os, sys, json
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.abspath(os.path.join(H, '..', '..', '..', '..'))
FONT = os.path.join(WORK, 'fonts'); W, HH = 1920, 1080; X0 = 80; MAXW = 1760
ORANGE, WHITE, INK = (255, 90, 0), (255, 255, 255), (10, 11, 14)
TOP = '30억 안팎에 팔린 집 크기'; PILL = '압구정동은 가장 싼 거래도 35억 넘어'
BIG = ['송파 신천동 85㎡ vs', '목동신시가지 96㎡']
def f(size, w='700'):
    if w == 'black':
        ft = ImageFont.truetype(os.path.join(FONT, 'NotoSansKR-Black.ttf'), size); ft.set_variation_by_name('Black'); return ft
    return ImageFont.truetype(os.path.join(FONT, f'pd{w}.ttf'), size)
def photo(name, y_anchor=0.0, x_anchor=0.5, zoom=1.0, dark=1.0):
    im = Image.open(os.path.join(H, name)).convert('RGB'); r = max(W / im.width, HH / im.height) * zoom
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x = int((im.width - W) * x_anchor); y = int((im.height - HH) * y_anchor); im = im.crop((x, y, x + W, y + HH))
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
def make(out, pname, kw, band=235, top_size=72, pill_size=84, ls=1.14):
    im = photo(pname, **kw); d0 = ImageDraw.Draw(im)
    bs = min(fit(d0, t, 200, 'black') for t in BIG); hb = len(BIG) * int(bs * ls); y = HH - 40 - hb
    pill_size = min(pill_size, fit(d0, PILL, pill_size, '700', MAXW - 64))
    im = shade(im, max(0, y - 160), HH, band); im = shade(im, 0, 380, 215, top=True)
    d = ImageDraw.Draw(im)
    d.text((X0, 36), TOP, font=f(top_size, '700'), fill=WHITE, stroke_width=3, stroke_fill=INK)
    yy = 36 + top_size + 24; ft = f(pill_size, '700'); tw = d.textlength(PILL, font=ft); ph = int(pill_size * 1.36)
    d.rounded_rectangle((X0, yy, X0 + tw + 64, yy + ph), 24, fill=ORANGE); d.text((X0 + 32, yy + ph // 2), PILL, font=ft, fill=WHITE, anchor='lm')
    for k, t in enumerate(BIG):
        d.text((X0, y - int(bs * 0.12)), t, font=f(bs, 'black'), fill=WHITE if k == 0 else ORANGE, stroke_width=6, stroke_fill=INK); y += int(bs * ls)
    im.resize((1280, 720), Image.LANCZOS).save(os.path.join(H, out)); print(out, f'큰 글 {hb / HH:.0%} 크기 {bs} 알약 {pill_size}')
make('h3n_a.png', 'p_38249703.jpg', dict(y_anchor=0.35, zoom=1.0))
make('h3n_b.png', 'p_3736898.jpg', dict(y_anchor=0.2, zoom=1.0))
json.dump({'p_38249703.jpg': {'site': 'Pexels', 'id': 38249703, 'by': 'Jueon Kim', 'url': 'https://www.pexels.com/photo/high-rise-residential-building-in-seoul-south-korea-38249703/', 'license': 'Pexels License', 'face': '없음'},
 'p_3736898.jpg': {'site': 'Pexels', 'id': 3736898, 'url': 'https://www.pexels.com/photo/modern-multistory-building-with-windows-and-balconies-in-city-3736898/', 'license': 'Pexels License', 'face': '없음'}}, open(os.path.join(H, 'sources.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
