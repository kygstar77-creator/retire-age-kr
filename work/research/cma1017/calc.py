# cma1017 계산 — 원문: raw/kis_m.txt(한국투자증권 CMA 안내, RP 2.50% 기준일 2026.08.31 · 발행어음 2.85% 2026.09.04 · MMF 1개월 3.05~3.15% 2026.10.16), raw/shinhan.txt(신한 RP 2.45%), ECOS 기준금리 3.0%(2026-08)
import sys; sys.stdout.reconfigure(encoding='utf-8')
P = 10_000_000; D = 30; TAX = 0.154
def it(r, p=P, d=D):
    g = p * r / 100 * d / 365; return round(g), round(g * (1 - TAX))
for name, r in [('신한 RP', 2.45), ('한투 RP', 2.50), ('한투 발행어음', 2.85), ('한투 MMF 1개월(최저)', 3.05), ('기준금리', 3.00)]:
    g, n = it(r); print(f'{name} {r}% 1천만원 30일 세전 {g:,} 세후 {n:,}')
g1, n1 = it(2.50); g2, n2 = it(2.85); print('발행어음-RP 세후 차', f'{n2-n1:,}')
for name, r in [('한투 RP', 2.50), ('한투 발행어음', 2.85)]:
    g, n = it(r, 100_000_000, 365); print(f'{name} 1억 1년 세전 {g:,} 세후 {n:,}')
print('RP vs 기준금리 차 %p', round(3.00 - 2.50, 2), round(3.00 - 2.45, 2))
