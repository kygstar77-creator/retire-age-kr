"""P-3 새 말 28줄 화면 — visual-designer 2026-11-04 15시(운영실장 배차, backlog 29행 한 조각).
youtube-loop 11/3 17:00 script.md (화면 [판]/[표]) 새 꼬리표 5개 중 1장·2장 두 개를 만든다.
- p3_two_bars (script.md 40행 1장): 국민연금 100만 / 연금저축 66만 두 칸 막대 + 문턱 자 위 1,200만 점
- p3_four_rows (script.md 65행 2장): 167·170·180·200만 네 줄 표 + '10만원 더 → 4천원쯤'
11/4 17시: 3장 p3_cut_calendar(101행) · 5장 p3_scale_999(146행) · 6장 p3_couple(157행) 더함 — 시행규칙 부칙 제907호 제3조 기간(80%~2023.10분·60%~2024.10분·40%~2025.10분·20% 2025.11~2026.8분), calc_out 16행 135,579원.
숫자는 calc_out.txt 33·6·7·36행 값만(100만×12=1,200만·기준까지 800만 / 67,926·69,146·73,213·81,348 / 차 4,067원).
사용: py -3.12 p3new1104.py → work/video/public/bg/p3/board/<이름>.png
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', 'K-1-shots'))
import k1boards as K
from k1boards import W, H, INK, GREY, OR, KRAFT_L, F_B, F_M, F_X, font, canvas, T, title, source, torn, hand_ellipse, hand_under, hand_arrow
from PIL import ImageDraw

OUT = os.path.join(K.WORK, 'video', 'public', 'bg', 'p3', 'board')
PAPER_N = (238, 230, 212); LIGHT = (205, 198, 186)
def wd(s, size, f=F_X): return font(f, size).getlength(s)
B = {}
def board(fn): B[fn.__name__] = fn; return fn

@board
def p3_two_bars(im):   # 40행: 같은 166만원이라도 피부양자 소득으로 세는 건 국민연금뿐
    d = ImageDraw.Draw(im); title(d, '한 달 166만원 = 국민연금 100만 + 연금저축 66만', 120)
    # 왼쪽: 한 달 막대 두 칸(쌓기) — 국민연금은 셈, 연금저축은 안 셈
    bx0, bx1, base, scale = 180, 600, 900, 3.6   # 1만원 = 3.6px
    h1, h2 = 100 * scale, 66 * scale
    d.rectangle((bx0, base - h1, bx1, base), fill=KRAFT_L, outline=INK, width=4)
    for k in range(40, int(h2), 30):   # 연금저축 칸 왼쪽 가장자리 빗금(셈에서 빠짐), 칸 안에서만
        d.line([(bx0 + 4, base - h1 - k + 30), (bx0 + 34, base - h1 - k)], fill=LIGHT, width=3)
    d.rectangle((bx0, base - h1 - h2, bx1, base - h1), outline=GREY, width=4)
    T(d, ((bx0 + bx1) // 2, base - h1 / 2 - 34), '국민연금', 50, INK, F_X)
    T(d, ((bx0 + bx1) // 2, base - h1 / 2 + 34), '한 달 100만원', 50, INK, F_X)
    T(d, ((bx0 + bx1) // 2, base - h1 - h2 / 2 - 22), '연금저축 한 달 66만원', 42, INK, F_B)
    T(d, ((bx0 + bx1) // 2, base - h1 - h2 / 2 + 36), '안 셈', 50, INK, F_X)
    # 오른쪽: 한 해 문턱 자 0~2천만, 셈하는 돈 1,200만에 점
    x0, x1, y = 760, 1700, 470
    torn(im, (x0 - 40, y - 70, x1 + 40, y + 70), PAPER_N, seed=1104); d = ImageDraw.Draw(im)
    for k in range(0, 21):
        x = x0 + (x1 - x0) * k / 20; L = 60 if k % 10 == 0 else (36 if k % 5 == 0 else 18)
        d.line([(x, y - 70), (x, y - 70 + L)], fill=INK, width=4 if k % 10 == 0 else 2)
    for k, lab in ((0, '0원'), (10, '1천만원'), (20, '2천만원 기준')):
        x = x0 + (x1 - x0) * k / 20; T(d, (x, y + 110), lab, 38, INK if k == 20 else GREY, F_B)
    xd = x0 + (x1 - x0) * 12 / 20
    d.ellipse((xd - 22, y - 22, xd + 22, y + 22), fill=INK)
    T(d, (xd, y - 130), '피부양자 소득으로 세는 돈 한 해 1,200만원', 48, INK, F_B)
    hand_arrow(d, (xd + 30, y), (x1 - 30, y), OR, 7)   # 점에서 기준까지 남은 거리
    s = '기준까지 800만원 남음'; cx = (x0 + x1) / 2; T(d, (cx, 780), s, 84, OR, F_X)
    hand_under(d, cx - wd(s, 84) / 2, cx + wd(s, 84) / 2, 850, seed=1105)
    source(d, '국민건강보험공단 웹진 2023.9 · 사적연금은 피부양자 소득에 안 넣음 · 100만 × 12 = 1,200만원')

@board
def p3_four_rows(im):  # 65행: 선을 넘은 뒤로는 조금씩 — 10만원 더 많아져도 4천원
    d = ImageDraw.Draw(im); title(d, '선을 넘은 뒤로는 조금씩 올라요', 120)
    rows = (('월 166만원', '0원'), ('월 167만원', '약 6만 8천원'), ('월 170만원', '약 6만 9천원'), ('월 180만원', '약 7만 3천원'), ('월 200만원', '약 8만 1천원'))
    cx = W // 2 - 120
    T(d, (cx - 60, 250), '국민연금만(한 달)', 40, GREY, F_M, 'rm'); T(d, (cx + 60, 250), '매달 내는 보험료', 40, GREY, F_M, 'lm')
    ys = []
    for i, (a, b) in enumerate(rows):
        y = 340 + i * 118; ys.append(y)
        if i: d.line([(cx - 520, y - 70), (cx + 520, y - 70)], fill=(170, 160, 150), width=2)
        T(d, (cx - 60, y), a, 62, GREY if i == 0 else INK, F_B, 'rm')
        T(d, (cx + 60, y), b, 68, GREY if i == 0 else INK, F_X, 'lm')
    d.line([(cx, 290), (cx, 900)], fill=(170, 160, 150), width=2)
    # 170→180 줄을 손 괄호로 묶고 답 하나만 주황
    bx = cx + 560
    hand_arrow(d, (bx + 20, ys[0] - 10), (bx + 20, ys[1] + 10), INK, 6); T(d, (bx + 70, (ys[0] + ys[1]) / 2), '여기서 한 번 크게 뜀', 46, INK, F_B, 'lm')
    ys = ys[1:]
    d.line([(bx, ys[1]), (bx + 40, ys[1]), (bx + 40, ys[2]), (bx, ys[2])], fill=INK, width=6)
    T(d, (bx + 80, (ys[1] + ys[2]) / 2 - 50), '10만원 더 받아도', 50, INK, F_B, 'lm')
    s = '4천원쯤 더'; T(d, (bx + 80, (ys[1] + ys[2]) / 2 + 40), s, 80, OR, F_X, 'lm')
    hand_under(d, bx + 80, bx + 80 + wd(s, 80), (ys[1] + ys[2]) / 2 + 100, seed=1106)
    source(d, '재산 0일 때 · 건강보험료 7.19% + 장기요양 13.14% · 73,213 − 69,146 = 4,067원')

import math, random
def hand_x(d, cx, cy, s=40, color=INK, width=9, seed=7):
    r = random.Random(seed); j = lambda: r.uniform(-3, 3)
    d.line([(cx - s + j(), cy - s + j()), (cx + s + j(), cy + s + j())], fill=color, width=width)
    d.line([(cx + s + j(), cy - s + j()), (cx - s + j(), cy + s + j())], fill=color, width=width)
def hand_o(d, cx, cy, r=40, color=INK, width=8, seed=9): hand_ellipse(d, (cx - r, cy - r, cx + r, cy + r), color, width, seed)

@board
def p3_cut_calendar(im):  # 101행: 경감 달력 한 줄 — 기간마다 비율이 줄고 2026년 9월분부터 0%
    d = ImageDraw.Draw(im); title(d, '깎아 주던 비율, 달력으로 보면', 120)
    cells = (('2022년 9월분부터', '80%'), ('2023년 11월분부터', '60%'), ('2024년 11월분부터', '40%'), ('2025년 11월분부터', '20%'), ('2026년 9월분부터', '0%'))
    cw, gap, y0, y1 = 300, 40, 330, 760; x = (W - (5 * cw + 4 * gap)) // 2; last = None
    for i, (a, b) in enumerate(cells):
        x0 = x + i * (cw + gap); fin = i == 4
        torn(im, (x0, y0, x0 + cw, y1), (250, 248, 242) if not fin else PAPER_N, seed=1200 + i); d = ImageDraw.Draw(im)
        d.rectangle((x0 + 6, y0 + 6, x0 + cw - 6, y0 + 92), fill=INK if not fin else GREY)   # 달력 머리(종이색 칸 위 진한 띠)
        for rx in (x0 + 70, x0 + cw - 70): d.ellipse((rx - 12, y0 - 22, rx + 12, y0 + 2), outline=GREY, width=5)   # 달력 고리
        T(d, (x0 + cw / 2, y0 + 50), a, 34, (250, 248, 242), F_B)
        T(d, (x0 + cw / 2, y0 + 250), b, 120, INK if not fin else OR, F_X)
        T(d, (x0 + cw / 2, y0 + 380), '깎아 줌' if not fin else '깎는 것 없음', 40, GREY if not fin else INK, F_B)
        if i < 3: hand_arrow(d, (x0 + cw + 6, (y0 + y1) / 2 + 120), (x0 + cw + gap - 6, (y0 + y1) / 2 + 120), GREY, 4)
        last = x0
    hand_ellipse(d, (last - 45, y0 - 95, last + cw + 55, y1 + 55), OR, 9, seed=1301)
    s = '이미 받던 분도 9월분부터 전부 내요'; T(d, (W // 2, 880), s, 60, INK, F_X)
    source(d, '국민건강보험법 시행규칙 부칙<보건복지부령 제907호, 2022.9.1> 제3조 · 경감 2026년 8월분까지')

@board
def p3_scale_999(im):  # 146행: 저울 — 999만은 안 셈 / 1,100만은 전부 → 탈락하면 월 13만 6천원
    d = ImageDraw.Draw(im); title(d, '연금 한 해 1,800만원에 이자·배당을 더하면', 120)
    cx, py, tilt = W // 2, 320, 40   # 받침 꼭대기, 기울기(오른쪽 내려감)
    lx, rx = cx - 520, cx + 520; ly, ry = py - tilt, py + tilt
    d.line([(cx, py), (cx, 900)], fill=INK, width=12); d.polygon([(cx - 90, 930), (cx + 90, 930), (cx, 870)], fill=INK)
    d.line([(lx, ly), (rx, ry)], fill=INK, width=12); d.ellipse((cx - 16, py - 16, cx + 16, py + 16), fill=INK)
    for x, y in ((lx, ly), (rx, ry)):
        d.line([(x, y), (x - 210, y + 150)], fill=GREY, width=3); d.line([(x, y), (x + 210, y + 150)], fill=GREY, width=3)
        d.arc((x - 230, y + 70, x + 230, y + 250), 0, 180, fill=INK, width=8)
    T(d, (lx, ly + 198), '이자·배당 999만원', 38, INK, F_B)
    T(d, (lx, ly + 320), '안 셈', 76, GREY, F_X)
    T(d, (lx, ly + 410), '소득으로 세는 돈 1,800만원', 40, GREY, F_B)
    T(d, (rx, ry + 198), '이자·배당 1,100만원', 38, INK, F_B)
    T(d, (rx, ry + 320), '전부 더함', 76, INK, F_X)
    T(d, (rx, ry + 400), '1,800 + 1,100 = 2,900만원', 40, INK, F_B)
    T(d, (rx, ry + 455), '기준 2천만원 넘음', 38, INK, F_B)
    T(d, (rx, ry + 520), '탈락하면', 44, INK, F_B)
    s = '월 13만 6천원'; T(d, (rx, ry + 590), s, 80, OR, F_X)
    hand_under(d, rx - wd(s, 80) / 2, rx + wd(s, 80) / 2, ry + 642, seed=1401)
    source(d, '재산 0일 때 · 135,579원(건강보험 7.19% + 장기요양 13.14%) · 999만원은 공단 확인 권함')

@board
def p3_couple(im):  # 157행: 두 사람 칸 — 170만 ✕ / 50만 ○ → 둘 다 ✕, 합쳐서 2천만? 아님
    d = ImageDraw.Draw(im); title(d, '부부는 한 사람씩 따로 따져요', 120)
    boxes = ((240, '한 분', '연금 월 170만원', '한 해 2,040만원'), (1080, '배우자', '연금 월 50만원', '한 해 600만원'))
    for i, (x0, who, a, b) in enumerate(boxes):
        torn(im, (x0, 250, x0 + 600, 640), (250, 248, 242), seed=1500 + i); d = ImageDraw.Draw(im)
        T(d, (x0 + 300, 310), who, 44, GREY, F_B); T(d, (x0 + 300, 400), a, 62, INK, F_X); T(d, (x0 + 300, 480), b, 40, GREY, F_B)
    hand_x(d, 540, 575, 34, INK, 9, 1); T(d, (540 + 70, 575), '2천만 넘음', 36, INK, F_B, 'lm')
    hand_o(d, 1380, 575, 36, GREY, 7, 2); hand_x(d, 1380, 575, 40, OR, 10, 3)   # 혼자면 ○인데 ✕로 덮음
    T(d, (1380 + 120, 575), '혼자면 ○', 36, GREY, F_B, 'lm')
    # 가운데: '합쳐서 2천만?' 줄 긋기
    q = '합쳐서 2천만원과 비교?'; T(d, (W // 2, 720), q, 50, GREY, F_B)
    qw = wd(q, 50, F_B); d.line([(W // 2 - qw / 2 - 10, 722), (W // 2 + qw / 2 + 10, 716)], fill=INK, width=6)
    s = '한 분이 넘으면 둘 다 빠져요'; T(d, (W // 2, 860), s, 84, OR, F_X)
    hand_under(d, W // 2 - wd(s, 84) / 2, W // 2 + wd(s, 84) / 2, 915, seed=1502)
    source(d, '국민건강보험법 시행규칙 [별표 1의2] 제1호라목 · 기혼자는 부부 모두 기준을 충족해야 함')

def main():
    os.makedirs(OUT, exist_ok=True)
    for n, fn in B.items():
        im = canvas(); fn(im); im.save(os.path.join(OUT, n + '.png')); print(n)

if __name__ == '__main__':
    main()
