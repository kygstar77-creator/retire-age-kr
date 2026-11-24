"""SQ-1 장면 판 — visual-designer 2026-11-23. H-6·KOSPI-1 판과 같은 꼴·같은 부품(k1boards):
구겨진 종이 바탕 · 펜 빗금 막대(hatch_bar) · 주황 #FF5A00은 그 화면의 답 하나 · 손 동그라미·밑줄 · 상자·카드 판 없음.
숫자는 ep/SQ-1 calc_mix_out_1112·calc_krw_out_1120·calc_tax_out_1121b 출력을 그대로 읽고 assert(옮겨 적지 않음),
법·보수 숫자는 script.md v1.6 자막 줄과 글자 그대로 대조.
판은 '답이 열린 마지막 모습' — '?' → 열림은 PD가 Remotion에서. 파일 이름은 shot_plan.md가 나오면 그 '파일' 칸에 이 이름을 적는다.
11/23 1차: 달·월별 줄이 필요 없는 13장. 남은 4장(15년→5년 선 그래프·매달 100만원 막대·환율 선·골짜기 둘)은 월말 값 시리즈를 calc에서 뽑아 다음 회차.
사용: py -3.12 sq1boards.py [이름 ...]   (없으면 전부) → work/video/public/bg/sq1/board/<이름>.png
"""
import os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'K-1-shots'))
from k1boards import (W, H, INK, GREY, OR, FADE, KRAFT, F_B, F_M, F_X, font, canvas, T, TF, source, obj,
                      hand_ellipse, hand_under, hand_check, hand_arrow, hatch_bar, bars, linechart)
from PIL import Image, ImageDraw, ImageFilter

sys.stdout.reconfigure(encoding='utf-8')
WORK = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'SQ-1')
OUT = os.path.join(WORK, 'video', 'public', 'bg', 'sq1', 'board')
LINE = (206, 198, 186)
rd = lambda fn: open(os.path.join(EP, fn), encoding='utf-8').read()
_mix, _krw, _tax, _sc = rd('calc_mix_out_1112.txt'), rd('calc_krw_out_1120.txt'), rd('calc_tax_out_1121b.txt'), rd('script.md')

# ── calc 출력에서 그대로 읽기 ─────────────────────────────────────────
MIX = {int(p): dict(end=float(e), cagr=float(c), mdd=float(m), y22=float(y)) for p, e, c, m, y in
       re.findall(r'^\s*(\d+)%\s+([\d.]+)억\s+([\d.]+)%\s+(-[\d.]+)%\s+(-?[\d.]+)%', _mix, re.M)}
assert sorted(MIX) == [0, 30, 50, 70, 100]
assert [MIX[p]['end'] for p in (100, 50, 0)] == [6.77, 10.10, 13.56]
assert [MIX[p]['y22'] for p in (100, 50, 0)] == [-3.3, -18.2, -32.6]
assert MIX[70]['end'] == 8.72 and MIX[30]['end'] == 11.50 and MIX[100]['cagr'] == 13.60 and MIX[0]['mdd'] == -32.6
_d = re.search(r'SCHD 100% (\d+)만원 · 50% (\d+)만원 · QQQ 100% (\d+)만원', _mix)
DIST = tuple(int(x) for x in _d.groups()); assert DIST == (295, 170, 45)
assert 'SCHD 1.0541$ / 10월말 35.78$ = 2.95%' in _mix and 'QQQ 3.0918$ / 690.49$ = 0.45%' in _mix
R5 = {int(p): float(v) for p, v in re.findall(r'SCHD (\d+)%: 1억→([\d.]+)억 연 [\d.]+% 최대낙폭', _mix.split('최근 5년')[1])}
assert R5 == {100: 1.66, 50: 1.82, 0: 1.84}
KRW15 = {int(p): float(v) for p, v in re.findall(r'SCHD\s+(\d+)%: 달러 1억→[\d.]+억 · 원화 1억→([\d.]+)억', _krw.split('최근 10년')[0])}
assert KRW15 == {100: 8.18, 50: 12.21, 0: 16.39}

def _taxsec(span):
    return _tax.split(f'■ {span}', 1)[1].split('\n■ ', 1)[0]
def _aftertax(span, pct):
    blk = _taxsec(span).split(f'SCHD {pct:>3}% (QQQ', 1)[1] if pct != 100 else _taxsec(span).split('SCHD 100% (QQQ', 1)[1]
    line0 = [l for l in blk.split('\n') if '[다른 소득 0]' in l][0]
    a = float(re.search(r'직투 세후 ([\d.]+)억', line0)[1]); b = float(re.search(r'국내 상장 세후 ([\d.]+)억', line0)[1])
    return a, b
TAX15 = _aftertax('15년', 100); assert TAX15 == (6.47, 5.61)
TAX15Q = _aftertax('15년', 0); assert TAX15Q == (12.87, 9.62)
TAX5 = _aftertax('최근 5년', 100); assert TAX5 == (1.70, 1.74)
for s in ('직투 1.70억 vs 국내 상장 1.74억(−366만원)', '총보수 SCHD 0.060%', 'QQQ 0.18%(Invesco)', '한 회사 24% 넘으면 20%로',
          '한 종목 4%·한 업종 25% 상한', '매년 3월 정기 교체', '원천징수 15.4%(14%+지방 1.4%)', '기본공제 연 250만원',
          '이자·배당 합 연 2,000만원 넘으면 종합과세', '다음 해 5월 종합소득세 확정신고(소득세법 제70조)', '2022년 한 해 SCHD −3.3%'):
    assert s in _sc, s
SRC_MIX = '야후 파이낸스 수정 종가 · 2011-10월 말 → 2026-10월 말 · 달러 기준 · 분배 재투자 · 매년 10월 말 비율 맞춤'
NAMES = ('SCHD만', '반반', '나스닥100만')
def eok(v): return f'{v:.2f}억'.replace('.00억', '억')

B = {}
def board(fn):
    B[fn.__name__] = fn; return fn

# ── 0. 여는 말 ───────────────────────────────────────────────────────
@board
def sq1_open3(im):          # 'SCHD만 ?' · '반반 ?' · '나스닥100만 ?' 열린 모습 — 답(주황)은 이 편의 주제 '반반'
    d = ImageDraw.Draw(im); TF(d, (W // 2, 120), '2011년에 1억, 15년 뒤', 96, INK, F_X)
    v = [MIX[100]['end'], MIX[50]['end'], MIX[0]['end']]
    bars(im, [(NAMES[0], v[0], KRAFT, eok(v[0]), INK), (NAMES[1], v[1], OR, eok(v[1]), OR), (NAMES[2], v[2], KRAFT, eok(v[2]), INK)],
         top_y=360, bw=260, gap=230, nsize=120, seed=21)
    source(d, SRC_MIX + ' · 세금·환율 뺌 안 함')

# ── 1. 나스닥100 ────────────────────────────────────────────────────
@board
def sq1_cal12(im):          # 달력 한 장 — 12월 주황 동그라미
    d = ImageDraw.Draw(im); TF(d, (W // 2, 130), '나스닥100 명단', 100, INK, F_X)
    x0, y0, cw, ch = 360, 300, 300, 170
    for i in range(12):
        r, c = divmod(i, 4); cx, cy = x0 + c * cw + cw // 2, y0 + r * ch + ch // 2
        T(d, (cx, cy), f'{i + 1}월', 78 if i == 11 else 64, OR if i == 11 else GREY, F_X if i == 11 else F_B)
    cx, cy = x0 + 3 * cw + cw // 2, y0 + 2 * ch + ch // 2
    hand_ellipse(d, (cx - 130, cy - 72, cx + 130, cy + 72), seed=12)
    T(d, (W // 2, 900), '해마다 12월에 한 번 바뀐다', 84, INK, F_X)
    source(d, 'Nasdaq-100 지수 방법론(Nasdaq 공식, 2026년판)')

@board
def sq1_cap20(im):          # 막대 하나가 선에 걸려 잘림 — 24% 넘으면 20%로
    d = ImageDraw.Draw(im); TF(d, (W // 2, 120), '한 회사가 너무 커지면', 96, INK, F_X)
    base, top = 900, 260; s = (base - top) / 30
    y24, y20 = base - 24 * s, base - 20 * s
    xa = 520; hatch_bar(im, (xa, y24 - 70, xa + 260, base), FADE, seed=31)          # 잘리기 전(옅게, 선 위로 넘침)
    d = ImageDraw.Draw(im)
    xb = 1140; hatch_bar(im, (xb, y20, xb + 260, base), OR, seed=32); d = ImageDraw.Draw(im)
    for y, lab in ((y24, '24%'), (y20, '20%')):
        xx = 380
        while xx < 1560: d.line([(xx, y), (min(xx + 24, 1560), y)], fill=GREY, width=4); xx += 40
        T(d, (1580, y), lab, 52, OR if lab == '20%' else GREY, F_X, 'lm')
    T(d, (xa + 130, base + 60), '넘으면', 50); T(d, (xb + 130, base + 60), '줄인다', 50, OR, F_X)
    hand_arrow(d, (xa + 300, y24 - 30), (xb - 40, y20 + 30), INK, 6)
    source(d, 'Nasdaq-100 지수 방법론 · 4.5% 넘는 회사들 합이 48% 넘으면 40%로')

# ── 2. SCHD ─────────────────────────────────────────────────────────
@board
def sq1_sieve4(im):         # 체 넷 → 100곳
    d = ImageDraw.Draw(im); TF(d, (W // 2, 110), 'SCHD는 네 가지 점수로 줄 세운다', 88, INK, F_X)
    items = ('빚에 비해 버는 현금', '가진 돈으로 내는 이익', '배당률', '5년 배당 늘린 속도')
    for i, s in enumerate(items):
        y = 270 + i * 130
        T(d, (560, y), f'{i + 1}', 74, OR, F_X); T(d, (640, y), s, 66, INK, F_B, 'lm')
        if i < 3: d.line([(520, y + 65), (1500, y + 65)], fill=LINE, width=2)
    hand_arrow(d, (W // 2, 760), (W // 2, 830), INK, 7)
    T(d, (W // 2, 905), '위에서부터 100곳', 92, OR, F_X)
    hand_under(d, W // 2 - 330, W // 2 + 330, 965, seed=41)
    source(d, 'S&P 다우존스 Dow Jones U.S. Dividend 100 지수 방법론(2026년 9월판) · 한 종목 4%·한 업종 25% 상한 · 매년 3월 교체')

@board
def sq1_fee2(im):           # 보수 0.06% / 0.18% · 1억이면 6만원 / 18만원
    d = ImageDraw.Draw(im); TF(d, (W // 2, 130), '운용 보수, 1억이면 한 해', 96, INK, F_X)
    for x, nm, p, won, col in ((560, 'SCHD', '0.06%', '6만원', OR), (1360, 'QQQ', '0.18%', '18만원', INK)):
        T(d, (x, 340), nm, 84, INK, F_X); T(d, (x, 480), p, 72, GREY, F_B); T(d, (x, 690), won, 170, col, F_X)
    assert round(1e8 * 0.0006) == 60000 and round(1e8 * 0.0018) == 180000
    d.line([(W // 2, 300), (W // 2, 800)], fill=LINE, width=3)
    hand_ellipse(d, (560 - 260, 600, 560 + 260, 790), seed=51)
    source(d, '총보수 SCHD 0.060%(Schwab, 2026-11-13) · QQQ 0.18%(Invesco) · 1억 × 보수 단순 계산, 세전')

# ── 3. 섞는 비율 ────────────────────────────────────────────────────
@board
def sq1_mix5(im):           # 다섯 줄 표 — 끝값·한 해 평균·가장 크게 빠진 폭
    d = ImageDraw.Draw(im); TF(d, (W // 2, 100), '섞는 비율별 15년 (1억 넣었다면)', 84, INK, F_X)
    cx = (420, 900, 1280, 1640)
    for x, h in zip(cx, ('SCHD 비율', '15년 뒤', '한 해 평균', '가장 크게 빠짐')): T(d, (x, 230), h, 46, GREY)
    d.line([(200, 275), (1780, 275)], fill=INK, width=4)
    for i, p in enumerate((100, 70, 50, 30, 0)):
        y = 350 + i * 128; m = MIX[p]; hi = p == 50
        col = OR if hi else INK
        T(d, (cx[0], y), f'{p}%', 70, col, F_X); T(d, (cx[1], y), eok(m['end']), 76, col, F_X)
        T(d, (cx[2], y), f"{m['cagr']:.1f}%", 62, col, F_B); T(d, (cx[3], y), f"{m['mdd']:.1f}%".replace('-', '−'), 62, col, F_B)
        if i < 4: d.line([(200, y + 64), (1780, y + 64)], fill=LINE, width=2)
    hand_ellipse(d, (130, 350 + 2 * 128 - 70, 1850, 350 + 2 * 128 + 70), seed=61)
    source(d, SRC_MIX + ' · 0% = 나스닥100(QQQ)만')

@board
def sq1_y2022(im):          # 2022년 막대 셋 아래로
    d = ImageDraw.Draw(im); TF(d, (W // 2, 120), '2022년 한 해', 104, INK, F_X)
    v = [MIX[100]['y22'], MIX[50]['y22'], MIX[0]['y22']]
    top, bw, gap = 300, 260, 230; tot = 3 * bw + 2 * gap; x = (W - tot) // 2; s = 520 / 35
    d.line([(x - 80, top), (x + tot + 80, top)], fill=INK, width=4)
    for i, (nm, val) in enumerate(zip(NAMES, v)):
        y1 = top + (-val) * s; col = OR if i == 0 else KRAFT
        hatch_bar(im, (x, top, x + bw, y1), col, seed=70 + i); d = ImageDraw.Draw(im)
        T(d, (x + bw // 2, top - 60), nm, 54)
        T(d, (x + bw // 2, y1 + 80), f'{round(val):d}%'.replace('-', '−'), 110, OR if i == 0 else INK, F_X)
        x += bw + gap
    source(d, '2022년 한 해 SCHD −3.3% · 반반 −18.2% · 나스닥100(QQQ) −32.6% · 월말 값 · 야후 파이낸스 · calc_mix')

# ── 5. 매달 들어오는 돈 ─────────────────────────────────────────────
@board
def sq1_dist3(im):          # 1억이면 한 해 세전 295만 · 170만 · 45만
    d = ImageDraw.Draw(im); TF(d, (W // 2, 120), '1억이면 한 해 분배금 (세전)', 96, INK, F_X)
    bars(im, [(NAMES[0], DIST[0], OR, f'{DIST[0]}만', OR), (NAMES[1], DIST[1], KRAFT, f'{DIST[1]}만', INK), (NAMES[2], DIST[2], KRAFT, f'{DIST[2]}만', INK)],
         top_y=380, bw=260, gap=230, nsize=120, seed=81)
    source(d, '최근 분배 4회 합 ÷ 2026-10월 말 값 · SCHD 2.95%(Schwab) · QQQ 0.45%(Nasdaq·야후) · 환율 고정')

# ── 6. 세금 ─────────────────────────────────────────────────────────
@board
def sq1_tax2way(im):        # 두 갈래 표
    d = ImageDraw.Draw(im); TF(d, (W // 2, 110), '같은 지수, 세금 매기는 법이 다르다', 88, INK, F_X)
    cols = ((520, '미국 상품 직접', ('판 차익에 22%', '한 해 250만원 빼고', '다른 소득과 안 합침')),
            (1400, '국내 상장 해외 ETF', ('분배도 차익도 15.4%', '배당소득으로 침', '한 해 2천만원 넘으면 합침')))
    for x, h, rows in cols:
        T(d, (x, 270), h, 66, INK, F_X); hand_under(d, x - 300, x + 300, 320, INK, 6, seed=x)
        for i, r in enumerate(rows):
            T(d, (x, 440 + i * 150), r, 60, OR if (x == 1400 and i == 2) else INK, F_X if i == 0 else F_B)
    d.line([(W // 2 + 20, 250), (W // 2 + 20, 900)], fill=LINE, width=3)
    source(d, '소득세법 제4조·제14조·제17조·제94조·제103조·제104조·시행령 제26조의2 · 지방세법 제103조의3 · 법제처')

@board
def sq1_tax15(im):          # SCHD 1억 15년 한 번에 팔았다면 세후 — 직투 6.5억 / 국내 상장 5.6억
    d = ImageDraw.Draw(im); TF(d, (W // 2, 110), 'SCHD 1억 15년, 한 번에 팔았다면 세후', 84, INK, F_X)
    a, b = TAX15
    bars(im, [('직접 산 미국 상품', a, OR, f'{a:.1f}억', OR), ('국내 상장', b, KRAFT, f'{b:.1f}억', INK)],
         top_y=360, bw=300, gap=420, nsize=130, seed=91)
    source(d, '원화·세후 · 다른 소득 0 · 국내 상장 상품도 같은 지수로 움직였다고 봄 · 현행 세법을 모든 해에 적용 · calc_tax')

@board
def sq1_tax5(im):           # 5년이면 국내 상장이 조금 더 — +366만원
    d = ImageDraw.Draw(im); TF(d, (W // 2, 95), '5년만 들고 있었다면 (세후)', 88, INK, F_X)
    a, b = TAX5; assert round((b - a) * 1e4) in range(350, 450)   # 억 둘째 자리 반올림 값 — 정확한 차이는 자막 '−366만원'
    bars(im, [('직접 산 미국 상품', a, KRAFT, f'{a:.2f}억', INK), ('국내 상장', b, OR, f'{b:.2f}억', OR)],
         top_y=380, bw=300, gap=420, nsize=120, seed=95, vmax=2.0)
    d = ImageDraw.Draw(im); T(d, (W // 2, 190), '국내 상장이 366만원 더 남음', 64, OR, F_X)
    source(d, '원화·세후 SCHD 100% · 다른 소득 0 · 2021-10월 말 → 2026-10월 말 · 다른 소득 5천만원이면 직접 산 쪽이 +257만원 · calc_tax')

# ── 7. 함정 ─────────────────────────────────────────────────────────
@board
def sq1_traps3(im):         # 함정 셋
    d = ImageDraw.Draw(im); T(d, (W // 2, 130), '걸리기 쉬운 함정 셋', 120, INK, F_X)
    rows = (('하나', '지난 값을 앞날로 읽기'), ('둘', '이름만 보고 고르기'), ('셋', '국내 상장을 한 해에 다 팔기'))
    for i, (n, s) in enumerate(rows):
        y = 380 + i * 200
        T(d, (520, y), n, 80, OR, F_X); T(d, (640, y), s, 80, INK, F_X, 'lm')
        if i < 2: d.line([(420, y + 100), (1600, y + 100)], fill=LINE, width=2)
    source(d, "예 — 'QQQ+SCHD'라는 말로 소개된 상품 가운데 나스닥100 커버드콜 ETF가 있었음 · 투자설명서 '기초지수' 확인")

# ── 8. 끝 ───────────────────────────────────────────────────────────
@board
def sq1_summary(im):        # 정리 표
    d = ImageDraw.Draw(im); T(d, (W // 2, 100), '한 장 정리', 110, INK, F_X)
    cx = (520, 940, 1240, 1560)
    for x, h in zip(cx[1:], NAMES): T(d, (x, 230), h, 52, GREY)
    d.line([(200, 275), (1780, 275)], fill=INK, width=4)
    rows = (('15년 1억', [eok(MIX[p]['end']) for p in (100, 50, 0)]),
            ('최근 5년 1억', [f'{path(w, (2021, 10))[-1][1]:.3f}억' for w in (1.0, 0.5, 0.0)]),   # 11/24 셋째 자리 — 1.82·1.84로는 차이가 200만원으로 보임(심사관)
            ('2022년 한 해', [f"{round(MIX[p]['y22'])}%".replace('-', '−') for p in (100, 50, 0)]),
            ('한 해 분배금(1억·세전)', [f'{x}만원' for x in DIST]))
    for i, (k, vals) in enumerate(rows):
        y = 360 + i * 140
        T(d, (cx[0], y), k, 54, INK, F_B, 'rm')
        for j, v in enumerate(vals): T(d, (cx[j + 1], y), v, 70, INK, F_X)   # 11/24 loop: 반반 칸 주황 뺌(값이 더 큰 나스닥100과 헷갈림)
        if i == 1:   # 5년 줄 옆 주황 작은 글 — 차이는 월말 경로로 다시 계산(sq1_line5와 같은 식)
            gap = round((path(0.0, (2021, 10))[-1][1] - path(0.5, (2021, 10))[-1][1]) * 1e4); assert gap == 263, gap
            T(d, ((cx[2] + cx[3]) // 2, y + 62), f'반반과 나스닥100만, 차이 약 {gap}만원', 40, OR, F_B)   # 두 칸 사이 아래(sq1_line5와 같은 말) — 심사관 2: 주어 없으면 무엇과의 차이인지 모름
        d.line([(200, y + (88 if i == 1 else 70)), (1780, y + (88 if i == 1 else 70))], fill=LINE, width=2)
    y = 360 + 4 * 140
    T(d, (cx[0], y), 'SCHD만 · 15년 세후', 54, INK, F_B, 'rm')
    T(d, (cx[1], y - 28), f'직접 {TAX15[0]:.1f}억', 46, INK, F_X); T(d, (cx[1], y + 30), f'국내 상장 {TAX15[1]:.1f}억', 46, INK, F_X)   # SCHD 칸 아래만(심사관: 세 칸에 걸치면 남의 값으로 읽힘)
    for x in cx[2:]: T(d, (x, y), '—', 60, GREY, F_B)
    source(d, '야후 파이낸스·Schwab·Invesco·한국은행·법제처 · 계산·비교 자료이며 매수·매도 권유가 아닙니다')

# ── 11/24 남은 4장: 월말 시리즈는 calc_mix·calc_dca·calc_krw를 그 폴더에서 불러 같은 식으로 다시 돌리고, 끝값을 calc 출력과 assert ──
def _calcs():
    import io, contextlib, importlib
    cwd = os.getcwd(); os.chdir(EP); sys.path.insert(0, EP)
    try:
        with open(os.devnull, 'w', encoding='utf-8') as _nul, contextlib.redirect_stdout(_nul):
            cm = importlib.import_module('calc_mix'); cd = importlib.import_module('calc_dca'); ck = importlib.import_module('calc_krw')
    finally:
        os.chdir(cwd)
    return cm, cd, ck
CM, CD, CK = _calcs()

def path(w, start=(2011, 10), end=(2026, 10)):
    """calc_mix.run과 같은 걸음(월말·매년 10월 말 비율 맞춤) — 달마다 평가액(1억=1.0)."""
    ms = [m for m in CM.months if start <= m <= end]; a, b = w, 1 - w; out = [(ms[0], 1.0)]
    for p, m in zip(ms, ms[1:]):
        a *= CM.S[m] / CM.S[p]; b *= CM.Q[m] / CM.Q[p]; v = a + b; out.append((m, v))
        if m[1] == 10: a, b = v * w, v * (1 - w)
    assert abs(out[-1][1] - CM.run(w, start, end)[0]) < 1e-9
    return out

def ddown(vals):
    pk = vals[0]; r = []
    for v in vals: pk = max(pk, v); r.append(v / pk - 1)
    return r

@board
def sq1_line5(im):          # 15년 선 셋(왼쪽 작게) → 마지막 5년 잘라 크게(오른쪽) · 반반과 나스닥100만 거의 겹침
    d = ImageDraw.Draw(im); TF(d, (W // 2, 95), '5년 전에 넣었다면', 100, INK, F_X)
    L = {w: path(w) for w in (1.0, 0.5, 0.0)}
    assert [round(L[w][-1][1], 2) for w in (1.0, 0.5, 0.0)] == [MIX[100]['end'], MIX[50]['end'], MIX[0]['end']]
    R = {w: path(w, (2021, 10)) for w in (1.0, 0.5, 0.0)}
    assert [round(R[w][-1][1], 2) for w in (1.0, 0.5, 0.0)] == [R5[100], R5[50], R5[0]]
    gap_man = round((R[0.0][-1][1] - R[0.5][-1][1]) * 1e4); assert gap_man in range(255, 272), gap_man   # 자막 '약 263만원'
    bx = (170, 300, 720, 760)
    ser = [[v for _, v in L[w]] for w in (1.0, 0.5, 0.0)]
    n = len(ser[0]); i5 = [m for m, _ in L[1.0]].index((2021, 10))
    X, Y = linechart(im, ser, bx, 0, 16, [KRAFT, INK, GREY], [4, 5, 4], [(0, '2011'), (n - 1, '2026')], yfmt='{:.0f}억', yticks=(1, 8, 16))
    d = ImageDraw.Draw(im)
    xx = X(i5); yy = bx[1]
    while yy < bx[3]: d.line([(xx, yy), (xx, min(yy + 20, bx[3]))], fill=OR, width=4); yy += 34
    T(d, ((X(i5) + bx[2]) // 2, bx[1] - 34), '마지막 5년', 40, OR, F_B)
    T(d, ((bx[0] + bx[2]) // 2, 840), '15년', 56, GREY, F_B)
    hand_arrow(d, (bx[2] + 50, 530), (bx[2] + 190, 530), INK, 7)
    bx2 = (960, 260, 1420, 860)
    ser2 = [[v for _, v in R[w]] for w in (1.0, 0.5, 0.0)]; n2 = len(ser2[0])
    X2, Y2 = linechart(im, ser2, bx2, 0.6, 2.0, [KRAFT, OR, INK], [6, 9, 6], [(0, '2021.10'), (n2 - 1, '2026.10')], yfmt='{:.0f}억', yticks=(1, 2))
    d = ImageDraw.Draw(im)
    e1, e5, e0 = R[1.0][-1][1], R[0.5][-1][1], R[0.0][-1][1]
    yl = Y2(e5)   # 이름 셋은 끝점 옆에 70px 간격으로(겹침 방지) — 위 나스닥100만 · 가운데 반반 · 아래 SCHD만
    for (v, nm, col, f, sz), yy in zip(((e0, NAMES[2], INK, F_B, 44), (e5, NAMES[1], OR, F_X, 52), (e1, NAMES[0], INK, F_B, 44)), (yl - 80, yl, yl + 80)):
        T(d, (bx2[2] + 30, yy), f'{nm} {v:.2f}억', sz, col, f, 'lm')
    T(d, ((bx2[0] + bx2[2]) // 2 + 100, 960), '반반과 나스닥100만, 차이 약 263만원', 60, INK, F_X)
    source(d, '2011-10월 말(왼쪽)·2021-10월 말(오른쪽) → 2026-10월 말 · 1억 · 달러 기준 · 분배 재투자 · 매년 10월 말 비율 맞춤 · 야후 파이낸스 · calc_mix')

@board
def sq1_dca(im):            # 매달 100만원 × 180번 → 끝값 셋
    d = ImageDraw.Draw(im); TF(d, (W // 2, 95), '매달 100만원씩 15년 (180번)', 92, INK, F_X)
    res = {w: CD.dca(w, (2011, 10)) for w in (1.0, 0.5, 0.0)}
    assert all(abs(res[w][1] - 180) < 1e-9 for w in res)
    v = {w: round(res[w][0] / 100, 2) for w in res}; assert [v[1.0], v[0.5], v[0.0]] == [5.34, 7.14, 8.81], v
    import random; rnd = random.Random(180)
    x0, y0 = 316, 205
    for k in range(180):
        yr, mo = divmod(k, 12); x = x0 + yr * 86 + mo * 6.2; j = rnd.uniform(-2, 2)
        d.line([(x + j, y0), (x - j, y0 + 44)], fill=GREY, width=3)
    T(d, (W // 2, 300), '넣은 돈 모두 1억 8천만원', 50, GREY, F_B)
    bars(im, [('넣은 돈', 1.8, FADE, '1.8억', GREY), (NAMES[0], v[1.0], KRAFT, eok(v[1.0]), INK),
              (NAMES[1], v[0.5], KRAFT, eok(v[0.5]), INK), (NAMES[2], v[0.0], OR, eok(v[0.0]), OR)],
         base_y=880, top_y=470, bw=220, gap=170, nsize=96, seed=101, vmax=9.0)
    source(d, '매달 말 100만원 · 2011-10월 말 → 2026-10월 말 평가 · 환율 고정 · 세금 뺌 안 함 · 야후 파이낸스 수정 종가 · calc_dca')

@board
def sq1_fx(im):             # 환율 선 하나 — 처음 1,105원 · 끝 1,335원
    d = ImageDraw.Draw(im); TF(d, (W // 2, 100), '원/달러 환율 15년', 100, INK, F_X)
    ms = [m for m in CM.months if (2011, 10) <= m <= (2026, 10)]
    fx = [CK.me[m][1] for m in ms]
    assert (CK.me[ms[0]][0], round(fx[0], 1)) == ('20111031', 1104.5) and (CK.me[ms[-1]][0], round(fx[-1], 1)) == ('20261030', 1335.3)
    up = fx[-1] / fx[0] - 1; assert 0.20 < up < 0.21
    bx = (470, 250, 1450, 840); n = len(fx)
    xl = [(i, f'{m[0]}') for i, m in enumerate(ms) if m[1] == 10 and m[0] in (2011, 2016, 2021, 2026)]
    X, Y = linechart(im, [fx], bx, 1000, 1500, [INK], [6], xl, yfmt='{:,.0f}', yticks=())
    d = ImageDraw.Draw(im)
    r5 = lambda v: f'{int(v + 0.5):,}원'   # 1,104.5 → 1,105원(대본 97행 '1,105원' — 반올림, 은행가 반올림 아님)
    assert r5(fx[0]) == '1,105원' and r5(fx[-1]) == '1,335원'
    for i, col, lab, anc, dx in ((0, INK, r5(fx[0]), 'rm', -36), (n - 1, OR, r5(fx[-1]), 'lm', 36)):
        x, y = X(i), Y(fx[i]); d.ellipse((x - 16, y - 16, x + 16, y + 16), fill=col)
        T(d, (x + dx, y), lab, 96, col, F_X, anc)
    xe, ye = X(n - 1), Y(fx[-1]); hand_ellipse(d, (xe + 10, ye - 80, xe + 450, ye + 80), seed=111)
    T(d, (W // 2, 960), '15년 사이 20% 넘게 올랐다', 64, INK, F_X)
    source(d, '월말 원/달러 매매기준율 · 2011-10-31 1,104.5원 → 2026-10-30 1,335.3원 · 한국은행 ECOS 731Y001')

@board
def sq1_valley2(im):        # 반반 골짜기 둘 — 달러로 센 낙폭 / 원화로 센 낙폭
    d = ImageDraw.Draw(im); TF(d, (W // 2, 95), '반반, 가장 크게 빠진 폭', 96, INK, F_X)
    P = path(0.5); ms = [m for m, _ in P]; usd = [v for _, v in P]
    fx0 = CK.me[ms[0]][1]; krw = [v * CK.me[m][1] / fx0 for m, v in P]
    assert round(krw[-1], 2) == KRW15[50]
    du, dk = ddown(usd), ddown(krw)
    iu, ik = min(range(len(du)), key=du.__getitem__), min(range(len(dk)), key=dk.__getitem__)
    assert (round(du[iu] * 100, 1), ms[iu]) == (-24.0, (2022, 9)), (du[iu], ms[iu])
    assert (round(dk[ik] * 100, 1), ms[ik]) == (-13.6, (2020, 3)), (dk[ik], ms[ik])
    assert '반반 −13.6%(2020-01→03)' in _sc and '−24.0%' in _sc
    n = len(ms); xl = [(i, str(m[0])) for i, m in enumerate(ms) if m[1] == 10 and m[0] in (2011, 2026)]
    for k, (bx, dd, i0, col, head, lab) in enumerate((
            ((170, 300, 890, 760), du, iu, KRAFT, '달러로 세면', '−24%'),
            ((1080, 300, 1800, 760), dk, ik, OR, '원화로 세면', '−14%'))):
        X, Y = linechart(im, [[x * 100 for x in dd]], bx, -30, 0, [INK], [4], xl, yfmt='{:.0f}%', yticks=(-30, -15, 0))
        poly = [(X(i), Y(v * 100)) for i, v in enumerate(dd)] + [(X(n - 1), Y(0)), (X(0), Y(0))]
        ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(ov).polygon(poly, fill=col + (150,))
        im.paste(ov, (0, 0), ov); d = ImageDraw.Draw(im)
        d.line([(X(i), Y(v * 100)) for i, v in enumerate(dd)], fill=INK, width=4, joint='curve')
        d.line([(bx[0], Y(0)), (bx[2], Y(0))], fill=INK, width=4)
        T(d, ((bx[0] + bx[2]) // 2, 235), head, 64, INK, F_X)
        x, y = X(i0), Y(dd[i0] * 100)
        T(d, (x, 860), lab, 110, OR if col == OR else INK, F_X)
        T(d, (x, 950), f'{ms[i0][0]}년 {ms[i0][1]}월', 44, GREY, F_B)
        hand_arrow(d, (x, 800), (x, y + 16), OR if col == OR else INK, 5)
    source(d, '반반(SCHD 50%·QQQ 50%) 2011-10월 말 → 2026-10월 말 · 월말 평가액 × 월말 매매기준율(한국은행 ECOS) · 야후 파이낸스 · calc_krw')

def main(names):
    os.makedirs(OUT, exist_ok=True)
    for n in names or list(B):
        im = canvas(); B[n](im); im.save(os.path.join(OUT, n + '.png')); print(n)

if __name__ == '__main__':
    main(sys.argv[1:])
