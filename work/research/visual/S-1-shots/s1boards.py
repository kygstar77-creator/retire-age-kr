"""S-1 장면 판 — visual-designer 2026-11-15. K-1·H-4·JT-1 판과 같은 꼴·같은 부품(k1boards):
구겨진 종이 바탕 · 펜 빗금 막대(hatch_bar) · 주황 #FF5A00은 그 화면의 답 하나 · 손 동그라미·밑줄 · 사물 그림 obj().
오름 빨강·내림 파랑(한국 시세 표기). 숫자는 ep/S-1 calc_out.txt 표·calc_pre_out.txt·calc_month_1115_out.txt·
raw/daum_005930_daily_1115.json(calc_month_1115.py와 같은 출처)·script.md 자막 값만 — 바꾸지 않음.
shot_plan.md '# 장면 계획'의 bg/s1/board/*.png 줄마다 한 장. 판은 '답이 열린 마지막 모습' — '?' → 열림은 PD가 Remotion에서.
남의 차트·뉴스·증권사·네이버 화면 캡처 0, 삼성 로고·사옥 0. 전자공시 판은 우리가 다시 그린 본뜬 판(캡처 아님).
사용: py -3.12 s1boards.py [이름 ...]   (없으면 전부) → work/video/public/bg/s1/board/<이름>.png
"""
import os, sys, re, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'K-1-shots'))
from k1boards import (W, H, INK, GREY, OR, KRAFT, FADE, F_B, F_M, F_X, canvas, T, TF, source,
                      hand_ellipse, hand_under, hand_check, hand_arrow, hatch_bar, obj)
from PIL import ImageDraw
from k1boards import font as _font

def under(d, xy, s, size, f, seed):
    x0, y0, x1, y1 = d.textbbox(xy, s, font=_font(f, size), anchor='mm')
    hand_under(d, x0, x1, y1 + 14, seed=seed)

def ring(d, xy, s, size, f, seed, ex=0.16, ey=0.30):
    """11/15 17시: 손 동그라미를 글자 실제 폭에 맞춘다 — 고정 상자라 −·+·% 기호에 걸렸음(새 심사관 r02·r09·r10·r12)."""
    x0, y0, x1, y1 = d.textbbox(xy, s, font=_font(f, size), anchor='mm')
    w, h = x1 - x0, y1 - y0
    hand_ellipse(d, (x0 - w * ex - 18, y0 - h * ey - 14, x1 + w * ex + 18, y1 + h * ey + 14), seed=seed)

WORK = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'S-1')
OUT = os.path.join(WORK, 'video', 'public', 'bg', 's1', 'board')
RED = (206, 38, 38); BLUE = (34, 86, 196); LINE = (206, 198, 186)
SRC_DART = '금융감독원 전자공시 삼성전자 영업(잠정)실적 · 주가 KRX 정규장 종가(다음 금융)'

# calc_out.txt '표:' 아래 44줄을 그대로 읽는다(옮겨 적지 않음): 날짜 · 기준일 · 영업이익 · 1년 전 · 발표 날 % · 20거래일 뒤 %
_t = open(os.path.join(EP, 'calc_out.txt'), encoding='utf-8').read().split('표:')[1]
ROWS = []
for ln in _t.strip().splitlines():
    p = ln.split()
    if len(p) == 6 and re.match(r'\d{4}-\d\d-\d\d', p[0]):
        f = lambda s: None if s == 'None' else float(s)
        ROWS.append(dict(date=p[0], op=f(p[2]), prev=f(p[3]), day=f(p[4]), m20=f(p[5])))
assert len(ROWS) == 44, len(ROWS)
RECORD = ['2017-07-07', '2017-10-13', '2018-01-09', '2018-04-06', '2018-10-05',
          '2026-01-08', '2026-04-07', '2026-07-07', '2026-10-08']          # calc_out '사상 최대 … 9번'
BYDATE = {r['date']: r for r in ROWS}
PX = {r['date'][:10]: r['tradePrice'] for r in json.load(open(os.path.join(EP, 'raw', 'daum_005930_daily_1115.json'),
      encoding='utf-8')) if r['accTradeVolume']}

def col(v): return INK if v is None else (RED if v > 0 else BLUE if v < 0 else FADE)

B = {}
def board(fn):
    B[fn.__name__] = fn; return fn

@board
def s1_open107(im):        # 0. 카운터 → 107.4조원 솟는 막대
    d = ImageDraw.Draw(im)
    hatch_bar(im, (250, 330, 520, 900), OR, seed=3); d = ImageDraw.Draw(im)
    d.line([(160, 900), (640, 900)], fill=INK, width=5)
    T(d, (1200, 300), '2026년 10월 8일 발표', 70, GREY, F_B)
    T(d, (1200, 520), '107.4조원', 230, OR, F_X)
    hand_under(d, 720, 1680, 650, seed=4)
    T(d, (1200, 790), '3분기 영업이익(잠정) · 2026.10.8 공시', 56, INK, F_B)
    source(d, SRC_DART)

@board
def s1_100ju(im):          # 0. '내 100주' 조건 카드
    d = ImageDraw.Draw(im)
    TF(d, (W // 2, 150), '100주를 갖고 있었다면', 110, INK, F_X)
    T(d, (560, 420), '10월 7일', 64, GREY, F_B); T(d, (560, 560), '2,685만원', 130, INK, F_X)
    hand_arrow(d, (880, 560), (1040, 560), INK, 8)
    T(d, (1360, 420), '10월 8일', 64, GREY, F_B); T(d, (1360, 560), '2,620만원', 130, INK, F_X)
    T(d, (W // 2, 820), '−65만원', 220, OR, F_X)
    ring(d, (W // 2, 820), '−65만원', 220, F_X, 6, ex=0.22, ey=0.16)
    source(d, '종가 268,500원 → 262,000원 × 100주 · KRX 정규장 종가(다음 금융)')

def record_bars(im, hi=(), labels=True, top=300, base=860):
    d = ImageDraw.Draw(im); vmax = 107.4; bw = 120; gap = 52; x0 = (W - (9 * bw + 8 * gap)) // 2
    for i, dt in enumerate(RECORD):
        r = BYDATE[dt]; x = x0 + i * (bw + gap); h = (base - top) * r['op'] / vmax
        hatch_bar(im, (x, base - h, x + bw, base), INK if dt in hi or not hi else FADE, seed=20 + i)
        d = ImageDraw.Draw(im); c = col(r['day']); cx = x + bw // 2; ay = base - h - 40
        if r['day'] > 0: hand_arrow(d, (cx, ay), (cx, ay - 90), c, 9)
        elif r['day'] < 0: hand_arrow(d, (cx, ay - 90), (cx, ay), c, 9)
        else: d.line([(cx - 34, ay - 45), (cx + 34, ay - 45)], fill=GREY, width=9)
        if labels: T(d, (cx, base + 46), f"{dt[2:4]}.{int(dt[5:7])}", 40, GREY, F_B)
    d.line([(x0 - 40, base), (x0 + 9 * (bw + gap), base)], fill=INK, width=5)
    return d, x0, bw, gap

@board
def s1_nine(im):           # 0. 사상 최대 9번 · 화살표 9개 중 하나만 위
    d, *_ = record_bars(im, labels=False, top=430, base=930)
    T(d, (W // 2, 80), '사상 최대 9번 중', 70, INK, F_B)
    T(d, (W // 2, 210), '오른 날 1번', 160, OR, F_X)
    source(d, SRC_DART + ' · 2011년 이후 잠정 공시 기준')

@board
def s1_nine_grow(im):      # 1. 9개 막대 · 2018.1·2026.7 강조
    d, x0, bw, gap = record_bars(im, hi=('2018-01-09', '2026-07-07'), labels=False, top=330)
    # 11/15 새 심사관 r07 못함: 제목 '14.0→107.4조원'과 강조 막대(8번째 2026.7)가 어긋나 '107.4조=−6.92%'로 읽힘 → 제목에서 107.4 빼고, 강조 막대에 연·월을 붙임
    # 2차(11/15 새 심사관 r07 못함): −6.92% 주황이 '오름'처럼 읽히고 숫자가 화살표 사이에 뜸, '9번 중 1번'이 숫자로 없음
    #   → 숫자를 그 화살표 바로 위에 파랑(내림 색)으로 붙이고, 제목에 '9번 중 오른 날 1번'
    T(d, (W // 2, 120), '사상 최대 9번 중 오른 날 1번', 120, INK, F_X)
    for dt in ('2018-01-09', '2026-07-07'):
        i = RECORD.index(dt); cx = x0 + i * (bw + gap) + bw // 2; r = BYDATE[dt]
        ytop = 860 - (860 - 330) * r['op'] / 107.4 - 40 - 90
        lab = f"{r['day']:+.2f}%".replace('-', '−')
        if dt == '2026-07-07': T(d, (cx - 40, ytop + 45), lab, 72, BLUE, F_X, 'rm')   # 9번째 화살표와 붙지 않게 제 화살표 왼쪽
        else: T(d, (cx, ytop - 50), lab, 60, BLUE, F_X)
        T(d, (cx, 940), f"{dt[:4]}.{int(dt[5:7])}", 46, INK, F_B)
    source(d, SRC_DART + ' · 막대 = 그 분기 영업이익 · 화살표 = 발표 날 등락')

@board
def s1_cal_stamp(im):      # 기초. 9/30 석 달 끝 → 10/8 공시
    d = ImageDraw.Draw(im)
    T(d, (560, 330), '9월 30일', 150, INK, F_X); T(d, (560, 480), '석 달 끝', 80, GREY, F_B)
    hand_arrow(d, (840, 380), (1080, 380), INK, 9)
    T(d, (1360, 330), '10월 8일', 150, OR, F_X); T(d, (1360, 480), '공시', 80, GREY, F_B)
    hand_under(d, 1110, 1610, 560, seed=32)
    TF(d, (W // 2, 780), '약 일주일 뒤 숫자만 먼저', 110, INK, F_X)
    source(d, '금융감독원 전자공시 · 삼성전자 2026년 3분기 영업(잠정)실적(공정공시)')

@board
def s1_dart_mock(im):      # 기초. 공시를 본뜬 판 — 두 칸 + 1년 전·바로 앞 석 달
    d = ImageDraw.Draw(im)
    T(d, (W // 2, 120), '연결재무제표기준영업(잠정)실적', 80, INK, F_X)
    rows = (('매출', '195.0조원', INK), ('영업이익', '107.4조원', OR))
    for i, (a, b, c) in enumerate(rows):
        y = 380 + i * 180
        T(d, (720, y), a, 80, GREY, F_B, 'rm'); T(d, (800, y), b, 150, c, F_X, 'lm')
        d.line([(300, y + 90), (1620, y + 90)], fill=LINE, width=3)
    hand_ellipse(d, (770, 460, 1460, 660), seed=41)
    T(d, (560, 790), '1년 전 같은 석 달 12.17조원', 60, INK, F_B); T(d, (1360, 790), '바로 앞 석 달 89.49조원', 60, INK, F_B)
    T(d, (W // 2, 900), '사업부별 실적  —  나중에', 54, FADE, F_B)
    source(d, '공시를 본떠 다시 그린 판(실제 화면 아님) · 금융감독원 전자공시 삼성전자 2026.10.8 · 연결 기준 잠정')

def grid44(im, key='day', top=330, cw=128, ch=96, gap=14, counts=True, last_grey=False):
    """해(열 11) × 발표 달(1·4·7·10월, 줄 4) 44칸. 칸 색 = 그날(또는 한 달 뒤) 등락 빨강·파랑·회색."""
    d = ImageDraw.Draw(im); years = list(range(2016, 2027)); x0 = (W - (11 * cw + 10 * gap)) // 2
    for r in ROWS:
        yi = years.index(int(r['date'][:4])); qi = (1, 4, 7, 10).index(int(r['date'][5:7]))
        x = x0 + yi * (cw + gap); y = top + qi * (ch + gap); v = r[key]
        c = (FADE if last_grey else INK) if v is None else col(v)
        r0 = min(cw, ch) * 0.42; cx, cy = x + cw / 2, y + ch / 2
        d.ellipse((cx - r0, cy - r0, cx + r0, cy + r0), fill=c)   # 칸 = 점(상자 0, bgcheck ⑥)
    for yi, yr in enumerate(years):
        cx = x0 + yi * (cw + gap) + cw // 2
        T(d, (cx, top - 46), f"'{str(yr)[2:]}", 44, GREY, F_B)
        if counts:
            n = sum(1 for r in ROWS if r['date'].startswith(str(yr)) and (r[key] or 0) > 0)
            T(d, (cx, top + 4 * (ch + gap) + 40), str(n), 56, RED if n else GREY, F_X)
    return d, x0

@board
def s1_grid44(im):         # 2. 44칸 달력판
    d, x0 = grid44(im, top=330)
    TF(d, (W // 2, 150), '오른 날 17 · 내린 날 26', 160, INK, F_X)
    T(d, (x0 - 30, 330 + 4 * 110 + 40), '오른 날', 40, RED, F_B, 'rm')
    source(d, SRC_DART + ' · 2016.1~2026.10 발표 44번 · 그대로 1')

@board
def s1_top5(im):           # 2. 크게 움직인 다섯 날
    d = ImageDraw.Draw(im); T(d, (W // 2, 130), '발표 날 가장 크게 움직인 다섯 번', 80, INK, F_X)
    top5 = sorted(ROWS, key=lambda r: -abs(r['day']))[:5]
    for i, r in enumerate(top5):
        cx = 240 + i * 360
        T(d, (cx, 470), f"{r['day']:+.2f}%", 88, col(r['day']), F_X)
        T(d, (cx, 610), f"{r['date'][:4]}.{int(r['date'][5:7])}", 56, GREY, F_B)
    under(d, (240, 470), f"{top5[0]['day']:+.2f}%", 88, F_X, 51)   # 칸 사이 30px라 동그라미 대신 밑줄
    T(d, (W // 2, 830), '빨강 넷 · 파랑 하나', 150, INK, F_X)
    source(d, SRC_DART + ' · 전날 종가 대비')

def scale(im, l_top, l_big, r_top, r_big, r_or=True, seed=61, mid=True):
    d = ImageDraw.Draw(im)
    obj(im, 'scale', W // 2, 330, 340, rot=0, seed=seed); d = ImageDraw.Draw(im)
    T(d, (480, 560), l_top, 64, GREY, F_B); T(d, (480, 740), l_big, 190, INK, F_X)
    T(d, (1440, 560), r_top, 64, GREY, F_B); T(d, (1440, 740), r_big, 190, OR if r_or else INK, F_X)
    if mid: d.line([(W // 2, 540), (W // 2, 880)], fill=LINE, width=4)
    return d

@board
def s1_scale_day(im):      # 3. 아무 날 vs 발표 날
    d = scale(im, '아무 날 2,634일', '50%', '발표 날 44일', '39%')
    ring(d, (1440, 740), '39%', 190, F_X, 62)
    T(d, (W // 2, 950), '오른 날 비율', 60, INK, F_B)
    source(d, '2016.1.8~2026.10.13 · 50.1% vs 38.6% · KRX 정규장 종가(다음 금융)')

@board
def s1_pre_split(im):      # 3-1. 발표 전 한 달 올라 있던 28번 vs 16번
    d = ImageDraw.Draw(im); TF(d, (W // 2, 140), '발표 전 한 달 올라 있었나', 110, INK, F_X)
    T(d, (500, 380), '올라 있던 28번', 80, INK, F_X); T(d, (500, 560), '내림 18', 190, OR, F_X)
    T(d, (1420, 380), '안 올랐던 16번', 80, INK, F_X); T(d, (1420, 560), '내림 8', 190, BLUE, F_X)
    d.line([(W // 2, 320), (W // 2, 760)], fill=LINE, width=4)
    hand_under(d, 250, 750, 680, seed=71)
    T(d, (W // 2, 880), '발표 날 내린 횟수', 60, GREY, F_B)
    source(d, '발표 전 한 달 = 21거래일 전 종가 → 발표 전날 종가')

def cells(d, x, y, vals, s=52, g=10):
    for i, v in enumerate(vals):
        cx = x + i * (s + g) + s / 2; cy = y + s / 2; d.ellipse((cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2), fill=col(v))

@board
def s1_yoy_rows(im):       # 4. 1년 전보다 늘었다 31 · 줄었다 13
    # 11/15 17시 새 심사관 2명 r12 '못함': 제목(늘었는데 내린)과 큰 예시(줄었는데 오른)가 갈려 요지 둘·범례 없음·어느 점인지 없음·−95.75% 없음
    # → 제목을 대본 4장 끝 문장('늘었는지 줄었는지만 봐서는 … 알 수 없었습니다')으로, 줄 이름표의 '내림·오름·그대로'를 점 색으로 칠해 범례 겸,
    #   2023.4 점에 손 동그라미 + 그 점에서 화살표, 아래 줄에 대본 자막 값(−95.75%)
    d = ImageDraw.Draw(im); TF(d, (W // 2, 130), '늘었는지 줄었는지만 봐서는 알 수 없었다', 84, INK, F_X)
    up = [r for r in ROWS if r['op'] > r['prev']]; dn = [r for r in ROWS if r['op'] <= r['prev']]
    up_s = sorted(up, key=lambda r: r['day']); dn_s = sorted(dn, key=lambda r: r['day'])
    def tally(y, rs):
        x = 900
        for word, n, c in (('내림', sum(r['day'] < 0 for r in rs), BLUE), ('오름', sum(r['day'] > 0 for r in rs), RED),
                           ('그대로', sum(r['day'] == 0 for r in rs), FADE)):
            if not n: continue
            t = f"{word} {n}"; T(d, (x, y), t, 64, c, F_X, 'lm')
            x += d.textlength(t, font=_font(F_X, 64)) + 50
    T(d, (170, 330), '이익 늘었다 31번', 64, INK, F_B, 'lm'); tally(330, up)
    cells(d, 170, 400, [r['day'] for r in up_s[:16]]); cells(d, 170, 470, [r['day'] for r in up_s[16:]])
    T(d, (170, 640), '이익 줄었다 13번', 64, INK, F_B, 'lm'); tally(640, dn)
    cells(d, 170, 710, [r['day'] for r in dn_s])
    r = BYDATE['2023-04-07']; k = dn_s.index(r); cx = 170 + k * 62 + 26
    hand_ellipse(d, (cx - 32, 736 - 32, cx + 32, 736 + 32), width=6, seed=82)
    hand_arrow(d, (cx + 50, 760), (1220, 840), GREY, 6)
    T(d, (1860, 850), f"{r['day']:+.2f}%", 170, RED, F_X, 'rm')
    T(d, (1860, 975), f"2023.4.7 · 이익 {r['prev']:.2f}조 → {r['op']:.1f}조원 (−{abs(r['op'] / r['prev'] - 1) * 100:.2f}%)", 42, INK, F_B, 'rm')
    source(d, SRC_DART)

@board
def s1_scale_month(im):    # 5. 한 달 뒤 — 저울 수평
    # 11/15 17시: 58.1%만 주황이면 '차이'로 읽힘(새 심사관 r13) → 두 숫자 같은 먹색, 답 '같다'는 가운데 주황 손 '=' 하나
    d = scale(im, '아무 날 → 4주 뒤', '58.2%', '발표 → 4주 뒤', '58.1%', r_or=False, seed=91, mid=False)
    hand_under(d, W // 2 - 70, W // 2 + 70, 712, seed=92); hand_under(d, W // 2 - 70, W // 2 + 70, 762, seed=93)
    T(d, (W // 2, 950), '한 달 뒤 오른 비율 · 2,615번 vs 43번', 56, INK, F_B)
    source(d, '20거래일 뒤 종가 ÷ 발표 전날 종가 · 이번(2026.10) 발표는 6장에서')

@board
def s1_100ju_two(im):      # 5. 4월·7월 100주 하루 vs 한 달
    d = ImageDraw.Draw(im); TF(d, (W // 2, 140), '100주라면, 하루 vs 한 달', 140, INK, F_X)
    for cx, mon, a, b in ((480, '2026년 4월 발표', '+34만원', '+784만원'), (1440, '2026년 7월 발표', '−220만원', '−720만원')):
        T(d, (cx, 320), mon, 64, GREY, F_B)
        T(d, (cx, 470), '하루 ' + a, 90, RED if a[0] == '+' else BLUE, F_X)
        T(d, (cx, 680), '한 달 ' + b, 112, RED if b[0] == '+' else BLUE, F_X)
    d.line([(W // 2, 280), (W // 2, 820)], fill=LINE, width=4)
    source(d, '발표 전날 종가 기준 · 한 달 = 20거래일 뒤 종가 · KRX 정규장(다음 금융)')

@board
def s1_after108(im):       # 6. 10/7 → 11/6 일별 종가 선
    d = ImageDraw.Draw(im)
    days = sorted(k for k in PX if '2026-10-07' <= k <= '2026-11-06')
    assert days[0] == '2026-10-07' and days[-1] == '2026-11-06' and len(days) == 22, days   # 전날+발표 날+20거래일
    x0, x1, y0, y1 = 220, 1300, 330, 880; vmax, vmin = 280000, 180000
    pt = lambda i, v: (x0 + (x1 - x0) * i / (len(days) - 1), y0 + (y1 - y0) * (vmax - v) / (vmax - vmin))
    pts = [pt(i, PX[k]) for i, k in enumerate(days)]
    d.line(pts, fill=INK, width=7, joint='curve')
    for i in range(1, len(days)):
        x = pts[i][0]; d.line([(x, y1 + 20), (x, y1 + 38)], fill=GREY, width=3)
    for k, lab in (('2026-10-07', '10/7 268,500'), ('2026-10-13', '10/13 232,000')):
        x, y = pts[days.index(k)]; d.ellipse((x - 12, y - 12, x + 12, y + 12), fill=INK)
        T(d, (x + 24, y - 40), lab, 44, GREY, F_B, 'lm')
    x, y = pts[-1]; d.ellipse((x - 16, y - 16, x + 16, y + 16), fill=OR)
    T(d, (x0, y1 + 80), '20거래일', 40, GREY, F_B, 'lm')
    T(d, (1600, 330), '11월 6일', 70, GREY, F_B); T(d, (1600, 470), '188,700원', 104, OR, F_X)
    T(d, (1600, 640), '100주', 60, GREY, F_B); T(d, (1600, 760), '−798만원', 104, BLUE, F_X)
    hand_ellipse(d, (x - 60, y - 60, x + 60, y + 60), seed=111)
    T(d, (W // 2, 150), '발표 전날보다 −29.72%', 140, INK, F_X)
    source(d, 'KRX 정규장 종가(다음 금융) · 2,685만원 → 1,887만원')

@board
def s1_howto(im):          # 7. 다음 발표 날 확인 순서 — 본뜬 판
    d = ImageDraw.Draw(im); T(d, (W // 2, 110), '전자공시(다트)에서 이 순서로', 90, INK, F_X)
    T(d, (300, 300), '①', 90, OR, F_X); T(d, (400, 300), '삼성전자', 110, INK, F_X, 'lm')
    hand_under(d, 390, 900, 370, INK, seed=121)
    T(d, (300, 500), '②', 90, OR, F_X); T(d, (400, 500), '영업(잠정)실적', 100, INK, F_X, 'lm')
    T(d, (300, 700), '③', 90, OR, F_X); T(d, (400, 700), '이번 · 1년 전 · 바로 앞 석 달', 76, INK, F_B, 'lm')
    T(d, (1560, 470), '다음 발표', 70, GREY, F_B); T(d, (1560, 640), '?', 220, OR, F_X)
    hand_ellipse(d, (1400, 520, 1720, 760), seed=122)
    T(d, (W // 2, 900), '발표 날 오른 건 열 번에 네 번꼴', 64, INK, F_B)
    source(d, '공시 화면을 본떠 다시 그린 판 · 실제 화면 아님 · dart.fss.or.kr')

@board
def s1_limits(im):         # 8. 한계 세 가지
    d = ImageDraw.Draw(im); TF(d, (W // 2, 140), '이 숫자로 말할 수 없는 것', 120, INK, F_X)
    rows = ('오른 날이 적었던 이유 — 공시에 없음', '삼성전자 한 회사의 기록', '지난 기록이 앞날을 보장하지 않음')
    for i, s in enumerate(rows):
        y = 380 + i * 200
        T(d, (250, y), '?', 120, OR if i == 0 else INK, F_X); T(d, (360, y), s, 84, INK, F_X, 'lm')
        if i < 2: d.line([(220, y + 100), (1700, y + 100)], fill=LINE, width=2)
    source(d, '발표 날 하루 통째로 셈 · 장 마감 가격끼리 비교 · 하루 안 흔들림 폭은 담기지 않음')

@board
def s1_summary(im):        # 9. 정리 세 줄
    d = ImageDraw.Draw(im); T(d, (W // 2, 140), '한 장 정리', 130, INK, F_X)
    rows = (('사상 최대 9번', '그날 오름 1'), ('발표 날 44번', '오름 39% vs 아무 날 50%'), ('한 달 뒤', '발표 58% vs 아무 날 58%'))
    for i, (a, b) in enumerate(rows):
        y = 380 + i * 200
        T(d, (720, y), a, 70, GREY, F_B, 'rm'); T(d, (780, y), b, 90, OR if i == 1 else INK, F_X, 'lm')
        if i < 2: d.line([(240, y + 100), (1700, y + 100)], fill=LINE, width=2)
    hand_check(d, 180, 580, 56)
    source(d, SRC_DART + ' · 2016.1~2026.10 · 44번 전체 표는 파이어맵 카페')

def main(names):
    os.makedirs(OUT, exist_ok=True)
    for n in names or list(B):
        im = canvas(); B[n](im); im.save(os.path.join(OUT, n + '.png')); print(n)

if __name__ == '__main__':
    main(sys.argv[1:])
