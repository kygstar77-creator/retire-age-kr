"""P-3 장면 판 24장 — visual-designer 2026-10-29. K-1 판(k1boards.py)과 같은 꼴·같은 부품.
구겨진 종이 바탕 · 찢은 종이 조각 · 주황 #FF5A00은 그 화면의 답 하나 · 손으로 그린 동그라미·밑줄.
숫자는 ep/P-3/calc_out.txt 값만(반올림은 대본 말 그대로: 6만 8천원쯤·800만원 넘음 등). 판은 '답이 열린 마지막 모습'.
사용: py -3.12 p3boards.py [이름 ...]   (없으면 전부) → work/video/public/bg/p3/board/<이름>.png
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'K-1-shots'))
import k1boards as K
from k1boards import (W, H, INK, GREY, OR, KRAFT, KRAFT_L, FADE, F_B, F_M, F_X, font, canvas, T, title, source,
                      torn, hand_ellipse, hand_under, hand_check, hand_arrow)
from PIL import ImageDraw

OUT = os.path.join(K.WORK, 'video', 'public', 'bg', 'p3', 'board')
PAPER_N = (238, 230, 212); MEMO = (246, 236, 178)
SRC_NHIS = '국민건강보험공단 · 2026년 건강보험료율 7.19% · 장기요양 13.14%'
B = {}
def board(fn):
    B[fn.__name__] = fn; return fn

def width(s, size, f=F_X): return font(f, size).getlength(s)

def strike(d, x0, x1, y, color=INK, w=7):
    d.line([(x0, y + 4), (x1, y - 4)], fill=color, width=w)

@board
def p3_hook(im):
    d = ImageDraw.Draw(im)
    T(d, (W // 2, 330), '국민연금 + 1만원', 110, INK, F_X)
    hand_arrow(d, (W // 2, 440), (W // 2, 560), INK, 8)
    T(d, (W // 2, 680), '건강보험료', 80, INK, F_B)
    s = '매달 7만원 가까이'; T(d, (W // 2, 820), s, 120, OR, F_X)
    hand_under(d, W // 2 - width(s, 120) / 2, W // 2 + width(s, 120) / 2, 900, seed=21)

@board
def p3_condition(im):
    d = ImageDraw.Draw(im); title(d, '예를 들어 이런 분이라면', 130)
    cards = (('나이', '65세'), ('건강보험', '자녀 직장보험\n피부양자'), ('국민연금', '월 165만원'), ('재산', '거의 없음'))
    for i, (a, b) in enumerate(cards):
        x0 = 150 + i * 420; torn(im, (x0, 330, x0 + 360, 820), KRAFT_L if i != 2 else PAPER_N, seed=40 + i)
        d = ImageDraw.Draw(im)
        T(d, (x0 + 180, 420), a, 46, GREY)
        lines = b.split('\n')
        for k, ln in enumerate(lines):
            T(d, (x0 + 180, 600 + (k - (len(lines) - 1) / 2) * 76), ln, 62 if len(lines) > 1 else 74, INK, F_X)
    hand_ellipse(d, (150 + 2 * 420 - 20, 520, 150 + 2 * 420 + 380, 690), seed=44)
    T(d, (W // 2, 930), '소득 기준은 나이와 상관없이 같아요', 46, INK, F_M)

@board
def p3_answer(im):
    d = ImageDraw.Draw(im); title(d, '답부터', 130)
    rows = (('국민연금 월 166만원', '0원', INK), ('국민연금 월 167만원', '매달 약 6만 8천원', OR))
    for i, (a, b, c) in enumerate(rows):
        y = 380 + i * 300
        torn(im, (220, y - 110, 1700, y + 110), KRAFT_L if i == 0 else PAPER_N, seed=50 + i); d = ImageDraw.Draw(im)
        T(d, (560, y), a, 62, INK, F_B)
        hand_arrow(d, (930, y), (1040, y), INK, 6)
        T(d, (1390, y), b, 72 if i else 110, c, F_X)
    hand_ellipse(d, (1070, 680 - 110, 1710, 680 + 110), seed=53)
    source(d, '건강보험료 + 장기요양보험료 · 재산이 거의 없을 때')

@board
def p3_kin_q(im):
    d = ImageDraw.Draw(im)
    torn(im, (360, 250, 1560, 830), MEMO, seed=60); d = ImageDraw.Draw(im)
    T(d, (W // 2, 340), '지식iN 질문 (요지)', 44, GREY, F_M)
    T(d, (W // 2, 500), '국민연금이 2천만원을 넘으면', 72, INK, F_X)
    T(d, (W // 2, 640), '건보료 부담은 어느 정도인가요?', 72, INK, F_X)
    hand_under(d, 560, 1360, 700, INK, 6, seed=61)
    T(d, (W // 2, 920), '질문 원문이 아니라 뜻만 옮겼어요', 36, GREY, F_M)

@board
def p3_ruler(im):
    d = ImageDraw.Draw(im); title(d, '피부양자 소득 기준', 120)
    x0, x1, y = 260, 1660, 560
    torn(im, (x0 - 40, y - 70, x1 + 40, y + 70), KRAFT_L, seed=70); d = ImageDraw.Draw(im)
    for k in range(0, 31):
        x = x0 + (x1 - x0) * k / 30; L = 60 if k % 10 == 0 else (36 if k % 5 == 0 else 20)
        d.line([(x, y - 70), (x, y - 70 + L)], fill=INK, width=4 if k % 10 == 0 else 2)
    for k, lab in ((0, '0원'), (10, '1천만원'), (20, '2천만원'), (30, '3천만원')):
        x = x0 + (x1 - x0) * k / 30; T(d, (x, y + 120), lab, 40, GREY if k != 20 else INK, F_B)
    xs = x0 + (x1 - x0) * 20 / 30
    d.line([(xs, y - 190), (xs, y + 80)], fill=OR, width=10)
    T(d, (xs, y - 240), '한 해 2천만원', 64, INK, F_X)
    T(d, (xs, 860), '한 달 166만원 남짓', 96, OR, F_X)
    source(d, '국민건강보험법 시행규칙 별표 1의2 · 2천만원 ÷ 12 = 약 166.7만원')

@board
def p3_public_private(im):
    d = ImageDraw.Draw(im); title(d, '어디서 받는 연금인가', 120)
    cols = (('국민연금', '받은 돈 전부 셈', OR, PAPER_N), ('연금저축 · IRP', '소득에 안 넣음', INK, KRAFT_L))
    for i, (a, b, c, bg) in enumerate(cols):
        x0 = 220 + i * 780; torn(im, (x0, 290, x0 + 700, 860), bg, seed=80 + i); d = ImageDraw.Draw(im)
        T(d, (x0 + 350, 450), a, 80, INK, F_X)
        T(d, (x0 + 350, 680), b, 66, c, F_X)
        if i == 0: hand_under(d, x0 + 350 - width(b, 66) / 2, x0 + 350 + width(b, 66) / 2, 740, seed=82)
    source(d, '국민건강보험공단 안내 · 국민연금은 세금 떼는지와 상관없이 전부')

def calc_rows(d, rows, y0=300, step=130, xl=560, xr=1380):
    for i, (a, b, c) in enumerate(rows):
        y = y0 + i * step
        T(d, (xl, y), a, 60, INK, F_B, 'rm'); T(d, (xl + 60, y), b, 60, GREY, F_B, 'lm')
        if c: T(d, (xr, y), c, 70, INK, F_X, 'lm')

@board
def p3_calc_health(im):
    d = ImageDraw.Draw(im); title(d, '건강보험료 계산', 120)
    torn(im, (300, 230, 1620, 860), PAPER_N, seed=90); d = ImageDraw.Draw(im)
    T(d, (W // 2, 330), '국민연금 월 167만원', 76, INK, F_X)
    T(d, (W // 2, 470), '× 절반  (보험료 매길 땐 연금의 절반만)', 54, INK, F_B)
    T(d, (W // 2, 590), '× 7.19%  (건강보험료율)', 54, INK, F_B)
    d.line([(520, 660), (1400, 660)], fill=INK, width=4)
    s = '= 약 6만원'; T(d, (W // 2, 760), s, 104, OR, F_X)
    source(d, SRC_NHIS)

@board
def p3_calc_ltc(im):
    d = ImageDraw.Draw(im); title(d, '고지서에는 하나 더', 120)
    torn(im, (300, 230, 1620, 900), PAPER_N, seed=91); d = ImageDraw.Draw(im)
    T(d, (560, 340), '건강보험료', 62, INK, F_B, 'lm'); T(d, (1360, 340), '약 6만원', 66, INK, F_X, 'rm')
    T(d, (560, 470), '+ 장기요양보험료', 62, INK, F_B, 'lm'); T(d, (1360, 470), '약 8천원', 66, INK, F_X, 'rm')
    T(d, (560, 560), '(건강보험료 × 13.14%)', 40, GREY, F_M, 'lm')
    d.line([(520, 630), (1400, 630)], fill=INK, width=4)
    T(d, (560, 760), '합계', 66, INK, F_B, 'lm')
    s = '매달 약 6만 8천원'; T(d, (1360, 760), s, 76, OR, F_X, 'rm')
    hand_ellipse(d, (1360 - width(s, 76) - 40, 690, 1410, 830), seed=92)
    source(d, SRC_NHIS)

@board
def p3_step_table(im):
    d = ImageDraw.Draw(im); title(d, '국민연금 월액별 건보료(재산 거의 없을 때)', 110)
    rows = (('월 166만원', '0원'), ('월 167만원', '약 6만 8천원'), ('월 170만원', '약 6만 9천원'), ('월 200만원', '약 8만 1천원'))
    T(d, (W // 2 - 60, 250), '국민연금', 40, GREY, F_M, 'rm'); T(d, (W // 2 + 60, 250), '매달 내는 보험료', 40, GREY, F_M, 'lm')
    for i, (a, b) in enumerate(rows):
        y = 360 + i * 140
        if i: d.line([(460, y - 70), (1460, y - 70)], fill=(170, 160, 150), width=2)
        T(d, (W // 2 - 60, y), a, 66, INK, F_B, 'rm')
        T(d, (W // 2 + 60, y), b, 74, OR if i == 1 else INK, F_X, 'lm')
    d.line([(W // 2, 300), (W // 2, 920)], fill=(170, 160, 150), width=2)
    hand_arrow(d, (1500, 380), (1500, 490), INK, 7); T(d, (1540, 435), '여기서 뜀', 46, INK, F_X, 'lm')  # 심사 1차: 주황 두 번 → 답만 주황
    source(d, '건강보험료 + 장기요양보험료 · ' + SRC_NHIS.split(' · ', 1)[1])

@board
def p3_10years(im):
    d = ImageDraw.Draw(im); title(d, '매달 6만 8천원쯤을 10년 동안', 110)
    cw, ch, gx, gy = 96, 52, 14, 14; x0 = (W - (12 * cw + 11 * gx)) // 2; y0 = 220
    for yr in range(10):
        T(d, (x0 - 30, y0 + yr * (ch + gy) + ch // 2), f'{yr + 1}년', 30, GREY, F_M, 'rm')
        for m in range(12):
            x = x0 + m * (cw + gx); y = y0 + yr * (ch + gy)
            d.rounded_rectangle((x, y, x + cw, y + ch), 6, fill=KRAFT if (yr + m) % 2 else KRAFT_L)
    s = '모두 더하면 800만원 넘음'; T(d, (W // 2, 935), s, 84, OR, F_X)
    source(d, '월 167만원 기준 67,926원 × 120달 = 약 815만원 · 보험료율이 그대로일 때')

@board
def p3_raise(im):
    d = ImageDraw.Draw(im); title(d, '국민연금은 해마다 1월에 물가만큼', 110)
    base, top = 880, 260; vmax = 175; lo = 140
    Y = lambda v: base - (base - top) * (v - lo) / (vmax - lo)
    torn(im, (520, Y(165), 820, base), KRAFT, seed=110); torn(im, (1100, Y(168.5), 1400, base), PAPER_N, seed=111)
    d = ImageDraw.Draw(im)
    T(d, (670, Y(165) + 90), '월 165만원', 56, INK, F_X); T(d, (670, base + 50), '올해', 46)
    T(d, (1250, Y(168.5) + 90), '168만원 남짓', 52, INK, F_X); T(d, (1250, base + 50), '내년', 46)
    hand_arrow(d, (840, Y(165) + 180), (1080, Y(168.5) + 180), INK, 6); T(d, (960, Y(165) + 240), '+2.1%', 50, INK, F_B)
    yt = Y(166.7); xx = 440
    while xx < 1500: d.line([(xx, yt), (min(xx + 26, 1500), yt)], fill=INK, width=6); xx += 44
    T(d, (1520, yt), '기준 166만원 남짓', 44, INK, F_X, 'lm')  # 심사 1차: 주황은 동그라미(답)만
    hand_ellipse(d, (1070, Y(168.5) + 30, 1430, Y(168.5) + 150), seed=112)
    source(d, '2026년 국민연금 물가 반영 2.1% · 내년도 같은 비율로 오른다고 가정')

@board
def p3_164_163(im):
    d = ImageDraw.Draw(im); title(d, '올해 받는 연금이 이만큼이면', 120)
    rows = (('올해 월 164만원', '내년 약 167.4만원', '기준 넘음', OR), ('올해 월 163만원', '내년 약 166.4만원', '안 넘음', INK))
    for i, (a, b, c, col) in enumerate(rows):
        y = 400 + i * 280
        torn(im, (180, y - 100, 1740, y + 100), PAPER_N if i == 0 else KRAFT_L, seed=120 + i); d = ImageDraw.Draw(im)
        T(d, (240, y), a, 62, INK, F_X, 'lm'); hand_arrow(d, (760, y), (860, y), INK, 6)
        T(d, (890, y), b, 56, INK, F_B, 'lm'); T(d, (1700, y), c, 72, col, F_X, 'rm')
    hand_ellipse(d, (1400, 400 - 90, 1730, 400 + 90), seed=123)
    source(d, '2.1%씩 오른다고 가정 · 기준 월 약 166.7만원(한 해 2천만원)')

@board
def p3_trap_cut(im):
    d = ImageDraw.Draw(im)
    torn(im, (360, 220, 1560, 600), KRAFT_L, seed=130); d = ImageDraw.Draw(im)
    d.polygon([(700, 590), (780, 590), (660, 700)], fill=KRAFT_L)
    s = '"탈락해도 처음 몇 년은 깎아 준대"'; T(d, (W // 2, 410), s, 64, INK, F_B)
    strike(d, W // 2 - width(s, 64, F_B) / 2, W // 2 + width(s, 64, F_B) / 2, 410)
    T(d, (W // 2, 800), '이제 끝났어요', 120, OR, F_X)
    source(d, '2022년 9월부터 정해진 기간에만 있던 경감 · 2026년 8월분으로 끝')

@board
def p3_cut_steps(im):
    d = ImageDraw.Draw(im); title(d, '깎아 주던 비율 (그 사이 처음 탈락한 사람만)', 110)
    steps = (('1년째', '80%'), ('2년째', '60%'), ('3년째', '40%'), ('4년째', '20%'))
    base = 860; bw = 250; gap = 80; x = (W - (5 * bw + 4 * gap)) // 2
    for i, (a, b) in enumerate(steps):
        h = 520 - i * 110
        torn(im, (x, base - h, x + bw, base), KRAFT if i < 3 else KRAFT_L, seed=140 + i); d = ImageDraw.Draw(im)
        T(d, (x + bw // 2, base - h - 50), b, 70, INK, F_X); T(d, (x + bw // 2, base + 50), a, 44)
        x += bw + gap
    T(d, (x + bw // 2, base - 120), '끝', 120, OR, F_X); T(d, (x + bw // 2, base + 50), '2026년 8월분까지', 38, OR, F_B)
    hand_ellipse(d, (x - 10, base - 240, x + bw + 10, base - 10), seed=145)
    source(d, '2022년 9월 시작 · 지금 새로 탈락하면 경감 없음')

@board
def p3_calendar_rule(im):
    d = ImageDraw.Draw(im); title(d, '피부양자 판정 때 보는 해', 110)
    x0, x1, xm = 360, 1640, 1180; ytop = 250
    torn(im, (x0 - 20, ytop, x1 + 20, 900), PAPER_N, seed=150); d = ImageDraw.Draw(im)
    T(d, ((x0 + 520 + xm) // 2, ytop + 70), '1월 ~ 10월', 52, INK, F_X); T(d, ((xm + x1) // 2, ytop + 70), '11월 ~ 12월', 52, INK, F_X)
    d.line([(x0, ytop + 130), (x1, ytop + 130)], fill=INK, width=3); d.line([(xm, ytop + 20), (xm, 880)], fill=INK, width=3)
    d.line([(x0 + 520, ytop + 20), (x0 + 520, 880)], fill=(170, 160, 150), width=2)
    for i, (lab, a, b) in enumerate((('국민연금', '작년 연금', '작년 연금'), ('이자·배당', '재작년 소득', '작년 소득'))):
        y = ytop + 290 + i * 260
        T(d, (x0 + 260, y), lab, 58, INK, F_X)
        T(d, ((x0 + 520 + xm) // 2, y), a, 58, INK, F_B); T(d, ((xm + x1) // 2, y), b, 58, OR if i == 1 else INK, F_B)
        if i == 0: d.line([(x0, y + 130), (x1, y + 130)], fill=(170, 160, 150), width=2)
    hand_ellipse(d, (xm + 20, ytop + 290 + 260 - 80, x1 - 10, ytop + 290 + 260 + 80), seed=151)
    source(d, '국민건강보험공단 · 연금은 1월, 이자·배당 등은 11월에 판정 기준 해가 넘어감')

@board
def p3_timeline(im):
    d = ImageDraw.Draw(im); title(d, '오른 연금은 언제 반영되나', 120)
    pts = (('올해', '월 165만원'), ('내년', '연금 오름\n168만원 남짓'), ('그다음 해', '판정 · 탈락\n고지서 시작'))
    xs = (380, W // 2, 1540); y = 560
    d.line([(xs[0], y), (xs[2], y)], fill=INK, width=6)
    for i, ((a, b), x) in enumerate(zip(pts, xs)):
        col = OR if i == 2 else INK
        d.ellipse((x - 26, y - 26, x + 26, y + 26), fill=col)
        T(d, (x, y - 110), a, 70, col, F_X)
        for k, ln in enumerate(b.split('\n')): T(d, (x, y + 110 + k * 74), ln, 54, col, F_B)
    hand_ellipse(d, (1300, y - 200, 1780, y + 270), seed=160)
    source(d, '연금은 작년 한 해 받은 돈으로 봄 · 내년에도 2.1% 오른다고 가정')

@board
def p3_kin_999(im):
    d = ImageDraw.Draw(im)
    torn(im, (360, 180, 1560, 560), MEMO, seed=170); d = ImageDraw.Draw(im)
    T(d, (W // 2, 260), '지식iN 질문 (요지)', 40, GREY, F_M)
    T(d, (W // 2, 400), '이자·배당이 999만원이면 0원으로 보나요?', 64, INK, F_X)
    for i, col in enumerate((KRAFT_L, KRAFT, FADE)):
        x0 = 420 + i * 380; torn(im, (x0, 650, x0 + 320, 900), col, seed=171 + i); d = ImageDraw.Draw(im)
        T(d, (x0 + 160, 740), f'답 {i + 1}', 40, GREY, F_M); T(d, (x0 + 160, 830), '?', 110, INK, F_X)
    T(d, (W // 2, 990), '답이 서로 엇갈렸어요', 48, INK, F_B)

@board
def p3_1000_line(im):
    d = ImageDraw.Draw(im); title(d, '이자·배당 한 해 1천만원 선', 110)
    base, top = 880, 250; Y = lambda v: base - (base - top) * v / 1300
    yl = Y(1000)
    torn(im, (560, Y(999), 820, base), KRAFT_L, seed=180); torn(im, (1100, Y(1100), 1360, base), OR, seed=181)
    d = ImageDraw.Draw(im)
    xx = 420
    while xx < 1520: d.line([(xx, yl), (min(xx + 26, 1520), yl)], fill=INK, width=5); xx += 44
    T(d, (1540, yl), '1천만원', 48, INK, F_X, 'lm')
    T(d, (690, base + 50), '999만원', 50, INK, F_B); T(d, (1230, base + 50), '1,100만원', 50, INK, F_B)
    T(d, (690, Y(999) + 120), '안 더함', 60, INK, F_X); T(d, (1230, Y(1100) + 140), '전부', 70, (255, 255, 255), F_X)
    T(d, (1230, Y(1100) + 220), '더함', 70, (255, 255, 255), F_X)
    source(d, '보험료 계산 기준 · 세금 떼기 전 · 피부양자 판정도 같은지는 공단에 확인(1577-1000)')

@board
def p3_mix_calc(im):
    d = ImageDraw.Draw(im); title(d, '예: 연금 + 이자·배당', 120)
    torn(im, (300, 230, 1620, 940), PAPER_N, seed=190); d = ImageDraw.Draw(im)
    T(d, (560, 340), '국민연금 한 해', 58, INK, F_B, 'lm'); T(d, (1360, 340), '1,000만원', 66, INK, F_X, 'rm')
    T(d, (560, 460), '+ 이자·배당', 58, INK, F_B, 'lm'); T(d, (1360, 460), '1,100만원', 66, INK, F_X, 'rm')
    d.line([(520, 530), (1400, 530)], fill=INK, width=4)
    T(d, (560, 600), '합계', 58, INK, F_B, 'lm'); T(d, (1360, 600), '2,100만원', 66, INK, F_X, 'rm')
    T(d, (W // 2, 690), '2천만원 넘음 → 피부양자 탈락', 50, INK, F_B)
    T(d, (560, 810), '보험료', 62, INK, F_B, 'lm')
    s = '매달 약 11만원'; T(d, (1360, 810), s, 90, OR, F_X, 'rm')
    hand_under(d, 1360 - width(s, 90), 1360, 875, seed=191)
    source(d, '연금의 절반 + 이자·배당 전부 · 장기요양 포함 · 재산이 거의 없을 때')

@board
def p3_three_roads(im):
    d = ImageDraw.Draw(im); title(d, '이런 분은 기준이 달라요', 120)
    roads = (('집이 있다', '재산 과세표준을 봄'), ('사업소득이 있다', '더 엄격'), ('부부라면', '각자 따지고, 한 사람만 넘어도 같이 빠짐'))
    for i, (a, b) in enumerate(roads):
        y = 340 + i * 220
        torn(im, (300, y - 85, 1620, y + 85), KRAFT_L if i else PAPER_N, seed=200 + i); d = ImageDraw.Draw(im)
        T(d, (360, y), a, 66, OR if i == 0 else INK, F_X, 'lm'); T(d, (1580, y), b, 46, INK, F_B, 'rm')

@board
def p3_property(im):
    d = ImageDraw.Draw(im); title(d, '집 같은 재산이 있으면', 110)
    T(d, (W // 2, 210), '재산 과세표준(시세가 아니라 재산세 매기는 기준 금액)', 40, GREY, F_M)
    rows = (('5억 4천만원 이하', '소득 기준 2천만원'), ('5억 4천만원 ~ 9억원', '소득 기준 1천만원'), ('9억원 넘음', '피부양자 안 됨'))
    for i, (a, b) in enumerate(rows):
        y = 380 + i * 190
        torn(im, (260, y - 75, 1660, y + 75), PAPER_N if i == 1 else KRAFT_L, seed=210 + i); d = ImageDraw.Draw(im)
        T(d, (320, y), a, 60, INK, F_X, 'lm'); T(d, (1600, y), b, 62, OR if i == 1 else INK, F_X, 'rm')
    source(d, '국민건강보험법 시행규칙 별표 1의2 · 탈락하면 재산분 보험료가 따로 붙음')

@board
def p3_scale(im):
    d = ImageDraw.Draw(im); title(d, '연금을 일찍 당겨 받으면', 120)
    cx = W // 2; d.line([(cx, 360), (cx, 900)], fill=INK, width=10); d.polygon([(cx - 90, 900), (cx + 90, 900), (cx, 830)], fill=INK)
    d.line([(cx - 560, 420), (cx + 560, 420)], fill=INK, width=10)
    for sx in (-1, 1):
        x = cx + sx * 520; d.line([(x, 420), (x - 160, 600)], fill=GREY, width=4); d.line([(x, 420), (x + 160, 600)], fill=GREY, width=4)
        d.arc((x - 220, 520, x + 220, 680), 0, 180, fill=INK, width=8)
    T(d, (cx - 520, 760), '한 해 당길 때마다', 46, INK, F_B); T(d, (cx - 520, 840), '평생 6% 줄어듦', 66, INK, F_X)
    T(d, (cx + 520, 760), '탈락하면 보험료', 46, INK, F_B); T(d, (cx + 520, 840), '월 약 6만 8천원', 66, OR, F_X)
    T(d, (W // 2, 990), '일찍 받은 연금도 피부양자 소득에 똑같이 들어가요', 42, INK, F_M)

@board
def p3_four_years(im):
    d = ImageDraw.Draw(im); title(d, '미뤄 받아도, 해마다 2.1%씩 오르면', 110)
    vals = (('시작', '1,900만'), ('1번 오름', '1,940만'), ('2번 오름', '1,981만'), ('3번 오름', '2,022만'))
    base, top = 880, 300; lo, hi = 1800, 2060; Y = lambda v: base - (base - top) * (v - lo) / (hi - lo)
    nums = (1900, 1939.9, 1980.6, 2022.2); bw = 240; gap = 110; x = (W - (4 * bw + 3 * gap)) // 2
    for i, ((a, b), v) in enumerate(zip(vals, nums)):
        torn(im, (x, Y(v), x + bw, base), OR if i == 3 else KRAFT_L, seed=220 + i); d = ImageDraw.Draw(im)
        T(d, (x + bw // 2, Y(v) - 50 if i == 3 else Y(v) + 60), b + '원', 52, OR if i == 3 else INK, F_X); T(d, (x + bw // 2, base + 50), a, 42)
        x += bw + gap
    yt = Y(2000); xx = 260
    while xx < 1660: d.line([(xx, yt), (min(xx + 26, 1660), yt)], fill=INK, width=5); xx += 44
    T(d, (250, yt), '2천만원', 44, INK, F_X, 'rm')
    source(d, '한 해 받는 연금 · 해마다 2.1%씩 오른다고 가정')

@board
def p3_todo3(im):
    d = ImageDraw.Draw(im); title(d, '연금이 기준 근처라면', 120)
    cards = (('셈해 보기', '통지서 꺼내서\n내년 연금 × 1.021\n한 해 2천만원 넘나'), ('확인', '이자·배당이\n선 근처면\n1577-1000'), ('신청', '탈락 뒤 소득이\n줄었으면\n조정 신청'))
    for i, (a, b) in enumerate(cards):
        x0 = 210 + i * 520; torn(im, (x0, 260, x0 + 460, 900), PAPER_N if i == 0 else KRAFT_L, seed=230 + i); d = ImageDraw.Draw(im)
        T(d, (x0 + 230, 360), f'{i + 1}', 80, OR if i == 0 else INK, F_X)
        T(d, (x0 + 230, 470), a, 64, OR if i == 0 else INK, F_X)
        for k, ln in enumerate(b.split('\n')): T(d, (x0 + 230, 620 + k * 72), ln, 46, INK, F_B)

@board
def p3_calendar_nov(im):
    """r24: AI 달력(가짜 숫자·이상한 손 3/3 못 씀) → 종이 달력 판. 2026년 11월 실제 날짜(1일 일요일), 연필 동그라미는 1일 — 대본 '11월이 되면'."""
    d = ImageDraw.Draw(im)
    torn(im, (460, 110, 1460, 990), (250, 248, 242), seed=240); d = ImageDraw.Draw(im)
    T(d, (W // 2, 200), '2026년 11월', 72, INK, F_X)
    days = '일월화수목금토'; cw, ch = 128, 118; x0 = W // 2 - cw * 3.5; y0 = 300
    for k, c in enumerate(days): T(d, (x0 + cw * k + cw / 2, y0), c, 36, GREY, F_B)
    for n in range(1, 31):
        k = (n - 1) % 7; r = (n - 1) // 7; x = x0 + cw * k; y = y0 + 50 + ch * r
        d.rectangle((x, y, x + cw, y + ch), outline=(200, 194, 184), width=2)
        T(d, (x + 18, y + 30), str(n), 34, INK, F_M, 'lm')
    hand_ellipse(d, (x0 - 6, y0 + 40, x0 + cw + 6, y0 + 50 + ch + 10), OR, 8, seed=241)

@board
def p3_nov_notice(im):
    """r27: 스톡 'SAVE THE DATE' 카드(영어·청첩장 글자) 심사 1차 못함 → 종이 판. 흰 봉투 + 11월 통지에서 볼 것."""
    d = ImageDraw.Draw(im); title(d, '11월에 오는 고지서·통지', 120)
    x0, y0, x1, y1 = 520, 260, 1400, 760
    torn(im, (x0, y0, x1, y1), (250, 248, 242), seed=250); d = ImageDraw.Draw(im)
    d.line([(x0 + 10, y0 + 10), ((x0 + x1) // 2, y0 + 280), (x1 - 10, y0 + 10)], fill=(190, 182, 170), width=5)
    T(d, ((x0 + x1) // 2, y0 + 330), '이자·배당 같은 소득', 58, INK, F_B)
    T(d, ((x0 + x1) // 2, y0 + 410), '11월부터 작년 소득으로 봐요', 62, OR, F_X)
    T(d, (W // 2, 880), '그달 고지서나 통지를 꼭 보세요', 64, INK, F_X)
    source(d, '국민건강보험공단 · 연금은 1월, 이자·배당 등은 11월에 판정 기준 해가 넘어감')

def main(names):
    os.makedirs(OUT, exist_ok=True)
    for n in names or list(B):
        im = canvas(); B[n](im); im.save(os.path.join(OUT, n + '.png')); print(n)

if __name__ == '__main__':
    main(sys.argv[1:])
