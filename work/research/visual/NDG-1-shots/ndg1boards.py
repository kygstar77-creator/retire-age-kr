"""NDG-1 장면 판 — visual-designer 2026-11-27. H-6 판(h6boards)과 같은 꼴·같은 부품(k1boards):
구겨진 종이 바탕 · 펜 빗금 막대(hatch_bar) · 주황 #FF5A00은 그 화면의 답 하나 · 손 동그라미·밑줄 · 상자·카드 판 없음(쪽지는 기울인 종이).
숫자는 ep/NDG-1 calc_out_1122.txt·calc3_out_1123.txt·calc_seoul_out_1124.txt와 script.md v1.7 [자막]·(화면) 줄 값만.
calc 출력 파일을 그대로 읽고 assert(옮겨 적지 않음). 보도·법 글은 script.md와 글자 그대로 대조.
판은 '답이 열린 마지막 모습' — '?' → 열림은 PD가 Remotion에서. 파일 이름은 shot_plan.md 장면 계획 '파일' 칸 그대로.
seoul3(구 지도)는 공개 경계 자료 라이선스 확인 뒤 따로(이 파일에 없음).
사용: py -3.12 ndg1boards.py [이름 ...]   (없으면 전부) → work/video/public/bg/ndg1/board/<이름>.png
"""
import os, sys, re, ast
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'K-1-shots'))
from k1boards import (W, H, INK, GREY, OR, FADE, F_B, F_M, F_X, font, canvas, T, TF, source, obj,
                      hand_ellipse, hand_under, hand_check, hand_arrow, hatch_bar)
from PIL import Image, ImageDraw, ImageFilter

sys.stdout.reconfigure(encoding='utf-8')
WORK = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'NDG-1')
OUT = os.path.join(WORK, 'video', 'public', 'bg', 'ndg1', 'board')
LINE = (206, 198, 186)
BLUE = (36, 74, 140)          # 80% 밑 묶음 — shot_plan '짙은 파랑'(주황 짝)
rd = lambda fn: open(os.path.join(EP, fn), encoding='utf-8').read()
SRC_RT = '국토교통부 아파트 매매 실거래 · 노원·도봉·강북 · 2026-11-22 받음 · 해제·공공기관 매수 뺌'

# ── calc 출력에서 그대로 읽기 ─────────────────────────────────────────
_c1, _c3, _cs, _sc = rd('calc_out_1122.txt'), rd('calc3_out_1123.txt'), rd('calc_seoul_out_1124.txt'), rd('script.md')
MON = {m: (int(a), int(b), int(c), int(s)) for m, a, b, c, s in
       re.findall(r'(\d{6}) 노원구 (\d+) · 도봉구 (\d+) · 강북구 (\d+) · 합 (\d+)', _c1)}
M = {m: v[3] for m, v in MON.items()}
YEAR = ast.literal_eval(re.search(r"연도 합 (\{.*\})", _c1).group(1))
assert len(M) == 71 and sum(M.values()) == 38022 and '38022건' in _c1
assert YEAR == {'2021': 6588, '2022': 1469, '2023': 4467, '2024': 6348, '2025': 8355, '2026': 10795}
Y26_10 = sum(v for m, v in M.items() if '202601' <= m <= '202610'); assert Y26_10 == 10574
assert M['202604'] == 1612 and (M['202608'], M['202609'], M['202610']) == (824, 709, 803)
AUT = (M['202608'] + M['202609'] + M['202610']) / 3; assert round(AUT) == 779 and round(100 * AUT / M['202604'], 1) == 48.3
assert (M['202101'], M['202112'], min(v for m, v in M.items() if m[:4] == '2022'), M['202209']) == (969, 107, 69, 69)
assert (M['202407'], M['202506'], M['202611']) == (1074, 1243, 221)
GRP = re.search(r'묶음 (\d+)개 · 지금/2021최고 가운데 ([\d.]+)% · 넘은 묶음 (\d+)개 · 80% 밑 (\d+)개', _c1).groups()
assert GRP == ('441', '90.0', '78', '68')
GU = {g: (int(n), float(p)) for g, n, p in re.findall(r'  (\S+구): 묶음 (\d+) · 가운데 ([\d.]+)%', _c1)}
assert GU == {'노원구': (277, 91.6), '도봉구': (120, 85.0), '강북구': (44, 92.5)}
CARD = {}
for gu, nm, a, v0, v1, n, p in re.findall(r'  (\S+구) (.+?) (\d+)㎡ · 2021 최고 ([\d.]+) · 2026-07~11 중앙 ([\d.]+)\((\d+)건\) · ([\d.]+)%', _c1):
    CARD[nm.split(' ', 1)[1] + f' {a}'] = (gu, nm.split(' ', 1)[0], int(a), float(v0), float(v1), int(n), float(p))
assert CARD['미성 50'][3:] == (8.75, 9.90, 22, 113.1) and CARD['주공2 45'][3:] == (5.83, 3.87, 39, 66.4)
assert CARD['태강아파트(아이파크) 50'][3:] == (6.50, 6.48, 32, 99.8) and CARD['주공17단지 36'][3:] == (5.99, 3.90, 33, 65.1)
NEW = re.search(r'신고가 묶음 (\d+)개 \(2026년 거래가 있는 묶음 (\d+)개 중\)', _c1).groups(); assert NEW == ('350', '1103')
NEWGU = dict(re.findall(r'  (\S+구): (\d+)개', _c1)); assert NEWGU == {'노원구': '206', '도봉구': '77', '강북구': '67'}
TOP = re.findall(r'  (\S+구) (\S+) (.+?) (\d+)㎡ · 이전 최고 ([\d.]+) → 2026 ([\d.]+) \((\d+)건, 처음 (\d{6})\)', _c1)
TOP9 = TOP[:9]; assert len(TOP) == 12 and all(t[1] == '월계동' for t in TOP9) and TOP[9][1] != '월계동'
assert TOP9[1][2:7] == ('한진한화그랑빌', '85', '10.50', '12.50', '36')
FIRST = ast.literal_eval(re.search(r"처음 넘은 달 (\{.*\})", _c1).group(1))
assert sum(FIRST.values()) == 350 and max(FIRST, key=FIRST.get) == '202610' and FIRST['202610'] == 50 and FIRST['202611'] == 16
DONG = ast.literal_eval(re.search(r'동별 상위 (\[.*\])', _c3).group(1))
assert DONG == [('공릉동', 58), ('창동', 51), ('상계동', 48), ('월계동', 42), ('미아동', 36), ('중계동', 31)]
WG = tuple(int(x) for x in re.search(r'월계동 2026 거래 묶음 (\d+) · 그중 신고가 (\d+)', _c3).groups()); assert WG == (96, 42)
MAX = {g: ast.literal_eval(re.search(g + r' 2026 최고 (\[.*?\]) · 20억↑ 0', _c3).group(1))[0] for g in ('노원구', '도봉구', '강북구')}
assert [MAX[g][4] for g in ('노원구', '도봉구', '강북구')] == [18.5, 14.0, 14.4]
assert '서울 전체: 꼭대기 대비 가운데 104.0%' in _cs
for s in ('38,022건', '1,612건', '48.3%', '10,574건', '1,469건', '709건', '441묶음', '가운데 90.0%', '104.0%', '350 / 2026년 거래가 있는 묶음 1,103(32%)',
          '96 중 신고가 42(44%)', '10.50억 → 2026 최고 12.50억', '광운대역 물류부지', '15년 만에 착공', '156,491㎡', '내 손안에 서울 2024-10-25',
          'HDC현대산업개발 본사 이전', '2028년 하반기 전체 시설 준공', '목표 — 확정 아님', '30일 이내 신고', '20억 이상 0건', 'rt.molit.go.kr'):
    assert s in _sc, s

def eok(v):      # 8.75 → '8억 7,500만'
    e, m = divmod(round(v * 10000), 10000); return f'{e}억 {m:,}만' if m else f'{e}억'

B = {}
def board(fn):
    B[fn.__name__] = fn; return fn

def slip(im, x0, y0, w, h, rot, paint, color=(246, 239, 220)):
    """기울여 붙인 종이 쪽지 한 장(H-6 slip 꼴) — paint(cd, w, h)로 글을 쓴다."""
    card = Image.new('RGBA', (w, h), (0, 0, 0, 0)); cd = ImageDraw.Draw(card); cd.rectangle((0, 0, w, h), fill=color); paint(cd, w, h)
    card = card.rotate(rot, expand=True, resample=Image.BICUBIC)
    sh = Image.new('L', card.size, 0); sh.paste(card.split()[3].point(lambda v: 70 if v else 0)); sh = sh.filter(ImageFilter.GaussianBlur(8))
    im.paste((150, 146, 140), (x0 + 8, y0 + 10), sh); im.paste(card, (x0, y0), card)

def dashed_h(d, x0, x1, y, color=GREY, w=4, seg=22):
    x = x0
    while x < x1: d.line([(x, y), (min(x + seg, x1), y)], fill=color, width=w); x += seg * 1.8

def mbars(im, rows, color_of, top_lab, box=(170, 300, 1750, 860), vmax=None, seed=10, lab_size=38, year_row=True):
    """월별 막대 — rows [(yyyymm, v)], color_of(m) → (색, 빗금 흐림 여부), top_lab(m) → 위 숫자 글자 크기(0 = 안 씀)."""
    d = ImageDraw.Draw(im); x0, top, x1, base = box; n = len(rows); slot = (x1 - x0) / n; bw = slot * 0.64
    vmax = vmax or max(v for _, v in rows)
    for i, (m, v) in enumerate(rows):
        x = x0 + i * slot + (slot - bw) / 2; yt = base - (base - top) * v / vmax; c, faint = color_of(m)
        hatch_bar(im, (x, yt, x + bw, base), FADE if faint else c, seed=seed + i, step=16 if faint else 11, width=4 if faint else 5); d = ImageDraw.Draw(im)
        s = top_lab(m)
        if s: T(d, (x + bw / 2, yt - s * 0.55), f'{v:,}', s, GREY if faint else c, F_X if s >= 50 else F_B)
        if lab_size: T(d, (x + bw / 2, base + 40), f'{int(m[4:])}월', lab_size, INK, F_B)
        if year_row and (m[4:] == '01' or i == 0): T(d, (x + bw / 2, base + 86), m[:4], 32, GREY, F_B)
    d.line([(x0 - 10, base), (x1 + 10, base)], fill=GREY, width=4)
    X = lambda i: x0 + i * slot + slot / 2; Y = lambda v: base - (base - top) * v / vmax
    return d, X, Y

def rng(a, b): return [(m, M[m]) for m in sorted(M) if a <= m <= b]

# ── 0. 여는 질문 ─────────────────────────────────────────────────────
@board
def claims(im):            # 쪽지 둘 — 정반대 이야기, 가운데 '?'
    for i, (k, a) in enumerate((('주장 A', '거래 끊기고\n값 뚝뚝'), ('주장 B', '노원에\n신고가'))):
        def paint(cd, w, h, k=k, a=a):
            T(cd, (w // 2, 90), k, 56, GREY, F_B)
            for j, ln in enumerate(a.split('\n')): T(cd, (w // 2, 250 + j * 130), ln, 104, INK, F_X)
        slip(im, (150, 1100)[i], (220, 260)[i], 660, 560, (-3.0, 2.4)[i], paint)
    d = ImageDraw.Draw(im); T(d, (W // 2, 560), '?', 300, OR, F_X)

@board
def question(im):          # 이 편이 세는 두 가지
    d = ImageDraw.Draw(im)
    TF(d, (W // 2, 380), '거래는 정말 끊겼나', 150, INK, F_X)
    TF(d, (W // 2, 600), '신고가는 몇 곳, 어디', 150, OR, F_X)
    hand_under(d, 470, 1450, 700, seed=7)
    T(d, (W // 2, 860), '국토교통부 매매 실거래 신고분 · 호가·매물 아님', 56, GREY, F_B)

# ── 1. 노도강은 어떤 곳 ─────────────────────────────────────────────
@board
def count(im):             # 센 범위 + 38,022건
    d = ImageDraw.Draw(im)
    def paint(cd, w, h):
        for j, ln in enumerate(('아파트 매매만', '2021년 1월 ~ 2026년 11월', '해제된 거래 · 공공기관 매수 뺌')):
            T(cd, (w // 2, 90 + j * 100), ln, 58 if j else 70, INK, F_X if j == 0 else F_B)
    slip(im, 170, 330, 780, 400, -2.2, paint)
    d = ImageDraw.Draw(im)
    T(d, (1420, 470), f'{sum(M.values()):,}건', 190, OR, F_X)
    T(d, (1420, 640), '노원 · 도봉 · 강북', 64, INK, F_B)
    hand_under(d, 1080, 1760, 560, seed=13)
    source(d, SRC_RT + ' · 계약 2021-01~2026-11')

@board
def claims2(im):           # 두 주장이 든 근거 — 근거 줄만 크게(11/27 심사 못함: 6줄)
    for i, (k, b) in enumerate((('거래가 끊겼다는 쪽', '가을 거래량이\n봄보다 크게 줄었다'), ('신고가라는 쪽', '노원 단지에서\n신고가 거래'))):
        def paint(cd, w, h, k=k, b=b):
            T(cd, (w // 2, 80), k, 52, GREY, F_B)
            for j, ln in enumerate(b.split('\n')): T(cd, (w // 2, 220 + j * 110), ln, 80, INK, F_X)
        slip(im, (130, 1040)[i], (250, 280)[i], 740, 460, (-2.2, 1.8)[i], paint)
    d = ImageDraw.Draw(im); T(d, (W // 2, 930), '근거부터 달랐다', 80, OR, F_X)

# ── 2. 거래는 정말 끊겼나 ───────────────────────────────────────────
@board
def m2026(im):             # 2026년 1~10월 — 4월 1,612 · 가을 석 달 평균 779(절반)
    d = ImageDraw.Draw(im); TF(d, (W // 2, 100), '2026년 · 달마다 몇 건 팔렸나', 92, INK, F_X)
    rows = rng('202601', '202610')
    d, X, Y = mbars(im, rows, lambda m: (GREY, True) if m in ('202608', '202609', '202610') else (INK, False),
                    lambda m: 72 if m == '202604' else (0 if m in ('202608', '202609', '202610') else 40), vmax=1700, seed=20, year_row=False)
    T(d, (X(3), Y(1612) - 110), '4월', 52, INK, F_B)
    yb = Y(AUT); dashed_h(d, X(7) - 60, X(9) + 60, yb, OR, 6)
    ya = Y(1480)
    T(d, (X(8), ya - 40), '석 달 평균 779건', 60, OR, F_X)
    T(d, (X(8), ya + 30), '4월의 절반', 60, OR, F_X)
    hand_ellipse(d, (X(7) - 95, ya - 95, X(9) + 95, ya + 85), seed=21)
    hand_arrow(d, (X(8), ya + 90), (X(8), yb - 70), OR, 6)
    source(d, SRC_RT + ' · 8월 824 · 9월 709 · 10월 803 · 평균은 4월의 48.3% · 막대는 0건부터')

@board
def years(im):             # 해마다 — 2026년 1~10월 10,574 > 2021년 6,588
    d = ImageDraw.Draw(im); TF(d, (W // 2, 100), '해마다 몇 건 팔렸나', 100, INK, F_X)
    rows = [(y, YEAR[y]) for y in ('2021', '2022', '2023', '2024', '2025')] + [('2026', Y26_10)]
    x0, x1, base, top = 200, 1720, 850, 290; slot = (x1 - x0) / 6; bw = slot * 0.6; vmax = 11000
    for i, (y, v) in enumerate(rows):
        x = x0 + i * slot + (slot - bw) / 2; yt = base - (base - top) * v / vmax; c = OR if y == '2026' else INK
        hatch_bar(im, (x, yt, x + bw, base), c, seed=30 + i, step=12, width=5); d = ImageDraw.Draw(im)
        T(d, (x + bw / 2, yt - 50), f'{v:,}', 84 if y == '2026' else 60, c, F_X)
        T(d, (x + bw / 2, base + 50), f'{y}년', 50, INK, F_B)
        if y == '2026': T(d, (x + bw / 2, base + 105), '1~10월', 42, OR, F_B)
    d.line([(x0 - 10, base), (x1 + 10, base)], fill=GREY, width=4)
    source(d, SRC_RT + ' · 2026년은 두 달 남기고 · 막대는 0건부터')

@board
def y2021(im):             # 2021~2022 월별 — 969 → 107, 2022년 바닥
    d = ImageDraw.Draw(im); TF(d, (W // 2, 100), '2021년부터 이미 줄었다', 100, INK, F_X)
    rows = rng('202101', '202212')
    d, X, Y = mbars(im, rows, lambda m: (OR, False) if m == '202112' else ((GREY, False) if m[:4] == '2022' else (INK, False)),
                    lambda m: 60 if m == '202101' else 0, vmax=1000, seed=40, lab_size=0, year_row=False)
    T(d, (X(11), Y(650)), '107', 80, OR, F_X); hand_arrow(d, (X(11), Y(650) + 50), (X(11), Y(107) - 20), OR, 6)
    T(d, (X(5.5), 920), '2021년', 52, INK, F_B); T(d, (X(17.5), 920), '2022년', 52, INK, F_B)
    d.line([(X(11.5), 880), (X(11.5), 950)], fill=GREY, width=3)
    T(d, (X(17.5), Y(400)), '2022년 1년 합계 1,469건', 64, INK, F_X)
    source(d, SRC_RT + ' · 2021-01 969건 → 2021-12 107건 · 2022년 월 최저 69건(9월) · 막대는 0건부터')

@board
def vs(im):                # 2022년 한 해 vs 2026년 9월 한 달
    d = ImageDraw.Draw(im); TF(d, (W // 2, 110), '2022년 한 해 vs 2026년 9월 한 달', 90, INK, F_X)
    r = M['202609'] / YEAR['2022']; assert round(100 * r) == 48
    base, top, vmax, bw = 860, 300, 1500, 360
    for i, (lab, v, c) in enumerate((('2022년 한 해', YEAR['2022'], INK), ('2026년 9월 한 달', M['202609'], OR))):
        x = 480 + i * 600; yt = base - (base - top) * v / vmax
        hatch_bar(im, (x, yt, x + bw, base), c, seed=50 + i, step=12, width=5); d = ImageDraw.Draw(im)
        T(d, (x + bw / 2, yt - 64), f'{v:,}건', 96, c, F_X)
        T(d, (x + bw / 2, base + 55), lab, 54, INK, F_B)
    d.line([(380, base), (1540, base)], fill=GREY, width=4)
    T(d, (1600, 520), '절반쯤', 84, INK, F_X, 'lm')
    source(d, SRC_RT + ' · 709 ÷ 1,469 = 48% · 막대는 0건부터')

@board
def peaks(im):             # 2024-01~2026-10 — 봉우리 셋
    d = ImageDraw.Draw(im); TF(d, (W // 2, 100), '해마다 한 번 몰렸다', 100, INK, F_X)
    PK = ('202407', '202506', '202604')
    assert all(M[p] == max(v for m, v in M.items() if m[:4] == p[:4] and m <= '202610') for p in PK)
    rows = rng('202401', '202610')
    d, X, Y = mbars(im, rows, lambda m: (OR, False) if m in PK else (INK, False), lambda m: 60 if m in PK else 0,
                    vmax=1700, seed=60, lab_size=0, year_row=False)
    for i, (m, _) in enumerate(rows):
        if m[4:] in ('01', '07'): T(d, (X(i), 910), f'{m[:4]}.{int(m[4:])}', 34, GREY, F_B)
    source(d, SRC_RT + ' · 봉우리 2024-07 1,074 · 2025-06 1,243 · 2026-04 1,612 · 막대는 0건부터')

@board
def lag(im):               # 30일 안 신고 — 11월은 덜 들어옴
    d = ImageDraw.Draw(im); TF(d, (W // 2, 100), '이번 달 숫자는 더 늘어나요', 96, INK, F_X)
    rows = rng('202607', '202611')
    d, X, Y = mbars(im, rows, lambda m: (GREY, True) if m == '202611' else (INK, False), lambda m: 60,
                    box=(360, 320, 1560, 840), vmax=1300, seed=70, lab_size=44, year_row=False)
    T(d, (X(4) - 40, Y(1150)), '아직 덜 들어옴', 56, OR, F_X)
    hand_arrow(d, (X(4), Y(1150) + 40), (X(4), Y(221) - 60), OR, 6)
    T(d, (W // 2, 960), '계약하고 30일 안에 신고', 64, INK, F_B)
    source(d, '부동산 거래신고법 제3조 — 계약 체결일부터 30일 이내 · 2026-11 221건은 11/22까지 들어온 신고')

# ── 3. 2021년 꼭대기의 몇 % ─────────────────────────────────────────
@board
def method(im):            # 비교 방법 — 실제 묶음 하나로(11/27 심사 못함: 숫자 없는 카드)
    d = ImageDraw.Draw(im); TF(d, (W // 2, 100), '같은 단지 · 같은 면적끼리', 100, INK, F_X)
    gu, dn, a, v0, v1, n, p = CARD['미성 50']
    T(d, (W // 2, 220), f'예) {dn} 미성 {a}㎡', 56, GREY, F_B)
    T(d, (540, 400), '2021년 가장 비싼 거래', 56, INK, F_B); T(d, (540, 530), eok(v0), 110, INK, F_X)
    T(d, (1380, 400), '2026년 7~11월 가운데 값', 56, INK, F_B); T(d, (1380, 530), eok(v1), 110, INK, F_X)
    T(d, (W // 2, 530), 'vs', 80, GREY, F_X)
    T(d, (W // 2, 740), f'{float(p):.0f}%', 170, OR, F_X); T(d, (W // 2, 895), '2021년 최고보다 요즘 값이 높다', 60, INK, F_B)
    hand_under(d, 760, 1160, 832, seed=17)
    T(d, (W // 2, 975), f'요즘 3건 넘게 팔린 묶음 {GRP[0]}곳을 모두 이렇게 비교', 44, GREY, F_B)
    source(d, SRC_RT + ' · 2026-07~11 거래 3건 이상 · 가운데 값 = 값 순서로 줄 세웠을 때 한가운데')

def _cards(im, keys, title):
    d = ImageDraw.Draw(im); TF(d, (W // 2, 100), title, 92, INK, F_X)
    for i, k in enumerate(keys):
        gu, dong, a, v0, v1, n, p = CARD[k]; nm = k.rsplit(' ', 1)[0].replace('아파트(아이파크)', '아파트').replace('주공', '주공')
        c = OR if p >= 99.5 or p > 100 else BLUE
        def paint(cd, w, h, gu=gu, dong=dong, nm=nm, a=a, v0=v0, v1=v1, n=n, p=p, c=c):
            T(cd, (w // 2, 70), f'{gu} {dong}', 48, GREY, F_B)
            TF(cd, (w // 2, 160), f'{nm} {a}㎡', 70, INK, F_X, maxw=w - 60)
            T(cd, (60, 290), '2021 최고', 46, GREY, F_B, 'lm'); T(cd, (w - 60, 290), eok(v0), 58, INK, F_X, 'rm')
            T(cd, (60, 390), '요즘 가운데', 46, GREY, F_B, 'lm'); T(cd, (w - 60, 390), eok(v1), 58, INK, F_X, 'rm')
            cd.line([(60, 450), (w - 60, 450)], fill=LINE, width=3)
            T(cd, (w // 2, 530), f'{p:.1f}%' if abs(p - 100) < 1 else f'{round(p)}%', 120, c, F_X); T(cd, (w // 2, 610), f'2021 최고 대비 · 요즘 거래 {n}건', 36, GREY, F_B)
        slip(im, (150, 1030)[i], (200, 230)[i], 740, 670, (-2.4, 2.0)[i], paint)
    return ImageDraw.Draw(im)

@board
def cards_a(im):           # 같은 노원 — 월계동 미성 113% vs 중계동 주공2 66%
    d = _cards(im, ('미성 50', '주공2 45'), '같은 노원구 안에서도')
    source(d, SRC_RT + ' · 2021년 최고 한 건 vs 2026-07~11 가운데 값')

@board
def cards_b(im):           # 공릉동 태강 100% vs 창동 주공17 65%
    d = _cards(im, ('태강아파트(아이파크) 50', '주공17단지 36'), '거래 서른 건 넘게 쌓인 두 곳')
    source(d, '국토교통부 실거래 · 2026-11-22 받음 · 태강아파트(아이파크) · 2021년 최고 vs 2026-07~11 가운데')

# ── 4. 신고가 350곳은 어디 ──────────────────────────────────────────
@board
def defn(im): pass   # 자리만 — 'def'는 파이썬 낱말이라 아래에서 이름 바꿔 등록
del B['defn']
def _def(im):              # 신고가 정의 — 부등호 하나 크게
    d = ImageDraw.Draw(im); T(d, (W // 2, 130), '신고가는 이렇게 셌어요', 92, INK, F_X)
    T(d, (W // 2, 250), '2026년 팔린 값  >  2021~2025년 그 묶음의 가장 비싼 값', 56, INK, F_B)
    g = TOP9[1]; T(d, (W // 2, 420), f'예) {g[1]} {g[2]} {g[3]}㎡', 60, GREY, F_B)
    T(d, (480, 560), '2026년', 60, INK, F_B); T(d, (480, 680), eok(float(g[5])), 110, INK, F_X)
    T(d, (W // 2, 640), '>', 220, OR, F_X)
    T(d, (1440, 560), '2021~2025년 최고', 60, INK, F_B); T(d, (1440, 680), eok(float(g[4])), 110, INK, F_X)
    T(d, (W // 2, 900), '같은 단지 · 같은 면적', 64, GREY, F_B)
    source(d, SRC_RT)
B['def'] = _def

@board
def n350(im):              # 350곳 / 1,103곳
    d = ImageDraw.Draw(im); T(d, (W // 2, 150), '2026년 신고가가 나온 묶음', 80, INK, F_X)
    T(d, (W // 2, 460), f'{NEW[0]}곳', 300, OR, F_X)
    hand_ellipse(d, (470, 270, 1450, 650), seed=81)
    T(d, (W // 2, 720), f'2026년 거래가 있는 묶음 {int(NEW[1]):,}곳 중 · 셋 중 하나', 60, INK, F_B)
    T(d, (W // 2, 840), f"노원 {NEWGU['노원구']} · 도봉 {NEWGU['도봉구']} · 강북 {NEWGU['강북구']}", 72, INK, F_X)
    source(d, SRC_RT + ' · 350 ÷ 1,103 = 32%')

@board
def dong(im):              # 동별 신고가 묶음 — 공릉동 맨 위, 월계동 밑줄
    d = ImageDraw.Draw(im); TF(d, (W // 2, 100), '동네별 신고가 묶음', 100, INK, F_X)
    x0, xmax, vmax = 520, 1560, 60
    for i, (dn, n) in enumerate(DONG):
        y = 250 + i * 120; x1 = x0 + (xmax - x0) * n / vmax; c = OR if dn == '월계동' else INK
        T(d, (x0 - 30, y + 40), dn, 64, c, F_X, 'rm')
        hatch_bar(im, (x0, y, x1, y + 80), INK, seed=90 + i, step=12, width=5); d = ImageDraw.Draw(im)
        T(d, (x1 + 30, y + 40), f'{n}곳', 64, c, F_X, 'lm')
        if dn == '월계동': hand_under(d, x0 - 260, x0 - 20, y + 95, seed=91)
    d.line([(x0, 230), (x0, 980)], fill=GREY, width=4)
    source(d, SRC_RT + ' · 신고가 묶음 350곳 중 많은 동 여섯 · 막대는 0곳부터')

@board
def wolgye(im):            # 월계동 96묶음 중 42 — 바둑판
    d = ImageDraw.Draw(im); TF(d, (W // 2, 100), '월계동은 절반 가까이', 100, INK, F_X)
    n, k = WG; cols = 16; r = 30; gx, gy = 96, 120; x0 = 170; y0 = 300
    for i in range(n):
        cx, cy = x0 + (i % cols) * gx * 0.62, y0 + (i // cols) * gy
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=OR if i < k else (186, 178, 166))
    T(d, (1520, 470), f'{k}곳', 170, OR, F_X)
    T(d, (1520, 620), f'{n}곳 중 · {round(100 * k / n)}%', 64, INK, F_X)
    T(d, (1520, 760), '노도강 전체는 32%', 52, GREY, F_B)
    source(d, SRC_RT + ' · 점 하나 = 2026년 거래가 있는 월계동 묶음 하나 · 주황 = 신고가')

@board
def top9(im):              # 신고가 거래 많은 묶음 아홉 — 모두 월계동(11/27 심사 못함: 동 칸·타원 → 제목으로)
    d = ImageDraw.Draw(im); T(d, (W // 2, 80), '신고가 거래가 많은 아홉 묶음', 76, INK, F_X); T(d, (W // 2, 170), '아홉 곳 모두 월계동', 84, OR, F_X)
    y0, rh = 300, 130
    T(d, (200, y0), '단지 · 면적', 44, GREY, F_B, 'lm'); T(d, (1500, y0), '그전 최고 → 2026 최고', 44, GREY, F_B, 'rm'); T(d, (1720, y0), '넘은 거래', 44, GREY, F_B, 'rm')
    for i, (gu, dn, nm, a, v0, v1, n, _) in enumerate(TOP9[:4]):
        y = y0 + 110 + i * rh
        T(d, (200, y), f'{nm} {a}㎡', 54, INK, F_X, 'lm')
        T(d, (1500, y), f'{eok(float(v0))} → {eok(float(v1))}', 54, INK, F_X, 'rm')
        T(d, (1720, y), f'{n}건', 60, INK, F_X, 'rm')
        d.line([(180, y + rh / 2), (1740, y + rh / 2)], fill=LINE, width=2)
    T(d, (W // 2, y0 + 110 + 4 * rh), f'외 {len(TOP9) - 4}곳 — 역시 모두 월계동', 56, GREY, F_B)
    source(d, SRC_RT + ' · 10위 공릉동 태강 59㎡·미아동 삼성래미안트리베라2단지 59㎡ 각 17건')

@board
def firstmonth(im):        # 처음 넘은 달 — 10월 50곳
    d = ImageDraw.Draw(im); TF(d, (W // 2, 100), '처음 그전 최고값을 넘은 달', 92, INK, F_X)
    rows = sorted(FIRST.items())
    d, X, Y = mbars(im, rows, lambda m: (GREY, True) if m == '202611' else ((OR, False) if m == '202610' else (INK, False)),
                    lambda m: 84 if m == '202610' else 44, vmax=56, seed=110, year_row=False)
    source(d, SRC_RT + ' · 2026년 신고가 묶음 350곳 · 11월은 신고 기한 안 · 막대는 0곳부터')

# ── 5. 월계동에서 무슨 일이 ─────────────────────────────────────────
@board
def seoulpr(im):           # 서울시 발표 인용
    d = ImageDraw.Draw(im); T(d, (W // 2, 140), '서울시 발표', 64, GREY, F_B)
    TF(d, (W // 2, 330), '광운대역 물류부지', 140, INK, F_X)
    TF(d, (W // 2, 560), '15년 만에 착공', 170, OR, F_X)
    hand_under(d, 560, 1360, 670, seed=121)
    T(d, (W // 2, 820), '노원구 월계동 156,491㎡', 76, INK, F_X)
    source(d, "서울시 '광운대역 물류부지 개발 첫 삽…동북권역 新 경제거점 발돋움' · 내 손안에 서울 2024-10-25")

@board
def target(im):            # 본사 이전 추진 · 2028년 하반기 목표 — 확정 아님
    d = ImageDraw.Draw(im); T(d, (W // 2, 140), '같은 발표에 있던 말', 64, GREY, F_B)
    TF(d, (W // 2, 360), 'HDC현대산업개발 본사 이전 추진', 104, INK, F_X)
    TF(d, (W // 2, 540), '2028년 하반기 전체 시설 준공 목표', 104, INK, F_X)
    T(d, (W // 2, 780), '목표 — 확정 아님', 120, OR, F_X)
    hand_under(d, 520, 1400, 870, seed=131)
    source(d, "서울시 내 손안에 서울 2024-10-25 · '본사 이전이 추진' · '2028년 하반기 전체 시설 준공을 목표'")

@board
def max3(im):              # 구별 2026년 가장 비싼 거래 — 20억 넘는 거래 0건
    d = ImageDraw.Draw(im); TF(d, (W // 2, 100), '2026년 가장 비싸게 팔린 한 건', 92, INK, F_X)
    base, top, vmax, bw = 840, 300, 22, 300; Y = lambda v: base - (base - top) * v / vmax
    for i, g in enumerate(('노원구', '도봉구', '강북구')):
        dn, nm, a, ym, v = MAX[g]; x = 330 + i * 470
        hatch_bar(im, (x, Y(v), x + bw, base), INK, seed=140 + i, step=12, width=5); d = ImageDraw.Draw(im)
        T(d, (x + bw / 2, base + 50), f'{g[:2]} · {eok(v)}', 56, INK, F_X)
        T(d, (x + bw / 2, base + 108), f'{dn} {nm} {a}㎡', 30, GREY, F_B)
    dashed_h(d, 260, 1700, Y(20), OR, 6)
    T(d, (1720, Y(20)), '20억', 52, OR, F_X, 'lm')
    T(d, (W // 2, 215), '20억 넘는 거래 0건', 96, OR, F_X)
    d.line([(260, base), (1700, base)], fill=GREY, width=4)
    source(d, SRC_RT + ' · 2026년 신고분 · 막대는 0억부터')

# ── 6. 누구라면 ─────────────────────────────────────────────────────
@board
def who2(im):              # 갈래 둘
    for i, (a, b) in enumerate((('노도강에', '집이 있다면'), ('노도강에서', '사려 한다면'))):
        def paint(cd, w, h, a=a, b=b):
            T(cd, (w // 2, 150), a, 80, INK, F_X); T(cd, (w // 2, 280), b, 96, INK, F_X)
        slip(im, (170, 1040)[i], (300, 330)[i], 720, 420, (-2.6, 2.2)[i], paint)
    d = ImageDraw.Draw(im); source(d, '계산·비교 자료이며 매수·매도 권유가 아닙니다')

@board
def calc(im):              # 따라 셈 — 9억 ÷ 10억 = 90%
    d = ImageDraw.Draw(im); T(d, (W // 2, 130), '예를 들어', 64, GREY, F_B)
    T(d, (560, 330), '2021년 가장 비싼 값', 60, GREY, F_B); T(d, (560, 450), '10억', 150, INK, F_X)
    T(d, (1360, 330), '요즘 가운데 값', 60, GREY, F_B); T(d, (1360, 450), '9억', 150, INK, F_X)
    T(d, (W // 2 - 20, 680), '9억 ÷ 10억 =', 110, INK, F_X, 'rm'); T(d, (W // 2 + 80, 680), '90%', 170, OR, F_X, 'lm')
    hand_ellipse(d, (W // 2 + 20, 555, W // 2 + 560, 815), seed=151)
    T(d, (W // 2, 900), f'노도강 {GRP[0]}곳의 가운데쯤', 64, INK, F_B)
    source(d, '예시 계산 · 441곳 가운데 90.0%(2021 최고 대비 2026-07~11 가운데 값)')

# ── 7. 함정과 직접 확인 ─────────────────────────────────────────────
TRAPS = (('호가 ≠ 실거래', '매물 가격과 팔린 가격은 다르다'), ('이번 달 숫자', '신고는 30일 안 — 아직 덜 들어옴'),
         ('면적 섞기', '같은 단지도 올랐다 내렸다 뒤집힌다'), ('한 건 신고가', '그 단지 전체 가격이 아니다'),
         ('특수 거래', '가족 간 거래 — 원자료에 표시 없음'))
WHY = ('매물값 ≠ 팔린 값', '신고 30일 남음', '면적마다 값이 다름', '그 단지 전체 아님', '가족 간 거래 표시 없음')
TRAP_SRC = '부동산 거래신고법 제3조 계약일부터 30일 이내 · 가족 간 거래 등은 원자료에 표시가 없어 이 편에서도 못 거름'

def _trap1(im, k):
    d = ImageDraw.Draw(im); T(d, (W // 2, 130), f'함정 {k + 1} / 5', 64, GREY, F_B)
    a, b = TRAPS[k]
    TF(d, (W // 2, 430), a, 180, INK, F_X); hand_under(d, 420, 1500, 560, seed=160 + k)
    TF(d, (W // 2, 720), b, 84, OR, F_X)
    source(d, TRAP_SRC)

for _k in range(5):
    B[f'traps_{_k + 1}'] = (lambda k: (lambda im: _trap1(im, k)))(_k)

@board
def traps(im):             # 다섯 모아 — 큰 제목 다섯 줄만(11/27 심사 못함: 쪽지 5장 = 슬라이드 티)
    d = ImageDraw.Draw(im); TF(d, (W // 2, 100), '함정 다섯', 100, INK, F_X)
    for i, (a, _) in enumerate(TRAPS):
        y = 260 + i * 150
        T(d, (300, y), f'{i + 1}', 76, GREY, F_X, 'mm'); T(d, (380, y), a, 90, INK, F_X, 'lm'); T(d, (1080, y), WHY[i], 54, GREY, F_B, 'lm')
    source(d, TRAP_SRC)

@board
def rt4(im):               # 실거래가 공개시스템 따라 하기 넷
    d = ImageDraw.Draw(im); TF(d, (W // 2, 110), '내 단지 직접 보기', 110, INK, F_X)
    R = ('단지 고르기', '면적 고르기', '기간 고르기', "'해제' 빼기")
    for i, a in enumerate(R):
        cx = 280 + i * 455; c = OR if i == 3 else INK
        T(d, (cx, 380), str(i + 1), 150, c, F_X)
        TF(d, (cx, 540), a, 64, c, F_X, maxw=420)
        if i < 3: hand_arrow(d, (cx + 160, 460), (cx + 300, 460), GREY, 7)
    T(d, (W // 2, 720), '2021년 최고  vs  올해 7월 이후 가운데 값', 56, INK, F_B)
    T(d, (W // 2, 880), 'rt.molit.go.kr', 120, INK, F_X)
    hand_under(d, 560, 1360, 950, color=INK, seed=171)
    source(d, '국토교통부 실거래가 공개시스템 · 화면은 우리가 다시 그림 · 가운데 값 = 값 순서로 줄 세웠을 때 한가운데')

# ── 8. 끝 ───────────────────────────────────────────────────────────
@board
def summary(im):           # 정리 표 세 줄
    d = ImageDraw.Draw(im); T(d, (W // 2, 130), '노도강 한 장 정리', 116, INK, F_X)
    rows = (('거래', '거래량은 4월의 절반 · 2021년보다는 많음'), ('값', f'2021 꼭대기의 90%쯤 · 넘은 곳 {GRP[2]}곳'),
            ('신고가', f'{NEW[0]}곳 · 월계동 묶음은 44%가 신고가'))
    for i, (k, v) in enumerate(rows):
        y = 360 + i * 200
        T(d, (420, y), k, 72, GREY, F_B, 'rm'); TF(d, (480, y), v, 84, OR if i == 1 else INK, F_X, 'lm', maxw=1340)
        if i < 2: d.line([(200, y + 100), (1760, y + 100)], fill=LINE, width=2)
    T(d, (W // 2, 920), '서울 전체는 꼭대기의 104%', 56, INK, F_B)
    source(d, '국토교통부 실거래(2026-11-22·24)·서울시·법제처 · 계산·비교 자료이며 매수·매도 권유가 아닙니다')

def main(names):
    os.makedirs(OUT, exist_ok=True)
    for n in names or list(B):
        im = canvas(); B[n](im); im.save(os.path.join(OUT, n + '.png')); print(n)

if __name__ == '__main__':
    main(sys.argv[1:])
