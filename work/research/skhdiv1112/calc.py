# skhdiv1112 계산 — DART 배당 결정 원문(raw/*.txt)·소득세법 제129조·지방세법 제103조의13·건보 시행규칙 제44조·시행령 제41조
import math, sys
sys.stdout.reconfigure(encoding='utf-8')
Q3 = 20000                    # 2026-10-28 현금·현물배당결정 20261028800045 (실적 10,000 + 키옥시아 특별 10,000 — 공정공시 20261028800040)
Y2026 = {'2025 결산(2026-01-28 결정, 3/25 주총)': 1875, '2026 1분기': 375, '2026 2분기': 375, '2026 3분기': Q3}
PER = sum(Y2026.values()); BEFORE = PER - Q3
CLOSE = 1277000               # 2026-11-11 종가(야후 000660.KS)
def tax(g):
    i = math.floor(g * 0.14); l = math.floor(i * 0.10); return i, l, g - i - l
print('2026년 받는 1주당 배당 합계:', PER, '/ 3분기 빼면', BEFORE, '/ 3분기 비중 %.1f%%' % (Q3/PER*100))
print('3분기 2만원은 2분기 375원의 %.1f배' % (Q3/375))
for n in (10, 100):
    g = n*Q3; i,l,net = tax(g); print(f'{n}주 3분기 세전 {g:,} 소득세 {i:,} 지방 {l:,} 실수령 {net:,} · 평가액 {n*CLOSE:,}')
for line in (10_000_000, 20_000_000):
    n = line//PER + 1; n0 = line//BEFORE + 1
    print(f'{line:,}원 넘는 주식 수 {n:,}주({n*PER:,}원, {n-1}주={(n-1)*PER:,}) · 평가액 {n*CLOSE:,} · 3분기 없으면 {n0:,}주(평가액 {n0*CLOSE:,})')
for dep in (3_000_000, 5_000_000):
    n = (10_000_000-dep)//PER + 1; print(f'예금 이자 {dep:,}원 있으면 {n}주({n*PER:,}원) · 평가액 {n*CLOSE:,}')
print('시가배당률 공시 1.56%% · 11/11 종가 기준 3분기 %.2f%% · 연간 %.2f%%' % (Q3/CLOSE*100, PER/CLOSE*100))
