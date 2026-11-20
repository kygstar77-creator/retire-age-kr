# 나스닥100(^NDX) 일별 종가(야후 chart API) — 직전 최고 대비 처음 -15% 닿은 날들과 그 뒤 1년·회복 기간 (2026-11-20 firemap-write)
import urllib.request, json, datetime, os, sys
sys.stdout.reconfigure(encoding='utf-8')
p = 'raw/ndx_max.json'
if not os.path.exists(p) or '--fetch' in sys.argv:
    u = 'https://query1.finance.yahoo.com/v8/finance/chart/%5ENDX?period1=496000000&period2=1800000000&interval=1d'
    d = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=30))
    json.dump(d, open(p, 'w'))
d = json.load(open(p))['chart']['result'][0]
r = [(datetime.datetime.fromtimestamp(a, datetime.UTC).date(), b) for a, b in zip(d['timestamp'], d['indicators']['quote'][0]['close']) if b]
print('기간', r[0][0], '~', r[-1][0], len(r), '거래일')
pk = r[0][1]; pkd = r[0][0]; armed = True; ev = []
for i, (dt, c) in enumerate(r):
    if c > pk: pk, pkd = c, dt; armed = True
    if armed and c <= pk * 0.85:
        armed = False
        j = next((k for k in range(i, len(r)) if r[k][0] >= dt + datetime.timedelta(days=365)), None)
        low = min(r[i:], key=lambda x: x[1]) if False else None
        # 다음 최고 회복일까지 최저
        rec = next((k for k in range(i, len(r)) if r[k][1] >= pk), None)
        seg = r[i:(rec or len(r))]
        lo = min(seg, key=lambda x: x[1])
        ev.append(dict(peak=str(pkd), peakv=round(pk, 1), hit=str(dt), hitv=round(c, 1),
                       y1=(round((r[j][1] / c - 1) * 100, 1) if j else None),
                       low=str(lo[0]), lowdd=round((lo[1] / pk - 1) * 100, 1),
                       rec=(str(r[rec][0]) if rec else None),
                       recdays=((r[rec][0] - dt).days if rec else None)))
for e in ev: print(e)
y = [e['y1'] for e in ev if e['y1'] is not None]
import statistics as s
print('-15% 처음 닿은 횟수', len(ev), '· 1년 뒤 있는 것', len(y), '· 1년 뒤 중간', s.median(y), '· 오른 횟수', sum(v > 0 for v in y))
print('최근', r[-1], '최고', pkd, round(pk, 1), round((r[-1][1] / pk - 1) * 100, 1))
