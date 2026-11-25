# 코스피200 ETF 4종 — 야후 chart(일별 종가·분배 events) + 네이버페이 증권 etfAnalysis. 2026-11-24 받음.
import json, urllib.request, sys
sys.stdout.reconfigure(encoding='utf-8')
T=['069500','102110','148020','105190']
UA={'User-Agent':'Mozilla/5.0'}
for t in T:
    u=f'https://query1.finance.yahoo.com/v8/finance/chart/{t}.KS?period1=946684800&period2=1800000000&interval=1d&events=div'
    d=urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=30).read()
    open(f'raw/{t}.json','wb').write(d)
    j=json.loads(d)['chart']['result'][0]
    print(t,'첫',j['timestamp'][0],'수',len(j['timestamp']),'분배',len(j.get('events',{}).get('dividends',{})))
    try:
        n=urllib.request.urlopen(urllib.request.Request(f'https://m.stock.naver.com/api/stock/{t}/etfAnalysis',headers=UA),timeout=30).read()
        open(f'raw/naver_etfan_{t}_1126.json','wb').write(n)
        nj=json.loads(n); print('  naver', {k:nj.get(k) for k in ('listedDate','totalFee','dividendPerShareTtm','etfBaseIndex','dividendMonthThisYear')})
    except Exception as e: print('  naver fail',e)
