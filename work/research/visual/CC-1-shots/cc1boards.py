"""CC-1 장면 판 — visual-designer 2026-11-26. SQ-1 sq1boards.py와 같은 꼴·같은 부품(k1boards):
구겨진 종이 바탕 · 펜 빗금 막대(hatch_bar) · 주황 #FF5A00은 그 화면의 답 하나 · 손 동그라미·밑줄 · 상자·카드 판 없음.
숫자는 ep/CC-1 cc1_calc_out_1122·cc1_windows_out_1122·cmp_div_out_1122 출력을 그대로 읽고 assert(옮겨 적지 않음),
자막에만 있는 값(포털 차트 1만 1,520원·총보수)은 script.md v1.3 자막 줄과 글자 그대로 대조.
판은 '답이 열린 마지막 모습' — '?' → 열림은 PD가 Remotion에서. 파일 이름 = shot_plan.md '파일' 칸.
cc1_ends6는 만들지 않음(motion 11/26 EndFlip 움직이는 판으로 대체, today.md [알림] 11:59).
사용: py -3.12 cc1boards.py [이름 ...]   (없으면 전부) → work/video/public/bg/cc1/board/<이름>.png
"""
import os, sys, re, ast, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'K-1-shots'))
from k1boards import (W, H, INK, GREY, OR, FADE, KRAFT, F_B, F_M, F_X, font, canvas, T, TF, source, obj,
                      hand_ellipse, hand_under, hand_check, hand_arrow, hatch_bar, bars, linechart)
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding='utf-8')
WORK = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'CC-1')
OUT = os.path.join(WORK, 'video', 'public', 'bg', 'cc1', 'board')
LINE = (206, 198, 186)
rd = lambda fn: open(os.path.join(EP, fn), encoding='utf-8').read()
_calc, _win, _div, _sc = rd('cc1_calc_out_1122.txt'), rd('cc1_windows_out_1122.txt'), rd('cmp_div_out_1122.txt'), rd('script.md')

# ── calc 출력에서 그대로 읽기 ─────────────────────────────────────────
R = {}
for nm, st, how, dic in re.findall(r'^(KODEX|TIGER) \S+ (\d{4}-\d\d-\d\d) (받아 씀|다시 넣음) (\{.*\})$', _calc, re.M):
    R[(nm, st, how)] = ast.literal_eval(dic)
K1, T1 = R[('KODEX', '2025-11-20', '받아 씀')], R[('TIGER', '2025-11-20', '받아 씀')]
K1r, T1r = R[('KODEX', '2025-11-20', '다시 넣음')], R[('TIGER', '2025-11-20', '다시 넣음')]
K3, T3 = R[('KODEX', '2023-06-20', '받아 씀')], R[('TIGER', '2023-06-20', '받아 씀')]
K3r, T3r = R[('KODEX', '2023-06-20', '다시 넣음')], R[('TIGER', '2023-06-20', '다시 넣음')]
K0, K0r = R[('KODEX', '2022-09-27', '받아 씀')], R[('KODEX', '2022-09-27', '다시 넣음')]
assert (K1['합만원'], T1['합만원'], K1['받은분배금_세후만원'], K1['평가액만원'], T1['받은분배금_세후만원'], T1['평가액만원']) == (9654, 11793, 793, 8862, 294, 11498)
assert (K3['합만원'], T3['합만원'], K3['받은분배금_세후만원'], K3['평가액만원'], T3['받은분배금_세후만원'], T3['평가액만원']) == (14524, 15783, 3056, 11468, 1220, 14563)
assert (K1r['합만원'], T1r['합만원'], K3r['합만원'], T3r['합만원'], K0['합만원'], K0r['합만원']) == (9580, 11798, 14790, 16069, 14498, 14921)
assert (K1['시작가'], K1['끝가'], K1['주당분배합'], T1['시작가'], T1['끝가'], T1['주당분배합']) == (12605, 11170, 1181, 12615, 14505, 439)
assert (K0['끝가'], K0['주당분배합'], K0['분배횟수']) == (11170, 3934, 50)

def _dd(nm, st):
    m = re.search(rf'^{nm} {st} 합계 최대 낙폭\(%·고점일·바닥일\) \((-[\d.]+), \'([\d-]+)\', \'([\d-]+)\'\) 값만 최대 낙폭 \((-[\d.]+),', _calc, re.M)
    return float(m[1]), m[2], m[3], float(m[4])
DD = {(n, s): _dd(n, s) for n in ('KODEX', 'TIGER') for s in ('2025-11-20', '2023-06-20')}
assert DD[('KODEX', '2025-11-20')][0] == -15.1 and DD[('TIGER', '2025-11-20')][0] == -11.9
assert DD[('KODEX', '2023-06-20')][0] == -13.3 and DD[('TIGER', '2023-06-20')][0] == -12.6
assert DD[('KODEX', '2023-06-20')][3] == -19.3 and DD[('TIGER', '2023-06-20')][3] == -14.1
assert DD[('KODEX', '2025-11-20')][3] == -19.3 and DD[('TIGER', '2025-11-20')][3] == -12.8

MK = ast.literal_eval(re.search(r'^KODEX 1억\(.*?\) 매달 세후 만원: (\[.*\])$', _calc, re.M)[1])
MT = ast.literal_eval(re.search(r'^TIGER 1억 매달 세후 만원: (\[.*\])$', _calc, re.M)[1])
assert len(MK) == len(MT) == 12
mk, mt = [x[2] for x in MK], [x[2] for x in MT]
assert (min(mk), max(mk), min(mt), max(mt)) == (61.7, 69.1, 20.1, 30.2)

DY = {int(y): int(v) for y, v in re.findall(r'(\d{4}) (\d+)', re.search(r'^삼성 annualTrend (.*)$', _div, re.M)[1])}
assert DY == {2022: 153, 2023: 634, 2024: 934, 2025: 1130, 2026: 1083} and sum(DY.values()) == K0['주당분배합']

for s in ("네이버 금융 일별 시세 1만 1,520원", "삼성자산운용 종가 1만 2,605원", "연 0.190%(삼성자산운용)", "연 0.01%(미래에셋자산운용",
          "KODEX 약 2억 1,300만원", "TIGER 약 5억 7,500만원", "= 144.3만원", "= 53.6만원", "7,933주", "TIGER 7,927주", "차이 1,259만원"):
    assert s in _sc, s

def man(v):
    v = int(round(v)); e, m = divmod(v, 10000)
    return (f'{e}억 {m:,}만원' if m else f'{e}억원') if e else f'{m:,}만원'
assert man(9654) == '9,654만원' and man(11793) == '1억 1,793만원'
def won(v): return f'{v // 10000}만 {v % 10000:,}원' if v >= 10000 else f'{v:,}원'
assert won(12605) == '1만 2,605원'
pct = lambda v, d=1: (f'{v:+.{d}f}%').replace('-', '−')
NAME_K, NAME_T = 'KODEX 미국배당커버드콜액티브', 'TIGER 미국배당다우존스'
SRC_1Y = '2025-11-20 → 2026-11-20 종가 · 1억 · 분배금 15.4% 뗌 · 수수료·판 때 세금 뺌 · 삼성자산운용·미래에셋자산운용 공시'

B = {}
def board(fn):
    B[fn.__name__] = fn; return fn

def coins(im, cx, base, n, h_each, color=KRAFT, rw=110, seed=1):
    """동전 n개를 아래에서 위로 쌓음(옆에서 본 납작한 타원) — 높이 h_each(px)씩."""
    d = ImageDraw.Draw(im); rnd = random.Random(seed); y = base
    for i in range(n):
        j = rnd.uniform(-6, 6); hh = max(10, h_each)
        d.ellipse((cx - rw + j, y - hh - 14, cx + rw + j, y - hh + 14), outline=color, width=6)
        d.line([(cx - rw + j, y - hh), (cx - rw + j, y)], fill=color, width=6)
        d.line([(cx + rw + j, y - hh), (cx + rw + j, y)], fill=color, width=6)
        y -= hh
    return y

def valley(im, box, depth_pct, vmax_pct, color, seed=1):
    """골짜기 하나 — 왼쪽 고점에서 바닥까지 depth_pct만큼 내려갔다가 오른쪽으로 일부 오름. 깊이만 숫자에 비례(모양은 그림)."""
    x0, y0, x1, y1 = box; d = ImageDraw.Draw(im); rnd = random.Random(seed)
    yb = y0 + (y1 - y0) * abs(depth_pct) / vmax_pct; n = 60; pts = []
    for i in range(n + 1):
        t = i / n; s = math.sin(math.pi * min(1, t / 0.72) / 2) if t <= 0.72 else 1 - 0.35 * (t - 0.72) / 0.28
        pts.append((x0 + (x1 - x0) * t, y0 + (yb - y0) * s + rnd.uniform(-3, 3)))
    poly = pts + [(x1, y0), (x0, y0)]
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(ov).polygon(poly, fill=color + (140,))
    im.paste(ov, (0, 0), ov); d = ImageDraw.Draw(im)
    d.line(pts, fill=INK, width=5, joint='curve'); d.line([(x0 - 30, y0), (x1 + 30, y0)], fill=INK, width=4)
    return x0 + (x1 - x0) * 0.72, yb

# ── 0. 여는 말 ───────────────────────────────────────────────────────
@board
def cc1_open2(im):          # 통장 둘 '커버드콜 ?'·'일반형 ?' 열린 모습 — 답(주황)은 질문의 주인공 커버드콜
    d = ImageDraw.Draw(im); TF(d, (W // 2, 120), '1년 전 1억, 지금 얼마 남았나', 96, INK, F_X)
    for cx, nm, sub, v, col, sd in ((560, '커버드콜', NAME_K, K1['합만원'], OR, 1), (1360, '일반형', NAME_T, T1['합만원'], INK, 2)):
        obj(im, 'bankbook', cx, 420, size=300, rot=-4 if sd == 1 else 3, seed=sd); d = ImageDraw.Draw(im)
        T(d, (cx, 640), nm, 84, INK, F_X); T(d, (cx, 720), sub, 40, GREY, F_B)
        T(d, (cx, 860), man(v), 116, col, F_X)
    hand_under(d, 560 - 300, 560 + 300, 935, seed=3)
    source(d, SRC_1Y + ' · 받은 분배금 + 남은 평가액')

# ── 1. 이 상품은 어떻게 분배금을 만드나 ────────────────────────────
@board
def cc1_cap(im):            # 선 하나가 오르다 천장에 닿아 평평 — 아래 동전 '대신 매달 받는 돈' (그림, 숫자 없음)
    d = ImageDraw.Draw(im); TF(d, (W // 2, 120), '오를 때는 위가 막힌다', 104, INK, F_X)
    x0, x1, base, cap = 260, 1300, 900, 470
    rnd = random.Random(9); up, capd = [], []
    for i in range(41):
        t = i / 40; x = x0 + (x1 - x0) * t; y = base - (base - cap + 150) * t + 22 * math.sin(t * 9) + rnd.uniform(-4, 4)
        up.append((x, y)); capd.append((x, max(y, cap)))
    xx = x0                                       # 천장 점선
    while xx < x1 + 60: d.line([(xx, cap), (min(xx + 26, x1 + 60), cap)], fill=GREY, width=4); xx += 44
    T(d, (x0 - 20, cap), '천장', 52, GREY, F_B, 'rm')
    d.line(up, fill=FADE, width=5, joint='curve')                 # 막히지 않았다면(옅게)
    d.line(capd, fill=INK, width=9, joint='curve')                # 커버드콜
    T(d, (x1 + 50, cap - 190), '주식 값이 더 오른 몫', 46, GREY, F_B, 'lm')
    T(d, (x1 + 50, cap - 130), '= 권리를 산 사람 몫', 46, GREY, F_B, 'lm')
    top = coins(im, 1600, 980, 6, 34, OR, rw=100, seed=11); d = ImageDraw.Draw(im)
    T(d, (1640, top - 80), '대신 매달 받는 돈', 54, OR, F_X)
    source(d, "삼성자산운용 상품 설명 — 배당 외에 콜옵션 매도로 추가 배당 재원 · 그림은 원리 설명(실제 값 아님)")

@board
def cc1_two(im):            # 이름표 둘 — 커버드콜: 배당주 + 옵션 팖 · 일반형: 배당주만
    d = ImageDraw.Draw(im); TF(d, (W // 2, 120), '두 상품, 무엇이 다른가', 100, INK, F_X)
    for cx, nm, prod, what, col in ((520, '커버드콜', NAME_K, '배당주 + 옵션 팖', OR), (1400, '일반형', NAME_T, '배당주만', INK)):
        T(d, (cx, 330), nm, 110, INK, F_X); T(d, (cx, 430), prod, 42, GREY, F_B)
        T(d, (cx, 620), what, 96, col, F_X)
        if col == OR: hand_under(d, cx - 330, cx + 330, 690, seed=21)
    d.line([(W // 2 + 20, 280), (W // 2 + 20, 760)], fill=LINE, width=3)
    T(d, (W // 2, 880), '분배 기준일 매월 15일 · 총보수 0.19% vs 0.01%', 50, INK, F_B)
    source(d, '삼성자산운용 상품 화면(2026-11-22 확인) · 미래에셋자산운용(2026-11-13)')

# ── 2. 최근 1년, 같은 날 1억 ───────────────────────────────────────
def _acct(im, title, r, nm, months_vals, coin_col, seed):
    d = ImageDraw.Draw(im); TF(d, (W // 2, 110), title, 92, INK, F_X)
    vmax = max(T1['평가액만원'], K1['평가액만원']); base, top_y = 800, 330
    # 왼쪽: 받은 분배금 — 동전 12개 쌓기, 높이 = 오른쪽 막대와 같은 눈금(만원당 px, 11/27 visual 고침 — 전엔 0.5px/만원이라 비율 틀림)
    sc = (base - top_y) / vmax; y = base; rnd = random.Random(seed)
    for i, v in enumerate(months_vals):
        hh = v * sc; j = rnd.uniform(-4, 4)
        d.ellipse((520 - 120 + j, y - hh - 10, 520 + 120 + j, y - hh + 10), fill=(236, 226, 208), outline=coin_col, width=4)
        y -= hh
    d.ellipse((400, base - 10, 640, base + 10), outline=coin_col, width=4)
    assert abs((base - y) - r['받은분배금_세후만원'] * sc) < 8, (base - y, r['받은분배금_세후만원'] * sc)
    T(d, (520, y - 80), man(r['받은분배금_세후만원']), 90, INK, F_X)
    T(d, (520, base + 60), '받은 분배금 (12번)', 50)
    # 오른쪽: 남은 평가액 막대
    h = (base - top_y) * r['평가액만원'] / vmax
    hatch_bar(im, (1100, base - h, 1400, base), KRAFT, seed=seed + 1); d = ImageDraw.Draw(im)
    T(d, (1250, base - h - 70), man(r['평가액만원']), 90, INK, F_X)
    T(d, (1250, base + 60), '남은 평가액', 50)
    T(d, (W // 2, 950), f'합 {man(r["합만원"])}', 70, OR, F_X)
    hand_under(d, W // 2 - 270, W // 2 + 270, 992, seed=seed + 2)

@board
def cc1_acct_cc(im):
    _acct(im, '커버드콜 통장, 1년 뒤', K1, NAME_K, mk, KRAFT, 31)
    source(ImageDraw.Draw(im), f'{NAME_K} · 7,933주쯤(1만 2,605원) · 1년 분배 12번 주당 1,181원 · ' + SRC_1Y.split(' · ', 1)[1])

@board
def cc1_acct_dj(im):
    _acct(im, '일반형 통장, 1년 뒤', T1, NAME_T, mt, KRAFT, 41)
    source(ImageDraw.Draw(im), f'{NAME_T} · 1년 분배 12번 주당 439원 · ' + SRC_1Y.split(' · ', 1)[1])

@board
def cc1_gap(im):            # 합계 막대 둘 + 차이 2,139만원
    d = ImageDraw.Draw(im); TF(d, (W // 2, 110), '같은 날, 같은 1억', 100, INK, F_X)
    gap = T1['합만원'] - K1['합만원']; assert gap == 2139
    tops = bars(im, [('커버드콜', K1['합만원'], KRAFT, man(K1['합만원']), INK), ('일반형', T1['합만원'], KRAFT, man(T1['합만원']), INK)],
                top_y=330, bw=260, gap=700, nsize=96, seed=51, vmax=12500)
    d = ImageDraw.Draw(im); (ax, ay, ax1), (bx, by, bx1) = tops
    xx = ax1 + 40
    while xx < bx - 20: d.line([(xx, ay), (min(xx + 22, bx - 20), ay)], fill=GREY, width=4); xx += 38
    mx = (ax1 + bx) // 2; hand_arrow(d, (mx, ay + 20), (mx, by + 10), OR, 7)
    T(d, (mx, ay + 70), '차이', 54, OR, F_B); T(d, (mx, ay + 150), man(gap), 96, OR, F_X)
    source(d, SRC_1Y + ' · 받아 씀 합(분배금 + 평가액)')

@board
def cc1_yield(im):          # 분배율 9.37% vs 1년 남은 돈 −3.5% — 동그라미는 총수익 쪽
    d = ImageDraw.Draw(im); TF(d, (W // 2, 120), '커버드콜, 분배율과 남은 돈', 96, INK, F_X)
    y = K1['주당분배합'] / K1['시작가'] * 100; assert f'{y:.2f}' == '9.37'
    tr = (K1['합만원'] / 10000 - 1) * 100; assert f'{tr:.1f}' == '-3.5'
    for cx, h, v, sub, col in ((560, '한 해 분배율', f'{y:.2f}%', '받은 돈만 셈', INK), (1360, '1년 남은 돈', pct(tr), '가격 + 분배금', OR)):
        T(d, (cx, 330), h, 76, INK, F_X); T(d, (cx, 570), v, 190, col, F_X); T(d, (cx, 760), sub, 56, GREY, F_B)
    hand_ellipse(d, (1360 - 330, 460, 1360 + 330, 680), seed=61)
    d.line([(W // 2, 280), (W // 2, 800)], fill=LINE, width=3)
    T(d, (W // 2, 920), '분배율 하나만 보지 말고 총수익을 따로', 64, INK, F_X)
    source(d, 'KODEX 1년 분배(세전) 1,181원 ÷ 1만 2,605원 = 9.37% · 받아 씀 합 9,654만원 = 1억 대비 −3.5%(세후)')

# ── 3. 더 길게 보면 ─────────────────────────────────────────────────
@board
def cc1_long2(im):          # 2023-06-20부터 막대 둘 — 분배금 몫(아래, 크래프트)·평가액 몫(위, 옅게)
    d = ImageDraw.Draw(im); TF(d, (W // 2, 110), '2023년 6월 20일에 1억씩 넣었다면', 90, INK, F_X)
    base, top_y, vmax, bw = 820, 320, 16500, 300
    for cx, nm, r, col, sd in ((600, '커버드콜', K3, INK, 71), (1320, '일반형', T3, OR, 73)):
        s = (base - top_y) / vmax; h_d = r['받은분배금_세후만원'] * s; h_v = r['평가액만원'] * s
        hatch_bar(im, (cx - bw // 2, base - h_d, cx + bw // 2, base), KRAFT, seed=sd)
        hatch_bar(im, (cx - bw // 2, base - h_d - h_v, cx + bw // 2, base - h_d), FADE, seed=sd + 1); d = ImageDraw.Draw(im)
        T(d, (cx, base - h_d - h_v - 70), man(r['합만원']), 96, col, F_X)
        T(d, (cx + bw // 2 + 24, base - h_d / 2), f'분배금 {man(r["받은분배금_세후만원"])}', 38, INK, F_B, 'lm')
        T(d, (cx, base + 60), nm, 56)
    assert T3['합만원'] - K3['합만원'] == 1259
    assert round(K3['받은분배금_세후만원'] / T3['받은분배금_세후만원'], 1) == 2.5
    T(d, (W // 2, 960), '분배금은 커버드콜이 2.5배, 남은 돈은 일반형이 1,259만원 더', 54, INK, F_X)
    source(d, '2023-06-20 → 2026-11-20 · 받아 씀 · 아래 진한 칸 = 받은 분배금(세후), 위 옅은 칸 = 평가액 · TIGER 시작 종가 야후 파이낸스(2차)')

@board
def cc1_since(im):          # 상장일부터 — 가격만 +11.7% · 분배금 포함 +45.0% · 한 주 3,934원 = 상장가의 39%
    d = ImageDraw.Draw(im); TF(d, (W // 2, 120), '커버드콜, 상장한 날부터 4년', 96, INK, F_X)
    p = (K0['끝가'] / K0['시작가'] - 1) * 100; t = (K0['합만원'] / 10000 - 1) * 100
    assert f'{p:.1f}' == '11.7' and f'{t:.1f}' == '45.0'
    for cx, h, v, col in ((560, '가격만', pct(p), INK), (1360, '분배금까지 더하면', pct(t), OR)):
        T(d, (cx, 330), h, 76, INK, F_X); T(d, (cx, 560), v, 200, col, F_X)
    hand_ellipse(d, (1360 - 360, 450, 1360 + 360, 670), seed=81)
    d.line([(W // 2, 280), (W // 2, 720)], fill=LINE, width=3)
    r39 = K0['주당분배합'] / K0['시작가'] * 100; assert f'{r39:.1f}' == '39.3'
    T(d, (W // 2, 860), f'한 주가 받은 분배금 {K0["주당분배합"]:,}원 = 상장가의 {r39:.0f}%', 70, INK, F_X)
    source(d, f'{NAME_K} 2022-09-27(1만원) → 2026-11-20 · 분배 {K0["분배횟수"]}번 · 세후 분배금 3,328만 + 평가액 1억 1,170만 · 삼성자산운용 공시')

@board
def cc1_divyear(im):        # 연도 막대 5개 — 한 주 분배금 연도 합
    d = ImageDraw.Draw(im); TF(d, (W // 2, 110), '커버드콜 한 주가 받은 분배금, 해마다', 88, INK, F_X)
    labs = {2022: '2022\n(석 달)', 2023: '2023', 2024: '2024', 2025: '2025', 2026: '2026\n(11월까지)'}
    items = [(str(y), DY[y], OR if y == 2025 else KRAFT, f'{DY[y]:,}원', OR if y == 2025 else INK) for y in sorted(DY)]
    tops = bars(im, items, top_y=420, bw=200, gap=110, nsize=72, seed=91, vmax=1200)
    d = ImageDraw.Draw(im)
    for (x, y, x1), yr in zip(tops, sorted(DY)):
        if yr in (2022, 2026): T(d, ((x + x1) // 2, 980), '석 달' if yr == 2022 else '11월까지', 38, GREY, F_B)
    assert round(DY[2025] / DY[2023], 1) == 1.8
    (a, ay, a1), (b, by, b1) = tops[1], tops[3]
    hand_arrow(d, ((a + a1) // 2, ay - 100), ((b + b1) // 2 - 30, by - 100), INK, 6)
    T(d, ((a1 + b) // 2, 250), '2년 사이 1.8배', 66, OR, F_X)
    source(d, '삼성자산운용 분배 이력(연도 합, 세전) · 2022년은 10~12월 · 2026년은 11월까지 11번')

# ── 4. 분배금은 많았는데 왜 덜 남았나 ──────────────────────────────
def _step(im, title, r, seed):
    d = ImageDraw.Draw(im); TF(d, (W // 2, 110), title, 92, INK, F_X)
    lo, hi = 10500, 15000; y0, y1 = 860, 300
    Y = lambda v: y0 - (y0 - y1) * (v - lo) / (hi - lo)
    a, b = r['시작가'], r['끝가']; xa0, xa1, xb1 = 240, 760, 1280
    d.line([(xa0, Y(a)), (xa1, Y(a)), (xa1, Y(b)), (xb1, Y(b))], fill=INK, width=9, joint='curve')
    T(d, ((xa0 + xa1) // 2, Y(a) - 60), won(a), 76, INK, F_X); T(d, (xa0 + 10, Y(a) + 44), '2025-11-20', 38, GREY, F_B, 'lm')
    T(d, ((xa1 + xb1) // 2, Y(b) - 60), won(b), 76, INK, F_X); T(d, (xb1 - 10, Y(b) + 44), '2026-11-20', 38, GREY, F_B, 'rm')
    diff = b - a
    hand_arrow(d, (xa1 + 40, Y(a)), (xa1 + 40, Y(b)), OR, 7)
    lab = f'{diff:+,}원'.replace('-', '−')
    if diff < 0: T(d, (xa1 - 30, Y(a) + 130), lab, 84, OR, F_X, 'rm')
    else: T(d, (xa1 + 70, (Y(a) + Y(b)) / 2), lab, 84, OR, F_X, 'lm')
    # 옆 동전 기둥 — 같은 눈금(원 → px)
    hh = (y0 - y1) * r['주당분배합'] / (hi - lo)
    top = coins(im, 1620, 860, 12, hh / 12, KRAFT, rw=110, seed=seed); d = ImageDraw.Draw(im)
    T(d, (1620, top - 70), f'분배 {r["주당분배합"]:,}원', 66, INK, F_X); T(d, (1620, 930), '1년 받은 분배금(세전)', 40, GREY, F_B)
    return diff

@board
def cc1_step_cc(im):        # 커버드콜 한 주 12,605 → 11,170 · 분배 1,181원 (같은 눈금)
    diff = _step(im, '커버드콜 한 주, 1년 사이', K1, 101); assert diff == -1435
    source(ImageDraw.Draw(im), 'KODEX 종가 2025-11-20 → 2026-11-20(−11.4%) · 1년 분배 주당 1,181원(세전) · 삼성자산운용 공시 · 막대·동전 같은 눈금')

@board
def cc1_step_dj(im):        # 일반형 한 주 12,615 → 14,505 · 분배 439원
    diff = _step(im, '일반형 한 주, 1년 사이', T1, 111); assert diff == 1890
    source(ImageDraw.Draw(im), 'TIGER 종가 2025-11-20(야후, 2차) → 2026-11-20(미래에셋 공시) · 1년 분배 주당 439원(세전) · 같은 눈금')

def _valleys(im, title, kv, tv, ksub, tsub, note=None, seed=121, circle=False):
    d = ImageDraw.Draw(im); TF(d, (W // 2, 110), title, 92, INK, F_X)
    for k, (bx, v, nm, sub, col) in enumerate((((200, 300, 880, 760), kv, '커버드콜', ksub, OR), ((1040, 300, 1720, 760), tv, '일반형', tsub, KRAFT))):
        xb, yb = valley(im, bx, v, 20, col, seed=seed + k); d = ImageDraw.Draw(im)
        T(d, ((bx[0] + bx[2]) // 2, 240), nm, 64, INK, F_X)
        T(d, (xb, yb + 90), pct(v).replace('+', ''), 110, OR if col == OR else INK, F_X)
        T(d, (xb, yb + 205 if circle else yb + 170), sub, 38, GREY, F_B)
        if col == OR and circle: hand_under(d, xb - 230, xb + 230, yb + 160, seed=seed + 9)   # 11/27 2차: 동그라미가 글자에 걸림(심사관 D) → 밑줄
    if note: T(d, (W // 2, 950), note, 54, INK, F_X)

@board
def cc1_dd(im):             # 1년 최대 낙폭(분배 더한 합계) −15.1% vs −11.9%
    k, t = DD[('KODEX', '2025-11-20')], DD[('TIGER', '2025-11-20')]
    _valleys(im, '최근 1년, 가장 많이 빠졌을 때', k[0], t[0], f'{k[1][2:]} → {k[2][2:]}', f'{t[1][2:]} → {t[2][2:]}', circle=True)
    d = ImageDraw.Draw(im)
    source(d, '분배금을 더한 합계 기준 · 가격만 KODEX −19.3% · TIGER −12.8% · 삼성·미래에셋자산운용 공시로 계산')

@board
def cc1_dd_long(im):        # 2023-06-20부터 −13.3% vs −12.6%, 아래 가격만 −19.3% vs −14.1%
    k, t = DD[('KODEX', '2023-06-20')], DD[('TIGER', '2023-06-20')]
    _valleys(im, '2023년 6월부터, 가장 많이 빠졌을 때', k[0], t[0], f'{k[1][2:]} → {k[2][2:]}', f'{t[1][2:]} → {t[2][2:]}',
             note=f'가격만 보면 {pct(k[3]).replace("+", "")} vs {pct(t[3]).replace("+", "")}', seed=141)
    source(ImageDraw.Draw(im), '2023-06-20 → 2026-11-20 · 분배금을 더한 합계 기준 · 삼성·미래에셋자산운용 공시로 계산')

# ── 5. 매달 얼마 들어왔나 ───────────────────────────────────────────
@board
def cc1_month12(im):        # 막대 12개 두 줄 — 1억 매달 세후 분배금, 가장 많은 달·적은 달 동그라미
    d = ImageDraw.Draw(im); TF(d, (W // 2, 100), '1억이면 매달 들어온 돈 (세후)', 92, INK, F_X)
    bw, gap, x0 = 92, 40, 330; s = 4.4
    for row, (nm, data, col, base) in enumerate((('커버드콜', MK, OR, 560), ('일반형', MT, KRAFT, 900))):
        T(d, (x0 - 40, base - 60), nm, 56, INK, F_X, 'rm')
        vals = [v for *_, v in data]; i_hi, i_lo = vals.index(max(vals)), vals.index(min(vals))
        for i, (dt, _, v) in enumerate(data):
            x = x0 + i * (bw + gap); h = v * s
            hatch_bar(im, (x, base - h, x + bw, base), col, seed=150 + row * 20 + i); d = ImageDraw.Draw(im)
            T(d, (x + bw // 2, base + 30), f'{int(dt[5:7])}월', 30, GREY, F_M)
            if i in (i_hi, i_lo):
                T(d, (x + bw // 2, base - h - 34), f'{v:g}만', 40, INK, F_X)
                if row == 0: hand_ellipse(d, (x - 30, base - h - 74, x + bw + 30, base - h + 2), INK, 5, seed=170 + i)
        T(d, (x0 + 12 * (bw + gap) + 10, base - 60), f'{min(vals):g}만~{max(vals):g}만원', 50, col if row == 0 else INK, F_X, 'lm')
    source(d, '1억 기준 매달 세후 · KODEX 7,933주(2025-12~2026-11) · TIGER(2025-11~2026-10 지급) · 삼성·미래에셋 분배 공시')

@board
def cc1_reinvest(im):       # 갈림길 — 받아 씀 vs 다시 넣음, 끝값 셋 줄
    d = ImageDraw.Draw(im); TF(d, (W // 2, 100), '분배금, 받아 쓰면 vs 다시 넣으면', 92, INK, F_X)
    hand_arrow(d, (1310, 200), (1080, 290), INK, 6); hand_arrow(d, (1310, 200), (1540, 290), INK, 6)
    cx = (500, 1060, 1560)
    T(d, (cx[1], 340), '받아 씀', 64, INK, F_X); T(d, (cx[2], 340), '다시 넣음', 64, INK, F_X)
    d.line([(160, 390), (1760, 390)], fill=INK, width=4)
    rows = (('커버드콜 · 최근 1년', K1, K1r), ('커버드콜 · 2023년 6월부터', K3, K3r), ('일반형 · 2023년 6월부터', T3, T3r))
    for i, (lab, a, b) in enumerate(rows):
        y = 490 + i * 150; hi = i == 2
        T(d, (cx[0] + 230, y), lab, 50, INK, F_B, 'rm')
        T(d, (cx[1], y), man(a['합만원']), 62, INK, F_X); T(d, (cx[2], y), man(b['합만원']), 62, OR if hi else INK, F_X)
        if i < 2: d.line([(160, y + 72), (1760, y + 72)], fill=LINE, width=2)
    hand_ellipse(d, (cx[2] - 260, 490 + 300 - 66, cx[2] + 260, 490 + 300 + 66), seed=181)
    T(d, (W // 2, 960), '두 기간 모두 남은 돈은 일반형이 더 많았다', 60, INK, F_X)
    source(d, '다시 넣음 = 분배금 세후로 그날 종가에 되삼 · 최근 1년 TIGER 받아 씀 1억 1,793만 · 다시 넣음 1억 1,798만 · 삼성·미래에셋자산운용 공시로 계산')

# ── 6. 세금 한 장 ───────────────────────────────────────────────────
@board
def cc1_tax(im):            # 분배금 × 15.4% → 144.3만 vs 53.6만
    d = ImageDraw.Draw(im); T(d, (W // 2, 150), '분배금 × 15.4%', 130, INK, F_X)
    hand_under(d, W // 2 - 420, W // 2 + 420, 240, INK, 7, seed=191)
    tk = 7933 * K1['주당분배합'] * 0.154 / 1e4; tt = 7927 * T1['주당분배합'] * 0.154 / 1e4
    assert f'{tk:.1f}' == '144.3' and f'{tt:.1f}' == '53.6'
    T(d, (W // 2, 360), '1억 넣고 1년, 세금으로 떼인 돈', 64, GREY, F_B)
    for x, nm, v, col in ((560, '커버드콜', tk, OR), (1360, '일반형', tt, INK)):
        T(d, (x, 520), nm, 80, INK, F_X); T(d, (x, 720), f'{v:.1f}만원', 160, col, F_X)
    d.line([(W // 2, 460), (W // 2, 820)], fill=LINE, width=3)
    T(d, (W // 2, 930), '운용사 설명: 과세는 현금분배금과 과표 늘어난 몫 중 작은 쪽', 46, GREY, F_B)
    source(d, '세전 분배 KODEX 7,933주 × 1,181원 · TIGER 7,927주 × 439원 · 이 계산은 분배금 전부 × 15.4% · 소득세법 제17조·제129조')

@board
def cc1_ruler(im):          # 눈금자 — 한 해 분배금 2천만원에 닿는 원금
    d = ImageDraw.Draw(im); TF(d, (W // 2, 110), '한 해 분배금 2천만원, 얼마부터 닿나', 92, INK, F_X)
    yk = K1['주당분배합'] / K1['시작가']; yt = T1['주당분배합'] / T1['시작가']
    pk, pt = 2000 / yk, 2000 / yt
    assert round(pk / 100) * 100 == 21300 and round(pt / 100) * 100 == 57500
    x0, x1, y = 240, 1640, 600; vmax = 60000; X = lambda v: x0 + (x1 - x0) * v / vmax
    d.line([(x0, y), (x1, y)], fill=INK, width=6)
    for v in range(0, vmax + 1, 10000):
        d.line([(X(v), y - 24), (X(v), y + 24)], fill=INK, width=5); T(d, (X(v), y + 70), f'{v // 10000}억', 44, GREY, F_B)
    for v in range(5000, vmax, 10000): d.line([(X(v), y - 12), (X(v), y + 12)], fill=GREY, width=3)
    for v, nm, col, dy in ((pk, '커버드콜', OR, -1), (pt, '일반형', INK, -1)):
        x = X(v); d.line([(x, y - 150), (x, y + 30)], fill=col, width=8)
        T(d, (x, y - 300), nm, 60, INK, F_X); T(d, (x, y - 235), '약 ' + man(round(v / 100) * 100), 64, col, F_X)
    T(d, (W // 2, 860), '이자·다른 배당이 있으면 더 일찍 닿는다', 60, INK, F_X)
    source(d, '세전 분배금 2,000만원 닿는 원금 · 이번 1년 분배율 KODEX 9.37% · TIGER 3.48% · 다른 이자·배당 없을 때 · 소득세법 제14조·제62조')

# ── 7. 함정 ─────────────────────────────────────────────────────────
@board
def cc1_chart2(im):         # 같은 날 가격 둘 — 포털 차트 1만 1,520원 · 운용사 종가 1만 2,605원
    d = ImageDraw.Draw(im); TF(d, (W // 2, 120), '2025년 11월 20일, 같은 날 가격 둘', 92, INK, F_X)
    for x, h, v, sub, col in ((560, '포털 차트', 11520, '분배금만큼 지난 값을 낮춘 값', INK), (1360, '운용사 종가', K1['시작가'], '그날 실제로 사고판 값', OR)):
        T(d, (x, 330), h, 80, INK, F_X); T(d, (x, 560), won(v), 140, col, F_X); T(d, (x, 720), sub, 46, GREY, F_B)
    hand_under(d, 1360 - 340, 1360 + 340, 655, seed=201)
    d.line([(W // 2, 280), (W // 2, 780)], fill=LINE, width=3)
    T(d, (W // 2, 900), '수익률을 셀 때는 한쪽 가격으로만', 70, INK, F_X)
    source(d, '네이버 금융 일별 시세(분배 반영 수정 값) · 삼성자산운용 상품 화면 수익률 표(2026-11-22 확인)')

@board
def cc1_fee(im):            # 총보수 0.19% vs 0.01% — 이미 가격에 빠짐
    d = ImageDraw.Draw(im); TF(d, (W // 2, 120), '한 해 총보수', 104, INK, F_X)
    for x, nm, v, col in ((560, '커버드콜', '0.19%', OR), (1360, '일반형', '0.01%', INK)):
        T(d, (x, 330), nm, 84, INK, F_X); T(d, (x, 580), v, 220, col, F_X)
    d.line([(W // 2, 280), (W // 2, 760)], fill=LINE, width=3)
    T(d, (W // 2, 880), '앞의 숫자는 모두 이 보수가 빠진 가격으로 셈', 64, INK, F_X)
    hand_under(d, W // 2 - 560, W // 2 + 560, 945, INK, 6, seed=211)
    source(d, 'KODEX 연 0.190%(삼성자산운용) · TIGER 연 0.01%(미래에셋자산운용, 2026-11-13) · 보수는 매일 순자산에서 빠짐')

# ── 8. 끝 ───────────────────────────────────────────────────────────
@board
def cc1_summary(im):        # 정리 표 다섯 줄
    d = ImageDraw.Draw(im); T(d, (W // 2, 100), '한 장 정리', 110, INK, F_X)
    cx = (560, 1040, 1530)
    T(d, (cx[1], 230), '커버드콜', 56, GREY); T(d, (cx[2], 230), '일반형', 56, GREY)
    d.line([(160, 275), (1760, 275)], fill=INK, width=4)
    win = re.findall(r'^\d{4}-\d\d-\d\d [\d.]+ [\d.]+ (커버드콜|일반형)$', _win, re.M); assert len(win) == 6
    nk, nt = win.count('커버드콜'), win.count('일반형'); assert (nk, nt) == (4, 2)
    assert int(min(mk) // 10) == 6 and int(min(mt) // 10) == 2 and int(max(mt) // 10) == 3
    rows = (('최근 1년 1억', man(K1['합만원']), man(T1['합만원'])),
            ('2023년 6월부터 1억', man(K3['합만원']), man(T3['합만원'])),
            ('1억 매달 세후', '60만원대', '20만원대'),
            ('가격만 가장 크게 빠짐(1년)', pct(DD[('KODEX', '2025-11-20')][3]).replace('+', ''), pct(DD[('TIGER', '2025-11-20')][3]).replace('+', '')),
            ('끝날 6개 중 앞선 횟수', f'{nk}번', f'{nt}번'))
    for i, (k, a, b) in enumerate(rows):
        y = 340 + i * 120
        T(d, (cx[0] + 190, y), k, 50, INK, F_B, 'rm'); T(d, (cx[1], y), a, 62, INK, F_X); T(d, (cx[2], y), b, 62, INK, F_X)
        d.line([(160, y + 64), (1760, y + 64)], fill=LINE, width=2)
    T(d, (W // 2, 950), '받는 돈과 남는 돈은 다른 숫자', 60, OR, F_X)
    source(d, '삼성자산운용·미래에셋자산운용 공시, 야후 파이낸스(2차) · 기준 2026-11-20 종가 · 계산·비교 자료이며 매수·매도 권유가 아닙니다')

def main(names):
    os.makedirs(OUT, exist_ok=True)
    for n in names or list(B):
        im = canvas(); B[n](im); im.save(os.path.join(OUT, n + '.png')); print(n)

if __name__ == '__main__':
    main(sys.argv[1:])
