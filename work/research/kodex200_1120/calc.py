# kodex200_1120 직접 계산 — KODEX 200(069500) 1억원을 1년·5년 전 종가에 샀다면: 종가만 vs 분배금 포함 vs 코스피200 지수
# 원자료: raw/y_069500.KS.json(야후 종가·분배 events), raw/kodex_divid.json(삼성 분배금 현황), raw/nv_kpi200.txt(네이버 코스피200 지수 일별), raw/kodex_prod.json(삼성 수익률·지수 대조)
import json, re, datetime as dt, sys
sys.stdout.reconfigure(encoding='utf-8')
y = json.load(open('raw/y_069500.KS.json'))['chart']['result'][0]
px = {dt.datetime.fromtimestamp(t).date(): c for t, c in zip(y['timestamp'], y['indicators']['quote'][0]['close']) if c}
days = sorted(px)
t = open('raw/nv_kpi200.txt', encoding='utf-8', errors='ignore').read()
ix = {dt.datetime.strptime(a, '%Y%m%d').date(): float(b) for a, b in re.findall(r'\["(\d{8})",\s*[\d.]+,\s*[\d.]+,\s*[\d.]+,\s*([\d.]+)', t)}
dv = json.load(open('raw/kodex_divid.json', encoding='utf-8'))['dividList']
D = sorted((dt.datetime.strptime(x['basicD'], '%Y%m%d').date(), dt.datetime.strptime(x['payD'], '%Y%m%d').date(), float(x['dividA'])) for x in dv)
# 대조: 야후 events 금액이 삼성 금액과 같은가
ye = sorted((dt.datetime.fromtimestamp(v['date']).date(), v['amount']) for v in y['events']['dividends'].values())
sam = {a: c for a, b, c in D}
print('야후 분배 vs 삼성(최근 8):', [(str(a), m, [s for k, s in sam.items() if abs((k - a).days) <= 5][:1]) for a, m in ye[-8:]])
END = dt.date(2026, 11, 19)
def nd(d): return next(x for x in days if x >= d)
def run(start, label):
    s = nd(start); p0 = px[s]; sh = int(100_000_000 // p0); cash0 = 100_000_000 - sh * p0
    e = END; pe = px[e]
    ds = [(b, p, a) for b, p, a in D if s < b <= e]
    cash = sum(sh * a for b, p, a in ds)
    # 재투자: 지급일 종가에 그날 살 수 있는 만큼(소수 주 허용 — 단순화)
    shr = float(sh)
    for b, p, a in ds:
        if p <= e: shr += shr * 0 + (shr_prev := 0)  # placeholder
    shr = float(sh)
    for b, p, a in ds:
        pp = px[nd(p)] if nd(p) in px else None
        if p <= e and pp: shr += (shr * a) / pp
    ixs = ix[s] if s in ix else ix[max(k for k in ix if k <= s)]; ixe = ix[e]
    val = sh * pe
    print(f'[{label}] 산 날 {s} 종가 {p0:,.0f}원 {sh:,}주(남는 현금 {cash0:,.0f}원) → 끝 {e} 종가 {pe:,.0f}원')
    print(f'  분배 {len(ds)}번 (세전): ' + ', '.join(f'{b}:{a:.0f}' for b, p, a in ds) + f' 합 주당 {sum(a for _,_,a in ds):,.0f}원 · 받은 돈 {cash:,.0f}원')
    print(f'  종가만: 평가 {val+cash0:,.0f}원 · {(val+cash0)/1e8*100-100:.2f}%')
    print(f'  분배금 포함(재투자 안 함): {val+cash0+cash:,.0f}원 · {(val+cash0+cash)/1e8*100-100:.2f}%  (분배금 몫 {cash/1e8*100:.2f}%p)')
    print(f'  분배금 재투자: {shr*pe+cash0:,.0f}원 · {(shr*pe+cash0)/1e8*100-100:.2f}%')
    print(f'  코스피200 지수({s} {ixs} → {ixe}): {ixe/ixs*100-100:.2f}%  (지수는 배당 안 들어간 값)')
    print(f'  종가만 - 지수: {(px[e]/p0-ixe/ixs)*100:.2f}%p · 분배금 포함 - 지수: {((val+cash0+cash)/1e8-ixe/ixs)*100:.2f}%p')
    return s
run(dt.date(2025, 11, 19), '1년')
run(dt.date(2021, 11, 19), '5년')
e = json.load(open('raw/kodex_prod.json', encoding='utf-8'))['suik']['earningRate']
print('삼성 공시 수익률: 1년 기준가격', e['yieldYear1'], '종가', e['clsYieldYear1'], '지수', e['idxYieldYear1'], '| 5년 기준가격', e['yieldYear5'], '종가', e['clsYieldYear5'], '지수', e['idxYieldYear5'])
