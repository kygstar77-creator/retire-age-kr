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
# 보강(21:2x): 더 빠진 깊이·회복 날수 중간, 되찾는 데 필요한 상승률, 국내 TIGER 미국나스닥100(원화)
past = [e for e in ev if e['y1'] is not None]
dd = sorted(e['lowdd'] for e in past); rd = sorted(e['recdays'] for e in past)
print('지난 15번 최저 깊이 중간', s.median(dd), '· -20% 넘게', sum(v <= -20 for v in dd), '· -30% 넘게', sum(v <= -30 for v in dd), '· -17% 안', sum(v > -17 for v in dd))
print('지난 15번 -15% 날부터 최고 되찾은 날수 중간', s.median(rd), '일 · 1년 안', sum(v <= 365 for v in rd), '· 최장', max(rd))
print('지금 최고 되찾으려면 필요한 상승률', round((pk / r[-1][1] - 1) * 100, 1))
def rows(f):
    q = json.load(open(f))['chart']['result'][0]
    return {str(datetime.datetime.fromtimestamp(a, datetime.UTC).date()): b for a, b in zip(q['timestamp'], q['indicators']['quote'][0]['close']) if b}
t = rows('raw/tiger_ndx_20261120.json'); k = rows('raw/usdkrw_20261120.json')
tp = max(t.items(), key=lambda x: x[1]); tl = sorted(t.items())[-1]
print('TIGER 미국나스닥100 최고', tp, '마지막', tl, round((tl[1] / tp[1] - 1) * 100, 1), '· 10/6', t['2026-10-06'], round((tl[1] / t['2026-10-06'] - 1) * 100, 1))
print('달러값(야후 KRW=X) 7/1', round(k['2026-07-01'], 1), '11/19', round(k['2026-11-19'], 1))
