# H-2 시험판 — 글자 '아래' 배치(10/19 textpos 조사: 경쟁 90장 중 82장이 큰 글 아래, 왼쪽 위 0장).
#   꼴은 N-2 thumb_A(rethumb-1019/make_r1019.py)와 같은 부품(작은 흰 줄 · 큰 글 · 주황 알약, 같은 글꼴·색).
#   큰 두 줄만 아래로(경쟁 공통: 아래 35~40%·두 줄·폭 거의 끝까지). 작은 흰 줄·알약은 왼쪽 위 작게(경쟁도 작은 글은 위에 둠:
#   월부 따옴표·김작가 노란 줄·똑재 위 줄). 세 층을 다 아래에 쌓으면 화면의 58%라 경쟁보다 너무 높아서 나눴다(첫 시도 실측).
#   문구는 meta.json thumb_text_top / thumb_text 그대로, 숫자는 h2f4 라벨·큰 글(잠실동 안에서 매매 43억 · 전세 5억 남짓) 그대로. 새 말 없음.
#   h2tp_a: 노을 실루엣(Pexels 5336495, frame1018 5차에서 '다른 단지 오인' 피하려 쓴 사진) — 아래 절반이 원래 어두운 땅이라 그 빈 곳에 글자
#   h2tp_b: 파란 하늘 고층 단지(Pexels 15928940) + 아래 짙은 그라데이션 띠 — 단지 꼭대기는 가운데, 큰 글은 아래 띠 위(경쟁 '얼굴 위·글 아래'와 같은 나눔)
#   h2tp_c: 대조판 — h2tp_a와 사진·문구 같고 글자만 왼쪽 위(지금 우리 꼴). 테스트 및 비교에서 자리만 견주는 용도
#   python make_h2tp.py → textpos-1019/h2tp_a.png, h2tp_b.png, h2tp_c.png (1280×720). meta.json·유튜브는 건드리지 않는다.
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(os.path.join(H, '..', '..', '..'))
FONT = os.path.join(WORK, 'fonts'); PX = os.path.join(WORK, 'research', 'aptreal', 'px')
LS = 1.10
W, HH = 1920, 1080; X0 = 80; MAXW = 1760
ORANGE, WHITE, INK = (255, 90, 0), (255, 255, 255), (10, 11, 14)
TOP = '잠실주공5단지, 잠실동 안에서'
BIG = ['매매는 가장 비싸고', '전세는 가장 쌌다']
PILL = '매매 43억 · 전세 5억 남짓'


def f(size, w='700'):
    if w == 'black':
        ft = ImageFont.truetype(os.path.join(FONT, 'NotoSansKR-Black.ttf'), size); ft.set_variation_by_name('Black'); return ft
    return ImageFont.truetype(os.path.join(FONT, f'pd{w}.ttf'), size)


def photo(pid, y_anchor=0.5, x_anchor=0.5, zoom=1.0, dark=1.0, blur=0):
    p = [x for x in os.listdir(PX) if x.endswith(f'_{pid}.jpg')][0]
    im = Image.open(os.path.join(PX, p)).convert('RGB')
    r = max(W / im.width, HH / im.height) * zoom
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x = int((im.width - W) * x_anchor); y = int((im.height - HH) * y_anchor)
    im = im.crop((x, y, x + W, y + HH))
    if blur: im = im.filter(ImageFilter.GaussianBlur(blur))  # 남의 단지 이름·동 번호가 읽히지 않게
    return ImageEnhance.Brightness(im).enhance(dark) if dark != 1.0 else im


def shade(im, y0, y1, alpha, top=False):
    """y0~y1 사이를 한쪽에서 옅어지게 어둡힌다(상자 아님)."""
    m = Image.new('L', im.size, 0); d = ImageDraw.Draw(m)
    for y in range(y0, y1):
        t = (y - y0) / max(1, (y1 - y0) * 0.45) if not top else (y1 - y) / max(1, (y1 - y0) * 0.45)
        d.line([(0, y), (W, y)], fill=int(alpha * min(1, t)))
    return Image.composite(Image.new('RGB', im.size, INK), im, m)


def fit(d, t, size, w, maxw=MAXW, floor=40):
    while size > floor and d.textlength(t, font=f(size, w)) > maxw: size -= 4
    return size


def layout(d, big=210):
    ws = fit(d, TOP, 76, '700'); bs = min(fit(d, t, big, 'black') for t in BIG); ps = 58
    return ws, bs, ps


def draw_small(d, y, ws, ps):
    d.text((X0, y), TOP, font=f(ws, '700'), fill=WHITE, stroke_width=3, stroke_fill=INK); y += ws + 20
    ft = f(ps, '700'); tw = d.textlength(PILL, font=ft); ph = int(ps * 1.4)
    d.rounded_rectangle((X0, y, X0 + tw + 52, y + ph), 18, fill=ORANGE)
    d.text((X0 + 26, y + ph // 2), PILL, font=ft, fill=WHITE, anchor='lm')
    return y + ph


def draw_big(d, y, bs):
    for k, t in enumerate(BIG):
        d.text((X0, y - int(bs * 0.12)), t, font=f(bs, 'black'), fill=WHITE if k == 0 else ORANGE, stroke_width=6, stroke_fill=INK)
        y += int(bs * LS)
    return y


def bottom(name, pid, band_alpha, top_alpha=200, **ph):
    im = photo(pid, **ph); d0 = ImageDraw.Draw(im)
    ws, bs, ps = layout(d0); hb = len(BIG) * int(bs * LS)
    y = HH - 40 - hb
    im = shade(im, max(0, y - 140), HH, band_alpha)
    im = shade(im, 0, 330, top_alpha, top=True)
    d = ImageDraw.Draw(im); draw_small(d, 40, ws, ps); draw_big(d, y, bs)
    save(im, name, hb)


def topleft(name, pid, **ph):
    """대조판: 지금 우리 꼴 그대로(작은 흰 줄 → 큰 두 줄 → 알약, 위에서부터)."""
    im = photo(pid, **ph); d0 = ImageDraw.Draw(im)
    ws, bs, ps = layout(d0); hb = len(BIG) * int(bs * 1.10)
    h = ws + 24 + hb + 30 + int(ps * 1.4)
    im = shade(im, 0, min(HH, 40 + h + 150), 225, top=True)
    d = ImageDraw.Draw(im)
    d.text((X0, 40), TOP, font=f(ws, '700'), fill=WHITE)
    y = draw_big(d, 40 + ws + 24, bs) + 30
    ft = f(ps, '700'); tw = d.textlength(PILL, font=ft); ph_ = int(ps * 1.4)
    d.rounded_rectangle((X0, y, X0 + tw + 52, y + ph_), 18, fill=ORANGE)
    d.text((X0 + 26, y + ph_ // 2), PILL, font=ft, fill=WHITE, anchor='lm')
    save(im, name, h)


def save(im, name, h):
    out = os.path.join(H, name); im.resize((1280, 720), Image.LANCZOS).save(out)
    print(out, f'큰 글 덩어리 높이 {h}px = 화면의 {h / HH:.0%}')


LS = 1.10
bottom('h2tp_a.png', '5336495', 150, y_anchor=0.35, zoom=1.0)       # 실루엣: 땅이 원래 어둡다 → 옅은 그늘만
bottom('h2tp_b.png', '15928940', 235, y_anchor=0.95, x_anchor=0.6, zoom=1.4, blur=9)  # 파란 하늘 고층 단지(Pexels 15928940) + 짙은 아래 띠. 벽에 다른 단지 이름('호수마을'·동 번호)이 보여 흐리게 함(잠실주공5단지 오인 방지). 지금 h2f4 사진(11932032)은 건물이 아래 40%에 몰려 큰 글에 다 가려져 뺐다(첫 시도 실측)
topleft('h2tp_c.png', '5336495', y_anchor=0.35, zoom=1.0)           # 대조판(왼쪽 위)

# 10/19 15시대 2차: 채점 1차(a 6점: 사진 어둡다·줄간격 좁다) 반영 — 같은 사진, 아래 그늘 옅게(150→70)·줄간격 1.10→1.14, 사진을 조금 밝게
LS = 1.14
bottom('h2tp_a2.png', '5336495', 70, y_anchor=0.35, zoom=1.0, dark=1.12)
