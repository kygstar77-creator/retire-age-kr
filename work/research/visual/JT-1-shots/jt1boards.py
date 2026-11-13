"""JT-1 장면 판 — visual-designer 2026-11-13. K-1·H-4 판과 같은 꼴·같은 부품(k1boards):
구겨진 종이 바탕 · 펜 빗금 막대(hatch_bar) · 주황 #FF5A00은 그 화면의 답 하나 · 손 동그라미·밑줄 · 사물 그림 obj()(11/12 B-51).
숫자는 ep/JT-1 calc.py 표(공사 월지급금 예시 2026.03.01, 천원)·calc_out.txt·script.md(editor 7eae791b) 자막 값만. 바꾸지 않음.
대본 '(화면 [판])'·'(화면 [표])' 줄마다 한 장. 판은 '답이 열린 마지막 모습' — '?' → 열림은 PD가 Remotion에서.
사용: py -3.12 jt1boards.py [이름 ...]   (없으면 전부) → work/video/public/bg/jt1/board/<이름>.png
"""
import os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'K-1-shots'))
import k1boards as K
from k1boards import (W, H, INK, GREY, OR, KRAFT, FADE, F_B, F_M, F_X, font, canvas, T, TF, source,
                      hand_ellipse, hand_under, hand_check, hand_arrow, hatch_bar, obj)
from PIL import ImageDraw

WORK = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'JT-1')
OUT = os.path.join(WORK, 'video', 'public', 'bg', 'jt1', 'board')
# 표는 calc.py 맨 위 T = {...} 를 그대로 읽는다(옮겨 적지 않음)
_src = open(os.path.join(EP, 'calc.py'), encoding='utf-8').read()
TBL = eval(re.search(r'T = (\{.*?\})', _src, re.S).group(1))
AGES = [55, 60, 65, 70, 75, 80]
SRC_HF = '한국주택금융공사 월지급금 예시 · 종신·정액형·일반주택 · 2026.03.01 기준'
LINE = (206, 198, 186)

def man(v_thousand):   # 천원 → '126만' (반올림 없이 내림 아님: 표 자막과 같은 반올림)
    return f'{round(v_thousand / 10):,}만'

B = {}
def board(fn):
    B[fn.__name__] = fn; return fn

@board
def jt1_note(im):          # 0. 여는 말 — 공책 판
    d = ImageDraw.Draw(im)
    obj(im, 'bankbook', 330, 300, 260, rot=-6, seed=11); d = ImageDraw.Draw(im)
    T(d, (1060, 250), '5억 집', 90, GREY, F_B)
    T(d, (1060, 420), '65세  126만원', 120, INK, F_X)
    T(d, (1060, 590), '70세  154만원', 120, INK, F_X)
    TF(d, (W // 2, 820), '그럼 기다릴까?', 170, OR, F_X)
    hand_under(d, 560, 1360, 920, seed=12)
    source(d, SRC_HF + ' · 매달')

@board
def jt1_check3(im):        # 1. 체크리스트 3칸
    d = ImageDraw.Draw(im); TF(d, (W // 2, 140), '들 수 있나? 세 가지', 130, INK, F_X)
    rows = (('나이', '부부 중 한 사람 55세 이상'), ('집값', '부부 합산 공시가격 12억 이하'), ('사는 집', '실제로 살기'))
    for i, (a, b) in enumerate(rows):
        y = 380 + i * 210
        hand_check(d, 250, y + 6, 80, OR if i == 1 else INK, 12)
        T(d, (400, y), a, 110, INK, F_X, 'lm'); T(d, (800, y), b, 64, INK, F_B, 'lm')
    source(d, '한국주택금융공사 주택연금이란 · 다주택자도 합산 가격 기준')

@board
def jt1_scale2(im):        # 1. 두 저울 칸
    d = ImageDraw.Draw(im)
    obj(im, 'scale', W // 2, 300, 300, rot=0, seed=21); d = ImageDraw.Draw(im)
    T(d, (480, 560), '들 수 있나?', 80, GREY, F_B); T(d, (480, 720), '공시가격', 140, INK, F_X)
    T(d, (1440, 560), '얼마 받나?', 80, GREY, F_B); T(d, (1440, 720), '시세', 170, OR, F_X)
    hand_ellipse(d, (1240, 620, 1640, 820), seed=22)
    d.line([(W // 2, 520), (W // 2, 860)], fill=LINE, width=4)
    T(d, (W // 2, 940), '표는 시세로 읽기 · 나이는 부부 중 젊은 쪽', 54, INK, F_B)
    source(d, '월지급금 예시표 주택가격 = 시세·감정평가액 · 가입 판정 = 공시가격')

def grid(im, hi=None, cap=False, y_top=330, x_left=420, cw=112, rh=104, labels=(55, 65, 80)):
    """나이 6줄 × 집값 12칸 격자(공사 표를 우리가 다시 그림) — 11/13 bgcheck ⑤(줄 8↓): 72칸 숫자 대신 점 크기(넓이 ∝ 매달 금액).
    숫자는 불 켠 칸 하나만. 나이 이름은 labels 줄만(나머지 줄은 점만). cap=True면 같은 값 반복 칸만 진하게."""
    import math
    d = ImageDraw.Draw(im); vmax = max(max(r) for r in TBL.values()); rmax = cw * 0.44
    T(d, (x_left + cw // 2, y_top), '1억', 40, GREY, F_B); T(d, (x_left + cw * 11 + cw // 2, y_top), '12억', 40, GREY, F_B)
    hand_arrow(d, (x_left + cw + 20, y_top), (x_left + cw * 11 - 30, y_top), GREY, 4)
    pos = {}
    for i, a in enumerate(AGES):
        y = y_top + 110 + i * rh
        if a in labels: T(d, (x_left - 40, y), f'{a}세', 50, INK, F_X, 'rm')
        row = TBL[a]
        for j, v in enumerate(row):
            x = x_left + cw * j + cw // 2; r = rmax * math.sqrt(v / vmax)
            same = (j > 0 and row[j - 1] == v) or (j < 11 and row[j + 1] == v)
            if hi == (a, j + 1): c = OR
            elif cap: c = INK if same else FADE
            else: c = INK if (hi and a == hi[0]) else FADE
            d.ellipse((x - r, y - r, x + r, y + r), fill=c)
            pos[(a, j + 1)] = (x, y, r)
    return d, pos

@board
def jt1_grid(im):          # 2. 6×12 격자 — 65세·5억 칸 불
    d = ImageDraw.Draw(im); T(d, (W // 2, 70), '65세 · 5억 집이면', 64, INK, F_B)
    T(d, (W // 2, 190), '매달 126만원', 150, OR, F_X)
    d, pos = grid(im, hi=(65, 5))
    x, y, r = pos[(65, 5)]
    hand_ellipse(d, (x - 58, y - 58, x + 58, y + 58), seed=31)
    source(d, SRC_HF + ' · 점 넓이 = 매달 금액')

@board
def jt1_cap(im):           # 2. 상한 칸 묶음
    d = ImageDraw.Draw(im); TF(d, (W // 2, 130), '여기부터 더 안 올라요', 150, OR, F_X)
    d, pos = grid(im, cap=True, labels=(55, 70, 80), y_top=250, rh=94)
    x0 = pos[(80, 9)][0] - 70; x1 = pos[(80, 12)][0] + 70; y = pos[(80, 9)][1]
    hand_ellipse(d, (x0, y - 70, x1, y + 70), seed=32)
    T(d, (W // 2, 975), '80세 9억~12억 모두 406만원 · 75세 10억부터 367만원', 46, INK, F_B)
    source(d, '한국주택금융공사 월지급금 예시 2026.03.01 · 점 넓이 = 매달 금액')

@board
def jt1_mar1(im):          # 2. 3월 1일 표가 바뀜
    d = ImageDraw.Draw(im)
    T(d, (W // 2, 200), '2026년 3월 1일 표가 바뀜', 96, INK, F_X)
    T(d, (W // 2, 360), '평균 가입자 (72세 · 4억)', 64, GREY, F_B)
    T(d, (900, 600), '130만', 150, INK, F_X); hand_arrow(d, (1120, 600), (1260, 600), INK, 8)
    T(d, (1500, 600), '134만', 170, OR, F_X)
    hand_under(d, 1310, 1690, 700, seed=42)
    T(d, (W // 2, 880), '3월 1일 뒤 새로 신청한 분부터', 66, INK, F_B)
    source(d, '금융위원회 보도자료 2026년 2월 · 129.7만원 → 133.8만원(3.13%)')

@board
def jt1_lost(im):          # 3. 못 받은 돈 식
    d = ImageDraw.Draw(im); TF(d, (W // 2, 170), '5년 기다리면 못 받는 돈', 110, INK, F_X)
    T(d, (W // 2, 440), '5년 × 12달 × 126만원', 110, INK, F_B)
    T(d, (W // 2, 700), '7,584만원', 220, OR, F_X)
    hand_ellipse(d, (W // 2 - 620, 560, W // 2 + 620, 840), seed=51)
    source(d, '5억 집 · 65세 월 1,264천원 × 60개월 · ' + SRC_HF[:13])

@board
def jt1_diff(im):          # 3. 매달 차
    d = ImageDraw.Draw(im); TF(d, (W // 2, 170), '70세에 들면 매달 더 받는 돈', 104, INK, F_X)
    T(d, (W // 2, 440), '154만 − 126만', 130, INK, F_B)
    T(d, (W // 2, 700), '27만 5천원', 210, OR, F_X)
    hand_under(d, W // 2 - 520, W // 2 + 520, 820, seed=61)
    source(d, '1,539천원 − 1,264천원 = 275천원 · ' + SRC_HF)

def cum_chart(im, a0, a1, cross, end=95, box=(260, 250, 1720, 860)):
    """받은 돈 합 두 선(5억 집, 집값 그대로 가정) — calc §1·§7 식 그대로: 월 × 12 × (나이 − 시작 나이)."""
    m0, m1 = TBL[a0][4], TBL[a1][4]; ages = list(range(a0, end + 1))
    s0 = [m0 * 12 * (x - a0) / 100000 for x in ages]   # 천원 → 억(100,000천원)
    s1 = [max(0, m1 * 12 * (x - a1)) / 100000 for x in ages]
    ymax = max(s0[-1], s1[-1]) * 1.08
    X, Y = K.linechart(im, [s0, s1], box, 0, ymax, [GREY, INK], [9, 11],
                       [(i, f'{x}세') for i, x in enumerate(ages) if x in (a0, a1, end)], yticks=())
    d = ImageDraw.Draw(im)
    i0 = ages.index(a0 + 10); T(d, (X(i0), Y(s0[i0]) - 60), f'{a0}세에 든 쪽', 46, GREY, F_B)
    i1 = ages.index(min(end, a1 + 5)); T(d, (X(i1) + 30, Y(s1[i1]) + 60), f'{a1}세에 든 쪽', 46, INK, F_B, 'lm')
    ic = ages.index(cross); cx, cy = X(ic), Y(s0[ic])
    hand_ellipse(d, (cx - 70, cy - 70, cx + 70, cy + 70), seed=70 + a0)
    T(d, (cx - 110, cy - 30), f'{cross}세', 150, OR, F_X, 'rm')
    return d

@board
def jt1_cross93(im):       # 3. 두 선 만남 93세
    d = ImageDraw.Draw(im); TF(d, (W // 2, 100), '받은 돈 합 · 65세 vs 70세', 90, INK, F_X)
    cum_chart(im, 65, 70, 93); d = ImageDraw.Draw(im)
    source(d, '5억 집 · 집값이 그대로라는 가정 · 7,584만원 ÷ 27.5만원 = 276개월 ≈ 23년')

@board
def jt1_mid3(im):          # 3. 80·85·90세 — 일찍 든 쪽이 더 받은 돈(말하는 숫자만, 합은 자막)
    d = ImageDraw.Draw(im); TF(d, (W // 2, 160), '65세에 든 쪽이 더 받은 돈', 116, INK, F_X)
    rows = (('80세까지', '4,284만원'), ('85세까지', '2,634만원'), ('90세까지', '984만원'))
    for i, (a, e) in enumerate(rows):
        y = 450 + i * 190
        T(d, (900, y), a, 80, INK, F_B, 'rm'); T(d, (1000, y), e, 120, OR if i == 0 else INK, F_X, 'lm')
        if i < 2: d.line([(420, y + 95), (1600, y + 95)], fill=LINE, width=2)
    T(d, (W // 2, 950), '차가 줄어 93세쯤 같아져요', 60, INK, F_B)
    source(d, '5억 집 · 집값이 그대로라는 가정')

@board
def jt1_cross81(im):       # 3. 55세 vs 65세 81세
    d = ImageDraw.Draw(im); TF(d, (W // 2, 100), '받은 돈 합 · 55세 vs 65세', 90, INK, F_X)
    cum_chart(im, 55, 65, 81, end=90); d = ImageDraw.Draw(im)
    source(d, '5억 집 · 집값이 그대로라는 가정 · 9,360만원 ÷ 48.4만원 ≈ 16.1년')

@board
def jt1_age3(im):          # 3. 같아지는 나이 3줄
    d = ImageDraw.Draw(im); TF(d, (W // 2, 130), '같아지는 나이', 130, INK, F_X)
    rows = (('55세 → 65세', '81세'), ('60세 → 65세', '90세'), ('65세 → 70세', '93세'))
    for i, (a, b) in enumerate(rows):
        y = 350 + i * 190
        T(d, (880, y), a, 80, INK, F_B, 'rm'); T(d, (1000, y), b, 120, OR if i == 2 else INK, F_X, 'lm')
        if i < 2: d.line([(360, y + 95), (1560, y + 95)], fill=LINE, width=2)
    T(d, (W // 2, 930), '3억 · 5억 · 9억 모두 같아요', 74, INK, F_X)
    hand_under(d, 620, 1300, 1000, seed=91)
    source(d, '집값이 그대로라는 가정 · 1억당 금액이 거의 같아서')

@board
def jt1_trap_price(im):    # 3. 함정 카드 — 집값이 내리면
    d = ImageDraw.Draw(im)
    obj(im, 'apt', 380, 420, 330, rot=-3, seed=101); d = ImageDraw.Draw(im)
    TF(d, (1200, 260), '기다리는 동안', 100, INK, F_X, maxw=1100)
    TF(d, (1200, 420), '집값이 내리면?', 140, OR, F_X, maxw=1100)
    pts = [(760, 620), (960, 600), (1160, 650), (1360, 720), (1560, 810)]
    d.line(pts, fill=INK, width=10, joint='curve'); hand_arrow(d, pts[-2], (1640, 850), INK, 10)
    T(d, (1200, 930), '늦게 든 쪽 금액도 줄어요', 70, INK, F_B)
    source(d, '월지급금 = 가입 때 시세·감정평가액 기준 · 그림은 방향만(값 아님)')

@board
def jt1_stack(im):         # 4. 쌓이는 잔액 — 세 갈래
    d = ImageDraw.Draw(im); TF(d, (W // 2, 110), '대출 잔액에 쌓이는 것', 120, INK, F_X)
    # 해마다 한 칸씩 커지는 막대 모양만(금액 없음 — 금리는 6개월 변동이라 값을 지어내지 않음)
    base = 880; x = 220; bw = 150; gap = 70
    for k in range(6):
        h = 90 + k * 95; parts = (0.62, 0.12, 0.26)
        y = base
        for c, p in zip((INK, GREY, KRAFT), parts):
            hh = h * p; hatch_bar(im, (x, y - hh, x + bw, y), c, seed=400 + k * 3 + parts.index(p), step=12, width=5); y -= hh
        x += bw + gap
    d = ImageDraw.Draw(im)
    for i, (s, c) in enumerate((('이자', KRAFT), ('보증료', GREY), ('받은 돈', INK))):
        T(d, (1660, 480 + i * 120), s, 76, c, F_X)
    T(d, (W // 2, 960), '현금으로 내지 않고 잔액에 더해요', 60, OR, F_B)
    source(d, '대출잔액 = 월지급금 + 보증료 + 이자 · 그림은 모양만(금액 아님)')

@board
def jt1_trap_exit(im):     # 4. 중도 해지 갚을 돈
    d = ImageDraw.Draw(im)
    obj(im, 'bill', 300, 300, 260, rot=-5, seed=111); d = ImageDraw.Draw(im)
    TF(d, (1150, 230), '중간에 그만두면 갚을 돈', 100, INK, F_X, maxw=1300)
    T(d, (W // 2, 600), '받은 돈 + 보증료 + 이자', 150, OR, F_X)
    hand_under(d, 220, 1700, 710, seed=112)
    T(d, (W // 2, 870), '받은 돈만 돌려주면 끝이 아니에요', 66, INK, F_B)
    source(d, '중도해지 상환액 = 월지급금 누계 + 보증료(초기·연) + 대출이자')

@board
def jt1_43(im):            # 5. 생활비 막대
    d = ImageDraw.Draw(im); TF(d, (W // 2, 130), '부부 적정생활비 297만원 중', 100, INK, F_X)
    x0, x1, y0, y1 = 220, 1700, 430, 610
    hatch_bar(im, (x0, y0, x1, y1), FADE, seed=501, step=16, width=5)
    xm = x0 + (x1 - x0) * 1264 / 2969
    hatch_bar(im, (x0, y0, xm, y1), OR, seed=502, step=12, width=7); d = ImageDraw.Draw(im)
    T(d, ((x0 + xm) / 2, 360), '126만원', 90, OR, F_X); T(d, (x1, 360), '297만원', 70, GREY, F_B, 'rm')
    T(d, (W // 2, 800), '43%', 230, OR, F_X)
    source(d, '국민연금연구원 2023 조사 50세 이상 응답 · 5억·65세 1,264천원 ÷ 2,969천원')

@board
def jt1_flow(im):          # 6. 정산 갈래 흐름도
    d = ImageDraw.Draw(im)
    obj(im, 'house', 300, 520, 300, rot=-3, seed=121); d = ImageDraw.Draw(im)
    T(d, (300, 760), '두 분 다 돌아가신 뒤', 50, GREY, F_B)
    T(d, (820, 520), '집 팔아', 80, INK, F_X); T(d, (820, 620), '정산', 110, INK, F_X)
    hand_arrow(d, (480, 540), (660, 540), INK, 8)
    hand_arrow(d, (990, 500), (1180, 320), INK, 8); hand_arrow(d, (990, 640), (1180, 800), INK, 8)
    T(d, (1220, 260), '남으면', 70, GREY, F_B, 'lm'); T(d, (1220, 370), '자녀에게', 120, INK, F_X, 'lm')
    T(d, (1220, 740), '모자라면', 70, GREY, F_B, 'lm'); T(d, (1220, 860), '공사가 부담', 120, OR, F_X, 'lm')
    T(d, (W // 2, 120), '자녀에게 청구하지 않아요', 90, INK, F_X)
    source(d, '한국주택금융공사 사망 후 절차 · "정산금액이 부족하면 공사가 부담하고 남으면 상속"')

@board
def jt1_tax2(im):          # 6. 재산세·기초연금
    d = ImageDraw.Draw(im)
    T(d, (500, 300), '재산세', 100, INK, F_X); T(d, (500, 520), '최대 −25%', 150, OR, F_X)
    T(d, (500, 700), '1주택 · 저당권 방식', 52, GREY, F_B); T(d, (500, 780), '2027년 말까지', 52, GREY, F_B)
    d.line([(W // 2, 240), (W // 2, 860)], fill=LINE, width=4)
    T(d, (1420, 300), '기초연금', 100, INK, F_X); T(d, (1420, 520), '그대로', 150, INK, F_X)
    T(d, (1420, 700), '월지급금은 소득 아님', 52, GREY, F_B)
    hand_check(d, 1660, 420, 70, INK, 10)
    source(d, '한국주택금융공사 주택연금 혜택 · 5억 초과는 5억 기준 · FAQ "월지급금은 소득에 포함되지 않아요"')

@board
def jt1_summary(im):       # 7. 정리 4줄
    d = ImageDraw.Draw(im); T(d, (W // 2, 130), '한 장 정리', 130, INK, F_X)
    rows = (('5억 · 65세', '매달 126만원'), ('70세에 들면', '93세에 받은 돈 합 같아짐'), ('잔액에 쌓임', '받은 돈 · 보증료 · 이자'), ('모자라도', '자녀에게 청구 없음'))
    for i, (a, b) in enumerate(rows):
        y = 330 + i * 165
        T(d, (760, y), a, 62, GREY, F_B, 'rm'); T(d, (820, y), b, 78, OR if i == 1 else INK, F_X, 'lm')
        if i < 3: d.line([(260, y + 82), (1700, y + 82)], fill=LINE, width=2)
    hand_check(d, 180, 495, 56)
    source(d, '집값이 그대로라는 가정 · 내 금액은 공사 누리집 예상연금조회 · 1688-8114')

def main(names):
    os.makedirs(OUT, exist_ok=True)
    for n in names or list(B):
        im = canvas(); B[n](im); im.save(os.path.join(OUT, n + '.png')); print(n)

if __name__ == '__main__':
    main(sys.argv[1:])
