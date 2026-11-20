"""H-5 장면 판 — visual-designer 2026-11-17. JT-1·H-4 판과 같은 꼴·같은 부품(k1boards·h4boards):
구겨진 종이 바탕 · 펜 빗금 막대(hatch_bar) · 주황 #FF5A00은 그 화면의 답 하나 · 손 동그라미·밑줄.
숫자는 ep/H-5 calc_out·calc2_out·calc4_out(11/19 23:09, 국토부 실거래 11/19 다시 받은 판 — facts '11/20 갱신' F'')과 script.md(editor 555e65b4) 자막 값만.
표는 calc 출력 파일을 그대로 읽는다(옮겨 적지 않음). 거래 점(dots)은 calc2.py와 같은 거름(해제·공공기관 뺌, 전용 80~86㎡)으로 raw/rt에서 다시 셈.
지도: 통계청 센서스용 행정구역경계 2013(southkorea-maps 정리본, geo/incheon_dong.json) — 모양만.
판은 '답이 열린 마지막 모습' — '?' → 열림은 PD가 Remotion에서. 파일 이름은 shot_plan·h5props.py 그대로.
사용: py -3.12 h5boards.py [이름 ...]   (없으면 전부) → work/video/public/bg/h5/board/<이름>.png
"""
import os, sys, re, json, glob, math, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'K-1-shots')); sys.path.insert(0, os.path.join(HERE, '..', 'H-4-shots'))
import k1boards as K
from k1boards import (W, H, INK, GREY, OR, KRAFT, KRAFT_L, FADE, F_B, F_M, F_X, font, canvas, T, TF, source,
                      hand_ellipse, hand_under, hand_check, hand_arrow, hatch_bar)
from h4boards import _rings, _proj, _wobble_rect
from PIL import ImageDraw

WORK = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'H-5')
OUT = os.path.join(WORK, 'video', 'public', 'bg', 'h5', 'board')
LINE = (206, 198, 186)
SRC_RT = '국토교통부 아파트 매매 실거래 · 송도동 84㎡대(전용 80~86㎡) · 해제·공공기관 매수 뺌'
rd = lambda fn: open(os.path.join(EP, fn), encoding='utf-8').read()

# ── calc 출력에서 그대로 읽기 ─────────────────────────────────────────
_c1, _c2, _c4 = rd('calc_out.txt'), rd('calc2_out.txt'), rd('calc4_out.txt')
YEAR = [(int(y), int(n), float(v)) for y, n, v in re.findall(r'  (20\d\d): (\d+)건 · 중앙 ([\d.]+)억', _c1)]
HALF = [(y, h, int(n), float(v)) for y, h, n, v in re.findall(r'  (20\d\d)H([12]): (\d+)건 · 중앙 ([\d.]+)억', _c1)]
CPX = [(nm, int(by), float(pk), float(rc), int(pc)) for nm, by, pk, rc, pc in
       re.findall(r'  (\S.*?)\((\d{4})\) 고점 ([\d.]+)억\(\d+건\) · 바닥 \S+ · 최근 ([\d.]+)억\(\d+건\) → (\d+)%', _c2)]
RATIO = [(nm, int(p)) for nm, p in re.findall(r'  (\S.*?) 전세 중앙 [\d.]+억\(\d+건\) ÷ 매매 중앙 [\d.]+억 = (\d+)%', _c1)]
JBIN = [(float(a), float(b), int(n)) for a, b, n in re.findall(r'  ([\d.]+)~([\d.]+)억 미만: (\d+)건', _c4)]
assert len(CPX) == 33 and len(RATIO) == 38 and sum(n for *_, n in JBIN) == 821, (len(CPX), len(RATIO))
assert len(YEAR) == 6 and len(HALF) == 12

def eok_kr(v):   # 9.00 → '9억', 7.40 → '7억 4천', 6.75 → '6억 7천5백'
    e = int(v); m = round((v - e) * 10000)
    if m == 0: return f'{e}억'
    ch, bk = divmod(m, 1000); s = f'{e}억 ' + (f'{ch}천' if ch else '') + (f'{bk // 100}백' if bk else '')
    return s

B = {}
def board(fn):
    B[fn.__name__] = fn; return fn

# ── 0. 여는 말 ───────────────────────────────────────────────────────
@board
def search(im):            # 검색창 '송도 집값' → 자동완성 '폭락' · 카드 '전고점 대비 6~70%'(우리가 다시 그림)
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = 300, 190, 1620, 350
    _wobble_rect(d, (x0, y0, x1, y1), INK, 6, seed=3)
    d.ellipse((x1 - 130, y0 + 42, x1 - 66, y0 + 106), outline=INK, width=8); d.line([(x1 - 76, y0 + 98), (x1 - 46, y0 + 128)], fill=INK, width=10)
    T(d, (x0 + 60, (y0 + y1) // 2), '송도 집값', 84, INK, F_B, 'lm')
    T(d, (x0 + 60, 470), '송도 집값', 72, GREY, F_B, 'lm')
    w = font(F_B, 72).getlength('송도 집값 ')
    T(d, (x0 + 60 + w, 470), '폭락', 96, OR, F_X, 'lm')
    hand_under(d, x0 + 60 + w, x0 + 60 + w + font(F_X, 96).getlength('폭락'), 530, seed=4)
    d.line([(x0, 600), (x1, 600)], fill=LINE, width=3)
    T(d, (W // 2, 780), '"전고점 대비 6~70%"', 140, INK, F_X)
    T(d, (W // 2, 920), '흔히 보는 말 두 가지', 60, GREY, F_B)
    source(d, '검색 자동완성 2026.10.22 · 유튜브 영상 설명란 문구 · 화면은 우리가 다시 그림')

@board
def open82(im):            # '고점의 ?%' → 82%
    d = ImageDraw.Draw(im)
    T(d, (W // 2, 210), '같은 넓이 · 같은 방법으로', 72, GREY, F_B)
    T(d, (560, 560), '고점의', 150, INK, F_X)
    T(d, (1260, 560), '82%', 330, OR, F_X)
    hand_ellipse(d, (960, 360, 1580, 770), seed=11)
    T(d, (W // 2, 900), '9억  →  7억 4천', 100, INK, F_X)
    source(d, SRC_RT + ' · 가운데 값 · 고점 1년 2021.07~2022.06 · 최근 2026.07~10')

# ── 기초 ────────────────────────────────────────────────────────────
@board
def map(im):               # 인천(섬 제외) 동 경계 — 송도동만 주황, 청라·영종 회색
    d = ImageDraw.Draw(im)
    feats = json.load(open(os.path.join(HERE, 'geo', 'incheon_dong.json'), encoding='utf-8'))['features']
    P = _proj(feats, (80, 90, 1240, 1010))
    SONGDO = {'2304062', '2304063'}; OUTS = {'2308074', '2308075', '2301062', '2301063', '2301064'}  # 청라1·2 · 영종·용유·운서
    pts_of = {'songdo': [], 'cheongna': [], 'yeongjong': [], 'yeonsu': []}
    for f in feats:
        c = f['properties']['code']
        if c in SONGDO: fill, key = (250, 196, 160), 'songdo'
        elif c in OUTS: fill, key = (176, 170, 160), ('cheongna' if c.startswith('2308') else 'yeongjong')
        elif c.startswith('23040'): fill, key = (222, 210, 190), 'yeonsu'
        else: fill, key = (236, 230, 220), None
        for r in _rings(f):
            pts = [P(x, y) for x, y in r]
            d.polygon(pts, fill=fill); d.line(pts + [pts[0]], fill=(160, 150, 136), width=2)
            if key: pts_of[key].extend(pts)
    # 송도 테두리 굵게(주황)
    for f in feats:
        if f['properties']['code'] in SONGDO:
            for r in _rings(f):
                pts = [P(x, y) for x, y in r]; d.line(pts + [pts[0]], fill=OR, width=7)
    cen = {k: (sum(p[0] for p in v) / len(v), sum(p[1] for p in v) / len(v)) for k, v in pts_of.items() if v}
    sx, sy = cen['songdo']
    T(d, (1600, 560), '송도동', 190, OR, F_X)
    d.line([(sx + 30, sy), (1380, 580)], fill=OR, width=5)
    T(d, (1600, 730), '인천 연수구', 70, INK, F_B)
    for k, lab in (('cheongna', '청라'), ('yeongjong', '영종')):
        x, y = cen[k]; T(d, (x, y), lab, 52, INK, F_B)
    T(d, (1600, 880), '청라 · 영종은 이번 편 빼고', 56, GREY, F_B)
    source(d, '경계 통계청 센서스용 행정구역 2013(모양만 · 그 뒤 매립지·동 나눔 반영 안 됨) · 섬 지역 일부 생략')

@board
def median9(im):           # 막대 아홉 개 값 순서 — 가운데만 주황
    d = ImageDraw.Draw(im); TF(d, (W // 2, 130), '가운데 값 = 줄 세웠을 때 한가운데', 92, INK, F_X)
    hs = [0.34, 0.42, 0.47, 0.52, 0.56, 0.60, 0.66, 0.74, 1.0]   # 모양만(값 아님) — 맨 끝 한 건이 아주 비싸도 가운데는 그대로
    base, top, bw, gap = 900, 330, 120, 60; x = (W - (9 * bw + 8 * gap)) / 2
    for i, h in enumerate(hs):
        y = base - (base - top) * h
        hatch_bar(im, (x, y, x + bw, base), OR if i == 4 else (INK if i != 8 else GREY), seed=20 + i, step=12, width=5)
        if i == 4: mx, my = x + bw / 2, y
        x += bw + gap
    d = ImageDraw.Draw(im); d.line([(250, base), (1670, base)], fill=GREY, width=4)
    T(d, (mx, my - 80), '가운데', 84, OR, F_X)
    T(d, (1560, 270), '아주 비싼 한 건', 46, GREY, F_B)
    T(d, (W // 2, 975), '비싼 한 건 · 싼 한 건에 덜 흔들려요', 58, INK, F_B)
    source(d, '그림은 모양만(값 아님)')

# ── 1. 5년 흐름 ─────────────────────────────────────────────────────
@board
def half(im):              # 반기 막대 2021 하반기~2026 하반기 · 건수
    d = ImageDraw.Draw(im); TF(d, (W // 2, 100), '반년마다 가운데 값', 90, INK, F_X)
    rows = [r for r in HALF if (r[0], r[1]) >= ('2021', '2')]
    n = len(rows); x0, x1, base, top = 150, 1770, 860, 300; slot = (x1 - x0) / n; bw = slot * 0.6; vmax = 9.6
    for i, (y, h, cnt, v) in enumerate(rows):
        x = x0 + i * slot + (slot - bw) / 2; yt = base - (base - top) * v / vmax
        key = (y, h)
        c = OR if key == ('2021', '2') else (INK if key in (('2023', '1'), ('2026', '2')) else FADE)
        hatch_bar(im, (x, yt, x + bw, base), c, seed=30 + i, step=11, width=5); d = ImageDraw.Draw(im)
        cx = x + bw / 2
        if key in (('2021', '2'), ('2023', '1'), ('2026', '2')):
            T(d, (cx, yt - 52), f'{v:.2f}억', 60 if key != ('2021', '2') else 72, c, F_X)
        T(d, (cx, base + 42), f"{y[2:]}년 {'상' if h == '1' else '하'}", 36, INK, F_B)
        T(d, (cx, base + 88), f'{cnt:,}건', 32, OR if key == ('2022', '1') else GREY, F_B)
    d.line([(x0 - 10, base), (x1 + 10, base)], fill=GREY, width=4)
    source(d, SRC_RT + ' · 막대는 0억부터 · 2026 하반기 = 7~10월')

@board
def count(im):             # 해마다 거래 건수 — 2022만 주황
    d = ImageDraw.Draw(im); TF(d, (W // 2, 110), '해마다 거래 건수', 100, INK, F_X)
    base, top, bw, gap = 830, 290, 190, 90; x = (W - (6 * bw + 5 * gap)) / 2; vmax = max(n for _, n, _ in YEAR)
    for i, (y, n, _) in enumerate(YEAR):
        yt = base - (base - top) * n / vmax; c = OR if y == 2022 else INK
        hatch_bar(im, (x, yt, x + bw, base), c, seed=40 + i, step=12, width=5); d = ImageDraw.Draw(im)
        T(d, (x + bw / 2, yt - 50), f'{n:,}', 70 if y == 2022 else 54, c, F_X)
        T(d, (x + bw / 2, base + 50), f'{y}' + ('*' if y == 2026 else ''), 46, c, F_B)
        x += bw + gap
    d.line([(200, base), (1720, base)], fill=GREY, width=4)
    T(d, (W // 2, 975), '2022년은 앞 해의 절반도 안 됨', 50, INK, F_B)
    source(d, SRC_RT + ' · * 2026년은 10월까지')

@board
def eq82(im):              # 식 쌓기 — 고점 / 가장 낮을 때 / 지금 → 82%
    d = ImageDraw.Draw(im)
    pk, lo, rc = 9.00, 6.75, 7.40   # calc2 §1
    assert f'고점 반기 426건 중앙 {pk:.2f}억' in _c2 and f'바닥 반기 1064건 중앙 {lo:.2f}억' in _c2 and f'최근 596건 중앙 {rc:.2f}억' in _c2
    rows = (('고점 1년', eok_kr(pk), '2021 하반기~2022 상반기'), ('가장 낮았던 1년', eok_kr(lo), '2022 하반기~2023 상반기'), ('지금', eok_kr(rc), '2026년 7~10월'))
    for i, (a, b, c) in enumerate(rows):
        y = 170 + i * 175
        T(d, (760, y - 18), a, 64, GREY, F_B, 'rm'); T(d, (820, y), b, 104, INK, F_X, 'lm')
        T(d, (760, y + 44), c, 34, GREY, F_B, 'rm')
        d.line([(300, y + 85), (1760, y + 85)], fill=LINE, width=2)
    T(d, (760, 760), '지금 ÷ 고점', 80, INK, F_B, 'rm')
    T(d, (850, 760), '=', 140, INK, F_X, 'lm')
    T(d, (990, 760), '82%', 200, OR, F_X, 'lm')
    hand_ellipse(d, (950, 640, 1430, 880), seed=51)
    T(d, (W // 2, 975), '고점보다 1억 6천 아래 · 가장 낮을 때보다 6천5백 위', 54, INK, F_B)
    source(d, SRC_RT + ' · 가운데 값 · 9.00억 − 7.40억 = 1.60억 · 7.40억 − 6.75억 = 0.65억')

# ── 2. 단지 33곳 ───────────────────────────────────────────────────
@board
def rank32(im):            # 단지 33곳 회복 비율(0%부터) · 100% 점선 · 가운데 84%
    d = ImageDraw.Draw(im); TF(d, (W // 2, 100), '단지 33곳 · 고점 1년 대비 지금', 84, INK, F_X)
    x0, x1, base, top = 150, 1770, 900, 340; n = len(CPX); slot = (x1 - x0) / n; bw = slot * 0.62
    Y = lambda p: base - (base - top) * p / 100
    for i, (nm, by, pk, rc, p) in enumerate(CPX):
        x = x0 + i * slot + (slot - bw) / 2
        hatch_bar(im, (x, Y(p), x + bw, base), INK if i in (0, n - 1) else FADE, seed=60 + i, step=10, width=4)
    d = ImageDraw.Draw(im)
    for xx in range(x0, x1, 36): d.line([(xx, Y(100)), (xx + 18, Y(100))], fill=GREY, width=4)
    T(d, (x1 + 10, Y(100) - 30), '고점 100%', 40, GREY, F_B, 'rm')
    med = st.median([c[4] for c in CPX]); assert round(med) == 84
    d.line([(x0 - 10, Y(med)), (x1 + 10, Y(med))], fill=OR, width=6)
    T(d, (W // 2, Y(100) - 85), f'가운데 {med:.0f}%', 104, OR, F_X)
    T(d, (x0 + slot / 2, Y(CPX[0][4]) - 32), f'{CPX[0][4]}%', 44, INK, F_X)
    T(d, (x1 - slot / 2, Y(CPX[-1][4]) - 40), f'{CPX[-1][4]}%', 48, INK, F_X)
    d.line([(x0 - 10, base), (x1 + 10, base)], fill=GREY, width=4)
    T(d, (W // 2, 960), '고점을 다시 넘은 곳 0 · 90% 넘은 곳 6', 52, INK, F_B)
    source(d, SRC_RT + ' · 단지마다 가운데 값끼리 · 고점 1년·최근 각 3건 이상 · 막대는 0%부터')

def cols3(im, rows, title_s, hi_last=False, seed=70):
    d = ImageDraw.Draw(im); TF(d, (W // 2, 120), title_s, 96, INK, F_X)
    for i, (nm, pk, rc, p) in enumerate(rows):
        cx = 330 + i * 630
        TF(d, (cx, 330), nm, 50, INK, F_B, maxw=560)
        T(d, (cx, 470), f'{pk:.2f}억', 64, GREY, F_B)
        hand_arrow(d, (cx, 525), (cx, 600), GREY, 6)
        T(d, (cx, 660), f'{rc:.2f}억', 76, INK, F_X)
        T(d, (cx, 830), f'{p}%', 170, OR if i == 0 else INK, F_X)
        if i < 2: d.line([(cx + 315, 300), (cx + 315, 900)], fill=LINE, width=3)
    return d

@board
def top3(im):              # 많이 돌아온 3곳
    rows = [(nm, pk, rc, p) for nm, by, pk, rc, p in CPX[:3]]
    d = cols3(im, rows, '많이 돌아온 3곳')
    hand_under(d, 200, 460, 915, seed=71)
    T(d, (W // 2, 985), '하버뷰는 최근 거래 3건 — 한 건에 크게 흔들려요', 46, INK, F_B)
    source(d, SRC_RT + ' · 고점 1년 가운데 값 → 최근(2026.07~10) 가운데 값')

@board
def pair(im):              # 센트럴시티 vs 힐스테이트레이크송도1차 — 고점 비슷, 지금 벌어짐
    d = ImageDraw.Draw(im); TF(d, (W // 2, 110), '고점은 비슷했는데', 100, INK, F_X)
    A = next(c for c in CPX if c[0] == '송도더샵센트럴시티'); Bc = next(c for c in CPX if c[0] == '힐스테이트레이크송도1차')
    base, top, vmax = 780, 300, 10.0; Y = lambda v: base - (base - top) * v / vmax
    for gi, (c, lab) in enumerate(((A, '송도더샵센트럴시티'), (Bc, '힐스테이트레이크송도1차'))):
        gx = 330 + gi * 860; bw = 190
        for k, (v, tag) in enumerate(((c[2], '고점 1년'), (c[3], '지금'))):
            x = gx + k * (bw + 70); col = INK if k == 0 else (OR if gi == 1 else INK)
            hatch_bar(im, (x, Y(v), x + bw, base), col if k == 1 else FADE, seed=80 + gi * 2 + k, step=12, width=5); d = ImageDraw.Draw(im)
            T(d, (x + bw / 2, Y(v) - 48), f'{v:.2f}억', 52 if k == 0 else 62, col if k == 1 else GREY, F_X)
            T(d, (x + bw / 2, base + 44), tag, 40, GREY, F_B)
        T(d, (gx + bw + 35, base + 130), lab, 54, INK, F_X)
    d.line([(220, base), (1700, base)], fill=GREY, width=4)
    source(d, SRC_RT + ' · 가운데 값 · 9.61억→9.25억 · 9.75억→6.90억 · 막대는 0억부터')

@board
def built(im):             # 지은 해 묶음 세 칸 — 모두 80%대
    d = ImageDraw.Draw(im); TF(d, (W // 2, 120), '새 아파트일수록 덜 빠졌을까?', 96, INK, F_X)
    G = re.findall(r'  ([^:\n]+?): (\d+)곳 · 최근÷고점 중앙 (\d+)%', _c2.split('## 3')[1].split('## 4')[0])
    assert len(G) == 3
    base, top, bw, gap = 740, 300, 280, 200; x = (W - (3 * bw + 2 * gap)) / 2
    for i, (lab, n, p) in enumerate(G):
        p = int(p); yt = base - (base - top) * p / 100
        hatch_bar(im, (x, yt, x + bw, base), INK, seed=90 + i, step=12, width=5); d = ImageDraw.Draw(im)
        T(d, (x + bw / 2, yt - 70), f'{p}%', 110, INK, F_X)
        T(d, (x + bw / 2, base + 50), lab, 50, INK, F_B); T(d, (x + bw / 2, base + 105), f'{n}곳', 40, GREY, F_B)
        x += bw + gap
    d.line([(300, base), (1620, base)], fill=GREY, width=4)
    T(d, (W // 2, 920), '세 묶음 모두 80%대', 72, OR, F_X)
    hand_under(d, W // 2 - 330, W // 2 + 330, 970, seed=93)
    source(d, SRC_RT + ' · 단지 33곳 · 묶음마다 단지 비율의 가운데 · 막대는 0%부터')

# ── 3. 반값·6~70% ───────────────────────────────────────────────────
def _deals():
    """calc2.py와 같은 거름 — 2022.07~2026.10 단지 33곳 84㎡대 거래 (년월, 그 단지 고점 1년 가운데 값 대비 비율, 직거래?)"""
    RT = os.path.join(EP, 'raw', 'rt'); num = lambda s: float(str(s or '0').replace(',', '') or 0)
    ym = lambda r: int(r['dealYear']) * 100 + int(r['dealMonth'])
    Tr = []
    for p in sorted(glob.glob(os.path.join(RT, '28185_*_trade.json'))): Tr += json.load(open(p, encoding='utf-8'))
    Tr = [r for r in Tr if not r.get('cdealType') and r.get('buyerGbn') != '공공기관' and r['umdNm'] == '송도동' and 80 <= num(r['excluUseAr']) <= 86]
    pk = {}
    for nm in {r['aptNm'] for r in Tr}:
        a = [num(r['dealAmount']) for r in Tr if r['aptNm'] == nm and 202107 <= ym(r) <= 202206]
        b = [r for r in Tr if r['aptNm'] == nm and 202607 <= ym(r) <= 202612]
        if len(a) >= 3 and len(b) >= 3: pk[nm] = st.median(a)
    out = [(ym(r), num(r['dealAmount']) / pk[r['aptNm']], r.get('dealingGbn') == '직거래') for r in Tr if ym(r) >= 202207 and r['aptNm'] in pk]
    return out

@board
def dots(im):              # 거래 점 4천여 개 — 50%·60% 선, 직거래만 주황
    D = _deals(); n = len(D); h50 = sum(1 for _, q, _ in D if q <= .5); h60 = [x for x in D if x[1] <= .6]
    dj = sum(1 for x in D if x[2]); dj60 = sum(1 for x in h60 if x[2])
    assert (n, h50, len(h60), dj60, dj) == (4284, 2, 27, 21, 131), (n, h50, len(h60), dj60, dj)
    d = ImageDraw.Draw(im); TF(d, (W // 2, 90), f'거래 {n:,}건 · 고점 1년 가운데 값의 몇 %에 팔렸나', 66, INK, F_X)
    x0, x1, y0, y1 = 220, 1700, 200, 760; q0, q1 = 0.4, 1.4
    m0 = 2022 * 12 + 6; m1 = 2026 * 12 + 9
    X = lambda m: x0 + (x1 - x0) * ((m // 100) * 12 + m % 100 - 1 - m0) / (m1 - m0)
    Y = lambda q: y1 - (y1 - y0) * (min(max(q, q0), q1) - q0) / (q1 - q0)
    import random; rnd = random.Random(5)
    for m, q, dj_ in sorted(D, key=lambda t: t[2]):
        x = X(m) + rnd.uniform(-9, 9); y = Y(q); r = 7 if dj_ else 4
        d.ellipse((x - r, y - r, x + r, y + r), fill=OR if dj_ else (150, 140, 128))
    for q, lab in ((1.0, '100%'), (0.6, '60%'), (0.5, '50%')):
        for xx in range(x0, x1, 34): d.line([(xx, Y(q)), (xx + 17, Y(q))], fill=INK if q < 1 else GREY, width=4)
        T(d, (x0 - 20, Y(q)), lab, 40, INK, F_B, 'rm')
    for yr in (2023, 2024, 2025, 2026): T(d, (X(yr * 100 + 1), y1 + 44), f'{yr}', 38, GREY, F_B)
    for m, q, _ in D:
        if q <= .5: x, y = X(m), Y(q); hand_ellipse(d, (x - 40, y - 40, x + 40, y + 40), seed=int(m) % 97)
    T(d, (W // 2, 880), '50% 이하 2건 · 둘 다 직거래', 76, OR, F_X)
    T(d, (W // 2, 960), '60% 이하 27건 중 직거래 21건', 50, INK, F_B)
    T(d, (x1, 160), '● 직거래', 40, OR, F_B, 'rm')
    source(d, f'{SRC_RT} · 2022.07~2026.10 단지 33곳 · 직거래 {dj}건({dj / n * 100:.1f}%) · 140% 넘는 점은 위 끝에')

@board
def ruler(im):             # 무엇 ÷ 무엇? — 잣대 두 줄 + 마리나베이
    d = ImageDraw.Draw(im)
    assert '최고 한 건 기준 중앙 73.9% (52~86%) · 가운데 값끼리 중앙 84.1%' in _c4
    TF(d, (W // 2, 110), '"6~70%"는 무엇 ÷ 무엇?', 96, INK, F_X)
    rows = (('지금 가운데 값 ÷ 고점 때 최고 한 건', '74%', INK), ('지금 가운데 값 ÷ 고점 1년 가운데 값', '84%', OR))
    for i, (a, b, c) in enumerate(rows):
        y = 320 + i * 200
        T(d, (130, y), f'{"①②"[i]}', 70, GREY, F_X, 'lm'); T(d, (230, y), a, 58, INK, F_B, 'lm')
        T(d, (1790, y), b, 150, c, F_X, 'rm')
        d.line([(130, y + 100), (1790, y + 100)], fill=LINE, width=2)
    T(d, (W // 2, 545 + 100), '같은 단지 33곳', 44, GREY, F_B)
    mb = next(c for c in CPX if c[0] == '더샵송도마리나베이'); assert (mb[2], mb[3], mb[4]) == (8.09, 6.45, 80)
    T(d, (W // 2, 760), '더샵송도마리나베이', 62, INK, F_X)
    T(d, (560, 880), '최고 한 건으로  52%', 70, INK, F_B); T(d, (1360, 880), '가운데 값끼리  80%', 70, INK, F_B)
    d.line([(W // 2, 830), (W // 2, 930)], fill=LINE, width=3)
    source(d, SRC_RT + ' · 최고 한 건 = 2021~22 가장 비싼 거래 · 마리나베이 12.45억 / 8.09억 → 6.45억')

# ── 4. 전세 ─────────────────────────────────────────────────────────
@board
def jeonse(im):            # 전세 가격대 막대(0.5억 칸) — 4.0~4.5억 주황
    d = ImageDraw.Draw(im); TF(d, (W // 2, 110), '84㎡ 전세 821건 · 가격대', 92, INK, F_X)
    bins = [b for b in JBIN if b[0] >= 2.0]   # 0.5~1.0억 1건은 출처 줄에
    base, top = 820, 280; vmax = max(n for *_, n in bins); slot = 1480 / len(bins); bw = slot * 0.66; x0 = 220
    for i, (a, b, n) in enumerate(bins):
        x = x0 + i * slot + (slot - bw) / 2; yt = base - (base - top) * n / vmax; c = OR if a == 4.0 else INK
        hatch_bar(im, (x, yt, x + bw, base), c, seed=110 + i, step=11, width=5); d = ImageDraw.Draw(im)
        T(d, (x + bw / 2, yt - 40), f'{n}', 64 if a == 4.0 else 40, c, F_X if a == 4.0 else F_B)
        T(d, (x + bw / 2, base + 40), f'{a:g}억', 36, c, F_B)
    d.line([(x0 - 10, base), (x0 + 1490, base)], fill=GREY, width=4)
    T(d, (W // 2, 960), '가운데 값 4억 1천5백 · 4억대 초반이 가장 많아요', 60, INK, F_X)
    source(d, '국토교통부 아파트 전월세 실거래 · 송도동 84㎡대 순수전세 2026.07~10 · 칸 = 0.5억(그 값 이상~다음 칸 미만) · 0.5~1.0억 1건 생략')

@board
def ratio(im):             # 단지별 전세가율 점 38곳 — 가운데 57% 선
    d = ImageDraw.Draw(im); TF(d, (W // 2, 110), '전세가 매매의 몇 %? 단지 38곳', 86, INK, F_X)
    rows = sorted(RATIO, key=lambda r: -r[1]); n = len(rows)
    x0, x1, y0, y1 = 220, 1620, 260, 840; p0, p1 = 35, 75
    Y = lambda p: y1 - (y1 - y0) * (p - p0) / (p1 - p0)
    for p in (40, 50, 60, 70):
        d.line([(x0, Y(p)), (x1, Y(p))], fill=LINE, width=2); T(d, (x0 - 20, Y(p)), f'{p}%', 38, GREY, F_B, 'rm')
    med = st.median([p for _, p in rows]); assert abs(med - 57) <= 1, med; med = 57   # calc_out §4 '단지 38곳 전세가율 중앙 57%'(반올림 전 값의 중앙)
    for i, (nm, p) in enumerate(rows):
        x = x0 + (x1 - x0) * (i + .5) / n; r = 14
        d.ellipse((x - r, Y(p) - r, x + r, Y(p) + r), fill=INK)
    d.line([(x0, Y(med)), (x1, Y(med))], fill=OR, width=7)
    T(d, (x1 + 20, Y(med)), '57%', 96, OR, F_X, 'lm')
    T(d, (x0 + 40, Y(rows[0][1]) - 50), f'높은 곳 {rows[0][1]}%', 46, INK, F_B, 'lm')
    T(d, (x1 - 40, Y(rows[-1][1]) + 55), f'낮은 곳 {rows[-1][1]}%', 46, INK, F_B, 'rm')
    T(d, (W // 2, 960), '가운데 57% · 39%~70%', 62, INK, F_X)
    source(d, '국토교통부 매매·전월세 실거래 · 송도동 84㎡대 2026.07~10 · 단지마다 전세 가운데 값 ÷ 매매 가운데 값 · 높은 순')

# ── 5. 직접 확인 ───────────────────────────────────────────────────
@board
def check5(im):            # 체크리스트 다섯 · rt.molit.go.kr
    d = ImageDraw.Draw(im); TF(d, (W // 2, 110), '내 단지 직접 셀 때', 100, INK, F_X)
    rows = ('아파트 매매인가 (오피스텔·경매 아님)', '같은 넓이끼리', '유난히 싼 한 건은 직거래인가', '고점 = 2021 하반기~2022 상반기 1년 가운데 값', "'해제' 표시 거래는 빼기")
    for i, s in enumerate(rows):
        y = 260 + i * 128
        hand_check(d, 300, y + 4, 52, OR if i == 3 else INK, 10)
        T(d, (400, y), s, 62, OR if i == 3 else INK, F_B, 'lm')
    T(d, (W // 2, 935), 'rt.molit.go.kr', 96, INK, F_X)
    source(d, '국토교통부 실거래가 공개시스템 · 신고 기한 계약일부터 30일 — 이번 달 거래는 덜 들어옴')

# ── 6. 정리 ─────────────────────────────────────────────────────────
@board
def summary(im):           # 정리 표 4줄
    d = ImageDraw.Draw(im); T(d, (W // 2, 120), '송도 84㎡ 한 장 정리', 110, INK, F_X)
    rows = (('동 전체', '고점 9억 → 지금 7억 4천 (82%)'), ('단지 33곳', '71% ~ 97% · 가운데 84%'),
            ('반값 거래', '2건 · 둘 다 직거래'), ('전세', '가운데 4억 1천5백 · 매매의 57%'))
    for i, (a, b) in enumerate(rows):
        y = 300 + i * 150
        T(d, (560, y), a, 60, GREY, F_B, 'rm'); T(d, (600, y), b, 76, OR if i == 0 else INK, F_X, 'lm')
        if i < 3: d.line([(200, y + 75), (1760, y + 75)], fill=LINE, width=2)
    T(d, (W // 2, 900), '내 단지는  rt.molit.go.kr  에서 같은 넓이로', 66, INK, F_X)
    source(d, SRC_RT + ' · 2026.07~10 · 계산·비교 자료이며 매수·매도 권유가 아닙니다')

def main(names):
    os.makedirs(OUT, exist_ok=True)
    for n in names or list(B):
        im = canvas(); B[n](im); im.save(os.path.join(OUT, n + '.png')); print(n)

if __name__ == '__main__':
    main(sys.argv[1:])
