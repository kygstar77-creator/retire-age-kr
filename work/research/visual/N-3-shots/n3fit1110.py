"""N-3 판 bgcheck 맞춤 — visual-designer 2026-11-10 17시(backlog ①: `py -3.12 work/boardcheck.py n3` 36장 중 33장 걸림).
P-3 p3fit1109·K-1 11/8과 같은 법: ① 그 화면의 답 하나를 130~150px(bgcheck ④ 9%↑) ② 찢은 종이 칸·네모 칸 빼고 종이 위에 바로
(⑥ UI 상자 1 이하) ③ 표의 한 줄은 한 글줄로 붙여 글자 줄 8 이하 ④ 급여명세서 그림은 줄 글씨 대신 회색 손 줄(읽을 글은 합계·실지급액만).
판 이름·크기(1920×1080) 그대로, 숫자는 옛 판(n3boards·n3fix1104 = calc_out.txt) 값 그대로 — 새 숫자 0.
사용: py -3.12 n3fit1110.py [이름 ...] → work/video/public/bg/n3/board/<이름>.png   검사: py -3.12 work/boardcheck.py n3
"""
import os, sys, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', 'K-1-shots'))
import k1boards as K
from k1boards import (W, H, INK, GREY, OR, KRAFT, KRAFT_L, FADE, F_B, F_M, F_X, font, canvas, T, TF, title, source,
                      torn, hand_ellipse, hand_under, hand_arrow)
from PIL import Image, ImageDraw
from n3boards import person, donut, LAD, RAISE

OUT = os.path.join(K.WORK, 'video', 'public', 'bg', 'n3', 'board')
PALE = (250, 248, 242); MEMO = (246, 236, 178); LINE = (170, 162, 150); SCRIB = (206, 199, 188)
COND = '1인 · 식대 비과세 월 20만원 · 2026년 보험료율·간이세액표'
SRC_NTS = '국세청 2024년 귀속 근로소득 백분위(1%씩 묶은 구간 평균 총급여)'
def wd(s, size, f=F_X): return font(f, size).getlength(s)
B = {}
def board(fn): B[fn.__name__] = fn; return fn

def big(d, xy, s, size=150, color=OR, under=True, seed=1, maxw=1760, ucolor=OR):
    size = TF(d, xy, s, size, color, F_X, maxw=maxw)
    if under: w = wd(s, size); hand_under(d, xy[0] - w / 2, xy[0] + w / 2, xy[1] + size * 0.55, ucolor, seed=seed)
    return size

def payslip(im, x0, y0, x1, seed, hi=None):
    """급여명세서 — 항목 줄은 회색 손 줄(글씨 아님), 읽히는 글은 제목·지급 합계·실지급액 셋. hi='gross'|'net'이면 주황 동그라미."""
    torn(im, (x0, y0, x1, y0 + 720), PALE, seed=seed); d = ImageDraw.Draw(im); rnd = random.Random(seed)
    cx = (x0 + x1) // 2
    T(d, (cx, y0 + 64), '급 여 명 세 서', 50, INK, F_X)
    d.line([(x0 + 40, y0 + 112), (x1 - 40, y0 + 112)], fill=INK, width=3)
    for i in range(6):                      # 지급·공제 항목 자리(흐린 손 줄)
        y = y0 + 170 + i * 48
        d.line([(x0 + 50, y), (x0 + 50 + rnd.randint(150, 230), y)], fill=SCRIB, width=12)
        d.line([(cx + 30, y), (cx + 30 + rnd.randint(140, 220), y)], fill=SCRIB, width=12)
    yg = y0 + 500; T(d, (cx, yg), '지급 합계 4,166,666원', 42, INK, F_X)
    d.line([(x0 + 40, y0 + 570), (x1 - 40, y0 + 570)], fill=INK, width=3)
    yn = y0 + 640; T(d, (cx, yn), '실지급액 3,571,586원', 52, OR if hi == 'net' else INK, F_X)
    if hi == 'net': w = wd('실지급액 3,571,586원', 52); hand_under(d, cx - w / 2, cx + w / 2, yn + 40, OR, 8, seed=seed + 1); hi = None
    if hi == 'gross': w = wd('지급 합계 4,166,666원', 42); hand_ellipse(d, (cx - w / 2 - 40, yg - 50, cx + w / 2 + 40, yg + 50), OR, 7, seed=seed + 1)
    if hi == 'net': w = wd('실지급액 3,571,586원', 52); hand_ellipse(d, (cx - w / 2 - 40, yn - 58, cx + w / 2 + 40, yn + 58), OR, 7, seed=seed + 1)
    return d

def stairs(d, x0, x1, ytop, ybot, color, width=7):
    """세전 → 통장 손 계단(6칸) — 막대 상자 대신 선 하나."""
    steps = (188380, 142600, 18730, 35690, 190620, 19060); pre, net = 4166666, 3571586
    Y = lambda v: ybot - (ybot - ytop) * (v - net) / (pre - net)
    n = len(steps); dx = (x1 - x0) / n; cur = pre; pts = [(x0, Y(cur))]
    for i, v in enumerate(steps):
        pts.append((x0 + (i + 1) * dx, Y(cur))); cur -= v; pts.append((x0 + (i + 1) * dx, Y(cur)))
    d.line(pts, fill=color, width=width, joint='curve')

# ── 0장 ──
@board
def n3_open(im):
    d = payslip(im, 1000, 180, 1760, seed=401)
    T(d, (520, 330), '파이어맵', 58, GREY, F_B)
    T(d, (520, 480), '오늘은', 92, INK, F_X)
    T(d, (520, 620), '연봉', 120, INK, F_X)
    s = '실수령액'; T(d, (520, 780), s, 140, OR, F_X)
    hand_under(d, 520 - wd(s, 140) / 2, 520 + wd(s, 140) / 2, 870, seed=402)

@board
def n3_line100_33(im):
    d = ImageDraw.Draw(im); title(d, '직장인 100명을 연봉 순으로 줄 세우면', 120)
    x0, x1 = 150, 1770; step = (x1 - x0) / 49; h = 120; r = step * 0.3
    for i in range(100):
        row, k = divmod(i, 50); person(d, x0 + k * step, 270 + row * 180, h, OR if i < 33 else (172, 164, 152), r)
    hand_under(d, x0 - 10, x0 + 32 * step + 10, 270 + h + 22, OR, 8, seed=31)
    big(d, (x0 + 15 * step, 760), '앞에서 33명 안', 140, seed=32, maxw=1080)
    T(d, (x0 + 42 * step, 760), '연봉 5천은 여기', 56, INK, F_B)
    hand_arrow(d, (x0 + 33 * step, 690), (x0 + 32.3 * step, 410), INK, 6)
    T(d, (W // 2, 930), '상위 33% 안쪽이라는 뜻이에요', 52, INK, F_B)
    source(d, SRC_NTS)

@board
def n3_toc(im):
    d = ImageDraw.Draw(im); T(d, (W // 2, 170), '오늘 볼 것', 150, INK, F_X)
    rows = ('연봉 3천에서 1억까지 일곱 칸', '천만원 올라도 통장이 가장 덜 느는 칸', '거꾸로 — 통장 300만원이 되려면', '같은 연봉, 다른 통장 두 가지')
    for i, s in enumerate(rows):
        y = 400 + i * 150
        d.line([(470, y + 30), (540, y + 30)], fill=INK, width=5)
        T(d, (580, y), s, 62, INK, F_B, 'lm')

# ── 1장 ──
@board
def n3_gross(im):
    d = payslip(im, 1040, 180, 1780, seed=411, hi='gross')
    T(d, (520, 260), '연봉은 어떤 돈?', 64, INK, F_B)
    T(d, (520, 430), '계약서 연봉', 96, INK, F_X)
    big(d, (520, 600), '= 세전', 150, seed=413, maxw=860)
    T(d, (520, 800), '떼기 전 돈 · 통장은 다 뗀 세후', 48, INK, F_B)
    hand_arrow(d, (880, 640), (1030, 680), OR, 7)
    source(d, '그림: 연봉 5천 한 달 예시 · ' + COND)

@board
def n3_three_money(im):
    d = ImageDraw.Draw(im); title(d, "'연봉'은 세 가지 돈", 120)
    T(d, (W // 2, 290), '계약서 연봉 = 떼기 전 돈(세전)', 60, INK, F_B)
    hand_arrow(d, (W // 2, 340), (W // 2, 410), INK, 6)
    big(d, (W // 2, 500), '국세청 총급여', 140, under=False)
    w = wd('국세청 총급여', 140); hand_ellipse(d, (W // 2 - w / 2 - 70, 400, W // 2 + w / 2 + 70, 600), seed=64)
    T(d, (W // 2, 650), '상여 넣고 식대 뺀 돈 · 줄 세울 때 쓰는 돈', 50, INK, F_B)
    hand_arrow(d, (W // 2, 700), (W // 2, 760), INK, 6)
    T(d, (W // 2, 810), '통장 = 다 뗀 돈(세후)', 60, INK, F_B)
    T(d, (W // 2, 950), '내 자리는 원천징수영수증의 총급여로 찾아요', 50, INK, F_B)

@board
def n3_percentile_box(im):
    d = ImageDraw.Draw(im); title(d, '국세청은 100명 중 1명씩 묶은 칸의 평균만 알려 줘요', 120)
    g = (150, 140, 126); xs = (260, 700, 1220, 1660)
    for x in xs: person(d, x, 260, 200, g, 30)
    T(d, (920, 520), '상위 32% 평균 4,837만원', 46, INK, F_B, 'rm'); T(d, (1000, 520), '상위 33% 평균 4,737만원', 46, INK, F_B, 'lm')
    mx = 960; d.ellipse((mx - 26, 400 - 26, mx + 26, 400 + 26), fill=OR)
    hand_arrow(d, (mx, 640), (mx, 440), OR, 7)
    big(d, (mx, 760), '4,760만원', 150, seed=81)
    T(d, (mx, 920), '연봉 5천(식대 빼고 총급여)은 이 두 칸 사이', 52, INK, F_B)
    source(d, SRC_NTS)

# ── 2장 사다리 ──
def lad_line(r): return f'연봉 {r[0]} · {r[1]} · 앞에서 {r[2]} 안'

@board
def n3_ladder_a(im):
    d = ImageDraw.Draw(im); title(d, '연봉 사다리 — 통장 한 달 · 100명 중 몇 번째', 110)
    for i, r in enumerate(LAD[:3]): T(d, (W // 2, 270 + i * 110), lad_line(r), 58, INK, F_X)
    r = LAD[3]; T(d, (W // 2, 640), f'연봉 {r[0]}이면', 64, INK, F_X)
    big(d, (W // 2, 790), f'통장 {r[1]}', 150, seed=93)
    T(d, (W // 2, 950), f'앞에서 {r[2]} 안', 56, INK, F_X)
    source(d, COND + ' · 줄 위치는 국세청 2024년 귀속')

@board
def n3_ladder_b(im):
    d = ImageDraw.Draw(im); title(d, '연봉 사다리 — 통장 한 달 · 100명 중 몇 번째', 110)
    T(d, (W // 2, 260), '연봉 3천 ~ 6천 · 224만 ~ 420만원', 50, FADE, F_X)
    for i, r in enumerate(LAD[4:6]): T(d, (W // 2, 380 + i * 110), lad_line(r), 58, INK, F_X)
    r = LAD[6]; T(d, (W // 2, 640), f'연봉 {r[0]}이면', 64, INK, F_X)
    big(d, (W // 2, 790), f'통장 {r[1]}', 150, seed=96)
    T(d, (W // 2, 950), f'앞에서 {r[2]} 안', 56, INK, F_X)
    source(d, COND + ' · 줄 위치는 국세청 2024년 귀속')

@board
def n3_ladder_c(im):
    d = ImageDraw.Draw(im); title(d, '1억 위 두 칸', 110)
    T(d, (W // 2, 250), lad_line(LAD[6]), 52, FADE, F_X)
    for i, r in enumerate(LAD[7:]): T(d, (W // 2, 370 + i * 110), lad_line(r), 60, INK, F_X)
    T(d, (W // 2, 640), '세전 월급에서 통장에 남는 몫', 60, INK, F_B)
    big(d, (W // 2, 800), '72%까지 내려와요', 150, seed=99)
    source(d, COND)

@board
def n3_share_bars(im):
    d = ImageDraw.Draw(im); title(d, '세전 월급 중 통장에 남는 몫', 110)
    vals = (89.8, 88.1, 85.7, 83.9, 82.7, 80.5, 78.4)
    x0, x1, top, base = 300, 1620, 300, 640; lo, hi = 76, 92
    X = lambda i: x0 + (x1 - x0) * i / 6; Y = lambda v: base - (base - top) * (v - lo) / (hi - lo)
    d.line([(x0 - 40, base + 40), (x1 + 40, base + 40)], fill=LINE, width=3)
    d.line([(X(i), Y(v)) for i, v in enumerate(vals)], fill=INK, width=7, joint='curve')
    for i, v in enumerate(vals):
        c = OR if i == 6 else INK; d.ellipse((X(i) - 14, Y(v) - 14, X(i) + 14, Y(v) + 14), fill=c)
    T(d, (X(0), Y(vals[0]) - 70), '연봉 3천 90%', 56, INK, F_X)
    big(d, (1300, 800), '연봉 1억 78%', 150, seed=118, maxw=1100)
    hand_arrow(d, (1500, 720), (X(6) - 10, Y(vals[6]) + 30), OR, 7)
    T(d, (W // 2, 960), '연봉이 오를수록 떼어 가는 몫이 커져요', 52, INK, F_B)
    source(d, COND + ' · 가운데 칸 4천~8천 = 88·86·84·83·81% · 76% 아래는 잘라 그림')

# ── 3장 어디서 빠지나 ──
DEDUCT = ('국민연금 19만 · 건강보험 14만 · 장기요양 2만', '고용보험 4만 · 소득세 19만 · 지방소득세 2만')

@board
def n3_leak_q(im):
    d = ImageDraw.Draw(im); title(d, '무엇이 얼마나 빠질까?', 110)
    stairs(d, 420, 1380, 300, 620, LINE, 6)
    T(d, (420, 250), '세전 월 417만원', 56, INK, F_X)
    T(d, (1560, 470), '통장에', 64, INK, F_X); big(d, (1560, 620), '얼마?', 150, seed=452, maxw=560)
    T(d, (W // 2, 790), '국민연금 · 건강보험 · 장기요양', 52, INK, F_B)
    T(d, (W // 2, 880), '고용보험 · 소득세 · 지방소득세 — 각각 얼마?', 52, INK, F_B)
    source(d, '연봉 5천 · ' + COND)

@board
def n3_waterfall(im):
    d = ImageDraw.Draw(im); title(d, '연봉 5천, 세전 월급에서 빠지는 돈', 110)
    stairs(d, 420, 1380, 300, 560, INK, 7)
    T(d, (420, 250), '세전 월 417만원', 56, INK, F_X)
    T(d, (1600, 560), '통장 357만원', 60, INK, F_X)
    for i, s in enumerate(DEDUCT): T(d, (W // 2, 680 + i * 80), s, 50, INK, F_B)
    big(d, (W // 2, 900), '다 합치면 60만원쯤', 140, seed=170)
    source(d, COND)

@board
def n3_donuts(im):
    d = ImageDraw.Draw(im); title(d, '빠지는 돈 중 세금은 얼마나? (주황 = 세금)', 110)
    for i, (lab, tot, tax, fr) in enumerate((('연봉 3천', '26만원', '3만원', 0.125), ('연봉 1억', '180만원', '109만원', 0.602))):
        cx = 540 + i * 840; cy = 440
        donut(d, (cx, cy), 200, fr, OR, KRAFT_L)
        T(d, (cx, cy), '세금 ' + tax, 38, OR if i else INK, F_X)
        T(d, (cx, 720), f'{lab} · 빠지는 돈 {tot}', 52, INK, F_B)
    big(d, (W // 2, 880), '빠지는 돈 중 60%가 세금', 140, seed=171)
    source(d, COND)

# ── 4장 1천만원 오를 때 ──
@board
def n3_why_q(im):
    d = ImageDraw.Draw(im)
    T(d, (W // 2, 200), '정말 많이 묻는 질문', 56, GREY, F_B)
    T(d, (W // 2, 400), '연봉이 올랐는데', 120, INK, F_X)
    big(d, (W // 2, 590), '월급은 왜 별로 안 늘까?', 140, seed=462)
    T(d, (W // 2, 860), '연봉 1천만원 오를 때 통장에 남는 돈, 칸마다 셌어요', 48, INK, F_B)

@board
def n3_x18(im):
    d = ImageDraw.Draw(im); title(d, '연봉이 두 배가 되면', 110)
    T(d, (520, 400), '연봉 5천 → 1억', 80, INK, F_X); T(d, (520, 600), '× 2', 150, INK, F_X)
    T(d, (1400, 400), '통장 357만 → 653만', 76, INK, F_X)
    s = '× 1.8'; T(d, (1400, 600), s, 150, OR, F_X)
    hand_ellipse(d, (1400 - wd(s, 150) / 2 - 60, 510, 1400 + wd(s, 150) / 2 + 60, 700), seed=181)
    d.line([(W // 2 + 20, 320), (W // 2 + 20, 720)], fill=FADE, width=4)
    T(d, (W // 2, 880), '통장은 1.8배쯤밖에 안 됩니다', 60, INK, F_B)
    source(d, COND)

def raise_rows(im, hi, note):
    d = ImageDraw.Draw(im); title(d, '연봉 오를 때 오른 돈 중 통장에 남는 몫', 110)
    y = 230; rows = [r for i, r in enumerate(RAISE) if i != hi]
    for k, (a, b, c) in enumerate(rows):
        T(d, (W // 2, y + k * 80), f'{a} · 통장 +{b} · {c}', 48, INK, F_X)
    a, b, c = RAISE[hi]
    T(d, (W // 2, 700), f'{a} · 통장 한 달 +{b}', 60, INK, F_X)
    big(d, (W // 2, 840), f'남는 몫 {c}', 140, seed=190 + hi)
    source(d, note + ' · ' + COND)

@board
def n3_raise_table(im): raise_rows(im, 4, '오른 돈의 삼분의 이 정도만 남는 칸')

@board
def n3_raise_table_b(im): raise_rows(im, 5, '국민연금이 월 31만원에서 더 안 늘어서')

@board
def n3_taxsteps(im):
    d = ImageDraw.Draw(im); title(d, '소득세율 계단 — 넘는 부분에만 높은 세율', 110)
    T(d, (W // 2, 240), '과세표준(연봉에서 이것저것 빼고 남은 돈)', 42, GREY, F_B)
    for y, s in ((350, '1,400만원 이하 6%'), (460, '5,000만원 이하 15%'), (790, '1억 5천만원 이하 35%')): T(d, (W // 2, y), s, 60, INK, F_X)
    s = '8,800만원 이하 24%'; sz = TF(d, (W // 2, 620), s, 130, OR, F_X)
    w = wd(s, sz); hand_ellipse(d, (W // 2 - w / 2 - 60, 620 - 100, W // 2 + w / 2 + 60, 620 + 100), seed=232)
    T(d, (W // 2, 930), '5천만원을 넘는 부분에만 15% 대신 24%', 54, INK, F_B)
    source(d, '소득세법 제55조① 종합소득세율(우리 글씨로 옮김, 1억 5천 위 칸 생략)')

@board
def n3_raise_top(im):
    d = ImageDraw.Draw(im); title(d, '1억 위로 오를 때', 110)
    T(d, (W // 2, 300), '1억 → 1억 2천 · 통장 +108만원 · 65%', 60, INK, F_X)
    T(d, (W // 2, 480), '1억 2천 → 1억 5천 · 통장 한 달 +141만원', 62, INK, F_X)
    big(d, (W // 2, 650), '남는 몫 56%', 150, seed=251)
    T(d, (W // 2, 880), '연금은 이미 끝에 닿아 — 더 떼는 돈 대부분이 소득세', 50, INK, F_B)
    source(d, COND + ' · 1억 2천 → 1억 5천은 3천만원 오름')

# ── 5장 거꾸로 ──
@board
def n3_rev_q(im):
    d = ImageDraw.Draw(im)
    T(d, (W // 2, 170), '검색창에 거꾸로 묻는 분도 많아요', 54, GREY, F_B)
    T(d, (550, 440), '통장에 한 달', 54, INK, F_B); T(d, (550, 580), '300만원', 120, INK, F_X)
    hand_arrow(d, (900, 525), (1060, 525), INK, 9)
    T(d, (1400, 440), '연봉은', 60, INK, F_B); T(d, (1400, 590), '얼마?', 140, OR, F_X)
    hand_ellipse(d, (1210, 490, 1590, 690), seed=473)
    T(d, (W // 2, 880), '세후 300 · 400 · 500 · 600만원 차례로', 50, INK, F_B)
    source(d, COND)

@board
def n3_rev300(im):
    d = ImageDraw.Draw(im); title(d, '거꾸로 — 통장에 한 달 300만원이 찍히려면', 110)
    T(d, (W // 2, 300), '통장 월 300만원', 80, INK, F_X)
    hand_arrow(d, (W // 2, 370), (W // 2, 460), INK, 8)
    big(d, (W // 2, 570), '연봉 4,100만원쯤', 150, seed=271)
    T(d, (W // 2, 780), '백 명 중 앞에서 44명 안', 66, INK, F_X)
    T(d, (W // 2, 870), '한가운데보다 조금 앞', 48, GREY, F_B)
    source(d, COND + ' · 줄 위치는 국세청 2024년 귀속')

@board
def n3_rev_cond(im):
    d = ImageDraw.Draw(im); title(d, '같은 통장 금액, 조건 따라 필요한 연봉', 110)
    T(d, (W // 2, 240), '통장에 한 달 400만원이 찍히려면', 60, INK, F_X)
    T(d, (W // 2, 360), '1인 · 식대 비과세 있음', 54, INK, F_B)
    big(d, (W // 2, 490), '연봉 5,680만원', 150, seed=291)
    T(d, (W // 2, 660), '식대 비과세 없으면 5,770만원 (+90만)', 54, INK, F_X)
    T(d, (W // 2, 760), '4인 · 자녀 2면 5,420만원 (−260만)', 54, INK, F_X)
    T(d, (W // 2, 900), '통장 300만원은 3,970만~4,170만 · 500만원은 7,000만~7,460만', 42, GREY, F_B)
    source(d, '식대 비과세 월 20만원 · 4인 = 본인·배우자·8~20세 자녀 2 · 2026년 요율·간이세액표')

# ── 6장 같은 연봉, 다른 통장 ──
@board
def n3_nontax(im):
    d = ImageDraw.Draw(im); title(d, '같은 연봉 5천인데 통장이 다른 이유', 110)
    T(d, (540, 255), '실제로는 훨씬 적게 들어와요', 42, INK, F_B)
    T(d, (1370, 255), '비과세가 없는 회사라 더 적어요', 42, INK, F_B)
    for i, (a, b) in enumerate((('식대 비과세 있음', '357만원'), ('식대 비과세 없음', '352만원'))):
        cx = 620 + i * 680; T(d, (cx, 470), a, 46, GREY, F_B); T(d, (cx, 580), b, 90, INK, F_X)
    big(d, (W // 2, 820), '차이 월 4만 8,810원', 140, seed=313)
    source(d, '1인 · 댓글은 우리 말로 줄임 · 2026년 요율·간이세액표')

@board
def n3_family(im):
    d = ImageDraw.Draw(im); title(d, '가족 수로도 달라져요 — 1인 vs 본인·배우자·자녀 2', 110)
    g = (150, 140, 126)
    person(d, 560, 220, 150, g, 26)
    for dx, h in ((-120, 150), (-45, 150), (30, 100), (95, 100)): person(d, 1360 + dx, 220 + (150 - h), h, g, 26 if h > 120 else 19)
    hand_arrow(d, (700, 300), (1180, 300), INK, 6)
    T(d, (W // 2, 500), '연봉 5천 · 357만원 → 373만원 (+16만원)', 60, INK, F_X)
    T(d, (W // 2, 640), '연봉 1억 · 653만원 → 683만원', 64, INK, F_X)
    big(d, (W // 2, 810), '+30만원', 150, seed=321)
    source(d, '통장 한 달 · 자녀 8~20세 · 식대 비과세 월 20만원 · 2026년 요율·간이세액표')

@board
def n3_8020(im):
    d = ImageDraw.Draw(im); title(d, '연봉 1억, 달마다 떼는 세금을 고르면', 110)
    for i, s in enumerate(('덜 떼기 80% · 통장 675만원', '그대로 100% · 통장 653만원', '더 떼기 120% · 통장 631만원')):
        T(d, (W // 2, 270 + i * 100), s, 60, INK, F_X)
    big(d, (W // 2, 640), '덜 떼면 한 달 +22만원', 150, seed=331)
    T(d, (W // 2, 810), '대신 연말정산 때 한꺼번에 더 낼 수 있음', 52, INK, F_B)
    T(d, (W // 2, 920), '한 해 세금은 같고, 내는 때만 바뀌어요', 54, INK, F_X)
    source(d, '소득세법 시행령 제194조① · 1인 · 식대 비과세 월 20만원')

@board
def n3_trap_yearend(im):
    d = ImageDraw.Draw(im); title(d, '달마다 떼는 소득세는 미리 어림한 값', 110)
    x0, cw = 140, 92
    for m in range(12):
        cx = x0 + m * cw + cw / 2
        d.ellipse((cx - 32, 330, cx + 32, 394), fill=(201, 160, 72), outline=INK, width=3)
        d.ellipse((cx - 19, 343, cx + 19, 381), outline=(150, 112, 40), width=3)
    T(d, (x0 + 6 * cw, 470), '1월부터 12월까지 12달 동안 미리 뗌', 52, INK, F_B)
    hand_arrow(d, (x0 + 12 * cw + 10, 362), (1310, 362), INK, 6)
    s = '연말정산'; T(d, (1590, 362), s, 140, OR, F_X)
    hand_ellipse(d, (1590 - wd(s, 140) / 2 - 40, 262, 1590 + wd(s, 140) / 2 + 40, 462), seed=354)
    hand_arrow(d, (1590, 480), (1450, 630), INK, 6); hand_arrow(d, (1590, 480), (1730, 630), INK, 6)
    T(d, (1430, 690), '더 냄', 54, INK, F_X); T(d, (1750, 690), '돌려받음', 54, INK, F_X)
    T(d, (W // 2, 900), "오늘 본 통장 금액은 '보통 달' 금액이에요", 60, INK, F_X)

@board
def n3_seven(im):   # r09 '이제 일곱 칸입니다. 칸마다 통장 금액과 줄 위치를 같이 볼게요.'
    d = ImageDraw.Draw(im)
    big(d, (W // 2, 190), '이제 일곱 칸', 150, color=INK, seed=421)
    x0, x1, yb = 260, 1660, 840; dx = (x1 - x0) / 7; pts = [(x0, yb)]
    for i in range(7): pts += [(x0 + i * dx, yb - 62 * (i + 1)), (x0 + (i + 1) * dx, yb - 62 * (i + 1))]
    d.line(pts, fill=INK, width=7, joint='curve')
    T(d, (W // 2, 930), '연봉 3천 · 4천 · 5천 · 6천 · 7천 · 8천 · 1억', 60, INK, F_X)
    T(d, (x1 - dx / 2, yb - 62 * 7 - 90), '통장 ?', 90, OR, F_X)
    T(d, (700, 470), '칸마다 통장 금액 · 백 명 줄에서 몇 번째', 46, INK, F_B)

@board
def n3_netcheck(im):
    d = payslip(im, 180, 150, 960, seed=441, hi='net')
    T(d, (1400, 300), '표의 통장 금액은', 60, INK, F_B)
    big(d, (1400, 450), '실지급액과 비교', 130, seed=443, maxw=900)
    hand_arrow(d, (1040, 560), (920, 780), INK, 7)
    T(d, (1400, 700), '상여 나온 달은 따로', 60, INK, F_X)
    T(d, (1400, 790), '보통 달끼리 비교하세요', 46, INK, F_B)
    source(d, '그림: 연봉 5천 한 달 예시 · ' + COND)

# ── 7장 평균과 상위 25% ──
@board
def n3_top25_q(im):
    d = ImageDraw.Draw(im)
    T(d, (W // 2, 150), '이번엔 이런 댓글이에요', 54, GREY, F_B)
    torn(im, (360, 230, 1560, 600), MEMO, seed=491); d = ImageDraw.Draw(im)
    T(d, (410, 280), '댓글', 36, GREY, F_B, 'lm')
    T(d, (W // 2, 380), '난 왜 상위 25%인데', 92, INK, F_X); T(d, (W // 2, 500), '삶이 힘드냐', 92, INK, F_X)
    T(d, (W // 2, 700), '백 명 중 앞에서 스물다섯 번째쯤 사람들은', 52, INK, F_B)
    big(d, (W // 2, 850), '통장에 얼마?', 150, seed=492)

@board
def n3_top25_10(im):
    d = ImageDraw.Draw(im); title(d, '앞에서 10번째, 25번째 사람의 통장', 110)
    x0, x1 = 150, 1770; step = (x1 - x0) / 49; h = 110; r = step * 0.3
    for i in range(100):
        row, k = divmod(i, 50); person(d, x0 + k * step, 300 + row * 160, h, (172, 164, 152), r)
    for n, hi in ((10, False), (25, True)):
        cx = x0 + (n - 1) * step; col = OR if hi else INK
        person(d, cx, 300, h, col, r)
        d.line([(cx, 280), (cx, 210)], fill=col, width=5); d.polygon([(cx, 210), (cx + 50, 225), (cx, 240)], fill=col)
    T(d, (420, 670), '앞에서 10번째 · 총급여 9,117만원', 44, INK, F_B); T(d, (420, 770), '통장 616만원', 80, INK, F_X)
    T(d, (1330, 670), '앞에서 25번째 · 총급여 5,727만원', 44, INK, F_B)
    big(d, (1330, 820), '통장 418만원', 150, seed=361, maxw=1000)
    source(d, SRC_NTS + ' · 통장은 1인·식대 비과세 월 20만원')

@board
def n3_partyear(im):
    d = ImageDraw.Draw(im); title(d, '이 줄에는 몇 달만 일한 사람도 있어요', 110)
    x0, x1 = 150, 1770; step = (x1 - x0) / 49; h = 110; r = step * 0.3
    for k in range(50): person(d, x0 + k * step, 250, h, (172, 164, 152) if k < 44 else (222, 214, 200), r)
    hand_ellipse(d, (x0 + 43.4 * step, 220, x1 + 30, 390), seed=381)
    T(d, (x1 - 120, 430), '맨 뒤', 40, GREY, F_B)
    T(d, (W // 2, 520), '한 해 중 몇 달만 일해도 줄에 들어가요', 52, INK, F_B)
    T(d, (W // 2, 640), '맨 뒤 구간 평균 총급여', 64, INK, F_X)
    big(d, (W // 2, 780), '21만원', 150, seed=382)
    T(d, (W // 2, 950), "'일 년 내내 일한 직장인 중 몇 번째'와는 조금 달라요", 48, INK, F_B)
    source(d, SRC_NTS + ' · 2,108만 명')

# ── 7장 끝 ──
@board
def n3_sameformula(im):
    d = ImageDraw.Draw(im)
    T(d, (W // 2, 180), '오늘 본 숫자는 전부', 70, INK, F_B)
    big(d, (W // 2, 330), '같은 계산식', 150, seed=501)
    T(d, (W // 2, 560), '연봉 + 식대 비과세 + 가족 수', 76, INK, F_X)
    hand_arrow(d, (W // 2, 630), (W // 2, 740), INK, 8)
    T(d, (W // 2, 820), '통장 금액', 90, INK, F_X)
    T(d, (W // 2, 960), '보험료율·간이세액표 올해 기준 · 국세청 줄 2024년 귀속', 40, GREY, F_B)

@board
def n3_calc_site(im):
    shot = Image.open(os.path.join(HERE, 'cap', 'r40_5000.png')).convert('RGB')
    k = 960 / 1600; card = shot.crop((52, 216, 1184, 610))           # 결과 칸(월 실수령액)만 — 아래 입력 칸들은 'UI 상자'
    cw = 860; card = card.resize((cw, round(card.height * cw / card.width)), Image.LANCZOS)
    ox, oy = 120, 300; im.paste(card, (ox, oy)); d = ImageDraw.Draw(im)
    cx = 1400
    T(d, (cx, 330), '파이어맵 월급 계산기에', 56, GREY, F_B)
    T(d, (cx, 450), '연봉 5,000만원 넣으면', 72, INK, F_X)
    big(d, (cx, 640), '3,571,586원', 150, seed=402, maxw=900)
    T(d, (cx, 860), '내 연봉·식대·가족 수를 넣어 보세요', 46, INK, F_B)
    source(d, 'firemap.kr/calc/salary · ' + COND)

def main(names):
    os.makedirs(OUT, exist_ok=True)
    for n in names or list(B):
        im = canvas(); B[n](im); im.save(os.path.join(OUT, n + '.png')); print(n)

if __name__ == '__main__':
    main(sys.argv[1:])
