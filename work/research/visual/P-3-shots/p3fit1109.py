"""P-3 판 bgcheck 맞춤 — visual-designer 2026-11-09 23시(PD 19:55 요청: p3_ds.mp4 bgcheck 거부 '판 큰 글자 중앙 7.3% < 9%').
K-1 11/8(k1boards bde455e)과 같은 법: ① 그 화면의 답 하나를 120~150px(bgcheck ④ 9%↑) ② 찢은 종이 칸·네모 칸 빼고 종이 위에 바로,
막대는 hatch_bar(손 빗금) — ⑥ UI 상자 0 ③ 한 줄로 읽히는 말은 한 줄로 붙여(이름 오른쪽 끝·값 왼쪽 끝) 글자 줄 8 이하.
판 이름·크기(1920×1080) 그대로, 숫자·사실은 옛 판(p3boards·p3new1104·p3fix1103)과 같은 값. 옛 함수는 지우지 않고 여기서 덮어 그린다.
실사 위 글자 3장(p3_over_r03·r31·r34): 큰 주황 글자 아래 끝을 자막 띠(화면 아래 20%, y 864) 위로 — y 880 → 730.
사용: py -3.12 p3fit1109.py [이름 ...] → work/video/public/bg/p3/board/<이름>.png · over/ 3장
검사: py -3.12 work/boardcheck.py p3
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', 'K-1-shots'))
import k1boards as K
from k1boards import (W, H, INK, GREY, OR, KRAFT, KRAFT_L, F_B, F_M, F_X, font, canvas, T, TF, title, source,
                      hand_ellipse, hand_under, hand_arrow, hatch_bar)
from PIL import Image, ImageDraw
import p3fix1103 as FX
from p3new1104 import hand_x, hand_o

OUT = os.path.join(K.WORK, 'video', 'public', 'bg', 'p3', 'board')
SRC_NHIS = '국민건강보험공단 · 2026년 건강보험료율 7.19% · 장기요양 13.14%'
LINE = (170, 160, 150)
def wd(s, size, f=F_X): return font(f, size).getlength(s)
B = {}
def board(fn): B[fn.__name__] = fn; return fn

def pair(d, cx, y, a, sa, ca, fa, b, sb, cb, fb, gap=18):
    """이름(오른쪽 끝)+값(왼쪽 끝)을 붙여 한 줄로 — 둘을 합친 폭의 가운데를 cx에. 값 왼쪽 x, 값 폭을 돌려줌."""
    wa, wb = wd(a, sa, fa), wd(b, sb, fb); x = cx - (wa + gap + wb) / 2
    T(d, (x + wa, y), a, sa, ca, fa, 'rm'); T(d, (x + wa + gap, y), b, sb, cb, fb, 'lm'); return x + wa + gap, wb

def big(d, y, s, size=140, color=OR, under=True, seed=1, cx=W // 2, maxw=1760):
    size = TF(d, (cx, y), s, size, color, F_X, maxw=maxw)
    if under: w = wd(s, size); hand_under(d, cx - w / 2, cx + w / 2, y + size * 0.55, seed=seed)
    return size

@board
def p3_auto_over(im):
    d = ImageDraw.Draw(im)
    T(d, (W // 2, 300), '올해 국민연금 월 165만원 · 아직은 기준 아래', 56, INK, F_B)
    T(d, (W // 2, 520), '아무것도 안 해도', 110, INK, F_X)
    big(d, 720, '넘을 수 있습니다', 150, seed=302)

@board
def p3_ruler(im):
    d = ImageDraw.Draw(im); title(d, '피부양자 소득 기준', 110)
    x0, x1, y = 260, 1660, 470
    d.line([(x0 - 30, y - 70), (x1 + 30, y - 70)], fill=INK, width=5)
    for k in range(0, 31):
        x = x0 + (x1 - x0) * k / 30; L = 60 if k % 10 == 0 else (36 if k % 5 == 0 else 20)
        d.line([(x, y - 70), (x, y - 70 + L)], fill=INK, width=4 if k % 10 == 0 else 2)
    for k, lab in ((0, '0원'), (10, '1천만원'), (20, '2천만원'), (30, '3천만원')):
        x = x0 + (x1 - x0) * k / 30; T(d, (x, y + 30), lab, 40, GREY if k != 20 else INK, F_B)
    xs = x0 + (x1 - x0) * 20 / 30
    d.line([(xs, y - 190), (xs, y - 10)], fill=OR, width=10)
    T(d, (xs, y - 240), '한 해 2천만원', 64, INK, F_X)
    big(d, 760, '한 달 166만원 남짓', 140, seed=71)
    source(d, '국민건강보험법 시행규칙 별표 1의2 · 2천만원 ÷ 12 = 약 166.7만원')

@board
def p3_public_private(im):
    d = ImageDraw.Draw(im); title(d, '어디서 받는 연금인가', 110)
    T(d, (W // 2, 270), '국민연금', 80, INK, F_X)
    big(d, 430, '받은 돈 전부 셈', 140, seed=82)
    d.line([(560, 560), (1360, 560)], fill=LINE, width=3)
    T(d, (W // 2, 660), '연금저축 · IRP', 80, INK, F_X)
    T(d, (W // 2, 800), '소득에 안 넣음', 96, INK, F_X)
    source(d, '국민건강보험공단 안내 · 국민연금은 세금 떼는지와 상관없이 전부')

def dash_rect(d, box, color, w=5, dash=26, gap=18):
    x0, y0, x1, y1 = box
    for (ax, ay, bx, by) in ((x0, y0, x1, y0), (x1, y0, x1, y1), (x1, y1, x0, y1), (x0, y1, x0, y0)):
        import math
        L = math.hypot(bx - ax, by - ay); t = 0
        while t < L:
            e = min(t + dash, L); d.line([(ax + (bx - ax) * t / L, ay + (by - ay) * t / L), (ax + (bx - ax) * e / L, ay + (by - ay) * e / L)], fill=color, width=w); t += dash + gap

@board
def p3_two_bars(im):
    d = ImageDraw.Draw(im); title(d, '한 달 166만원 = 국민연금 100만 + 연금저축 66만', 110)
    bx0, bx1, base, scale = 110, 650, 900, 3.6
    h1, h2 = 100 * scale, 66 * scale
    hatch_bar(im, (bx0, base - h1, bx1, base), KRAFT, seed=1104); d = ImageDraw.Draw(im)
    dash_rect(d, (bx0, base - h1 - h2, bx1, base - h1), GREY)
    T(d, ((bx0 + bx1) // 2, base - h1 / 2), '국민연금 한 달 100만원', 46, INK, F_X)
    T(d, ((bx0 + bx1) // 2, base - h1 - h2 / 2 - 26), '연금저축 한 달 66만원', 40, INK, F_B)
    T(d, ((bx0 + bx1) // 2, base - h1 - h2 / 2 + 34), '안 셈', 54, INK, F_X)
    x0, x1, y = 760, 1720, 420
    d.line([(x0, y - 70), (x1, y - 70)], fill=INK, width=5)
    for k in range(0, 21):
        x = x0 + (x1 - x0) * k / 20; L = 60 if k % 10 == 0 else (36 if k % 5 == 0 else 18)
        d.line([(x, y - 70), (x, y - 70 + L)], fill=INK, width=4 if k % 10 == 0 else 2)
    T(d, (x1, y + 30), '2천만원 기준', 38, INK, F_B)
    xd = x0 + (x1 - x0) * 12 / 20
    d.ellipse((xd - 22, y - 92, xd + 22, y - 48), fill=INK)
    T(d, ((x0 + x1) / 2, y - 170), '피부양자 소득으로 세는 돈 한 해 1,200만원', 46, INK, F_B)
    hand_arrow(d, (xd + 30, y - 70), (x1 - 20, y - 70), OR, 7)
    cx = (x0 + x1) / 2
    T(d, (cx, 610), '기준까지', 90, INK, F_X)
    big(d, 760, '800만원 남음', 150, seed=1105, cx=cx, maxw=1000)
    source(d, '국민건강보험공단 웹진 2023.9 · 사적연금은 피부양자 소득에 안 넣음 · 100만 × 12 = 1,200만원')

@board
def p3_calc_health(im):
    d = ImageDraw.Draw(im); title(d, '건강보험료 계산', 110)
    T(d, (W // 2, 260), '국민연금 월 167만원', 76, INK, F_X)
    T(d, (W // 2, 390), '× 절반  (보험료 매길 땐 연금의 절반만)', 54, INK, F_B)
    T(d, (W // 2, 500), '× 7.19%  (건강보험료율)', 54, INK, F_B)
    d.line([(520, 580), (1400, 580)], fill=INK, width=4)
    big(d, 720, '= 약 6만원', 150, seed=90)
    source(d, SRC_NHIS)

@board
def p3_calc_ltc(im):
    d = ImageDraw.Draw(im); title(d, '고지서에는 하나 더', 110)
    pair(d, W // 2, 250, '건강보험료', 62, INK, F_B, '약 6만원', 66, INK, F_X, 60)
    pair(d, W // 2, 370, '+ 장기요양보험료', 62, INK, F_B, '약 8천원', 66, INK, F_X, 60)
    T(d, (W // 2, 450), '(건강보험료 × 13.14%)', 40, GREY, F_M)
    d.line([(420, 520), (1500, 520)], fill=INK, width=4)
    T(d, (W // 2, 600), '합계', 66, INK, F_B)
    s = '매달 약 6만 8천원'; sz = TF(d, (W // 2, 760), s, 140, OR, F_X); w = wd(s, sz)
    hand_ellipse(d, (W // 2 - w / 2 - 50, 760 - 110, W // 2 + w / 2 + 50, 760 + 110), seed=92)
    source(d, SRC_NHIS)

@board
def p3_step_table(im):
    d = ImageDraw.Draw(im); title(d, '국민연금 월액별 건보료(재산 거의 없을 때)', 110)
    rows = (('월 166만원', '0원'), ('월 167만원', '약 6만 8천원'), ('월 170만원', '약 6만 9천원'), ('월 200만원', '약 8만 1천원'))
    pair(d, W // 2, 230, '국민연금', 40, GREY, F_M, '매달 내는 보험료', 40, GREY, F_M)
    cx = W // 2 - 140
    for i, (a, b) in enumerate(rows):
        y = 350 + i * 150 + (30 if i > 1 else 0)
        if i: d.line([(300, y - 80 - (15 if i == 2 else 0)), (1620, y - 80 - (15 if i == 2 else 0))], fill=LINE, width=2)
        T(d, (cx - 9, y), a, 66, INK, F_B, 'rm')
        T(d, (cx + 9, y), b, 140 if i == 1 else 74, OR if i == 1 else INK, F_X, 'lm')
    hand_arrow(d, (250, 360), (250, 490), INK, 7); T(d, (220, 425), '여기서 뜀', 46, INK, F_X, 'rm')
    source(d, '건강보험료 + 장기요양보험료 · ' + SRC_NHIS.split(' · ', 1)[1])

@board
def p3_four_rows(im):
    d = ImageDraw.Draw(im); title(d, '선을 넘은 뒤로는 조금씩 올라요', 110)
    rows = (('월 166만원', '0원'), ('월 167만원', '약 6만 8천원'), ('월 170만원', '약 6만 9천원'), ('월 180만원', '약 7만 3천원'), ('월 200만원', '약 8만 1천원'))
    cx = 760; ys = []
    for i, (a, b) in enumerate(rows):
        y = 250 + i * 110; ys.append(y)
        if i: d.line([(cx - 460, y - 55), (cx + 460, y - 55)], fill=LINE, width=2)
        T(d, (cx - 9, y), a, 62, GREY if i == 0 else INK, F_B, 'rm')
        T(d, (cx + 9, y), b, 68, GREY if i == 0 else INK, F_X, 'lm')
    bx = cx + 480
    T(d, (cx + 9 + wd(rows[1][1], 68) + 18, ys[1]), '← 여기서 한 번 크게 뜀', 44, INK, F_B, 'lm')
    d.line([(bx, ys[2]), (bx + 40, ys[2]), (bx + 40, ys[3]), (bx, ys[3])], fill=INK, width=6)
    hand_arrow(d, (bx + 40, (ys[2] + ys[3]) / 2), (bx + 40, 760), INK, 6)
    x, w = pair(d, W // 2, 850, '10만원 더 받아도', 60, INK, F_B, '4천원쯤 더', 140, OR, F_X)
    hand_under(d, x, x + w, 930, seed=1106)
    source(d, '국민연금(한 달) → 매달 내는 보험료 · 재산 0일 때 · 건강보험료 7.19% + 장기요양 13.14% · 73,213 − 69,146 = 4,067원')

@board
def p3_10years(im):
    d = ImageDraw.Draw(im); title(d, '매달 6만 8천원쯤을 10년 동안', 110)
    cw, ch, gx, gy = 96, 40, 14, 10; x0 = (W - (12 * cw + 11 * gx)) // 2 + 60; y0 = 200
    for yr in range(10):
        for m in range(12):
            x = x0 + m * (cw + gx); y = y0 + yr * (ch + gy)
            hatch_bar(im, (x, y, x + cw, y + ch), KRAFT if (yr + m) % 2 else (176, 140, 100), seed=yr * 12 + m, step=13, width=5)
    d = ImageDraw.Draw(im); yb = y0 + 10 * (ch + gy) - gy
    d.line([(x0 - 40, y0), (x0 - 60, y0), (x0 - 60, yb), (x0 - 40, yb)], fill=INK, width=6)
    T(d, (x0 - 90, (y0 + yb) / 2), '10년', 54, INK, F_X, 'rm')
    big(d, 820, '모두 더하면 800만원 넘음', 136, seed=101)
    source(d, '월 167만원 기준 67,926원 × 120달 = 약 815만원 · 보험료율이 그대로일 때')

@board
def p3_raise(im):
    d = ImageDraw.Draw(im); title(d, '국민연금은 해마다 1월에 물가만큼', 110)
    base, top = 900, 330; vmax = 175; lo = 140
    Y = lambda v: base - (base - top) * (v - lo) / (vmax - lo)
    hatch_bar(im, (540, Y(165), 840, base), KRAFT, seed=110); hatch_bar(im, (1160, Y(168.5), 1460, base), OR, seed=111)
    d = ImageDraw.Draw(im)
    T(d, (510, Y(165) + 90), '월 165만원', 80, INK, F_X, 'rm'); T(d, (690, base + 50), '올해', 46)
    T(d, (1310, Y(168.5) - 90), '168만원 남짓', 130, OR, F_X); T(d, (1310, base + 50), '내년', 46)
    hand_arrow(d, (860, 700), (1140, 640), INK, 6); T(d, (1000, 760), '+2.1%', 56, INK, F_B)
    yt = Y(166.7); xx = 500
    while xx < 1500: d.line([(xx, yt), (min(xx + 26, 1500), yt)], fill=INK, width=6); xx += 44
    T(d, (1520, yt + 40), '기준 166만원 남짓', 44, INK, F_X, 'lm')
    source(d, '2026년 국민연금 물가 반영 2.1% · 내년도 같은 비율로 오른다고 가정')

@board
def p3_164_163(im):
    d = ImageDraw.Draw(im); title(d, '올해 받는 연금이 이만큼이면', 110)
    rows = (('올해 월 164만원', '내년 약 167.4만원', '기준 넘음', OR, 140), ('올해 월 163만원', '내년 약 166.4만원', '안 넘음', INK, 96))
    for i, (a, b, c, col, sz) in enumerate(rows):
        y = 260 + i * 360
        T(d, (W // 2 - 70, y), a, 62, INK, F_X, 'rm'); hand_arrow(d, (W // 2 - 45, y), (W // 2 + 45, y), INK, 6)
        T(d, (W // 2 + 70, y), b, 58, INK, F_B, 'lm')
        TF(d, (W // 2, y + 150), c, sz, col, F_X)
        if i == 0:
            w = wd(c, sz); hand_ellipse(d, (W // 2 - w / 2 - 60, y + 150 - 105, W // 2 + w / 2 + 60, y + 150 + 105), seed=123)
        else: d.line([(400, y - 190), (1520, y - 190)], fill=LINE, width=2)
    source(d, '2.1%씩 오른다고 가정 · 기준 월 약 166.7만원(한 해 2천만원)')

@board
def p3_cut_steps(im):
    d = ImageDraw.Draw(im); title(d, '깎아 주던 비율 (그 사이 처음 탈락한 사람만)', 110)
    steps = (('1년째', '80%'), ('2년째', '60%'), ('3년째', '40%'), ('4년째', '20%'))
    base = 880; bw = 230; gap = 70; x = (W - (5 * bw + 4 * gap)) // 2
    for i, (a, b) in enumerate(steps):
        h = 480 - i * 100
        hatch_bar(im, (x, base - h, x + bw, base), KRAFT, seed=140 + i); d = ImageDraw.Draw(im)
        T(d, (x + bw // 2 - 8, base - h - 50), a, 44, INK, F_B, 'rm'); T(d, (x + bw // 2 + 8, base - h - 50), b, 56, INK, F_X, 'lm')
        x += bw + gap
    T(d, (x + bw // 2, base - 150), '끝', 150, OR, F_X); T(d, (x + bw // 2, base + 50), '2026년 8월분까지', 40, OR, F_B)
    hand_ellipse(d, (x - 10, base - 290, x + bw + 10, base - 10), seed=145)
    source(d, '2022년 9월 시작 · 지금 새로 탈락하면 경감 없음')

@board
def p3_cut_calendar(im):
    d = ImageDraw.Draw(im); title(d, '깎아 주던 비율, 달력으로 보면', 110)
    cells = (('2022년 9월분부터', '80%', '깎아 줌'), ('2023년 11월분부터', '60%', '깎아 줌'), ('2024년 11월분부터', '40%', '깎아 줌'),
             ('2025년 11월분부터', '20%', '깎아 줌'))
    cx = W // 2 - 40
    for i, (a, b, c) in enumerate(cells):
        y = 240 + i * 105
        T(d, (cx - 9, y), a, 50, INK, F_B, 'rm'); T(d, (cx + 9, y), b, 64, INK, F_X, 'lm')
        T(d, (cx + 9 + wd(b, 64) + 12, y), c, 40, GREY, F_B, 'lm')
        if i < 3: hand_arrow(d, (cx - 640, y + 20), (cx - 640, y + 85), GREY, 4)
    y = 700
    T(d, (cx - 12, y), '2026년 9월분부터', 56, INK, F_X, 'rm'); T(d, (cx + 12, y), '0%', 150, OR, F_X, 'lm')
    hand_ellipse(d, (cx - 520, y - 110, cx + 640, y + 110), OR, 9, seed=1301)
    T(d, (W // 2, 900), '깎는 것 없음 — 이미 받던 분도 9월분부터 전부 내요', 58, INK, F_X)
    source(d, '국민건강보험법 시행규칙 부칙<보건복지부령 제907호, 2022.9.1> 제3조 · 경감 2026년 8월분까지')

@board
def p3_old_erase(im):
    d = ImageDraw.Draw(im)
    T(d, (W // 2, 200), '예전 기사·영상 속 계산', 54, GREY, F_B)
    for k, s in enumerate(('탈락해도 첫해는 80% 깎아 줌', '다음 해 60% · 40% · 20%')):
        y = 320 + k * 120; T(d, (W // 2, y), s, 64, INK, F_B)
        x0, x1 = W // 2 - wd(s, 64, F_B) / 2 - 20, W // 2 + wd(s, 64, F_B) / 2 + 20
        d.line([(x0, y + 6), (x1, y - 6)], fill=INK, width=8)
    T(d, (W // 2, 560), '2026년 8월분으로 모두 끝남', 46, GREY, F_M)
    big(d, 760, '그 계산은 지우셔야 합니다', 140, seed=332)
    source(d, '국민건강보험공단 · 피부양자 탈락자 보험료 경감 2026년 8월분 종료')

@board
def p3_calendar_rule(im):
    d = ImageDraw.Draw(im)
    x0, x1, xm = 120, 1800, 1220; xa = x0 + 440; ytop = 150
    T(d, ((x0 + xa) // 2, ytop + 70), '피부양자 판정 때 보는 해', 38, GREY, F_B)
    T(d, (xa + 48 + 190, ytop + 70), '1월 ~ 10월', 56, INK, F_X); T(d, ((xm + x1) // 2, ytop + 70), '11월 ~ 12월', 56, INK, F_X)
    d.line([(x0, ytop + 140), (x1, ytop + 140)], fill=INK, width=3); d.line([(xm, ytop + 20), (xm, 880)], fill=INK, width=3)
    for i, (lab, a, b) in enumerate((('국민연금', '작년 연금', '작년 연금'), ('이자·배당', '재작년 소득', '작년 소득'))):
        y = ytop + 290 + i * 300
        T(d, (xa + 30, y), lab, 64, INK, F_X, 'rm')
        T(d, (xa + 48, y), a, 72, INK, F_B, 'lm'); T(d, ((xm + x1) // 2, y), b, 120 if i == 1 else 72, OR if i == 1 else INK, F_X if i == 1 else F_B)
        if i == 0: d.line([(x0, y + 150), (x1, y + 150)], fill=LINE, width=2)
    hand_ellipse(d, (xm + 20, ytop + 590 - 100, x1 + 10, ytop + 590 + 100), seed=151)
    source(d, '국민건강보험공단 · 연금은 1월, 이자·배당 등은 11월에 판정 기준 해가 넘어감')

@board
def p3_timeline(im):
    d = ImageDraw.Draw(im); title(d, '오른 연금은 언제 반영되나', 110)
    pts = (('올해', '월 165만원'), ('내년', '연금 오름 168만원 남짓'), ('그다음 해', '판정 · 탈락 고지서 시작'))
    xs = (330, 900, 1470); y = 480
    d.line([(xs[0], y), (xs[2], y)], fill=INK, width=6)
    for i, ((a, b), x) in enumerate(zip(pts, xs)):
        col = OR if i == 2 else INK
        d.ellipse((x - 26, y - 26, x + 26, y + 26), fill=col)
        T(d, (x, y - 130), a, 130 if i == 2 else 80, col, F_X)
        T(d, (x, y + 110), b, 52, col, F_B)
    hand_ellipse(d, (1100, y - 240, 1850, y + 200), seed=160)
    source(d, '연금은 작년 한 해 받은 돈으로 봄 · 내년에도 2.1% 오른다고 가정')

@board
def p3_nov_notice(im):
    d = ImageDraw.Draw(im); title(d, '11월에 오는 고지서·통지', 110)
    x0, x1, y0 = 620, 1300, 220
    d.line([(x0, y0), ((x0 + x1) // 2, y0 + 170), (x1, y0)], fill=(150, 142, 130), width=6)   # 봉투 날개만(칸 없이)
    T(d, (W // 2, 470), '이자·배당 같은 소득', 64, INK, F_B)
    big(d, 640, '11월부터 작년 소득으로 봐요', 136, seed=251)
    T(d, (W // 2, 860), '그달 고지서나 통지를 꼭 보세요', 64, INK, F_X)
    source(d, '국민건강보험공단 · 연금은 1월, 이자·배당 등은 11월에 판정 기준 해가 넘어감')

@board
def p3_1000_line(im):
    d = ImageDraw.Draw(im); title(d, '이자·배당 한 해 1천만원 선', 110)
    base, top = 880, 330; Y = lambda v: base - (base - top) * v / 1300
    yl = Y(1000)
    hatch_bar(im, (560, Y(999), 820, base), KRAFT, seed=180); hatch_bar(im, (1100, Y(1100), 1360, base), OR, seed=181)
    d = ImageDraw.Draw(im)
    xx = 420
    while xx < 1520: d.line([(xx, yl), (min(xx + 26, 1520), yl)], fill=INK, width=5); xx += 44
    T(d, (1540, yl), '1천만원', 48, INK, F_X, 'lm')
    T(d, (690, base + 50), '999만원', 50, INK, F_B); T(d, (1230, base + 50), '1,100만원', 50, INK, F_B)
    T(d, (690, Y(999) - 70), '안 더함', 80, INK, F_X); T(d, (1230, Y(1100) - 90), '전부 더함', 130, OR, F_X)
    source(d, '보험료 계산 기준 · 세금 떼기 전 · 피부양자 판정도 같은지는 공단에 확인(1577-1000)')

@board
def p3_mix_calc(im):
    d = ImageDraw.Draw(im); title(d, '예: 연금 + 이자·배당', 110)
    pair(d, W // 2, 250, '국민연금 한 해', 58, INK, F_B, '1,000만원', 66, INK, F_X, 50)
    pair(d, W // 2, 360, '+ 이자·배당', 58, INK, F_B, '1,100만원', 66, INK, F_X, 50)
    d.line([(520, 430), (1400, 430)], fill=INK, width=4)
    pair(d, W // 2, 500, '합계', 58, INK, F_B, '2,100만원', 66, INK, F_X, 50)
    T(d, (W // 2, 600), '2천만원 넘음 → 피부양자 탈락', 50, INK, F_B)
    x, w = pair(d, W // 2, 770, '보험료', 62, INK, F_B, '매달 약 11만원', 140, OR, F_X, 40)
    hand_under(d, x, x + w, 850, seed=191)
    source(d, '연금의 절반 + 이자·배당 전부 · 장기요양 포함 · 재산이 거의 없을 때')

@board
def p3_scale_999(im):
    d = ImageDraw.Draw(im); title(d, '연금 한 해 1,800만원에 이자·배당을 더하면', 110)
    cx, py, tilt = W // 2, 250, 30
    lx, rx = cx - 500, cx + 480; ly, ry = py - tilt, py + tilt
    d.line([(cx, py), (cx, 880)], fill=INK, width=12); d.polygon([(cx - 90, 910), (cx + 90, 910), (cx, 850)], fill=INK)
    d.line([(lx, ly), (rx, ry)], fill=INK, width=12); d.ellipse((cx - 16, py - 16, cx + 16, py + 16), fill=INK)
    for x, y in ((lx, ly), (rx, ry)):
        d.line([(x, y), (x - 210, y + 100)], fill=GREY, width=3); d.line([(x, y), (x + 210, y + 100)], fill=GREY, width=3)
        d.arc((x - 230, y + 40, x + 230, y + 160), 0, 180, fill=INK, width=8)
    T(d, (lx, ly + 210), '이자·배당 999만원', 44, INK, F_B)
    pair(d, lx, ly + 310, '안 셈', 64, GREY, F_X, '→ 소득으로 세는 돈 1,800만원', 40, GREY, F_B)
    T(d, (rx, ry + 210), '이자·배당 1,100만원', 44, INK, F_B)
    T(d, (rx, ry + 300), '전부 더함', 80, INK, F_X)
    T(d, (rx, ry + 385), '1,800 + 1,100 = 2,900만원', 40, INK, F_B)
    T(d, (rx, ry + 440), '기준 2천만원 넘음 → 탈락하면', 40, INK, F_B)
    s = '월 13만 6천원'; ax = rx + 50; sz = TF(d, (ax, ry + 560), s, 130, OR, F_X, maxw=780)
    hand_under(d, ax - wd(s, sz) / 2, ax + wd(s, sz) / 2, ry + 560 + sz * 0.55, seed=1401)
    source(d, '재산 0일 때 · 135,579원(건강보험 7.19% + 장기요양 13.14%) · 999만원은 공단 확인 권함')

@board
def p3_property(im):
    d = ImageDraw.Draw(im); title(d, '집 같은 재산이 있으면', 110)
    T(d, (W // 2, 200), '재산 과세표준(시세가 아니라 재산세 매기는 기준 금액)', 40, GREY, F_M)
    rows = (('5억 4천만원 이하', '소득 기준 2천만원'), ('5억 4천만원 ~ 9억원', '소득 기준 1천만원'), ('9억원 넘음', '피부양자 안 됨'))
    cx = 700
    for i, (a, b) in enumerate(rows):
        y = 360 + i * 230
        if i: d.line([(160, y - 115), (1760, y - 115)], fill=LINE, width=2)
        T(d, (cx - 12, y), a, 60, INK, F_X, 'rm')
        T(d, (cx + 12, y), b, 136 if i == 1 else 62, OR if i == 1 else INK, F_X, 'lm')
    source(d, '국민건강보험법 시행규칙 별표 1의2 · 탈락하면 재산분 보험료가 따로 붙음')

@board
def p3_couple(im):
    d = ImageDraw.Draw(im); title(d, '부부는 한 사람씩 따로 따져요', 110)
    for i, (who, a, b) in enumerate((('한 분', '연금 월 170만원', '한 해 2,040만원'), ('배우자', '연금 월 50만원', '한 해 600만원'))):
        y = 260 + i * 130
        x, w = pair(d, 820, y, who, 48, GREY, F_B, a + ' · ' + b, 56, INK, F_X, 30)
        mx = x + w + 70
        if i == 0: hand_x(d, mx, y, 30, INK, 9, 1); T(d, (mx + 50, y), '2천만 넘음', 40, INK, F_B, 'lm')
        else: hand_o(d, mx, y, 32, GREY, 7, 2); hand_x(d, mx, y, 36, OR, 10, 3); T(d, (mx + 50, y), '혼자면 ○', 40, GREY, F_B, 'lm')
    q = '합쳐서 2천만원과 비교?'; T(d, (W // 2, 560), q, 56, GREY, F_B)
    qw = wd(q, 56, F_B); d.line([(W // 2 - qw / 2 - 10, 563), (W // 2 + qw / 2 + 10, 556)], fill=INK, width=6)
    big(d, 760, '한 분이 넘으면 둘 다 빠져요', 140, seed=1502)
    source(d, '국민건강보험법 시행규칙 [별표 1의2] 제1호라목 · 기혼자는 부부 모두 기준을 충족해야 함')

@board
def p3_three_roads(im):
    d = ImageDraw.Draw(im); title(d, '이런 분은 기준이 달라요', 110)
    roads = (('집이 있다', '재산 과세표준을 봄'), ('사업소득이 있다', '더 엄격'), ('부부라면', '각자 따지고, 한 사람만 넘어도 같이 빠짐'))
    for i, (a, b) in enumerate(roads):
        y = 300 + i * 230
        if i: d.line([(160, y - 115), (1760, y - 115)], fill=LINE, width=2)
        T(d, (160, y), a, 130 if i == 0 else 76, OR if i == 0 else INK, F_X, 'lm'); T(d, (1760, y), b, 48, INK, F_B, 'rm')

@board
def p3_early_q(im):
    d = ImageDraw.Draw(im)
    T(d, (W // 2, 280), '피부양자를 지키려면', 60, GREY, F_B)
    T(d, (W // 2, 440), '연금을 일찍 당겨 받아서', 96, INK, F_X)
    T(d, (W // 2, 640), '줄이면 되지 않을까?', 140, OR, F_X)
    T(d, (W // 2, 880), '이런 생각이 드실 수 있어요', 46, GREY, F_M)

@board
def p3_scale(im):
    d = ImageDraw.Draw(im); title(d, '연금을 일찍 당겨 받으면', 110)
    cx = W // 2; d.line([(cx, 300), (cx, 560)], fill=INK, width=10); d.polygon([(cx - 90, 560), (cx + 90, 560), (cx, 490)], fill=INK)
    d.line([(cx - 480, 330), (cx + 480, 330)], fill=INK, width=10)
    for sx in (-1, 1):
        x = cx + sx * 440; d.line([(x, 330), (x - 160, 470)], fill=GREY, width=4); d.line([(x, 330), (x + 160, 470)], fill=GREY, width=4)
        d.arc((x - 220, 400, x + 220, 540), 0, 180, fill=INK, width=8)
    T(d, (cx - 440, 640), '한 해 당길 때마다', 50, INK, F_B); T(d, (cx - 440, 740), '평생 6% 줄어듦', 72, INK, F_X)
    T(d, (cx + 440, 640), '탈락하면 보험료', 50, INK, F_B); TF(d, (cx + 440, 760), '월 약 6만 8천원', 136, OR, F_X, maxw=950)
    T(d, (W // 2, 930), '일찍 받은 연금도 피부양자 소득에 똑같이 들어가요', 42, INK, F_M)

@board
def p3_four_years(im):
    d = ImageDraw.Draw(im); title(d, '미뤄 받아도, 해마다 2.1%씩 오르면', 110)
    rows = (('시작', '1,900만'), ('1번 오름', '1,940만'), ('2번 오름', '1,981만'), ('3번 오름', '2,022만'))
    nums = (1900, 1939.9, 1980.6, 2022.2); lo, hi = 1800, 2060; X = lambda v: 160 + 700 * (v - lo) / (hi - lo)
    xt = X(2000); labs = []
    for i, ((a, b), v) in enumerate(zip(rows, nums)):
        y = 330 + i * 150 + (40 if i == 3 else 0)
        hatch_bar(im, (160, y - 36, X(v), y + 36), OR if i == 3 else KRAFT, seed=220 + i); d = ImageDraw.Draw(im)
        sz = 130 if i == 3 else 60
        labs.append((X(v), y, b + '원', sz, OR if i == 3 else INK, a))
    yy = 250
    while yy < 900: d.line([(xt, yy), (xt, min(yy + 26, 900))], fill=INK, width=5); yy += 44
    T(d, (xt, 220), '2천만원', 44, INK, F_X)
    for xv, y, b, sz, col, a in labs:   # 점선 위에 종이색 테두리로 글자
        d.text((xv + 30, y), b, font=font(F_X, sz), fill=col, anchor='lm', stroke_width=8, stroke_fill=(238, 238, 236))
        T(d, (xv + 30 + wd(b, sz) + 16, y + (20 if sz > 100 else 4)), a, 44, INK, F_B, 'lm')
    source(d, '한 해 받는 연금 · 해마다 2.1%씩 오른다고 가정')

@board
def p3_take_notice(im):
    d = ImageDraw.Draw(im); title(d, '오늘 할 일은 하나', 110)
    x0, x1, y0 = 640, 1280, 200
    d.line([(x0, y0), ((x0 + x1) // 2, y0 + 150), (x1, y0)], fill=(150, 142, 130), width=6)
    T(d, (W // 2, 430), '국민연금 통지서', 80, INK, F_X)
    T(d, (W // 2, 580), '꺼내서, 내년에 연금이 물가만큼 오르면', 60, INK, F_B)
    big(d, 760, '한 해 2천만원 넘는지 셈해 보기', 136, seed=371)

def over_up(src, small, big_s, out, t=2.0):
    """p3fix1103.over와 같은 꼴 — 큰 글자 아래 끝을 자막 띠(y 864) 위로: 작은 줄 742→600, 큰 줄 880→730, 그라데이션 45%→35%부터."""
    im = FX.frame(src, t)
    g = Image.new('L', (W, H), 0); gd = ImageDraw.Draw(g)
    for y in range(int(H * 0.35), H):
        gd.line([(0, y), (W, y)], fill=int(200 * ((y - H * 0.35) / (H * 0.65)) ** 1.1))
    im.paste((0, 0, 0), (0, 0), g); d = ImageDraw.Draw(im)
    d.text((W // 2, 600), small, font=font(F_B, 66), fill=(255, 255, 255), anchor='mm', stroke_width=5, stroke_fill=(0, 0, 0))
    d.text((W // 2, 730), big_s, font=font(F_X, 112), fill=OR, anchor='mm', stroke_width=7, stroke_fill=(0, 0, 0))
    bb = d.textbbox((W // 2, 730), big_s, font=font(F_X, 112), anchor='mm', stroke_width=7)
    im.save(os.path.join(FX.PUB, 'over', out)); print('over', out, '큰 글자 아래 끝 y', bb[3], '(자막 띠 864)')

def main(names):
    for n in names or list(B):
        im = canvas(); B[n](im); im.save(os.path.join(OUT, n + '.png')); print(n)
    if not names:
        over_up('ai/notice_magnifier.png', '자녀 직장보험 피부양자라면', '건강보험료 한 푼도 안 내요', 'p3_over_r03.png')
        over_up('stock/phone_pickup.mp4', '999만원처럼 선 근처라면 먼저', '공단 고객센터 1577-1000', 'p3_over_r31.png', 3.0)
        over_up('stock/apartment_windows.mp4', '재산세 고지서의 과세표준(시세 아님)', '과세표준 5억 4천만원 넘으면', 'p3_over_r34.png')

if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')
    main(sys.argv[1:])
