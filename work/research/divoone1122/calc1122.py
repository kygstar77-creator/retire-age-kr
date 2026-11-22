# divoone1122 — 최근 12개월 분배율 / 가장 큰 한 번이 차지한 몫 / 그 한 번을 다른 회차 평균으로 바꾸면 (write-b 2026-11-21)
import json, datetime, sys, glob
sys.stdout.reconfigure(encoding='utf-8')
T = ['DIVO','JEPI','JEPQ','QYLD','XYLD','SCHD','SPYD','VYM','HDV','DGRO']
D = lambda s: datetime.datetime.utcfromtimestamp(s).date()
for t in T:
    j = json.load(open(f'raw/{t}_chart_20261122.json'))['chart']['result'][0]
    ts = j['timestamp']; cl = j['indicators']['quote'][0]['close']
    last = max(i for i in range(len(ts)) if cl[i] is not None); lastd = D(ts[last]); px = cl[last]
    cut = lastd - datetime.timedelta(days=365)
    dv = sorted((D(int(k)), v['amount']) for k, v in j['events']['dividends'].items())
    ttm = [(d, a) for d, a in dv if cut < d <= lastd]
    s = sum(a for _, a in ttm); n = len(ttm)
    md, ma = max(ttm, key=lambda x: x[1]); oth = (s - ma) / (n - 1)
    print(f'{t}\t종가 {lastd} {px:.2f}\t회차 {n}\t12개월 합 {s:.4f}\t분배율 {s/px*100:.2f}%\t가장 큰 회 {md} {ma:.4f} = 합의 {ma/s*100:.1f}% (고르면 {100/n:.1f}%) · 다른 회 평균의 {ma/oth:.1f}배\t그 회 빼면 {(s-ma)/px*100:.2f}%\t평균으로 바꾸면 {(s-ma+oth)/px*100:.2f}%  차이 {(s/px-(s-ma+oth)/px)*100:.2f}%p')
    print('   ', ' '.join(f'{d.strftime("%y-%m-%d")}:{a:.4f}' for d, a in ttm))
