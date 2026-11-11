"""H-4 장면 판 — visual-designer 2026-11-09. K-1 판(k1boards.py)과 같은 꼴·같은 부품을 불러 쓴다:
구겨진 종이 바탕 · 펜 빗금 막대(hatch_bar, bgcheck ⑥ 상자 안 걸림) · 주황 #FF5A00은 그 화면의 답 하나 · 손 동그라미·밑줄.
숫자는 ep/H-4/facts.txt·calc_out.txt 값만(바꾸지 않음). 막대 높이는 0원부터(11/1 교훈 — 바닥 자르면 오독).
지도: 통계청 센서스용 행정구역경계 2013(southkorea-maps 정리본, geo/) — 모양만 쓰고 출처 줄에 적는다.
판은 '답이 열린 마지막 모습' — '?' → 열림 움직임은 PD가 Remotion에서 건다.
사용: py -3.12 h4boards.py [이름 ...]   (없으면 전부) → work/video/public/bg/h4/board/<이름>.png
"""
import os, sys, json, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'K-1-shots'))
import k1boards as K
from k1boards import (W, H, INK, GREY, SRC, OR, KRAFT, KRAFT_L, FADE, F_B, F_M, F_X, font, canvas, T, TF, title, source,
                      hand_ellipse, hand_under, hand_check, hand_arrow, hatch_bar)
from PIL import ImageDraw

WORK = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
OUT = os.path.join(WORK, 'video', 'public', 'bg', 'h4', 'board')
GEO = os.path.join(HERE, 'geo')
SRC_RT = '국토교통부 아파트 매매 실거래 · 84㎡대(전용 80~85㎡) 가운데 값'

# calc_out §1 (2026.07~09 계약) — 26곳, 비싼 순
RANK = [('강남구', 30.30), ('서초구', 24.99), ('송파구', 22.00), ('성동구', 19.30), ('용산구', 19.25), ('광진구', 17.80), ('마포구', 16.55),
        ('중구', 16.30), ('동작구', 16.00), ('강동구', 15.00), ('영등포구', 14.30), ('동대문구', 12.05), ('종로구', 12.00), ('양천구', 12.00),
        ('서대문구', 12.00), ('강서구', 11.00), ('성북구', 10.00), ('광명시', 9.70), ('관악구', 9.44), ('은평구', 9.40), ('구로구', 8.26),
        ('노원구', 8.20), ('강북구', 8.10), ('중랑구', 8.00), ('금천구', 7.10), ('도봉구', 6.20)]
# calc_out §2 — 철산동 84㎡대 1년 매매 가운데 값, 16곳
LADDER = [('롯데캐슬&SKVIEW', 2022, 15.95), ('센트럴푸르지오', 2021, 15.09), ('주공13', 1986, 13.85), ('래미안자이', 2009, 13.40),
          ('주공12', 1986, 13.25), ('푸르지오하늘채', 2010, 12.80), ('광명푸르지오', 2007, 9.95), ('브라운스톤2차', 2007, 9.40),
          ('브라운스톤', 2006, 9.39), ('쌍마한신', 1992, 8.90), ('도덕파크타운1단지', 2002, 8.45), ('두산위브', 2007, 8.06),
          ('롯데낙천대', 2005, 7.10), ('우성', 1990, 7.00), ('광복현대', 1998, 6.73), ('철산리버빌주공', 2001, 6.35)]

B = {}
def board(fn):
    B[fn.__name__] = fn; return fn

def rank_bars(im, hi=None, x0=150, x1=1770, base=900, top=300, seed=40, col_hi=OR):
    """26칸 막대(0부터). hi: 강조할 이름 집합 → 그 칸만 진하게, 나머지는 바랜 색. 막대 x 범위를 돌려준다."""
    n = len(RANK); slot = (x1 - x0) / n; bw = slot * 0.62; vmax = RANK[0][1]; xs = {}
    for i, (nm, v) in enumerate(RANK):
        x = x0 + i * slot + (slot - bw) / 2; y = base - (base - top) * v / vmax
        if nm == '광명시': c = col_hi
        elif hi is None or nm in hi: c = INK
        else: c = FADE
        hatch_bar(im, (x, y, x + bw, base), c, seed=seed + i, step=11, width=5)
        xs[nm] = (x, y, x + bw)
    d = ImageDraw.Draw(im); d.line([(x0 - 10, base), (x1 + 10, base)], fill=GREY, width=4)
    return xs

@board
def rank26(im):
    d = ImageDraw.Draw(im)
    TF(d, (W // 2, 110), '서울 25개 구 + 광명, 비싼 순', 80, INK, F_B)
    xs = rank_bars(im); d = ImageDraw.Draw(im)
    x, y, xr = xs['광명시']; cx = (x + xr) / 2
    T(d, (cx, y - 190), '18번째', 150, OR, F_X)
    hand_ellipse(d, (cx - 60, y - 40, cx + 60, y + 130), seed=41)
    T(d, (cx, 960), '광명시', 44, OR, F_B)
    source(d, SRC_RT + ' · 2026년 7~9월 계약')

def source_card(im):   # 파일 이름은 source.png(장면 계획 그대로) — 함수 이름은 출처 줄 source()와 안 겹치게
    d = ImageDraw.Draw(im)
    T(d, (W // 2, 230), '같은 잣대', 150, INK, F_X)
    rows = (('자료', '국토교통부 아파트 매매 실거래'), ('기간', '2026년 7~9월 계약 · 같은 석 달'), ('크기', '84㎡대만 (전용 80~85㎡)'), ('값', '가운데 값'))
    for i, (a, b) in enumerate(rows):
        y = 470 + i * 130
        T(d, (560, y), a, 54, GREY, F_B, 'rm'); T(d, (620, y), b, 68 if i < 3 else 80, OR if i == 3 else INK, F_X if i == 3 else F_B, 'lm')
    hand_under(d, 620, 620 + font(F_X, 80).getlength('가운데 값'), 470 + 3 * 130 + 56, seed=51)
    source(d, '서울 25개 구와 광명시 · 해제·공공기관 매수 거래는 뺌')
B['source'] = source_card

@board
def rank_zoom(im):
    d = ImageDraw.Draw(im); TF(d, (W // 2, 110), '광명 바로 위·아래', 110, INK, F_X)
    seg = RANK[15:20]; vmax = 11.0; base, top = 900, 330; bw, gap = 210, 120
    tot = len(seg) * bw + (len(seg) - 1) * gap; x = (W - tot) / 2
    for i, (nm, v) in enumerate(seg):
        lab = nm in ('성북구', '광명시', '관악구'); c = OR if nm == '광명시' else (INK if lab else FADE)
        y = base - (base - top) * v / vmax
        hatch_bar(im, (x, y, x + bw, base), c, seed=60 + i); d = ImageDraw.Draw(im)
        if lab:
            T(d, (x + bw / 2, y - 70), f'{v:.2f}억', 84 if nm != '광명시' else 96, c, F_X)
            T(d, (x + bw / 2, base + 60), nm, 54, c, F_B)
        x += bw + gap
    d.line([(200, base), (1720, base)], fill=GREY, width=4)
    source(d, SRC_RT + ' · 2026년 7~9월 계약 · 막대는 0억부터')

@board
def rank_ends(im):
    d = ImageDraw.Draw(im)
    xs = rank_bars(im, hi={'강남구', '도봉구'}); d = ImageDraw.Draw(im)
    x, y, xr = xs['강남구']; T(d, (xr + 30, y + 40), '강남구 30억', 134, INK, F_X, 'lm')
    x, y, xr = xs['도봉구']; T(d, ((x + xr) / 2, y - 60), '도봉구 6억', 64, INK, F_B, 'rm')
    gx, gy, gxr = xs['광명시']; dx, dy, dxr = xs['도봉구']
    # 11/11 copywriter 요청: 광명보다 비싼 서울 구 17곳(25−8, facts [2][3]) — 위 한 줄 + 강남~성북 17칸 위에 손 괄호선
    TF(d, (W // 2, 105), '광명보다 비싼 서울 구 17곳', 92, INK, F_X)
    hand_under(d, xs['강남구'][0], xs['성북구'][2], 190, INK, 7, seed=17)
    # 손 화살표: 도봉(맨 아래)부터 광명까지 아홉 칸을 거꾸로 셈
    for k in range(9):
        nm = RANK[25 - k][0]; a, _, b = xs[nm]
        T(d, ((a + b) / 2, 930), str(k + 1), 40, OR if k == 8 else GREY, F_B)
    hand_arrow(d, (dxr, 968), (gx, 968), OR, 6)   # 11/9 심사 r08: 출처 줄 덮던 화살표 위로
    T(d, ((gx + gxr) / 2, gy - 90), '아래에서 9번째', 72, OR, F_X)
    source(d, SRC_RT + ' · 2026년 7~9월 계약')

def _geo(fn):
    return json.load(open(os.path.join(GEO, fn), encoding='utf-8'))['features']

def _rings(f):
    g = f['geometry']; polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
    return [p[0] for p in polys]

def _proj(feats, box):
    xs = [x for f in feats for r in _rings(f) for x, _ in r]; ys = [y for f in feats for r in _rings(f) for _, y in r]
    lat0 = sum(ys) / len(ys); k = math.cos(math.radians(lat0))
    w0, h0 = (max(xs) - min(xs)) * k, max(ys) - min(ys); bx0, by0, bx1, by1 = box
    s = min((bx1 - bx0) / w0, (by1 - by0) / h0); ox = bx0 + ((bx1 - bx0) - w0 * s) / 2; oy = by0 + ((by1 - by0) - h0 * s) / 2
    mnx, mxy = min(xs), max(ys)
    return lambda x, y: (ox + (x - mnx) * k * s, oy + (mxy - y) * s)

@board
def dong3(im):
    d = ImageDraw.Draw(im); feats = _geo('gm_dong.json'); P = _proj(feats, (110, 170, 900, 1000))
    grp = {'철산': INK, '하안': OR, '광명': GREY}
    cen = {}
    for f in feats:
        nm = f['properties']['name']; g = next((k for k in grp if nm.startswith(k)), None)
        fill = (226, 214, 192) if g is None else ((246, 206, 176) if g == '하안' else (214, 200, 176))
        for r in _rings(f):
            pts = [P(x, y) for x, y in r]; d.polygon(pts, fill=fill); d.line(pts + [pts[0]], fill=(150, 140, 126), width=2)
            if g: cen.setdefault(g, []).extend(pts)
    for g, pts in cen.items():
        cx = sum(p[0] for p in pts) / len(pts); cy = sum(p[1] for p in pts) / len(pts)
        cen[g] = (cx, cy)
    rows = (('철산동', '10.30억', '45건', INK), ('광명동', '8.50억', '46건', INK), ('하안동', '12.50억', '17건', OR))
    for i, (a, b, c, col) in enumerate(rows):
        y = 320 + i * 190
        tot = row(d, 1800, y, [(a, 64, col, F_B), (c, 44, GREY, F_B), (b, 130, col, F_X)], 24, 'r')
        tx, ty = cen[a[:2]]; d.ellipse((tx - 12, ty - 12, tx + 12, ty + 12), fill=col)
        d.line([(tx + 14, ty), (1800 - tot - 20, y)], fill=col, width=4)   # 11/9 심사 r10: 지도 어느 칸인지 — 줄에서 그 동 가운데로 손 선
    hand_under(d, 1800 - font(F_X, 130).getlength('12.50억'), 1800, 320 + 2 * 190 + 78, seed=71)   # 원이 숫자를 가로지름 → 밑줄
    T(d, (1400, 900), '1년 전체 매매  철산 1,015 · 하안 791 · 광명 683건', 44, INK, F_B)
    source(d, '국토교통부 매매 실거래 · 84㎡대 석 달(2026년 7~9월) 가운데 값 · 1년(2025.11~2026.10)은 전 면적 · 경계 통계청 2013')

@board
def memo30(im):
    d = ImageDraw.Draw(im)
    T(d, (W // 2, 330), '10월 계약은', 120, INK, F_X)
    T(d, (W // 2, 500), '아직 덜 들어왔어요', 140, OR, F_X)
    hand_under(d, 420, 1500, 590, seed=81)
    T(d, (W // 2, 760), '실거래 신고 기한 30일 → 이번 순위는 7~9월 계약만', 54, INK, F_B)
    source(d, '부동산 거래신고: 계약일부터 30일 안')

@board
def new_vs_all(im):
    d = ImageDraw.Draw(im); TF(d, (W // 2, 110), '광명 84㎡대 가운데 값', 90, INK, F_B)
    tops = K.bars(im, [('광명 전체 171건', 9.70, INK, '', INK), ('2019년 뒤 지은 단지 24건', 14.71, OR, '', OR)],
                  base_y=860, top_y=330, bw=330, gap=420, vmax=15.5, seed=90, nsize=140)
    d = ImageDraw.Draw(im)
    for (x, y, xr), v, c in zip(tops, ('9.70억', '14.71억'), (INK, OR)): T(d, ((x + xr) / 2, y - 105), v, 140, c, F_X)   # 11/9 심사 r13: 원 빼고 숫자를 막대에서 띄움
    x, y, xr = tops[1]; hand_under(d, (x + xr) / 2 - 240, (x + xr) / 2 + 240, y - 22, seed=91)
    d.line([(300, 860), (1620, 860)], fill=GREY, width=4)
    source(d, SRC_RT + ' · 2026년 7~9월 계약 · 막대는 0억부터')

@board
def new_rank(im):
    """youtube-loop 대본 줄 확인 ②: '영등포구보다 위로' — new_vs_all 다음 박자."""
    d = ImageDraw.Draw(im); TF(d, (W // 2, 120), '새 단지만 서울 줄에 끼우면', 96, INK, F_B)
    rows = (('10', '강동구', '15.00억', INK), ('', '광명 2019년 뒤 단지', '14.71억', OR), ('11', '영등포구', '14.30억', INK))   # 11/9: 동대문구 줄 뺌(대본에 없음, ⑤ 8줄)
    for i, (r, a, b, c) in enumerate(rows):
        y = 330 + i * 170
        T(d, (300, y), a, 64 if c == OR else 62, c, F_X if c == OR else F_B, 'lm'); T(d, (1620, y), b, 124 if c == OR else 72, c, F_X, 'rm')
    hand_under(d, 300, 1620, 330 + 170 + 76, seed=101)   # 11/9 심사 r14: 이름 줄이고 숫자 오른쪽 끝 맞춤
    source(d, SRC_RT + ' · 2026년 7~9월 계약')

@board
def gap171(im):
    """youtube-loop 대본 줄 확인 ③: '광명 전체 171건 9억 7천 · 새 단지 24건 14억 7천'."""
    d = ImageDraw.Draw(im)
    T(d, (W // 2, 300), '광명 전체 171건', 70, GREY, F_B); T(d, (W // 2, 420), '9억 7천', 150, INK, F_X)
    T(d, (W // 2, 620), '새 단지 24건', 70, GREY, F_B); T(d, (W // 2, 740), '14억 7천', 150, OR, F_X)
    hand_under(d, 700, 1220, 830, seed=111)
    T(d, (W // 2, 930), '같은 광명, 같은 84㎡대 · 차이 약 5억', 54, INK, F_B)
    source(d, SRC_RT + ' · 2026년 7~9월 계약 · 새 단지 = 2019년 뒤 지은 단지')

@board
def rt_steps(im):
    d = ImageDraw.Draw(im)
    T(d, (W // 2, 170), 'rt.molit.go.kr', 140, INK, F_X)
    T(d, (W // 2, 300), '국토교통부 실거래가 공개시스템 · 누구나 무료', 54, GREY, F_B)
    steps = ('아파트 · 매매', '같은 동 · 같은 크기', '1년 치 가운데 값')
    for i, s in enumerate(steps):
        cx = 380 + i * 580; y = 600
        hand_ellipse(d, (cx - 70, y - 200, cx + 70, y - 60), INK, 6, seed=120 + i); T(d, (cx, y - 130), str(i + 1), 80, OR if i == 2 else INK, F_X)
        T(d, (cx, y + 20), s, 66, OR if i == 2 else INK, F_B)
        if i < 2: hand_arrow(d, (cx + 230, y - 130), (cx + 350, y - 130), GREY, 5)
    hand_under(d, 380 + 2 * 580 - 230, 380 + 2 * 580 + 230, 690, seed=125)
    source(d, '우리가 다시 그린 순서 · 화면 캡처 아님')

def _wobble_rect(d, box, color=INK, width=5, seed=1):
    import random
    rnd = random.Random(seed); x0, y0, x1, y1 = box; pts = []
    for (ax, ay, bx, by) in ((x0, y0, x1, y0), (x1, y0, x1, y1), (x1, y1, x0, y1), (x0, y1, x0, y0)):
        for i in range(12): t = i / 12; pts.append((ax + (bx - ax) * t + rnd.uniform(-2.5, 2.5), ay + (by - ay) * t + rnd.uniform(-2.5, 2.5)))
    d.line(pts + [pts[0]], fill=color, width=width, joint='curve')

@board
def zero_deal(im):
    d = ImageDraw.Draw(im)
    hand_under(d, 280, 1640, 335, INK, 6, seed=131)
    T(d, (320, 270), '철산자이더헤리티지', 76, INK, F_B, 'lm')
    cx, cy, r = 1570, 262, 36; d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=INK, width=8); d.line([(cx + 25, cy + 25), (cx + 58, cy + 58)], fill=INK, width=10)
    T(d, (W // 2, 520), '매매 실거래', 90, INK, F_B)
    T(d, (W // 2, 690), '0건', 200, OR, F_X)
    hand_ellipse(d, (W // 2 - 220, 590, W // 2 + 220, 800), seed=132)
    T(d, (W // 2, 900), '분양권 거래는 이 자료에 없음', 54, INK, F_B)
    source(d, '국토교통부 아파트 매매 실거래(분양권 전매 제외) · 2025.11~2026.10 계약 · 검색창은 다시 그림')

@board
def ladder16(im):
    d = ImageDraw.Draw(im); TF(d, (W // 2, 100), '철산동 84㎡대, 같은 동 같은 크기', 84, INK, F_B)
    x0, x1, base, top = 140, 1780, 880, 330; n = len(LADDER); slot = (x1 - x0) / n; bw = slot * 0.66; vmax = 16.5
    def col(yr): return INK if yr >= 2019 else ((140, 104, 66) if yr >= 2000 else GREY)
    for i, (nm, yr, v) in enumerate(LADDER):
        x = x0 + i * slot + (slot - bw) / 2; y = base - (base - top) * v / vmax
        hatch_bar(im, (x, y, x + bw, base), col(yr), seed=140 + i, step=11, width=5)
        if i in (0, n - 1):
            d = ImageDraw.Draw(im)
            if i == 0: T(d, (x + bw / 2 + 110, y - 90), f'{v:.2f}억', 132, OR, F_X)
            else:   # 11/9 심사 r20: 어느 막대인지 — 맨 오른쪽 막대 위로 올리고 손 선
                T(d, (x + bw + 10, y - 250), f'{v:.2f}억', 132, OR, F_X, 'rm'); d.line([(x + bw / 2, y - 175), (x + bw / 2, y - 12)], fill=OR, width=5)
    d = ImageDraw.Draw(im); d.line([(x0 - 10, base), (x1 + 10, base)], fill=GREY, width=4)
    for (lab, c), xx in zip((('2019년 뒤', INK), ('2000~2010년', (140, 104, 66)), ('1980~90년대', GREY)), (560, 960, 1380)):
        hatch_bar(im, (xx - 120, 935, xx - 80, 975), c, seed=150, step=9, width=4); d = ImageDraw.Draw(im)
        T(d, (xx - 64, 955), lab, 40, c, F_B, 'lm')
    source(d, '국토교통부 매매 실거래 · 2025.11~2026.10 계약 · 5건 이상 16곳 · 막대는 0억부터')

@board
def duel(im):
    d = ImageDraw.Draw(im)
    for i, (yr, nm, v, c) in enumerate((('1986년', '주공13단지', '13.85억', OR), ('2009년', '래미안자이', '13.40억', INK))):
        cx = 520 + i * 880
        T(d, (cx, 280), yr, 90, GREY, F_X); T(d, (cx, 420), nm, 84, INK, F_B); T(d, (cx, 610), v, 170, c, F_X)
    T(d, (W // 2, 610), '>', 120, GREY, F_X)
    hand_under(d, 260, 780, 720, seed=161)
    T(d, (W // 2, 880), '오래된 단지가 조금 더 비쌈 · 차이 5천만원 아래', 60, INK, F_B)
    source(d, '국토교통부 매매 실거래 · 84㎡대 1년 가운데 값 · 주공13 32건 · 래미안자이 35건')

@board
def gosi2(im):
    d = ImageDraw.Draw(im)
    for i, (no, nm, dt) in enumerate((('제2025-105호', '철산주공13단지', '2025. 5. 9.'), ('제2025-190호', '철산주공12단지', '2025. 8. 4.'))):
        x0 = 220 + i * 780
        T(d, (x0 + 350, 260), no, 96, INK, F_X); T(d, (x0 + 350, 420), f'{nm} · {dt}', 54, INK, F_B)
    T(d, (W // 2, 130), '경기도 광명시 고시', 60, GREY, F_B)
    T(d, (W // 2, 760), '정비구역 지정', 160, OR, F_X)
    hand_under(d, 460, 1460, 860, seed=175)
    T(d, (W // 2, 950), '원문 제목: 정비계획 수립 및 정비구역 지정', 46, INK, F_B)
    source(d, '토지이음 고시 원문 제목 그대로 · 사업시행인가 고시는 찾지 못함 · 다시 그림')

@board
def hagan(im):
    d = ImageDraw.Draw(im)
    T(d, (W // 2, 220), '하안동', 150, INK, F_X)
    T(d, (W // 2, 420), '84㎡대 석 달 17건 가운데 값', 60, GREY, F_B)
    T(d, (W // 2, 580), '12.50억', 170, OR, F_X); hand_under(d, 640, 1280, 680, seed=181)
    T(d, (W // 2, 820), '1년 매매(전 면적) 791건 · 단지별 값은 이번에 안 셈', 52, INK, F_B)
    source(d, '국토교통부 매매 실거래 · 2026년 7~9월(1년은 2025.11~2026.10) 계약')

def row(d, x, y, parts, gap=26, anchor='l'):
    """한 줄을 조각(글, 크기, 색, 글꼴)으로 이어 그림 — 칸을 멀리 띄우면 bgcheck가 글자 줄을 따로 세서(⑤ 8줄) 붙여 쓴다."""
    ws = [font(f, z).getlength(t) for t, z, c, f in parts]; tot = sum(ws) + gap * (len(parts) - 1)
    if anchor == 'c': x -= tot / 2
    elif anchor == 'r': x -= tot
    for (t, z, c, f), w in zip(parts, ws): T(d, (x, y), t, z, c, f, 'lm'); x += w + gap
    return tot

def _under9(im, rows, last, page):
    """11/9 2차 심사 r25·r26: 가운데 맞춤이라 칸이 들쭉날쭉 → 값(폭 같음)을 앞에 두고 왼쪽 맞춤 — 값·이름 칸이 세로로 맞는다.
    세 칸을 멀리 띄우면 bgcheck ⑤가 칸마다 줄로 세므로 한 줄로 붙여 쓴다. 제목에 1/2·2/2."""
    d = ImageDraw.Draw(im)
    row(d, W // 2, 140, [('9억 안쪽 7곳', 140, INK, F_X), (page, 60, GREY, F_B)], 30, 'c')
    for i, (nm, yr, v) in enumerate(rows):
        y = 370 + i * 150
        row(d, 420, y, [(f'{v:.2f}억', 84, INK, F_X), (nm, 66, INK, F_B), (f'{yr}년', 60, OR if yr == last else GREY, F_B)], 28, 'l')
    T(d, (W // 2, 370 + 4 * 150 - 10), '가장 새것도 2007년' if last == 2007 else '가장 오래된 곳 1990년', 60, OR, F_X)
    source(d, '국토교통부 매매 실거래 · 철산동 84㎡대 1년 가운데 값(비싼 순) · 2025.11~2026.10 계약')

UNDER9 = [r for r in LADDER if r[2] <= 9.0]
@board
def under9(im): _under9(im, UNDER9[:4], 2007, '1/2')      # 비싼 순 앞 4곳 · 가장 새것 2007년 주황
@board
def under9b(im): _under9(im, UNDER9[4:], 1990, '2/2')    # 뒤 3곳 · 가장 오래된 1990년 주황

@board
def loan_q(im):
    """5장 첫 줄 '대출 질문 · 실거주에 현찰 있는 사람만?' — 11/9 2차 심사 r33: 영어 서류 클립(8061370) 못함, 도장 AI 6장은 서양 밀랍 봉인 → 댓글 메모 판."""
    d = ImageDraw.Draw(im)
    T(d, (W // 2, 170), '댓글에 많았던 말', 60, GREY, F_B)
    T(d, (W // 2, 360), '실거주에 현찰 있는', 130, INK, F_X)
    T(d, (W // 2, 540), '사람만 사는 동네?', 130, INK, F_X)
    hand_under(d, 380, 1540, 630, INK, seed=271)
    T(d, (W // 2, 790), '대출 한도·허가, 두 가지만 봅니다', 72, OR, F_X)
    source(d, '유튜브 광명 영상 댓글 요약 · 우리가 다시 씀')

@board
def jeonse_line(im):
    d = ImageDraw.Draw(im); TF(d, (W // 2, 100), '새 단지 전세 vs 옆 단지 매매', 96, INK, F_X)
    x0, x1, base, top = 200, 1720, 900, 260; vmax, vmin = 16.5, 5.5
    Y = lambda v: base - (base - top) * (v - vmin) / (vmax - vmin)
    yl = Y(8.70); xx = x0
    while xx < x1: d.line([(xx, yl), (min(xx + 30, x1), yl)], fill=OR, width=7); xx += 48
    T(d, (x1 + 10, yl - 330), '새 단지 전세 8.70억', 132, OR, F_X, 'rm'); d.line([(x1 - 200, yl - 255), (x1 - 200, yl - 10)], fill=OR, width=5)   # 11/9 심사 r27: 점과 안 겹치게 위로
    n = len(LADDER); below = 0
    for i, (nm, yr, v) in enumerate(LADDER):
        cx = x0 + 40 + i * (x1 - x0 - 380) / (n - 1); cy = Y(v); r = 20
        if v <= 8.70: below += 1; d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=INK, width=7)
        else: d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=FADE)
    T(d, (560, Y(6.0) + 10), f'매매가 이 선 아래 {below}곳', 66, INK, F_X)
    T(d, (x0 + 40 + 36, Y(15.95)), '15.95억', 48, GREY, F_B, 'lm'); _cx = x0 + 40 + (n - 1) * (x1 - x0 - 380) / (n - 1); T(d, (_cx + 36, Y(6.35)), '6.35억', 48, INK, F_B, 'lm')
    T(d, (140, top - 70), '점 = 단지별 매매 가운데 값', 40, GREY, F_B, 'lm')
    source(d, '국토교통부 전월세·매매 실거래 · 철산자이더헤리티지 전세 12건(신규) · 철산동 84㎡대 16곳 1년')

@board
def newjeonse_eq(im):
    """youtube-loop 대본 줄 확인 ⑤."""
    d = ImageDraw.Draw(im)
    row(d, W // 2, 260, [('새 단지 전세', 130, OR, F_X), ('8.70억', 130, OR, F_X)], 40, 'c'); T(d, (W // 2, 420), '≈', 110, GREY, F_X)
    row(d, W // 2, 580, [('옆 단지 매매', 130, INK, F_X), ('6.35~8.45억', 110, INK, F_X)], 40, 'c')   # 11/9 심사 r28: 숫자 붙임(facts [10][11])
    hand_under(d, 360, 1560, 670, INK, seed=191)
    T(d, (W // 2, 820), '왜 이 값인지는 자료에 없음', 56, GREY, F_B)
    source(d, '국토교통부 전월세·매매 실거래 · 둘 다 9억 근처')

@board
def jeonse3(im):
    d = ImageDraw.Draw(im); TF(d, (W // 2, 110), '같은 철산동 84㎡, 새로 맺은 전세', 84, INK, F_B)
    rows = (('2025년 새 단지', 8.70, OR), ('2009년 래미안자이', 7.00, INK), ('1986년 주공13', 3.80, INK))
    x0, x1 = 640, 1260   # 11/9 심사 r29: 8.70억이 오른쪽에서 잘림
    for i, (nm, v, c) in enumerate(rows):
        y = 330 + i * 210
        T(d, (x0 - 40, y + 50), nm, 60, INK, F_B, 'rm')
        hatch_bar(im, (x0, y, x0 + (x1 - x0) * v / 9.0, y + 100), c, seed=200 + i); d = ImageDraw.Draw(im)
        T(d, (x0 + (x1 - x0) * v / 9.0 + 30, y + 50), f'{v:.2f}억', 144 if c == OR else 84, c, F_X, 'lm')
    T(d, (W // 2, 990 - 30), '두 배 넘게 차이', 60, INK, F_X)
    source(d, '국토교통부 전월세 실거래 · 신규 계약만 가운데 값 · 막대는 0억부터')

@board
def ratio(im):
    d = ImageDraw.Draw(im); TF(d, (W // 2, 110), '매매 대비 전세 (%)', 110, INK, F_X)
    tops = K.bars(im, [('주공13 (1986)', 27, OR, '27%', OR), ('래미안자이 (2009)', 52, INK, '52%', INK)],
                  base_y=860, top_y=300, bw=320, gap=440, vmax=100, seed=210, nsize=150)
    d = ImageDraw.Draw(im); d.line([(300, 860), (1620, 860)], fill=GREY, width=4)
    yy = 860 - (860 - 300); xx = 300
    while xx < 1620: d.line([(xx, yy), (min(xx + 20, 1620), yy)], fill=FADE, width=3); xx += 40
    T(d, (1630, yy), '100%', 36, GREY, F_M, 'lm')
    source(d, '주공13 3.80억 ÷ 13.85억 · 래미안자이 7.00억 ÷ 13.40억 · 신규 전세·1년 매매 가운데 값')

@board
def trap_renew(im):
    """youtube-loop 대본 줄 확인 ⑥."""
    d = ImageDraw.Draw(im)
    T(d, (W // 2, 300), '신규 전세와 갱신 전세,', 120, INK, F_X)
    T(d, (W // 2, 470), '섞지 마세요', 150, OR, F_X); hand_under(d, 560, 1360, 560, seed=221)
    T(d, (W // 2, 720), '새로 맺은 계약만 보기 · 갱신엔 옛날 값이 남음', 58, INK, F_B)
    source(d, '국토교통부 전월세 실거래 \'계약 구분\' 신규/갱신')

def _stamp(d, cx, cy, s, r=150, seed=1):
    hand_ellipse(d, (cx - r, cy - r * 0.62, cx + r, cy + r * 0.62), (200, 40, 30), 7, seed=seed)
    TF(d, (cx, cy), s, 46, (200, 40, 30), F_X, maxw=r * 1.7)

@board
def reg_map(im):
    d = ImageDraw.Draw(im); feats = [f for f in _geo('muni_capital.json') if f['properties']['code'][:2] == '11' or f['properties']['code'] == '31060']
    others = [f for f in _geo('muni_capital.json') if f['properties']['code'] in ('31050', '31100', '31090', '31040', '31010', '31110', '31020')]
    P = _proj(feats, (120, 180, 1060, 1000))
    for f in others:
        for r in _rings(f):
            pts = [P(x, y) for x, y in r]; d.line(pts + [pts[0]], fill=(200, 192, 180), width=2)
    for f in feats:
        gm = f['properties']['code'] == '31060'
        for r in _rings(f):
            pts = [P(x, y) for x, y in r]; d.polygon(pts, fill=(246, 206, 176) if gm else (226, 206, 180)); d.line(pts + [pts[0]], fill=(150, 130, 110), width=2)
        if gm:
            xs = [P(x, y) for r in _rings(f) for x, y in r]; cx = sum(p[0] for p in xs) / len(xs); cy = sum(p[1] for p in xs) / len(xs)
            T(d, (cx - 20, cy + 10), '광명', 54, OR, F_X)
    T(d, (560, 560), '서울', 80, INK, F_X)
    TF(d, (1430, 220), '서울과 같은 규제', 134, INK, F_X, maxw=900)
    for i, s in enumerate(('조정대상지역', '투기과열지구', '토지거래허가구역')):
        _stamp(d, 1440, 420 + i * 200, s, 170, seed=230 + i)
    K.source(d, '관계부처 합동 주택시장 안정화 대책(2025-10-15) · 국토교통부공고 제2025-1219호 · 경계 통계청 2013')

@board
def loan6(im):
    d = ImageDraw.Draw(im)
    T(d, (W // 2, 300), '15억 이하 집', 120, INK, F_X)
    T(d, (W // 2, 470), '주택담보대출 한도', 90, INK, F_B)
    T(d, (W // 2, 680), '6억', 230, OR, F_X); hand_ellipse(d, (W // 2 - 230, 560, W // 2 + 230, 800), seed=241)
    T(d, (W // 2, 900), '"수도권·규제지역의 시가 15억 원 이하 주택의 주담대 한도는 현행과 동일한 6억 원"', 38, GREY, F_M)
    source(d, '관계부처 합동 주택시장 안정화 대책 · korea.kr 2025-10-15')

@board
def cal1231(im):
    d = ImageDraw.Draw(im)
    T(d, (W // 2, 230), '토지거래허가구역', 110, INK, F_X)
    T(d, (W // 2, 430), '2025. 10. 20. 부터', 80, INK, F_B); T(d, (W // 2, 600), '2026. 12. 31.', 160, OR, F_X)
    hand_under(d, 470, 1450, 700, seed=251)
    T(d, (W // 2, 780), '허가 대상 = 매매 계약 · 전세 계약은 아님', 60, INK, F_B)
    source(d, '국토교통부공고 제2025-1219호 지정기간 · 경기도 토지거래허가구역 지정현황')

@board
def steps3(im):
    d = ImageDraw.Draw(im); T(d, (W // 2, 140), '사기 전 순서', 140, INK, F_X)
    steps = (('같은 동·크기', '1년 값 확인'), ('계약 전', '토지거래허가 신청'), ('계약 전', '대출 한도 은행 확인'))
    for i, (a, b) in enumerate(steps):
        y = 380 + i * 200
        s2 = a + ' ' + b; T(d, (360, y), str(i + 1), 120, OR if i == 1 else INK, F_X); T(d, (470, y), s2, 80, OR if i == 1 else INK, F_X, 'lm')
    hand_under(d, 470, 470 + font(F_X, 80).getlength('계약 전 토지거래허가 신청'), 380 + 200 + 60, seed=261)
    source(d, '허가 뒤 이용 의무 등 세부 조건은 관할 시청 확인')

@board
def summary4(im):
    d = ImageDraw.Draw(im); T(d, (W // 2, 130), '한 장 정리', 130, INK, F_X)
    rows = (('광명 전체', '26곳 중 18번째 · 9억 7천'), ('2019년 뒤 새 단지', '14억 7천'), ('철산동 사다리', '16억 ~ 6억'), ('새 단지 전세', '8억 7천'))
    for i, (a, b) in enumerate(rows):
        y = 330 + i * 165
        T(d, (840, y), a, 62, GREY, F_B, 'rm'); T(d, (900, y), b, 84, OR if i == 0 else INK, F_X, 'lm')
        if i < 3: d.line([(260, y + 82), (1700, y + 82)], fill=(206, 198, 186), width=2)
    hand_check(d, 200, 330, 56)
    source(d, SRC_RT + ' · 전세는 신규 계약')

def main(names):
    os.makedirs(OUT, exist_ok=True)
    for n in names or list(B):
        im = canvas(); B[n](im); im.save(os.path.join(OUT, n + '.png')); print(n)

if __name__ == '__main__':
    main(sys.argv[1:])
