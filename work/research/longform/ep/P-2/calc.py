# P-2 계산 — 35세에 조기은퇴하면 국민연금은: 그냥 둠 / 임의가입 10년 / 임의가입 60세까지 (2026-10-16 youtube-loop)
#   py -3.12 calc.py   → 공단 예상연금월액표 전 칸 대조 + 세 길 결과 (calc_out.txt로 저장)
# 식(공단 표 주석 원문 그대로): 연금액 = (Σ 계수_y × (A+B) × P_y/P) × (1 + 0.05n/12) × 지급률
#   계수: 2008~2025 옛 부칙 제20조(현행 법에 실림) 1.500→1.245(해마다 0.015↓), 2026~ 제51조① 1.290
#   지급률: 제63조① 10년 50% + 10년 넘는 1년마다 5%(월 단위 5/12%), 20년부터 100%
#   상한: 제53조 월 지급액 ≤ max(최종 5년 기준소득월액 평균, 전 기간 평균)
#   공단 표 끝자리: 10원 미만 버림(대조로 확인)
# 가정(대본·화면에 그대로 밝힘): 오늘 돈 기준 — A값 2026년 3,193,511원 고정, 재평가·물가 0, 보험료 기준소득월액도 오늘 값 고정
import os, sys, openpyxl
sys.stdout.reconfigure(encoding='utf-8')
D = os.path.dirname(os.path.abspath(__file__))
A = 3193511                     # 공단 2026 적용 A값(표 첫 줄·P-1 F3)
COEF = {y: 1.500 - 0.015 * (y - 2008) for y in range(2008, 2026)}
RATE = {2026: .095, 2027: .100, 2028: .105, 2029: .110, 2030: .115, 2031: .120, 2032: .125}  # 부칙(2025.4.2) 제4조② 지역·임의
def coef(y): return round(COEF.get(y, 1.290), 3)
def rate(y): return RATE.get(y, .130)                                                     # 2033~ 제88조④ 1천분의 130

def pension(months):            # months: [(연도, 기준소득월액)] 한 달에 한 줄
    P = len(months); B = sum(m for _, m in months) / P
    base = sum(coef(y) for y, _ in months) / P * (A + B)
    n = max(0, P - 240)
    pay = 1.0 if P >= 240 else (0.5 + 0.05 * (P - 120) / 12 if P >= 120 else 0)
    amt = base * (1 + 0.05 * n / 12) * pay / 12
    last5 = [m for _, m in months[-60:]]
    cap = max(sum(last5) / len(last5), B)
    return int(min(amt, cap) // 10 * 10), B, P

# 1) 공단 표 대조: 2026년 1월 첫 가입·같은 소득 Y년(계수 1.290 하나)
wb = openpyxl.load_workbook(os.path.join(D, 'raw', 'nps_easypension_1_2026_3.xlsx'), data_only=True)
rows = [r for r in wb.worksheets[0].iter_rows(values_only=True) if isinstance(r[0], int)]
bad = 0; cells = 0
for r in rows:
    b = r[1]
    for k, yrs in enumerate([10, 15, 20, 25, 30, 35, 40]):
        got = pension([(2026, b)] * (yrs * 12))[0]; cells += 1
        if got != r[3 + k]: bad += 1; bad <= 5 and print('불일치', b, yrs, got, r[3 + k])
    if int(b * .095) // 10 * 10 != r[2] and int(b * .095) != r[2]: print('보험료 불일치', b, r[2])
out = [f'# P-2 calc · 공단 노령연금 예상월액표(easypension_1_2026_3.xlsx) {len(rows)}행×7칸 = {cells}칸 대조: 불일치 {bad}']

# 2) 세 길 — 가상 인물: 1991년생, 2016.1~2025.12 회사 10년(기준소득월액 400만원, 오늘 돈), 2026.1 퇴사(35세), 65세(2056) 수령
WORK = [(y, 4_000_000) for y in range(2016, 2026) for _ in range(12)]
LOW = 1_013_000                 # 임의(계속)가입 중위수 기준소득월액 2026.4~ 101.3만원 — 공단 안내 getOHAF0032M0(raw/nps_getOHAF0032M0_20261016.html), 공단 예상월액표 행과 같음
LOW_2025 = 1_000_000            # '25.4~'26.3 적용 중위수 100만원(같은 공단 표) — 2026년 1~3월분
def vol(y0, y1, inc=LOW):
    ms = [(y, inc) for y in range(y0, y1 + 1) for _ in range(12)]
    if y0 == 2026: ms[:3] = [(2026, LOW_2025)] * 3   # 2026.1~3은 '25.4 기준 금액
    return ms
def paid(ms): return sum(int(m * rate(y)) // 10 * 10 for y, m in ms)   # 공단 표 보험료 열도 10원 버림(1,013,000 → 96,230)
paths = [('그냥 둠(10년에서 멈춤)', []),
         ('45세 전까지 10년만 최저로 임의가입', vol(2026, 2035)),
         ('60세 전까지 25년 최저로 임의가입', vol(2026, 2050))]
base_amt = pension(WORK)[0]
out.append(f'A값 {A:,} · 회사 10년 기준소득월액 400만원 · 임의가입 기준 {LOW:,}원(공단 안내 2026.4~) · 오늘 돈·재평가 0')
out.append('| 길 | 가입 | B(평균 소득) | 65세부터 월 | 더 받는 월 | 더 낸 보험료 합 | 더 낸 돈 ÷ 더 받는 돈(년) | 본전 나이 |')
out.append('|---|---|---|---|---|---|---|---|')
for name, extra in paths:
    amt, B, P = pension(WORK + extra); add = amt - base_amt; cost = paid(extra)
    yrs = cost / (add * 12) if add else 0
    out.append(f'| {name} | {P // 12}년 | {B:,.0f} | {amt:,} | {add:,} | {cost:,} | {yrs:.1f} | {65 + yrs:.1f}세 |' if add else
               f'| {name} | {P // 12}년 | {B:,.0f} | {amt:,} | - | - | - | - |')
# 보험료 해마다(최저 기준)
out.append('최저 임의가입 월 보험료: ' + ' · '.join(f'{y} {int(LOW * rate(y)) // 10 * 10:,}' for y in (2026, 2027, 2030, 2033)))
# 계수 차이: 같은 10년이 2026년 뒤였다면
amt26 = pension([(2026, 4_000_000)] * 120)[0]
out.append(f'같은 10년·400만원을 2026년부터 냈다면 월 {amt26:,}원(계수 1.290) vs 2016~2025 실제 계수 평균 {sum(coef(y) for y in range(2016, 2026)) / 10:.4f} → 월 {base_amt:,}원')
# 3) 대본용 중간값(2026-10-16 youtube-loop 추가) — 지급률 전 금액·A값 비중·20년 넘는 가산
for name, extra in paths:
    ms = WORK + extra; P = len(ms); B = sum(m for _, m in ms) / P
    c = sum(coef(y) for y, _ in ms) / P
    full = c * (A + B) / 12
    pay = 1.0 if P >= 240 else 0.5 + 0.05 * (P - 120) / 12
    plus = 1 + 0.05 * max(0, P - 240) / 12
    out.append(f'{name}: 계수 평균 {c:.4f} · (A+B) {A + B:,.0f} 중 A 비중 {A / (A + B):.1%} · 지급률 전 월 {int(full):,} · 지급률 {pay:.0%} · 20년 넘는 가산 ×{plus:.2f}')
# 4) 낸 돈을 물가보다 r만큼 더 불렸다면(실질 이자, 오늘 돈 기준) 본전 나이
#    보험료는 2026.1부터 다달이, 더 받는 연금은 2056.1(65세)부터 다달이 · 65세 시점 값으로 맞춤
def breakeven(extra, add, r):
    m = (1 + r) ** (1 / 12) - 1; T = 30 * 12
    fv = sum((int(inc * rate(y)) // 10 * 10) * (1 + m) ** (T - i) for i, (y, inc) in enumerate(extra))
    got = 0.0
    for k in range(12 * 60):
        got += add / (1 + m) ** k
        if got >= fv: return 65 + (k + 1) / 12
    return float('nan')
for name, extra in paths[1:]:
    add = pension(WORK + extra)[0] - base_amt
    out.append(f'{name} 본전 나이(물가보다 더 불린 이자 연 0%·1%·2%·3%): ' + ' · '.join(f'{r:.0%} {breakeven(extra, add, r):.1f}세' for r in (0, .01, .02, .03)))
txt = '\n'.join(out); print(txt)
open(os.path.join(D, 'calc_out.txt'), 'w', encoding='utf-8').write(txt + '\n')
