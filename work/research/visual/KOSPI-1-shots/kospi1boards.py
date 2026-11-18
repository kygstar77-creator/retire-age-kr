"""KOSPI-1 장면 판 — visual-designer 2026-11-18. H-5·JT-1·K-1 판과 같은 꼴·같은 부품(k1boards):
구겨진 종이 바탕 · 펜 빗금 막대(hatch_bar) · 주황 #FF5A00은 그 화면의 답 하나 · 손 동그라미·밑줄.
숫자는 ep/KOSPI-1 calc2_out·calc3_out·calc4_out·kospi_daily_ecos.json(한국은행 ECOS 일별 종가)와 script.md 자막 값만.
calc 출력 파일을 그대로 읽고 assert(옮겨 적지 않음). 판은 '답이 열린 마지막 모습' — '?' → 열림은 PD가 Remotion에서.
판 목록은 script.md의 (화면 [판]/[표]) 줄 순서 + shot_plan(11/18 PD) '판으로' 돌린 줄. 이름은 PD가 props에서 그대로 쓰면 됨.
사용: py -3.12 kospi1boards.py [이름 ...]   (없으면 전부) → work/video/public/bg/kospi1/board/<이름>.png
"""
import os, sys, re, json, math, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'K-1-shots')); sys.path.insert(0, os.path.join(HERE, '..', 'H-4-shots'))
from k1boards import (W, H, INK, GREY, OR, FADE, F_B, F_M, F_X, font, canvas, T, TF, source,
                      hand_ellipse, hand_under, hand_check, hand_arrow, hatch_bar)
from h4boards import _wobble_rect
from PIL import ImageDraw

WORK = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'KOSPI-1')
OUT = os.path.join(WORK, 'video', 'public', 'bg', 'kospi1', 'board')
LINE = (206, 198, 186)
SRC = '한국은행 경제통계시스템(ECOS) 코스피 일별 종가 1995.01.03~2026.11.13 · 하루 = 전날 종가 대비 종가'
rd = lambda fn: open(os.path.join(EP, fn), encoding='utf-8').read()

# ── calc 출력에서 그대로 읽기 ─────────────────────────────────────────
_c2, _c3, _cd = rd('calc2_out.txt'), rd('calc3_out.txt'), rd('calc4_out.txt')
YEAR5 = {int(k): v for k, v in eval(re.search(r'하루 -5% 이하 날 수\(0인 해 생략\): (\{.*?\})', _c2).group(1)).items()}
GRP = [dict(d=d, drop=float(dr), y1=(float(y1) if y1 else None), rec=int(rc))
       for d, dr, y1, rc in re.findall(r'(\d{8}) (-[\d.]+)% 종가 [\d,.]+ \| 1년 뒤 ([+-][\d.]+)?%? ?\| 3년 뒤 [^|]*\| 전날 값 되찾기 (\d+)거래일', _c2)]
LOW = dict((d, float(v)) for d, v in re.findall(r"\('(\d{8})', (-?[\d.]+)\)", _cd.split('중앙')[1]))
UP8 = [(d, float(v)) for d, v in re.findall(r"\('(\d{8})', ([\d.]+)\)", _c2.split('하루 상승 상위 8:')[1].split('\n')[0])]
PM5 = int(re.search(r'±5% 넘은 날 수 (\d+)', _c2).group(1))
m = re.search(r'한 번에: 최저 (\d+) 중앙 (\d+) 최고 (\d+) 원금 넘은 편 (\d+)', _c3); ONE = [int(x) for x in m.groups()]
m = re.search(r'나눠 넣기: 최저 (\d+) 중앙 (\d+) 최고 (\d+) 원금 넘은 편 (\d+)', _c3); SPL = [int(x) for x in m.groups()]
SPLIT_WIN = int(re.search(r'나눠 넣기가 더 많은 편 (\d+) / 15', _c3).group(1))
DAILY = json.load(open(os.path.join(EP, 'kospi_daily_ecos.json'), encoding='utf-8'))
assert YEAR5[2026] == 23 and sum(v for k, v in YEAR5.items() if k <= 2025) == 57 and YEAR5[1997] == YEAR5[1998] == 9 and YEAR5[2000] == 11
assert len(GRP) == 16 and len(LOW) == 15 and len(UP8) == 8 and PM5 == 40
done = [g for g in GRP if g['y1'] is not None]
assert len(done) == 15 and sum(g['y1'] > 0 for g in done) == 10 and st.median(g['y1'] for g in done) == 19.1
assert sum(v < 0 for v in LOW.values()) == 14 and st.median(LOW.values()) == -11.8
assert st.median(g['rec'] for g in GRP[:15]) == 8 and max(g['rec'] for g in GRP) == 1367
assert ONE == [5506998, 11914250, 26712009, 10] and SPL == [7714515, 10852500, 17673118, 10] and SPLIT_WIN == 5
CL = {t: v for t, v in DAILY}
assert CL['20260102'] == 4309.63 and CL['20260622'] == 9114.55 and CL['20261113'] == 5290.53

def man(v): return f'{round(v / 10000):,}만'          # 5506998 → '551만'
def ymd(d): return f'{d[:4]}.{d[4:6]}.{d[6:]}'
def pct(v): return f'{v:+.1f}%'

B = {}
def board(fn):
    B[fn.__name__] = fn; return fn

def qa(im, q, a, sub=None, src=SRC, asize=330):   # 공책 판 — 질문 위, 답(주황) 가운데, 동그라미
    d = ImageDraw.Draw(im)
    TF(d, (W // 2, 200), q, 84, INK, F_X)
    T(d, (W // 2, 560), a, asize, OR, F_X)
    w = font(F_X, asize).getlength(a)
    hand_ellipse(d, (W // 2 - w / 2 - 90, 380, W // 2 + w / 2 + 90, 760), seed=len(a))
    if sub: T(d, (W // 2, 900), sub, 72, INK, F_X)
    source(d, src)

# ── 0. 여는 말 ───────────────────────────────────────────────────────
@board
def open23(im):            # '하루 -5% 넘게 빠진 날, 올해 몇 번?' → 23번
    qa(im, '하루 5% 넘게 빠진 날, 올해 몇 번?', '23번', 'IMF 외환위기 때는 한 해 9번',
       SRC + ' · 2026.01.02~11.13 · 1997·1998 각 9일')

# ── 1. 올해 코스피 ──────────────────────────────────────────────────
def _line(im, box, a, b, marks):
    d = ImageDraw.Draw(im); x0, y0, x1, y1 = box
    pts = [(t, v) for t, v in DAILY if a <= t <= b]
    vmin, vmax = 0, 10000
    X = lambda i: x0 + (x1 - x0) * i / (len(pts) - 1); Y = lambda v: y1 - (y1 - y0) * (v - vmin) / (vmax - vmin)
    for g in (2500, 5000, 7500, 10000):
        d.line([(x0, Y(g)), (x1, Y(g))], fill=LINE, width=2); T(d, (x0 - 20, Y(g)), f'{g:,}', 34, GREY, F_B, 'rm')
    d.line([(x0, y1), (x1, y1)], fill=GREY, width=4)
    d.line([(X(i), Y(v)) for i, (t, v) in enumerate(pts)], fill=INK, width=7, joint='curve')
    idx = {t: i for i, (t, _) in enumerate(pts)}
    for mo in range(1, 13):
        t = next((t for t, _ in pts if t[4:6] == f'{mo:02d}'), None)
        if t: T(d, (X(idx[t]), y1 + 40), f'{mo}월', 34, GREY, F_B)
    out = {}
    for t in marks:
        x, y = X(idx[t]), Y(CL[t]); d.ellipse((x - 18, y - 18, x + 18, y + 18), fill=INK); out[t] = (x, y)
    return d, out

@board
def line2026(im):          # 올해 선 — 4,309 · 9,114 · 5,290 세 점이 한 선 위에(이해 시험: 세 점 계속) · -42%
    d, P = _line(im, (230, 230, 1700, 900), '20260102', '20261113', ('20260102', '20260622', '20261113'))
    TF(d, (W // 2, 100), '올해 코스피, 하루 마감 숫자', 84, INK, F_X)
    (ax, ay), (px, py), (ex, ey) = P['20260102'], P['20260622'], P['20261113']
    T(d, (ax + 30, ay + 70), '1월 4,309', 56, INK, F_X, 'lm')
    T(d, (px, py - 60), '6월 꼭대기 9,114', 56, INK, F_X)
    T(d, (ex - 10, ey + 80), '지금 5,290', 56, INK, F_X, 'rm')
    hand_arrow(d, (px + 60, py + 20), (ex - 10, ey - 40), OR, 8)
    T(d, (1560, 330), '-42%', 150, OR, F_X)
    source(d, 'ECOS 코스피 일별 종가 · 2026.01.02 4,309.63 · 06.22 9,114.55 · 11.13 5,290.53 · 세로축 0부터')

@board
def arrows3(im):           # 한 점(지금 5,290)에서 세 화살표 — 작년 첫날 +120% · 올해 첫날 +23% · 6월 꼭대기 -42%
    d = ImageDraw.Draw(im)
    TF(d, (W // 2, 110), '지금 5,290 — 어디서부터 재느냐에 따라', 80, INK, F_X)
    cx, cy = 360, 560
    d.ellipse((cx - 30, cy - 30, cx + 30, cy + 30), fill=INK); T(d, (cx, cy + 80), '지금', 56, INK, F_X)
    rows = (('작년 첫날부터', '+120%', INK, 330), ('올해 첫날부터', '+23%', INK, 560), ('6월 꼭대기부터', '-42%', OR, 790))
    for lab, v, c, y in rows:
        hand_arrow(d, (cx + 50, cy), (900, y), c, 7)
        T(d, (940, y), lab, 64, GREY, F_B, 'lm'); T(d, (1740, y), v, 130, c, F_X, 'rm')
    source(d, SRC + ' · 2025.01.02 2,398.94 · 2026.01.02 4,309.63 · 06.22 9,114.55 → 11.13 5,290.53')

@board
def yearbars(im):          # 해마다 하루 -5% 넘게 빠진 날 — 2026만 주황(23), 1997·1998 9 · 2000 11 · 2008 8 이름
    d = ImageDraw.Draw(im); TF(d, (W // 2, 100), '하루 5% 넘게 빠진 날, 해마다', 84, INK, F_X)
    ys = sorted(YEAR5); n = len(ys); x0, x1, base, top = 150, 1770, 850, 260; slot = (x1 - x0) / n; bw = slot * 0.62
    for i, y in enumerate(ys):
        v = YEAR5[y]; x = x0 + i * slot + (slot - bw) / 2; yt = base - (base - top) * v / 24
        c = OR if y == 2026 else (INK if y in (1997, 1998, 2000, 2008) else FADE)
        hatch_bar(im, (x, yt, x + bw, base), c, seed=40 + i, step=11, width=5); d = ImageDraw.Draw(im)
        if y in (1997, 1998, 2000, 2008, 2026):
            T(d, (x + bw / 2, yt - (80 if y == 2026 else 46)), f'{v}', 130 if y == 2026 else 64, c, F_X)
        T(d, (x + bw / 2, base + 40), f"'{str(y)[2:]}", 36, OR if y == 2026 else INK, F_B)
    d.line([(x0 - 10, base), (x1 + 10, base)], fill=GREY, width=4)
    T(d, (W // 2, 980), '1995~2025년 31년을 다 더하면 57번', 58, INK, F_B)
    source(d, SRC + ' · 0인 해는 뺌 · 2026 = 11.13까지')

# ── 2. 서킷브레이커와 사이드카 ────────────────────────────────────────
@board
def breaker3(im):          # 계단 세 칸 8% · 15% · 20%
    d = ImageDraw.Draw(im); TF(d, (W // 2, 110), '서킷브레이커 = 시장 전체를 멈춤', 84, INK, F_X)
    steps = (('8%', '20분 멈춤'), ('15%', '20분 멈춤'), ('20%', '그날 끝'))
    x, y = 250, 360
    for i, (p, t) in enumerate(steps):
        d.line([(x, y), (x + 470, y)], fill=INK, width=9); d.line([(x + 470, y), (x + 470, y + 200)], fill=INK, width=9)
        T(d, (x + 235, y - 80), f'-{p}', 130, OR if i == 0 else INK, F_X); T(d, (x + 235, y + 80), t, 58, INK, F_B)
        x += 470; y += 200
    T(d, (W // 2, 1000 - 40), '전날 마감보다 떨어진 채 1분 넘게', 56, GREY, F_B)
    source(d, '한국거래소 시장운영 규정(2차: 뉴시스 2026.03.06 · 토스뱅크) · 1단계·2단계 20분 매매 중단, 3단계 그날 매매 종료')

@board
def sidecar(im):           # 사이드카 = 프로그램 주문만 5분
    d = ImageDraw.Draw(im)
    T(d, (W // 2, 330), '사이드카', 200, INK, F_X)
    T(d, (W // 2, 600), '프로그램 주문만 5분', 130, OR, F_X)
    hand_under(d, W // 2 - 600, W // 2 + 600, 690, seed=12)
    T(d, (W // 2, 840), '사람이 넣는 주문은 그대로', 64, GREY, F_B)
    source(d, '코스피200 선물 기준가 대비 5% 이상 1분 → 프로그램매매 호가 5분 효력 정지(2차: foxcg · 한경 생글)')

@board
def cb11(im):              # '올해 서킷브레이커 몇 번째?' → 11번째(보도 기준)
    qa(im, '올해 서킷브레이커, 몇 번째였나?', '11번째', '2026.11.06 아침 · 보도 기준',
       '아시아경제 2026.11.06 "올해 11번째·역대 17번째" · 보도 순번 기준(거래소 공식 목록 대조 안 됨)', asize=280)

@board
def nov6(im):              # 두 칸 — 아침 9시 3분 -8.55% · 같은 날 마감 -6.02%
    d = ImageDraw.Draw(im); TF(d, (W // 2, 120), '11월 6일, 같은 날 두 숫자', 84, INK, F_X)
    for cx, lab, v, c in ((520, '아침 9시 3분', '-8.55%', INK), (1400, '같은 날 마감', '-6.02%', OR)):
        T(d, (cx, 380), lab, 72, GREY, F_B); T(d, (cx, 580), v, 200, c, F_X)
    d.line([(W // 2, 330), (W // 2, 760)], fill=LINE, width=4)
    hand_under(d, 1110, 1690, 700, seed=21)
    T(d, (W // 2, 900), '하루 비교는 마감 숫자로 셌어요', 64, INK, F_X)
    source(d, '발동 시점 4,923.47(-8.55%, 2차: 경향신문 · 아시아경제) · 종가 5,059.69 전날 대비 -6.02%(ECOS)')

@board
def check2(im):            # 체크 두 칸 — 신용·미수 / 레버리지
    d = ImageDraw.Draw(im); TF(d, (W // 2, 150), '이런 날 먼저 볼 것 두 가지', 84, INK, F_X)
    for i, s in enumerate(('신용·미수 있나?', '레버리지 상품 있나?')):
        y = 430 + i * 230
        _wobble_rect(d, (420, y - 60, 540, y + 60), INK, 6, seed=30 + i); hand_check(d, 480, y, 60)
        T(d, (600, y), s, 100, INK, F_X, 'lm')
    T(d, (W // 2, 920), '담보 비율 아래로 내려가면 반대매매될 수 있어요', 56, GREY, F_B)
    source(d, '신용거래·미수거래 반대매매 기준은 증권사마다 다름')

# ── 3. 지난 31년 ────────────────────────────────────────────────────
@board
def group2008(im):         # '묶음' 뜻 — 2008년 가을 하루 -5% 날 8개를 한 괄호로(이해 시험: 일주일 새 두 날을 한 괄호로)
    d = ImageDraw.Draw(im); TF(d, (W // 2, 110), '몰려 온 날은 한 묶음으로 셌어요', 84, INK, F_X)
    p, days = None, []
    for t, v in DAILY:
        if p and t[:4] == '2008' and v / p - 1 <= -0.05: days.append((t, (v / p - 1) * 100))
        p = v
    assert len(days) == YEAR5[2008] == 8 and days[0][0] == '20080916'
    t0 = [t for t, _ in DAILY].index('20080901'); t1 = [t for t, _ in DAILY].index('20081128')
    x0, x1, yb = 200, 1720, 640
    X = lambda t: x0 + (x1 - x0) * ([s for s, _ in DAILY].index(t) - t0) / (t1 - t0)
    d.line([(x0, yb), (x1, yb)], fill=GREY, width=5)
    for mo, lab in (('20080901', '9월'), ('20081001', '10월'), ('20081103', '11월')):
        T(d, (X(mo), yb + 60), lab, 48, GREY, F_B)
    for t, r in days:
        x = X(t); d.ellipse((x - 20, yb - 20, x + 20, yb + 20), fill=OR if t == days[0][0] else INK)
    xa, xb = X(days[0][0]) - 30, X(days[-1][0]) + 30
    d.line([(xa, yb - 70), (xa, yb - 110), (xb, yb - 110), (xb, yb - 70)], fill=OR, width=8)
    T(d, ((xa + xb) / 2, yb - 190), '8번 → 한 묶음', 110, OR, F_X)
    T(d, (X(days[0][0]), yb + 140), '첫날 9월 16일', 56, INK, F_X)
    T(d, (W // 2, 960), '석 달(60거래일) 안에 이어진 날은 첫날 하나로', 58, INK, F_B)
    source(d, SRC + ' · 2008.09.16~11.20 하루 -5% 이하 8일')

@board
def table16(im):           # 무리 첫날 표 16줄 — 첫날 하락률 · 1년 뒤 · 1년 안 최저
    d = ImageDraw.Draw(im); T(d, (W // 2, 70), '묶음 열여섯 — 첫날 그 뒤', 64, INK, F_X)
    cols = (520, 880, 1260, 1640); y = 150
    for x, h in zip(cols, ('첫날', '그날 하락', '1년 뒤', '1년 안 가장 낮을 때')):
        T(d, (x, y), h, 36, GREY, F_B)
    d.line([(300, y + 30), (1820, y + 30)], fill=LINE, width=3)
    for i, g in enumerate(GRP):
        y = 205 + i * 50
        T(d, (cols[0], y), ymd(g['d']), 36, INK, F_B)
        T(d, (cols[1], y), f"{g['drop']:.2f}%", 36, INK, F_B)
        T(d, (cols[2], y), pct(g['y1']) if g['y1'] is not None else '1년 안 됨', 38 if g['y1'] is not None else 32, INK if g['y1'] is not None else GREY, F_X if g['y1'] is not None else F_B)
        lo = LOW.get(g['d']); T(d, (cols[3], y), pct(lo) if lo is not None else '—', 38, INK if lo is not None else GREY, F_X)
    source(d, SRC + ' · 60거래일 안은 한 묶음 · 1년 뒤 = 252거래일 뒤 종가 · 첫날 종가 대비')

@board
def names4(im):            # 묶음 첫날 이름표 네 장
    d = ImageDraw.Draw(im); TF(d, (W // 2, 120), '열여섯 묶음 중에는 이런 날들', 84, INK, F_X)
    rows = (('외환위기', '19971024'), ('미국 테러 다음 날', '20010912'), ('금융위기', '20080916'), ('코로나', '20200319'))
    G = {g['d']: g for g in GRP}
    for i, (nm, dd) in enumerate(rows):
        y = 320 + i * 170
        T(d, (900, y), nm, 92, INK, F_X, 'rm'); T(d, (960, y), ymd(dd), 60, GREY, F_B, 'lm')
        T(d, (1500, y), f"{G[dd]['drop']:.1f}%", 80, INK, F_X, 'lm')
        if i < 3: d.line([(250, y + 85), (1700, y + 85)], fill=LINE, width=2)
    source(d, SRC + ' · 그날 전날 종가 대비')

@board
def q14(im):               # '1년 안에 첫날보다 더 내려간 적 있나?' → 14/15
    qa(im, '1년 안에 첫날보다 더 내려간 적 있나?', '14 / 15', '더 내려간 폭 가운데 -11.8%',
       SRC + ' · 1년 다 지난 묶음 15 · 첫날 종가 대비 1년 안 최저')

@board
def dots15(im):            # 15칸 점 — 1년 뒤 오른 편 10/15(주황)
    d = ImageDraw.Draw(im); TF(d, (W // 2, 140), '1년 뒤, 첫날보다 올랐나?', 84, INK, F_X)
    gap = 104; x0 = W // 2 - gap * 7
    for i, g in enumerate(done):
        x = x0 + i * gap; up = g['y1'] > 0
        if up: d.ellipse((x - 38, 430 - 38, x + 38, 430 + 38), fill=OR)
        else: d.ellipse((x - 38, 430 - 38, x + 38, 430 + 38), outline=INK, width=7)
        T(d, (x, 520), f"{g['d'][2:4]}.{g['d'][4:6]}", 26, GREY, F_B)
    T(d, (W // 2, 720), '오른 편 10 / 15', 150, OR, F_X)
    T(d, (W // 2, 900), '가운데 +19.1% · 크게 빠진 해도 있었어요', 62, INK, F_X)
    source(d, SRC + ' · 묶음 첫날 종가 → 252거래일 뒤 종가')

# ── 4. 되찾기까지 ───────────────────────────────────────────────────
@board
def recover15(im):         # 열다섯 칸 막대 — 되찾기까지 거래일(위 잘림 표시) · 가운데 8
    d = ImageDraw.Draw(im); TF(d, (W // 2, 100), '전날 마감 숫자를 다시 넘기까지', 84, INK, F_X)
    gs = sorted(GRP[:15], key=lambda g: g['rec']); cap = 100
    n = 15; x0, x1, base, top = 200, 1720, 860, 290; slot = (x1 - x0) / n; bw = slot * 0.6
    for i, g in enumerate(gs):
        v = min(g['rec'], cap); x = x0 + i * slot + (slot - bw) / 2; yt = base - (base - top) * v / cap
        c = OR if i == 7 else INK if g['rec'] > cap else FADE
        hatch_bar(im, (x, yt, x + bw, base), c, seed=60 + i, step=11, width=5); d = ImageDraw.Draw(im)
        if g['rec'] > cap:
            d.line([(x - 6, yt + 30), (x + bw + 6, yt + 14)], fill=(236, 228, 214), width=12)
            T(d, (x + bw / 2, yt - (44 if g['rec'] < 1000 else 104)), f"{g['rec']:,}", 46, INK, F_X)
        if i == 7: T(d, (x + bw / 2, yt - 90), '8', 150, OR, F_X)
        T(d, (x + bw / 2, base + 40), f"{g['d'][2:4]}.{g['d'][4:6]}", 28, GREY, F_B)
    d.line([(x0 - 10, base), (x1 + 10, base)], fill=GREY, width=4)
    T(d, (W // 2, 965), '가운데 8거래일 · 가장 길게 1,367거래일', 58, INK, F_B)
    source(d, SRC + ' · 묶음 첫날 기준 15 · 막대 단위 거래일 · 100 넘는 막대는 위를 자름(숫자 표시)')

@board
def long1367(im):          # 긴 막대 하나가 화면 밖까지 — 5년 넘게
    d = ImageDraw.Draw(im); TF(d, (W // 2, 150), '닷컴 거품 때 (2000년 1월)', 84, INK, F_X)
    hatch_bar(im, (120, 430, W + 40, 600), OR, seed=71, step=12, width=6); d = ImageDraw.Draw(im)
    hatch_bar(im, (120, 700, 120 + 20, 800), INK, seed=72, step=8, width=4); d = ImageDraw.Draw(im)
    T(d, (170, 750), '가운데 8거래일', 56, INK, F_B, 'lm')
    T(d, (W // 2, 360), '1,367거래일 · 5년 넘게', 110, OR, F_X)
    T(d, (W // 2, 930), '다시 넘은 건 2005년 7월', 72, INK, F_X)
    source(d, SRC + ' · 2000.01.05 묶음 · 막대 길이 같은 비율(8거래일 = 짧은 막대)')

@board
def pair2008(im):          # 금융위기: 일주일 만에 되찾음 · 그 뒤 1년 안에 32% 더 내려감
    d = ImageDraw.Draw(im); TF(d, (W // 2, 140), '금융위기 (2008년 9월 16일 묶음)', 84, INK, F_X)
    T(d, (300, 420), '되찾기까지', 64, GREY, F_B, 'lm'); T(d, (1620, 420), '5거래일', 130, INK, F_X, 'rm')
    d.line([(280, 540), (1640, 540)], fill=LINE, width=3)
    T(d, (300, 680), '그 뒤 1년 안', 64, GREY, F_B, 'lm'); T(d, (1620, 680), '-32.4%', 150, OR, F_X, 'rm')
    hand_under(d, 1160, 1630, 770, seed=31)
    T(d, (W // 2, 920), '되찾았다고 끝난 게 아니었어요', 64, INK, F_X)
    source(d, SRC + ' · 첫날 종가 대비 1년 안 최저')

# ── 5. 오른 날 ─────────────────────────────────────────────────────
@board
def up17(im):              # 올해 오른 날 17 vs 빠진 날 23 — 점
    d = ImageDraw.Draw(im); TF(d, (W // 2, 120), '올해, 하루 5% 넘게 움직인 날 40번', 84, INK, F_X)
    for row, (lab, n, c) in enumerate((('빠진 날', 23, INK), ('오른 날', PM5 - 23, OR))):
        y = 400 + row * 260; T(d, (330, y), lab, 70, c, F_X, 'rm')
        for i in range(n):
            x = 410 + i * 54
            if c == OR: d.ellipse((x - 20, y - 20, x + 20, y + 20), fill=OR)
            else: d.ellipse((x - 20, y - 20, x + 20, y + 20), outline=INK, width=6)
        T(d, (410 + n * 54 + 30, y), f'{n}', 100, c, F_X, 'lm')
    T(d, (W // 2, 920), '하루에 가장 많이 오른 날 8개 중 5개가 올해', 60, INK, F_X)
    source(d, SRC + ' · 2026.01.02~11.13 · 하루 +5% 이상 17일 · -5% 이하 23일')

@board
def up8(im):               # 상승 상위 8일 표 — 2026 줄만 주황
    d = ImageDraw.Draw(im); T(d, (W // 2, 110), '1995년부터 하루에 가장 많이 오른 날 8', 70, INK, F_X)
    for i, (dd, v) in enumerate(UP8):
        y = 215 + i * 88; c = OR if dd[:4] == '2026' else INK
        T(d, (860, y), ymd(dd), 60, c, F_X, 'rm'); T(d, (1060, y), f'+{v:.2f}%', 64, c, F_X, 'lm')
        if i < 7: d.line([(500, y + 46), (1420, y + 46)], fill=LINE, width=2)
    T(d, (W // 2, 960), '주황 = 올해 (5개)', 50, GREY, F_B)
    source(d, SRC + ' · 전날 종가 대비')

# ── 6. 1천만원 ─────────────────────────────────────────────────────
@board
def split2(im):            # 두 줄 표 — 한 번에 / 열두 번 나눠 · 가장 나빴던 때 · 가운데 · 가장 좋았던 때 · 원금 넘은 편
    d = ImageDraw.Draw(im); TF(d, (W // 2, 120), '1천만원, 묶음 첫날에 넣고 1년 뒤', 80, INK, F_X)
    cols = (700, 1030, 1360, 1690)
    for x, h in zip(cols, ('가장 나빴을 때', '가운데', '가장 좋았을 때', '원금 넘은 편')):
        T(d, (x, 300), h, 44, GREY, F_B)
    for r, (lab, v) in enumerate((('한 번에', ONE), ('열두 번 나눠', SPL))):
        y = 470 + r * 220
        T(d, (480, y), lab, 72, INK, F_X, 'rm')
        for j, x in enumerate(cols):
            s = man(v[j]) if j < 3 else f'{v[3]} / 15'
            T(d, (x, y), s, 72, OR if (j == 1) else INK, F_X)
        d.line([(200, y + 110), (1820, y + 110)], fill=LINE, width=3) if r == 0 else None
    T(d, (W // 2, 930), '나눠 넣은 쪽이 더 많았던 묶음 5 / 15', 58, INK, F_B)
    source(d, '지수 값만 · 배당·보수·세금·수수료 뺌 · 나눠 = 21거래일마다 1/12씩 · 평가는 첫날로부터 1년 뒤 종가 · ECOS')

@board
def scale(im):             # 저울 — 한 번에: 위로도 아래로도 크게 · 나눠서: 덜 벌고 덜 잃음
    d = ImageDraw.Draw(im)
    d.line([(W // 2, 300), (W // 2, 820)], fill=INK, width=10); d.line([(W // 2 - 160, 820), (W // 2 + 160, 820)], fill=INK, width=10)
    d.line([(360, 360), (1560, 360)], fill=INK, width=10)
    for cx in (460, 1460):
        d.line([(cx - 120, 360), (cx - 160, 480)], fill=INK, width=5); d.line([(cx + 120, 360), (cx + 160, 480)], fill=INK, width=5)
        d.arc((cx - 200, 400, cx + 200, 560), 0, 180, fill=INK, width=8)
    T(d, (460, 650), '한 번에', 100, INK, F_X); T(d, (460, 770), '위로도 아래로도 크게', 54, INK, F_B)
    T(d, (1460, 650), '나눠서', 100, INK, F_X); T(d, (1460, 770), '덜 벌고 덜 잃음', 54, INK, F_B)
    T(d, (W // 2, 970), '어느 쪽이 맞다는 게 아니라, 지난 기록이 이렇게 갈렸어요', 54, GREY, F_B)
    source(d, '열다섯 묶음 · 지수 값만 · 계산·비교 자료이며 투자 권유가 아닙니다')

# ── 7. 함정 · 8. 정리 ──────────────────────────────────────────────
@board
def trap1(im):
    d = ImageDraw.Draw(im); T(d, (W // 2, 200), '함정 하나', 70, GREY, F_B)
    T(d, (W // 2, 520), '지수 ≠ 내 계좌', 200, INK, F_X); hand_under(d, 560, 1360, 640, seed=41)
    T(d, (W // 2, 820), 'ETF·펀드는 보수가 빠지고, 배당·세금이 붙거나 빠져요', 58, INK, F_B)
    source(d, '지수 값만 센 숫자')

@board
def trap2(im):
    d = ImageDraw.Draw(im); T(d, (W // 2, 200), '함정 둘', 70, GREY, F_B)
    T(d, (W // 2, 520), '지난 값 ≠ 앞날', 200, INK, F_X); hand_under(d, 560, 1360, 640, seed=42)
    T(d, (W // 2, 820), '열 번 올랐다고 열한 번째도 오른다는 뜻이 아니에요', 58, INK, F_B)
    source(d, SRC)

@board
def summary(im):           # 정리 표 4줄
    d = ImageDraw.Draw(im); T(d, (W // 2, 120), '한 장 정리', 110, INK, F_X)
    rows = (('올해', '하루 5% 넘게 빠진 날 23번 · 31년 합 57번'), ('서킷브레이커', '걸린 날 ≠ 마감으로 크게 빠진 날'),
            ('그 뒤 1년', '더 내려간 적 14/15 · 오른 편 10/15'), ('되찾기', '가운데 8거래일 · 가장 길게 5년 넘게'))
    for i, (a, b) in enumerate(rows):
        y = 300 + i * 160
        T(d, (560, y), a, 58, GREY, F_B, 'rm'); T(d, (600, y), b, 66, OR if i == 0 else INK, F_X, 'lm')
        if i < 3: d.line([(200, y + 80), (1760, y + 80)], fill=LINE, width=2)
    source(d, SRC + ' · 계산·비교 자료이며 투자 권유가 아닙니다')

@board
def ecos(im):              # 한국은행 경제통계시스템 → 코스피 일별 종가 · 내가 산 날 / 오늘
    d = ImageDraw.Draw(im); TF(d, (W // 2, 150), '내 숫자로 직접 보려면', 84, INK, F_X)
    x0, y0, x1, y1 = 300, 290, 1620, 430
    _wobble_rect(d, (x0, y0, x1, y1), INK, 6, seed=5)
    T(d, (x0 + 60, (y0 + y1) // 2), '한국은행 경제통계시스템', 72, INK, F_X, 'lm')
    hand_arrow(d, (W // 2, 460), (W // 2, 560), INK, 7)
    T(d, (W // 2, 630), '코스피 일별 종가', 96, INK, F_X)
    T(d, (W // 2, 840), '내가 산 날  ·  오늘', 120, OR, F_X); hand_under(d, 560, 1360, 920, seed=51)
    source(d, 'ecos.bok.or.kr · 화면은 우리가 다시 그림')

def main(names):
    os.makedirs(OUT, exist_ok=True)
    for n in names or list(B):
        im = canvas(); B[n](im); im.save(os.path.join(OUT, n + '.png')); print(n)

if __name__ == '__main__':
    main(sys.argv[1:])
