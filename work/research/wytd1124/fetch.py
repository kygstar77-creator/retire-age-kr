# wytd1124: 야후 차트 API 일봉(2025-12-01~) 받아 raw/<T>.json 저장
import json, urllib.request, urllib.parse, os, sys, time
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
T = ['^GSPC', '^NDX', '^KS11', '^N225', '^STOXX50E', 'KRW=X', 'JPYKRW=X', 'EURKRW=X', '^SP500TR']
p1 = int(time.mktime((2025, 12, 1, 0, 0, 0, 0, 0, 0))); p2 = int(time.time())
for t in T:
    u = 'https://query1.finance.yahoo.com/v8/finance/chart/' + urllib.parse.quote(t) + f'?period1={p1}&period2={p2}&interval=1d'
    r = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=30).read()
    open(os.path.join(HERE, 'raw', t.replace('^', '').replace('=', '_') + '.json'), 'wb').write(r)
    print(t, len(r))
