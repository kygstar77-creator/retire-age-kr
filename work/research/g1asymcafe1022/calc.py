# g1asymcafe1022 계산 — KRX 금시장 금 1kg 일별 종가(원/g, 네이버 증권 marketIndex M04020000), 2026-10-22 07:5x 받음
import json, os
H = os.path.dirname(__file__)
rows = json.load(open(os.path.join(H, 'raw/krxgold_20261022.json'), encoding='utf-8'))
s = sorted((r['localTradedAt'][:10], int(r['closePrice'].replace(',', ''))) for r in rows)
print('기간', s[0], '~', s[-1], len(s), '영업일')
pk = max(s, key=lambda x: x[1]); print('고점', pk)
after = [x for x in s if x[0] > pk[0]]
lo = min(after, key=lambda x: x[1]); print('고점 뒤 최저', lo)
last = s[-1]; print('마지막', last)
for name, p in (('고점', pk), ):
    v = 1000 * last[1] / p[1]
    print(f'1천만원 → {v:.1f}만원, 손해 {1000 - v:.1f}만원 ({(1 - last[1] / p[1]) * 100:.2f}%), 본전까지 {(p[1] / last[1] - 1) * 100:.2f}%')
# 10/06 쇼츠 기준
d6 = dict(s)['2026-10-06']; print('10/06', d6, f'{1000 * d6 / pk[1]:.1f}만원 본전까지 {(pk[1] / d6 - 1) * 100:.2f}%')
# 떨어진 % → 본전까지 오를 %
for d in (10, 20, 30, 35, 50):
    print(f'{d}% 내리면 본전까지 {(1 / (1 - d / 100) - 1) * 100:.1f}%')
# 고점 뒤 반등: 최저 뒤 가장 높은 값
aft_lo = [x for x in s if x[0] > lo[0]]
if aft_lo:
    hi2 = max(aft_lo, key=lambda x: x[1]); print('최저 뒤 최고', hi2, f'최저 대비 +{(hi2[1] / lo[1] - 1) * 100:.2f}%')
# 고점 뒤 각 월말 값
import itertools
for m, g in itertools.groupby(after, key=lambda x: x[0][:7]):
    g = list(g); print(m, g[-1], f'{1000 * g[-1][1] / pk[1]:.0f}만원')
# 1년 전·3개월 전·한 달 전 같은 날 기준
for d in ('2025-10-21', '2026-07-21', '2026-09-21', '2026-09-22'):
    if d in dict(s): print('산 날', d, dict(s)[d], f'{1000 * last[1] / dict(s)[d]:.1f}만원')
