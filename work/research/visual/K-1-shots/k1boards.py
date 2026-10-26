"""K-1 장면 판 25장 — visual-designer 2026-10-26.
H-3 판(board_loan 등)과 같은 꼴: 구겨진 종이 바탕 · 찢은 종이 막대·조각 · 주황 #FF5A00은 그 화면의 답 하나 · 손으로 그린 동그라미·밑줄.
숫자는 ep/K-1/facts.txt(F1~F25)·raw/series.json 값만. 판은 '답이 열린 마지막 모습' — '?' → 열림 움직임은 PD가 Remotion에서 건다.
사용: py -3.12 k1boards.py [이름 ...]   (없으면 전부) → work/video/public/bg/k1/board/<이름>.png
"""
import os, sys, json, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'K-1')
OUT = os.path.join(WORK, 'video', 'public', 'bg', 'k1', 'board')
PAPER = os.path.join(WORK, 'video', 'public', 'human', 'paper_crumple.jpg')
F_B = os.path.join(WORK, 'fonts', 'pd700.ttf')
F_M = os.path.join(WORK, 'fonts', 'pd500.ttf')
F_X = os.path.join(WORK, 'fonts', 'NotoSansKR-Black.ttf')
W, H = 1920, 1080
INK = (24, 24, 27); GREY = (92, 92, 98); SRC = (110, 110, 116)
OR = (255, 90, 0); KRAFT = (192, 156, 114); KRAFT_L = (214, 190, 160); FADE = (196, 182, 160)
SER = json.load(open(os.path.join(EP, 'raw', 'series.json'), encoding='utf-8'))

_FC = {}
def font(path, size):
    k = (path, size)
    if k not in _FC:
        f = ImageFont.truetype(path, size)
        if path == F_X:
            try: f.set_variation_by_axes([900])   # NotoSansKR-Black은 가변 글꼴 — 기본이 Thin이라 900으로
            except Exception: pass
        _FC[k] = f
    return _FC[k]

def canvas(sepia=False):
    im = Image.open(PAPER).convert('RGB').resize((W, H))
    if sepia:
        tint = Image.new('RGB', (W, H), (236, 222, 196))
        im = Image.blend(im, tint, 0.45)
    return im

def T(d, xy, s, size, fill=INK, f=F_B, anchor='mm'):
    d.text(xy, s, font=font(f, size), fill=fill, anchor=anchor)

def title(d, s, y=96): T(d, (W // 2, y), s, 64)

def source(d, s): T(d, (W - 48, H - 44), s, 26, SRC, F_M, 'rs')

def torn(im, box, color, seed=1, shadow=True):
    """찢은 종이 사각형(가장자리 들쭉날쭉) + 옅은 그림자."""
    rnd = random.Random(seed); x0, y0, x1, y1 = box; pts = []
    def edge(ax, ay, bx, by):
        n = max(4, int(math.hypot(bx - ax, by - ay) / 14))
        for i in range(n):
            t = i / n; j = rnd.uniform(-3.5, 3.5)
            if ax == bx: pts.append((ax + j, ay + (by - ay) * t))
            else: pts.append((ax + (bx - ax) * t, ay + j))
    edge(x0, y0, x1, y0); edge(x1, y0, x1, y1); edge(x1, y1, x0, y1); edge(x0, y1, x0, y0)
    if shadow:
        sh = Image.new('L', (W, H), 0); ImageDraw.Draw(sh).polygon([(x + 7, y + 8) for x, y in pts], fill=70)
        sh = sh.filter(ImageFilter.GaussianBlur(7)); im.paste((150, 146, 140), (0, 0), sh)
    ImageDraw.Draw(im).polygon(pts, fill=color)

def hand_ellipse(d, box, color=OR, width=8, seed=3):
    rnd = random.Random(seed); x0, y0, x1, y1 = box; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; rx, ry = (x1 - x0) / 2, (y1 - y0) / 2
    pts = []
    for i in range(0, 361):
        a = math.radians(i * 1.0 - 100); k = 1 + 0.035 * math.sin(i / 23) + rnd.uniform(-0.004, 0.004)
        pts.append((cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)))
    d.line(pts, fill=color, width=width, joint='curve')

def hand_under(d, x0, x1, y, color=OR, width=9, seed=5):
    rnd = random.Random(seed); pts = [(x0 + (x1 - x0) * i / 30, y + 6 * math.sin(i / 5) * 0.5 + rnd.uniform(-1.5, 1.5) + (i / 30) * 6) for i in range(31)]
    d.line(pts, fill=color, width=width, joint='curve')

def hand_check(d, x, y, s=44, color=OR, width=9):
    d.line([(x, y), (x + s * 0.38, y + s * 0.42), (x + s, y - s * 0.55)], fill=color, width=width, joint='curve')

def hand_arrow(d, a, b, color=INK, width=6):
    d.line([a, b], fill=color, width=width)
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    for s in (2.6, -2.6):
        d.line([b, (b[0] + 26 * math.cos(ang + s), b[1] + 26 * math.sin(ang + s))], fill=color, width=width)

def bars(im, items, base_y=860, top_y=260, bw=260, gap=200, vmax=None, fmt=lambda v: f'{v}', seed=10):
    """items: (아래 이름, 값, 색, 위 숫자 글, 숫자 색)"""
    d = ImageDraw.Draw(im); n = len(items); vmax = vmax or max(v for _, v, *_ in items)
    tot = n * bw + (n - 1) * gap; x = (W - tot) // 2; tops = []
    for i, (lab, v, col, top, tcol) in enumerate(items):
        h = (base_y - top_y) * v / vmax; y = base_y - h
        torn(im, (x, y, x + bw, base_y), col, seed=seed + i)
        T(d, (x + bw // 2, y - 64), top, 84, tcol, F_X)
        T(d, (x + bw // 2, base_y + 60), lab, 46)
        tops.append((x, y, x + bw)); x += bw + gap
    return tops

def months(key, a, b): return [(m, SER[key][m]) for m in sorted(SER[key]) if a <= m <= b]

def linechart(im, series, box, ymin, ymax, colors, widths, xlabels, dash=None, fill_between=None, yfmt='{:.0f}%', yticks=()):
    d = ImageDraw.Draw(im); x0, y0, x1, y1 = box; n = len(series[0])
    X = lambda i: x0 + (x1 - x0) * i / (n - 1); Y = lambda v: y1 - (y1 - y0) * (v - ymin) / (ymax - ymin)
    for v in yticks:
        T(d, (x0 - 18, Y(v)), yfmt.format(v), 30, GREY, F_M, 'rm')
    d.line([(x0, y1), (x1, y1)], fill=(150, 146, 140), width=3)
    if fill_between:
        a, b, col = fill_between
        poly = [(X(i), Y(v)) for i, v in enumerate(series[a])] + [(X(i), Y(v)) for i, v in reversed(list(enumerate(series[b])))]
        ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(ov).polygon(poly, fill=col)
        im.paste(ov, (0, 0), ov)
    if dash is not None:
        yy = Y(dash); xx = x0
        while xx < x1: d.line([(xx, yy), (min(xx + 22, x1), yy)], fill=GREY, width=4); xx += 38
    for s, c, w in zip(series, colors, widths):
        d.line([(X(i), Y(v)) for i, v in enumerate(s)], fill=c, width=w, joint='curve')
    for i, lab in xlabels: T(d, (X(i), y1 + 40), lab, 32, GREY, F_M)
    return X, Y

B = {}
def board(fn):
    B[fn.__name__] = fn; return fn

@board
def k1_two_q(im):
    d = ImageDraw.Draw(im); title(d, '미국 국채금리 5%, 그럼 내 통장은?', 150)
    for i, (lab, seed) in enumerate((('내 예금 이자', 21), ('내 대출 이자', 22))):
        y = 400 + i * 260
        torn(im, (330, y, 1590, y + 190), KRAFT_L, seed=seed)
        T(d, (560, y + 95), lab, 70)
        T(d, (1330, y + 95), '?', 150, OR if i == 0 else INK, F_X)
    source(d, '한국은행 경제통계시스템 · 2025년 8월과 2026년 8월 비교')

@board
def k1_answer2(im):
    d = ImageDraw.Draw(im); title(d, '답부터', 130)
    rows = (('예금 1억, 1년 이자', '74만원 더', '작년 8월 대비'), ('2021년 고정 대출, 한 달', '28만원 정도 더', '2021년 대비'))
    for i, (a, b, c) in enumerate(rows):
        y = 360 + i * 300
        T(d, (W // 2, y), a, 56, GREY)
        T(d, (W // 2, y + 110), b, 110, INK, F_X)
        T(d, (W // 2, y + 225), c, 40, INK, F_M)
        bw = font(F_X, 110).getlength(b); hand_under(d, W // 2 - bw / 2, W // 2 + bw / 2, y + 180, seed=7 + i)
    source(d, '세금(15.4%) 뗀 이자 · 대출은 3억원·30년, 평균 금리로 다시 정한 가정')

@board
def k1_q5(im):
    d = ImageDraw.Draw(im); title(d, '오늘 볼 다섯 가지', 120)
    qs = ('미국 국채금리 5%, 무슨 숫자인가', '내 예금 이자는 얼마나 따라왔나', '내 대출 이자는 — 고정형과 변동형', '정말 미국 때문일까', '고정 끝나는 사람은 얼마나 오르나')
    for i, q in enumerate(qs):
        y = 260 + i * 150
        T(d, (470, y), f'{i + 1}', 76, OR if i == 3 else INK, F_X)
        T(d, (560, y), q, 58, INK, F_B, 'lm')
        if i == 3: hand_ellipse(d, (400, y - 70, 1210, y + 70), seed=9)

@board
def k1_bond_note(im):
    d = ImageDraw.Draw(im)
    torn(im, (260, 150, 1660, 930), (238, 230, 212), seed=31)
    d.rectangle((320, 210, 1600, 870), outline=(150, 120, 80), width=4); d.rectangle((336, 226, 1584, 854), outline=(150, 120, 80), width=2)
    T(d, (W // 2, 300), '미국 정부에 빌려준 돈', 52, GREY)
    T(d, (W // 2, 420), '1만 달러 · 10년', 96, INK, F_X)
    T(d, (W // 2, 560), '금리 5%', 72, INK, F_B)
    T(d, (W // 2 - 40, 720), '한 해 이자 500달러', 96, OR, F_X)
    # 돋보기(이자 칸)
    cx, cy, r = 1490, 600, 80
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=INK, width=12)
    d.line([(cx + r * 0.7, cy + r * 0.7), (cx + r * 1.5, cy + r * 1.5)], fill=INK, width=24)
    source(d, '1만 달러 × 5% = 500달러')

@board
def k1_dgs10(im):
    d = ImageDraw.Draw(im); title(d, '미국 10년 국채금리', 90)
    pts = sorted(SER['us_d'].items()); vals = [v for _, v in pts]; n = len(vals)
    box = (200, 220, 1760, 880)
    xl = [(i, k[:4]) for i, (k, _) in enumerate(pts) if k[5:10] in ('01-03', '01-02') or (k[:4] == '2023' and i == 0)]
    seen = set(); xl2 = []
    for i, k in enumerate(pts):
        y = k[0][:4]
        if y not in seen: seen.add(y); xl2.append((i, y + '년'))
    X, Y = linechart(im, [vals], box, 3.0, 6.0, [INK], [5], xl2, dash=5.0, yticks=(3, 4, 5))
    T(d, (box[0] + 10, Y(5.0) - 30), '5%', 40, GREY, F_B, 'lm')
    i_first = next(i for i, (k, v) in enumerate(pts) if k >= '2026-09-15' and v >= 5.0)
    i_max = max(range(n), key=lambda i: vals[i])
    d.line([(X(i), Y(vals[i])) for i in range(i_first, n)], fill=OR, width=8, joint='curve')
    hand_ellipse(d, (X(i_max) - 140, Y(vals[i_max]) - 110, X(i_max) + 40, Y(vals[i_max]) + 60), seed=12)
    T(d, (X(i_max) - 170, Y(vals[i_max]) - 60), '최고 5.31%', 50, OR, F_X, 'rm')
    T(d, (760, 300), '9월 15일부터 5% 넘은 날 19일', 46, INK, F_B)
    source(d, '미국 연준 FRED DGS10 · 2023.1~2026.10.19 매일 값')

@board
def k1_2007(im):
    im.paste(canvas(sepia=True).crop((0, 0, 1000, H)), (0, 0)); d = ImageDraw.Draw(im)
    d.line([(1000, 140), (1000, 940)], fill=(170, 160, 150), width=3)
    T(d, (500, 200), '2007년 6월', 70, (120, 100, 76), F_X)
    T(d, (500, 420), '미국 10년 5.1%', 66, (120, 100, 76))
    T(d, (500, 620), '한국 주담대 평균', 52, (120, 100, 76), F_M)
    T(d, (500, 730), '6.13%', 110, (120, 100, 76), F_X)
    T(d, (1460, 200), '2026년 8월', 70, INK, F_X)
    T(d, (1460, 420), '미국 10년 4.68%', 66, INK)
    T(d, (1460, 620), '한국 주담대 평균', 52, INK, F_M)
    T(d, (1460, 730), '4.66%', 110, OR, F_X)
    source(d, '월평균 · FRED · 한국은행 예금은행 가중평균금리(신규취급액)')

@board
def k1_us_kr_now(im):
    d = ImageDraw.Draw(im); title(d, '같은 10년짜리 국채금리', 100)
    tops = bars(im, [('미국 (10/15)', 5.10, KRAFT, '5.10%', INK), ('한국 (10/16)', 4.18, KRAFT, '4.18%', INK)], vmax=5.6, top_y=300)
    (ax, ay, ax1), (bx, by, bx1) = tops
    d.line([(ax1 + 10, ay), (bx1 + 40, ay)], fill=OR, width=5)
    hand_arrow(d, (bx1 + 30, ay + 6), (bx1 + 30, by - 6), OR, 7)
    T(d, (bx1 + 60, (ay + by) / 2), '1%p 가까이 낮음', 50, OR, F_X, 'lm')
    source(d, 'FRED DGS10 · 한국 국고채 10년(금융투자협회)')

@board
def k1_dep_bar(im):
    d = ImageDraw.Draw(im); title(d, '1년 정기예금 평균 금리', 100)
    tops = bars(im, [('작년 8월', 2.51, KRAFT, '2.5%', INK), ('올해 8월', 3.39, KRAFT, '3.4%', INK)], vmax=4.0, top_y=300)
    T(d, (W // 2, 200), '1년 새 거의 1%p ↑', 60, OR, F_X)
    source(d, '한국은행 · 예금은행 정기예금 1년, 그달 새로 받은 예금 평균')

@board
def k1_dep_calc(im):
    d = ImageDraw.Draw(im); title(d, '정기예금 1억, 1년 이자 (세금 뗀 뒤)', 110)
    for i, (lab, f, ans) in enumerate((('작년 금리', '1억 × 2.5% − 세금', '212만원'), ('지금 금리', '1억 × 3.4% − 세금', '287만원'))):
        y = 330 + i * 190
        T(d, (330, y), lab, 50, GREY, F_B, 'lm')
        T(d, (640, y), f, 62, INK, F_B, 'lm')
        T(d, (1600, y), '= ' + ans, 76, INK, F_X, 'rm')
    d.line([(330, 650), (1600, 650)], fill=INK, width=4)
    T(d, (W // 2, 790), '차이 74만원', 130, OR, F_X)
    source(d, '이자소득세 15.4% · 한 달로 나누면 6만원 정도')

@board
def k1_coins3(im):
    d = ImageDraw.Draw(im); title(d, '같은 1억, 1년 이자', 100)
    data = (('5년 전 (2021.8)', '1.2%', 98, True), ('1년 전 (2025.8)', '2.5%', 212, False), ('지금 (2026.8)', '3.4%', 287, False))
    for i, (lab, r, v, faded) in enumerate(data):
        cx = 420 + i * 540; n = round(v / 18); base = 820
        col = FADE if faded else (214, 168, 70); edge = (170, 150, 120) if faded else (150, 110, 30)
        for k in range(n):
            y = base - k * 26
            d.ellipse((cx - 110, y - 22, cx + 110, y + 22), fill=col, outline=edge, width=3)
        top = base - n * 26
        T(d, (cx, top - 80), f'{v}만원', 80, (150, 140, 128) if faded else (OR if i == 2 else INK), F_X)
        T(d, (cx, 900), lab, 42, (150, 140, 128) if faded else INK)
        T(d, (cx, 960), r, 40, (150, 140, 128) if faded else GREY, F_M)
    source(d, '세금 뗀 이자 · 한국은행 정기예금 1년 평균')

@board
def k1_cofix89(im):
    d = ImageDraw.Draw(im); title(d, '신규 코픽스 — 은행이 새로 모은 돈의 금리', 100)
    bars(im, [('작년 8월', 2.49, FADE, '2.49%', (150, 140, 128)), ('올해 8월', 3.18, KRAFT, '3.18%', INK), ('9월', 3.43, KRAFT, '3.43%', OR)], vmax=3.9, top_y=300, bw=240, gap=160)
    source(d, '은행연합회 코픽스 · 9월분 10월 15일 발표')

@board
def k1_gap(im):
    d = ImageDraw.Draw(im); title(d, '대출 금리 − 예금 금리', 90)
    a, b = '201901', '202608'
    mt = [v for _, v in months('mtg', a, b)]; dp = [v for _, v in months('dep', a, b)]; ms = [m for m, _ in months('mtg', a, b)]
    box = (220, 210, 1720, 860)
    xl = [(i, m[:4]) for i, m in enumerate(ms) if m.endswith('01')]
    X, Y = linechart(im, [mt, dp], box, 0.5, 5.5, [INK, (120, 100, 76)], [6, 6], xl, fill_between=(0, 1, (255, 90, 0, 40)), yticks=(1, 3, 5))
    T(d, (X(len(ms) - 1) + 12, Y(mt[-1])), '주택담보대출', 34, INK, F_B, 'lm')
    T(d, (X(len(ms) - 1) + 12, Y(dp[-1])), '정기예금', 34, (120, 100, 76), F_B, 'lm')
    for m, lab, col, dx in (('202108', '5년 전 1.9%p', INK, 0), ('202608', '지금 1.5%p', OR, -1)):
        i = ms.index(m); x = X(i); d.line([(x, Y(mt[i])), (x, Y(dp[i]))], fill=col, width=5)
        for yy in (Y(mt[i]), Y(dp[i])): d.line([(x - 12, yy), (x + 12, yy)], fill=col, width=5)
        T(d, (x - 26, (Y(mt[i]) + Y(dp[i])) / 2 + (50 if dx else 0)), lab, 44, col, F_X, 'rm')
    source(d, '한국은행 · 그달 새로 맺은 대출·예금 평균 금리 차이 (공식 예대금리차 지표 아님)')

@board
def k1_fix_var(im):
    d = ImageDraw.Draw(im); title(d, '1년 동안 오른 폭 (새로 받은 주담대)', 100)
    bars(im, [('고정형', 0.94, KRAFT, '+0.94%p', OR), ('변동형', 0.45, KRAFT, '+0.45%p', INK)], vmax=1.15, top_y=300)
    T(d, (W // 2 - 230, 990), '3.94 → 4.88%', 42, INK, F_B); T(d, (W // 2 + 230, 990), '4.08 → 4.53%', 42, INK, F_B)
    source(d, '한국은행 · 2025년 8월 → 2026년 8월')

@board
def k1_cross(im):
    d = ImageDraw.Draw(im); title(d, '고정형과 변동형, 순서가 바뀐 달', 90)
    a, b = '202501', '202608'
    fx = [v for _, v in months('mfix', a, b)]; vr = [v for _, v in months('mvar', a, b)]; ms = [m for m, _ in months('mfix', a, b)]
    box = (220, 220, 1700, 860)
    xl = [(i, f"{m[2:4]}.{m[4:]}") for i, m in enumerate(ms) if m[4:] in ('01', '05', '09')]
    X, Y = linechart(im, [fx, vr], box, 3.6, 5.0, [OR, INK], [7, 6], xl, yfmt='{:.1f}%', yticks=(3.6, 4.0, 4.4, 4.8))
    T(d, (X(len(ms) - 1) + 14, Y(fx[-1])), '고정형', 38, OR, F_B, 'lm')
    T(d, (X(len(ms) - 1) + 14, Y(vr[-1])), '변동형', 38, INK, F_B, 'lm')
    i = ms.index('202604'); hand_ellipse(d, (X(i) - 80, Y(4.31) - 80, X(i) + 80, Y(4.31) + 80), seed=21)
    T(d, (X(i), Y(4.31) + 130), '2026년 4월', 46, INK, F_X)
    source(d, '한국은행 · 예금은행 주담대 고정형·변동형 평균(신규취급액)')

@board
def k1_3eok_table(im):
    d = ImageDraw.Draw(im); title(d, '3억원 · 30년 · 고정형으로 새로 빌리면', 110)
    cx = [560, 1000, 1440]
    for x, h in zip(cx[1:], ('작년 8월', '올해 8월')): T(d, (x, 300), h, 52, GREY)
    rows = (('금리', '3.94%', '4.88%'), ('한 달에', '142만원', '159만원'))
    for r, (a, b, c) in enumerate(rows):
        y = 440 + r * 170
        T(d, (cx[0], y), a, 56, INK, F_B, 'rm'); T(d, (cx[1], y), b, 72, INK, F_X); T(d, (cx[2], y), c, 72, INK, F_X)
    d.line([(380, 360), (1600, 360)], fill=(150, 146, 140), width=3); d.line([(380, 700), (1600, 700)], fill=INK, width=4)
    T(d, (cx[0], 820), '차이', 56, INK, F_B, 'rm'); T(d, ((cx[1] + cx[2]) / 2, 820), '한 달 17만원 정도 더', 90, OR, F_X)
    source(d, '원리금균등 · 평균 금리로 셈한 값, 실제 금리는 은행·상품마다 다름')

@board
def k1_cofix3(im):
    d = ImageDraw.Draw(im)
    T(d, (W // 2, 170), '내 변동금리 = 코픽스 + 은행이 붙이는 금리', 64)
    hand_under(d, 690, 900, 215, INK, 6, seed=2)
    root = (795, 250)
    items = (('신규 코픽스', '그달 새로 모은 돈', '+0.7%p', INK), ('잔액 코픽스', '은행에 남은 돈 전부', '+0.1%p', OR), ('신잔액 코픽스', '', '+0.17%p', INK))
    for i, (a, b, c, col) in enumerate(items):
        x = 420 + i * 540
        d.line([root, (x, 452)], fill=INK, width=5)
        torn(im, (x - 230, 450, x + 230, 830), KRAFT_L, seed=40 + i); d = ImageDraw.Draw(im)
        T(d, (x, 560), a, 52); T(d, (x, 710), c, 90, col, F_X)
    hand_ellipse(d, (960 - 300, 425, 960 + 300, 870), seed=44)
    source(d, '은행연합회 · 2025년 8월 → 2026년 8월 오른 폭')

@board
def k1_trap(im):
    d = ImageDraw.Draw(im); title(d, '조심할 것 두 가지', 110)
    cards = (('하나', '같은 코픽스라도', '사람마다 금리가 달라요'), ('둘', '뉴스 속 평균 금리는', '새로 빌린 사람 평균이에요'))
    for i, (n, a, b) in enumerate(cards):
        x0 = 170 + i * 820; rot = (-1.6, 1.3)[i]
        card = Image.new('RGBA', (760, 560), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
        cd.rectangle((0, 0, 760, 560), fill=(246, 239, 220))
        T(cd, (380, 110), n, 72, OR, F_X); T(cd, (380, 290), a, 62, INK, F_B); T(cd, (380, 400), b, 62, INK, F_X)
        card = card.rotate(rot, expand=True, resample=Image.BICUBIC)
        sh = Image.new('L', card.size, 0); sh.paste(card.split()[3].point(lambda v: 70 if v else 0)); sh = sh.filter(ImageFilter.GaussianBlur(8))
        im.paste((150, 146, 140), (x0 + 8, 270 + 10), sh); im.paste(card, (x0, 270), card)
    d = ImageDraw.Draw(im)
    hand_under(d, 170 + 820 + 120, 170 + 820 + 640, 270 + 450, seed=4)

@board
def k1_us_kr_1y(im):
    d = ImageDraw.Draw(im); title(d, '1년 동안 오른 폭 (10년 국채, 월평균)', 100)
    bars(im, [('미국', 0.42, KRAFT, '+0.4%p', INK), ('한국', 1.47, OR, '+1.5%p', OR)], vmax=1.8, top_y=300)
    T(d, (W // 2, 200), '한국이 세 배 넘게', 58, INK, F_X)
    source(d, '2025년 8월 → 2026년 8월 · FRED · 한국은행')

@board
def k1_us_kr_sep(im):
    d = ImageDraw.Draw(im); title(d, '9월까지 넣으면', 100)
    base, top = 860, 300; vmax = 1.8; bw, gap = 260, 200; x = (W - (2 * bw + gap)) // 2
    for i, (lab, v8, v9) in enumerate((('미국', 0.42, 0.87), ('한국', 1.47, 1.61))):
        h8 = (base - top) * v8 / vmax; h9 = (base - top) * v9 / vmax
        torn(im, (x, base - h9, x + bw, base - h8 + 4), (KRAFT_L if i == 0 else (255, 170, 120)), seed=70 + i)
        torn(im, (x, base - h8, x + bw, base), KRAFT if i == 0 else OR, seed=72 + i, shadow=False); d = ImageDraw.Draw(im)
        T(d, (x + bw // 2, base - h9 - 64), f'+{v9:.2f}%p'.replace('0.87', '0.9').replace('1.61', '1.6'), 84, OR if i == 1 else INK, F_X)
        T(d, (x + bw // 2, base + 60), lab, 46)
        x += bw + gap
    source(d, '연한 칸 = 9월에 더해진 몫 · 2025년 9월 → 2026년 9월 월평균')

@board
def k1_samedir(im):
    d = ImageDraw.Draw(im); title(d, '정기예금과 같은 쪽으로 움직인 달 — 열 달에', 100)
    ms = [m for m in sorted(SER['dep1']) if '201301' <= m <= '202608']
    ch = lambda k: [SER[k][ms[i]] - SER[k][ms[i - 1]] for i in range(1, len(ms))]
    sg = lambda v: (v > 1e-9) - (v < -1e-9)
    dep = ch('dep1'); n1 = sum(sg(a) * sg(b) == 1 for a, b in zip(dep, ch('kr3'))); n2 = sum(sg(a) * sg(b) == 1 for a, b in zip(dep, ch('us_m'))); N = len(dep)
    for j, (lab, n, col, word) in enumerate((('한국 3년 국채', n1, OR, '거의 일곱 달'), ('미국 10년 국채', n2, INK, '다섯 달 남짓'))):
        y = 330 + j * 330; frac = n / N * 10
        T(d, (200, y), lab, 54, col, F_B, 'lm')
        for k in range(10):
            cx = 640 + k * 104; r = 40; f = max(0.0, min(1.0, frac - k))
            if f > 0:
                m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).ellipse((cx - r, y - r, cx + r, y + r), fill=255)
                m2 = Image.new('L', (W, H), 0); ImageDraw.Draw(m2).rectangle((cx - r, y - r, cx - r + 2 * r * f, y + r), fill=255)
                from PIL import ImageChops
                im.paste(col, (0, 0), ImageChops.multiply(m, m2)); d = ImageDraw.Draw(im)
            d.ellipse((cx - r, y - r, cx + r, y + r), outline=col if f > 0 else (170, 164, 156), width=4)
        T(d, (640 - r, y + 100), f'{word} · {N}달 중 {n}달', 48, col, F_X, 'lm')
    source(d, '2013년 1월~2026년 8월 달마다 오르내림 · 같이 움직였다는 뜻, 원인은 아님')

@board
def k1_base_steps(im):
    d = ImageDraw.Draw(im); title(d, '한국은행 기준금리', 100)
    steps = (('2025.5.29', 2.50), ('2026.7.16', 2.75), ('2026.8.27', 3.00))
    x = 360; base = 860
    for i, (dt, v) in enumerate(steps):
        h = 180 + i * 170
        torn(im, (x, base - h, x + 400, base), OR if i == 2 else KRAFT, seed=80 + i); d = ImageDraw.Draw(im)
        T(d, (x + 200, base - h - 64), f'{v:.2f}%', 80, OR if i == 2 else INK, F_X)
        T(d, (x + 200, base + 50), dt, 38, GREY, F_M)
        x += 400
    source(d, '한국은행 통화정책방향 · 1년 새 두 번 올림')

@board
def k1_2023(im):
    im.paste(canvas(sepia=True)); d = ImageDraw.Draw(im); col = (120, 100, 76)
    T(d, (W // 2, 100), '2023년 가을, 정기예금 1년 평균', 62, col)
    pts = months('dep1', '202306', '202406'); vals = [v for _, v in pts]; ms = [m for m, _ in pts]
    box = (260, 230, 1660, 840)
    xl = [(i, f"{m[2:4]}.{m[4:]}") for i, m in enumerate(ms) if m[4:] in ('06', '09', '12', '03', '06')]
    X, Y = linechart(im, [vals], box, 3.2, 4.4, [col], [7], xl, yfmt='{:.1f}%', yticks=(3.4, 3.8, 4.2))
    i = ms.index('202311'); j = ms.index('202402')
    hand_ellipse(d, (X(i) - 90, Y(4.18) - 90, X(i) + 90, Y(4.18) + 70), color=OR, seed=91)
    T(d, (X(i), Y(4.18) - 130), '11월 4.2%', 54, OR, F_X)
    T(d, (X(j) + 40, Y(3.63) + 80), '석 달 뒤 3.6%', 48, col, F_X)
    source(d, '한국은행 · 예금은행 정기예금 1년(신규취급액)')

def flow_box(im, box, lines, seed, color=KRAFT_L):
    torn(im, box, color, seed=seed); d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = box; cy = (y0 + y1) / 2 - (len(lines) - 1) * 40
    for k, (s, size, col, f) in enumerate(lines): T(d, ((x0 + x1) / 2, cy + k * 80), s, size, col, f)

@board
def k1_reset_flow(im):
    d = ImageDraw.Draw(im); title(d, '2021년 여름, 3억원 · 30년 · 5년 고정', 100)
    flow_box(im, (100, 260, 600, 640), (('2021년', 44, GREY, F_B), ('고정 2.98%', 56, INK, F_X), ('한 달 126만원', 52, INK, F_B)), 101)
    flow_box(im, (710, 260, 1210, 640), (('5년 뒤', 44, GREY, F_B), ('남은 원금', 50, INK, F_B), ('2억 6,662만원', 52, INK, F_X)), 102)
    flow_box(im, (1320, 260, 1820, 640), (('지금 고정형', 44, GREY, F_B), ('4.88% · 25년', 54, INK, F_X), ('한 달 154만원', 52, INK, F_B)), 103)
    d = ImageDraw.Draw(im)
    hand_arrow(d, (612, 450), (698, 450)); hand_arrow(d, (1222, 450), (1308, 450))
    T(d, (W // 2, 820), '2021년보다 한 달 28만원 정도 더', 96, OR, F_X)
    source(d, '평균 금리로 셈한 가정 · 원리금균등 · 실제 금리는 은행·상품마다 다름')

@board
def k1_reset_two(im):
    d = ImageDraw.Draw(im); title(d, '5년 고정이 끝나고 다시 정하면', 100)
    flow_box(im, (140, 380, 640, 700), (('2021년', 44, GREY, F_B), ('한 달 126만원', 54, INK, F_X)), 111)
    flow_box(im, (1080, 200, 1780, 500), (('고정형 4.88%', 48, INK, F_B), ('154만원 · +28만원', 60, INK, F_X)), 112)
    flow_box(im, (1080, 580, 1780, 880), (('변동형 4.53%', 48, INK, F_B), ('149만원 · +22만원', 60, OR, F_X)), 113)
    d = ImageDraw.Draw(im)
    hand_arrow(d, (660, 520), (1060, 360)); hand_arrow(d, (660, 560), (1060, 730))
    source(d, '2021년 대비 한 달 · 남은 원금 2억 6,662만원 · 25년 원리금균등 · 평균 금리 가정')

@board
def k1_check3(im):
    d = ImageDraw.Draw(im); title(d, '약정서·통장에서 날짜 한 줄 찾기', 110)
    rows = (('변동형 대출', '금리가 다시 정해지는 날'), ('고정형 대출', '고정이 끝나는 날'), ('정기예금', '만기일'))
    for i, (a, b) in enumerate(rows):
        y = 320 + i * 170
        d.rectangle((300, y - 42, 384, y + 42), outline=INK, width=6)
        hand_check(d, 312, y, 70, OR, 11)
        T(d, (440, y), a, 60, INK, F_X, 'lm'); T(d, (900, y), b, 58, INK, F_B, 'lm')
    T(d, (W // 2, 880), '다음 코픽스 발표 11월 16일', 64, OR, F_X)
    source(d, '은행연합회 · 매달 15일 무렵 발표')

@board
def k1_calendar(im):
    """벽에 건 달력 한 장(2026년 8월, 요일 실제) · 한 칸에 손 동그라미 — 날짜 자체는 예시, 숫자 주장 없음."""
    import calendar as C
    d = ImageDraw.Draw(im)
    torn(im, (430, 70, 1490, 1020), (252, 251, 247), seed=120); d = ImageDraw.Draw(im)
    for hx in (760, 1160): d.ellipse((hx - 16, 92, hx + 16, 124), fill=(70, 70, 74))
    T(d, (960, 205), '8', 120, INK, F_X); T(d, (1060, 220), '2026', 40, GREY, F_B, 'lm')
    days = '일월화수목금토'; x0, y0, cw, rh = 500, 330, 132, 112
    for k, ch in enumerate(days): T(d, (x0 + k * cw + cw // 2, y0), ch, 36, OR if k == 0 else GREY, F_B)
    cal = C.Calendar(firstweekday=6).monthdayscalendar(2026, 8)
    for r, wk in enumerate(cal):
        y = y0 + 70 + r * rh; d.line([(x0, y - 50), (x0 + 7 * cw, y - 50)], fill=(214, 210, 202), width=2)
        for k, dd in enumerate(wk):
            if dd: T(d, (x0 + k * cw + cw // 2, y), str(dd), 48, OR if k == 0 else INK, F_B)
    # 손 동그라미 + 손글씨 꼬리
    r, k = next((r, k) for r, wk in enumerate(cal) for k, dd in enumerate(wk) if dd == 20)
    cx, cy = x0 + k * cw + cw // 2, y0 + 70 + r * rh
    hand_ellipse(d, (cx - 70, cy - 52, cx + 70, cy + 52), color=(214, 40, 30), width=9, seed=121)
    T(d, (1530, cy + 150), '고정 끝', 58, (214, 40, 30), F_X, 'lm')
    hand_arrow(d, (1520, cy + 140), (cx + 72, cy + 30), (214, 40, 30), 6)

@board
def k1_passbook(im):
    """2장 시작: 펼친 종이 통장(은행 이름 없음, 칸 머리만 실제 말, 거래 줄은 비움) + 장 제목. 4차 심사 'AI 통장이 지갑으로 보임' → 종이 그림으로."""
    d = ImageDraw.Draw(im)
    T(d, (W // 2, 130), '내 예금 이자는', 84, INK, F_X); T(d, (W // 2, 240), '얼마나 따라왔나', 84, OR, F_X)
    x0, y0, x1, y1 = 300, 340, 1620, 960; mid = (x0 + x1) // 2
    torn(im, (x0, y0, x1, y1), (236, 243, 246), seed=130, shadow=True); d = ImageDraw.Draw(im)
    d.line([(mid, y0 + 6), (mid, y1 - 6)], fill=(170, 186, 196), width=4)
    heads = ('날짜', '찾으신 금액', '맡기신 금액', '잔액')
    for side in (0, 1):
        sx = x0 + 40 + side * (mid - x0); cw = (mid - x0 - 80) / 4
        for k, h in enumerate(heads): T(d, (sx + cw * k + cw / 2, y0 + 60), h, 25, (70, 96, 116), F_B)
        for r in range(9):
            y = y0 + 100 + r * 54; d.line([(sx, y), (sx + cw * 4, y)], fill=(180, 198, 208), width=2)
        for k in range(1, 4): d.line([(sx + cw * k, y0 + 36), (sx + cw * k, y0 + 100 + 8 * 54)], fill=(200, 214, 222), width=2)
    # 이자 줄 하나에 손 밑줄(빈 칸 — 숫자는 다음 장면에서)
    T(d, (x0 + 40 + (mid - x0 - 80) / 8, y0 + 100 + 5 * 54 + 27), '이자', 34, OR, F_X)
    hand_under(d, x0 + 40, mid - 40, y0 + 100 + 6 * 54 + 4, seed=131)

def main(names):
    os.makedirs(OUT, exist_ok=True)
    for n in names or list(B):
        im = canvas(); B[n](im); im.save(os.path.join(OUT, n + '.png')); print(n)

if __name__ == '__main__':
    main(sys.argv[1:])
