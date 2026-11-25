"""H-6 장면 판 — visual-designer 2026-11-22. H-5·KOSPI-1 판과 같은 꼴·같은 부품(k1boards):
구겨진 종이 바탕 · 펜 빗금 막대(hatch_bar) · 주황 #FF5A00은 그 화면의 답 하나 · 손 동그라미·밑줄 · 상자·카드 판 없음.
숫자는 ep/H-6 calc_out·calc2_out(국토부 실거래 11/25 받음 — 11/25 visual: 76건·84㎡ 27·10~11 34.50억 10건으로 다시)과 script.md v1.6(editor 95a5c935) 화면·자막 줄 값만.
거래·월별 건수는 calc 출력 파일을 그대로 읽고 assert(옮겨 적지 않음). 보도·법 숫자는 script.md 자막 줄과 글자 그대로 대조.
판은 '답이 열린 마지막 모습' — '?' → 열림은 PD가 Remotion에서. 파일 이름은 shot_plan.md 장면 계획 '파일' 칸 그대로.
사용: py -3.12 h6boards.py [이름 ...]   (없으면 전부) → work/video/public/bg/h6/board/<이름>.png
"""
import os, sys, re, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'K-1-shots'))
from k1boards import (W, H, INK, GREY, OR, FADE, F_B, F_M, F_X, font, canvas, T, TF, source, obj,
                      hand_ellipse, hand_under, hand_check, hand_arrow, hatch_bar)
from PIL import Image, ImageDraw, ImageFilter

sys.stdout.reconfigure(encoding='utf-8')
WORK = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'H-6')
OUT = os.path.join(WORK, 'video', 'public', 'bg', 'h6', 'board')
LINE = (206, 198, 186)
rd = lambda fn: open(os.path.join(EP, fn), encoding='utf-8').read()
SRC_RT = '국토교통부 아파트 매매 실거래 · 은마 · 2026-11-25 받음 · 해제 거래 뺌'

# ── calc 출력에서 그대로 읽기 ─────────────────────────────────────────
_c1, _c2, _sc = rd('calc_out.txt'), rd('calc2_out.txt'), rd('script.md')
def _sec(head):
    return _c1.split(head, 1)[1].split('\n## ', 1)[0]
DEAL84 = [(dt, float(v), int(fl)) for dt, v, fl in re.findall(r'(\d{4}\.\d\d\.\d\d) ([\d.]+)억 (\d+)층', _sec('## 전용 84㎡'))]
DEAL77 = [(dt, float(v), int(fl)) for dt, v, fl in re.findall(r'(\d{4}\.\d\d\.\d\d) ([\d.]+)억 (\d+)층', _sec('## 전용 77㎡'))]
MON = [(m, int(n)) for m, n in re.findall(r'(\d{4}\.\d\d) (\d+)', _sec('## 월별 건수'))]
RENT = [(m, int(n)) for m, n in re.findall(r'(\d{4}\.\d\d) (\d+)', _sec('## 전월세'))]
GRP = {(a, p): (int(n), float(v)) for a, p, n, v in re.findall(r'(\d\d)㎡ (\S+): (\d+)건 가운데 ([\d.]+)억', _c2)}
assert len(DEAL84) == 27 and len(DEAL77) == 49 and '# 은마 매매 76건(해제 7건 뺌)' in _c1
assert len(MON) == 14 and sum(n for _, n in MON) == 76 and dict(MON)['2026.09'] + dict(MON)['2026.10'] == 34 and dict(MON)['2026.10'] == 22 and dict(MON)['2026.11'] == 4
assert len(RENT) == 13 and sum(n for _, n in RENT) == 893 and dict(RENT)['2025.12'] == 162 and dict(RENT)['2026.09'] == 20 and dict(RENT)['2025.10'] == 92
assert GRP[('84', '2025.10~12')] == (3, 42.80) and GRP[('84', '2026.01~06')] == (8, 38.83) and GRP[('84', '2026.07~09')] == (6, 37.08) and GRP[('84', '2026.10~11')] == (10, 34.50)
assert GRP[('77', '2025.10~12')] == (8, 37.38) and GRP[('77', '2026.01~06')] == (9, 34.80) and GRP[('77', '2026.10~11')] == (16, 31.45)
RECENT9 = [v for dt, v, _ in DEAL84 if dt >= '2026.10']
assert len(RECENT9) == 10 and st.median(RECENT9) == 34.50 and (min(RECENT9), max(RECENT9)) == (33.00, 36.00)
CHARGE = 46334   # 만원 — 강남구 보도자료 2026-11-10(script 146행 자막)
assert '1인당 평균 4억 6,334만원' in _sc and '4,326명' in _sc
def man(v):      # 41701 → '4억 1,701만'
    e, m = divmod(round(v), 10000); return f'{e}억 {m:,}만' if m else f'{e}억'
RELIEF = [('감경 없음', 0), ('6년 보유', 10), ('10~15년 보유', 50), ('20년 이상 보유', 70)]
assert [man(CHARGE * (100 - r) / 100) for _, r in RELIEF] == ['4억 6,334만', '4억 1,701만', '2억 3,167만', '1억 3,900만']
for s in ('4,424세대', '1979-08-30', '지하 6층~지상 49층', '29개동', '5,850세대', '3억 1,994만', '3억 2,010만', '4억 3,000만', '90일 이내', '60일 이내'):
    assert s in _sc, s

B = {}
def board(fn):
    B[fn.__name__] = fn; return fn

def slip(im, x0, y0, w, h, rot, paint, color=(246, 239, 220)):
    """기울여 붙인 종이 쪽지 한 장(K-1 k1_trap 꼴) — paint(cd, w, h)로 글을 쓴다."""
    card = Image.new('RGBA', (w, h), (0, 0, 0, 0)); cd = ImageDraw.Draw(card); cd.rectangle((0, 0, w, h), fill=color); paint(cd, w, h)
    card = card.rotate(rot, expand=True, resample=Image.BICUBIC)
    sh = Image.new('L', card.size, 0); sh.paste(card.split()[3].point(lambda v: 70 if v else 0)); sh = sh.filter(ImageFilter.GaussianBlur(8))
    im.paste((150, 146, 140), (x0 + 8, y0 + 10), sh); im.paste(card, (x0, y0), card)

def dashed_v(d, x, y0, y1, color=GREY, w=4, seg=16):
    for y in range(int(y0), int(y1), seg * 2): d.line([(x, y), (x, min(y + seg, y1))], fill=color, width=w)

# ── 0. 여는 말 ───────────────────────────────────────────────────────
@board
def open85(im):            # '1년 사이 ?억' → 8억 3천만원 (11/25 값)
    d = ImageDraw.Draw(im)
    T(d, (W // 2, 170), '은마아파트 34평(전용 84㎡) · 가운데 값', 64, GREY, F_B)
    T(d, (W // 2, 400), '1년 사이', 150, INK, F_X)
    T(d, (W // 2, 640), '8억 3천만원', 230, OR, F_X)
    hand_ellipse(d, (290, 490, 1630, 800), seed=11)
    a, b = GRP[('84', '2025.10~12')][1], GRP[('84', '2026.10~11')][1]; assert round(a - b, 2) == 8.30
    T(d, (W // 2, 905), '42억 8천  →  34억 5천', 96, INK, F_X)
    source(d, SRC_RT + ' · 2025.10~12 계약 3건 → 2026.10~11 계약 10건')

# ── 1. 은마는 지금 어디까지 ─────────────────────────────────────────
@board
def built(im):             # 1979년 준공 · 4,424세대
    d = ImageDraw.Draw(im)
    obj(im, 'apt', 470, 560, size=520, rot=-3, seed=3); d = ImageDraw.Draw(im)
    T(d, (1280, 400), '1979년', 220, OR, F_X)
    T(d, (1280, 560), '준공', 110, INK, F_X)
    T(d, (1280, 770), '4,424세대', 150, INK, F_X)
    hand_under(d, 960, 1600, 860, color=INK, seed=13)
    source(d, '국토교통부 건축HUB 건축물대장 · 사용승인 1979-08-30')

@board
def steps(im):             # 계단 7칸 — 지난 두 단계 주황 점 (11/22 심사 못함: 날짜가 옆 칸 위·동그라미 겹침 → 날짜 점 바로 위, 동그라미 대신 밑줄)
    d = ImageDraw.Draw(im); TF(d, (W // 2, 110), '재건축은 계단처럼', 104, INK, F_X)
    S = [('조합설립', '2023.9', 1), ('사업시행\n계획인가', '2026.7.2', 1), ('분양신청', '', 0), ('관리처분', '', 0), ('이주', '', 0), ('착공', '', 0), ('준공', '', 0)]
    x0, y0, sw, sh = 150, 930, 240, 92; pts = [(x0 - 40, y0)]
    for i in range(len(S)):
        x, y = x0 + i * sw, y0 - i * sh
        pts += [(x, y), (x, y - sh), (x + sw, y - sh)]
    d.line(pts, fill=INK, width=7, joint='curve')
    for i, (nm, dt, done) in enumerate(S):
        cx, cy = x0 + i * sw + sw / 2, y0 - (i + 1) * sh
        r = 24; d.ellipse((cx - r, cy - 50 - r, cx + r, cy - 50 + r), fill=OR if done else None, outline=OR if done else GREY, width=7)
        for k, ln in enumerate(nm.split('\n')):
            T(d, (cx - 16, cy + 46 + k * 50), ln, 42, INK if done else GREY, F_X if done else F_B)
        if dt: T(d, (cx, cy - 115), dt, 46, OR, F_X)
    cx = x0 + sw + sw / 2; cy = y0 - 2 * sh
    hand_under(d, cx - 120, cx + 90, cy + 150, seed=17)
    source(d, '조합설립인가 2023-09-26 · 사업시행계획인가 2026-07-02(강남구 고시 제2026-130호) · 정비사업 정보몽땅·강남구')

@board
def plan49(im):            # 새 단지 계획
    d = ImageDraw.Draw(im); T(d, (W // 2, 150), '계획대로라면', 84, GREY, F_B)
    T(d, (W // 2, 400), '지상 49층', 250, OR, F_X)
    hand_under(d, 470, 1450, 540, seed=21)
    T(d, (W // 2, 690), '지하 6층 · 29개동', 104, INK, F_X)
    T(d, (W // 2, 850), '5,850세대', 130, INK, F_X)
    source(d, '강남구 보도자료 2026-07-02 · 공공임대 909·공공분양 195 포함')

# ── 2. 1년 실거래, 평형별 ───────────────────────────────────────────
@board
def count75(im):           # 75건 = 77㎡ 49 · 84㎡ 26
    d = ImageDraw.Draw(im); TF(d, (W // 2, 120), f'지난 1년 매매 {len(DEAL77) + len(DEAL84)}건', 120, INK, F_X)
    T(d, (W // 2, 230), '2025.10~2026.11 계약 · 해제 7건 뺌', 56, GREY, F_B)
    base, top, bw = 880, 440, 300; vmax = 49
    for i, (lab, sub, n) in enumerate((('31평', '전용 77㎡', len(DEAL77)), ('34평', '전용 84㎡', len(DEAL84)))):
        x = 560 + i * 520; yt = base - (base - top) * n / vmax; c = OR if i == 0 else INK
        hatch_bar(im, (x, yt, x + bw, base), c, seed=30 + i, step=12, width=5); d = ImageDraw.Draw(im)
        T(d, (x + bw / 2, yt - 70), f'{n}건', 120, c, F_X)
        T(d, (x + bw / 2, base + 55), f'{lab} · {sub}', 50, INK, F_B)
    d.line([(420, base), (1500, base)], fill=GREY, width=4)
    source(d, SRC_RT + ' · 막대는 0건부터')

def _dot_axes(d, box, v0, v1):
    x0, y0, x1, y1 = box
    m0, m1 = 2025 * 12 + 9, 2026 * 12 + 11
    X = lambda dt: x0 + (x1 - x0) * ((int(dt[:4]) * 12 + int(dt[5:7]) - 1 + (int(dt[8:10]) - 1) / 31) - m0) / (m1 - m0)
    Y = lambda v: y1 - (y1 - y0) * (v - v0) / (v1 - v0)
    for v in range(int(v0) + 1, int(v1) + 1, 2):
        d.line([(x0, Y(v)), (x1, Y(v))], fill=LINE, width=2); T(d, (x0 - 18, Y(v)), f'{v}억', 36, GREY, F_B, 'rm')
    for lab, dt in (('2025.10', '2025.10.01'), ('2026.1', '2026.01.01'), ('2026.4', '2026.04.01'), ('2026.7', '2026.07.01'), ('2026.10', '2026.10.01')):
        T(d, (X(dt), y1 + 40), lab, 34, GREY, F_B)
    return X, Y

@board
def pairs(im, k=2):        # 84㎡ 26건 점 · 한 장에 한 쌍만 선(11/22 심사 못함: 선 셋이 얽힘) — pairs_1(12↔12) → pairs_2(13↔14) → pairs(13↔1)
    d = ImageDraw.Draw(im); TF(d, (W // 2, 90), '34평 · 어느 두 건을 붙이느냐에 따라', 76, INK, F_X)
    X, Y = _dot_axes(d, (230, 190, 1240, 900), 32, 44)
    for dt, v, fl in DEAL84:
        x, y = X(dt), Y(v); d.ellipse((x - 11, y - 11, x + 11, y + 11), fill=(170, 160, 148))
    P = [(('2025.10.14', 42.80, 12), ('2026.09.09', 39.00, 12), '12층 ↔ 12층'),
         (('2025.10.31', 43.10, 13), ('2026.10.31', 35.00, 14), '13층 ↔ 14층'),
         (('2025.10.31', 43.10, 13), ('2026.10.31', 33.00, 1), '13층 ↔ 1층')]
    for a, b, _ in P: assert a in DEAL84 and b in DEAL84, (a, b)
    a, b, _ = P[k]; xa, ya, xb, yb = X(a[0]), Y(a[1]), X(b[0]), Y(b[1])
    d.line([(xa, ya), (xb, yb)], fill=OR, width=8)
    for x, y, fl in ((xa, ya, a[2]), (xb, yb, b[2])):
        d.ellipse((x - 17, y - 17, x + 17, y + 17), fill=OR)
        T(d, (x + (34 if x < 700 else -34), y), f'{fl}층', 40, OR, F_X, 'lm' if x < 700 else 'rm')
    for i, (a2, b2, lab) in enumerate(P[:k + 1]):
        gap = round(a2[1] - b2[1], 2); assert gap in (3.80, 8.10, 10.10)
        cur = i == k; yy = 330 + i * 190
        T(d, (1330, yy), lab, 52 if cur else 40, INK if cur else GREY, F_B, 'lm')
        T(d, (1330, yy + 80), f'−{gap:.1f}억', 120 if cur else 64, OR if cur else GREY, F_X, 'lm')
    source(d, SRC_RT + ' · 전용 84㎡ 27건 · 점 하나 = 한 건 · 세로 32억부터')

@board
def pairs_1(im): pairs(im, 0)
@board
def pairs_2(im): pairs(im, 1)

@board
def m77(im):               # 77㎡ 묶음 가운데 값 셋 — 인가 전에 이미 −2.58억 (11/22 심사 못함: 31.45억 자리·꼬리표 둘·㎡ 깨짐 → 막대 셋+괄호 하나)
    d = ImageDraw.Draw(im); TF(d, (W // 2, 100), '31평도 같은 모양', 104, INK, F_X)
    T(d, (W // 2, 200), '전용 77㎡ · 묶음마다 가운데 값', 52, GREY, F_B)
    a, mid, b = GRP[('77', '2025.10~12')][1], GRP[('77', '2026.01~06')][1], GRP[('77', '2026.10~11')][1]
    assert (round(a - b, 2), round(a - mid, 2)) == (5.93, 2.58)
    base, top, vmax, bw = 900, 430, 40, 260; Y = lambda v: base - (base - top) * v / vmax
    xs = (330, 830, 1330)
    for i, (x, v, lab) in enumerate(zip(xs, (a, mid, b), ('2025.10~12', '2026.1~6 (인가 전)', '2026.10~11'))):
        hatch_bar(im, (x, Y(v), x + bw, base), INK, seed=40 + i, step=12, width=5); d = ImageDraw.Draw(im)
        T(d, (x + bw / 2, Y(v) - 50), f'{v:.2f}억', 64, INK, F_X)
        T(d, (x + bw / 2, base + 46), lab, 40, OR if i == 1 else GREY, F_B)
    d.line([(250, base), (1700, base)], fill=GREY, width=4)
    x0, x1 = xs[0] + bw / 2, xs[1] + bw / 2; yb = Y(a) - 120
    d.line([(x0, yb + 30), (x0, yb), (x1, yb), (x1, yb + 30)], fill=OR, width=6)
    T(d, ((x0 + x1) / 2, yb - 50), '인가 전에 이미 −2.58억', 64, OR, F_X)
    source(d, SRC_RT + ' · 가운데 값 8건 → 9건 → 16건 · 1년 −5.93억 · 막대는 0억부터')

# ── 3. 거래는 언제 몰렸나 ───────────────────────────────────────────
def monthbars(im, rows, hi, partial, vmax, title, seed, lab_hi, note_x=None):
    d = ImageDraw.Draw(im); TF(d, (W // 2, 100), title, 92, INK, F_X)
    x0, x1, base, top = 170, 1750, 860, 300; n = len(rows); slot = (x1 - x0) / n; bw = slot * 0.62
    for i, (m, v) in enumerate(rows):
        x = x0 + i * slot + (slot - bw) / 2; yt = base - (base - top) * v / vmax
        c = OR if m == hi else (GREY if m == partial else INK)
        if m == partial:
            hatch_bar(im, (x, yt, x + bw, base), FADE, seed=seed + i, step=16, width=4)
        else:
            hatch_bar(im, (x, yt, x + bw, base), c, seed=seed + i, step=11, width=5)
        d = ImageDraw.Draw(im)
        T(d, (x + bw / 2, yt - 36), f'{v}', 72 if m == hi else (50 if m in lab_hi else 38), c, F_X if m in (hi,) + tuple(lab_hi) else F_B)
        yy, mm = m.split('.'); T(d, (x + bw / 2, base + 40), f'{int(mm)}월', 36, INK, F_B)
        if mm == '01' or i == 0: T(d, (x + bw / 2, base + 86), yy, 32, GREY, F_B)
        if m == partial: T(d, (x + bw / 2, base + 86), '덜 들어옴', 32, GREY, F_B)
        if m == '2026.07': kx = x - (slot - bw) / 2
    d.line([(x0 - 10, base), (x1 + 10, base)], fill=GREY, width=4)
    dashed_v(d, kx, top - 40, base); T(d, (kx + 10, top - 60), '인가 7.2', 38, GREY, F_B, 'lm')
    return d

@board
def monthly(im):           # 월별 매매 14개 — 10월 주황, 11월 덜 들어옴
    d = monthbars(im, MON, '2026.10', '2026.11', 24, '은마 매매 · 달마다 몇 건?', 50, ('2026.09', '2025.10', '2026.08'))
    n910, nall = dict(MON)['2026.09'] + dict(MON)['2026.10'], sum(n for _, n in MON); assert round(100 * n910 / nall) == 45
    T(d, (560, 420), f'9~10월 {n910}건', 96, OR, F_X)
    T(d, (560, 520), f'1년 {nall}건의 {round(100 * n910 / nall)}%', 56, INK, F_B)
    source(d, SRC_RT + ' · 31평·34평 · 계약일부터 30일 안 신고 — 11월은 아직 덜 들어옴')

# ── 4. 세 가지 숙제 ─────────────────────────────────────────────────
@board
def cards3(im):            # 쪽지 셋 — 첫째 앞으로 (11/22 심사 못함: 반듯한 3칸·구분선 = AI 티 → 기울인 종이 쪽지)
    d = ImageDraw.Draw(im); TF(d, (W // 2, 120), '조합원 앞에 놓인 숙제 셋', 104, INK, F_X)
    R = (('①', '분담금', '새 집 받으려 더 내는 돈'), ('②', '재건축 부담금', '재초환 · 나라가 거둬 가는 돈'), ('③', '이주', '공사 동안 나가 살 곳'))
    for i in (2, 1, 0):
        n, a, b = R[i]; big = i == 0
        w, h = (580, 460) if big else (520, 400)
        def paint(cd, w, h, n=n, a=a, b=b, big=big):
            T(cd, (w // 2, 95), n, 96, OR if big else GREY, F_X)
            T(cd, (w // 2, 230), a, 80 if big else 62, INK, F_X)
            T(cd, (w // 2, 340), b, 36, INK, F_B)
        slip(im, (130, 690, 1240)[i], (300, 340, 320)[i], w, h, (-3.2, 1.8, -1.2)[i], paint)
    for i, (nm, x, y) in enumerate((('coins', 600, 330), ('bill', 1110, 370), ('house', 1660, 350))):   # 11/22 2차 못함 '글자만 있는 쪽지' → 쪽지마다 그 돈·일의 그림 하나
        obj(im, nm, x, y, size=190 if i == 0 else 160, rot=(6, -5, 4)[i], seed=70 + i)
    d = ImageDraw.Draw(im); hand_under(d, 260, 600, 590, seed=61)
    source(d, '재건축초과이익 환수법 · 도시정비법 · 강남구 보도자료')

@board
def share2(im):            # 보도마다 갈리는 분담금 — 주황 없음
    d = ImageDraw.Draw(im); TF(d, (W // 2, 110), '34평 내고 84㎡ 받을 때 · 추정 분담금', 86, INK, F_X)
    rows = (('보도 3곳', 3.2, '약 3억 2천만원'), ('보도 1곳', 4.3, '4억 3천만원'))
    x0, xmax = 470, 1500
    for i, (lab, v, s) in enumerate(rows):
        y = 380 + i * 260; x1 = x0 + (xmax - x0) * v / 5
        T(d, (x0 - 30, y + 60), lab, 64, INK, F_B, 'rm')
        hatch_bar(im, (x0, y, x1, y + 120), INK, seed=70 + i, step=12, width=5); d = ImageDraw.Draw(im)
        T(d, (x1 + 30, y + 60), s, 80, INK, F_X, 'lm')
    d.line([(x0, 330), (x0, 900)], fill=GREY, width=4)
    T(d, (W // 2, 960), '조합 원문은 확인 못 함 — 어느 쪽이 맞는지 말하지 않아요', 52, INK, F_B)
    source(d, '아시아경제 5/21 3억 1,994만 · 중앙일보 5/30 3억 2천만 · 머니투데이 9/29 3억 2,010만 / 비즈니스워치 9/24 4억 3,000만 · 막대는 0원부터')

@board
def charge(im):            # 재건축 부담금 예정액 1인당 평균
    d = ImageDraw.Draw(im)
    obj(im, 'bill', 380, 560, size=460, rot=-5, seed=5); d = ImageDraw.Draw(im)
    T(d, (1180, 260), '② 재건축 부담금 예정액', 76, INK, F_X)
    T(d, (1180, 400), '1인당', 80, GREY, F_B)
    T(d, (1180, 580), man(CHARGE) + '원', 170, OR, F_X)
    cx, cy = 1630, 790
    hand_ellipse(d, (cx - 150, cy - 85, cx + 150, cy + 85), color=OR, seed=81)
    T(d, (cx, cy), '평균', 84, OR, F_X)
    T(d, (1040, 790), '내 몫이 아니라 평균', 60, INK, F_B)
    source(d, '강남구 보도자료 2026-11-10 · 통지 2026-10-30 · 4,326명 · 2035년 준공 가정 · 장기보유 감경 미반영')

@board
def move(im):              # ③ 이주 · 공식 일정 없음
    d = ImageDraw.Draw(im)
    obj(im, 'calendar', 520, 560, size=520, rot=3, seed=9); d = ImageDraw.Draw(im)
    T(d, (520, 560), '?', 260, OR, F_X)
    T(d, (1300, 380), '③ 이주', 150, INK, F_X)
    T(d, (1300, 600), '공식 일정', 120, INK, F_X)
    T(d, (1300, 760), '없음', 160, OR, F_X)
    hand_under(d, 1150, 1450, 850, seed=91)
    source(d, "보도는 '내년 상반기 목표'(비즈니스워치 9/24) 등 — 모두 목표, 공식 일정 아님")

# ── 5. 세입자 계약 신고 ─────────────────────────────────────────────
@board
def rent(im):              # 전월세 신고 13개월 — 9월 주황, 10월 덜 들어옴
    d = monthbars(im, RENT, '2026.09', '2026.10', 170, '은마 전세·월세 신고 · 달마다', 100, ('2025.12', '2025.10', '2026.08'))
    T(d, (1545, 360), f"{dict(RENT)['2025.12']} → {dict(RENT)['2026.09']}", 100, OR, F_X)
    T(d, (1545, 455), '가장 많던 12월 → 9월', 44, INK, F_B)
    source(d, '국토교통부 전월세 실거래 · 은마 전세+월세 893건 · 2026-11-25 받음 · 10월은 아직 덜 들어옴')

# ── 6. 누구라면 ─────────────────────────────────────────────────────
@board
def relief(im):            # 보유기간 감경 표 — 70% 줄 주황
    d = ImageDraw.Draw(im); TF(d, (W // 2, 110), '오래 가진 1주택이면 줄어요', 100, INK, F_X)
    T(d, (W // 2, 210), '평균 예정액에 감경률만 곱한 계산 · 실제 개인 몫 아님', 48, GREY, F_B)
    for i, (lab, r) in enumerate(RELIEF):
        y = 360 + i * 150; c = OR if r == 70 else INK
        T(d, (760, y), lab, 62, c, F_B, 'rm')
        T(d, (900, y), f'{r}%' if r else '—', 72, c, F_X, 'mm')
        T(d, (1660, y), man(CHARGE * (100 - r) / 100) + '원', 90 if r == 70 else 76, c, F_X, 'rm')
        if i < 3: d.line([(220, y + 75), (1700, y + 75)], fill=LINE, width=2)
    hand_ellipse(d, (1060, 360 + 450 - 78, 1750, 360 + 450 + 78), seed=101)
    source(d, '재초환법 제14조의2 · 1세대 1주택 · 평균 4억 6,334만원 × (1 − 감경률) · 파이어맵 계산')

@board
def cash(im):              # 분양신청 안 하면 → 90일 협의 → 60일 수용재결·매도청구
    d = ImageDraw.Draw(im); TF(d, (W // 2, 120), '분양신청을 안 하면', 110, INK, F_X)
    R = (('현금청산', '새 집 대신 돈으로'), ('90일 안 협의', '관리처분 인가·고시 다음 날부터'), ('60일 안', '수용재결 · 매도청구'))
    for i, (a, b) in enumerate(R):
        cx = 330 + i * 630; c = OR if i == 1 else INK
        T(d, (cx, 520), a, 84, c, F_X); T(d, (cx, 640), b, 44, INK, F_B)
        if i < 2: hand_arrow(d, (cx + 265, 520), (cx + 365, 520), GREY, 7)
        if i == 1: T(d, (cx + 315, 455), '안 되면', 40, GREY, F_B)
    source(d, '도시정비법 제73조① 손실보상 협의 90일 이내 · ② 불성립 시 60일 이내 수용재결 신청 또는 매도청구소송')

@board
def recent9(im):           # 84㎡ 요즘 10건 — 가운데 34.50억, 33.00~36.00 (11/25 값, 파일 이름은 PD 장면 그대로 recent9)
    d = ImageDraw.Draw(im); TF(d, (W // 2, 110), f'34평 요즘 거래 {len(RECENT9)}건', 110, INK, F_X)
    T(d, (W // 2, 220), '2026.10~11 계약', 56, GREY, F_B)
    v0, v1, x0, x1, y = 32.5, 36.5, 220, 1700, 720
    X = lambda v: x0 + (x1 - x0) * (v - v0) / (v1 - v0)
    d.line([(x0, y), (x1, y)], fill=GREY, width=4)
    for v in (33, 34, 35, 36): d.line([(X(v), y - 14), (X(v), y + 14)], fill=GREY, width=4); T(d, (X(v), y + 60), f'{v}억', 42, GREY, F_B)
    seen = {}
    for v in sorted(RECENT9):
        k = seen.get(v, 0); seen[v] = k + 1; cx, cy = X(v), y - 40 - k * 56
        d.ellipse((cx - 22, cy - 22, cx + 22, cy + 22), fill=INK)
    med = st.median(RECENT9); mx = X(med)
    dashed_v(d, mx, 380, y, OR, 6)
    T(d, (mx, 330), f'가운데 {med:.2f}억', 96, OR, F_X)
    lo, hi = min(RECENT9), max(RECENT9)
    hand_under(d, X(lo), X(hi), y + 120, color=INK, seed=111)
    T(d, (X((lo + hi) / 2), y + 180), f'{lo:.2f}억 ~ {hi:.2f}억', 60, INK, F_X)
    source(d, SRC_RT + ' · 전용 84㎡ · 점 하나 = 한 건 · 10/31 하루 5건')

# ── 7. 함정과 직접 확인 ─────────────────────────────────────────────
TRAPS = (('한 건끼리 비교', '고르기에 따라 4억도 10억도'), ('이번 달 숫자', '신고는 30일 안 — 아직 덜 들어옴'),
         ('평균 부담금', '내 몫이 아니라 평균'), ('매물 수', '팔린 건수가 아님'))
TRAP_SRC = '부동산 거래신고법 제3조① 계약일부터 30일 이내 · 강남구 보도자료 2026-11-10 · 매물 수 = 민간 중개 사이트 자료'

def _trap1(im, k):         # 11/22 심사 못함(번호 목록 = AI 슬라이드 티) → 함정 하나씩 한 장
    d = ImageDraw.Draw(im); T(d, (W // 2, 130), f'함정 {k + 1} / 4', 64, GREY, F_B)
    a, b = TRAPS[k]
    TF(d, (W // 2, 430), a, 180, INK, F_X); hand_under(d, 420, 1500, 560, seed=130 + k)
    TF(d, (W // 2, 720), b, 84, OR, F_X)
    source(d, TRAP_SRC)

@board
def traps_1(im): _trap1(im, 0)
@board
def traps_2(im): _trap1(im, 1)
@board
def traps_3(im): _trap1(im, 2)
@board
def traps_4(im): _trap1(im, 3)

@board
def traps(im):             # 넷 모아 — 기울인 쪽지 2×2(넷 다 말한 뒤 한 번)
    d = ImageDraw.Draw(im); TF(d, (W // 2, 100), '함정 넷', 100, INK, F_X)
    for i, (a, b) in enumerate(TRAPS):
        def paint(cd, w, h, a=a, b=b, i=i):
            T(cd, (w // 2, 70), '①②③④'[i], 64, OR, F_X); T(cd, (w // 2, 170), a, 64, INK, F_X); T(cd, (w // 2, 260), b, 34, INK, F_B)
        slip(im, (230, 1000)[i % 2], (200, 600)[i // 2], 700, 330, (-2.0, 1.5, 1.2, -1.6)[i], paint)
    source(d, TRAP_SRC)

@board
def rt4(im):               # 실거래가 공개시스템 따라 하기 넷
    d = ImageDraw.Draw(im); TF(d, (W // 2, 110), '내 평형 직접 세기', 110, INK, F_X)
    R = ('단지 고르기', '같은 면적', '지난 1년', "'해제' 빼기")
    for i, a in enumerate(R):
        cx = 300 + i * 440; c = OR if i == 3 else INK
        T(d, (cx, 380), str(i + 1), 150, c, F_X)
        T(d, (cx, 540), a, 70, c, F_X)
        if i < 3: hand_arrow(d, (cx + 150, 460), (cx + 290, 460), GREY, 7)
    T(d, (W // 2, 720), '인가 7월 앞뒤로 나눠 가운데 값', 64, INK, F_B)
    T(d, (W // 2, 880), 'rt.molit.go.kr', 120, INK, F_X)
    hand_under(d, 560, 1360, 950, seed=121)
    source(d, '국토교통부 실거래가 공개시스템 · 화면은 우리가 다시 그림 · 가운데 값 = 값 순서로 줄 세웠을 때 한가운데')

# ── 8. 정리 ─────────────────────────────────────────────────────────
@board
def summary(im):           # 정리 표 5줄
    d = ImageDraw.Draw(im); T(d, (W // 2, 110), '은마 한 장 정리', 116, INK, F_X)
    a, mid, b = GRP[('84', '2025.10~12')][1], GRP[('84', '2026.01~06')][1], GRP[('84', '2026.10~11')][1]
    assert round(a - b, 2) == 8.30 and round(a - mid, 2) == 3.97
    rows = (('34평 1년 새', '8억 3천 내림'), ('그중 인가 전에', '4억 가까이 내림'), ('9~10월 두 달', '34건 팔림 (1년 76건)'),
            ('전월세 신고', '1년 전 92건 → 9월 20건'), ('재건축 부담금', '평균 4억 6천 (감면 전)'))   # 11/22 심사 못함: 명사형이라 뜻이 안 읽힘 → 서술형
    for i, (k, v) in enumerate(rows):
        y = 280 + i * 140
        T(d, (720, y), k, 58, INK if i == 0 else GREY, F_B, 'rm'); T(d, (780, y), v, 80, OR if i == 0 else INK, F_X, 'lm')
        if i < 4: d.line([(200, y + 70), (1760, y + 70)], fill=LINE, width=2)
    source(d, '국토교통부 실거래(2026-11-25)·강남구 보도자료 · 계산·비교 자료이며 매수·매도 권유가 아닙니다')

def main(names):
    os.makedirs(OUT, exist_ok=True)
    for n in names or list(B):
        im = canvas(); B[n](im); im.save(os.path.join(OUT, n + '.png')); print(n)

if __name__ == '__main__':
    main(sys.argv[1:])
