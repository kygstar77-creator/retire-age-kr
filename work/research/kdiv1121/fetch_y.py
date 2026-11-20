# 2차 씨앗: 야후 분배 events — 국내 고배당 ETF 같은 갈래(11/20 firemap-write)
import json, urllib.request, datetime as D, sys
sys.stdout.reconfigure(encoding='utf-8')
T={'161510.KS':'PLUS 고배당주','279530.KS':'KODEX 고배당주(?)','458730.KS':'(확인용)','211560.KS':'TIGER 배당성장(?)','0105E0.KS':'(?)'}
import re
for t in sys.argv[1:]:
    u=f'https://query1.finance.yahoo.com/v8/finance/chart/{t}?range=3y&interval=1d&events=div'
    try:
        d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=20))
    except Exception as e: print(t,'ERR',e); continue
    r=d['chart']['result'][0]; json.dump(d,open(f'raw/y_{t}.json','w'))
    ev=sorted((int(k),v['amount']) for k,v in r.get('events',{}).get('dividends',{}).items())
    print(t, r['meta'].get('longName'), r['meta'].get('regularMarketPrice'), r['meta'].get('fiftyTwoWeekHigh'))
    print('   ', ' '.join(f"{D.date.fromtimestamp(k):%y%m}:{v:g}" for k,v in ev[-26:]))
