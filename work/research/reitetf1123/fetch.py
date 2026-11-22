# 야후 일별 종가·분배 받기(2026-11-22 write-b). 사용: py -3.12 fetch.py
import json,urllib.request,datetime,sys,time
sys.stdout.reconfigure(encoding='utf-8')
for t in ['429740.KS','329200.KS','476800.KS','182480.KS','VNQ']:
    u=f'https://query1.finance.yahoo.com/v8/finance/chart/{t}?period1=1546300800&period2={int(time.time())}&interval=1d&events=div'
    d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=30))
    open(f'raw/{t}.json','w').write(json.dumps(d))
    r=d['chart']['result'][0]; ts=r['timestamp']; c=r['indicators']['quote'][0]['close']
    dv=r.get('events',{}).get('dividends',{})
    print(t, datetime.date.fromtimestamp(ts[0]), datetime.date.fromtimestamp(ts[-1]), c[-1], 'divs',len(dv))
    ds=sorted(dv.values(),key=lambda x:x['date'])[-13:]
    print('  ',[(str(datetime.date.fromtimestamp(x['date'])),round(x['amount'],2)) for x in ds])
