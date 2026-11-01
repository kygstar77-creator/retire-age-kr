"""N-3 장면 판 — visual-designer 2026-11-01. P-3 p3boards.py·K-1 k1boards.py와 같은 꼴·같은 부품.
구겨진 종이 바탕 · 찢은 종이 조각 · 주황 #FF5A00은 그 화면의 답 하나 · 손으로 그린 동그라미·밑줄 · 가운데 맞춤.
숫자는 ep/N-3/calc_out.txt 값만, 말은 say_v1.txt 그대로(357만원쯤·앞에서 서른세 명 안 등). 판은 '답이 열린 마지막 모습'.
1회차(11/1 19시): 0~2장 판 10장(r02·r03·r04·r06·r07·r08·r10·r11·r12·r14).
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

def main(names):
    os.makedirs(OUT, exist_ok=True)
    for n in names or list(B):
        im = canvas(); B[n](im); im.save(os.path.join(OUT, n + '.png')); print(n)

if __name__ == '__main__':
    main(sys.argv[1:])
