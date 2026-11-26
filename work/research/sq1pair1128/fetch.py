# sq1pair1128 — 영상(10/30 끝) 뒤 한 달: QQQ·SCHD 일봉 수정종가 2026-10-30 → 최근 거래일 (야후 chart API)
import json, urllib.request, datetime, os
UA = {'User-Agent': 'Mozilla/5.0'}
os.makedirs('raw', exist_ok=True)
out = {}
for t in ('QQQ', 'SCHD'):
    u = f'https://query1.finance.yahoo.com/v8/finance/chart/{t}?period1=1761609600&period2=1796083200&interval=1d&events=div'
    j = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30))
    open(f'raw/{t}_1d.json', 'w', encoding='utf-8').write(json.dumps(j))
    r = j['chart']['result'][0]
    ts = [datetime.datetime.utcfromtimestamp(x).date().isoformat() for x in r['timestamp']]
    adj = r['indicators']['adjclose'][0]['adjclose']; cl = r['indicators']['quote'][0]['close']
    divs = r.get('events', {}).get('dividends', {})
    out[t] = dict(ts=ts, adj=adj, close=cl, divs={datetime.datetime.utcfromtimestamp(int(k)).date().isoformat(): v['amount'] for k, v in divs.items()})
for t, d in out.items():
    i0 = d['ts'].index('2026-10-30')
    print(t, '10/30', round(d['close'][i0], 2), '→', d['ts'][-1], round(d['close'][-1], 2), '수정종가 변화 %.2f%%' % ((d['adj'][-1] / d['adj'][i0] - 1) * 100), '분배', {k: v for k, v in d['divs'].items() if k >= '2026-10-31'})
rq = out['QQQ']['adj'][-1] / out['QQQ']['adj'][out['QQQ']['ts'].index('2026-10-30')]
rs = out['SCHD']['adj'][-1] / out['SCHD']['adj'][out['SCHD']['ts'].index('2026-10-30')]
for name, s in (('SCHD 100%', 1.0), ('SCHD 50%', .5), ('SCHD 0%', 0.0)):
    end = {'SCHD 100%': 6.77, 'SCHD 50%': 10.10, 'SCHD 0%': 13.56}[name]
    print(f'15년 달러 기준 {name}: 10/30 {end:.2f}억 → {out["QQQ"]["ts"][-1]} {end*(s*rs+(1-s)*rq):.2f}억 (10/30 비율 그대로, 리밸런싱 없음)')
