# R-1 '1억의 1년 영수증' — 2025-10-02 1억을 넣고 2026-10-02에 뺐다면(과거 값, 미래 보장 아님)
# 원자료: raw/collect_20261003.json(ECOS 예금금리), raw/collect2_20261003.json(FMP SPY·ECOS 원/달러), raw/yahoo_20261003.json(SPY·SCHD·GLD 종가·분배금)
# 분배금 세금(2026-10-03 결정): 미국 원천징수 15% — IRS Tax Treaty Table 1(Rev. May 2023, raw/irs_treaty_table1.pdf) Korea 'Paid by U.S. Corporations—General' 15%, 조약 제12조(2) · 국내 추가 원천징수 0(소득세법 제129조④, A-1 facts [5])
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
SCHWAB = {'2025-12-10': 0.2782, '2026-03-25': 0.2569, '2026-06-24': 0.2525, '2026-09-23': 0.2665}
rows = []; WHT = 0.15
# 끝값(2026-10-02 종가) 확정치 — 나스닥 원자료(raw/nasdaq_*_20261003b.json)와 야후 10/03 12:5x 재조회가 같음. 처음 받은 야후 값(SPY 769.68·SCHD 32.71·GLD 379.56)은 마감 확정 전 값이라 교체
END = {'SPY': 769.64, 'SCHD': 32.72, 'GLD': 380.14}
dep = {t: float(v) for t, v in c1['정기예금1년_신규_M']}; r = dep['202510']
g = round(P * r / 100); tax = math.floor(g * 0.14 / 10) * 10; tax += math.floor(tax * 0.1 / 10) * 10
rows.append(('정기예금(2025-10 신규 평균 %.2f%%)' % r, P + g, g, 0, tax, P + g - tax))
for s in ['SPY', 'SCHD', 'GLD']:
    p0, p1 = y[s]['px'][S], END.get(s, y[s]['px'][E]); usd = P / f0; sh = usd / p0
    divs = {k: v for k, v in y[s]['div'].items() if S < k <= E}; dv = sh * sum(divs.values()) * f1
    if s == 'SCHD': divs = SCHWAB  # 운용사 원문(슈왑 분배금 표, research/schd1003/schwab_dist.txt) — 야후 3자리 반올림 대신
    dv = sh * sum(divs.values()) * f1
    sale = sh * p1 * f1; gain = sale - P
    cg = max(0, gain - 2_500_000); cgt = math.floor(cg * 0.20) + math.floor(cg * 0.02)
    px_only = sh * p0 * f1  # 가격 그대로, 환율만 바뀐 경우
    dt = math.floor(dv * WHT)  # 분배금 미국 원천징수
    rows.append((s, round(sale), round(gain), round(dv), cgt + dt, round(sale + dv - cgt - dt)))
    print(f'[{s}] 종가 {p0:.2f}→{p1:.2f} ({(p1/p0-1)*100:+.2f}% 달러 기준) · 분배 {len(divs)}회 {sum(divs.values()):.3f}달러/주 · 환율 효과만 {round(px_only-P):,}원 · 원화 매도액 {round(sale):,} · 차익 {round(gain):,} · 분배금(세전) {round(dv):,} · 양도세 {cgt:,} · 분배금 원천징수 15% {dt:,} · 분배금(세후) {round(dv)-dt:,}')
print('\n[영수증] 이름 | 1년 뒤 평가(세전) | 차익 | 분배금(세전) | 세금(양도세+분배금 15%) | 통장(세후)')
for n, a, gg, dv, t, net in sorted(rows, key=lambda x: -x[5]): print(f'  {n} | {a:,} | {gg:,} | {dv:,} | {t:,} | {net:,} ({(net/P-1)*100:+.2f}%)')
# 분배금 세율을 0%·15.4%로 바꿔도 순위가 같은지(지금 값 15%에 더하고 빼서)
for rt in [0, 0.154]:
    rk = sorted(rows, key=lambda x: -(x[5] + x[3] * WHT - x[3] * rt)); print(f'  분배금 세율 {rt*100:.1f}%일 때 순위', [x[0][:6] for x in rk])
print('세전 순위', [x[0][:6] for x in sorted(rows, key=lambda x: -(x[1] + x[3]))])
