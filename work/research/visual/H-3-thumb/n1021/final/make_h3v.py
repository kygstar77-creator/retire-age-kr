# visual 10/21 09시 최종판 — copywriter make_h3c.py 복사, 문구는 titles.md 끝 1위(c) 그대로, 168px 윗줄 흐림(3/3) 때문에 윗줄·알약만 키움
#   1차 이해 시험(judges.md) 막힘: 압구정 알약이 따로 놂·168px 윗줄 뭉개짐·㎡→평·vs 결론 없음·최근 거래인가
#   숫자는 ep/H-3/facts.txt [1][2][12][24]만: 85㎡(25.7평)·96㎡(29.0평)·차이 11㎡ ≈ 3.3평(전용 기준, 말 '집 안 넓이로 3평쯤')
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
sys.stdout.reconfigure(encoding='utf-8')
O = os.path.dirname(os.path.abspath(__file__)); H = os.path.dirname(O); WORK = os.path.abspath(os.path.join(H, '..', '..', '..', '..'))
FONT = os.path.join(WORK, 'fonts'); W, HH = 1920, 1080; X0 = 80; MAXW = 1760
ORANGE, WHITE, INK = (255, 90, 0), (255, 255, 255), (10, 11, 14)
BIG = ['송파 신천동 85㎡ vs', '목동신시가지 96㎡']
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
def make(out, top, pill, top_size=88, pill_size=100, band=235, ls=1.14):
    im = photo('p_3736898.jpg', y_anchor=0.2); d0 = ImageDraw.Draw(im)
    bs = min(fit(d0, t, 200, 'black') for t in BIG); hb = len(BIG) * int(bs * ls); y = HH - 40 - hb
    top_size = fit(d0, top, top_size, '700')
    im = shade(im, max(0, y - 160), HH, band); im = shade(im, 0, 420, 215, top=True); d = ImageDraw.Draw(im)
    d.text((X0, 36), top, font=f(top_size, '700'), fill=WHITE, stroke_width=4, stroke_fill=INK)
    if pill:
        pill_size = fit(d0, pill, pill_size, '700', MAXW - 64)
        yy = 36 + top_size + 28; ft = f(pill_size, '700'); tw = d.textlength(pill, font=ft); ph = int(pill_size * 1.36)
        d.rounded_rectangle((X0, yy, X0 + tw + 64, yy + ph), 24, fill=ORANGE); d.text((X0 + 32, yy + ph // 2), pill, font=ft, fill=WHITE, anchor='lm')
    for k, t in enumerate(BIG):
        d.text((X0, y - int(bs * 0.12)), t, font=f(bs, 'black'), fill=WHITE if k == 0 else ORANGE, stroke_width=6, stroke_fill=INK); y += int(bs * ls)
    sm = im.resize((1280, 720), Image.LANCZOS); sm.save(os.path.join(O, out))
    for px in (412, 168): sm.resize((px, px * 9 // 16), Image.LANCZOS).save(os.path.join(O, out.replace('.png', f'_{px}.png')))
    print(out, top_size, pill_size if pill else '-')



make('h3v_a.png', '최근 1년 30억 안팎에 팔린 집 크기', '목동신시가지가 3평쯤 더 넓다', top_size=112, pill_size=116)
make('h3v_b.png', '최근 1년 30억 안팎에 팔린 집 크기', '목동신시가지가 3평쯤 더 넓다', top_size=132, pill_size=132)
