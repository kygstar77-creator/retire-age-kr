# k1s_us 올리기 전 확인용 — 최신 월평균(미국 10년 GS10·한국 10년/3년 ECOS 721Y001) 다시 받기 (PD 11/14)
import sys, json, urllib.request, datetime
sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work'); sys.stdout.reconfigure(encoding='utf-8')
import apis
K = apis.key('ecos'); F = apis.key('fred')
def ecos(item):
    u = f'https://ecos.bok.or.kr/api/StatisticSearch/{K}/json/kr/1/1000/721Y001/M/202409/202612/{item}'
    return {r['TIME']: float(r['DATA_VALUE']) for r in json.load(urllib.request.urlopen(u, timeout=40))['StatisticSearch']['row']}
def fred(sid):
    u = f'https://api.stlouisfed.org/fred/series/observations?series_id={sid}&api_key={F}&file_type=json&observation_start=2024-09-01'
    return {o['date'][:4]+o['date'][5:7]: float(o['value']) for o in json.load(urllib.request.urlopen(u, timeout=40))['observations'] if o['value'] != '.'}
S = dict(us=fred('GS10'), kr10=ecos('5050000'), kr3=ecos('5020000'))
json.dump(S, open('fresh_%s.json' % datetime.date.today().strftime('%Y%m%d'), 'w'), indent=0)
for k, v in S.items(): print(k, '끝', max(v), {m: v[m] for m in sorted(v) if m >= '202508'})
for a, b in (('202509', '202609'), ('202510', '202610')):
    if all(b in v and a in v for v in S.values()):
        print(a, '→', b, {k: f'{v[a]}→{v[b]} ({v[b]-v[a]:+.2f}%p)' for k, v in S.items()})
