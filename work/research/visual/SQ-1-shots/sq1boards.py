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
                      hand_ellipse, hand_under, hand_check, hand_arrow, hatch_bar, bars)
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
            ('최근 5년 1억', [eok(R5[p]) for p in (100, 50, 0)]),
            ('2022년 한 해', [f"{round(MIX[p]['y22'])}%".replace('-', '−') for p in (100, 50, 0)]),
            ('한 해 분배금(세전)', [f'{x}만원' for x in DIST]))
    for i, (k, vals) in enumerate(rows):
        y = 360 + i * 140
        T(d, (cx[0], y), k, 54, INK, F_B, 'rm')
        for j, v in enumerate(vals): T(d, (cx[j + 1], y), v, 70, OR if (i == 1 and j == 1) else INK, F_X)
        d.line([(200, y + 70), (1780, y + 70)], fill=LINE, width=2)
    y = 360 + 4 * 140
    T(d, (cx[0], y), '15년 SCHD 세후', 54, INK, F_B, 'rm')
    T(d, ((cx[1] + cx[3]) // 2, y), f'직접 {TAX15[0]:.1f}억 · 국내 상장 {TAX15[1]:.1f}억', 70, INK, F_X)
    source(d, '야후 파이낸스·Schwab·Invesco·한국은행·법제처 · 계산·비교 자료이며 매수·매도 권유가 아닙니다')

def main(names):
    os.makedirs(OUT, exist_ok=True)
    for n in names or list(B):
        im = canvas(); B[n](im); im.save(os.path.join(OUT, n + '.png')); print(n)

if __name__ == '__main__':
    main(sys.argv[1:])
