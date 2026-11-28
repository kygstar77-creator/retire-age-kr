# krndx1129 — 국내상장 나스닥100 ETF(TIGER 133690) vs QQQ·원달러, 야후 chart API 일봉
import json, urllib.request, datetime, os, sys
UA = {'User-Agent': 'Mozilla/5.0'}
os.makedirs('raw', exist_ok=True)
out = {}
for t in ('QQQ', '133690.KS', '379810.KS', '448300.KS', 'KRW=X', '^NDX'):
    u = f'https://query1.finance.yahoo.com/v8/finance/chart/{t}?period1=1735689600&period2=1796083200&interval=1d'
    j = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30))
    open(f'raw/{t.replace("^","").replace("=","")}_1d.json', 'w', encoding='utf-8').write(json.dumps(j))
    r = j['chart']['result'][0]
    tz = r['meta'].get('gmtoffset', 0)
    ts = [datetime.datetime.utcfromtimestamp(x + tz).date().isoformat() for x in r['timestamp']]
    cl = r['indicators']['quote'][0]['close']
    out[t] = {d: c for d, c in zip(ts, cl) if c}
    ks = sorted(out[t]); print(t, len(ks), ks[0], ks[-1], round(out[t][ks[-1]], 2), 'max', max(out[t].values()))
json.dump(out, open('raw/closes.json', 'w', encoding='utf-8'))
