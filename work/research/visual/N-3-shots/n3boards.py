"""N-3 장면 판 — visual-designer 2026-11-01. P-3 p3boards.py·K-1 k1boards.py와 같은 꼴·같은 부품.
구겨진 종이 바탕 · 찢은 종이 조각 · 주황 #FF5A00은 그 화면의 답 하나 · 손으로 그린 동그라미·밑줄 · 가운데 맞춤.
숫자는 ep/N-3/calc_out.txt 값만, 말은 say_v1.txt 그대로(357만원쯤·앞에서 서른세 명 안 등). 판은 '답이 열린 마지막 모습'.
1회차(11/1 19시): 0~2장 판 10장(r02·r03·r04·r06·r07·r08·r10·r11·r12·r14).
2회차(11/1 23시): 3~7장 판 15장(r16·r17·r21~25·r27·r29·r31~34·r36·r38). r18·r28은 motion PayBlocks·RaiseStairs가 맡음.
사용: py -3.12 n3boards.py [이름 ...]   (없으면 전부) → work/video/public/bg/n3/board/<이름>.png
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'K-1-shots'))
import k1boards as K
from k1boards import (W, H, INK, GREY, OR, KRAFT, KRAFT_L, FADE, F_B, F_M, F_X, font, canvas, T, title, source,
                      torn, hand_ellipse, hand_under, hand_check, hand_arrow)
from PIL import ImageDraw

OUT = os.path.join(K.WORK, 'video', 'public', 'bg', 'n3', 'board')
PAPER_N = (238, 230, 212); MEMO = (246, 236, 178); PALE = (250, 248, 242)
COND = '1인 · 식대 비과세 월 20만원 · 2026년 보험료율·간이세액표'
SRC_NTS = '국세청 2024년 귀속 근로소득 백분위(1%씩 묶은 구간 평균 총급여)'
B = {}
def board(fn):
    B[fn.__name__] = fn; return fn

def width(s, size, f=F_X): return font(f, size).getlength(s)

def person(d, cx, top, h, color, r=None):
    """줄 선 사람 — 머리 동그라미 + 몸 둥근 기둥(얼굴 없음)."""
    r = r or h * 0.17
    d.ellipse((cx - r, top, cx + r, top + 2 * r), fill=color)
    d.rounded_rectangle((cx - r * 1.25, top + 2 * r + 4, cx + r * 1.25, top + h), radius=int(r), fill=color)

# ── 0장 ──
@board
def n3_hook357(im):
    d = ImageDraw.Draw(im)
    T(d, (W // 2, 330), '연봉 5,000만원', 120, INK, F_X)
    hand_arrow(d, (W // 2, 440), (W // 2, 560), INK, 8)
    T(d, (W // 2, 650), '통장에 한 달', 72, INK, F_B)
    s = '357만원쯤'; T(d, (W // 2, 800), s, 150, OR, F_X)
    hand_under(d, W // 2 - width(s, 150) / 2, W // 2 + width(s, 150) / 2, 895, seed=21)
    source(d, COND)

@board
def n3_line100_33(im):
    d = ImageDraw.Draw(im); title(d, '직장인 100명을 연봉 순으로 줄 세우면', 120)
    x0, x1 = 150, 1770; step = (x1 - x0) / 49; h = 120; r = step * 0.3
    for i in range(100):
        row, k = divmod(i, 50); cx = x0 + k * step; top = 300 + row * 190
        person(d, cx, top, h, OR if i < 33 else (172, 164, 152), r)
    hand_under(d, x0 - 10, x0 + 32 * step + 10, 300 + h + 22, OR, 8, seed=31)
    T(d, (x0, 270), '연봉 높은 쪽', 36, GREY, F_M, 'lm'); T(d, (x1, 270), '낮은 쪽', 36, GREY, F_M, 'rm')
    T(d, (x0 + 16 * step, 780), '앞에서 33명 안', 96, OR, F_X)
    T(d, (x0 + 41 * step, 780), '연봉 5천은 여기', 56, INK, F_B)
    hand_arrow(d, (x0 + 33 * step, 760), (x0 + 32.3 * step, 440), INK, 6)
    T(d, (W // 2, 910), '상위 33% 안쪽이라는 뜻이에요', 52, INK, F_B)
    source(d, SRC_NTS)

@board
def n3_toc(im):
    d = ImageDraw.Draw(im); title(d, '오늘 볼 것', 130)
    rows = ('연봉 3천에서 1억까지 일곱 칸', '천만원 올라도 통장이 가장 덜 느는 칸', '거꾸로 — 통장 300만원이 되려면', '같은 연봉, 다른 통장 두 가지')
    torn(im, (380, 230, 1540, 940), PALE, seed=40); d = ImageDraw.Draw(im)
    for i, s in enumerate(rows):
        y = 340 + i * 160
        d.rectangle((470, y - 36, 542, y + 36), outline=INK, width=5)
        T(d, (590, y), s, 62, INK, F_B, 'lm')

# ── 1장 ──
@board
def n3_three_money(im):
    d = ImageDraw.Draw(im); title(d, "'연봉'은 세 가지 돈", 120)
    cards = (('계약서 연봉', '세전', '떼기 전 돈'), ('국세청 총급여', '줄 세울 때', '상여 넣고 식대 뺌'), ('통장', '세후', '다 뗀 돈'))
    for i, (a, b, c) in enumerate(cards):
        x0 = 170 + i * 560; torn(im, (x0, 330, x0 + 460, 820), PAPER_N if i == 1 else KRAFT_L, seed=60 + i); d = ImageDraw.Draw(im)
        T(d, (x0 + 230, 440), b, 48, GREY, F_B)
        T(d, (x0 + 230, 570), a, 64 if i == 1 else 72, OR if i == 1 else INK, F_X)
        T(d, (x0 + 230, 710), c, 46, INK, F_B)
        if i < 2: hand_arrow(d, (x0 + 475, 575), (x0 + 545, 575), INK, 7)
    hand_ellipse(d, (170 + 560 - 30, 480, 170 + 560 + 490, 660), seed=64)
    T(d, (W // 2, 930), '내 자리는 원천징수영수증의 총급여로 찾아요', 52, INK, F_B)

@board
def n3_4760(im):
    d = ImageDraw.Draw(im); title(d, '식대를 한 달 20만원 받는 회사라면', 120)
    T(d, (W // 2, 330), '연봉 5,000만원', 90, INK, F_X)
    T(d, (W // 2, 470), '− 식대 240만원 (한 해)', 72, INK, F_B)
    d.line([(560, 560), (1360, 560)], fill=INK, width=6)
    torn(im, (560, 610, 1360, 880), PALE, seed=70); d = ImageDraw.Draw(im)
    T(d, (W // 2, 670), '원천징수영수증 · 총급여', 42, GREY, F_B)
    s = '4,760만원'; T(d, (W // 2, 790), s, 120, OR, F_X)
    hand_ellipse(d, (W // 2 - width(s, 120) / 2 - 70, 705, W // 2 + width(s, 120) / 2 + 70, 880), seed=71)
    T(d, (W // 2, 960), '국세청 줄에는 이 숫자로 섭니다', 50, INK, F_B)

@board
def n3_percentile_box(im):
    d = ImageDraw.Draw(im); title(d, '국세청은 100명 중 1명씩 묶은 칸의 평균만 알려 줘요', 120)
    labs = (('상위 31%', ''), ('상위 32%', '4,837만'), ('상위 33%', '4,737만'), ('상위 34%', ''))
    bw = 360; gap = 60; x = (W - (4 * bw + 3 * gap)) // 2; xs = []
    for i, (a, b) in enumerate(labs):
        torn(im, (x, 330, x + bw, 700), KRAFT_L, seed=80 + i); d = ImageDraw.Draw(im)
        person(d, x + bw // 2 - 70, 370, 190, (150, 140, 126), 28)
        d.line([(x + bw // 2, 580), (x + bw // 2, 660)], fill=INK, width=4)
        d.polygon([(x + bw // 2, 580), (x + bw // 2 + 60, 600), (x + bw // 2, 620)], fill=INK)
        T(d, (x + bw // 2, 760), a, 44, GREY, F_B); T(d, (x + bw // 2, 830), ('평균 ' + b + '원') if b else '평균 …', 52, INK if b else FADE, F_X)
        xs.append(x); x += bw + gap
    mx = xs[2] - gap // 2
    d.ellipse((mx - 26, 600 - 26, mx + 26, 600 + 26), fill=OR)
    T(d, (mx, 950), '연봉 5천(총급여 4,760만)은 이 두 칸 사이', 54, OR, F_X)
    hand_arrow(d, (mx, 900), (mx, 650), OR, 7)
    source(d, SRC_NTS)

# ── 2장 사다리 ──
LAD = (('3천', '224만원', '62명'), ('4천', '294만원', '45명'), ('5천', '357만원', '33명'), ('6천', '420만원', '25명'),
       ('7천', '482만원', '19명'), ('8천', '537만원', '15명'), ('1억', '653만원', '9명'), ('1억 2천', '761만원', '6명'), ('1억 5천', '902만원', '3명'))

def ladder(im, rows, hi, grey=(), y0=260, rh=86, ttl='연봉 사다리'):
    d = ImageDraw.Draw(im); title(d, ttl, 110)
    cx = (420, 960, 1500)
    for k, h in enumerate(('연봉', '통장 한 달', '100명 중 앞에서')): T(d, (cx[k], y0 - 50), h, 44, GREY, F_B)
    d.line([(220, y0 - 20), (1700, y0 - 20)], fill=INK, width=4)
    for i, r in enumerate(rows):
        y = y0 + 40 + i * rh; idx = LAD.index(r)
        col = FADE if idx in grey else (OR if idx == hi else INK)
        T(d, (cx[0], y), '연봉 ' + r[0], 54, col, F_X); T(d, (cx[1], y), r[1], 60, col, F_X); T(d, (cx[2], y), r[2] + ' 안', 54, col, F_X)
        if idx == hi: hand_ellipse(d, (cx[1] - 200, y - 50, cx[1] + 200, y + 50), seed=90 + i)
    return d

@board
def n3_ladder_a(im):
    ladder(im, LAD[:4], 3, y0=300, rh=130)
    source(ImageDraw.Draw(im), COND + ' · 줄 위치는 국세청 2024년 귀속')

@board
def n3_ladder_b(im):
    ladder(im, LAD[:7], 6, grey=(0, 1, 2, 3), y0=260, rh=100)
    source(ImageDraw.Draw(im), COND + ' · 줄 위치는 국세청 2024년 귀속')

@board
def n3_ladder_c(im):
    d = ladder(im, LAD[6:], -1, grey=(6,), y0=300, rh=140, ttl='1억 위 두 칸')
    T(d, (W // 2, 850), '세전 월급에서 통장에 남는 몫', 54, INK, F_B)
    s = '72%까지 내려와요'; T(d, (W // 2, 950), s, 72, OR, F_X)
    source(d, COND)

@board
def n3_share_bars(im):
    d = ImageDraw.Draw(im); title(d, '세전 월급 중 통장에 남는 몫', 110)
    vals = (('3천', 89.8), ('4천', 88.1), ('5천', 85.7), ('6천', 83.9), ('7천', 82.7), ('8천', 80.5), ('1억', 78.4))
    base, top = 820, 260; lo, hi = 70, 92; Y = lambda v: base - (base - top) * (v - lo) / (hi - lo)
    bw, gap = 170, 70; x = (W - (7 * bw + 6 * gap)) // 2
    for i, (a, v) in enumerate(vals):
        last = i == 6
        torn(im, (x, Y(v), x + bw, base), OR if last else KRAFT_L, seed=110 + i); d = ImageDraw.Draw(im)
        T(d, (x + bw // 2, Y(v) - 44), f'{int(v + 0.5)}%', 56, OR if last else INK, F_X)
        T(d, (x + bw // 2, base + 48), a, 46, INK, F_B)
        if i == 0: lx = x
        x += bw + gap
    hand_ellipse(d, (x - gap - bw - 40, Y(78.4) - 100, x - gap + 40, Y(78.4) + 40), seed=118)
    T(d, (W // 2, 960), '연봉이 오를수록 떼어 가는 돈이 커져요', 52, INK, F_B)
    source(d, COND + ' · 70% 아래는 잘라 그림')

# ── 3장 어디서 빠지나 (2회차 11/1 23시) ──
@board
def n3_waterfall(im):
    d = ImageDraw.Draw(im); title(d, '연봉 5천, 세전 월급에서 빠지는 돈', 110)
    steps = (('국민연금', 188380, '19만'), ('건강보험', 142600, '14만'), ('장기요양', 18730, '2만'), ('고용보험', 35690, '4만'),
             ('소득세', 190620, '19만'), ('지방소득세', 19060, '2만'))
    pre, net = 4166666, 3571586
    lo, hi, base, top = 3000000, 4200000, 850, 250
    Y = lambda v: base - (base - top) * (v - lo) / (hi - lo)
    n = 8; bw = 150; gap = (1680 - n * bw) / (n - 1); X = lambda i: 120 + i * (bw + gap)
    torn(im, (X(0), Y(pre), X(0) + bw, base), KRAFT_L, seed=160); d = ImageDraw.Draw(im)
    T(d, (X(0) + bw / 2, Y(pre) - 76), '세전 월', 36, GREY, F_B); T(d, (X(0) + bw / 2, Y(pre) - 32), '417만원', 44, INK, F_X)
    cur = pre
    for i, (a, v, lab) in enumerate(steps, 1):
        nxt = cur - v; d.line([(X(i - 1) + bw, Y(cur)), (X(i), Y(cur))], fill=GREY, width=3)
        torn(im, (X(i), Y(cur), X(i) + bw, max(Y(nxt), Y(cur) + 10)), FADE, seed=160 + i, shadow=False); d = ImageDraw.Draw(im)
        T(d, (X(i) + bw / 2, Y(cur) - 34), '−' + lab, 42, INK, F_X)
        T(d, (X(i) + bw / 2, base + 46), a, 34 if len(a) < 5 else 30, INK, F_B)
        cur = nxt
    d.line([(X(6) + bw, Y(net)), (X(7), Y(net))], fill=GREY, width=3)
    torn(im, (X(7), Y(net), X(7) + bw, base), OR, seed=169); d = ImageDraw.Draw(im)
    T(d, (X(0) + bw / 2, base + 46), '세전', 34, INK, F_B); T(d, (X(7) + bw / 2, base + 46), '통장', 38, OR, F_X)
    T(d, (X(7) + bw / 2, Y(net) - 40), '357만원', 46, OR, F_X)
    s = '다 합치면 60만원쯤'; T(d, (1180, 700), s, 58, INK, F_X)
    hand_under(d, 1180 - width(s, 58) / 2, 1180 + width(s, 58) / 2, 745, INK, 6, seed=170)
    source(d, COND + ' · 300만원 아래는 잘라 그림')

def donut(d, c, r, frac, col_a, col_b, w=70):
    box = (c[0] - r, c[1] - r, c[0] + r, c[1] + r)
    d.arc(box, -90, -90 + 360 * frac, fill=col_a, width=w); d.arc(box, -90 + 360 * frac, 270, fill=col_b, width=w)

@board
def n3_donuts(im):
    d = ImageDraw.Draw(im); title(d, '빠지는 돈 중 세금은 얼마나?', 110)
    for i, (lab, tot, tax, fr) in enumerate((('연봉 3천', '26만원', '3만원', 0.125), ('연봉 1억', '180만원', '109만원', 0.602))):
        cx = 560 + i * 800; cy = 500; hi = i == 1
        donut(d, (cx, cy), 210, fr, OR, KRAFT_L)
        T(d, (cx, cy - 30), '빠지는 돈', 36, GREY, F_B); T(d, (cx, cy + 30), tot, 64, INK, F_X)
        T(d, (cx, 790), lab, 56, INK, F_X)
        s = '그중 세금 ' + tax; T(d, (cx, 880), s, 52, OR if hi else INK, F_X)
        if hi: hand_under(d, cx - width(s, 52) / 2, cx + width(s, 52) / 2, 925, seed=171)
    for j, (c, t) in enumerate(((OR, '세금'), (KRAFT_L, '보험료'))):
        lx = W // 2 - 190 + j * 220; d.rectangle((lx, 975, lx + 36, 1011), fill=c); T(d, (lx + 52, 993), t, 40, INK, F_B, 'lm')
    source(d, COND)

# ── 4장 1천만원 오를 때 ──
@board
def n3_x18(im):
    d = ImageDraw.Draw(im); title(d, '연봉이 두 배가 되면', 110)
    T(d, (520, 360), '연봉', 54, GREY, F_B); T(d, (520, 480), '5천 → 1억', 96, INK, F_X); T(d, (520, 640), '× 2', 150, INK, F_X)
    T(d, (1400, 360), '통장 한 달', 54, GREY, F_B); T(d, (1400, 480), '357만 → 653만', 84, INK, F_X)
    s = '× 1.8'; T(d, (1400, 640), s, 150, OR, F_X)
    hand_ellipse(d, (1400 - width(s, 150) / 2 - 60, 550, 1400 + width(s, 150) / 2 + 60, 740), seed=181)
    d.line([(W // 2 + 20, 330), (W // 2 + 20, 760)], fill=FADE, width=4)
    T(d, (W // 2, 900), '통장은 1.8배쯤밖에 안 됩니다', 60, INK, F_B)
    source(d, COND)

RAISE = (('3천 → 4천', '69만원', '83.0%'), ('4천 → 5천', '64만원', '76.3%'), ('5천 → 6천', '62만원', '74.9%'),
         ('6천 → 7천', '63만원', '75.1%'), ('7천 → 8천', '55만원', '65.5%'), ('8천 → 1억(+2천만)', '116만원', '69.8%'))

def raise_table(im, hi, note=None):
    d = ImageDraw.Draw(im); title(d, '오른 돈 중 남는 몫', 110)
    cx = (480, 980, 1460); y0 = 240; rh = 100
    for k, h in enumerate(('오른 칸', '통장 한 달 더', '남는 몫')): T(d, (cx[k], y0), h, 44, GREY, F_B)
    d.line([(240, y0 + 40), (1680, y0 + 40)], fill=INK, width=4)
    for i, (a, b, c) in enumerate(RAISE):
        y = y0 + 100 + i * rh; col = OR if i == hi else INK
        T(d, (cx[0], y), '연봉 ' + a, 50, col, F_X); T(d, (cx[1], y), b, 56, col, F_X); T(d, (cx[2], y), c, 56, col, F_X)
        if i == hi: hand_ellipse(d, (cx[2] - 150, y - 48, cx[2] + 150, y + 48), seed=190 + i)
    if note: T(d, (W // 2, 970), note, 48, INK, F_B)
    source(d, COND)
    return d

@board
def n3_raise_table(im): raise_table(im, 4, '오른 돈의 삼분의 이 정도만 남는 칸')

@board
def n3_raise_table_b(im): raise_table(im, 5, '국민연금이 월 31만원에서 더 안 늘어서')

@board
def n3_taxsteps(im):
    d = ImageDraw.Draw(im); title(d, '소득세율 계단 — 넘는 부분에만 높은 세율', 110)
    rows = (('1,400만원 이하', '6%'), ('5,000만원 이하', '15%'), ('8,800만원 이하', '24%'), ('1억 5천만원 이하', '35%'))
    torn(im, (360, 210, 1560, 870), PALE, seed=230); d = ImageDraw.Draw(im)
    T(d, (W // 2, 285), '과세표준(연봉에서 이것저것 빼고 남은 돈)', 40, GREY, F_B)
    for i, (a, b) in enumerate(rows):
        y = 410 + i * 120; col = OR if i == 2 else INK
        T(d, (W // 2 + 30, y), a, 60, col, F_X, 'rm'); T(d, (W // 2 + 110, y), b, 66, col, F_X, 'lm')
        if i in (1, 2): hand_under(d, W // 2 + 30 - width(a, 60), W // 2 + 110 + width(b, 66), y + 44, (200, 30, 30), 6, seed=231 + i)
    T(d, (W // 2, 960), '5천만원을 넘는 부분에만 15% 대신 24%', 54, INK, F_B)
    source(d, '소득세법 제55조① 종합소득세율(우리 글씨로 옮김, 1억 5천 위 칸 생략)')

@board
def n3_raise_top(im):
    d = ImageDraw.Draw(im); title(d, '1억 위로 오를 때', 110)
    rows = (('1억 → 1억 2천', '108만원', '65%'), ('1억 2천 → 1억 5천', '141만원', '56%'))
    cx = (500, 1060, 1480)
    for k, h in enumerate(('오른 칸', '통장 한 달 더', '남는 몫')): T(d, (cx[k], 300), h, 44, GREY, F_B)
    d.line([(200, 345), (1720, 345)], fill=INK, width=4)
    for i, (a, b, c) in enumerate(rows):
        y = 470 + i * 170; col = OR if i == 1 else INK
        T(d, (cx[0], y), '연봉 ' + a, 54, col, F_X); T(d, (cx[1], y), b, 60, col, F_X); T(d, (cx[2], y), c, 84, col, F_X)
        if i == 1: hand_ellipse(d, (cx[2] - 140, y - 70, cx[2] + 140, y + 70), seed=251)
    T(d, (W // 2, 920), '연금은 이미 끝에 닿아 — 더 떼는 돈 대부분이 소득세', 50, INK, F_B)
    source(d, COND + ' · 1억 2천 → 1억 5천은 3천만원 오름')

# ── 5장 거꾸로 ──
@board
def n3_rev300(im):
    d = ImageDraw.Draw(im); title(d, '거꾸로 — 통장에 한 달 300만원이 찍히려면', 110)
    T(d, (1400, 470), '통장 월 300만원', 84, INK, F_X)
    hand_arrow(d, (1060, 470), (860, 470), INK, 8)
    s = '연봉 4,100만원쯤'; T(d, (500, 470), s, 84, OR, F_X)
    hand_under(d, 500 - width(s, 84) / 2, 500 + width(s, 84) / 2, 535, seed=271)
    T(d, (W // 2, 720), '백 명 중 앞에서 44명 안', 66, INK, F_X)
    T(d, (W // 2, 820), '한가운데보다 조금 앞', 48, GREY, F_B)
    source(d, COND + ' · 줄 위치는 국세청 2024년 귀속')

@board
def n3_rev_cond(im):
    d = ImageDraw.Draw(im); title(d, '같은 통장 금액, 조건 따라 필요한 연봉', 110)
    cols = ('1인 · 식대 있음', '식대 없음', '4인 · 자녀 2'); cx = (300, 760, 1200, 1640)
    rows = (('300만원', '4,100만', '4,170만', '3,970만'), ('400만원', '5,680만', '5,770만', '5,420만'), ('500만원', '7,330만', '7,460만', '7,000만'))
    T(d, (cx[0], 290), '통장 월', 44, GREY, F_B)
    for k, h in enumerate(cols): T(d, (cx[k + 1], 290), h, 44, GREY, F_B)
    d.line([(160, 335), (1780, 335)], fill=INK, width=4)
    for i, r in enumerate(rows):
        y = 440 + i * 170; hi = i == 1
        for k, v in enumerate(r): T(d, (cx[k], y), v, 60 if k else 54, OR if hi else INK, F_X)
    T(d, (cx[2], 440 + 170 + 58), '+90만', 40, INK, F_B); T(d, (cx[3], 440 + 170 + 58), '−260만', 40, INK, F_B)
    hand_under(d, cx[0] - 100, cx[3] + 110, 705, seed=291)
    source(d, '식대 비과세 월 20만원 · 4인 = 본인·배우자·8~20세 자녀 2 · 2026년 요율·간이세액표')

# ── 6장 같은 연봉, 다른 통장 ──
def bubble(im, box, text, size, seed):
    torn(im, box, PALE, seed=seed); d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = box; d.polygon([(x0 + 60, y1 - 2), (x0 + 110, y1 - 2), (x0 + 50, y1 + 46)], fill=PALE)
    T(d, ((x0 + x1) / 2, (y0 + y1) / 2), text, size, INK, F_B); return d

@board
def n3_nontax(im):
    d = ImageDraw.Draw(im); title(d, '같은 연봉 5천인데 통장이 다른 이유', 110)
    bubble(im, (180, 210, 900, 330), '실제로는 훨씬 적게 들어와요', 44, 311)
    d = bubble(im, (1000, 390, 1740, 510), '비과세가 없는 회사라 더 적어요', 44, 312)
    for i, (a, b) in enumerate((('식대 비과세 있음', '357만원'), ('식대 비과세 없음', '352만원'))):
        cx = 620 + i * 680; T(d, (cx, 660), a, 46, GREY, F_B); T(d, (cx, 760), b, 90, INK, F_X)
    s = '차이 월 4만 8,810원'; T(d, (W // 2, 920), s, 70, OR, F_X)
    hand_under(d, W // 2 - width(s, 70) / 2, W // 2 + width(s, 70) / 2, 970, seed=313)
    source(d, '1인 · 댓글은 우리 말로 줄임 · 2026년 요율·간이세액표')

@board
def n3_family(im):
    d = ImageDraw.Draw(im); title(d, '가족 수로도 달라져요', 110)
    cx = (420, 1000, 1540); g = (150, 140, 126)
    person(d, cx[1], 220, 150, g, 26)
    for dx, h in ((-120, 150), (-45, 150), (30, 100), (95, 100)): person(d, cx[2] + dx, 220 + (150 - h), h, g, 26 if h > 120 else 19)
    T(d, (cx[1], 420), '1인', 50, INK, F_X); T(d, (cx[2], 420), '본인·배우자·자녀 2', 46, INK, F_X)
    d.line([(220, 470), (1700, 470)], fill=INK, width=4)
    rows = (('연봉 5천', '357만원', '373만원', '+16만원'), ('연봉 1억', '653만원', '683만원', '+30만원'))
    for i, (a, b, c, e) in enumerate(rows):
        y = 570 + i * 200; hi = i == 1
        T(d, (cx[0], y), a, 58, INK, F_X); T(d, (cx[1], y), b, 62, INK, F_X); T(d, (cx[2], y), c, 62, INK, F_X)
        T(d, (cx[2], y + 88), e, 50, OR if hi else INK, F_X)
        if hi: hand_ellipse(d, (cx[2] - 150, y + 46, cx[2] + 150, y + 134), seed=321)
    source(d, '통장 한 달 · 자녀 8~20세 · 식대 비과세 월 20만원 · 2026년 요율·간이세액표')

@board
def n3_8020(im):
    d = ImageDraw.Draw(im); title(d, '연봉 1억, 달마다 떼는 세금을 고르면', 110)
    cols = (('덜 떼기', '80%', '675만원'), ('그대로', '100%', '653만원'), ('더 떼기', '120%', '631만원'))
    for i, (a, b, c) in enumerate(cols):
        cx = 460 + i * 500; hi = i == 0
        T(d, (cx, 300), a, 50, GREY, F_B); T(d, (cx, 420), b, 110, OR if hi else INK, F_X)
        T(d, (cx, 560), '통장 ' + c, 52, INK, F_X)
    T(d, (460, 670), '+22만원', 72, OR, F_X); hand_ellipse(d, (250, 340, 670, 500), seed=331)
    T(d, (460, 760), '연말정산 때 한꺼번에', 40, INK, F_B); T(d, (460, 810), '더 낼 수 있음', 40, INK, F_B)
    T(d, (W // 2, 950), '한 해 세금은 같고, 내는 때만 바뀌어요', 54, INK, F_B)
    source(d, '소득세법 시행령 제194조① · 1인 · 식대 비과세 월 20만원')

@board
def n3_trap_yearend(im):
    d = ImageDraw.Draw(im); title(d, '달마다 떼는 소득세는 미리 어림한 값', 110)
    cw, gap = 88, 10; x0 = 150
    for m in range(12):
        x = x0 + m * (cw + gap); torn(im, (x, 330, x + cw, 470), KRAFT_L, seed=340 + m, shadow=False); d = ImageDraw.Draw(im)
        T(d, (x + cw / 2, 365), f'{m + 1}월', 30, INK, F_B)
        d.ellipse((x + cw / 2 - 24, 405, x + cw / 2 + 24, 453), fill=(201, 160, 72), outline=INK, width=3)
        d.ellipse((x + cw / 2 - 14, 415, x + cw / 2 + 14, 443), outline=(150, 112, 40), width=3)
    xe = x0 + 12 * (cw + gap) + 40
    torn(im, (xe, 300, xe + 300, 500), PALE, seed=353); d = ImageDraw.Draw(im)
    T(d, (xe + 150, 400), '연말정산', 56, OR, F_X)
    hand_ellipse(d, (xe - 20, 290, xe + 320, 510), seed=354)
    hand_arrow(d, (xe + 150, 530), (xe + 20, 680), INK, 6); hand_arrow(d, (xe + 150, 530), (xe + 280, 680), INK, 6)
    T(d, (xe + 10, 740), '더 냄', 50, INK, F_X); T(d, (xe + 300, 740), '돌려받음', 50, INK, F_X)
    T(d, (x0 + 6 * (cw + gap), 560), '12달 동안 미리 뗌', 52, INK, F_B)
    T(d, (W // 2, 930), "오늘 본 통장 금액은 '보통 달' 금액이에요", 56, INK, F_B)

# ── 7장 평균과 상위 25% ──
@board
def n3_top25_10(im):
    d = ImageDraw.Draw(im); title(d, '앞에서 10번째, 25번째 사람의 통장', 110)
    x0, x1 = 150, 1770; step = (x1 - x0) / 49; h = 110; r = step * 0.3
    for i in range(100):
        row, k = divmod(i, 50); person(d, x0 + k * step, 330 + row * 170, h, (172, 164, 152), r)
    for n, hi in ((10, False), (25, True)):
        cx = x0 + (n - 1) * step; col = OR if hi else INK
        person(d, cx, 330, h, col, r)
        d.line([(cx, 310), (cx, 230)], fill=col, width=5); d.polygon([(cx, 230), (cx + 50, 245), (cx, 260)], fill=col)
    for cx, lab, tot, net, hi in ((x0 + 9 * step - 160, '앞에서 10번째', '총급여 9,117만원', '통장 616만원', False),
                                  (x0 + 24 * step + 360, '앞에서 25번째', '총급여 5,727만원', '통장 418만원', True)):
        T(d, (cx, 720), lab, 48, INK, F_X); T(d, (cx, 800), tot, 44, GREY, F_B); T(d, (cx, 890), net, 70, OR if hi else INK, F_X)
        if hi: hand_under(d, cx - width(net, 70) / 2, cx + width(net, 70) / 2, 940, seed=361)
    source(d, SRC_NTS + ' · 통장은 1인·식대 비과세 월 20만원')

@board
def n3_partyear(im):
    d = ImageDraw.Draw(im); title(d, '이 줄에는 몇 달만 일한 사람도 있어요', 110)
    x0, x1 = 150, 1770; step = (x1 - x0) / 49; h = 110; r = step * 0.3
    for k in range(50): person(d, x0 + k * step, 270, h, (172, 164, 152) if k < 44 else (222, 214, 200), r)
    hand_ellipse(d, (x0 + 43.4 * step, 240, x1 + 30, 410), seed=381)
    T(d, (x0, 430), '앞', 34, GREY, F_M, 'lm'); T(d, (x1, 430), '맨 뒤', 34, GREY, F_M, 'rm')
    cw = 92; gx = (W - 12 * cw - 11 * 8) // 2
    for m in range(12):
        x = gx + m * (cw + 8); torn(im, (x, 500, x + cw, 590), KRAFT if m < 2 else PALE, seed=390 + m, shadow=False); d = ImageDraw.Draw(im)
        T(d, (x + cw / 2, 545), f'{m + 1}', 30, INK, F_B)
    T(d, (W // 2, 645), '한 해 중 몇 달만 일해도 줄에 들어가요', 44, GREY, F_B)
    s = '맨 뒤 구간 평균 총급여 21만원'; T(d, (W // 2, 780), s, 72, OR, F_X)
    hand_under(d, W // 2 - width(s, 72) / 2, W // 2 + width(s, 72) / 2, 835, seed=382)
    T(d, (W // 2, 940), "'일 년 내내 일한 직장인 중 몇 번째'와는 조금 달라요", 48, INK, F_B)
    source(d, SRC_NTS + ' · 2,108만 명')

def main(names):
    os.makedirs(OUT, exist_ok=True)
    for n in names or list(B):
        im = canvas(); B[n](im); im.save(os.path.join(OUT, n + '.png')); print(n)

if __name__ == '__main__':
    main(sys.argv[1:])
