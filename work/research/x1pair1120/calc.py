# x1pair1120 계산 — 본전 환율 = 산 날 환율 ÷ (끝날 SPY ÷ 산 날 SPY). 가격 기준(배당 미포함), 수수료·환전 스프레드 미포함
import json, glob, sys
fx = json.load(open(sorted(glob.glob('raw/ecos_usd_*.json'))[-1]))
spy = json.load(open(sorted(glob.glob('raw/yahoo_SPY_*.json'))[-1]))
both = sorted(set(fx) & set(spy))
END = both[-1]
out = [f'끝날 {END}: 원/달러 {fx[END]:,} · SPY {spy[END]:.2f} (ECOS 최신 {max(fx)} {fx[max(fx)]:,})']
def line(name, d):
    m = spy[END] / spy[d]; be = fx[d] / m
    won = m * fx[END] / fx[d] - 1
    return f'{name} {d}: 환율 {fx[d]:,} · SPY {spy[d]:.2f} → 배수 {m:.4f}(달러 {m-1:+.2%}) · 본전 환율 {be:,.1f} · 끝날 환율과 차 {fx[END]-be:+,.1f} · 원화 수익률 {won:+.2%} · 1천만원 → {1e7*(1+won):,.0f}'
out.append('## 1. 쇼츠 예 두 날을 끝날 종가로 다시')
for nm, d in (('쇼츠 첫 예', '20251013'), ('쇼츠 최고점 예', '20260702'), ('쇼츠 기준 끝날', '20261015')):
    out.append(line(nm, d))
out.append('## 2. 지난 1년 매달 첫 거래일에 샀다면')
months = {}
for d in both:
    if d >= '20251101' and d[:6] not in months: months[d[:6]] = d
rows = []
for m, d in sorted(months.items()):
    out.append(line('매달 첫날', d)); rows.append(d)
under = [d for d in rows if fx[END] < fx[d] / (spy[END]/spy[d])]
out.append(f'끝날 환율이 본전 환율보다 낮은(원화 손해) 달: {len(under)}/{len(rows)} {under}')
out.append('## 3. 환율 최고·최저 (2025-11-01~끝날)')
win = [d for d in both if d >= '20251101']
hi = max(win, key=lambda d: fx[d]); lo = min(win, key=lambda d: fx[d])
out.append(line('환율 최고날', hi)); out.append(line('환율 최저날', lo))
out.append('## 4. 달러 수익률별 본전 환율 — 산 날 환율 1,450원이면')
for r in (0.05, 0.10, 0.16, 0.20, 0.30):
    out.append(f'달러 +{r:.0%}: 1,450 ÷ {1+r:.2f} = {1450/(1+r):,.1f}원')
open('calc_out.txt', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('\n'.join(out))
