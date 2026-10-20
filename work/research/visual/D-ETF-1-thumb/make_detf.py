# D-ETF-1 썸네일 시안(10/20 17시, 지시 13:08 기한 10/23 12:00) — N-2 thumb_A 꼴 + 큰 글 두 줄 아래 40~45%(C-01·C-02·C-06), 알약 없음(C-10, 큰 글이 답 숫자를 품음).
#   부품·글꼴·색은 X-1-thumb/n1019/make_x1n.py와 같다. 문구는 ep/D-ETF-1/copy/titles.md 1위(copywriter 10/20 07:58) 그대로. 새 말 없음.
#   숫자: facts [Y3] SCHD 한 주당 배당 10년 연 10.8%(→11%)·최근 1년 2.0%(1.034→1.055달러), calc_out.txt 27행 2.0/…/10.8.
#   사진: Pexels 9755376(Towfiqu barbhuiya, 손으로 동전 쌓기·얼굴 없음) · 4912789(동전 더미·지폐 가까이, 사람 없음) — 28504956 휴대폰 판은 남의 앱 화면을 흐린 경계가 어색해 버림.
#   py -3.12 make_detf.py → ep/D-ETF-1/thumb_detf_a.png, _b.png (1280×720). meta.json·유튜브는 건드리지 않는다.
import os, sys, json
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(os.path.join(H, '..', '..', '..'))
FONT = os.path.join(WORK, 'fonts'); PH = os.path.join(H, 'photo')
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'D-ETF-1')
W, HH = 1920, 1080; X0 = 80; MAXW = 1760; LS = 1.14
ORANGE, WHITE, INK = (255, 90, 0), (255, 255, 255), (10, 11, 14)
TOP = 'SCHD 한 주당 배당금 · 10년 평균 vs 최근 1년'
BIG = ['해마다 11%씩 늘던 배당', '최근엔 2%만 늘었다']


def f(size, w='700'):
    if w == 'black':
        ft = ImageFont.truetype(os.path.join(FONT, 'NotoSansKR-Black.ttf'), size); ft.set_variation_by_name('Black'); return ft
    return ImageFont.truetype(os.path.join(FONT, f'pd{w}.ttf'), size)


def photo(name, y_anchor=0.5, x_anchor=0.5, zoom=1.0, dark=1.0, blur_box=None):
    im = Image.open(os.path.join(PH, name)).convert('RGB')
    if blur_box:  # 원본 좌표 비율 (x0,y0,x1,y1) — 남의 앱 화면 흐림
        b = tuple(int(v * s) for v, s in zip(blur_box, (im.width, im.height) * 2))
        im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(28)), b[:2])
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


def make(name, pic, band=215, top_alpha=200, bigmax=210, **ph):
    im = photo(pic, **ph); d0 = ImageDraw.Draw(im)
    ws = fit(d0, TOP, 76, '700'); bs = min(fit(d0, t, bigmax, 'black') for t in BIG)
    hb = len(BIG) * int(bs * LS); y = HH - 40 - hb
    im = shade(im, max(0, y - 140), HH, band)
    im = shade(im, 0, 300, top_alpha, top=True)
    d = ImageDraw.Draw(im)
    d.text((X0, 40), TOP, font=f(ws, '700'), fill=WHITE, stroke_width=3, stroke_fill=INK)
    for k, t in enumerate(BIG):
        d.text((X0, y - int(bs * 0.12)), t, font=f(bs, 'black'), fill=WHITE if k == 0 else ORANGE, stroke_width=6, stroke_fill=INK)
        y += int(bs * LS)
    out = os.path.join(EP, name); im.resize((1280, 720), Image.LANCZOS).save(out)
    print(out, f'큰 글 {bs}px · 덩어리 {hb / HH:.0%}')


make('thumb_detf_a.png', 'detf_coins.jpg', y_anchor=1.0, zoom=1.0, dark=0.9)
make('thumb_detf_b.png', 'detf_coins2.jpg', y_anchor=0.3, zoom=1.0, dark=0.85)
json.dump({k: v for k, v in json.load(open(os.path.join(H, '..', 'rethumb-1019', 'photo', 'sources.json'), encoding='utf-8')).items() if k.startswith('detf_')},
          open(os.path.join(PH, 'sources.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
