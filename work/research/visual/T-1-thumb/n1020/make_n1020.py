# T-1 새 꼴(10/20 운영실장 지시) — N-2 thumb_A 꼴 + 큰 글 아래 40~45%(textpos-1019 h2tp_a2 만드는 법 그대로).
#   사진: Pexels 영상 31400388 '손이 열쇠를 들고 있다(돈·작은 집 모형 위)' Jakub Zerdzicki, 3초 프레임(ep/T-1/stock/credits.json). 얼굴 없음.
#   문구: ep/T-1/meta.json thumb_text_small / thumb_text / thumb_text_pill (copywriter 10/19 19:01) 그대로. 새 말 없음.
#   python make_n1020.py → t1n_a.png(그늘 옅게), t1n_b.png(주황을 '10년 거주의 약 12배'로 바꾼 대안, 1초 시험에서 '세금 인상' 오독 시)
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.abspath(os.path.join(H, '..', '..', '..', '..'))
FONT = os.path.join(WORK, 'fonts')
W, HH = 1920, 1080; X0 = 80; MAXW = 1760
ORANGE, WHITE, INK = (255, 90, 0), (255, 255, 255), (10, 11, 14)
TOP = '양도세 정부안 · 20억 집 10년 보유'
PILL = '10년 다 거주한 집보다'

def f(size, w='700'):
    if w == 'black':
        ft = ImageFont.truetype(os.path.join(FONT, 'NotoSansKR-Black.ttf'), size); ft.set_variation_by_name('Black'); return ft
    return ImageFont.truetype(os.path.join(FONT, f'pd{w}.ttf'), size)

def photo(name, y_anchor=0.5, x_anchor=0.5, zoom=1.0, dark=1.0):
    im = Image.open(os.path.join(H, name)).convert('RGB')
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

def make(out, big, band, pid_kw, ls=1.14, bigsize=210):
    im = photo('f_31400388.jpg', **pid_kw); d0 = ImageDraw.Draw(im)
    ws = fit(d0, TOP, 76, '700'); bs = min(fit(d0, t, bigsize, 'black') for t in big); ps = 58
    hb = len(big) * int(bs * ls); y = HH - 40 - hb
    im = shade(im, max(0, y - 140), HH, band); im = shade(im, 0, 330, 200, top=True)
    d = ImageDraw.Draw(im)
    d.text((X0, 40), TOP, font=f(ws, '700'), fill=WHITE, stroke_width=3, stroke_fill=INK)
    yy = 40 + ws + 20; ft = f(ps, '700'); tw = d.textlength(PILL, font=ft); ph = int(ps * 1.4)
    d.rounded_rectangle((X0, yy, X0 + tw + 52, yy + ph), 18, fill=ORANGE); d.text((X0 + 26, yy + ph // 2), PILL, font=ft, fill=WHITE, anchor='lm')
    for k, t in enumerate(big):
        d.text((X0, y - int(bs * 0.12)), t, font=f(bs, 'black'), fill=WHITE if k == 0 else ORANGE, stroke_width=6, stroke_fill=INK); y += int(bs * ls)
    im.resize((1280, 720), Image.LANCZOS).save(os.path.join(H, out)); print(out, f'큰 글 {hb / HH:.0%}')

if __name__ == '__main__':
    kw = dict(y_anchor=0.0, zoom=1.0, dark=1.0)
    make('t1n_a.png', ['10년 중 2년만 거주했으면', '2029년 양도세 약 12배'], 160, kw)
    make('t1n_b.png', ['10년 중 2년만 거주했으면', '10년 거주의 약 12배'], 160, kw)
