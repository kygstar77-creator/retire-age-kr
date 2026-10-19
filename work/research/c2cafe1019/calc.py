# c2cafe1019 새 계산(2026-10-19): 2026년 1월에 3억으로 시작했다면 10월 16일 값으로 통장은?
# C-2와 같은 방식: 연말 지수 × 연말 환율, 1월 초 1년 치 2,400만원 매도. 첫해라 판 이익이 거의 없어 세금 0으로 둠.
import json, datetime
r = json.load(open('raw/yahoo_SP500TR_1y_1019.json'))['chart']['result'][0]
px = {datetime.datetime.fromtimestamp(t, datetime.UTC).date().isoformat(): v for t, v in zip(r['timestamp'], r['indicators']['quote'][0]['close']) if v}
fx = {d: float(v) for d, v, _ in json.load(open('raw/ecos_731Y001_D_1019.json', encoding='utf-8'))}
p0, p1 = px['2025-12-31'], px['2026-10-16']
f0 = 1434.9            # 2025년 연말 원/달러(ECOS 731Y004 연, C-2 raw와 같은 값)
f1 = fx['20261016']    # ECOS 731Y001 일별 매매기준율
usd = p1 / p0 - 1; fxc = f1 / f0 - 1; krw = (1 + usd) * (1 + fxc) - 1
left = 300_000_000 - 24_000_000
now = left * (1 + krw)
out = [f'S&P500 총수익 지수 2025-12-31 {p0:.2f} → 2026-10-16 {p1:.2f} : 달러 {usd*100:+.1f}%',
       f'원/달러 2025 연말 {f0} → 2026-10-16 {f1} : {fxc*100:+.1f}%',
       f'원화 수익률 {krw*100:+.1f}%',
       f'3억 - 1월 2,400만원 = {left/1e8:.2f}억 → 10/16 {now/1e8:.4f}억 · 처음 3억과 차이 {(now-3e8)/1e4:,.0f}만원',
       f'규칙(1월 통장 < 3억이면 그해 월 100만원): 10/16 값 그대로면 {"해당" if now < 3e8 else "아님"}']
print('\n'.join(out)); open('calc_out.txt', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
