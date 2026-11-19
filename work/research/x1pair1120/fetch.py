# x1pair1120 원자료 받기 — ECOS 731Y001(원/달러 매매기준율, 일) · 야후 SPY 일별 종가
import sys, json, time, urllib.request
sys.path.insert(0, r'C:/Users/강영준/Documents/GitHub/retire-age-kr/work')
import apis
stamp = time.strftime('%Y%m%d')
k = apis.key('ecos')
u = f'https://ecos.bok.or.kr/api/StatisticSearch/{k}/json/kr/1/1000/731Y001/D/20250101/{stamp}/0000001'
d = json.loads(urllib.request.urlopen(u, timeout=30).read().decode('utf-8'))
rows = d['StatisticSearch']['row']
fx = {r['TIME']: float(r['DATA_VALUE']) for r in rows}
json.dump(fx, open(f'raw/ecos_usd_{stamp}.json', 'w'), ensure_ascii=False, indent=0)
print('ECOS', len(fx), min(fx), max(fx), fx[max(fx)])
req = urllib.request.Request('https://query1.finance.yahoo.com/v8/finance/chart/SPY?range=2y&interval=1d', headers={'User-Agent': 'Mozilla/5.0'})
y = json.loads(urllib.request.urlopen(req, timeout=30).read())
r = y['chart']['result'][0]
ts = r['timestamp']; cl = r['indicators']['quote'][0]['close']
spy = {time.strftime('%Y%m%d', time.gmtime(t - 4*3600)): c for t, c in zip(ts, cl) if c}
json.dump(spy, open(f'raw/yahoo_SPY_{stamp}.json', 'w'), indent=0)
print('SPY', len(spy), max(spy), spy[max(spy)])
