# R-1 '1억의 1년 영수증' — 2025-10-02 1억을 넣고 2026-10-02에 뺐다면(과거 값, 미래 보장 아님)
# 원자료: raw/collect_20261003.json(ECOS 예금금리), raw/collect2_20261003.json(FMP SPY·ECOS 원/달러), raw/yahoo_20261003.json(SPY·SCHD·GLD 종가·분배금)
# 가정: 환전은 ECOS 매매기준율(수수료 줄은 증권사마다 달라 비움), 분배금은 재투자 안 하고 끝날 환율로 원화 환산, 해외 ETF 매매차익 22%(20%+2%)·기본공제 250만(다른 양도차익 없음 가정)
import json, os, sys, math
sys.stdout.reconfigure(encoding='utf-8'); D = os.path.dirname(os.path.abspath(__file__))
c1 = json.load(open(f'{D}/raw/collect_20261003.json', encoding='utf-8')); c2 = json.load(open(f'{D}/raw/collect2_20261003.json', encoding='utf-8'))
y = json.load(open(f'{D}/raw/yahoo_20261003.json'))
fx = dict(c2['USDKRW_D']); f0, f1 = float(fx['20251002']), float(fx['20261002'])
P = 100_000_000; S, E = '2025-10-02', '2026-10-02'
print(f'[환율] 매매기준율 2025-10-02 {f0} → 2026-10-02 {f1} ({(f1/f0-1)*100:+.2f}%)')
fmp = {x['date']: x['price'] for x in c2['SPY_px']}
print(f'[교차] SPY 2026-10-02 FMP {fmp.get(E)} vs 야후 {round(y["SPY"]["px"][E],2)} · 2025-10-02 FMP {fmp.get(S)} vs 야후 {round(y["SPY"]["px"][S],2)}')
rows = []
dep = {t: float(v) for t, v in c1['정기예금1년_신규_M']}; r = dep['202510']
g = round(P * r / 100); tax = math.floor(g * 0.14 / 10) * 10; tax += math.floor(tax * 0.1 / 10) * 10
rows.append(('정기예금(2025-10 신규 평균 %.2f%%)' % r, P + g, g, 0, tax, P + g - tax))
for s in ['SPY', 'SCHD', 'GLD']:
    p0, p1 = y[s]['px'][S], y[s]['px'][E]; usd = P / f0; sh = usd / p0
    divs = {k: v for k, v in y[s]['div'].items() if S < k <= E}; dv = sh * sum(divs.values()) * f1
    sale = sh * p1 * f1; gain = sale - P
    cg = max(0, gain - 2_500_000); cgt = math.floor(cg * 0.20) + math.floor(cg * 0.02)
    px_only = sh * p0 * f1  # 가격 그대로, 환율만 바뀐 경우
    rows.append((s, round(sale), round(gain), round(dv), cgt, round(sale + dv - cgt)))
    print(f'[{s}] 종가 {p0:.2f}→{p1:.2f} ({(p1/p0-1)*100:+.2f}% 달러 기준) · 분배 {len(divs)}회 {sum(divs.values()):.3f}달러/주 · 환율 효과만 {round(px_only-P):,}원 · 원화 매도액 {round(sale):,} · 차익 {round(gain):,} · 분배금(세전) {round(dv):,} · 양도세 {cgt:,}')
print('\n[영수증] 이름 | 1년 뒤 평가(세전) | 차익 | 분배금(세전) | 세금 | 통장(세후, 분배금 세금 줄 비움)')
for n, a, gg, dv, t, net in sorted(rows, key=lambda x: -x[5]): print(f'  {n} | {a:,} | {gg:,} | {dv:,} | {t:,} | {net:,} ({(net/P-1)*100:+.2f}%)')
# 분배금 세금 줄을 0~15.4%로 바꿔도 순위가 같은지
for rt in [0, 0.154]:
    rk = sorted(rows, key=lambda x: -(x[5] - x[3] * rt)); print(f'  분배금 세율 {rt*100:.1f}%일 때 순위', [x[0][:6] for x in rk])
print('세전 순위', [x[0][:6] for x in sorted(rows, key=lambda x: -(x[1] + x[3]))])
