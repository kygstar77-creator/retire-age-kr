# bankdiv1015 자료 받기 — 야후 일별 종가(KRX) + DART 배당에 관한 사항(2025 사업보고서)
import json, sys, urllib.request, urllib.parse, io, zipfile, re
sys.path.insert(0, '../../')
import apis
T = {'KB금융': '105560', '신한지주': '055550', '하나금융지주': '086790', '우리금융지주': '316140', 'BNK금융지주': '138930'}
out = {}
for n, c in T.items():
    u = f'https://query1.finance.yahoo.com/v8/finance/chart/{c}.KS?range=1mo&interval=1d'
    r = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
    j = json.load(urllib.request.urlopen(r, timeout=25))
    res = j['chart']['result'][0]
    import datetime
    ts = [datetime.datetime.fromtimestamp(t + 9 * 3600, datetime.UTC).strftime('%m-%d') for t in res['timestamp']]
    cl = res['indicators']['quote'][0]['close']
    out[n] = {'code': c, 'close': dict(zip(ts, cl))}
    print(n, list(zip(ts, cl))[-4:])
json.dump(out, open('src/yahoo.json', 'w', encoding='utf-8'), ensure_ascii=False)
